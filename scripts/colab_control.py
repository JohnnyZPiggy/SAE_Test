"""Bounded existing-CLI orchestration; imports never allocate a session."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

from environment_preflight import PreflightError, preflight, resolve_cli, diagnostic_python


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-sha', required=True)
    p.add_argument('--run-id', required=True)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--cli', default='colab', help='Executable verified in this shell context')
    p.add_argument('--device', choices=['T4', 'L4', 'G4', 'A100', 'H100'], default='T4')
    p.add_argument('--task-seconds', type=float, default=5400)
    p.add_argument('--allocation-seconds', type=float, default=600)
    p.add_argument('--cleanup-seconds', type=float, default=60)
    p.add_argument('--kernel-timeout', type=float, default=30)
    p.add_argument('--work-timeout', type=float, default=240)
    p.add_argument('--temp-root', type=Path)
    p.add_argument('--diagnostic', action='store_true', help='Opt-in process-local HTTP/stack diagnostics')
    p.add_argument('--diagnostic-python', help='CLI environment Python; otherwise verified CLI shebang')
    p.add_argument('--preflight-only', action='store_true', help='Never invoke sessions/new/exec')
    p.add_argument('--install-local', action='store_true', help='Explicit no-deps install of exact export in temp')
    return p


def utc():
    return datetime.now(timezone.utc).isoformat()


def run(args):
    start = time.monotonic()
    task_deadline = start + args.task_seconds
    report = {'status': 'FAIL',
              'source_sha': args.source_sha if re.fullmatch(r'[0-9a-f]{40}', args.source_sha) else None,
              'run_id': args.run_id if re.fullmatch(r'[a-z0-9][a-z0-9-]{0,39}', args.run_id) else None,
              'created': False, 'cleanup_confirmed': False, 'utc_start': utc(), 'commands': [],
              'classification': 'PREFLIGHT_ONLY' if args.preflight_only else 'LIVE_REQUESTED',
              'events': {name: None for name in ('cli_resolution', 'environment_preflight', 'snapshot_extraction',
                         'wheel_pip_install', 'first_cpu_pass', 'exact_pinned_cpu_test',
                         'kernel_probe', 'remote_workload', 'artifact_download',
                         'github_publication', 'cleanup')},
              'per_attempt_approvals_actual': None, 'api_escalation_requests_actual': None,
              'handoffs_actual': None}
    attempted, owns_out = False, False
    allocation_start = None
    work_deadline = task_deadline - args.cleanup_seconds
    cleanup_deadline = task_deadline
    session = 'sae-' + args.run_id
    cli_path, diagnostic = None, None
    scripts = Path(__file__).resolve().parent

    def cli(*cmd, timeout=30, cleanup=False, slots=1):
        remaining = (cleanup_deadline if cleanup else work_deadline) - time.monotonic()
        if remaining <= 0:
            raise PreflightError('CLEANUP_BUDGET_EXPIRED' if cleanup else 'TIME_BUDGET_EXPIRED')
        timeout = min(timeout, remaining / slots)
        tick = time.monotonic()
        code, output, status = -1, '', 'FAIL'
        try:
            prefix = [cli_path]
            if args.diagnostic and cmd[0] == 'exec':
                prefix = [diagnostic, str(scripts / 'colab_entry.py')]
            result = subprocess.run([*prefix, '--auth=oauth2', *map(str, cmd)],
                                    stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)
            code, output = result.returncode, result.stdout + result.stderr
            status = 'PASS' if code == 0 else 'FAIL'
        except subprocess.TimeoutExpired:
            status = 'TIMEOUT'
        except OSError:
            status = 'EXECUTABLE_FAILED'
        finally:
            # Raw output/argv may contain credentials, session URLs or private paths.
            report['commands'].append({'operation': cmd[0], 'status': status, 'exit_code': code,
                                       'timeout_seconds': timeout, 'elapsed_seconds': time.monotonic() - tick})
        return code, output

    def step(name, action):
        tick = time.monotonic()
        report['events'][name] = {'utc_start': utc(), 'status': 'FAIL'}
        try:
            value = action()
            report['events'][name]['status'] = 'PASS'
            return value
        finally:
            report['events'][name].update(utc_end=utc(), elapsed_seconds=time.monotonic() - tick)

    try:
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,39}', args.run_id):
            raise PreflightError('INVALID_RUN_ID')
        if not re.fullmatch(r'[0-9a-f]{40}', args.source_sha):
            raise PreflightError('INVALID_SOURCE_SHA')
        if not (0 < args.cleanup_seconds < args.allocation_seconds <= 2700
                and args.allocation_seconds <= args.task_seconds <= 5400
                and 0 < args.kernel_timeout <= 60 and 0 < args.work_timeout <= 420):
            raise PreflightError('INVALID_TIMEOUT_BOUNDS')
        args.out.mkdir(parents=True, exist_ok=False)
        owns_out = True
        cli_path = step('cli_resolution', lambda: resolve_cli(args.cli))
        if args.diagnostic:
            diagnostic = diagnostic_python(cli_path, args.diagnostic_python)
        report['transport_script_sha256'] = {name: hashlib.sha256((scripts / name).read_bytes()).hexdigest()
            for name in ('colab_control.py', 'colab_entry.py', 'kernel_smoke.py', 'colab_remote.py')}
        report['preflight'] = step('environment_preflight', lambda: preflight(
            scripts.parent, args.source_sha, cli_path, args.temp_root, args.install_local,
            deadline=work_deadline))
        for key in ('snapshot_extraction', 'wheel_pip_install'):
            report['events'][key] = report['preflight']['events'][key]
        if args.preflight_only:
            report['status'] = 'PREFLIGHT_PASS'
            return report
        code, sessions = cli('sessions')
        if code or 'No active sessions found on server.' not in sessions:
            raise PreflightError('EXISTING_OR_UNKNOWN_SESSIONS')
        code, usage = cli('usage')
        balance = re.search(r'Current balance:\s*([0-9.]+) compute units', usage)
        if code or not balance or float(balance[1]) <= 0 or not re.search(r'Active assignments:\s*0\b', usage):
            raise PreflightError('ENTITLEMENT_NOT_ESTABLISHED')
        report['balance_before'] = float(balance[1])
        (args.out / 'allocation_attempted.lock').touch(exist_ok=False)
        attempted = True
        allocation_start = time.monotonic()
        cleanup_deadline = min(task_deadline, allocation_start + args.allocation_seconds)
        work_deadline = cleanup_deadline - args.cleanup_seconds
        code, _ = cli('new', '-s', session, '--gpu', args.device, timeout=120)
        if code:
            raise PreflightError('ALLOCATION_FAILED')
        report['created'] = True

        def probe():
            code, output = cli('exec', '-s', session, '-f', scripts / 'kernel_smoke.py',
                               '--timeout', args.kernel_timeout, timeout=args.kernel_timeout + 5)
            if code or not re.search(r'^KERNEL_REACHABLE\s*$', output, re.MULTILINE):
                raise PreflightError('KERNEL_PROBE_FAILED')
        step('kernel_probe', probe)

        def workload():
            code, output = cli('exec', '-s', session, '-f', scripts / 'colab_remote.py',
                               '--timeout', args.work_timeout, '--env', 'SAE_SOURCE_SHA=' + args.source_sha,
                               timeout=args.work_timeout + 5)
            if code:
                raise PreflightError('WORK_EXEC_FAILED')
            return output
        execution = step('remote_workload', workload)

        def download():
            for name in ('gpu-probe.json', 'gpu-result.json', 'tpu-availability.json'):
                code, _ = cli('download', '-s', session, '/content/' + name, args.out / name)
                if code:
                    raise PreflightError('DOWNLOAD_FAILED')
                raw = (args.out / name).read_bytes()
                match = re.search(r'ARTIFACT\s+' + re.escape(name) + r'\s+(\d+)\s+([0-9a-f]{64})', execution)
                if not match or len(raw) != int(match[1]) or hashlib.sha256(raw).hexdigest() != match[2]:
                    raise PreflightError('ARTIFACT_INTEGRITY_FAILED')
                data = json.loads(raw)
                if name != 'tpu-availability.json' and (data['source_sha'] != args.source_sha
                        or data['status'] != 'PASS' or data['environment']['device'] != 'cuda'):
                    raise PreflightError('ARTIFACT_SOURCE_OR_STATUS_FAILED')
                report.setdefault('artifact_sha256', {})[name] = hashlib.sha256(raw).hexdigest()
        step('artifact_download', download)
        report['status'] = 'PASS'
    except BaseException as exc:
        report['error'] = exc.code if isinstance(exc, PreflightError) else (
            'INTERRUPTED' if isinstance(exc, KeyboardInterrupt) else 'LOCAL_OPERATION_FAILED')
        if isinstance(exc, PreflightError) and exc.report:
            report['preflight'] = exc.report
            for key in ('snapshot_extraction', 'wheel_pip_install'):
                report['events'][key] = exc.report['events'].get(key)
    finally:
        tick = time.monotonic()
        if attempted:
            report['events']['cleanup'] = {'utc_start': utc(), 'status': 'FAIL'}
            for attempt in range(2):
                try:
                    code, _ = cli('stop', '-s', session, timeout=15, cleanup=True, slots=4 - attempt * 2)
                    verify, listing = cli('sessions', timeout=15, cleanup=True, slots=3 - attempt * 2)
                    if code == 0 and verify == 0 and 'No active sessions found on server.' in listing:
                        report['cleanup_confirmed'] = True
                        report['utc_cleanup_verified'] = utc()
                        report['events']['cleanup']['status'] = 'PASS'
                        break
                except (PreflightError, OSError, KeyboardInterrupt):
                    continue
            report['allocation_lifecycle_seconds'] = time.monotonic() - allocation_start
            report['events']['cleanup'].update(utc_end=utc(), elapsed_seconds=time.monotonic() - tick)
            if not report['cleanup_confirmed']:
                report['status'] = 'CLEANUP_FAILED'
        report.update(cleanup_seconds=time.monotonic() - tick,
                      total_seconds=time.monotonic() - start, utc_end=utc())
        if owns_out:
            with (args.out / 'colab-control.json').open('x', encoding='utf-8', newline='\n') as handle:
                json.dump(report, handle, indent=2)
                handle.write('\n')
    return report


if __name__ == '__main__':
    result = run(parser().parse_args())
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['status'] in ('PASS', 'PREFLIGHT_PASS') else 1)

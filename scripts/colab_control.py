"""One bounded allocation; cleanup in finally, including partial new failures."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--source-sha', required=True)
p.add_argument('--out', required=True)
p.add_argument('--diagnostic', action='store_true')
args = p.parse_args()
out = Path(args.out).resolve()
out.mkdir(parents=True, exist_ok=True)
session = 'sae37-range-20261020'
start = time.monotonic()
report = {'status':'FAIL','source_sha':args.source_sha,'created':False,'cleanup_confirmed':False,
          'utc_start':datetime.now(timezone.utc).isoformat(), 'commands':[]}
allocation_start = None
deadline = None
attempted = False


def cli(*cmd, timeout=30, check=True, cleanup=False):
    if deadline is not None and not cleanup:
        timeout = min(timeout, max(1, deadline-time.monotonic()))
        if time.monotonic() >= deadline:
            raise TimeoutError('Allocation deadline reached')
    t = time.monotonic()
    try:
        prefix = (['/home/zhangru/.local/share/uv/tools/google-colab-cli/bin/python',
                   str(Path(__file__).with_name('colab_entry.py'))]
                  if args.diagnostic and cmd[0] == 'exec' else ['colab'])
        r = subprocess.run([*prefix,'--auth=oauth2',*cmd], text=True, capture_output=True, timeout=timeout)
        code, output = r.returncode, r.stdout+r.stderr
    except subprocess.TimeoutExpired as exc:
        partial = (exc.stdout or b'') + (exc.stderr or b'')
        if isinstance(partial, bytes):
            partial = partial.decode(errors='replace')
        code, output = -1, 'TIMEOUT\n' + partial
    # Keep only sanitized execution evidence; never publish auth/session URLs.
    output = re.sub(r'https?://\S+', '[URL_REDACTED]', output)
    output = re.sub(r'(?i)((?:access_token|refresh_token|authorization|token|code)[\s"\x27:=]+)\S+', r'\1[REDACTED]', output)
    report['commands'].append({'command':list(cmd),'exit_code':code,'elapsed_seconds':time.monotonic()-t,'output':output})
    print(cmd[0], 'exit', code, flush=True)
    if check and code:
        raise RuntimeError(f'{cmd[0]} exit {code}: {output[-1200:]}')
    return code, output


try:
    assert datetime.now(timezone.utc) < datetime(2026,10,20,14,30,tzinfo=timezone.utc), 'Reserve cleanup/publication before task ceiling'
    marker = out/'allocation_attempted.lock'
    assert not marker.exists(), 'Refuse accidental duplicate allocation'
    _, sessions = cli('sessions')
    assert 'No active sessions found on server.' in sessions, 'Existing sessions: do not interfere'
    _, usage = cli('usage')
    balance = re.search(r'Current balance:\s*([0-9.]+) compute units', usage)
    assert balance and float(balance[1]) > 0 and re.search(r'Active assignments:\s*0\b',usage), 'Existing entitlement not established'
    report['usage_before'] = usage
    marker.touch(exist_ok=False)
    attempted = True
    allocation_start = time.monotonic()
    deadline = allocation_start + 600
    cli('new','-s',session,'--gpu','T4',timeout=120)
    report['created'] = True
    if args.diagnostic:
        _, smoke = cli('exec','-s',session,'-f',str(Path(__file__).with_name('kernel_smoke.py')),
                       '--timeout','30',timeout=75)
        assert 'KERNEL_REACHABLE' in smoke, 'Kernel smoke did not execute'
    _, execution = cli('exec','-s',session,'-f',str(Path(__file__).with_name('colab_remote.py')),
                       '--timeout','420','--env','SAE_SOURCE_SHA='+args.source_sha,timeout=440)
    for name in ('gpu-probe.json','gpu-result.json','tpu-availability.json'):
        cli('download','-s',session,'/content/'+name,str(out/name),timeout=30)
        raw = (out/name).read_bytes()
        match = re.search(r'ARTIFACT\s+'+re.escape(name)+r'\s+(\d+)\s+([0-9a-f]{64})',execution)
        assert match and len(raw)==int(match[1]) and hashlib.sha256(raw).hexdigest()==match[2], 'Artifact integrity mismatch '+name
        data = json.loads(raw)
        if name != 'tpu-availability.json':
            assert data['source_sha'] == args.source_sha and data['status']=='PASS'
            assert data['environment']['device']=='cuda'
        report.setdefault('artifact_sha256',{})[name] = hashlib.sha256(raw).hexdigest()
    report['status'] = 'PASS'
    report['utc_first_gpu_evidence'] = json.loads((out/'gpu-probe.json').read_text())['utc_end']
except BaseException as exc:
    report['error'] = f'{type(exc).__name__}: {exc}'
    print(report['error'],flush=True)
finally:
    cleanup_start = time.monotonic()
    if attempted:
        for _ in range(2):
            try:
                cli('stop','-s',session,timeout=30,check=False,cleanup=True)
                code, sessions = cli('sessions',timeout=20,check=False,cleanup=True)
                if code==0 and 'No active sessions found on server.' in sessions:
                    report['cleanup_confirmed'] = True
                    report['utc_cleanup_verified'] = datetime.now(timezone.utc).isoformat()
                    break
            except Exception as exc:
                report['cleanup_error'] = str(exc)
        report['allocation_lifecycle_seconds'] = time.monotonic()-allocation_start
        if not report['cleanup_confirmed']:
            report['status'] = 'CLEANUP_FAILED'
    report['cleanup_seconds'] = time.monotonic()-cleanup_start
    try:
        _, report['usage_after'] = cli('usage',timeout=20,check=False,cleanup=True)
    except Exception as exc:
        report['usage_after_error'] = str(exc)
    report['total_seconds'] = time.monotonic()-start
    report['utc_end'] = datetime.now(timezone.utc).isoformat()
    (out/'colab-control.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='commands'},indent=2),flush=True)

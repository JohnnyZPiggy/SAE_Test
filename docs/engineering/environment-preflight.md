# Environment Preflight and Colab Fast Start (Issue 2)

This modifies the existing controller; it is not a new runner service. No algorithm, `colab_remote.py`, `kernel_smoke.py`, historical run evidence or pinned `.sae/` content changes. No Actions, scheduler, installation/login fallback or approval gate is added.

From the repository root, in the same shell that will run the controller (for WSL, use the already configured login shell):

```sh
python3 scripts/colab_control.py --preflight-only --cli colab \
  --source-sha 77b1027aaaa89ad0f08919b3c96cff41da299030 \
  --run-id local-check-001 --out reports/local-check-001
```

This calls only CLI `version` and local Git/filesystem operations. It never calls `sessions`, `usage`, `new`, `exec` or authentication. `--cli` accepts a verified executable or resolves PATH in that exact shell; failure stops with a sanitized code instead of guessing a developer home, installing software or prompting for login. Use a fresh run ID/output directory each time. An existing output directory is refused without modifying it.

Preflight verifies a full immutable commit SHA, records whether the local tree is dirty, exports exact blobs using `git ls-tree`/`cat-file --batch`, and preserves LF/CRLF and binary bytes independently of checkout/archive conversion. Symlinks, submodules and unsafe export paths are rejected. It checks writable temp/build/cache directories outside the checkout and Dropbox. `--temp-root` can select another non-synced OS-local directory; no global pip/environment/permission setting is changed. Default preflight does not install anything. Explicit `--install-local` builds/installs the exact export into temporary staging using existing Python/pip/build dependencies, `--no-deps --no-build-isolation --no-cache-dir`; failure is reported and no speculative dependency installation occurs. Temporary staging is removed on return.

Live execution is a separate invocation: omit `--preflight-only` only in a separately authorized compute task. CLI options are `--run-id`, `--source-sha`, `--out`, `--device` (GPU variant, default T4), `--task-seconds` (max 5400), `--allocation-seconds` (default 600, max 2700), `--cleanup-seconds` (default 60), `--kernel-timeout` (default 30, max 60), `--work-timeout` (default 240, max 420). The unchanged scientific driver is CUDA-only; this change adds no CPU/TPU runner.

After provider zero-session/positive-entitlement checks, one `new` is attempted. Every fresh allocation now runs the existing `kernel_smoke.py` before `colab_remote.py`, without diagnostics by default. The probe gets its configured remote timeout plus at most 5 seconds for CLI startup, capped by the remaining main budget. Missing marker/error/timeout produces `KERNEL_PROBE_FAILED` and cleanup immediately; no workload runs. This shortens the connection diagnosis window, but cannot prevent later workload hangs or prove why the earlier pilot hung.

Work subprocesses use the smaller of their timeout and remaining allocation/task budget after reserving cleanup. The cleanup reserve stays available after main-budget exhaustion: at most two stop+server-verification pairs share the remaining cleanup deadline. A partial `new` failure or interrupt also enters cleanup. PASS requires successful stop and server-confirmed zero active sessions. Otherwise status is `CLEANUP_FAILED`; no overlapping allocation or indefinite retry is attempted. A provider/network failure can still prevent release; the controller reports that failure rather than claiming cleanup.

`--diagnostic` is explicit opt-in. Its Python is resolved from the CLI Python shebang or explicit `--diagnostic-python`; no developer-home path is embedded. Only that child process temporarily bounds requests timeouts and enables a stack dump; hooks are restored on exit. The controller's external subprocess timeout supplies the total bound (an HTTP read timeout alone is not a total runtime limit). Missing interpreter support blocks instead of silently switching environments. No automatic causal claim or diagnostic retry is made.

The report keeps prior status/source/command-duration fields and adds UTC/monotonic per-step events, CLI/source/temp checks and transport-script hashes. Unobserved CPU/package-install/publication events and human approval/handoff counts remain `null`. A SHA label is not trusted proof: the exact export/source identity and local dirty state are explicit; transport scripts can differ from the candidate and have separate hashes. Raw subprocess output/arguments are not saved because they can contain OAuth URLs, credentials or private paths. Safe failure codes preserve diagnosis without publishing those values. Publication is separate; a GitHub receipt may supply its observed timestamp afterward.

Engineering-only tests (no installed Colab invocation):

```sh
python -m unittest discover -s tests -p test_environment_preflight.py -v
python -m unittest discover -s tests -p test_colab_control.py -v
```

These use real temporary Git repositories plus fake CLI/pip responses, a deterministic clock and one real sleeping local Python child to exercise external timeout termination. They do not rerun the numerical CPU oracle or establish live CPU/GPU/TPU support. Live Colab fast start remains NOT RUN for this change.

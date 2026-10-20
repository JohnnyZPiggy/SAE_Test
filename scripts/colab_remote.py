"""Run only exact committed source; this script performs no GitHub writes."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sha = os.environ['SAE_SOURCE_SHA']
assert len(sha) == 40 and all(c in '0123456789abcdef' for c in sha)
source = f'git+https://github.com/JohnnyZPiggy/SAE_Test.git@{sha}'
subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-deps', '--no-build-isolation', source], check=True, timeout=180)
import importlib.metadata
dist = importlib.metadata.distribution('torch-rand-range-lab')
direct = json.loads(dist.read_text('direct_url.json'))
assert direct['vcs_info']['commit_id'] == sha
for name, extra in [('gpu-probe.json', ['--probe-only']), ('gpu-result.json', [])]:
    subprocess.run([sys.executable, '-m', 'torch_rand_range_lab.benchmarks.run',
                    '--device', 'cuda', '--source-sha', sha,
                    '--output', '/content/' + name, *extra], check=True, timeout=180)
    raw = Path('/content/' + name).read_bytes()
    assert json.loads(raw)['status'] == 'PASS'
    print('ARTIFACT', name, len(raw), hashlib.sha256(raw).hexdigest(), flush=True)

# A GPU allocation is not a TPU allocation. Do not install XLA speculatively.
import importlib.util
tpu = {'status': 'NOT_RUN', 'classification': 'PROBE_ONLY',
       'reason': 'No TPU allocated in the one GPU session; TPU/XLA QR not executed',
       'torch_xla_installed': importlib.util.find_spec('torch_xla') is not None,
       'tpu_environment_present': any(os.environ.get(k) for k in ('TPU_NAME','TPU_WORKER_ID','COLAB_TPU_ADDR'))}
Path('/content/tpu-availability.json').write_text(json.dumps(tpu, indent=2)+'\n')
raw = Path('/content/tpu-availability.json').read_bytes()
print('ARTIFACT', 'tpu-availability.json', len(raw), hashlib.sha256(raw).hexdigest(), flush=True)
print('REMOTE_COMPLETE', sha, flush=True)

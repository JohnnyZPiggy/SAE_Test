# Issue 37 engineering handoff

Target: JohnnyZPiggy/SAE_Test, branch feat/37-lean-lab-pilot. Framework 3fa17c605fbd3389439eee8bf016305632fb25ab. Exact candidate dc055f42ea9d7f5318cc52b936305cfa3c733fc2. Primary coordination: https://github.com/JohnnyZPiggy/SAE-Framework/issues/37.

The installable package exposes range_basis(A,Omega), loop_basis(A,Omega), project(A,Q) and `python -m torch_rand_range_lab.benchmarks.run`. All numerical run values live in the linked [pilot report](../../reports/pilot-20261020/summary.md), not duplicated here. The scoped [mathematical rationale](../research/range-finder-tensorization.md) states assumptions and limits; independent GPT readiness/acceptance is pending.

NATIVE_REUSE: torch matmul + reduced QR suffice. NumPy supplies benchmark input hashing through tensor interop; setuptools builds packaging. Final review corrected dependency metadata to declare NumPy, already present during the runs. All algorithm/test Python files remain byte-identical to the tested candidate; report/orchestration/metadata changes are distinguished from its SHA. The reference loops over independent matrices; tensor version uses batched native operations. No custom CUDA, power iteration, learned model, approximate rank selection or novelty claim.

Tests cover three exact rank16 seeds, slow/full-rank diagnostic, projection agreement, orthogonality, finite values, zero matrices/sketches, singleton, wide matrices, float64, single matrix, empty batch, dimension/dtype/sketch rejection. CPU tests use 2 threads, float32 first; randomized fixtures explicitly originate on CPU. Both implementations get the same tensors/Omega on each device. QR bases themselves are not compared. Timing includes matmul and QR, excludes projection, input generation and transfer. Two warmup calls and seven alternating-order samples are recorded per implementation and workload. First timed call is reported separately after correctness: it is not fresh-process kernel startup latency.

Reproduce after installing the exact candidate:

```sh
python -m pip install --no-deps --no-build-isolation git+https://github.com/JohnnyZPiggy/SAE_Test.git@dc055f42ea9d7f5318cc52b936305cfa3c733fc2
python -m torch_rand_range_lab.benchmarks.run --device cpu --source-sha dc055f42ea9d7f5318cc52b936305cfa3c733fc2 --output cpu-result.json
```

The source SHA argument labels a run; CLI alone does not authenticate provenance. This pilot's local install extracted package/tests directly from Git objects and the remote driver asserts pip direct_url commit_id. Reports preserve that distinction. New runs need their own source verification and artifact directory.

Snapshot adoption: 90 source files match exact framework blob bytes. Eight unresolved template links in `.sae/examples/project/AGENTS.md` refer to the eventual adopting root and are preserved upstream template content; project-root adapted links resolve. Bilingual mirrors copied unchanged. No GitHub Actions enabled. Setup repaired Git's Windows archive newline conversion and a Dropbox build staging lock. A non-login WSL invocation lacked CLI PATH before allocation; login shell fixed invocation. No numerical implementation failure was observed and no synthetic failure was injected to inflate repair counts.

Session controller is one invocation with a 600-second allocation deadline, bounded subprocess calls and finally-stop/verify. It refuses duplicate allocation markers and preexisting sessions. The checked-in controller is for this dated pilot, with an absolute task cutoff, not a perpetual runner. It performs no purchases, remote GitHub writes, credential reads or billing changes. All formal acceptance and merge decisions remain with GPT Architect; Codex does not self-merge.

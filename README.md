# SAE Test · Lean Research Lab Pilot

A dedicated public sandbox for testing the [SAE Framework](https://github.com/JohnnyZPiggy/SAE-Framework) Lean Research Lab `EXPLORE → VALIDATE` workflow.

**Pilot control:** [SAE-Framework Issue #37](https://github.com/JohnnyZPiggy/SAE-Framework/issues/37)

**Pinned SAE Framework revision:** `3fa17c605fbd3389439eee8bf016305632fb25ab` (PR #36).

**First algorithm:** Gaussian Randomized Range Finder (batched PyTorch), a reproducible workflow fixture rather than a novelty claim.

**Execution:** Codex Engineer handles a single bounded implementation → CPU numerical testing → autonomous repair → available Colab GPU and optional TPU-XLA probe → verified cleanup → one consolidated GitHub evidence return. GPT Architect/Mentor reviews mathematical and experimental evidence and eligible pull requests; Scientist sets goals without per-stage approval.

**Current state:** implementation and exact-source CPU tests completed; see the [measured pilot evidence](reports/pilot-20261020/summary.md) for device results and limitations. GPT Architect acceptance and merge remain pending.

**Safety:** No changes to legacy algorithm repositories, no GitHub Actions/background scheduler, no incremental billing, no leaked credentials. Respect real tool/account rights, at most one Colab session, Issue #37's task-defined time limits, and accurate `PASS/FAIL/NOT_RUN/BLOCKED` reporting.

The self-contained `.sae/` snapshot contains all 90 framework source files, verified against the pinned Git blobs in `framework-snapshot.json`. Root `AGENTS.md` and `sae.yaml` adapt the project rules. No hosted CI or background service is installed.

```sh
python -m pip install .
python -m unittest discover -s tests -v
python -m torch_rand_range_lab.benchmarks.run --device cpu --source-sha dc055f42ea9d7f5318cc52b936305cfa3c733fc2 --output cpu-result.json
```

The benchmark's NumPy tensor interop dependency is declared in package metadata. The recorded tested candidate predates this metadata correction; all algorithm/test Python files are unchanged. Use the exact candidate installation command in the [engineering handoff](docs/engineering/range-finder-engineering.md) for reproducibility. A supplied SHA label alone does not prove the working tree matches it.

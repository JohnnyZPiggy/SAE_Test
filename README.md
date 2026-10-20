# SAE Test · Lean Research Lab Pilot

A dedicated public sandbox for testing the [SAE Framework](https://github.com/JohnnyZPiggy/SAE-Framework) Lean Research Lab `EXPLORE → VALIDATE` workflow.

**Pilot control:** [SAE-Framework Issue #37](https://github.com/JohnnyZPiggy/SAE-Framework/issues/37)

**Pinned SAE Framework revision:** `3fa17c605fbd3389439eee8bf016305632fb25ab` (PR #36).

**First algorithm:** Gaussian Randomized Range Finder (batched PyTorch), a reproducible workflow fixture rather than a novelty claim.

**Execution:** Codex Engineer handles a single bounded implementation → CPU numerical testing → autonomous repair → available Colab GPU and optional TPU-XLA probe → verified cleanup → one consolidated GitHub evidence return. GPT Architect/Mentor reviews mathematical and experimental evidence and eligible pull requests; Scientist sets goals without per-stage approval.

**Current state:** `BOOTSTRAP_PENDING / EXPERIMENTS_NOT_RUN`. This repository's initial README is not evidence of a completed PyTorch implementation, validated hardware, automatic publisher or benchmark.

**Safety:** No changes to legacy algorithm repositories, no GitHub Actions/background scheduler, no incremental billing, no leaked credentials. Respect real tool/account rights, at most one Colab session, Issue #37's task-defined time limits, and accurate `PASS/FAIL/NOT_RUN/BLOCKED` reporting.

**Next work:** Codex should adopt a project-local `.sae/` snapshot **pinned to the exact framework SHA above**, replacing project-specific placeholders and verifying links. Develop on a separate branch and submit a reviewable PR, not directly on `main`.

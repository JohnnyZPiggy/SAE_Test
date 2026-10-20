# Issue 37 — engineering evidence collected, GPT review pending

One resumed bounded batch started 2026-10-20T13:09:23+00:00; report cutoff 2026-10-20T13:35:32.971191+00:00 (1569.971 seconds). Total through GitHub publication is recorded in the upstream return receipt, not projected here. Source dc055f42ea9d7f5318cc52b936305cfa3c733fc2; SAE snapshot 3fa17c605fbd3389439eee8bf016305632fb25ab. This is a workflow fixture of classical range finding, not algorithmic novelty. Codex does not self-approve science or merge.

CPU PASS: exact-committed package/test bytes installed and tested using Python 3.14.6, torch 2.14.1+cpu, 2 CPU threads. GPU PASS: exact Git SHA installed by pip, commit_id verified, on Tesla T4, Python 3.13.15, torch 2.11.0+cu130, CUDA 13.0. Ten numerical case groups plus invalid-input/empty-batch checks passed on each device. Worst seeded rank16 residual: CPU 4.819255e-07, GPU 4.5108786e-07, limit 1e-3. Full-rank slow-spectrum residual is diagnostic, not subject to that bound.

| Device | B,m,n,rank,width | Loop median ms | Batched median ms | Observed loop/batched |
|---|---|---:|---:|---:|
| CPU | 16,128,96,16,24 | 1.710400 | 1.257400 | 1.3603x |
| CPU | 16,512,256,32,40 | 5.419500 | 4.443800 | 1.2196x |
| T4 | 16,128,96,16,24 | 3.701198 | 1.641565 | 2.2547x |
| T4 | 16,512,256,32,40 | 5.414449 | 4.882213 | 1.1090x |

These are same-device eager matmul+QR comparisons, identical A/Omega within each comparison, 2 warmups/7 alternating-order synchronized timings. Input generation/transfer/projection excluded. No cross-device operator-fusion or universal speedup claim. Raw samples, spread, p95 and CPU input hashes are in JSON/CSV. `first_call_seconds` occurs after correctness, not fresh-process cold-start timing.

GPU PROBE_ONLY smoke passed before the full numerical/benchmark candidate. TPU NOT_RUN: no TPU allocated, torch_xla absent, no TPU runtime environment detected; this is an availability observation, not a TPU/XLA QR pass. Optional TPU is not inferred from CUDA. torch.compile fullgraph eager capture passed locally with zero projection error; native compiler/GPU compile NOT_RUN.

First T4 execution timed out after 440s; underlying cause unproven (status IDLE, creation-only event log). It was released before retry. The retry used a process-local HTTP timeout/stack diagnostic wrapper plus a short KERNEL_REACHABLE probe, then the same exact algorithm SHA. It passed; wrapper causality vs transient recovery is not established. Two sequential allocations, maximum one active; conservative allocation lifecycles total 478.914 seconds, below 2700s. Both stopped; final server state no active sessions. Existing unit balances were 62.67 initially and 62.54 after retry, with delayed accounting between checks; no purchase or billing change. Do not treat rounded balance changes as exact experimental charge.

Seven substantive failures: host Git DNS/WSL sandbox boundaries (resolved using authorized escalations), snapshot CRLF mismatch (exact blobs restored), pip temporary-directory permission failure, Dropbox wheel lock (temporary build fixed), WSL PATH missing colab (login shell fixed), and first GPU timeout. Five batch repair actions: implementation 1, dependency 3, timeout 1; numerical failures/repairs 0. Two host permission boundary resolutions counted separately. No artificial failure was injected. Per-failure times absent from logs remain null. Diagnostic help/file-discovery errors are not additional experiment attempts.

This resumed batch has one user-relayed engineering dispatch and one consolidated evidence packet returned via the PR plus the single upstream Issue comment; these two cross-links are one packet, not repeated per-attempt returns. Prior blocked attempt remains separately visible. No per-repair science/compute signoff requests. Host sandbox escalations did occur; actual human approval clicks vs automatic stored-rule approval are not observable, so no unattended/zero-human-approval claim is made. Snapshot adoption verifies all 90 files and root links; eight preserved upstream example-template links require deployment at an adopting root. No legacy algorithm repository or framework remote branch changed; no Actions, background agent, new service or self-merge.

Formal VALIDATE acceptance needs independent GPT Mentor/Architect review of the scoped mathematical rationale, exact numerical evidence and final PR. This report is an engineering return, not that decision. Final review corrected package metadata to declare NumPy, already present in the tested environments. All algorithm/test Python files remain byte-identical to the tested SHA; report/orchestration/metadata changes are separate from it. Dependency resolution in a fully empty environment was not run. No claim of efficiency improvement over legacy SAE, since no comparison baseline was measured.

Primary coordination: https://github.com/JohnnyZPiggy/SAE-Framework/issues/37. Reproduction commands and source-provenance limits: [engineering handoff](../../docs/engineering/range-finder-engineering.md) and [research rationale](../../docs/research/range-finder-tensorization.md).

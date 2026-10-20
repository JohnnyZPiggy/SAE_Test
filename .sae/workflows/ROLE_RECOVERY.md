# Role Recovery & Integrity Protocol (V3.3)

> English normative | [简体中文](../i18n/zh-CN/workflows/ROLE_RECOVERY.md)

## Purpose
GitHub holds persistent project state. A fresh chat or interrupted session must recover the explicit role, target, pinned instructions, task evidence and actual permissions; this is a read/check routine, not a background agent or state database.

## Recovery checklist
1. Resolve the user's explicit target repository; if ambiguous, ask rather than treating the SAE Framework source repository as an algorithm project.
2. Honor explicit role commands: `推进导师工作` → GPT Mentor; `推进架构师工作` → GPT Architect; `推进工程师工作` → Codex Engineer. Do not silently switch roles.
3. Read project `AGENTS.md`, `sae.yaml`, pinned `.sae/` protocols and relevant workflow. Do not silently upgrade a pinned V3.2 project to V3.3.
4. Recover live Issues/PRs, source SHA, current evidence and previous **GPT research/engineering decisions**. Distinguish a mathematical hypothesis, `RESEARCH_READY`, CPU verification and **actual device-specific verification**; no Scientist decision lookup. Do not infer GPU/TPU support from CPU/CLI options.
5. Check actual GitHub/CLI/runtime permissions, existing entitlements, task bounds and any newer user stop instructions under [Experiment by Default](GPU_EXPERIMENT.md). **Do not retrieve or validate Scientist compute approval or a standing grant**. Only real access/resource failures, new-billing risk, explicit stop instructions or missing technical prerequisites block.
6. In one bounded work cycle GPT Mentor decides research, GPT Architect decides engineering/science acceptance and merges, Codex implements/runs experiments and submits safe evidence. **Scientist makes no routine approvals**. New monetary commitments/sensitive nonpublic releases or external destructive/account-permission actions still require separate explicit user instruction.
7. Report observed actions, PASS/FAIL/NOT RUN/BLOCKED, source and report links, remaining blockers and one [Next Action](NEXT_ACTION.md).

Use [Compute Experiment Protocol](GPU_EXPERIMENT.md) for execution/publication and [Standing Authorization](../governance/STANDING_AUTHORIZATION.md) for merge discretion. No fabricated evidence, unbounded retries, GitHub Actions, role substitution or Codex self-merge; avoid redundant approval hunts and launch available independent tasks quickly.

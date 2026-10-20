# Next-Action Protocol — Agent Handoff and One-Tap Continuation

> Language: **English** | [简体中文](../i18n/zh-CN/workflows/NEXT_ACTION.md)

## Purpose

At the end of **each substantive SAE Mentor, Architect or Codex Engineer work cycle**, provide the Scientist with a short, actionable next step. This is a presentation and handoff contract, **not** an autonomous scheduler, new agent, extra task database, or permission to execute future work without a new instruction.

## Mandatory compact footer
End each substantive reply with this short user-facing **SAE · Next action** footer (fill real values, not placeholders):

> **SAE · Next action**  
> **Current state:** <verified status or UNVERIFIED> · **Evidence:** <Issue/PR/report/commit or NOT RUN>  
> **Recommended:** <one full copyable Chinese role command or Scientist action> — <reason>  
> **Alternatives:** <zero to two only if genuinely different>  
> **Needs Scientist:** <none by default; only genuinely required new billing, sensitive-data, external-permission or irreversible action>

Choose from current **GitHub evidence, task priority, dependencies, readiness and actual permissions**, not stale chat state. Typical routing: `RESEARCH_BLOCKED` → GPT Mentor/Architect mathematical revision; `RESEARCH_READY` → Architect; `CPU_IN_PROGRESS` → Codex; `CPU_VALIDATED` → Architect readiness review; `GPU_READY` → Codex experiment under [Experiment by Default](GPU_EXPERIMENT.md), **without Scientist compute authorization or grant checks**; `GPU_BLOCKED` → local Architect/Codex diagnosis. Correctness/security blockers override the default route.

A recommended command **does not execute an Agent**, allocate compute or authorize merges. Never request formal accelerator acceptance before `GPU_READY`; bounded `PROBE_ONLY` hardware probes may run earlier, reveal credentials, bypass merge authority or promise background execution. [Task Management](TASK_MANAGEMENT.md) owns Issue/PR state; this file owns the response handoff.

## Next-Action Completion Gate — pre-send check (V3.3)

Before sending the **final user-facing reply** of every substantive Mentor, Architect or Codex cycle—including long research, code changes, experimental runs, failures and blocked work—perform this compact self-check. A substantive cycle is **not communicatively complete** until the footer is present; keep the footer even when shortening the rest of a long response.

1. **Status and evidence:** state what was actually completed versus NOT RUN / UNVERIFIED / BLOCKED, with verifiable Issue, PR, report or commit links when available. Never fabricate activity, approvals or progress.
2. **One recommended handoff:** when a feasible next step exists, provide **one full, stand-alone, immediately copyable Chinese command** naming its target and action: `推进架构师工作：…`, `推进导师工作：…`, `推进工程师工作：…`, or `Scientist：…`. No placeholders, ambiguous fragments or commands to an agent that cannot actually be invoked.
3. **Meaningful choices:** offer zero to two distinct, feasible alternatives only when there is a real fork in the workflow. Rank one as the recommendation; do not pad choices or repeat the same work with different wording.
4. **No human approval queue:** GPT owns scoped science, readiness, engineering and T1/T2/T3 evidence decisions; Codex runs existing-account compute under [Experiment by Default](GPU_EXPERIMENT.md). Never recommend waiting for Scientist science, CPU/GPU, T3 or PR signoff. Preserve real access, SHA, evidence, and new-billing/nonpublic-data external boundaries; a command is not proof of execution.
5. **Last visible section:** end the reply with **SAE · Next action** (including current state, evidence, recommendation/alternatives and Scientist requirements). Explicitly write DONE / BLOCKED / WAITING_FOR_EXTERNAL_ACTION if there is no honest executable next action; when a safe recovery or approval step exists, make that the copyable recommendation.

### Copy/paste and interactive-choice fallback

- **Always expose complete command text**, even when the client also shows a working Copy / Continue control. If the client supports *real* copy and one-tap actions, associate each action with **exactly the same command** as its visible text; never draw pretend buttons or assert an external agent was invoked.
- **If controls are unavailable (Codex CLI/desktop, terminal, Markdown-only clients), put each recommended/alternative command in its own fenced plain-text block**, so the Scientist can copy and paste it without editing. Do not combine multiple commands in a single block.
- If no executable action exists, display the terminal/blocked status and needed external condition without inventing an actionable command. This protocol is a **response-level self-check**, not a machine-enforced output validator; context loss or interrupted execution can still prevent compliance.

## Example (illustrative only)

**SAE · Next action**  
**Current state:** CPU_VALIDATED *(example, not a real project claim)* · **Evidence:** example Issue #42  
**Recommended:** `推进架构师工作：审核 Issue #42 的 GPU Readiness` — verify the CPU evidence before Colab.  
**Alternative:** `推进工程师工作：复核 Issue #42 的 CPU 编译日志`  
**Needs Scientist:** None for scoped science, engineering, experiment and merge; only real new-billing/nonpublic-data/external-permission actions.

## Integration

The task-management workflow remains the canonical GitHub Issue/PR handoff; this protocol only standardizes **what the agent tells the Scientist after each cycle**. Root/project AGENTS and role protocols should point here. Never duplicate the entire protocol into every role file.

## Role recovery and integrity
At cycle start apply [Role Recovery](ROLE_RECOVERY.md) to validate role, pinned rules and real permissions; end with this Completion Gate.

# SAE Framework V3.3

> English normative | [简体中文](README.zh-CN.md)

**Scientist–Architect–Engineer** is a GitHub-first collaboration framework for mathematical algorithms, PyTorch scientific computing and ML engineering. It pursues **two equal goals**: reliable low-cost engineering and the Scientist's deeper mathematical/numerical/ML-systems learning.

## Architecture

![SAE V3.3 — native card-style research and engineering architecture (English)](docs/figures/SAE_Framework_V3.3.en.svg)

[Open the full-resolution SVG](docs/figures/SAE_Framework_V3.3.en.svg)

[Editable Mermaid source (.mmd)](docs/figures/SAE_Framework_V3.3.en.mmd)

<details>
<summary>Editable Mermaid architecture diagram</summary>

```mermaid
flowchart TB
    subgraph OBJECTIVES["01 · Two Equal Objectives"]
      direction LR
      O1["Engineering Productivity<br/>Correct · Reproducible · Low Cost"]
      O2["Scientific Learning<br/>Math · Numerics · ML Systems"]
    end

    S["Scientist · Human<br/>Set Goals · Redirect / Stop"]

    subgraph PEOPLE["02 · Research and Engineering Roles"]
      direction LR
      G["GPT · Chief Architect + Scientific Mentor<br/>Autonomous Math / Research Decisions · Fast Dispatch<br/>Evidence Review · Eligible PR Merges"]
      E["Codex · Engineer<br/>Implement / Test · Local CPU<br/>Default Colab CPU / GPU / TPU"]
    end

    H[("GitHub · Single Collaboration and Evidence Hub<br/>Issues · Code · PRs · Source SHA · Reports")]

    subgraph COMPUTE["03 · Codex Execution / Evidence Loop"]
      direction LR
      L["Local CPU<br/>Install · Numerical correctness · Regression tests"]
      C["Colab CLI / WSL2<br/>CPU · GPU · TPU*<br/>Run / Integrity check / Session cleanup"]
    end

    P["Pinned source SHA → No-GitHub-write benchmark<br/>→ Optional, GPT-reviewed safe evidence PR"]
    D["Google Drive<br/>Optional notebook scratch"]

    O1 --> S
    O2 --> S
    S <-->|Set goals / Feedback / Stop| G
    S -.->|No routine approval queue| E
    G <-->|Issues / Review feedback| H
    E <-->|Code / Evidence PR| H
    G <-->|Iterative collaboration| E
    E --> L
    E -->|Default eligible compute| C
    L --> P
    C --> P
    P -.->|Verified reports via PR| H
    D -.->|Temporary files only| C
    H -.->|New evidence / Next research cycle| G

    classDef goal fill:#EFF5FC,stroke:#9EB9D8,color:#243F5B,stroke-width:1.5px
    classDef human fill:#FFF4E2,stroke:#DDB875,color:#6E4820,stroke-width:2px
    classDef agent fill:#EEF2FF,stroke:#9FA8E7,color:#2D3D73,stroke-width:1.5px
    classDef engineer fill:#EAF8F5,stroke:#78B8AD,color:#164E4B,stroke-width:1.5px
    classDef github fill:#F3EDFB,stroke:#B19ACF,color:#4E3974,stroke-width:2px
    classDef compute fill:#F2F7FA,stroke:#B1C6D4,color:#274659,stroke-width:1.5px
    classDef scratch fill:#F7F7F9,stroke:#C8CBD0,color:#66717D,stroke-dasharray:5 4
    class O1,O2 goal
    class S human
    class G agent
    class E engineer
    class H github
    class L,C,P compute
    class D scratch
```

</details>

The bilingual SVGs faithfully reconstruct the **confirmed ChatGPT Native UI card architecture**: two equal objectives → Scientist goal setting/stop control → GPT Chief Architect + Scientific Mentor autonomous decisions → Codex execution → CPU/GPU/TPU → GitHub evidence feedback. Rounded cards, vector icons, arrows and execution boundaries are all drawn as SVG primitives. The embedded Mermaid and linked `.mmd` are the editable **logical** view; the SVG is documentation, not proof of executed experiments.

*TPU/PyTorch-XLA and automated report publication remain unverified.*

## Who does what?
- **Scientist (human):** sets/changes research goals and can stop work; **no routine mathematical, experimental, resource, T3 or PR approvals**.
- **GPT Architect:** autonomously decides science, mathematical readiness, engineering/experimental acceptance, iterations and eligible PR merges under [Standing Authorization](governance/STANDING_AUTHORIZATION.md).
- **GPT Mentor:** leads mathematical structure/tensorization research and explains numerical/experimental results.
- **Codex Engineer:** implements, tests and runs eligible existing-account local CPU and Colab CLI CPU/GPU/TPU experiments by default; verifies outputs and resource cleanup; submits safe evidence through GitHub branches/PRs without self-merging.

**GitHub** is the collaboration and evidence hub. **Colab CLI** supplies remote compute. **Drive** is an optional thin notebook workspace, not a sync/results transport.

## Workflow
GPT-decided concise [mathematical study](workflows/MATHEMATICAL_RESEARCH.md) + parallel [Build-vs-Reuse](workflows/ECOSYSTEM_REVIEW.md), reference work and `PROBE_ONLY` device checks → Codex implementation, correctness and eligible compute → GitHub evidence PR → GPT review/iteration/eligible merge. **No Scientist stage signoffs.** Multiple rounds can return to research.

Experiments have **three separate stages**: exact source-SHA install, benchmark **without GitHub writes**, and optional GPT-reviewed, sanitized report publication (separate user permission remains required for sensitive release or new billing). See [Compute Experiment Protocol](workflows/GPU_EXPERIMENT.md); the [historically named compatibility file](workflows/COLAB_TWO_COMMAND.md) remains linked.

## Start
Read [AGENTS.md](AGENTS.md), then [Bootstrap V3.3](SAE_BOOTSTRAP.md). Adopt [project AGENTS](examples/project/AGENTS.md) and [sae.yaml](examples/project/sae.yaml) with a **real pinned framework commit SHA**; do not silently upgrade existing projects.

| Role command | Purpose |
| --- | --- |
| `推进导师工作` | Mathematical discovery and scientific learning |
| `推进架构师工作` | Design, delegate, review and decide merges |
| `推进工程师工作` | Implement, execute authorized experiments and submit PR evidence |

These are user-invoked bounded cycles, not a hosted autonomous agent. No default GitHub Actions/paid CI, secrets in reports, fabricated benchmarks or Drive sync.

## Verification status (2026-10-19)
The Scientist reported one successful Codex → WSL2 → Colab CLI T4 GPU smoke test with result integrity verification and zero active sessions after shutdown. **Not yet verified:** Colab CPU, TPU allocation/PyTorch-XLA, automatic GitHub publication, cross-project reuse and a complete SAE benchmark-to-PR workflow. Bootstrap/Publisher automation is not established by documentation alone.

## Documentation
[Architect](protocols/ARCHITECT.md) · [Engineer](protocols/ENGINEER.md) · [Mentor](protocols/MENTOR.md) · [Scientist](protocols/SCIENTIST.md) · [Role Recovery](workflows/ROLE_RECOVERY.md) · [Changelog](CHANGELOG.md) · [Chinese index](i18n/zh-CN/README.md)

**Version:** V3.3 architecture and protocol; existing pinned V3.2 project snapshots remain unchanged until explicitly upgraded. **License:** [MIT License](LICENSE) · Copyright © 2026 JohnnyZPiggy. The MIT grant covers original content in this repository; any third-party materials retain their own license terms.

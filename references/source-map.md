# Source Map

This skill follows source-faithful adaptation. Source snapshots are pinned in `C:\c\Users\Administrator\projects\financial-skill-sources\SOURCE_SNAPSHOTS.md`.

## Pinned Sources

| Source | Commit | Role in this skill |
|---|---|---|
| `anthropics/financial-services` | `4bbabc7cd1a474c1667fa05a2bfe58e411dcf9c1` | Reference plugin architecture, financial research workflows, modeling/reporting capability parity. |
| `LLMQuant/quant-mind` | `8e218884a6cec3122ba42f9fa2277d593b907361` | QuantMind Layer pattern for interpreting source material into structured research evidence. |
| `tjboudreaux/cc-thinking-skills` | `0313ee0d476bf9db2c38ad8bd11d9933a61350d4` | Thinking Model Adapter pattern and progressive disclosure for explicit reasoning models. |
| `jwangkun/claude-for-financial-services-cn` | `59e97ee6683391a05ce6c69502a0fd16bbce4690` | Secondary reference for market-localization style; not a crypto market authority. |

## Adaptation Rules

- Preserve useful source capability before simplifying the skill.
- Cite the source row when adding or changing a capability derived from an upstream project.
- Record deliberate omissions in `references/capability-matrix.md`; do not leave omissions implicit.
- Prefer adapted instructions over large verbatim copied passages.

## Capability Trace

| Local capability | Primary source | Adaptation note |
|---|---|---|
| Research output modes | `anthropics/financial-services` | Consolidates research, modeling, and reporting workflows into crypto-local modes. |
| Market overview and thematic research | `anthropics/financial-services` | Preserve sector/market landscape structure, adapt to crypto sectors, protocols, chains, liquidity regimes, and narratives. |
| Thesis tracking and catalyst monitoring | `anthropics/financial-services` | Preserve thesis/catalyst monitoring, adapt catalysts to unlocks, protocol upgrades, ETF/regulatory events, exchange listings, macro liquidity, and derivatives positioning. |
| Idea generation and screening | `anthropics/financial-services` | Preserve screening and idea-sourcing pattern, adapt to token universes, liquidity filters, derivatives context, and on-chain/protocol metrics. |
| Model update and research note drafting | `anthropics/financial-services` | Preserve update workflow, adapt to fast-moving market data, protocol metrics, token economics, and venue-specific limitations. |
| Structured evidence extraction | `LLMQuant/quant-mind` | Use source/parser/workflow/structured knowledge concepts to turn reports, datasets, exchange data, and on-chain observations into evidence units before analysis. |
| Thinking model routing | `tjboudreaux/cc-thinking-skills` | Use selected thinking frameworks as progressive-disclosure checks, not as accuracy guarantees. |
| China financial-services adaptation style | `jwangkun/claude-for-financial-services-cn` | Use only as a reference for source-faithful localization discipline; do not import A-share market assumptions into crypto. |


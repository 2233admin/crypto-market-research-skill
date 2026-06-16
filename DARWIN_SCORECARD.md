# Darwin Scorecard

Date: 2026-06-16
Eval mode: `dry_run + opencli_1.8.4_smoke`

This score uses the Darwin Skill 8-dimension rubric. Runtime-neutral red-light scan found no matches in `SKILL.md`.

## Score

| Dimension | Weight | Rating | Weighted |
|---|---:|---:|---:|
| Frontmatter quality | 8 | 9.0 | 7.2 |
| Workflow clarity | 15 | 8.2 | 12.3 |
| Boundary conditions | 10 | 8.5 | 8.5 |
| Checkpoint design | 7 | 6.5 | 4.6 |
| Instruction specificity | 15 | 8.5 | 12.8 |
| Resource integration | 5 | 9.0 | 4.5 |
| Overall architecture | 15 | 9.0 | 13.5 |
| Tested performance | 25 | 8.8 | 22.0 |
| **Total** | **100** |  | **85.4** |

## Read

The crypto skill is already strong as a market research skill. It separates spot, derivatives, order book, protocol fundamentals, on-chain/protocol context, executable source-health diagnostics, and trade-planning discipline. OpenCLI smoke tests passed across Binance, CoinGecko, DefiLlama, and the latest CoinGlass source-doctor check.

## Main Weaknesses

- CoinGlass browser-backed source was flaky across runs; `scripts/source_doctor.py` now reports browser failures and falls back to CoinGecko derivatives when needed.
- Checkpoint design is light: trade-plan and alert/order workflows need explicit user confirmation boundaries.
- The skill has good evidence contracts but still needs concrete output templates and regression fixtures.

## Priority Fixes

1. Add fixture tests for source diagnostic events and repair candidates.
2. Add explicit confirmation checkpoints for trade plans, alert creation, and any order-adjacent workflow.
3. Add output templates for market-structure analysis, factor candidates, and philosophical analysis.

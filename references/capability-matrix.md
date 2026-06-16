# Capability Matrix

Use this matrix to prevent capability loss while adapting the source projects for crypto market research.

## source_parity

| Capability group | Required local coverage |
|---|---|
| Research workflows | Market overview, thematic research, idea generation, thesis tracking, catalyst monitoring, research note drafting, and model/update workflows where applicable. |
| Financial analysis patterns | Comparable analysis, scenario analysis, data cleaning, chart/table preparation, and document/spreadsheet authoring patterns where useful for crypto research. |
| QuantMind layer | Source ingestion, parsing, structured knowledge units, retrieval-ready evidence, batch processing pattern, and natural-language input resolution pattern. |
| Thinking models | Router-style selection, Bayesian update, scientific method, systems thinking, inversion, pre-mortem, second-order thinking, and OODA as the default crypto-research subset. |
| Source-faithful localization | Preserve upstream workflow intent while adapting market semantics; do not copy A-share assumptions from the China-localized source. |

## market_adaptation

| Adaptation area | Required local behavior |
|---|---|
| Venue and instrument structure | Separate spot, perpetuals, dated futures, options, staking/yield, protocol revenue, and on-chain activity. |
| Market-structure evidence | Follow `references/market-structure-policy.md` for funding, open interest, liquidations, basis, order-book/liquidity context, volatility, stablecoin flows, and chain activity. |
| Data sources | Follow `references/data-source-policy.md`; record venue, chain, provider, timestamp, and known limitations. |
| Timeframe discipline | Separate higher-timeframe bias from lower-timeframe execution context when trade planning is requested. |
| Reflexivity | Treat leverage, liquidation clusters, funding crowding, narrative reflexivity, and liquidity gaps as first-class risk context. |
| Protocol context | Distinguish token price action from protocol usage, revenue, emissions, unlocks, governance, and security events. |

## quality_upgrade

| Upgrade | Required local behavior |
|---|---|
| Evidence traceability | Every conclusion should point to structured evidence or explicitly state that source support is missing. |
| Source health loop | Every source failure, stale result, partial result, or suspicious output should produce a diagnostic event, user warning, fallback note, and repair candidate. |
| Freshness gate | State data timestamp, exchange/venue, chain, source provider, and known lag when available. |
| Output modes | Support `report_parsing`, `factor_engineering`, and `philosophical_analysis` without treating any one mode as the whole skill. |
| Factor contract | Require the seven-field factor candidate contract before any factor-like output is accepted. |
| Thinking model adapter | Use progressive disclosure and output model labels/checks/risk flags rather than generic long reasoning. |
| Source parity audit | Add omissions to `deliberate_omissions` before removing upstream capability. |

## deliberate_omissions

- None yet. Add a note here before removing any useful upstream capability.

# Crypto Market Research Skill

Market-specific agent skill for crypto asset, derivatives, protocol, liquidity, and market-structure research.

This repository packages a source-traced research workflow for crypto research notes, exchange data, funding, open interest, liquidity, order-book context, on-chain and protocol evidence, factor hypotheses, and trade-plan evidence.

## What It Does

- Keeps the top-level boundary at the research market: crypto.
- Preserves upstream financial-services capabilities before adapting them.
- Converts raw or semi-structured market material into structured research evidence.
- Supports three output modes: `report_parsing`, `factor_engineering`, and `philosophical_analysis`.
- Emits source-health diagnostics before conclusions when live data is required.
- Treats factor candidates and trade-plan evidence as research outputs, not final unvalidated signals.

## Quick Start

Use the skill root directly from an agent runtime that supports `SKILL.md`.

For local source checks:

```powershell
python scripts\source_doctor.py --symbol ETHUSDT --derivative-symbol ETH --protocol lido --limit 5
```

The source doctor returns JSON with:

- `source_health`
- `diagnostic_events`
- fallback source usage
- repair candidates for missing, stale, partial, suspicious, or failed sources

## Current OpenCLI Status

The latest smoke test used OpenCLI `1.8.4`.

- Binance price, klines, and depth are usable.
- CoinGecko derivatives are usable.
- DefiLlama protocol fundamentals are usable.
- CoinGlass open interest passed in the latest run, while browser-backed sources remain monitored for profile connectivity regressions.
- See `OPENCLI_SMOKE_TEST.md` for evidence and score.

## Provenance

This skill is a source-faithful adaptation inspired by:

- Anthropic financial-services skills
- `jwangkun/claude-for-financial-services-cn`
- `LLMQuant/quant-mind`
- `tjboudreaux/cc-thinking-skills`

See `references/source-map.md` and `NOTICE` for pinned source mapping and attribution.

## License

Apache-2.0. See `LICENSE`.

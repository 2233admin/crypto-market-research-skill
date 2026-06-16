# QuantMind Layer

The QuantMind Layer turns raw or semi-structured crypto source material into structured research evidence before report writing, factor construction, philosophical analysis, or trade-plan reasoning.

## Inputs

- Exchange market data and derivatives data
- On-chain and protocol datasets
- Tokenomics, unlock schedules, governance posts, and protocol docs
- Research reports, market notes, news, and macro commentary
- Academic papers, blogs, and other research material

## Evidence Unit Contract

Use this contract when normalizing source material:

- `source_id`: stable local identifier or URL/path
- `source_type`: exchange_data, derivatives_data, onchain_data, protocol_report, news, research_report, paper, note, or other
- `market`: `crypto`
- `entity`: asset, pair, protocol, chain, sector, venue, or asset universe
- `instrument`: spot, perpetual, future, option, token, protocol_metric, onchain_metric, or other
- `period_or_timestamp`: data timestamp, block/time window, event date, or publication date
- `extracted_facts`: facts directly supported by the source
- `interpreted_claims`: analysis derived from facts
- `source_limitations`: known gaps, stale data, venue/provider limitations, or disagreement
- `downstream_uses`: report_parsing, factor_engineering, philosophical_analysis, trade_plan_context, or multiple

## Use Rules

- Build evidence units before strong conclusions.
- Keep source facts separate from interpreted claims.
- For factor work, transform evidence units into factor candidates only after the calculation logic and economic hypothesis are explicit.
- For report parsing, preserve document structure when it carries meaning, such as thesis, methodology, protocol metrics, risks, tokenomics, or catalyst sections.
- For philosophical analysis, ground assumptions and failure modes in evidence units rather than unsupported narrative.

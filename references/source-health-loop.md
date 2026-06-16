# Source Health Loop

The skill must not silently ignore data-source failures. Every source call should produce evidence or a diagnostic event that the agent can use to warn the user and choose a safe fallback.

## Diagnostic Event Contract

Use this contract when a source is called:

- `source_name`: Binance, CoinGecko, DefiLlama, CoinGlass, TradingView, Xquik, exchange direct API, on-chain provider, report, news source, or other
- `source_category`: exchange_direct, derivatives_aggregator, onchain_protocol, market_aggregator, browser_source, social_discourse, research_news, or unknown
- `command_or_access_path`: command, API, URL, file path, or manual source
- `entity`: asset, pair, protocol, chain, venue, sector, or universe
- `requested_fields`: requested data fields or document type
- `status`: pass, fail, stale, partial, suspicious
- `observed_at`: local run time or source timestamp
- `data_timestamp`: market timestamp, block/time window, funding interval, or publication date
- `failure_reason`: missing_credentials, browser_profile_disconnected, no_data, timeout, schema_drift, adapter_error, stale_data, rate_limit, source_disagreement, or none
- `fallback_used`: source name or none
- `user_message`: concise warning or confirmation request to show the user
- `repair_candidates`: list of safe repair actions

## Required Loop

1. Run the most primary relevant source from `data-source-policy.md`.
2. Validate that output is non-empty, fresh enough, and contains expected fields.
3. If the source fails or looks suspicious, emit a diagnostic event.
4. Try a safe fallback source if one exists.
5. Tell the user when a key source failed, when a fallback was used, or when a result is incomplete.
6. Propose repair candidates, but do not perform credential, browser-profile, alert, order, or write-side repairs without confirmation.

## Executable Doctor

Run the source doctor before analysis when live source health is unknown:

```bash
python scripts/source_doctor.py --symbol ETHUSDT --derivative-symbol ETH --protocol lido --limit 5
```

The script emits:

- `source_health`: summary status, failed sources, fallback sources, user warning, and repair candidates
- `diagnostic_events`: one event per checked source

If `source_health.status` is `partial` or `fail`, show the user the warning before relying on conclusions.

## Crypto Repair Candidates

| Failure | Agent-visible message | Safe repair candidates |
|---|---|---|
| Browser profile disconnected | A browser-backed source is unavailable because the profile or extension is not connected. | Ask user to connect Browser Bridge; retry with `opencli doctor`; fall back to non-browser sources such as CoinGecko or Binance. |
| Exchange API no data | Exchange direct data returned empty output. | Retry symbol normalization; check spot/perp suffix; try another venue or market aggregator. |
| Derivatives aggregator unavailable | Funding/open-interest source failed. | Fall back to CoinGecko derivatives; mark CoinGlass unavailable; ask whether reduced derivatives coverage is acceptable. |
| Stale market data | Data timestamp is too old for the requested decision. | Warn user; rerun fresh command; avoid issuing trade-plan conclusions. |
| Social discourse incomplete | Public X discourse coverage is missing, stale, or sample-limited. | Use Xquik or another documented source with the query and time window recorded; keep conclusions narrative-only until corroborated. |
| Source disagreement | Venues or providers disagree on price, funding, OI, or TVL. | Preserve disagreement; cite provider-specific values; avoid averaging unless user asks. |
| Order-adjacent request | User asks to create alerts/orders or executable trade workflow. | Require explicit confirmation; preview only by default; do not fire orders from analysis output. |

## User Warning Template

```json
{
  "source_health": {
    "status": "partial",
    "failed_sources": ["CoinGlass open-interest"],
    "fallback_sources": ["CoinGecko derivatives"],
    "user_warning": "CoinGlass failed because the browser profile is disconnected. I used CoinGecko derivatives as fallback, so open-interest coverage is provider-limited.",
    "repair_candidates": ["run opencli doctor", "connect Browser Bridge profile", "retry CoinGlass after profile reconnect"]
  }
}
```

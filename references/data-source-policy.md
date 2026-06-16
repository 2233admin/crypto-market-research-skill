# Data Source Policy

Use source categories to make crypto evidence auditable. Crypto data is venue-specific, chain-specific, and often time-sensitive, so never treat a source as universal without checking scope.

## Source Categories

| Category | Use for | Notes |
|---|---|---|
| Exchange direct data | OHLCV, trades, order books, spot/perp/futures markets, funding where provided. | Record venue, symbol, market type, and timestamp. |
| Derivatives aggregators | Funding, open interest, liquidations, basis, options volatility, positioning, and leverage context. | Providers can disagree; cite provider and timestamp. |
| On-chain and protocol data | TVL, revenue, fees, active addresses, flows, staking, emissions, unlocks, governance, bridge activity, and protocol health. | Record chain, contract/protocol scope, and methodology limits. |
| Market data aggregators | Prices, market cap, volume, token metadata, circulating supply, and exchange coverage. | Use for broad context; verify critical figures against primary or specialist sources. |
| Research and news | Protocol reports, market updates, governance posts, regulatory news, and macro-liquidity narratives. | Separate reported facts from interpretation and opinion. |

## Fallback Rules

1. Prefer primary venue or chain data for precise market claims.
2. Use aggregators for breadth, but mark provider methodology and timestamp.
3. If a source fails or returns suspicious output, emit a diagnostic event using `source-health-loop.md` before using fallback data.
4. If sources disagree, preserve the disagreement instead of averaging it away and emit a source-disagreement diagnostic.
5. For fast-moving markets, treat stale data as a material limitation.
6. Never include user secrets, API keys, private wallet data, or private account data in outputs, examples, or committed files.

## Freshness Notes

For market data, include timestamp and venue. For on-chain data, include chain, block/time window, and provider. For reports or news, include publication date. For trade planning, explicitly separate historical evidence from live conditions.

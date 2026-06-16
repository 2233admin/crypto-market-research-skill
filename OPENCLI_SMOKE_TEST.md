# OpenCLI Smoke Test

Date: 2026-06-16
OpenCLI: `1.8.4`

## Commands

```powershell
opencli binance price ETHUSDT -f json
opencli binance klines ETHUSDT --interval 4h --limit 8 -f json
opencli binance depth ETHUSDT --limit 5 -f json
opencli coingecko derivatives --symbol ETH --limit 5 -f json
opencli defillama protocol lido -f json
opencli coinglass open-interest -f json
python scripts/source_doctor.py --symbol ETHUSDT --derivative-symbol ETH --protocol lido --limit 5
```

## Result

| Check | Status | Evidence |
|---|---|---|
| Spot price | Pass | Binance returned ETHUSDT price `1676.70000000`, 24h change `0.141%`, quote volume `295818037.72370700`. |
| 4H klines | Pass | Binance returned eight 4H candles with OHLCV. |
| Order book | Pass | Binance returned five bid/ask levels; best bid `1676.70000000`, best ask `1676.71000000`. |
| Derivatives | Pass | CoinGecko returned ETH perpetual markets with funding rate, open interest, and 24h volume. |
| Protocol fundamentals | Pass | DefiLlama returned Lido category, TVL, market cap, chains, audits, and protocol metadata. |
| CoinGlass browser source | Pass | CoinGlass returned open-interest data with timestamp `2026-06-13T10:36:24.082Z` in the latest run. |
| Source doctor | Pass | Script emitted `status: pass`; Binance, CoinGecko, DefiLlama, and CoinGlass checks returned usable data. |

## Contract Fit

- Can produce `report_parsing` from market/protocol datasets and research notes.
- Can produce `factor_engineering` candidates from momentum, liquidity/depth, funding/open-interest, and protocol TVL/market-cap evidence.
- Can produce market-structure analysis from spot, 4H candles, order book, derivatives, and protocol evidence.
- Must mark CoinGlass/browser-source failure as a source limitation if Browser Bridge/profile connectivity regresses.
- `scripts/source_doctor.py` emits browser-source failures as diagnostic events with fallback and repair candidates when they recur.

## Score

`8.8 / 10`

The skill contract is already strong with OpenCLI because sources cover spot, candles, order book, derivatives, protocol fundamentals, and source-health diagnostics. It becomes production-grade after browser-profile failure fixtures and live freshness assertions are added.

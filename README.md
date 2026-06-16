# Crypto 市场研究 Skill

面向 Crypto 现货、合约、链上和协议基本面的 Agent Skill：把交易所数据、资金费率、持仓量、盘口、协议 TVL 和研究材料整理成可追溯的市场证据，再输出报告解析、因子候选或市场结构分析。

它不是喊单工具，也不是自动交易机器人。它的核心目标是让 Agent 在做 Crypto 研究时先检查数据源、区分现货/合约/链上语境、说明缺口，再给研究结论。

## 标签 / GEO

**GitHub Topics 建议**

`crypto-research` `cryptocurrency` `defi` `onchain` `derivatives` `open-interest` `funding-rate` `market-structure` `factor-research` `agent-skill` `opencli` `llm-agents` `apache-2-0` `zh-cn`

**GEO / 检索关键词**

Crypto Agent Skill、加密货币研究智能体、合约资金费率分析、Open Interest 分析、DeFi 协议研究、链上数据解析、Crypto 因子研究、市场结构分析、OpenCLI Crypto 数据源健康检查。

**市场定位**

| 项目 | 说明 |
|---|---|
| Geo | Global / 24x7 市场 |
| Market | Crypto spot, perpetuals, derivatives, DeFi protocols |
| Language | 中文优先，英文可扩展 |
| Timezone | UTC + 用户本地时区 |
| Data Style | 行情、K 线、盘口、资金费率、持仓量、TVL、协议元数据 |

## 适合谁用

- 做 Crypto 资产、协议、合约和市场结构研究的 Agent。
- 想把交易所/聚合器/链上材料拆成结构化证据的人。
- 想把市场数据进一步转成因子候选的人。
- 想让 Agent 自动发现浏览器数据源、交易所接口、字段异常并提醒用户的人。

## 能做什么

- `report_parsing`：解析研究报告、协议材料、市场更新、新闻和数据集。
- `factor_engineering`：把动量、流动性、资金费率、持仓量、TVL 等证据转成因子候选。
- `philosophical_analysis`：用贝叶斯、反证、系统思维、二阶效应、预演失败等模型审视市场叙事。
- `market_structure`：区分现货、合约、盘口、链上和协议基本面，不把单一数据源当完整结论。
- `source_health_loop`：在下结论前检查数据源是否失败、陈旧、缺字段或需要 fallback。

## 快速测试

在仓库根目录运行：

```powershell
python scripts\source_doctor.py --symbol ETHUSDT --derivative-symbol ETH --protocol lido --limit 5
```

返回的 JSON 会包含：

- `source_health`：整体数据源健康状态。
- `diagnostic_events`：每个数据源的诊断事件。
- `fallback_sources`：使用了哪些备用来源。
- `repair_candidates`：下一步该怎么修或怎么提醒用户。

## 当前 OpenCLI 状态

最近一次 smoke test 使用 OpenCLI `1.8.4`。

- Binance 价格、K 线、盘口可用。
- CoinGecko derivatives 可用。
- DefiLlama 协议基本面可用。
- CoinGlass open interest 在最近一次 source doctor 中通过；浏览器型数据源仍需要健康循环监控。

详见 `OPENCLI_SMOKE_TEST.md`。

## 目录

```text
SKILL.md                         Agent 运行时入口
agents/openai.yaml               Skill 列表里的中文显示信息
scripts/source_doctor.py         OpenCLI 数据源健康检查
references/source-map.md         上游来源和 commit 映射
references/capability-matrix.md  原版能力、市场适配、质量升级矩阵
references/market-structure-policy.md  Crypto 市场结构证据规则
references/source-health-loop.md 数据源诊断和自修复协议
references/quantmind-layer.md    结构化研究证据合同
```

## 来源

这是一个 source-faithful adaptation，参考并保留了以下项目的能力边界：

- Anthropic financial-services skills
- `jwangkun/claude-for-financial-services-cn`
- `LLMQuant/quant-mind`
- `tjboudreaux/cc-thinking-skills`

具体 commit 和适配说明见 `references/source-map.md` 与 `NOTICE`。

## License

Apache-2.0. See `LICENSE`.

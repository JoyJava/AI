# 搜索查询模板库

标准化的搜索查询，确保每次简报质量一致。执行时根据当前日期动态替换 `[DATE]`。

---

## 模块 A：国际要闻

```
# 第一轮：宏观国际局势（执行2–3次，覆盖不同地区）
international news today March 2026 latest
geopolitical risk breaking news today
US China Europe Middle East Africa news today

# 第二轮：热点深挖（根据第一轮结果选择3–5个热点）
[热点关键词] breaking news today latest update
[热点关键词] latest development what happened

# 第三轮：补充地区搜索（确保至少6条不同地区新闻）
Asia Pacific news today
Europe news today
Middle East conflict update today
Africa Latin America major news today
```

目标：覆盖至少6个地区/议题，每条有具体事实、数字、人名，不只是标题。
**推荐来源**：Reuters、AP News、BBC World、Financial Times、Foreign Policy

---

## 模块 G：AI行业动态（新增，每次至少4次独立搜索）

```
# 模型与产品
AI model release launch today 2026
OpenAI Anthropic Google DeepMind new model today
LLM benchmark comparison latest

# 研究突破
AI research paper breakthrough today arxiv
artificial intelligence capability advance today
AI safety alignment research latest

# 监管与政策
AI regulation policy news today 2026
EU AI Act implementation update
US AI executive order legislation today
China AI regulation Cyberspace Administration today

# 投融资与并购
AI startup funding investment today 2026
artificial intelligence acquisition merger today
AI unicorn valuation news latest

# 大厂战略
OpenAI news today strategy product
Anthropic news today Claude update
Google DeepMind Gemini news today
Meta AI Llama news today
xAI Grok Elon Musk AI today
Microsoft Copilot Azure AI today
Nvidia AI chip GPU news today
Baidu Alibaba ByteDance AI China today
```

---

## 模块 B：宏观财经

```
# 央行与货币政策
Federal Reserve latest decision OR statement today
ECB Bank of England latest policy
"interest rate" decision news today

# 经济数据
US economic data released today CPI OR jobs OR GDP
"economic calendar" major release today

# 大宗商品与汇率
gold oil price today movement
USD DXY dollar index latest
Treasury yield 10 year today

# 研报摘要
Goldman Sachs Morgan Stanley research note today
"Wall Street" forecast outlook latest
```

**推荐来源**：Bloomberg、Reuters、WSJ、FT、Macro Voices

---

## 模块 C：加密货币

```
# 行情与市场
Bitcoin BTC price today analysis
Ethereum ETH latest news today
crypto market update today

# 监管与机构
crypto regulation news today
institutional bitcoin news latest
SEC CFTC crypto ruling latest

# 链上与技术
Bitcoin on-chain data today
DeFi TVL latest update
crypto hacks exploits today
```

**推荐来源**：CoinDesk、The Block、Decrypt、Cointelegraph、Glassnode（链上）

---

## 模块 D：美股动态

```
# 大盘表现
US stock market today S&P 500 Nasdaq performance
"market wrap" OR "market recap" today
Wall Street today summary

# 热门个股与行业
stock movers today biggest gainers losers
earnings reports today after hours
tech stocks AI stocks today

# 机构资金流向
fund flows institutional buying selling today
options unusual activity today
hedge fund positioning latest
```

**推荐来源**：Bloomberg、CNBC、MarketWatch、Seeking Alpha、Zacks

---

## 模块 E：大佬观点

### 批量搜索模板（按人执行）

```
# Ray Dalio
Ray Dalio latest 2025 interview OR article OR LinkedIn
site:linkedin.com Ray Dalio

# Warren Buffett
Warren Buffett Berkshire Hathaway latest letter OR statement 2025
Buffett latest interview CNBC OR Bloomberg

# Stanley Druckenmiller
Druckenmiller latest speech OR interview 2025
Stanley Druckenmiller macro view latest

# Jamie Dimon
Jamie Dimon JPMorgan latest comments 2025
Dimon economy warning OR outlook latest

# Larry Fink
Larry Fink BlackRock annual letter 2025
Fink latest speech OR interview

# Michael Burry
Michael Burry Scion 13F latest 2025
Burry tweet OR post latest

# Cathie Wood
Cathie Wood ARK latest video OR blog 2025
ARK Invest monthly update latest

# Paul Tudor Jones
Paul Tudor Jones interview 2025 latest
Tudor Jones macro view inflation gold

# Bill Ackman
Bill Ackman Twitter X latest 2025
Ackman Pershing Square latest position

# Howard Marks
Howard Marks Oaktree memo 2025 latest
Marks investment memo market outlook
```

---

## 快速全局搜索（时间有限时使用）

```
market news today summary all sectors
top financial news today international
crypto US stocks macro news today wrap
```

---

## 模块 G：Polymarket 预测市场

Polymarket 是全球最大的链上预测市场，赔率由真实 USDC 资金博弈形成，对即将发生事件有先行指示意义。

```
# 直接抓取 Polymarket 当日热门盘口
polymarket trending markets today
polymarket top markets latest odds

# 地缘政治 / 战争类
polymarket Iran war ceasefire odds today
polymarket Israel Iran conflict latest
polymarket war geopolitical markets 2026

# 美国政治类
polymarket Trump policy tariffs latest
polymarket US election 2026 midterms
polymarket recession 2026 probability

# 宏观经济 / 美联储类
polymarket Federal Reserve rate cut 2026 odds
polymarket US recession probability latest
polymarket inflation CPI prediction market

# 加密类
polymarket Bitcoin price prediction
polymarket ETH ETF approval odds

# 综合热门
site:polymarket.com trending
polymarket biggest movers today odds change
```

**直接访问盘口（优先 web_fetch 获取最新赔率）：**
- 热门列表：`https://polymarket.com/markets?_s=volume`
- 搜索特定盘口：搜索 `polymarket [关键词] odds 2026`

**数据解读要点：**
- 赔率 = 该事件发生的市场隐含概率（如 72% = 市场认为72%概率发生）
- 24h 赔率变化 > ±5pp → 视为重大信号，须标注 🚨
- 总流动性（Volume）越高 → 赔率越可信，越难被小资金操控
- 重点关注："赔率大幅变动但新闻面尚未跟进"的盘口，往往是市场的领先指标

---

## 模块 G：Polymarket 预测市场

```
# 直接抓取页面
polymarket.com markets politics
polymarket.com markets crypto
polymarket.com markets economics

# 搜索当前热门盘口
polymarket Iran war ceasefire odds 2026
polymarket US recession 2026 odds
polymarket Bitcoin price end 2026 odds
polymarket Fed rate cut 2026 probability
polymarket Trump impeachment odds
polymarket oil price odds 2026

# 赔率变动新闻
polymarket latest odds change today
"prediction market" Iran war odds today
```

**推荐来源**：polymarket.com（直接抓取）、Kalshi、metaculus、The Block Polymarket报道

---

## 模块 H：走势推演搜索

```
# 分析师对美股情景的最新预测
S&P 500 forecast scenarios war oil price 2026
Wall Street bull bear case S&P 500 latest
Goldman Sachs JPMorgan S&P 500 target 2026

# BTC分析师情景预测
Bitcoin price forecast scenarios 2026
BTC bull bear case analysis latest
crypto market outlook war impact 2026

# 关键变量追踪
Fed rate cut probability CME FedWatch latest
oil price forecast Goldman Sachs 2026
US recession probability latest 2026
```

---

## 模块 J：技术指标（每次简报必须搜索）

```
# J-1 市场参与度
S&P 500 percent above 50 day moving average today
Nasdaq 100 breadth indicator above 50MA today
NYSE advance decline line today
stock market breadth indicators current

# J-2 美联储流动性
Fed balance sheet total assets latest 2026
Federal Reserve reverse repo RRP balance today
Fed bank reserves deposits latest
M2 money supply year over year latest 2026

# J-3 链上盈利地址占比
Bitcoin addresses in profit percentage today glassnode
BTC percent addresses profit latest intotheblock
Ethereum ETH addresses in profit percentage latest
crypto on-chain profitability indicator today
```

**J 模块数据来源优先级：**
- 市场参与度：Barchart.com、Macroaxis、StockCharts
- 美联储数据：FRED（fred.stlouisfed.org）、Federal Reserve H.4.1 报告
- 链上数据：Glassnode、IntoTheBlock、CryptoQuant、MacroMicro

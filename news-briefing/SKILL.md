---
name: news-briefing
description: 24小时全球新闻情报快报技能。当用户询问"最新新闻"、"今日快报"、"市场动态"、"大佬观点"、"宏观形势"、"crypto行情"、"美股动态"、"研报摘要"、"国际局势"时立即触发。也用于用户说"帮我看看今天发生了什么"、"有什么大事"、"市场怎么样"、"大佬们怎么看"、"整理一下新闻"时。触发词：新闻、快报、动态、行情、早报、晚报、日报、国际、宏观、美股、A股、港股、crypto、比特币、大佬观点、研报、市场消息、今日要闻。覆盖：国际政治/经济、全球宏观、加密货币、美股、顶级投资人最新观点。即使用户只是简单问"今天有什么新闻"也应立即触发此技能。
---

# 📰 24小时全球新闻情报快报

本技能提供结构化的全球新闻情报简报，覆盖国际局势、宏观财经、加密货币、美股动态及顶级大佬最新观点。

---

## 🎯 执行框架

### 第一步：明确用户需求

用户可能要求以下任一或全部模块：
- **A. 国际要闻** — 地缘政治、外交、重大事件（**至少6条**，重大冲突/危机期间8–10条，每条都要有足够深度，不只是标题）
- **B. 宏观财经** — 央行政策决议、重要经济数据发布、贸易规则/关税变化、信用评级机构对主权评级调整、重大金融事件（**不列具体标的价格**，聚焦政策和事件本身）
- **C. 加密货币** — 监管动态、交易所上架/下架事件、监管机构对币种分类变更（是否视为证券）、稳定币监管规则变化、重大行业事件、链上异常活动、机构进出场事件（**不列具体币价**，聚焦事件和趋势）
- **D. 美股动态** — 标普500/纳斯达克100成分股调整（纳入/剔除）、交易所上市规则修改（退市标准、IPO门槛）、SEC监管规则变更（披露要求、做空规则、保证金要求）、交易机制变化（熔断、交易时间）、重要财报、并购事件、行业重大变化（**不列指数和个股价格**，聚焦公司事件、规则变更和行业趋势）
- **E. 大佬观点** — 40位大佬过去24小时内的公开发言/采访/社媒
- **F. 大佬仓位变化** — 40位大佬过去24小时内的持仓变动、买卖操作
- **G. 🤖 AI行业动态** — 模型发布、研究突破、监管、投融资、大厂战略（独立模块，内容丰富，见下方专项说明）
- **H. Polymarket 预测市场** — 政治/军事/宏观相关盘口的最新赔率与24小时变动
- **I. 情景推演** — 综合所有模块，对当前局势进行多情景逻辑推演（**不含具体价格目标**）

**如果用户没有特别指定，默认输出全部九个模块（A–I）。**

**重要原则：简报聚焦新闻和事件，不列具体标的价格。** 不要在简报中列出任何股票指数数值、个股价格、加密货币价格、汇率数值、债券收益率数值、大宗商品价格等。用户自行查看行情终端获取实时价格。

**E 与 F 的区别：**
- E 模块 = 大佬"说了什么"（观点/言论）
- F 模块 = 大佬"做了什么"（实际买卖/仓位变动）
- 两个模块独立过滤：某大佬当日有观点但无操作，则出现在 E、不出现在 F；反之亦然。
- F 模块当日全部40人均无变化时，整个模块省略，不出现在简报中。

**G 模块说明（AI行业动态）：**
这是一个独立的深度模块，覆盖过去24小时内AI领域的重要进展，内容量应与宏观财经模块相当。搜索时每次至少执行3–4次独立搜索，涵盖以下五个子类：

① **模型与产品发布** — 新模型/版本/功能上线，包含性能基准对比
② **研究突破** — 重要论文（arXiv/Nature/顶会）、能力边界突破、安全研究
③ **监管与政策** — 美国/欧盟/中国AI监管动态，国会听证，行政令
④ **投融资与并购** — 大额融资轮次、战略收购、估值变动
⑤ **大厂战略动态** — OpenAI/Anthropic/Google/Meta/xAI/Microsoft/百度/阿里/字节等的战略调整、人事变动、合作协议

搜索查询模板：
```
AI model release news today 2026
artificial intelligence research breakthrough today
AI regulation policy news today
AI startup funding investment today
OpenAI Anthropic Google DeepMind news today
China AI Baidu ByteDance Alibaba latest
Nvidia GPU AI chip news today
```

输出格式：每条消息含影响评级 非常重要/中等重要/一般 + 2–3句实质内容 + 对AI产业或相关公司股价的影响判断。

**H 模块说明（Polymarket 预测市场）：**
- 重点追踪三类盘口：①地缘政治/战争 ②各国选举/政治 ③宏观经济/美联储/美股/加密
- 每个盘口展示：当前赔率、24小时赔率变化、总流动性体量
- 赔率大幅变动（±5个百分点以上）须重点标注

**I 模块说明（情景推演）：**
- 综合 A–H 所有模块，对当前局势进行多情景逻辑推演
- 给出明确的乐观/基准/悲观情景，含触发条件和时间窗口
- **不包含任何具体价格目标**，只描述方向性影响（如"利好风险资产"/"利空大宗商品"）
- 必须标注：**这是逻辑推演，不是投资建议**

---

### 第二步：搜索策略

每个模块执行独立的搜索，使用以下策略并参考 `references/search-queries.md` 中的查询模板。

**搜索原则：**
- 优先搜索过去24小时内容，查询中加入 `"2024" OR "today" OR "latest"`
- 每个模块至少执行 **2-3次** web_search，再用 web_fetch 读取关键全文
- 大佬观点模块额外搜索其 Twitter/X、最新采访、致股东信等
- 遇到冲突信息，以更权威来源为准，并在简报中注明

**规则修改类事件专项搜索查询模板：**
```
# B模块 — 宏观规则变更
central bank policy framework change today
tariff trade rule change today 2026
sovereign credit rating change Moody's S&P Fitch today
sanctions list update OFAC today

# C模块 — 加密货币规则变更
Coinbase Binance listing delisting today
SEC crypto security classification today
stablecoin regulation rule change today
crypto exchange regulatory action today

# D模块 — 美股规则变更
S&P 500 index rebalance constituent change today
Nasdaq 100 index addition removal today
SEC rule change regulation disclosure today
NYSE listing standard change delisting today
stock exchange trading hours circuit breaker change today
SEC short selling margin requirement rule today
IPO listing threshold change today
```

---

### 第三步：输出格式

输出结构化简报，遵循 `references/output-template.md` 中的模板规范。

**核心格式原则：**
1. 每条新闻附 **影响评级**：重大 / 中等 / 一般
2. 事实必须具体（人名、机构、具体日期、决策内容），**但不列任何标的价格**
3. E 模块（观点）标注来源平台 + 日期
4. F 模块（仓位）用表格呈现，含方向/资产/代码/规模（**不含具体买入价格**）
5. F 模块无变化时整体省略，不显示空模块
6. H 模块（Polymarket）展示赔率 + 24h变化 + 流动性，赔率变动±5pp以上须加 🚨 标注
7. 结尾附 **编辑点评**：跨模块关联分析（不超过150字）

---

## 👑 四十大顶级大佬名单

对每位大佬，**同时追踪两件事**：
1. **最新观点** — 过去24小时内的公开发言、采访、社交媒体
2. **最新操作/仓位变化** — 过去24小时内的持仓变动、买入/卖出、监管披露

**过滤规则：过去24小时内没有新动态（观点或操作均无）的大佬，直接跳过，不在简报中出现。**

---

### 🏦 A组：宏观对冲 & 全球视野（10人）

| # | 大佬 | 机构/身份 | 仓位来源 | 观点来源 |
|---|------|-----------|---------|---------|
| 1 | **Ray Dalio** | Bridgewater创始人 | Bridgewater 13F | LinkedIn（高频）、Bloomberg/CNBC |
| 2 | **Stanley Druckenmiller** | Duquesne Family Office | Duquesne 13F | Bloomberg/CNBC 罕见专访 |
| 3 | **Paul Tudor Jones** | Tudor Investment | Tudor 13F | Bloomberg TV、CNBC |
| 4 | **George Soros** | Soros Fund Management | Soros Fund 13F | 官方声明、Project Syndicate |
| 5 | **Jeffrey Gundlach** | DoubleLine Capital CEO | DoubleLine持仓披露 | Twitter/X @TruthGundlach（高频）|
| 6 | **Mohamed El-Erian** | Allianz首席顾问 | — | Bloomberg专栏、Twitter/X（高频）|
| 7 | **David Tepper** | Appaloosa Management | Appaloosa 13F | CNBC专访（每季度）|
| 8 | **Mark Spitznagel** | Universa Investments | Universa 持仓 | 媒体采访、著作观点 |
| 9 | **Nouriel Roubini** | Atlas Capital Team CEO | — | Project Syndicate、Twitter/X |
| 10 | **Jim Rogers** | Rogers Holdings | 持仓披露 | 媒体采访、新加坡 Bloomberg |

---

### 💰 B组：价值投资 & 激进主义（10人）

| # | 大佬 | 机构/身份 | 仓位来源 | 观点来源 |
|---|------|-----------|---------|---------|
| 11 | **Warren Buffett** | 伯克希尔·哈撒韦CEO | 13F、SEC Form 4 ⚡ | 股东信、CNBC专访 |
| 12 | **Howard Marks** | 橡树资本联创 | 橡树资本持仓 | oaktreecapital.com 备忘录 |
| 13 | **Bill Ackman** | Pershing Square | 13F、Twitter实时披露 ⚡ | Twitter/X @BillAckman（极高频）|
| 14 | **Seth Klarman** | Baupost Group | Baupost 13F | 罕见发言、致投资人信 |
| 15 | **David Einhorn** | Greenlight Capital | Greenlight 13F | 季度投资人信、CNBC |
| 16 | **Carl Icahn** | Icahn Enterprises | SEC披露、13F | Twitter/X、CNBC |
| 17 | **Dan Loeb** | Third Point | Third Point 13F | 季度投资人信、Twitter/X |
| 18 | **Nelson Peltz** | Trian Fund Management | Trian 13F、SEC 13D/G | 媒体采访、代理权争夺公告 |
| 19 | **Leon Cooperman** | Omega Advisors（已关闭） | — | CNBC（极高频出镜）、Twitter/X |
| 20 | **John Paulson** | Paulson & Co. | Paulson 13F | 偶发媒体采访 |

---

### 🏛️ C组：华尔街掌门 & 机构资管（8人）

| # | 大佬 | 机构/身份 | 仓位来源 | 观点来源 |
|---|------|-----------|---------|---------|
| 21 | **Jamie Dimon** | 摩根大通CEO | Form 4 内部持股 | 财报电话会、股东信、达沃斯 |
| 22 | **Larry Fink** | 贝莱德CEO | 贝莱德持仓披露 | 年度信（1月）、达沃斯、Bloomberg |
| 23 | **Ken Griffin** | Citadel创始人 | Citadel Advisors 13F | Bloomberg、WSJ 采访 |
| 24 | **Steve Cohen** | Point72创始人 | Point72 13F | 偶发媒体采访 |
| 25 | **Israel Englander** | Millennium Management | Millennium 13F | 极少公开发言 |
| 26 | **David Solomon** | 高盛CEO | — | 财报电话会、达沃斯 |
| 27 | **Ted Pick** | 摩根士丹利CEO | — | 财报电话会、Bloomberg |
| 28 | **Jane Fraser** | 花旗CEO | — | 财报电话会、CNBC |

---

### 🚀 D组：科技 & 成长 & 颠覆性投资（6人）

| # | 大佬 | 机构/身份 | 仓位来源 | 观点来源 |
|---|------|-----------|---------|---------|
| 29 | **Cathie Wood** | ARK Invest | ARK每日交易披露 ark-funds.com ⚡实时 | Twitter/X、ARK YouTube（高频）|
| 30 | **Chamath Palihapitiya** | Social Capital | 13F、SPAC公告 | Twitter/X @chamath（极高频）|
| 31 | **Peter Thiel** | Founders Fund | 13F、SEC披露 | 演讲、媒体采访 |
| 32 | **Masayoshi Son** | 软银集团 | 软银财报、持仓公告 | 软银财报发布会、Bloomberg |
| 33 | **Zhang Lei (张磊)** | 高瓴资本 | 13F（美股部分）、港股权益披露 | 演讲、《价值》著作观点 |
| 34 | **Li Lu (李录)** | 喜马拉雅资本 | Himalaya Capital 13F | 极罕见发言，关注专访 |

---

### ₿ E组：加密货币 & Web3（6人）

| # | 大佬 | 机构/身份 | 仓位来源 | 观点来源 |
|---|------|-----------|---------|---------|
| 35 | **Michael Saylor** | Strategy（原MicroStrategy）执行主席 | 公司BTC持仓公告 ⚡实时 | Twitter/X @saylor（极高频）|
| 36 | **Brian Armstrong** | Coinbase CEO | Form 4、公司持仓 | Twitter/X、财报电话会 |
| 37 | **Arthur Hayes** | BitMEX联创 / Maelstrom | 公开持仓 | Substack（Medium）文章（高频）|
| 38 | **Raoul Pal** | Real Vision CEO | — | Twitter/X、Real Vision视频（高频）|
| 39 | **Mike Novogratz** | Galaxy Digital CEO | 公司持仓披露 | Twitter/X、CNBC crypto专访 |
| 40 | **Willy Woo** | 链上数据分析师 | — | Twitter/X @woonomic（链上数据高频）|

---

### 仓位搜索查询模板

```
# 通用（每人执行）
"[大佬/机构名]" buy OR sell OR position OR stake today
"[大佬/机构名]" portfolio change filing latest
SEC filing "[机构名]" today OR yesterday

# ⚡ 每日必查（高频变动者）
ARK Invest daily trades today                          # Cathie Wood
Bill Ackman position update today site:x.com           # Ackman
Michael Saylor bitcoin purchase today                  # Saylor
Berkshire Hathaway SEC Form 4 today                   # Buffett

# 季度13F（刚发布时引用）
"[机构名]" 13F filing SEC latest 2025
site:sec.gov "[机构名]" 13F

# Twitter/X 高频观点（优先搜索）
Jeffrey Gundlach tweet today site:x.com
Chamath Palihapitiya tweet today
Leon Cooperman CNBC today
Mohamed El-Erian Bloomberg today
Arthur Hayes substack latest
Raoul Pal Real Vision latest
Willy Woo on-chain analysis today
```

### 操作信息输出规范

生成过程中不要有小图标

找到仓位变化时，用以下格式呈现在大佬条目内：

```
📊 最新操作（[日期]）
• 🟢 新建仓/加仓：[资产名称]（[代码]） — [金额或股数（如披露）]
• 🔴 减仓/清仓：[资产名称]（[代码]） — [金额或股数（如披露）]
📋 来源：[SEC披露 / ARK每日报告 / Twitter / 媒体报道]
```

**输出逻辑：**
- 24小时内有观点 + 有操作 → 两个区块都输出
- 24小时内只有观点 → 只输出观点，不显示操作区块
- 24小时内只有操作 → 只输出操作区块，备注"暂无最新公开发言"
- 两者都没有 → **整个大佬条目跳过，不出现在简报中**

**搜索效率提示：**
- ⚡ 标记的来源每日必查（ARK、Ackman Twitter、Saylor、Berkshire Form 4）
- 13F 为季度报告，仅在刚发布时引用，不算每日新增
- 高频 Twitter 用户（Gundlach、Chamath、Ackman、Saylor）优先搜 X
- 中文补充来源：华尔街见闻、彭博中文版、财联社

---

### 第四步：质量控制

输出前检查：
- [ ] A 模块国际要闻至少6条，重大冲突期间8–10条，每条含具体事实/人名/日期
- [ ] 所有新闻来源可信（避免低质量博客/论坛）
- [ ] **简报中不包含任何标的价格**（股票指数、个股价格、加密货币价格、汇率、债券收益率、大宗商品价格等一律不列）
- [ ] E 模块大佬观点有明确来源，不猜测
- [ ] F 模块仓位变化有 SEC/ARK/媒体明确出处，不推断
- [ ] F 模块当日无变化时整体省略（不显示空表格）
- [ ] G 模块 AI 行业涵盖五个子类（模型发布/研究突破/监管政策/投融资/大厂动态），内容量足够充实
- [ ] H 模块 Polymarket 赔率为当日最新，±5pp以上变动加 🚨 标注
- [ ] B/C/D 模块规则修改类事件已搜索覆盖（成分股调整、上市规则、SEC规则、交易所上架下架、币种分类变更等）
- [ ] 整体简报阅读时间控制在8分钟内

---

---

## 📚 参考文件索引

- `references/search-queries.md` — 各模块标准化搜索查询模板（含 G 模块 Polymarket）
- `references/output-template.md` — 完整输出格式模板（含 A–G 七模块）
- `references/sources-guide.md` — 可信来源列表与优先级

**使用时机**：执行搜索前先查阅 search-queries.md，输出前参考 output-template.md。

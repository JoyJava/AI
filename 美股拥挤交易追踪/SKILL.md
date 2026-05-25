---
name: 美股拥挤交易追踪
description: 当用户询问"最拥挤的交易"、"crowded trade"、"BofA FMS"、"基金经理共识"、"一致预期"、"CFTC COT"、"机构持仓拥挤度"、"资金流向"、"ETF资金流"、"原油/半导体/黄金是否见顶"时使用。也用于每日 7:57 定时生成/更新"拥挤交易追踪.html"。四层数据架构：BofA FMS（月频心理层）+ CFTC COT（周频杠杆层）+ 标的价格（日频松动信号）+ OBV机构资金流向（日频真金白银）。核心原则：一手数据源，不凭印象推断；拥挤度是投票/杠杆指标，不是仓位指标。
---

# 美股拥挤交易追踪 · 四层数据框架

## 何时使用本 skill

- 用户问"最拥挤的交易"、"crowded trade"、"共识交易"、"一致预期"
- 用户问 BofA 基金经理调查（FMS）或 CFTC COT 持仓的最新结果
- 用户要生成/更新 `拥挤交易追踪.html` 报告
- 每日早上 7:57 定时任务触发

---

## 核心认知：拥挤度有三层，不是一个数

```
第一层 · 心理层（BofA FMS）
  "基金经理认为谁最拥挤"
  数据：问卷投票，月频
  性质：主观共识，领先指标
  局限：193人样本，元认知 ≠ 真实仓位

第二层 · 杠杆层（CFTC COT）
  "期货市场上谁在裸压杠杆"
  数据：CFTC 每周五发布
  性质：客观数字，实际仓位
  局限：只覆盖期货期权，不含股票

第三层 · 价格层（Yahoo Finance）
  "拥挤交易的标的今天怎么走"
  数据：日频价格
  性质：实时松动信号
  局限：无法直接反映拥挤度

第四层 · 资金流向层（OBV · On-Balance Volume）
  "真金白银往哪个方向涌"
  数据：日频，从 Yahoo v8 price+volume 计算
  性质：量化资金流入/流出的方向和强度
  计算：如果今天涨就把成交量加入 OBV，跌就减去
  输出：7天/30天 OBV 变化 × 均价 = 美元资金流量估算
  优势：完全免费、日频更新、与 FMS 心理层形成对照
  局限：OBV 是代理指标，不等于真实 ETF 申赎（份额变化）

四层同时指向一个方向 = 真正的风险拥挤
四层背离 = 不要行动，继续观察
```

---

## 数据源与抓取方法

### 🥇 BofA FMS（月频，心理层）

**抓取方法**：

```
触发条件：当月 ≥ 第二个周二 且 本地基线不是本月
工具：mcp__exa__web_search_exa
查询模板：
  "BofA Global Fund Manager Survey <year> <month> most crowded trade"
  "BofA FMS <month> <year> results summary"
优先来源（按可靠度）：
  1. macenews.com（通常第一时间发布，数据完整）
  2. hedgefundtips.com（格式化摘要，易解析）
  3. investing.com
  4. atranicapital.substack.com（Igor Rotor 每月整理）
  5. fxstreet.com

必抓字段：
  - 发布日期、调查周期、样本数、AUM 规模
  - 前三名"最拥挤交易"及百分比
  - Bull & Bear 指标值
  - 现金水平百分比
  - 前三大尾部风险
  - 年末资产价格预期（油价、美元、债券）

交叉验证：3 个以上来源的数字必须一致（允许 ±1pp 四舍五入差异）
```

### 🥈 CFTC COT（周频，杠杆层）

**官方 API**：
```
基础 URL: https://publicreporting.cftc.gov/resource/6dca-aqww.json
查询参数示例（原油 WTI）:
  ?market_and_exchange_names=CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE
  &$limit=52
  &$order=report_date_as_yyyy_mm_dd DESC

关键字段：
  - noncomm_positions_long_all（非商业多头，通常是投机基金）
  - noncomm_positions_short_all（非商业空头）
  - net_position = long - short
  - 计算 Z-Score = (当前 net - 3年均值) / 3年标准差

拥挤度阈值：
  Z-Score > +2.0σ → 极端多头拥挤
  Z-Score > +1.5σ → 高度多头拥挤
  Z-Score < -1.5σ → 极端空头拥挤

需要追踪的合约（与 FMS 当前拥挤交易对齐）：
  原油 → CRUDE OIL, LIGHT SWEET (NYMEX)
  黄金 → GOLD (COMEX)
  美债 → 10Y NOTE (CBOT) / 30Y BOND (CBOT)
  标普 → S&P 500 E-MINI (CME)
  纳斯达克 → NASDAQ-100 E-MINI (CME)
  美元 → U.S. DOLLAR INDEX (ICE)
  半导体期货没有 → 用 SOXX ETF 资金流替代
```

### 🥉 标的价格（日频，松动信号）

**API**：
```
主用：Yahoo Finance（yfinance Python 库 或 query1.finance.yahoo.com CSV）
备用：Stooq.com（免费 CSV）

需要每日抓取的标的（按 FMS 当前前三对齐）:
  原油：USO（United States Oil Fund ETF）或 CL=F（WTI 期货）
  半导体：SOXX（iShares Semiconductor ETF）
  黄金：GLD（SPDR Gold Shares）
  Mag 7：MAGS（Roundhill Magnificent Seven ETF）或各股
  比特币：BTC-USD
  美债：TLT（20+ Year Treasury ETF）
  美元：DXY（Dollar Index）
  VIX：^VIX
  高收益利差：HYG（iShares HY Corporate Bond ETF）

触发告警阈值：
  🟡 单日 ±2% 以上 → 黄灯关注
  🟠 单日 ±3% 以上 → 橙灯
  🔴 单日 ±5% 或周度 ±7% → 红灯：拥挤交易可能正在解除
```

---

## 定时任务协议（每日 7:57 执行）

### 三层执行清单

**Layer 1 - 日度必跑（每天 7:57）**：
1. 读 `拥挤交易追踪.html` 的 `data-last-fms` 字段，获取当前基线月份
2. 抓取 8 个核心标的的最新价格和 24h / 7d 变化
3. 计算告警级别（黄/橙/红）
4. 更新 HTML 的"今日价格快照"板块
5. 写日志：`[工作区根目录]/投资/美股宏观追踪/分析结论/拥挤交易-更新日志.md`

**Layer 2 - 周度刷（每周六 7:57 或周五 COT 发布后次日）**：
1. 抓 CFTC COT 最新数据
2. 对 7 个核心合约计算 Z-Score
3. 更新 HTML 的"期货杠杆拥挤度"板块

**Layer 3 - 月度刷（每月第二个周二后 7 天内）**：
1. 抓新一期 BofA FMS
2. 解析前三名拥挤交易 + 完整结构数据
3. 更新 HTML 的"FMS 月度快照"和"12 月演变时间线"板块
4. 更新 `data-last-fms` 字段

### 执行判断逻辑（伪代码）

```
def daily_update():
    now = today()
    html = read("拥挤交易追踪.html")
    last_fms_month = html.meta["data-last-fms"]

    # Layer 3 判断
    second_tuesday = get_second_tuesday(now.year, now.month)
    if now >= second_tuesday + 1_day and last_fms_month != now.strftime("%Y-%m"):
        try:
            new_fms = fetch_bofa_fms()
            update_fms_section(html, new_fms)
        except NoDataAvailable:
            annotate_top_banner(html, "⚠️ 5月FMS暂未发布，预计5/13左右")

    # Layer 2 判断
    if now.weekday() == SATURDAY or (now.weekday() == FRIDAY and is_cot_release_day()):
        cot = fetch_cftc_cot()
        update_cot_section(html, cot)

    # Layer 1 每天必跑
    prices = fetch_prices(["USO","SOXX","GLD","MAGS","BTC-USD","TLT","DXY","^VIX","HYG"])
    alerts = compute_alerts(prices)
    update_price_section(html, prices, alerts)

    write_log(日期, 更新内容, 告警数)
```

### 失败兜底

```
❌ 绝不做：
  - BofA 新期未发布就编造当月数据
  - 抓不到价格就用"估计值"
  - 网络失败时保留空白不标注

✅ 必须做：
  - 数据缺失 → HTML 顶部红色横幅标注缺失来源和预计恢复时间
  - 数字冲突 → 以官方 API（CFTC）> Mace News > 其他，注明选择理由
  - 全部失败 → 生成一个"今日数据抓取失败"占位更新，附手动核查清单
```

---

## HTML 报告结构

**输出路径**：`[工作区根目录]/投资/美股宏观追踪/分析结论/拥挤交易追踪.html`

### 模块划分

```
┌─ 顶部横幅 ─────────────────────────────────────
│  当月 FMS #1 拥挤交易 + 百分比 + FMS 发布日期
│  今日综合告警级别（绿/黄/橙/红）
│  数据截至：YYYY-MM-DD HH:MM
└─────────────────────────────────────────────

┌─ 第一层：FMS 心理拥挤度（月度） ────────────────
│  ① 当月前三名投票表
│  ② 近 12 个月前三名演变时间线（Chart.js 堆叠柱状图）
│  ③ 2013-至今完整历史轨迹（长条形时间线）
│  ④ 样本信息 + 来源链接
└─────────────────────────────────────────────

┌─ 第二层：CFTC COT 杠杆拥挤度（周度） ───────────
│  ① 7 大合约 Z-Score 雷达图
│  ② 非商业净多头 3 年走势（折线）
│  ③ 极值标注：当前处于 3 年百分位
│  ④ CFTC 报告日期 + 下次发布
└─────────────────────────────────────────────

┌─ 第三层：标的价格松动信号（日度） ──────────────
│  ① 9 个标的今日 / 7天 / 30天 涨跌表
│  ② 价格告警级别（🟢🟡🟠🔴）
│  ③ 与 FMS 拥挤交易的联动关系
│  ④ 触发事件列表（今日有几个标的触发告警）
└─────────────────────────────────────────────

┌─ 决策面板 ────────────────────────────────────
│  "综合看，当前最拥挤的交易是 X，风险级别 Y"
│  联动：美股逃顶大佬仓位 / 综合诊断报告
│  下次关键事件：FMS/COT/财报
└─────────────────────────────────────────────

┌─ 更新日志 ────────────────────────────────────
│  最近 7 天每日更新摘要
└─────────────────────────────────────────────
```

### 视觉规范

- 深色主题 `#0d1117`，与 `/投资/美股宏观追踪/分析结论/` 其他报告一致
- 告警配色：绿 `#10b981` / 黄 `#eab308` / 橙 `#f97316` / 红 `#dc2626`
- 图表：Chart.js，优先本地引用 `references/chart.min.js`
- 所有数字必须可点击跳转原始来源

---

## 诚实与核实原则

```
每个数字的出处必须标明：
  ⚪ 实测：有一手链接（BofA 原文、CFTC API 响应、Yahoo Finance）
  🔵 推算：基于实测数据计算（Z-Score、涨跌幅）
  🟡 待核实：数据来源不稳定（社交媒体转载）
  🔴 缺失：本期抓取失败，显示上次值并标红

绝不做：
  - 在 HTML 里写具体百分比但没有一手来源链接
  - 用"大约"、"估计"、"据说"替代实际数字
  - 把 Chart 24 的历史演变当作当前数据
  - 拿不到新 FMS 就假装"和上月一样"
```

---

## 核心认知（重要）

### 拥挤度的三层差异

```
一个具体的例子（2026-04）：

FMS 说：     Long Oil 24% 最拥挤（心理层投票）
CFTC 说：    WTI 非商业净多头 Z-Score = +1.8σ（真实杠杆）
价格说：     USO 近 30 天 +12%，未破位（还在涨）

三层一致 → 真拥挤，风险高
```

### 什么叫"拥挤交易解除"

- 价格层先动：标的一天跌 3%+ 或一周跌 7%+
- CFTC 次之：净多头头寸单周减仓 20%+
- FMS 最后变：百分比从 24% 跌到 10% 以下（月频反应最慢）

**领先顺序**：价格 → COT → FMS。等 FMS 显示"不再拥挤"时，实际行情早已走完大半。

### 最强信号：背离

```
如果 FMS 显示某交易拥挤度继续上升（如从 24% → 30%）
但同时价格层已经开始下跌 或 CFTC 净多头开始减少
→ 这是最强的"拥挤交易即将见顶"信号
→ 机构嘴上还说拥挤，手上已经开始走
```

---

## 参考资料

- references/chart.min.js（本地 Chart.js）
- references/bofa-fms-历史演变.md（Chart 24 中文版，2013-至今）
- references/cftc-api-查询示例.md（CFTC COT API 参数和字段说明）
- references/yahoo-finance-标的清单.md（所有追踪标的的 ticker 对照）

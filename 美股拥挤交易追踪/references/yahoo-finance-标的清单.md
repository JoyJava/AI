# 追踪标的清单 · Yahoo Finance

## 核心追踪池（9 个，每日必抓）

| Ticker | 名称 | 对应 FMS 选项 | 类型 |
|--------|------|--------------|------|
| USO | United States Oil Fund ETF | Long Oil | ETF |
| SOXX | iShares Semiconductor ETF | Long Semiconductors | ETF |
| GLD | SPDR Gold Shares | Long Gold | ETF |
| MAGS | Roundhill Magnificent Seven ETF | Long Mag 7 | ETF |
| BTC-USD | Bitcoin | Long Bitcoin | 加密 |
| TLT | iShares 20+ Yr Treasury ETF | Long Treasuries | ETF |
| DX-Y.NYB | US Dollar Index | Short/Long USD | 指数 |
| ^VIX | CBOE Volatility Index | 市场恐慌 | 指数 |
| HYG | iShares HY Corp Bond ETF | 信用利差代理 | ETF |

## 扩展池（按需抓取）

| Ticker | 用途 |
|--------|------|
| CL=F | WTI 原油期货（比 USO 更直接） |
| GC=F | 黄金期货 |
| NVDA / MSFT / GOOGL / META / AAPL / TSLA / AMZN | Mag 7 分股 |
| SOX | 费城半导体指数 |
| QQQ / SPY | 宽基比较 |
| BRENT / BZ=F | 布伦特原油 |

## 抓取方式

### 方式 1：yfinance Python 库（推荐）
```python
import yfinance as yf

tickers = ["USO","SOXX","GLD","MAGS","BTC-USD","TLT","DX-Y.NYB","^VIX","HYG"]
data = yf.download(tickers, period="30d", interval="1d")
```

### 方式 2：直接 CSV 端点
```bash
# 30 天历史（period1=unix时间戳）
curl "https://query1.finance.yahoo.com/v7/finance/download/SOXX?period1=$(date -v-30d +%s)&period2=$(date +%s)&interval=1d&events=history"
```

### 方式 3：Stooq 备选
```bash
curl "https://stooq.com/q/d/l/?s=soxx.us&d1=20260401&d2=20260504&i=d"
```

## 计算规则

```python
# 单日涨跌
daily_change_pct = (close_today - close_yesterday) / close_yesterday * 100

# 7 天涨跌
week_change_pct = (close_today - close_7d_ago) / close_7d_ago * 100

# 30 天涨跌
month_change_pct = (close_today - close_30d_ago) / close_30d_ago * 100

# 波动率（20 日年化）
volatility_20d = returns.rolling(20).std() * sqrt(252)
```

## 告警阈值

| 级别 | 日变化 | 周变化 | 动作 |
|------|--------|--------|------|
| 🟢 绿 | < ±2% | < ±3% | 无动作 |
| 🟡 黄 | ±2-3% | ±3-5% | HTML 标注关注 |
| 🟠 橙 | ±3-5% | ±5-7% | HTML 顶部横幅 |
| 🔴 红 | > ±5% | > ±7% | 综合告警：拥挤交易可能正在解除 |

## 失败兜底

- Yahoo Finance 偶尔 API 限速 → 等待 60s 重试
- CSV 端点返回 `{"error":...}` → 切换到 Stooq
- 所有来源失败 → HTML 价格板块标注"抓取失败"，保留上次数据并显示时间戳

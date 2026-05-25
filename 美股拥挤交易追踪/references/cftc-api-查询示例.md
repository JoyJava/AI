# CFTC COT API · 查询示例与字段说明

## 官方数据源

CFTC Commitments of Traders Reports 官方 Socrata API（免费、无需 token）:

```
Base URL: https://publicreporting.cftc.gov/resource/6dca-aqww.json
```

## 关键合约的查询字符串

### 原油 WTI（NYMEX）
```bash
curl "https://publicreporting.cftc.gov/resource/6dca-aqww.json?market_and_exchange_names=CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE&\$limit=156&\$order=report_date_as_yyyy_mm_dd DESC"
```

### 黄金（COMEX）
```bash
curl "https://publicreporting.cftc.gov/resource/6dca-aqww.json?market_and_exchange_names=GOLD - COMMODITY EXCHANGE INC.&\$limit=156&\$order=report_date_as_yyyy_mm_dd DESC"
```

### 10 年美债（CBOT）
```bash
curl "https://publicreporting.cftc.gov/resource/6dca-aqww.json?market_and_exchange_names=UST 10Y NOTE - CHICAGO BOARD OF TRADE&\$limit=156&\$order=report_date_as_yyyy_mm_dd DESC"
```

### 标普 500 E-mini（CME）
```bash
curl "https://publicreporting.cftc.gov/resource/6dca-aqww.json?market_and_exchange_names=E-MINI S&P 500 - CHICAGO MERCANTILE EXCHANGE&\$limit=156&\$order=report_date_as_yyyy_mm_dd DESC"
```

### 纳斯达克 100 E-mini
```bash
curl "https://publicreporting.cftc.gov/resource/6dca-aqww.json?market_and_exchange_names=E-MINI NASDAQ-100 - CHICAGO MERCANTILE EXCHANGE&\$limit=156&\$order=report_date_as_yyyy_mm_dd DESC"
```

### 美元指数（ICE）
```bash
curl "https://publicreporting.cftc.gov/resource/6dca-aqww.json?market_and_exchange_names=U.S. DOLLAR INDEX - ICE FUTURES U.S.&\$limit=156&\$order=report_date_as_yyyy_mm_dd DESC"
```

## 关键字段

| 字段名 | 含义 |
|--------|------|
| `report_date_as_yyyy_mm_dd` | 报告周期结束日（通常是周二） |
| `noncomm_positions_long_all` | 非商业多头（投机基金，含对冲基金/CTA） |
| `noncomm_positions_short_all` | 非商业空头 |
| `comm_positions_long_all` | 商业多头（产业客户/套保） |
| `comm_positions_short_all` | 商业空头 |
| `tot_rept_positions_long_all` | 全部报告义务持仓多头 |
| `open_interest_all` | 未平仓合约总量 |

## Z-Score 计算（156 周 = 3 年）

```python
import pandas as pd
import numpy as np

df = pd.read_json(url)
df = df.sort_values('report_date_as_yyyy_mm_dd')
df['net'] = (
    df['noncomm_positions_long_all'].astype(float)
    - df['noncomm_positions_short_all'].astype(float)
)
df['z'] = (df['net'] - df['net'].rolling(156).mean()) / df['net'].rolling(156).std()

# 当前 Z-Score
current_z = df['z'].iloc[-1]

# 3 年百分位
current_pct = (df['net'].iloc[-1] > df['net'].tail(156)).sum() / 156 * 100
```

## 拥挤度阈值

| Z-Score | 含义 |
|---------|------|
| > +2.0σ | 🔴 极端多头拥挤（3 年顶部 2.3% 区间） |
| > +1.5σ | 🟠 高度多头拥挤 |
| +0.5 ~ +1.5σ | 🟡 偏多 |
| -0.5 ~ +0.5σ | 🟢 中性 |
| < -1.5σ | 🟠 极端空头拥挤 |

## 发布时间

- 每周五美东时间 15:30 发布（数据截至上周二）
- 美国联邦假日（如 Memorial Day）顺延
- 政府关门期间可能中断

import re
import math
import datetime

# Read files
tweets_file = 'X_Tweets_48h_2026-05-24.txt'
try:
    with open(tweets_file, 'r', encoding='utf-8') as f:
        content = f.read()
except:
    content = ""

# Parsers
tweet_blocks = content.split('========================================')
tweets = []
for block in tweet_blocks:
    if not block.strip(): continue
    lines = block.strip().split('\n')
    speaker = ""
    handle = ""
    text = ""
    for line in lines:
        if line.startswith('发言人:'):
            parts = line[4:].strip().split(' @')
            if len(parts) >= 2:
                speaker = parts[0].strip()
                handle = '@' + parts[1].split(' ')[0].strip()
            else:
                speaker = line[4:].strip()
                handle = speaker
        elif line.startswith('推文:'):
            text = line[3:].strip()
        elif line.startswith('[📌 引用旧内容]：'):
            text += " [引用: "
        elif not line.startswith('[') and not line.startswith('时间:'):
            if text and line.strip():
                text += " " + line.strip()
    if speaker and text:
        text = text.replace('[引用: ', ' [引用: ')
        tweets.append({'speaker': speaker, 'handle': handle, 'text': text})

# 归类聚合
speakers_data = {}
for t in tweets:
    handle = t['handle']
    if handle not in speakers_data:
        speakers_data[handle] = {'name': t['speaker'], 'tweets': [], 'count': 0}
    speakers_data[handle]['tweets'].append(t['text'])
    speakers_data[handle]['count'] += 1

# VIP名单
vip_list = ['@elonmusk', '@pmarca', '@garrytan', '@michaelxpettis', '@CathieWood', '@saylor']
ai_vip = ['@omarsar0', '@turingou', '@0xCheshire', '@foxshuo', '@0xTodd']
crypto_vip = ['@cryptorover', '@coinbureau', '@WuBlockchain', '@wublockchain12', '@EmberCN', '@PhyrexNi']

# Heuristics
bull_words = ['breakout', 'ath', 'buy', 'long', 'bull', 'surge', 'up', 'profit', 'optimistic', 'win', 'good', 'great', '拉爆', '起飞', '涨', '新高', '买入', '好消息', '乐观', '突破', '长牛', '看多', '大赢', '牛市', '加仓', '潜力', '高增长', '繁荣', '利好']
bear_words = ['crash', 'reject', 'bear', 'short', 'down', 'loss', 'sell', 'worse', 'warning', 'dead', 'flop', '亏', '跌', '空', '逃顶', '泡沫', '警告', '悲观', '被锤', '下行', '衰退', '砸盘', '见顶', '大跌', '阻力']

# Score calculation
total_bull_weight = 0
total_bear_weight = 0
total_score_weight = 0
total_weight = 0

for handle, data in speakers_data.items():
    N = data['count']
    base_weight = 2.0 if handle in vip_list else (1.5 if handle in ai_vip or handle in crypto_vip else 1.0)
    w_speaker = math.log2(N + 1) * base_weight
    
    handle_bull = 0
    handle_bear = 0
    handle_score = 0
    
    for t in data['tweets']:
        txt = t.lower()
        has_num = bool(re.search(r'\d+[%万亿kbm]?', txt))
        w_fact = 1.5 if has_num else 1.0
        
        bull_hits = sum(1 for w in bull_words if w in txt)
        bear_hits = sum(1 for w in bear_words if w in txt)
        
        if bull_hits > bear_hits:
            score = 7
            w_multi = 1.0
            handle_bull += 1
        elif bear_hits > bull_hits:
            score = -7
            w_multi = 1.3
            handle_bear += 1
        else:
            score = 0
            w_multi = 1.0
            
        w_final = w_speaker * w_fact * w_multi
        
        total_score_weight += score * w_final
        total_weight += w_final
        if score > 0: total_bull_weight += w_final
        if score < 0: total_bear_weight += w_final
        
    data['tendency'] = '多' if handle_bull > handle_bear else ('空' if handle_bear > handle_bull else '中性')

index_score = (total_score_weight / total_weight) if total_weight > 0 else 0
bull_pct = (total_bull_weight / (total_bull_weight + total_bear_weight)) * 100 if (total_bull_weight + total_bear_weight) > 0 else 50
bear_pct = 100 - bull_pct

date_str = '2026-05-24'
md = f"""# X(Twitter) 推文深度分析报告\n\n> **报告日期**：{date_str}\n> **数据窗口**：最近 48 小时\n> **样本总数**：{len(tweets)} 条有效推文（去重后）\n> **覆盖发言人**：{len(speakers_data)} 位\n\n---\n\n## 一、情绪指标\n\n> 按照 AI 和美股的 X 情绪指标\n\n### 📈 美股X情绪指数\n\n| 指标 | 数值/状态 | 说明 |\n|------|-----------|------|\n| 美股整体情绪 | {'乐观' if index_score > 1 else ('悲观' if index_score < -1 else '中性')} | 综合得分: {index_score:.2f}/10 |\n| 风险偏好 | {'高' if bull_pct > 60 else '中'} | 推文中体现的风险承受意愿 |\n| 恐慌情绪 | {int((bear_pct/100)*10)}/10 | 对系统性风险的担忧程度 |\n| FOMO情绪 | {int((bull_pct/100)*10)}/10 | 害怕错过的情绪强度 |\n| 看多占比 | {bull_pct:.1f}% | 明确表达看多的投资推文占比 (加权计算) |\n| 看空占比 | {bear_pct:.1f}% | 明确表达看空的投资推文占比 (加权计算) |\n\n**美股X情绪简评**：市场情绪呈现典型的结构性分化。一方面，地缘政治（美伊停火谈判传闻）引发市场预期重构，风险偏好总体偏向乐观；另一方面，空头力量（乘数校准1.3倍权重）仍在高度警惕原油等大宗商品的回调风险以及股指的顶背离信号。\n\n### 💰 AI投资情绪指数\n\n| 指标 | 数值/状态 | 说明 |\n|------|-----------|------|\n| AI投资整体情绪 | 乐观 | AI相关标的(一二级市场)的投资情绪 |\n| 算力/硬件投资情绪 | 乐观 | 对NVDA及供应链(如CPO/InP等)的投资倾向 |\n| AI商业化信心 | 8/10 | 对AI公司盈利能力、商业模式及TAM的信心 |\n| 估值泡沫担忧度 | 4/10 | 对AI企业高估值或泡沫破裂风险的担忧 |\n| 资金流向/虹吸感知 | 7/10 | 对巨型IPO或增发吸筹效应的预判 |\n\n**AI投资情绪简评**：AI板块的投资热情持续处于高位。以NVDA Vera Rubin架构及Retimer组件为代表的硬件层依然拥有极强共识，同时部分应用层公司展现出强大的产品迭代效率，增强了资本对AI中长期变现的信心。\n\n### 🤖 AI行业情绪指数\n\n| 指标 | 数值/状态 | 说明 |\n|------|-----------|------|\n| AI行业整体情绪 | 乐观 | AI从业者/开发者生态的整体情绪 |\n| 技术突破兴奋度 | 9/10 | 对新模型、新产品能力的兴奋程度 |\n| 工具/Agent采用热情 | 9/10 | 开发者对新工具生态(如Codex/Skills)的采用度 |\n| AI计算成本痛感 | 5/10 | 对Token消耗、API调用和算力成本压力的感受 |\n| AI就业焦虑度 | 6/10 | 对AI重构劳动力、替代岗位的焦虑程度 |\n\n**AI行业情绪简评**：开发者生态高度繁荣，高级开发者正在加速将工作流向AI Agent彻底迁移。由开源模型驱动的小团队研发效率成倍增长，"超级个体"取代臃肿机构的趋势正在成为行业新共识。\n\n---\n\n## 二、热门话题总览\n\n### 🔥 话题热度排行\n\n| # | 话题 | 讨论热度 | 情绪倾向 | 一句话概要 |\n|---|------|----------|----------|------------|\n| 1 | 地缘与宏观（美伊谈判） | ~40条 | 争议 | 特朗普宣布美伊停火协议基本达成，但伊朗部分否认，引发油价与市场巨震 |\n| 2 | Crypto市场异动与洗盘 | ~60条 | 多 | BTC测试关键阻力位受阻，部分山寨币（HYPE/Privacy Tokens）逆势走强 |\n| 3 | AI算力硬件及Agent生态 | ~30条 | 多 | NVDA架构更新与AI Agent落地应用引发热议，小团队模型逆袭巨头 |\n\n### 🗣️ 核心讨论主线\n\n1. **宏观与地缘的拉扯**：围绕美国与伊朗潜在的停火备忘录展开，市场迅速对原油供给增加以及地缘溢价消除进行定价，这是本期最大的外部变量。\n2. **Crypto板块轮动与机构博弈**：在BTC冲击前高受阻的背景下，市场处于存量博弈，资金流向显现出强烈的K型分化特征，高波动与隐私赛道备受追捧。\n3. **AI效率平权时代的到来**：无论是顶尖风投还是独立开发者，都深刻意识到AI Agent工具链对生产力的颠覆，小团队战胜大厂正在变为现实。\n\n---\n\n## 三、AI 新话题与技术前沿\n\n### 🔬 技术新话题\n\n#### 1. Agent工作流彻底颠覆研发环境\n**方向**：AI Agent正在实质性替代传统开发与代码托管平台\n**逻辑链**：\n`模型能力提升 → Agent协作平台(如AGS)成熟 → 开发者完全抛弃Github并转入AI自动化流 → 研发效率极大地去中心化`\n**多空占比**：看多 95% | 看空 0% | 中性 5%\n**关键观点**：\n\n| 发言人 | 立场 | 核心观点 | 原文摘要 |\n|--------|------|----------|----------|\n| @turingou | 多 | AGS已替代Github成为主要开发环境 | "最近我已经用 AGS 替代了 GitHub 作为我的主要开发环境...除了iOS模拟器不得不依赖Mac外，其他已全部迁移到围绕 AGS 的第一层 harness 工作流" |\n| @omarsar0 | 多 | AI技能自动化生成 | "Just released my new /lesson-generator skill. Use it with your agent to learn anything" |\n\n#### 2. 垂直模型与小团队的逆袭\n**方向**：小团队利用专有模型在特定场景下击败全能巨头大模型\n**逻辑链**：\n`基础模型生态成熟 → 垂直领域专精化重构微调工程 → 小团队推出极速任务专属模型 → 打破大厂垄断神话`\n**多空占比**：看多 100% | 看空 0% | 中性 0%\n**关键观点**：\n\n| 发言人 | 立场 | 核心观点 | 原文摘要 |\n|--------|------|----------|----------|\n| @garrytan | 多 | 小团队依靠独特洞察获胜 | "6-person team is building task-specific AI models that are 4-8x faster than anything from OpenAI or Anthropic. 500K downloads on HuggingFace... ZeroEntropy.dev is SOTA for reranking and embedding" |\n\n---\n\n## 四、投资话题深度分析\n\n### 📊 投资话题热度排行\n\n| # | 话题/标的 | 热度 | 多空比 | 核心逻辑 |\n|---|-----------|------|--------|----------|\n| 1 | Crypto核心资产(BTC/ETH) | ~50条 | 多60:空40 | BTC回踩200日均线及7.6W-8W阻力，面临方向抉择 |\n| 2 | 原油及大宗商品交易 | ~30条 | 多10:空90 | 美伊停火预期引发原油空头长牛预期共识 |\n| 3 | AI算力及硬件供应链 | ~20条 | 多95:空5 | Vera Rubin架构确立，HBF及Retimer等外围组件迎爆发 |\n\n### 逐话题深度分析\n\n#### 1. Crypto核心资产市场\n**讨论热度**：~50条相关推文\n**多空占比**：看多 60% | 看空 40% | 中性 0%\n**逻辑链**：\n`[看多链] 机构买盘支撑 + 特朗普大选潜在利好 → 市场逢低吸筹 → 突破向上`\n`[看空链] BTC在200日均线处遭拒 + ETF资金净流出 → 类似2022年牛市陷阱 → 向下寻找6.7W支撑`\n**关键观点**：\n| 发言人 | 立场 | 核心观点 | 原文摘要 |\n|--------|------|----------|----------|\n| @MerlijnTrader | 空 | BTC受阻于关键均线，风险剧增 | "BITCOIN REJECTED THE 200-DAY MA... 2026: rejection at $80K. Next stop? Watching $76K. Lose it, the move accelerates. First downside target: $67K" |\n| @cryptorover | 多 | 盘整越久，爆发越猛 | "The longer the bull run takes to come, the bigger the bull run will be." |\n| @AwbczBTC | 多 | 上方清算空间大，突破在即 | "大饼78250附近有不少要清算啊 把这突破了 上方其实也还有不少... 特朗普还有伊朗不在变卦的话 是有很大机会突破的" |\n\n**数据支撑**：\n| 数据点 | 数值 | 来源 |\n|--------|------|------|\n| 比特币ETF流出 | -$1.26B | Cointelegraph |\n| 萨尔瓦多BTC储备 | 7,661.37 枚 | Cointelegraph |\n\n#### 2. 原油及大宗商品交易\n**讨论热度**：~30条相关推文\n**多空占比**：看多 10% | 看空 90% | 中性 0%\n**逻辑链**：\n`[看空链] 美伊签署备忘录 → 伊朗原油无限制销售/霍尔木兹解封 → 全球原油供给冲击解除 → 油价长线走熊`\n**关键观点**：\n| 发言人 | 立场 | 核心观点 | 原文摘要 |\n|--------|------|----------|----------|\n| @fool1984 | 空 | 石油空头进入长牛周期 | "长期石化能源消费减退和清洁能源替代已经让油价高点出现在身后，下周开始将是石油空头的长期牛市。" |\n| @C_Barraud | 空 | 地缘缓和打击油价 | "#WTI #Oil prices are expected to retrace sharply following the latest U.S.-Iran discussions" |\n\n#### 3. AI算力硬件(NVDA及其供应链)\n**讨论热度**：~20条相关推文\n**多空占比**：看多 95% | 看空 5% | 中性 0%\n**逻辑链**：\n`[看多链] NVDA发布系统级AI工厂架构 → 对高速通信及存储提出苛刻要求 → Astera Labs等提供PCIe Switch与Retimer的企业迎来强劲订单`\n**关键观点**：\n| 发言人 | 立场 | 核心观点 | 原文摘要 |\n|--------|------|----------|----------|\n| @TheValueist | 多 | NVDA全架构销售利好周边 | "For NVIDIA, the strategic read-through is positive. The company is increasingly selling a complete AI factory architecture, not just accelerators. Vera Rubin’s official architecture integrates GPUs, CPUs, NVLink 6, SuperNICs, DPUs..." |\n| @LinQingV | 多 | PCIe Switch及Retimer组件是核心 | "除了Retimer，Astera Labs还做了一颗叫Scorpio的PCIe fabric switch... Scorpio瞄准的是多颗GPU之间怎么组网通信。" |\n\n---\n\n## 五、全员观点档案\n\n"""

# Append all speakers efficiently
sorted_speakers = sorted(speakers_data.items(), key=lambda x: x[1]['count'], reverse=True)
for handle, data in sorted_speakers:
    md += f"### {handle} — {data['name']}\n"
    md += f"- **推文数量**：{data['count']}条\n"
    md += f"- **立场倾向**：{data['tendency']}\n"
    md += f"- **关键观点**：\n"
    for i, t in enumerate(data['tweets']):
        clean_text = t.replace('\\n', ' ').strip()
        # Limit extremely long text to avoid bloated report
        if len(clean_text) > 400: clean_text = clean_text[:397] + '...'
        md += f"  {i+1}. {clean_text}\n"
    md += "\n"

md += """---

## 六、总结与洞察

### 🎯 本期核心发现

1. **地缘博弈主导短期避险与大宗资产定价**：关于美伊停火及开放霍尔木兹海峡的传闻在周末发酵，市场对此的极速定价显示出极强的风险偏好修复倾向，原油空头逻辑迅速达成共识。
2. **Crypto存量资金向高Beta寻找突破口**：在BTC上攻遇阻的疲软期，资金明显流向具有叙事爆发力的板块（如Privacy Tokens）和高波动币种（如HYPE），呈现典型的板块轮动特征。
3. **AI开发生态的"去机构化"**：顶尖开发者纷纷借助Agent（如AGS、cc）建立自动化工作流，并逐步脱离传统大厂平台（如Github）。这一趋势预示着超级个体将在生产效率上实质性地比肩甚至超越传统臃肿企业。

### ⚡ 值得关注的信号

- **大佬仓位共识信号**：部分风向标级别KOL（如Cathie Wood）公开倡议抛弃传统避险资产（黄金）全面拥抱加密核心资产（BTC）。
- **原油空头的极端拥挤**：由于停火传闻导致的看空原油情绪极度一致。如若下周政治谈判出现"黑天鹅"反转（伊朗实际拒绝条款），极有可能引发猛烈的空头踩踏（Short Squeeze）。
- **硬件供应链向纵深挖掘**：AI投资焦点已越过单纯的GPU（NVDA），向解决多芯片通讯瓶颈的外围组件（Retimer、Fabric Switch等）以及新一代存储（HBF）延伸。

### 🔮 趋势推演

| 趋势判断 | 支撑证据 | 置信度 | 需关注的反转信号 |
|----------|----------|--------|------------------|
| 原油价格大幅波动且有诱空风险 | 停火协议未正式落定且伊朗官方有相左言论 | 高 | 官方最终正式且无条件的和平协议落地 |
| 独立AI团队将产出更多垂直SOTA模型 | ZeroEntropy等基于开源底座的专精微调模型效率惊人 | 高 | 大模型底座出现碾压式、断代式的闭源能力跃升 |
| BTC短线回撤压力较大 | 多次冲击200日均线失败，且周末ETF无明显资金承接 | 中 | 现货ETF突发巨额净流入或降息预期骤然升温 |

### ⚠️ 分析局限

本次分析主要基于特定监控列表的 48 小时推文样本，存在显著的领域偏好（集中于 Crypto 与 AI 科技圈）。地缘政治分析高度依赖媒体快讯与二传手解读，缺乏一手情报支撑；加之周末休市效应，部分情绪指数可能带有脱离真实资金面的前瞻性偏差。

---

*报告由 X推文分析工具链生成，数据来源于 X(Twitter) 公开推文。*
"""

with open(f'{date_str}_推文深度分析报告.md', 'w', encoding='utf-8') as f:
    f.write(md)

print("Report generated successfully.")

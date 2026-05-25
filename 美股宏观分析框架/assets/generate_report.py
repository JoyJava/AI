# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
美股宏观诊断报告生成器 — V2 模版
用法：
  python3 generate_report.py [YYYY-MM-DD] [输出目录]

示例：
  python3 generate_report.py                          # 用今天日期，输出到当前目录
  python3 generate_report.py 2026-05-21               # 指定日期，输出到当前目录
  python3 generate_report.py 2026-05-21 ~/Documents  # 指定日期+目录

集成到 SKILL 工作流：
  1. 搜索最新指标数据（Exa）
  2. 更新 STAGES 列表中的 concl / col_now 字段
  3. 更新 CHART_JS 中最新数据点
  4. python3 generate_report.py $(date +%F) /你的输出路径
"""
import sys, os
from datetime import date as _date

DATE = sys.argv[1] if len(sys.argv) > 1 else _date.today().isoformat()
_out_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
OUT = os.path.join(_out_dir, f'{DATE}-综合诊断.html')

CSS = """
:root{--red:#dc2626;--orange:#ea580c;--yellow:#ca8a04;--green:#16a34a;--bg:#0f172a;--card:#1e293b;--border:#334155;--text:#e2e8f0;--muted:#94a3b8;--accent:#38bdf8;--purple:#8b5cf6;}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:-apple-system,'SF Pro Text','Helvetica Neue',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;}
.container{max-width:1360px;margin:0 auto;padding:20px;}
h1{font-size:1.8em;margin-bottom:8px;}
h2{font-size:1.4em;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid var(--accent);color:var(--accent);}
h3{font-size:1.1em;margin:20px 0 10px;color:#f1f5f9;}
.header{text-align:center;padding:40px 20px;border-bottom:1px solid var(--border);}
.header .verdict{font-size:2.5em;margin:16px 0;}
.badge{display:inline-block;padding:4px 12px;border-radius:12px;font-size:.85em;font-weight:600;margin:2px;}
.badge-red{background:rgba(220,38,38,.2);color:#fca5a5;border:1px solid rgba(220,38,38,.4);}
.badge-orange{background:rgba(234,88,12,.2);color:#fdba74;border:1px solid rgba(234,88,12,.4);}
.badge-yellow{background:rgba(202,138,4,.2);color:#fde047;border:1px solid rgba(202,138,4,.4);}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin:16px 0;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
@media(max-width:900px){.grid2{grid-template-columns:1fr;}}
table{width:100%;border-collapse:collapse;margin:12px 0;font-size:.9em;}
th{background:#1a2744;text-align:left;padding:10px 12px;border:1px solid var(--border);color:var(--accent);font-weight:600;vertical-align:top;}
td{padding:10px 12px;border:1px solid var(--border);vertical-align:top;}
tr:nth-child(even){background:rgba(255,255,255,.02);}
.dot-r,.dot-o,.dot-y,.dot-g{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle;}
.dot-r{background:var(--red);}.dot-o{background:var(--orange);}.dot-y{background:var(--yellow);}.dot-g{background:var(--green);}
.stage-indicator{display:flex;align-items:center;gap:4px;margin:16px 0;flex-wrap:wrap;}
.stage-box{min-width:82px;height:44px;padding:0 8px;display:flex;align-items:center;justify-content:center;border-radius:6px;font-size:.78em;font-weight:600;color:white;cursor:pointer;user-select:none;}
.stage-box:hover{transform:translateY(-2px);transition:transform .15s;}
.stage-arrow{color:var(--muted);font-size:.8em;}
.stage-box.red{background:rgba(220,38,38,.55);border:1px solid var(--red);}
.stage-box.orange{background:rgba(234,88,12,.55);border:1px solid var(--orange);}
.stage-box.yellow{background:rgba(202,138,4,.55);border:1px solid var(--yellow);}
.stage-box.active{box-shadow:0 0 0 2px var(--accent),0 0 16px rgba(56,189,248,.5);}
.split{display:grid;grid-template-columns:240px 1fr;gap:24px;margin:24px 0;}
@media(max-width:960px){.split{grid-template-columns:1fr;}}
.side-nav{position:sticky;top:16px;align-self:start;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:10px;max-height:calc(100vh - 32px);overflow-y:auto;}
.side-btn{display:flex;align-items:center;gap:10px;width:100%;text-align:left;padding:10px 12px;border:none;background:transparent;color:var(--text);cursor:pointer;border-radius:8px;margin-bottom:2px;font-family:inherit;font-size:.92em;transition:all .15s;border-left:3px solid transparent;}
.side-btn:hover{background:rgba(56,189,248,.1);}
.side-btn.active{background:rgba(56,189,248,.15);color:var(--accent);border-left-color:var(--accent);font-weight:600;}
.side-btn .num{display:inline-block;min-width:22px;height:22px;line-height:22px;border-radius:50%;background:#334155;color:white;text-align:center;font-size:.78em;font-weight:700;}
.side-btn.active .num{background:var(--accent);color:var(--bg);}
.content-area{min-width:0;}
.tab-panel{display:none;animation:fadeIn .2s ease;}
.tab-panel.active{display:block;}
@keyframes fadeIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.info{display:inline-block;width:16px;height:16px;line-height:14px;text-align:center;border:1px solid var(--muted);border-radius:50%;font-size:.7em;color:var(--muted);cursor:help;margin-left:4px;vertical-align:middle;font-weight:700;position:relative;}
.info:hover{background:var(--accent);color:var(--bg);border-color:var(--accent);}
.info:hover::after{content:attr(data-tip);position:absolute;left:50%;top:calc(100%+8px);transform:translateX(-50%);background:#0b1220;color:var(--text);border:1px solid var(--accent);padding:10px 14px;border-radius:6px;font-size:.85em;width:300px;text-align:left;line-height:1.5;z-index:1000;box-shadow:0 8px 24px rgba(0,0,0,.7);white-space:normal;}
.info:hover::before{content:'';position:absolute;left:50%;top:calc(100%+3px);transform:translateX(-50%);border:6px solid transparent;border-bottom-color:var(--accent);z-index:1001;}
a.src{color:var(--text);text-decoration:none;border-bottom:1px dotted var(--accent);}
a.src:hover{color:var(--accent);}
.verify{font-size:.7em;padding:2px 6px;border-radius:4px;font-weight:600;white-space:nowrap;}
.v-ok{background:rgba(22,163,74,.2);color:#86efac;border:1px solid rgba(22,163,74,.4);}
.v-warn{background:rgba(202,138,4,.2);color:#fde047;border:1px solid rgba(202,138,4,.4);}
.earnings-mark{color:var(--accent);margin-right:2px;}
.era3{background:rgba(139,92,246,.2);color:#c4b5fd;border:1px solid rgba(139,92,246,.4);padding:1px 6px;border-radius:4px;font-size:.7em;margin-left:4px;font-weight:600;}
.lead-tag{display:inline-block;font-size:.68em;padding:1px 5px;border-radius:3px;font-weight:700;margin-right:4px;vertical-align:middle;}
.lead-lead{background:rgba(56,189,248,.2);color:#7dd3fc;border:1px solid rgba(56,189,248,.4);}
.lead-sync{background:rgba(139,92,246,.2);color:#c4b5fd;border:1px solid rgba(139,92,246,.4);}
.lead-lag{background:rgba(148,163,184,.2);color:#cbd5e1;border:1px solid rgba(148,163,184,.4);}
.stage-header{padding:18px 22px;border-radius:12px 12px 0 0;}
.stage-header.red{background:rgba(220,38,38,.15);border:1px solid rgba(220,38,38,.4);border-bottom:none;}
.stage-header.orange{background:rgba(234,88,12,.15);border:1px solid rgba(234,88,12,.4);border-bottom:none;}
.stage-header.yellow{background:rgba(202,138,4,.15);border:1px solid rgba(202,138,4,.4);border-bottom:none;}
.stage-title{font-size:1.25em;margin-bottom:6px;}
.stage-q{color:var(--muted);font-size:.95em;}
.stage-body{border:1px solid var(--border);border-top:none;border-radius:0 0 12px 12px;padding:20px 22px;background:var(--card);}
.vc{display:grid;gap:10px;margin-bottom:16px;}
.vc-card{padding:14px 16px;border-radius:8px;border-left:4px solid;}
.vc-card.concl{background:rgba(56,189,248,.08);border-left-color:var(--accent);}
.vc-card.logic{background:rgba(139,92,246,.08);border-left-color:var(--purple);}
.vc-card.action{background:rgba(234,88,12,.08);border-left-color:var(--orange);}
.vc-card strong.lbl{display:block;margin-bottom:6px;font-size:.9em;}
.vc-card.concl strong.lbl{color:var(--accent);}
.vc-card.logic strong.lbl{color:#c4b5fd;}
.vc-card.action strong.lbl{color:#fdba74;}
.vc-card ul{margin:4px 0 0 18px;}
.vc-card li{margin-bottom:4px;}
.col-2000{background:rgba(139,92,246,.05);}
.col-2008{background:rgba(220,38,38,.05);}
.col-now{background:rgba(56,189,248,.1);font-weight:600;}
.cmp-table th:first-child{width:30%;}
.cmp-table th:nth-child(2){width:17%;}
.cmp-table th:nth-child(3){width:17%;}
.cmp-table th:nth-child(4){width:28%;}
.cmp-table th:nth-child(5){width:8%;}
.important{background:rgba(220,38,38,.15);border:1px solid rgba(220,38,38,.3);border-radius:8px;padding:16px;margin:16px 0;}
.triggered{background:rgba(220,38,38,.25);border:2px solid var(--red);border-radius:8px;padding:14px;margin:10px 0;}
.diff-worse{color:#fca5a5;font-weight:600;}
.diff-better{color:#86efac;font-weight:600;}
.diff-same{color:var(--muted);}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:20px 0 8px;}
.chart-grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:20px 0 8px;}
@media(max-width:900px){.chart-grid,.chart-grid-3{grid-template-columns:1fr;}}
.cw{background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:10px;padding:14px 14px 10px;}
.cw h4{font-size:.75em;color:var(--muted);margin:0 0 8px;text-transform:uppercase;line-height:1.4;}
.cw canvas{display:block;max-height:190px;}
.chart-legend{display:flex;gap:14px;flex-wrap:wrap;font-size:.76em;color:var(--muted);margin:6px 0 0;}
.ldot{width:9px;height:9px;border-radius:2px;flex-shrink:0;display:inline-block;margin-right:4px;vertical-align:middle;}
"""

# ──────────────────────────────────────────────
# 阶段数据（11阶段，每阶段 2 或 3 个图）
# (id, lamp, color, title, q, concl, logic[], action[], table_rows[], charts[])
# chart = (canvas_id, title)
# ──────────────────────────────────────────────
STAGES = [
  ("t1","🟡","yellow","阶段1：收入端压力","底层是否还有足够现金流入？",
   "<strong>4月非农05-08实际+115K（远超预期+65K）</strong>，3月上修至+185K（vs初值+178K），2月下修至-156K（vs-133K）。失业率持平4.3%——<strong>但靠的是劳动力参与率下降</strong>。2-4月3个月均值仅<strong>+48K</strong>（前3月61K），动能持续走弱。3月JOLTS：招聘率从2月3.1%反弹至<strong>3.5%</strong>，辞职率微升至<strong>2.0%</strong>。<strong>T3未触发（非负），T1短期解除（招聘率>3%）。但'连续两月正增'被市场解读为软着陆，框架视角看是'底层仍在被慢慢放出血'</strong>。",
   ["4月+115K表面超预期，但2月被下修到-156K——3个月均值48K，远低于人口增长盈亏平衡的~80K；","失业率持平4.3%靠劳动力参与率下降——'隐性失业'增加；","辞职率2.0%连续<strong>11个月</strong>≤2.0% — 工人依然不敢换工作（2024年初约2.2%）；","就业增长仅集中在医疗/运输仓储/零售贸易，联邦政府继续减员；","时薪YoY +3.6%，低于预期——工资/通胀缓冲减弱。"],
   ["T1短期解除（招聘率3.5%>3%）；T3未触发（非农连续2月正）；","但底层趋势仍指向阶段1压力上升：3M均值48K + 联邦减员 + 隐性失业；","下一关键节点：6月2日4月JOLTS发布，6月5日5月非农；","5月21日WMT Q1 FY27财报已公布，证实高收入向下买入且低收入预算受限，需密切关注消费向阶段4g-4h固化。"],
   [("领先","lead-lead","JOLTS辞职率","~2.5%","2.2%→1.4%","<strong>2.0%（Mar，连续11月≤2.0%）</strong>","✅","v-ok","https://www.bls.gov/news.release/jolts.nr0.htm"),
    ("领先","lead-lead","JOLTS招聘率","~4%+","4%→3%","<strong>3.5%（Mar，T1暂时解除）</strong>","✅","v-ok","https://www.bls.gov/news.release/jolts.nr0.htm"),
    ("滞后","lead-lag","失业率U-3","4.0%→6.3%","4.7%→10.0%","<strong>4.3%（Apr，靠劳动参与率下降稳住）</strong>","✅","v-ok","https://www.bls.gov/news.release/empsit.nr0.htm"),
    ("滞后","lead-lag","非农月度新增","正增长","2008Q1转负","<strong>Feb -156K / Mar +185K / Apr +115K（3M均值仅48K）</strong>","✅","v-ok","https://www.bls.gov/news.release/empsit.nr0.htm")],
   [("c1a","① JOLTS 辞职率（%）— 领先指标，黄虚=T1触发线3.0%"),
    ("c1b","② 失业率 U-3（%）— 滞后指标，亮红时已是危机中期")]),

  ("t2","🔴","red","阶段2：储蓄耗尽","没有流入之后，还有多少家底能撑？",
   "个人储蓄率降至<strong>3.5%</strong>（2008以来最低）。家庭过去12个月动用约<strong>4700亿美元</strong>维持消费。SF Fed超额储蓄追踪停更，底层50%早已耗尽。K型分化：2026年税退主要惠及中高收入，底层获益极少。",
   ["3.5%是警戒水位——但这是全体平均，高收入严重拉高了均值；","底层耗尽→被迫举债（传导阶段3）；","401(k)提前支取处历史高位，是底层'最后手段'；","2008年低储蓄是全体低，当前是K�  ("t4","🔴","red","阶段4：消费降级 ⚡T4触发","砍哪些支出？",
   "<strong>MCD Q1 2026（5月7日发布）US SSS +3.9%</strong>（vs Q4'25 +7%大幅减速），但CEO Kempczinski明确警告Q2将出现<strong>'meaningful deceleration'</strong>——'消费者焦虑加剧'，CFO Borden直言'低收入消费者承压，钱包里钱很有限'。MCD推出$3菜单/$4早餐套餐应对低端流失。WMT Q4 FY26 CEO Furner已明确触发T4'发薪日'措辞。<strong>同期WHR下调全年EPS指引并暂停股息，CEO称'recession-level industry decline'；SHAK崩跌-28%</strong>。<strong>5月21日发布的 WMT Q1 FY27 财报已证实低收入客群财务状况'特别受限'（remained particularly constrained），高收入家庭（>10万）由于预算压缩向下买入（Trading Down）</strong>。",
   ["MCD 'meaningful deceleration'es Q1业绩公告中的明确警告——历史上CEO主动用此词通常领先消费衰退1-2季度；","白电（WHR）'衰退级行业下降' + 餐饮（SHAK -28%）= 中产开始砍耐用品 + 砍外食，4阶段在固化向中段；","MCD推$3菜单替代BOGO = 价格点下移10-30%，反映低端客群已无法承担$5菜单；","油价从$126回落至$95-100缓解低端能源压力，但不解决K型分化结构。"],
   ["<strong>仓位40-50%维持</strong>；MCD警告确认K型恶化——不是'减仓最后窗口'而是'窗口已经在关'；","减持DG/DLTR/SHAK（底层+中产快餐双崩）；","<strong>5月21日 WMT Q1 FY27 财报已证实低收入承压且发薪日效应固化，维持40-50%防御仓位，若进一步恶化随时准备降至30-40%</strong>；","SNAP若连续3月增→进入4h，加速减仓。"],��层'最后手段'压力")]),

  ("t3","🔴","red","阶段3：举债求生","储蓄没了，借了多少？借了什么？",
   "2026 Q1 信用卡余额为<strong>$1.25万亿</strong>（环比季节性下降$25B，但同比仍增长5.9%）。严重逾期流入率（90天+）在 2026 Q1 为<strong>7.10%</strong>（高于去年同期的7.04%）。家庭总债务再创历史新高至<strong>$18.80万亿</strong>（环比小幅增加$18B）。<strong>季节性余额下降并没有掩盖底层信用质量的压力，严重逾期流入率仍旧维持在历史相对高位。</strong>",
   ["2026 Q1 信用卡余额 $1.25T 发生季节性回落，但同比 +5.9% 的扩张速度在紧缩周期下依然高企；","90天+严重逾期流入率 7.10%（Q1 2025 同期为 7.04%），微弱的环比回落不足以构成质量改善的拐点；","家庭总债务 $18.80T 再创历史最高，反映负债压力依然沉重；","影子信贷（如 BNPL 购买食物占比高）等未统计债务继续构成了系统外的'暗债'。"],
   ["<strong>密切关注 Q2 数据</strong>，随着发薪日效应进一步显现，逾期率可能在夏季再度上行；","监测学生贷严重逾期情况（Q4 已跳升至 16.19%），还款对底层消费力的剥夺效应依然在持续；","规避非必需消费品以及次级信贷敞口较大的金融机构。"],
   [("同步","lead-sync","信用卡总余额","~$0.7T","~$1.0T","<strong>$1.25T（Q1 2026，同比+5.9%）</strong>","✅","v-ok","https://www.newyorkfed.org/microeconomics/hhdc"),
    ("同步","lead-sync","信用卡90天+逾期率","~4%","峰值~10%+","<strong>7.10%（Q1 2026流入率，同期2025 7.04%）</strong>","✅","v-ok","https://www.newyorkfed.org/microeconomics/hhdc"),
    ("滞后","lead-lag","家庭总债务","~$7T","$12T（房贷）","<strong>$18.80T（Q1 2026历史新高）</strong>","✅","v-ok","https://www.newyorkfed.org/microeconomics/hhdc")],
   [("c3a","① 信用卡总余额（万亿$）— 规模三周期对比"),
    ("c3b",'② 信用卡 90天+ 流入严重逾期率（flow into, 年化%）— 质量恶化核心信号')]),

  ("t4","🔴","red","阶段4：消费降级 ⚡T4触发","砍哪些支出？",
   "<strong>MCD Q1 2026（5月7日发布）US SSS +3.9%</strong>（vs Q4'25 +7%大幅减速），但CEO Kempczinski明确警告Q2将出现<strong>'meaningful deceleration'</strong>——'消费者焦虑加剧'，CFO Borden直言'低收入消费者承压，钱包里钱很有限'。MCD推出$3菜单/$4早餐套餐应对低端流失。WMT Q4 FY26 CEO Furner已明确触发T4'发薪日'措辞。<strong>同期WHR下调全年EPS指引并暂停股息，CEO称'recession-level industry decline'；SHAK崩跌-28%</strong>。WMT Q1 FY27财报<strong>5月15日</strong>是关键观察。",
   ["MCD 'meaningful deceleration'是Q1业绩公告中的明确警告——历史上CEO主动用此词通常领先消费衰退1-2季度；","白电（WHR）'衰退级行业下降' + 餐饮（SHAK -28%）= 中产开始砍耐用品 + 砍外食，4阶段在固化向中段；","MCD推$3菜单替代BOGO = 价格点下移10-30%，反映低端客群已无法承担$5菜单；","油价从$126回落至$95-100缓解低端能源压力，但不解决K型分化结构。"],
   ["<strong>仓位40-50%维持</strong>；MCD警告确认K型恶化——不是'减仓最后窗口'而是'窗口已经在关'；","减持DG/DLTR/SHAK（底层+中产快餐双崩）；","<strong>5月15日WMT Q1 FY27财报 — 若CEO Furner再次升级'发薪日'措辞，立即降至30-40%</strong>；","SNAP若连续3月增→进入4h，加速减仓。"],
   [],
   [("c4a","① 储蓄率代理（%）+WMT触发标注（▲红=2007，▲黄=2026）"),
    ("c4b","② 可选品 vs 必需品消费指数（100=平衡）— 降级阶梯量尺")]),

  ("t5","🟠","orange","阶段5：系统内信用压力","还在系统里的人，还能撑多久？",
   "COF Q1 2025 Domestic Card NCO <strong>6.14%</strong>（+24bp YoY）；JPM Card NCO指引<strong>~3.4%</strong>（Q1 2026稳定）；AXP NCO ~2.3%（低位，K型对照）。<strong>关键反直觉：信用卡流入严重逾期率Q4 2025=7.13%（2024同期7.18%，表面改善），而银行NCO表面改善——幸存者偏差：次级被踢出分母后系统内质量'变好'了。</strong>",
   ["逾期率=逾期余额÷总余额——次级被踢出后分母缩小，比率'好看'；","NCO（核销）比逾期率可靠——是银行认赔，不允许粉饰；","AXP vs COF：AXP高端客群维持低位→K型分化量尺；","T5触发（JPM/BAC NCO加速）目前未触发——是唯一重要缓冲。"],
   ["不被COF/SYF'改善'叙事迷惑，交叉验证阶段6和7；","若AXP NCO开始上升→压力传至高端，即刻降仓；","T5目前未触发，监控Q2数据。"],
   [("同步","lead-sync","COF Domestic Card NCO","~6%","峰值~10%","<strong>6.14%（Q1 2025）</strong>","✅","v-ok","https://investor.capitalone.com/"),
    ("同步","lead-sync","JPM Card NCO（Q1 2026）","~5%","~10%","<strong>~3.4%（稳定）</strong>","✅","v-ok","https://www.jpmorganchase.com/ir/quarterly-earnings"),
    ("同步","lead-sync","AXP NCO（K型对照）","~5%","~8%","<strong>~2.3%（低位，高端尚稳）</strong>","⚠️","v-warn",""),
    ("同步","lead-sync","汽车贷60天+逾期率","~2%","峰值~4%","<strong>2.97%（Q1 2026严重逾期流入率，平稳）</strong>","✅","v-ok","https://www.newyorkfed.org/microeconomics/hhdc")],
   [("c5a","① COF Domestic Card NCO（%）— 次级信用卡压力"),
    ("c5b","② AXP NCO（%）— K型高端对照组，参考线=COF当前6.14%"),
    ("c5c","③ 汽车贷 60天+ 逾期率（%）— 分母稳定更可靠")]),

  ("t6","🔴","red","阶段6：被踢出系统","银行对次级借款人是否还开放？",
   "次级发卡率（FICO&lt;660）Q4 2025小幅回升至<strong>17.8%</strong>（上次16.4%），为近两年最高——轻微改善，但仍意味着约<strong>30%次级借款人被排除在正规信贷体系外</strong>。被排除者流向BNPL/EWA/当铺——不在Fed统计里=真正的'暗债'。",
   ["此指标直接量化幸存者偏差大小：被踢出越多，阶段5的'改善'越虚假；","SLOOS净收紧25-30%，显著但未达2008极端（&gt;40%）；","R1缓和触发器（&gt;20%）距17.8%还有2.2pp，未触发；","17.8%回升是唯一好消息。"],
   ["R1未触发，不考虑加仓；","SLOOS若净收紧&gt;40%→2008级别极端，直接降仓；","继续追踪费城联储季度报告。"],
   [("领先","lead-lead","次级发卡率FICO&lt;660","&gt;25%","先宽后骤紧","<strong>17.8%（Q4 2025，略升）</strong>","✅","v-ok","https://fred.stlouisfed.org/series/RCCCOACTPCTSCORELT660"),
    ("领先","lead-lead","SLOOS净收紧比例","~10%","&gt;40%","<strong>25-30%（显著未极端）</strong>","✅","v-ok","https://www.federalreserve.gov/data/sloos.htm")],
   [("c6a","① 次级发卡率 FICO&lt;660（%）— 绿虚=R1缓和线20%，红虚=排斥线15%"),
    ("c6b","② SLOOS 消费贷净收紧比例（%）— 红虚=2008极端线40%")]),

  ("t7","🔴","red","阶段7：硬资产损失","汽车被收回、房屋止赎了吗？",
   "汽车收回量2025年拍卖渠道~185万辆，实际总量估算<strong>~400万辆</strong>——<strong>远超2008-2009峰值210万辆</strong>。房屋止赎~35万件（低位）——<strong>当前是汽车贷危机而非房贷危机。</strong>",
   ["物理事件无法统计美化，绝对数没有分母扭曲；","与阶段5（汽车贷逾期2.95%稳定）背离：72-84月长贷款期压缩逾期窗口，逾期直接跳到收回；","汽车负资产比例~25%历史高位——二手车价再跌10%就是新一波抛售；","Cox官方只统计拍卖渠道（182万），行业数据约低估2.2倍。"],
   ["避开KMX/CVNA（拍卖供给过剩）；","ALLY等汽车金融股高度警惕；","关注Manheim批发指数——若跌幅扩大则负资产比例进一步恶化。"],
   [("同步","lead-sync","汽车收回量（年化）","~150万/年","峰值~210万","<strong>拍卖~185万；实际~400万</strong>","⚠️","v-warn","https://curepossession.com"),
    ("同步","lead-sync","房屋止赎量","低位","峰值~280万/年","<strong>~35万/年（低位）</strong>","✅","v-ok","https://www.attomdata.com"),
    ("领先","lead-lead","汽车负资产比例","~10%","~15%","<strong>~25%（历史高位）</strong>","⚠️","v-warn","")],
   [("c7a","① 汽车收回量（万辆/年）— 最诚实的物理信号，红虚=2008峰值210万"),
    ("c7b","② 房屋止赎启动量（万件/年）— 当前不是房贷危机")]),

  ("t8","🔴","red","阶段8：正式退出（破产）⚡T6触发","从'挣扎求生'到'彻底放弃'有多少人？",
   "2025全年<strong>574,314件</strong>（美国法院），同比+11%，超T6阈值60万。Ch.7（清算型）+15%，Ch.13（重组型）+6%——<strong>Ch.7增速更快=越来越多人从'挣扎'走向'绝望'</strong>。12月月环比+21%（Ch.7+24%）。企业破产Ch.11创2010以来新高。",
   ["Ch.7（清算）=彻底放弃；Ch.13（重组）=还在挣扎——前者增速更快=情况恶化；","12月月环比+21%：若2026年月均&gt;5万件，年化将破70万；","企业Ch.11创2010新高=阶段4（消费降级）的延迟反应。"],
   ["T6已触发；月度跟踪uscourts.gov；","Ch.7占比若突破65%=绝望升级，加速减仓；","避开高杠杆零售/餐饮ETF（XRT等）。"],
   [("同步","lead-sync","破产申请年化","~130万（高基数）","峰值~150万","<strong>574,314（2025全年，+11%）</strong>","✅","v-ok","https://www.uscourts.gov/statistics-reports/bankruptcy-filings-statistics"),
    ("同步","lead-sync","Ch.7清算型占比","~70%","~72%","<strong>62.1%（上升中）</strong>","✅","v-ok","https://www.uscourts.gov/statistics-reports/bankruptcy-filings-statistics"),
    ("领先","lead-lead","12月月环比增速","持平","月度+15-20%","<strong>+21%（Ch.7 +24%）</strong>","✅","v-ok","https://www.abi.org")],
   [("c8a","① 个人破产年化（万件）— 黄虚=T6触发线60万"),
    ("c8b","② Ch.7 清算型占比（%）— 绝望程度，红虚=升级线65%")]),

  ("t9","🟠","orange","阶段9：银行端暴露","损失传到银行资产负债表了吗？",
   "JPM Q1 2026稳健：净收入$165亿（+13%），全公司NCO $23亿（持平），<strong>ACL建仓仅$191M</strong>（远低于Q1 2025的$973M），Card NCO指引维持3.4%。大小银行核销倍数<strong>2.36x</strong>（严重K型分化）。<strong>大行稳健是当前最重要缓冲；银行杠杆10-15x是最大结构性保护。</strong>",
   ["ACL建仓从$973M→$191M大幅放缓，是相对乐观信号但方向仍在建仓；","大小银行倍数2.36x（历史正常1.5-2.0x）——严重分化持续；","杠杆10-15x=Dodd-Frank后最重要保护——这是当前与2008最大区别；","CRE（商业地产）是新风险来源，非2008房贷危机重演。"],
   ["大银行可暂持但减至标配；减持区域银行ETF（KRE）；","下季度ACL若重新&gt;$5亿加速建仓→T5接近触发；","关注FDIC季度报告小银行倒闭数。"],
   [("领先","lead-lead","JPM ACL/Loans率","~1.5%","峰值~3%","<strong>~1.7%（建仓放缓）</strong>","✅","v-ok","https://www.jpmorganchase.com/ir/quarterly-earnings"),
    ("同步","lead-sync","大小银行核销倍数","~1.5x","~2.0x","<strong>2.36x（严重K型分化）</strong>","✅","v-ok","https://www.fdic.gov/analysis/quarterly-banking-profile/"),
    ("滞后","lead-lag","银行杠杆倍数","15-20x","30-40x","<strong>10-15x（最重要结构保护）</strong>","✅","v-ok","")],
   [("c9a","① JPM ACL/Loans 准备金率（%）— 银行内部前瞻预测"),
    ("c9b","② 大小银行核销倍数（x）— K型分化强度，红虚=警戒线2.5x")]),

  ("t10","🟠","orange","阶段10：实体经济反馈","宏观指标是否确认衰退开始？",
   "LEI 4月2025单月-1.0%（2023年3月以来最大），6M跌幅<strong>-2.0%</strong>——Conference Board：'出现增长预警信号，但未触发衰退信号'。ISM制造业PMI<strong>48.7%</strong>（4月，新订单三连跌）。2025年GDP预测从2.8%降至<strong>1.6%</strong>。收益率曲线2024年底解除倒挂，<strong>处于衰退高危窗口第5个月</strong>。",
   ["LEI -2.0%/6M进入增长预警区；关税冲击Q3将充分显现；","收益率曲线：历史上倒挂解除后12-18个月衰退概率&gt;80%，当前第5个月；","2月非农-133K：伊朗冲突扰动（框架外部冲击盲区）；","FedEx多次下调指引=货运量萎缩，2007年式早期信号。"],
   ["5月8日4月非农是关键——再负则T3接近触发；","关税冲击Q3充分显现；不要赌软着陆。"],
   [("领先","lead-lead","LEI（6M变化）","仍上升","持续下降&gt;6%","<strong>-2.0%/6M（增长预警）</strong>","✅","v-ok","https://www.conference-board.org/topics/us-leading-indicators"),
    ("同步","lead-sync","ISM制造业PMI","&lt;45","&lt;40","<strong>48.7%（Apr，三连跌）</strong>","✅","v-ok","https://www.ismworld.org"),
    ("领先","lead-lead","10Y-2Y收益率曲线","2000初倒挂","2007解除→衰退","<strong>2024底解除（高危窗口第5月）</strong>","✅","v-ok","https://fred.stlouisfed.org/series/T10Y2Y"),
    ("滞后","lead-lag","非农就业","正增长","2008Q1转负","<strong>Feb -133K / Mar +178K</strong>","✅","v-ok","https://www.bls.gov/news.release/empsit.nr0.htm")],
   [("c10a","① ISM 制造业 PMI — 绿虚=荣枯线50，跌破40=强衰退信号"),
    ("c10b","② 非农月度新增就业（万人）— 红虚=零增长线，连负=T3触发")]),

  ("t11","🟡","yellow","阶段11：市场重定价（⚠️黄灯=最危险的假稳）","市场有没有在价格中反映前10个阶段的恶化？",
   "HY利差5月11日<strong>279bp</strong>（5/8非农数据后短暂扩至281bp，11日回落到279bp——市场对'两月连正非农'解读为软着陆确认，<strong>背离继续</strong>）。VIX <strong>17.08</strong>，从3月27日峰值31跌至当前——伊朗MOU临近+科技股超买推动。S&P 500 7,398（上周+2.36%）。CAPE 36+。<strong>但下游警报频发：</strong>WHR-13%/SHAK-28%/MCD警告Q2恶化。这是教科书式的'市场最后乐观窗口'——基本面vs价格历史上最大背离之一。框架历史对照：2007 Q1 HY利差250bp、VIX 12，到2008雷曼还有5-6季度。",
   ["HY 279bp：市场为软着陆定价，忽视前10阶段恶化；MCD CEO直接警告Q2恶化时市场涨2.36%——典型背离；","基本面vs市场背离历史上最多持续6-18个月——'连续两月正非农'让市场再延展；","VIX从45→17：不是'没事了'，而是'更脆弱了'——VIX/3M VIX = 0.84 contango连续23天；","CAPE 36+：估值+信用双重风险，历史上从未同时出现。"],
   ["<strong>维持仓位40-50%，不要被本周市场+2.36%反弹诱导加仓</strong>；","HY利差从279bp扩大至350bp+ → 市场开始重新定价，窗口正式关闭；","若WMT Q1 FY27（5月15日）确认低端进一步恶化 → 立即减至30-40%；","Mag 7财报季若3家+下调指引→科技撑盘力量消失。"],
   [("领先","lead-lead","HY信用利差","350-600bp","峰值2000bp+","<strong>279bp（5/11，历史极端背离）</strong>","✅","v-ok","https://fred.stlouisfed.org/series/BAMLH0A0HYM2"),
    ("同步","lead-sync","VIX恐慌指数","20→40+","12→80+","<strong>17.08（5/11，3月峰值31已快速回落）</strong>","✅","v-ok","https://www.cboe.com"),
    ("同步","lead-sync","CAPE席勒市盈率","44.2x（历史顶）","27x","<strong>36+（接近2000年）</strong>","✅","v-ok","https://www.multpl.com/shiller-pe")],
   [("c11a","① CAPE 席勒市盈率（倍）— 红虚=泡沫警戒线35x"),
    ("c11b","② HY 信用利差（bp）— 橙虚=衰退定价500bp，红虚=危机1000bp")]),
]

def make_table(rows):
    if not rows:
        return ""
    h = '<table class="cmp-table"><tr><th>指标</th><th>2000泡沫</th><th>2008危机</th><th>当前（2026-04）</th><th>核实</th></tr>'
    for lead_text, lead_cls, name, c2000, c2008, cnow, sym, vcls, href in rows:
        ls = f'<a class="src" href="{href}" target="_blank">' if href else ''
        le = '</a>' if href else ''
        h += (f'<tr><td><span class="lead-tag {lead_cls}">{lead_text}</span>{name}</td>'
              f'<td class="col-2000">{c2000}</td><td class="col-2008">{c2008}</td>'
              f'<td class="col-now">{ls}{cnow}{le}</td>'
              f'<td><span class="verify {vcls}">{sym}</span></td></tr>')
    return h + '</table>'

def make_charts_html(charts):
    n = len(charts)
    cls = "chart-grid-3" if n == 3 else "chart-grid"
    inner = ''.join(f'<div class="cw"><h4>{t}</h4><canvas id="{cid}"></canvas></div>' for cid, t in charts)
    return f'<div class="{cls}">{inner}</div>'

def make_stage(s):
    sid, lamp, color, title, q, concl, logic, action, rows, charts = s
    logic_items = ''.join(f'<li>{i}</li>' for i in logic)
    action_items = ''.join(f'<li>{i}</li>' for i in action)
    table_html = make_table(rows)
    charts_html = make_charts_html(charts)

    extra = ""
    if sid == "t4":
        extra = """
<div class="triggered"><strong>🔴 T4触发（2026-02-19）</strong> — WMT CEO：<em>"households managing spending <strong>paycheck to paycheck</strong>"</em><br>
框架行动：消费升级到阶段4g，<strong>仓位立即降10%</strong>。
来源：<a class="src" href="https://www.fool.com/earnings/call-transcripts/2026/02/19/walmart-wmt-q4-2026-earnings-call-transcript/" target="_blank">🏛️ WMT Q4 FY26 财报电话会 ✅</a></div>
<table><tr><th>阶段</th><th>观察公司</th><th>信号</th><th>当前状态</th></tr>
<tr><td>4b 外食</td><td>MCD vs CMG</td><td>US SSS</td><td>MCD负/CMG正（K型早中期）</td></tr>
<tr><td>4e 降级业态</td><td>WMT</td><td>高收入流入</td><td>&gt;10万家庭占主要增量</td></tr>
<tr><td>4f 极端降级</td><td>DG/DLTR</td><td>SSS</td><td>底层客群持续承压</td></tr>
<tr><td><strong>4g 只买食物</strong></td><td><strong>WMT CEO</strong></td><td><strong>发薪日效应</strong></td><td><strong class="diff-worse">🔴 已触发 2026-02-19</strong></td></tr>
<tr><td>4h 食品援助</td><td>USDA SNAP</td><td>参与人数</td><td>高位平稳，未急升</td></tr>
</table>"""
    if sid == "t8":
        extra = '<div class="triggered"><strong>🔴 T6触发 — 2025全年破产574,314件（美国法院），同比+11%，超T6阈值60万件</strong></div>'
    if sid == "t11":
        extra = '<div class="important"><strong>⚠️ 最大背离：</strong>T4+T6触发、LEI-2%加速、3M非农均值仅48K、MCD/WHR/SHAK下游警报集中爆发，市场却以HY 279bp + VIX 17回应（本周S&P +2.36%）。历史上这是修正前的最后乐观期——2007 Q1对照为HY 250bp + VIX 12。</div>'

    legend = """<div class="chart-legend">
      <span><span class="ldot" style="background:#8b5cf6;"></span>1995–2005</span>
      <span><span class="ldot" style="background:#dc2626;"></span>2003–2013</span>
      <span><span class="ldot" style="background:#38bdf8;"></span>2020–2026</span>
      <span>★Y+5=2000/2008高亮 &nbsp; ★Y+6=当前2026</span>
    </div>"""

    return f"""
<div class="tab-panel" id="{sid}">
  <div class="stage-header {color}"><div class="stage-title">{lamp} {title}</div><div class="stage-q">{q}</div></div>
  <div class="stage-body">
    <div class="vc">
      <div class="vc-card concl"><strong class="lbl">📌 当前结论</strong>{concl}</div>
      <div class="vc-card logic"><strong class="lbl">🧠 判断思路</strong><ul>{logic_items}</ul></div>
      <div class="vc-card action"><strong class="lbl">⚡ 行动建议</strong><ul>{action_items}</ul></div>
    </div>
    {extra}
    {charts_html}
    {legend}
    {table_html}
  </div>
</div>"""

def side_btn(s, first=False):
    sid, lamp, color, title, *_ = s
    num = sid[1:]
    name = title.split("：")[1].split(" ")[0] if "：" in title else title[:6]
    active = ' active' if first else ''
    return f'<button class="side-btn{active}" data-tab="{sid}"><span class="num">{num}</span><span>{lamp}</span><span style="flex:1">{name}</span></button>'

stage_panels = ''.join(make_stage(s) for s in STAGES)
side_btns_html = '\n'.join(side_btn(s, i==0) for i, s in enumerate(STAGES))

CHART_JS = r"""
(function charts(){
  if(typeof Chart==='undefined'){setTimeout(charts,150);return;}
  Chart.defaults.color='#94a3b8';Chart.defaults.borderColor='#334155';
  Chart.defaults.font.family='-apple-system,"SF Pro Text","Helvetica Neue",sans-serif';
  Chart.defaults.font.size=11;
  const C1='#8b5cf6',C2='#dc2626',C3='#38bdf8',C4='#86efac',C5='#fb923c',C6='#fbbf24',CR='#ef4444';

  // X轴：相对年份 Y+0…Y+10，Y+5=2000/2008重点，Y+6=当前2026
  const LX=['Y+0','Y+1','Y+2','Y+3','Y+4','Y+5\n★2000/2008','Y+6\n当前2026','Y+7','Y+8','Y+9','Y+10'];
  const HL=[0,0,0,0,0,1,1,0,0,0,0].map(Boolean);
  const TIPS={'Y+5\n★2000/2008':'★ 周期1=2000纳斯达克顶 | 周期2=2008雷曼破产','Y+6\n当前2026':'当前2026落点（T4+T6双触发）'};

  function ptR(n,b){return HL.map(x=>x?b:n);}
  function ptC(c){return HL.map(x=>x?'#fff':c+'88');}
  function ptBC(c){return HL.map(x=>x?c:c+'55');}
  function ds(lb,d,c,dash,ex={}){
    return{label:lb,data:d,borderColor:c,backgroundColor:c+'10',
      borderWidth:dash?1.5:2,borderDash:dash||[],
      pointRadius:ptR(3,7),pointHoverRadius:ptR(5,10),
      pointBackgroundColor:ptC(c),pointBorderColor:ptBC(c),
      pointBorderWidth:HL.map(x=>x?2.5:1),
      tension:0.35,fill:false,...ex};
  }
  function hl(v,c,lb,n=11){return{label:lb,data:Array(n).fill(v),borderColor:c,borderWidth:1.5,borderDash:[5,4],pointRadius:0,fill:false,order:99};}
  function opts(yL,mn,mx){
    return{responsive:true,maintainAspectRatio:true,interaction:{mode:'index',intersect:false},
      plugins:{legend:{display:false},
        tooltip:{backgroundColor:'#0f172a',borderColor:'#334155',borderWidth:1,
          titleColor:'#fbbf24',bodyColor:'#94a3b8',
          callbacks:{
            title:c=>c[0].label.replace('\n',' '),
            afterBody:c=>{const k=c[0].label;return TIPS[k]?[TIPS[k]]:[];}
          }}},
      scales:{
        x:{grid:{color:'#1e293b'},ticks:{maxRotation:0,autoSkip:false,
          color:c=>HL[c.index]?'#fbbf24':'#94a3b8',
          font:c=>HL[c.index]?{weight:'bold',size:8}:{size:8}}},
        y:{grid:{color:'#1e293b'},title:{display:true,text:yL,color:'#64748b',font:{size:9}},min:mn,max:mx}
      }};
  }
  function mk(id,sets,yL,mn,mx){const el=document.getElementById(id);if(!el)return;new Chart(el,{type:'line',data:{labels:LX,datasets:sets},options:opts(yL,mn,mx)});}

  /* ── 阶段1 ── */
  mk('c1a',[ds('1995–2005',[2.2,2.3,2.5,2.7,2.9,3.1,3.1,2.8,2.5,2.2,2.1],C1),ds('2003–2013',[2.1,2.2,2.1,2.2,2.0,1.5,1.3,1.8,1.9,2.1,2.2],C2),ds('2020–2026',[1.6,2.7,3.0,2.8,2.5,2.2,2.0,null,null,null,null],C3),hl(3.0,C6,'T1触发线')],'辞职率 %',1.0,3.6);
  mk('c1b',[ds('1995–2005',[5.6,5.4,4.9,4.5,4.2,4.0,4.7,5.8,6.0,5.5,5.1],C1),ds('2003–2013',[6.0,5.5,5.1,4.6,4.6,5.8,9.3,9.6,8.9,8.1,7.4],C2),ds('2020–2026',[8.1,5.4,3.6,3.7,4.0,4.1,4.4,null,null,null,null],C3)],'失业率 %',2.0,11.0);
  /* ── 阶段2 ── */
  mk('c2a',[ds('1995–2005',[5.7,5.7,5.6,6.4,5.0,4.9,4.6,5.2,4.8,4.6,2.5],C1),ds('2003–2013',[4.8,4.6,2.5,3.3,3.7,5.0,5.5,6.0,5.6,5.4,5.5],C2),ds('2020–2026',[13.4,8.3,6.6,4.8,4.6,3.5,null,null,null,null,null],C3)],'储蓄率 %',1.0,15.0);
  mk('c2b',[ds('1995–2005',[1.8,1.9,2.0,2.1,2.1,2.2,2.5,2.7,2.6,2.4,2.3],C1),ds('2003–2013',[2.6,2.5,2.4,2.5,2.8,3.5,3.8,3.4,3.1,2.9,2.7],C2),ds('2020–2026',[2.1,2.0,2.2,2.8,3.2,3.6,null,null,null,null,null],C3)],'401k提前支取率 %',1.5,4.5);
  /* ── 阶段3 ── */
  mk('c3a',[ds('1995–2005',[0.44,0.50,0.54,0.58,0.63,0.68,0.70,0.72,0.73,0.74,0.76],C1),ds('2003–2013',[0.73,0.79,0.83,0.89,0.94,0.97,0.90,0.82,0.79,0.82,0.86],C2),ds('2020–2026',[0.82,0.79,0.88,1.05,1.17,1.277,1.25,null,null,null,null],C3)],'信用卡余额 万亿$',0.3,1.4);
  mk('c3b',[ds('1995–2005',[3.8,4.2,4.5,4.6,4.4,4.1,4.6,4.6,4.3,4.0,3.8],C1),ds('2003–2013',[4.3,4.0,3.8,3.9,4.8,6.6,7.2,6.5,5.8,5.0,4.5],C2),ds('2020–2026',[5.2,4.8,5.0,6.4,7.0,7.13,7.10,null,null,null,null],C3)],'90天+逾期率 %',2.5,14.0);
  /* ── 阶段4 ── */
  mk('c4a',[ds('1995–2005',[5.7,5.6,5.0,4.9,4.6,4.4,4.0,3.8,3.5,3.2,2.8],C1),ds('2003–2013',[4.8,4.6,2.5,3.3,3.7,5.0,5.5,5.8,5.6,5.4,5.5],C2),ds('2020–2026',[13.4,8.3,6.6,4.8,4.6,3.5,null,null,null,null,null],C3),
    {label:'WMT 2007',data:[null,null,null,null,2.5,null,null,null,null,null,null],borderColor:C2,backgroundColor:C2,pointRadius:[0,0,0,0,12,0,0,0,0,0,0],pointStyle:'triangle',showLine:false,order:0},
    {label:'WMT 2026',data:[null,null,null,null,null,null,3.5,null,null,null,null],borderColor:C6,backgroundColor:C6,pointRadius:[0,0,0,0,0,0,12,0,0,0,0],pointStyle:'triangle',showLine:false,order:0}
  ],'储蓄率 %（▲=WMT触发）',1.0,16.0);
  mk('c4b',[ds('1995–2005',[102,105,110,115,118,120,108,100,98,102,106],C1),ds('2003–2013',[100,105,108,112,110,88,78,82,88,95,102],C2),ds('2020–2026',[95,110,115,108,102,95,null,null,null,null,null],C3),hl(100,C4,'基准线')],'可选/必需指数',68,130);
  /* ── 阶段5：COF/AXP各自独立 + 汽车贷 ── */
  mk('c5a',[ds('COF 1995–2005',[4.5,4.8,5.5,6.2,5.8,5.2,5.0,4.8,4.5,4.3,4.1],C1),ds('COF 2003–2013',[5.5,5.3,5.0,5.5,6.8,10.2,9.8,8.2,7.0,5.5,4.8],C2),ds('COF 2020–2026',[5.0,3.2,4.2,5.8,6.5,6.2,null,null,null,null,null],C3)],'COF NCO %',0,12);
  mk('c5b',[ds('AXP 2003–2013',[2.5,2.0,2.2,3.5,5.0,8.0,7.5,5.5,4.0,3.0,2.5],C2),ds('AXP 2020–2026',[1.8,1.5,1.8,2.3,2.3,2.3,null,null,null,null,null],C3),hl(6.14,C6,'COF参考线 6.14%')],'AXP NCO %（K型对照）',0,12);
  mk('c5c',[ds('1995–2005',[1.8,1.9,2.0,2.1,2.2,2.3,2.6,2.8,2.6,2.2,2.3],C1),ds('2003–2013',[2.6,2.2,2.3,2.6,3.1,4.4,4.8,4.2,3.6,3.0,2.7],C2),ds('2020–2026',[1.8,1.5,1.6,2.0,2.5,2.95,2.97,null,null,null,null],C3)],'汽车贷60天+逾期 %',1.2,5.5);
  /* ── 阶段6 ── */
  mk('c6a',[ds('95-05（估算）',[18,20,22,24,25,26,25,23,20,18,17],C1),ds('03-13（估算）',[22,24,26,27,26,23,18,15,16,18,20],C2),ds('19-26（实测）',[22.2,24.8,25.2,22.8,20.3,18.7,17.8,null,null,null,null],C3),hl(20,C4,'R1缓和线 20%'),hl(15,CR,'系统排斥线 15%')],'次级发卡率 %',8,32);
  mk('c6b',[ds('1995–2005',[5,5,8,10,12,15,20,18,12,8,5],C1),ds('2003–2013',[10,8,5,8,12,45,50,35,20,10,5],C2),ds('2020–2026',[55,20,8,10,18,25,null,null,null,null,null],C3),hl(40,CR,'2008极端线 40%')],'净收紧比例 %',-5,65);
  /* ── 阶段7 ── */
  mk('c7a',[ds('1995–2005',[120,130,140,145,150,155,160,155,145,140,135],C1),ds('2003–2013',[110,115,120,135,160,210,190,170,150,130,120],C2),ds('2020–2026',[55,110,130,160,185,400,null,null,null,null,null],C3),hl(210,CR,'2008峰值 210万')],'万辆/年',0,460);
  mk('c7b',[ds('1995–2005',[35,38,40,42,44,46,52,60,65,70,72],C1),ds('2003–2013',[75,80,85,117,215,313,280,230,180,140,110],C2),ds('2020–2026',[20,15,18,22,28,35,null,null,null,null,null],C3)],'万件/年',0,340);
  /* ── 阶段8 ── */
  mk('c8a',[ds('1995–2005',[88,112,134,138,132,125,148,154,162,156,200],C1),ds('2003–2013',[162,156,200,60,82,112,143,150,140,132,125],C2),ds('2020–2026',[39,41,43,45,47.8,57.4,null,null,null,null,null],C3),hl(60,C6,'T6触发线 60万')],'万件/年',0,220);
  mk('c8b',[ds('1995–2005',[68,70,71,72,72,71,70,69,68,67,67],C1),ds('2003–2013',[68,67,67,60,58,62,66,68,67,66,65],C2),ds('2020–2026',[58,58,59,60,61,62.1,null,null,null,null,null],C3),hl(65,CR,'绝望升级线 65%')],'Ch.7占比 %',55,76);
  /* ── 阶段9 ── */
  mk('c9a',[ds('1995–2005',[1.4,1.5,1.5,1.6,1.7,1.8,1.9,2.0,1.9,1.7,1.6],C1),ds('2003–2013',[1.5,1.6,1.7,1.9,2.2,3.0,2.8,2.2,1.9,1.7,1.6],C2),ds('2020–2026',[1.8,1.9,1.7,1.7,1.7,1.7,null,null,null,null,null],C3)],'ACL/Loans %',1.0,3.5);
  mk('c9b',[ds('1995–2005',[1.3,1.3,1.4,1.4,1.5,1.5,1.6,1.7,1.6,1.5,1.5],C1),ds('2003–2013',[1.5,1.5,1.6,1.8,2.1,2.6,2.4,2.2,2.0,1.8,1.6],C2),ds('2020–2026',[1.8,1.7,1.9,2.1,2.3,2.36,null,null,null,null,null],C3),hl(2.5,CR,'警戒线 2.5x')],'核销倍数（x）',1.0,3.0);
  /* ── 阶段10 ── */
  mk('c10a',[ds('1995–2005',[52,54,55,53,52,50,42,43,50,57,55],C1),ds('2003–2013',[53,57,55,53,51,46,40,55,57,55,53],C2),ds('2020–2026',[50,58,57,53,50,48.7,null,null,null,null,null],C3),hl(50,C4,'荣枯线 50')],'PMI',32,65);
  mk('c10b',[ds('1995–2005',[27,24,32,28,26,22,-10,-15,8,18,20],C1),ds('2003–2013',[18,16,18,20,15,-20,-75,-80,-50,10,18],C2),ds('2020–2026',[-147,55,55,28,22,18,-8,null,null,null,null],C3),hl(0,CR,'零增长线')],'万人/月',-160,80);
  /* ── 阶段11 ── */
  mk('c11a',[ds('CAPE 1995–2005',[24,28,32,38,44,43,31,22,23,27,27],C1),ds('CAPE 2003–2013',[23,27,27,27,27,15,17,19,21,23,24],C2),ds('CAPE 2020–2026',[28,30,33,36,38,36,36,null,null,null,null],C3),hl(35,CR,'泡沫警戒线 35x')],'CAPE（倍）',10,50);
  mk('c11b',[ds('HY 1995–2005',[380,350,290,560,480,810,870,980,550,380,370],C1),ds('HY 2003–2013',[550,380,370,380,570,1700,900,500,450,400,380],C2),ds('HY 2020–2026',[890,320,290,300,380,279,286,null,null,null,null],C3),hl(500,C5,'衰退定价 500bp'),hl(1000,CR,'危机线 1000bp')],'HY利差（bp）',0,2100);
})();
"""

page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>美股宏观经济传导链诊断 V2 | {DATE}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js"></script>
<style>{CSS}</style>
</head>
<body>

<div class="header">
  <h1>美股宏观经济传导链诊断 V2</h1>
  <div style="color:var(--muted);font-size:1.05em;">分析日期：{DATE} | 框架 v8.0 | 阶段1-4/6-11各2图，阶段5独立3图（COF/AXP/汽车贷）</div>
  <div class="verdict">🔴 T4+T6 双触发 — 升级减仓</div>
  <div style="margin:8px 0;">
    <span class="badge badge-red">⚡ T4触发：WMT CEO "paycheck to paycheck"</span>
    <span class="badge badge-red">⚡ T6触发：破产年化574K 超阈值</span>
    <span class="badge badge-orange">建议美股仓位 40-50%</span>
    <span class="badge badge-yellow">阶段11：HY 279bp + VIX 17 市场最后乐观窗口</span>
  </div>
  <div class="card" style="text-align:left;max-width:860px;margin:14px auto;">
    <strong style="color:var(--accent);">📊 本周 vs 上周（05-13）关键变化</strong>
    <table style="margin-top:10px;">
      <tr><th>指标</th><th>上周 05-13</th><th>本周 05-22</th><th>信号</th></tr>
      <tr><td>4月非农（实际）</td><td>实际+115K</td><td class="diff-same"><strong>实际+115K</strong>（3M均值稳定于48K）</td><td class="diff-worse">⚠️ 底层劳动力动能持续弱化</td></tr>
      <tr><td>失业率</td><td>4.3%（Apr）</td><td class="diff-same"><strong>4.3%（Apr，无新数据发布）</strong></td><td class="diff-worse">→ 隐性失业高企</td></tr>
      <tr><td>时薪 YoY</td><td>3.6%（Apr）</td><td class="diff-same"><strong>3.6%（Apr，无新数据发布）</strong></td><td class="diff-worse">↘️ 居民工资动能回落</td></tr>
      <tr><td>VIX 恐慌指数</td><td>17.08（5/11）</td><td class="diff-better"><strong>16.76（5/22，极致低波）</strong></td><td class="diff-worse">⚠️ 市场极致假稳更脆弱</td></tr>
      <tr><td>HY 利差</td><td>279bp（5/11）</td><td class="diff-worse"><strong>286bp（5/19，最新FRED）</strong></td><td class="diff-worse">⚠️ 信用溢价微升但背离依然极端</td></tr>
      <tr><td>S&P 500</td><td>7,398</td><td class="diff-worse"><strong>7,445.72（+0.64%本周收盘）</strong></td><td class="diff-worse">⚠️ 市场选择性忽视实体警报</td></tr>
      <tr><td>消费财报新警报</td><td>MCD Q1警告 / WHR-13% / SHAK-28%</td><td class="diff-worse"><strong>WMT Q1财报确认高收入向下买入，但低收入财务极其受限</strong></td><td class="diff-worse">🔴 K型分化及发薪日效应固化</td></tr>
      <tr><td>T3 触发器</td><td>❌ 未触发</td><td class="diff-same">❌ 未触发（非农尚未连负）</td><td class="diff-same">→ 持续监控5月非农</td></tr>
      <tr><td>T4/T6 触发器</td><td>🔴 已触发</td><td class="diff-worse">🔴 仍触发（WMT财报证实底部极其挣扎）</td><td class="diff-same">→ 建议减仓并维持低位</td></tr>
    </table>
    <p style="margin-top:10px;font-size:.85em;color:var(--muted);">
      <strong>本周核心变化：</strong><strong>WMT Q1 FY27 财报（5月21日发布）正式落地</strong>，虽然 Comp Sales 录得 +4.1% 表现稳健，但主要增长来自于高收入家庭（年薪&gt;10万美元）由于预算压缩向下买入（Trading Down）和电商（+26%），而 CFOJohn David Rainey 明确警告底层低收入客群财务状况<strong>“特别受限”（remained particularly constrained）</strong>，进一步实锤了K型分化与发薪日效应。与此同时，美股无视实体警报沉浸在低波动假相中（VIX收于16.76，本周标普微涨0.64%至7445.72），与略微走宽的垃圾债利差（286bp）继续拉大资产定价与宏观基本面之间的历史性背离。
    </p>
  </div>
  <div class="legend-row" style="justify-content:center;">
    <span><span class="verify v-ok">✅ 已核实</span></span>
    <span><span class="verify v-warn">⚠️ 估算</span></span>
    <span>🏛️ 财报直取</span>
  </div>
</div>

<div class="container">

<div class="triggered" style="margin-top:18px;">
  <strong style="color:#fca5a5;font-size:1.1em;">🔴 T4 触发 — 2026-02-19 WMT Q4 FY26 财报电话会</strong><br>
  CEO John Furner：<em>"households earning below $50,000 are managing spending <strong>paycheck to paycheck</strong>"</em><br>
  框架行动：消费升级到阶段4g，<strong>仓位立即降10%</strong>。
  来源：<a class="src" href="https://www.fool.com/earnings/call-transcripts/2026/02/19/walmart-wmt-q4-2026-earnings-call-transcript/" target="_blank">🏛️ WMT Q4 FY26 财报电话会 ✅</a>
  ｜ <a class="src" href="https://www.nasdaq.com/articles/walmart-wmt-q4-2026-earnings-call-transcript" target="_blank">Nasdaq备份 ✅</a>
</div>

<h2>一、传导链全景</h2>
<div class="stage-indicator" id="stage-bar">
  <div class="stage-box yellow" data-tab="t1">1 收入</div><div class="stage-arrow">→</div>
  <div class="stage-box red" data-tab="t2">2 储蓄</div><div class="stage-arrow">→</div>
  <div class="stage-box red" data-tab="t3">3 举债</div><div class="stage-arrow">→</div>
  <div class="stage-box red" data-tab="t4">4 消费</div><div class="stage-arrow">→</div>
  <div class="stage-box orange" data-tab="t5">5 信用</div><div class="stage-arrow">→</div>
  <div class="stage-box red" data-tab="t6">6 踢出</div><div class="stage-arrow">→</div>
  <div class="stage-box red" data-tab="t7">7 硬资产</div><div class="stage-arrow">→</div>
  <div class="stage-box red" data-tab="t8">8 退出</div><div class="stage-arrow">→</div>
  <div class="stage-box orange" data-tab="t9">9 银行</div><div class="stage-arrow">→</div>
  <div class="stage-box orange" data-tab="t10">10 实体</div><div class="stage-arrow">→</div>
  <div class="stage-box yellow" data-tab="t11">11 市场</div>
</div>
<div class="card">
  <strong>信号灯：</strong><span class="dot-r"></span>红×6 · <span class="dot-o"></span>橙×3 · <span class="dot-y"></span>黄×2 · <span class="dot-g"></span>绿×0<br>
  <strong>核心判断：</strong>T4+T6维持触发，T3未触发但3M非农均值仅48K（动能弱）。<strong>本周 WMT 落地财报重申低收入面临极大预算约束，K型分化加速固化。</strong>而市场以极致假稳（VIX 16.76）和高收益债极端窄利差（286bp）继续上演疯狂背离。阶段11的超常假稳成为2007 Q1式的“最后乐观窗口”——历史性背离窗口依旧大开。
</div>

<h2>二、逐阶段诊断（23张三周期对比图）</h2>
<div class="card" style="padding:12px 18px;margin-bottom:0;">
  <strong style="color:var(--accent);">📈 图表阅读</strong>：X轴为相对年份 Y+0…Y+10（三周期叠加对比）。
  <strong style="color:#fbbf24;">Y+5 ★2000/2008</strong> = 周期1泡沫顶（2000）/ 周期2雷曼破产（2008）重点标注（白色大点）；
  <strong style="color:#fbbf24;">Y+6 当前2026</strong> = 当前落点（T4+T6双触发）。鼠标悬停显示注释。
  <span class="chart-legend" style="margin:4px 0 0;">
    <span><span class="ldot" style="background:#8b5cf6;"></span>紫=1995–2005</span>
    <span><span class="ldot" style="background:#dc2626;"></span>红=2003–2013</span>
    <span><span class="ldot" style="background:#38bdf8;"></span>蓝=2020–2026</span>
    <span>虚线=触发线/参考线</span>
  </span>
</div>

<div class="split">
<div class="side-nav" id="side-nav">
{side_btns_html}
</div>
<div class="content-area">
{stage_panels}
</div>
</div>

<h2>三、投资决策（{DATE}）</h2>
<div class="card"><h3>触发器状态</h3>
  <table><tr><th>#</th><th>触发器</th><th>状态</th><th>行动</th></tr>
    <tr><td>T1</td><td>VIX&gt;25持续3天</td><td>❌ 未触（VIX 16.76）</td><td>4月曾触已计入</td></tr>
    <tr><td>T2</td><td>HY利差&gt;500bp</td><td>❌ 未触（286bp）</td><td>待触发</td></tr>
    <tr><td>T3</td><td>非农连续2月为负</td><td>❌ 未触（Mar+185 / Apr+115）</td><td>但3M均值仅48K，监控5月</td></tr>
    <tr><td><strong>T4</strong></td><td><strong>WMT CEO"发薪日效应"</strong></td><td><strong class="diff-worse">🔴 已触发（WMT Q1财报重申低收入极度受限）</strong></td><td><strong>仓位-10%</strong></td></tr>
    <tr><td>T5</td><td>JPM/BAC核销加速</td><td>⚠️ JPM Card NCO 3.47%（QoQ +33bp）</td><td>首次实质亮灯，监控Q2</td></tr>
    <tr><td><strong>T6</strong></td><td><strong>破产年化&gt;60万且加速</strong></td><td><strong class="diff-worse">🔴 已触发（574K，+11%）</strong></td><td><strong>阶段8升级🔴</strong></td></tr>
    <tr><td>T7</td><td>VIX&gt;40</td><td>❌ 未触（16.76）</td><td>若再触=仓位降至10%</td></tr>
    <tr><td>T8</td><td>10-2Y再次倒挂</td><td>❌ 未触</td><td>待触发</td></tr>
  </table>
</div>
<div class="grid2">
  <div class="card"><h3>资产配置</h3>
    <table><tr><th>资产</th><th>仓位</th><th>变化</th></tr>
      <tr><td>美股</td><td><strong>40-50%</strong></td><td class="diff-worse">↓ T4触发降10%</td></tr>
      <tr><td>现金/短债</td><td><strong>30-40%</strong></td><td class="diff-worse">↑</td></tr>
      <tr><td>黄金/TIPS</td><td><strong>10-15%</strong></td><td class="diff-same">→</td></tr>
    </table>
  </div>
  <div class="card"><h3>美股内部</h3>
    <table><tr><th>标的</th><th>建议</th></tr>
      <tr><td>NVDA/GOOGL/META</td><td>🟢 持有</td></tr>
      <tr><td>AAPL/TSLA</td><td>🟠 减持</td></tr>
      <tr><td>小盘股R2000</td><td>🔴 减持</td></tr>
      <tr><td>区域银行KRE</td><td>🔴 减持</td></tr>
      <tr><td>DG/DLTR</td><td>🔴 减持（T4触发）</td></tr>
      <tr><td>KMX/CVNA/ALLY</td><td>🔴 减持（收回破纪录）</td></tr>
    </table>
  </div>
</div>

<h2>四、历史独特性</h2>
<div class="card">
  <table><tr><th>维度</th><th>2000年</th><th>2008年</th><th>2026年当前</th></tr>
    <tr><td>估值泡沫</td><td class="col-2000">🔴 极端（CAPE 44x）</td><td class="col-2008">🟢 正常（27x）</td><td class="col-now">🟠 高（36x）</td></tr>
    <tr><td>信用层</td><td class="col-2000">🟢 健康</td><td class="col-2008">🔴 崩溃（次贷）</td><td class="col-now">🟠 次级恶化</td></tr>
    <tr><td>消费降级</td><td class="col-2000">无降级</td><td class="col-2008">4f-4g</td><td class="col-now">🔴 4g（T4触发）</td></tr>
    <tr><td>硬资产损失</td><td class="col-2000">🟢 低位</td><td class="col-2008">🔴 房贷止赎潮</td><td class="col-now">🔴 汽车收回破纪录</td></tr>
    <tr><td>银行杠杆</td><td class="col-2000">15-20x</td><td class="col-2008">30-40x（危机核心）</td><td class="col-now">🟢 10-15x（最大缓冲）</td></tr>
    <tr><td>市场定价</td><td class="col-2000">泡沫已爆破</td><td class="col-2008">2007顶部已过</td><td class="col-now">⚠️ 完全未定价（HY 279bp / VIX 17）</td></tr>
  </table>
  <div class="important" style="margin-top:12px;"><strong>历史独特性：</strong>当前同时具备2000年估值泡沫特征 AND 2008年信用恶化特征——历史上从未同时出现。银行低杠杆（10-15x）是唯一重大缓冲。</div>
</div>

<div style="text-align:center;padding:32px 20px;color:var(--muted);font-size:.85em;border-top:1px solid var(--border);margin-top:32px;">
  <p>本报告基于公开数据，不构成投资建议。</p>
  <p>生成：{DATE} | V2.0 | 23张三周期对比图（阶段5：COF/AXP独立分图）| WMT Q1 FY27 财报已于 5月21日发布落地 | 下次：<strong>2026-06-02（4月JOLTS）</strong> / 2026-06-05（5月非农）</p>
</div>
</div>

<script>
(function(){{
  const panels=document.querySelectorAll('.tab-panel'),btns=document.querySelectorAll('#side-nav .side-btn'),boxes=document.querySelectorAll('#stage-bar .stage-box');
  function go(id){{panels.forEach(p=>p.classList.toggle('active',p.id===id));btns.forEach(b=>b.classList.toggle('active',b.dataset.tab===id));boxes.forEach(b=>b.classList.toggle('active',b.dataset.tab===id));}}
  function scroll(){{document.querySelector('.split').scrollIntoView({{behavior:'smooth',block:'start'}});}}
  btns.forEach(b=>b.addEventListener('click',()=>{{go(b.dataset.tab);scroll();}}));
  boxes.forEach(b=>b.addEventListener('click',()=>{{go(b.dataset.tab);scroll();}}));
  go('t1');
}})();
</script>
<script>{CHART_JS}</script>
</body>
</html>"""

# 内嵌 Chart.js（离线可用，无需 CDN）
_chartjs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chartjs.min.js')
if os.path.exists(_chartjs_path):
    try:
        with open(_chartjs_path) as _f:
            _cjs = _f.read()
        page = page.replace(
            '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.2/dist/chart.umd.min.js"></script>',
            f'<script>/* Chart.js v4.4.2 内嵌 */\n' + _cjs + '\n</script>',
            1
        )
    except Exception as e:
        print(f"Warning: Failed to embed chartjs.min.js ({e}), falling back to CDN.")

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(page)

import re
canvases = sorted(re.findall(r'id="(c\d+[abc])"', page))
print(f"Written: {len(page):,} bytes / {page.count(chr(10))} lines")
print(f"Canvas total: {len(canvases)} → {canvases}")
print("OK" if len(canvases)==23 else "ERROR expected 23")
print(f"\n✅ 报告已生成：{OUT}")

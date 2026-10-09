# -*- coding: utf-8 -*-
# 《CI/CD 的意義：讓迴圈自己轉，AI 的倍數才成立》：docs/slides/loops-need-cicd-before-ai-multiplies.{html,pdf}
# 執行：python3 docs/figures/loops-need-cicd-before-ai-multiplies/build.py
#
# 讀者：公司內部的主管與工程師。大致認同「迭代式開發＋CI/CD」的方向，但懷疑它是否非做不可；熟 IC 設計流程，不熟軟體業的用語。
# 讀完要能：用一句話說出為什麼《把版控當備份的團隊》裡的症狀代價很大：它們打斷的是 AI 本來能放大的那個迴圈。
# 主旨：CI/CD 把一個行動的「查、判」交給機器，inner loop 才自己轉；outer loop（比較 N 個候選）靠許多 inner loop 平行轉；
#       沒有 CI/CD，AI 只能加速「改」，判還是人，倍數歸一。
# 消化與來源：research/loops-and-ai-multiplier.md。軟體業的 inner/outer 以 commit 為界，與這裡的用法不同，第 1 頁有註明。
# 順序：1 一個改動的內圈 → 2 IC 的迴圈分層 → 3 沒有 CI/CD 時內圈的樣子 → 4 迭代相對 waterfall 的時間與風險 → 5 接棒（下一棒能不能是 agent）
#       → 6 外圈 → 7 agent 平行後瓶頸在判 → 8 務實的上限 → 9 沒有 CI/CD 的連鎖 → 10 六個原則各撐住迴圈的哪個條件。
# 括號裡的「圖 N」指《把版控當備份的團隊》的頁碼；長條與次數都是示意。
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from slides import *

NAME = "loops-need-cicd-before-ai-multiplies"
KICKER = "CI/CD 的意義"


def nbox(s, x, y, w, h, title, sub=None, col=INK2, kind="plain", sub2=None):
    if kind == "solid":
        rect(s, x, y, w, h, col=col, fill=col, op=".10", sw=1.6)
    elif kind == "dash":
        rect(s, x, y, w, h, col=col, fill=col, op=".05", sw=1.4, dash="6 4")
    else:
        rect(s, x, y, w, h, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
    T(s, x + 12, y + 21, title, cls="tx", fill=col, w=700)
    if sub:
        T(s, x + 12, y + 39, sub, fill=INK2)
    if sub2:
        T(s, x + 12, y + 55, sub2, fill=INK2)


def loop(s, x0, y0, steps, back_label="不過", pass_label="過", w=96, h=44, gap=36, cols=None):
    """水平的迴圈：steps = [(標題, 小字, 顏色)]；最後一步有「過」往右、「不過」繞回第一步。回傳最後一步的右邊 x。"""
    xs = []
    for i, (t, sub, col) in enumerate(steps):
        x = x0 + i * (w + gap)
        xs.append(x)
        c = col or INK2
        if col:
            rect(s, x, y0, w, h, col=c, fill=c, op=".10", sw=1.5)
        else:
            rect(s, x, y0, w, h, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
        T(s, x + w / 2, y0 + 20, t, cls="tx", anchor="middle", fill=c, w=700)
        if sub:
            T(s, x + w / 2, y0 + 36, sub, anchor="middle", fill=INK2)
        if i < len(steps) - 1:
            arrow(s, x + w + 3, y0 + h / 2, x + w + gap - 3, y0 + h / 2, col=INK2, ar="ar", sw=1.4)
    xl = xs[-1] + w
    # 不過：從最後一步底下繞回第一步
    yb = y0 + h + 22
    path(s, "M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" % (xs[-1] + w / 2, y0 + h + 2, xs[-1] + w / 2, yb, xs[0] + w / 2, yb, xs[0] + w / 2, y0 + h + 6),
         col=WARN, ar="ar-w", sw=1.4)
    T(s, (xs[0] + xs[-1] + w) / 2, yb + 14, back_label, anchor="middle", fill=WARN)
    arrow(s, xl + 3, y0 + h / 2, xl + 34, y0 + h / 2, col=GOAL, ar="ar-g", sw=1.6)
    T(s, xl + 18, y0 + h / 2 - 8, pass_label, anchor="middle", fill=GOAL)
    return xl + 36


# ── 圖 1：一個行動的迴圈 ─────────────────────────────────────────────
def p1():
    s = []
    T(s, 20, 20, "這份文件回答：CI/CD 對這個團隊的意義是什麼；《把版控當備份的團隊》裡的症狀，代價到底多大 ↓", cls="tx-lbl", fill=INK2)
    T(s, 20, 50, "內圈（inner loop）：一個改動（加功能、修 bug）= 改、查、判，轉到過為止", cls="tx-lbl", fill=INK2)
    xr = loop(s, 20, 64, [("改", "人或 agent", None), ("查", "lint、sim", GOAL), ("判", "全 PASS 才過", GOAL)], w=104, gap=30)
    nbox(s, xr, 64, 92, 44, "改動完成", "下一個改動", col=GOAL, kind="solid")
    pill(s, 20, 160, "CI/CD 做的事：查和判由機器做，每一圈一樣", GOAL)
    # 右邊：例子
    rect(s, 548, 44, 312, 150, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
    T(s, 560, 66, "一個改動的例子（示意）", cls="tx", fill=INK2, w=700)
    for j, (k, v) in enumerate([("改動", "給 DMA 加 burst 模式"), ("改", "改 RTL，加一個 testcase"), ("查", "跑 lint、compile、DMA 的 sim 子集"), ("判", "全部 PASS 才過；有一個 FAIL 就回去改")]):
        T(s, 560, 92 + 24 * j, k, cls="tx", fill=GOAL, w=700)
        T(s, 600, 92 + 24 * j, v, fill=INK2)
    # 用語註記
    rect(s, 20, 212, 840, 64, col="var(--rule-2)", fill="var(--surface)", sw=1, dash="4 3")
    T(s, 32, 234, "用語：軟體業把 commit 前叫 inner loop（本機的改、lint、unit test），commit 後的整合與 CI/CD 叫 outer loop。", fill=GRAY)
    T(s, 32, 254, "這份文件的內圈（inner loop）指「一個改動的迴圈」，外圈（outer loop）指第 6 頁的「探索」：比 N 個方案的 PPA。", fill=GRAY)
    bottom(s, 300, [
        ("CI/CD 把查和判交給機器：每一圈一樣的環境、一樣的標準、不用人在旁邊。", True),
        ("人或 agent 只負責改；內圈什麼時候轉、轉幾圈，都和人的空檔無關。", False),
    ])
    aria = ("一個行動的迴圈：改（人或 agent）、查（跑 lint、compile、sim）、判（PASS 才算過），不過就繞回改，過了就行動完成。"
            "CI/CD 做的事是查和判由機器做、每一圈一樣。右邊是示意的例子：給 DMA 加 burst 模式；改 RTL 加 testcase；lint、compile、跑 DMA 的 sim 子集；全部 PASS 才過。"
            "下方註明軟體業的 inner/outer loop 以 commit 為界，這份文件的 inner loop 指一個行動的迴圈、outer loop 指探索。")
    return svg(s, 880, 480, aria)


# ── 圖 2：IC 的迴圈有快有慢 ──────────────────────────────────────────
TIERS = [("lint、compile", "快", 100, "每次改完就跑", "人或 agent 等得起"),
         ("sanity sim（子集）", "中", 210, "每包 submit 都跑", "排進 queue，結果回來機器判"),
         ("完整 regression", "慢", 330, "每晚跑一次", "早上看結果，附 CL 號"),
         ("synthesis、STA", "很慢", 430, "每個里程碑、每個候選各跑一次", "跑完自動抓 PPA")]


def p2():
    s = []
    T(s, 20, 30, "一圈要多久", cls="tx-lbl", fill=INK2)
    T(s, 200, 30, "長條是示意，不代表任何實際時間", fill=GRAY)
    T(s, 640, 30, "CI/CD 怎麼排", cls="tx-lbl", fill=GOAL)
    for i, (name, speed, wbar, when, how) in enumerate(TIERS):
        y = 48 + 62 * i
        T(s, 20, y + 20, name, cls="tx", fill=INK2, w=700)
        T(s, 20, y + 38, speed, fill=GRAY)
        rect(s, 170, y + 8, wbar, 26, col=INK2, fill=INK2, op=".12", sw=1)
        T(s, 640, y + 20, when, cls="tx", fill=GOAL, w=600)
        T(s, 640, y + 38, how, fill=INK2)
    y = 48 + 62 * 4
    T(s, 20, y + 10, "快的每圈都跑、慢的定時跑；哪一層都由機器判，結果放在大家看得到的地方。", cls="tx", fill=INK2)
    bottom(s, 330, [
        ("CI/CD 不會讓 sim 或 synthesis 變快；它做的是讓每一層不用人顧、結果能信，慢的那幾層在背景轉。", True),
        ("agent 能自己轉的是快的那幾層；慢的那幾層由它排進去、等結果。", False),
    ])
    aria = ("四層迴圈，長條示意一圈的長短：lint 與 compile 快，每次改完就跑；sanity sim 子集中等，每包 submit 都跑；完整 regression 慢，每晚跑一次；"
            "synthesis 與 STA 很慢，每個里程碑或候選各跑一次，跑完自動抓 PPA。哪一層都由機器判。")
    return svg(s, 880, 480, aria)


# ── 圖 3：沒有 CI/CD 的 inner loop ───────────────────────────────────
def p3():
    s = []
    T(s, 20, 30, "同一個改動，沒有 CI/CD 的時候：內圈長這樣", cls="tx-lbl", fill=WARN)
    steps = [("改", "人", None), ("設環境", "人：環境、license", WARN), ("跑", "人：盯著 queue", WARN), ("看 log", "人：挑幾個看", WARN), ("判", "人：「應該可以」", WARN)]
    xr = loop(s, 20, 48, steps, w=104, gap=30)
    T(s, 20, 150, "每一圈都卡在人身上；agent 改完也一樣，要等人設環境、人跑、人判。", cls="tx", fill=INK2)
    # 右下：每一圈的代價
    T(s, 20, 196, "每一圈的代價", cls="tx-lbl", fill=WARN)
    costs = [("一圈的時間 = 那個人的空檔", "圖 1"), ("兩圈的環境不保證一樣，比不出好壞", "圖 14"), ("判的標準每個人不同", "圖 15"), ("結果對不回是哪一圈改的", "圖 4")]
    for j, (t, fig) in enumerate(costs):
        y = 222 + 24 * j
        check(s, 32, y, False, t)
        pill(s, 400, y - 14, fig, WARN, h=20)
    T(s, 480, 222, "agent 的處境", cls="tx-lbl", fill=AGENT)
    for j, t in enumerate(["改得很快，然後停下來等人", "一步一步等，速度等於人的速度", "平行幾個 agent 也一樣，排同一條人龍"]):
        T(s, 492, 246 + 22 * j, "· " + t, fill=INK2)
    T(s, 20, 326, "括號裡的圖號指《把版控當備份的團隊》", fill=GRAY)
    bottom(s, 346, [
        ("沒有 CI/CD，一圈裡四個步驟靠人：設環境、跑、看、判；迴圈轉多快由人的空檔決定。", True),
        ("兩圈之間環境和標準不一樣，連「這一圈比上一圈好」都說不準。", False),
    ])
    aria = ("沒有 CI/CD 時同一個行動的迴圈：改、設環境（人）、跑（人盯著 queue）、看 log（人挑幾個看）、判（人說應該可以），不過就繞回去。"
            "每一圈的代價：時間等於那個人的空檔；兩圈環境不保證一樣（圖 14）；判的標準每個人不同（圖 15）；結果對不回哪一圈改的（圖 4）。"
            "agent 的處境：改得很快然後停下來等人，平行幾個也排同一條人龍。")
    return svg(s, 880, 480, aria)


# ── 圖 4：迭代相對 waterfall（2026-10-09 加）────────────────────────
WF_PHASES = [("spec", 90, False), ("RTL 全部寫完", 170, False), ("DV 才開始", 150, True), ("大整合", 110, True), ("synthesis、PD", 130, False)]


def p_iter():
    s = []
    T(s, 20, 30, "waterfall：每個階段做完才交下去，整合與驗證留到最後", cls="tx-lbl", fill=WARN)
    x = 20
    for name, w, hot in WF_PHASES:
        if hot:
            rect(s, x, 42, w, 32, col=WARN, fill=WARN, op=".10", sw=1.3)
        else:
            rect(s, x, 42, w, 32, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
        T(s, x + w / 2, 62, name, anchor="middle", fill=WARN if hot else INK2)
        x += w + 6
    T(s, 20, 96, "問題到 DV 和大整合才浮現：interface 對不上、timing 差很多；越晚改越貴（業界叫 shift left：test early and test often）", fill=WARN)
    T(s, 20, 114, "能交付的狀態：只在最後才有一個；進度 = 文件寫完的比例", fill=GRAY)
    T(s, 20, 150, "迭代：每一包走完內圈就併入；每一包都查過，隨時有能交付的狀態", cls="tx-lbl", fill=GOAL)
    for i in range(10):
        x = 20 + i * 66
        rect(s, x, 162, 58, 32, col=GOAL, fill=GOAL, op=".10", sw=1.2)
        T(s, x + 29, 182, "改查判併", anchor="middle", fill=GOAL)
        if i in (1, 4, 7):
            s.append('<circle cx="%d" cy="160" r="4" fill="%s"/>' % (x + 52, WARN))
    T(s, 20, 216, "問題小、早、就在那一包裡（紅點）；DV 與 synthesis 的檢查分層跟著每一包跑（第 2 頁）", fill=INK2)
    T(s, 20, 234, "能交付的狀態：每一包併入後都有一個；進度 = 通過檢查的功能數", fill=GRAY)
    T(s, 20, 270, "時間上", cls="tx-lbl", fill=GOAL)
    T(s, 440, 270, "風險上", cls="tx-lbl", fill=GOAL)
    for j, t in enumerate(["問題早發現，改的代價小", "沒有最後的大整合，時程的變異小", "下游用不著等全部做完才開始（下一頁）"]):
        T(s, 32, 294 + 20 * j, "· " + t, fill=INK2)
    for j, t in enumerate(["未知早曝光，留到最後的少", "隨時有 known-good 可退回（《把版控當備份的團隊》圖 16）", "進度用通過的檢查量，用不著靠文件"]):
        T(s, 452, 294 + 20 * j, "· " + t, fill=INK2)
    bottom(s, 362, [
        ("迭代把整合和驗證攤到每一包，問題在小的時候就被看見；waterfall 把它們留到最後，一次爆。", True),
        ("tape-out 本身還是一次性的；迭代的是它之前的每一步。", False),
    ])
    aria = ("上半是 waterfall 的時間軸：spec、RTL 全部寫完、DV 才開始、大整合、synthesis 與 PD；問題到 DV 和大整合才浮現，能交付的狀態只在最後。"
            "下半是迭代：十個改查判併的小包依序併入，紅點標出早期就被看見的小問題；能交付的狀態每一包併入後都有。"
            "時間上：問題早發現改的代價小、沒有最後的大整合、下游用不著等全部做完。風險上：未知早曝光、隨時有 known-good 可退回、進度用通過的檢查量。")
    return svg(s, 880, 480, aria)


# ── 圖 5：接棒（2026-10-09 加）───────────────────────────────────────
def p_baton():
    s = []
    T(s, 20, 24, "一棒交給下一棒：架構 → RTL → DV → PD；或同一件工作，白天的人交給晚上的 agent", cls="tx-lbl", fill=INK2)
    rect(s, 20, 40, 400, 150, col=WARN, fill=WARN, op=".05", sw=1.4, dash="6 4")
    T(s, 32, 62, "waterfall 的棒子", cls="tx", fill=WARN, w=700)
    nbox(s, 32, 74, 110, 44, "上一棒", "做完全部才交")
    arrow(s, 146, 96, 176, 96, col=WARN, ar="ar-w", sw=1.4)
    rect(s, 180, 74, 140, 44, col=WARN, fill="var(--surface)", sw=1.2)
    T(s, 192, 92, "spec 文件", cls="tx", fill=WARN, w=700)
    T(s, 192, 110, "＋tarball＋人的記憶", fill=INK2)
    arrow(s, 324, 96, 344, 96, col=WARN, ar="ar-w", sw=1.4)
    nbox(s, 348, 74, 64, 44, "下一棒", "等")
    T(s, 32, 142, "✗ 等全部做完、等人解釋、等環境", fill=WARN)
    T(s, 32, 162, "✗ agent 接不了：讀得懂檔案，接不到環境、判不了對不對", fill=WARN)
    rect(s, 440, 40, 420, 150, col=GOAL, fill=GOAL, op=".05", sw=1.4, dash="6 4")
    T(s, 452, 62, "迭代＋CI/CD 的棒子", cls="tx", fill=GOAL, w=700)
    nbox(s, 452, 74, 100, 44, "上一棒", "每一包併入就交", col=GOAL, kind="solid")
    arrow(s, 556, 96, 586, 96, col=GOAL, ar="ar-g", sw=1.4)
    rect(s, 590, 74, 160, 44, col=GOAL, fill="var(--surface)", sw=1.2)
    T(s, 602, 92, "查過、跑得起來的狀態", cls="tx", fill=GOAL, w=700)
    T(s, 602, 110, "版控裡，附 manifest", fill=INK2)
    arrow(s, 754, 96, 766, 96, col=GOAL, ar="ar-g", sw=1.4)
    nbox(s, 770, 74, 84, 44, "下一棒", "馬上開跑", col=GOAL, kind="solid")
    T(s, 452, 142, "✓ 人或 agent 都接得了：sync、跑 check、看結果", fill=GOAL)
    T(s, 452, 162, "✓ 晚上 agent 接棒：跑 regression、修 lint、讓測試過；早上人接回來", fill=GOAL)
    T(s, 20, 220, "agent 接得了的那一段（務實）", cls="tx-lbl", fill=AGENT)
    for j, t in enumerate(["打包、跑 check、修 lint、讓測試過、附 manifest", "人不在的時候讓內圈繼續轉"]):
        T(s, 32, 244 + 20 * j, "· " + t, fill=INK2)
    T(s, 440, 220, "還是人的那一段", cls="tx-lbl", fill=PM)
    for j, t in enumerate(["設計對不對、取捨怎麼選（Code review）", "下一棒要做什麼"]):
        T(s, 452, 244 + 20 * j, "· " + t, fill=INK2)
    T(s, 20, 300, "跨團隊交 spec 文件時，waterfall 是唯一能協調的方式；交出去的東西換成跑得起來的，迭代才過得了交界。", fill=GRAY)
    bottom(s, 320, [
        ("迭代的每一棒小而查過，下一棒不用等；棒子交得給人，也交得給 agent。", True),
        ("棒子是文件加記憶，agent 接不了；棒子是版控裡跑得起來的狀態，agent 才接得了。", False),
    ])
    aria = ("左邊 waterfall 的棒子：上一棒做完全部才交，交的是 spec 文件加 tarball 加人的記憶，下一棒要等全部做完、等人解釋、等環境；agent 接不了。"
            "右邊迭代加 CI/CD 的棒子：上一棒每一包併入就交，交的是版控裡查過、跑得起來的狀態，附 manifest 與 check，下一棒馬上開跑；人或 agent 都接得了，晚上 agent 接棒跑 regression、修 lint，早上人接回來。"
            "下方：agent 接得了的那一段是打包、跑 check、修 lint、讓測試過、附 manifest，以及人不在時讓內圈繼續轉；還是人的那一段是設計對不對、取捨怎麼選、下一棒要做什麼。")
    return svg(s, 880, 480, aria)


# ── 圖 6：outer loop ─────────────────────────────────────────────────
CANDS = [("候選 A", "cache 32K・bus 64"), ("候選 B", "cache 64K・bus 64"), ("候選 C", "cache 32K・bus 128"), ("候選 D", "cache 64K・bus 128")]


def p4():
    s = []
    rect(s, 20, 24, 560, 250, col=GOAL, fill=GOAL, op=".04", sw=1.4, dash="6 4")
    T(s, 32, 46, "外圈（outer loop）：探索（示意）", cls="tx", fill=GOAL, w=700)
    T(s, 32, 64, "問題：cache 多大、bus 多寬？每個方案都要走完一整圈內圈，才拿得到 PPA；這裡的「比」是比 PPA 好壞", fill=INK2)
    for i, (name, cfg) in enumerate(CANDS):
        x = 32 + i * 136
        rect(s, x, 80, 124, 60, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
        T(s, x + 10, 100, name, cls="tx", fill=INK2, w=700)
        T(s, x + 10, 118, cfg, fill=GRAY)
        T(s, x + 10, 133, "改 → 查 → 判", fill=GOAL)
        arrow(s, x + 62, 144, x + 62, 160, col=GOAL, ar="ar-g", sw=1.2)
        pill(s, x + 62, 164, "PPA", GOAL, anchor="middle", h=18)
    for i in range(4):
        x = 32 + i * 136 + 62
        line(s, x, 184, x, 198, col=GOAL, sw=1.2)
    line(s, 94, 198, 502, 198, col=GOAL, sw=1.2)
    arrow(s, 298, 198, 298, 210, col=GOAL, ar="ar-g", sw=1.4)
    rect(s, 150, 214, 296, 48, col=GOAL, fill=GOAL, op=".12", sw=1.6)
    T(s, 298, 234, "同一標準下比較，選一個", cls="tx", anchor="middle", fill=GOAL, w=700)
    T(s, 298, 252, "同一版工具、同一環境、同一約束", anchor="middle", fill=INK2)
    # 右：業界
    rect(s, 600, 24, 260, 250, col="var(--rule-2)", fill="var(--surface)", sw=1.2)
    T(s, 612, 46, "業界已經有機器在跑這個外圈", cls="tx", fill=INK2, w=700)
    T(s, 612, 70, "Synopsys 對 DSO.ai 的說法：", fill=GRAY)
    rect(s, 612, 78, 236, 50, col="var(--rule-2)", fill="var(--surface-2)", sw=1)
    T(s, 622, 97, "「autonomously search design", fill=INK2)
    T(s, 622, 115, "spaces for optimal PPA solutions」", fill=INK2)
    T(s, 612, 150, "Cadence Cerebrus：自動探索 implementation", fill=INK2)
    T(s, 612, 166, "flow，多 block、多人", fill=INK2)
    T(s, 612, 196, "前提（推論，非 vendor 所述）：", fill=WARN)
    T(s, 612, 214, "flow 能被機器帶參數呼叫", fill=INK2)
    T(s, 612, 230, "PPA 能被機器讀回來", fill=INK2)
    T(s, 612, 246, "每次跑的環境一致", fill=INK2)
    T(s, 612, 266, "出處：research/loops-and-ai-multiplier.md", fill=GRAY)
    bottom(s, 300, [
        ("要比 N 個方案，每個方案都要走完一整圈內圈，拿到同一標準下的 PPA。", True),
        ("內圈轉不起來，外圈就沒有東西可以比；買了 DSO.ai 這類工具也接不上。", False),
    ])
    aria = ("outer loop 探索的示意：cache 多大、bus 多寬，四個候選組合各走一整圈 inner loop 拿到 PPA，在同一版工具、同一環境、同一約束下比較後選一個。"
            "右邊：業界已經有機器在跑這個外圈，Synopsys 說 DSO.ai autonomously search design spaces for optimal PPA solutions；Cadence Cerebrus 自動探索 implementation flow。"
            "前提是推論：flow 能被機器帶參數呼叫、PPA 能被機器讀回來、每次跑的環境一致。")
    return svg(s, 880, 480, aria)


# ── 圖 7：agent 平行之後，瓶頸在判 ───────────────────────────────────
def p5():
    s = []
    T(s, 20, 30, "N 個 agent 平行做「改」：產生候選、改 RTL、寫 testbench", cls="tx-lbl", fill=AGENT)
    for i in range(4):
        x = 20 + i * 100
        rect(s, x, 40, 88, 36, col=AGENT, fill=AGENT, op=".10", sw=1.4)
        T(s, x + 44, 63, "agent %d" % (i + 1), cls="tx", anchor="middle", fill=AGENT, w=700)
    T(s, 20, 102, "然後每一個都要被「判」", cls="tx", fill=INK2, w=600)
    # 左：人判
    rect(s, 20, 118, 400, 150, col=WARN, fill=WARN, op=".05", sw=1.4, dash="6 4")
    T(s, 32, 140, "判由人做", cls="tx", fill=WARN, w=700)
    for i in range(4):
        arrow(s, 60 + i * 100, 150, 220, 186, col=WARN, ar="ar-w", sw=1.1)
    rect(s, 150, 190, 140, 40, col=WARN, fill="var(--surface)", sw=1.4)
    T(s, 220, 214, "一個人看 log", cls="tx", anchor="middle", fill=WARN, w=700)
    T(s, 32, 254, "吞吐量 = 一個人看 log 的速度，agent 再多也一樣", fill=INK2)
    # 右：機器判
    rect(s, 440, 118, 420, 150, col=GOAL, fill=GOAL, op=".05", sw=1.4, dash="6 4")
    T(s, 452, 140, "判由機器做（CI）", cls="tx", fill=GOAL, w=700)
    for i in range(4):
        x = 452 + i * 100
        arrow(s, x + 44, 150, x + 44, 160, col=GOAL, ar="ar-g", sw=1.1)
        rect(s, x, 164, 88, 30, col=GOAL, fill="var(--surface)", sw=1.2)
        T(s, x + 44, 184, "機器判", anchor="middle", fill=GOAL)
        line(s, x + 44, 196, x + 44, 206, col=GOAL, sw=1.1)
    line(s, 496, 206, 796, 206, col=GOAL, sw=1.1)
    arrow(s, 646, 206, 646, 214, col=GOAL, ar="ar-g", sw=1.2)
    pill(s, 646, 218, "人只在併入前看一次（Code review）", PM, anchor="middle")
    T(s, 452, 254, "吞吐量 = license 與算力的寬度", fill=INK2)
    # 外部觀察
    rect(s, 20, 286, 840, 50, col="var(--rule-2)", fill="var(--surface-2)", sw=1)
    T(s, 32, 306, "管理平行 coding agent 的工具 Superset 在部落格寫的：「every agent needs a human to review its code… it's the humans that don't scale」", fill=INK2)
    T(s, 32, 324, "另一位實作者的結論：產生與驗證可以平行，語意上的接受要串行。出處見 research/loops-and-ai-multiplier.md", fill=GRAY)
    bottom(s, 356, [
        ("agent 讓「改」變得很便宜，平行灑 N 個之後，瓶頸整個移到「判」。", True),
        ("判由人做，N 個 agent 排成一條人龍；判由機器做，人只在併入前看一次。", False),
    ])
    aria = ("四個 agent 平行做改，每一個都要被判。左邊判由人做：四條箭頭匯到一個人看 log，吞吐量等於一個人看 log 的速度。"
            "右邊判由機器做（CI）：四個機器判平行，人只在併入前看一次（Code review），吞吐量等於 license 與算力的寬度。"
            "下方引用 Superset 部落格：every agent needs a human to review its code, it's the humans that don't scale；另一位實作者：產生與驗證可以平行，語意上的接受要串行。")
    return svg(s, 880, 480, aria)


# ── 圖 8：務實的上限 ─────────────────────────────────────────────────
CAPS = [("平行的寬度", "由 license 與算力決定", ["N 個 agent 要 N 份 license", "agent 再多也排隊", "寬度是 CAD 與預算的事"]),
        ("一圈的底線", "heavy flow 一圈仍然慢", ["regression、synthesis 一圈還是那麼久", "AI 省的是等人的時間", "省不了工具跑的時間"]),
        ("比較的前提", "同一版工具、環境、約束", ["少一樣，PPA 的差異", "就分不出是候選的差", "還是環境的差（圖 14）"])]


def p6():
    s = []
    for i, (name, sub, items) in enumerate(CAPS):
        x = 20 + i * 284
        rect(s, x, 30, 272, 150, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
        T(s, x + 14, 54, name, cls="tx", fill=INK2, w=700)
        T(s, x + 14, 74, sub, fill=WARN)
        for j, t in enumerate(items):
            T(s, x + 14, 104 + 22 * j, "· " + t, fill=INK2)
    rect(s, 20, 200, 840, 70, col=GOAL, fill=GOAL, op=".08", sw=1.6)
    T(s, 440, 230, "AI 的加成 ＝ 不用人顧的圈數 × 可信的比較", cls="tx-b", anchor="middle", fill=GOAL)
    T(s, 440, 254, "把 AI 的效益講成「sim 變快」是講錯了；它加的是圈數和比較，而且三個上限都還在", anchor="middle", fill=INK2)
    T(s, 20, 302, "CI/CD 直接解的是第三個（比較的前提）；前兩個是排程與預算的問題，但要先有 CI/CD 才排得起來。", cls="tx", fill=INK2)
    bottom(s, 330, [
        ("平行有上限，一圈有底線，比較有前提；三個都是工程問題，講清楚效益才算得出來。", True),
        ("CI/CD 解的是比較的前提，也讓前兩個能被排程。", False),
    ])
    aria = ("三個務實的上限：平行的寬度由 license 與算力決定；一圈的底線是 heavy flow 仍然慢，AI 省的是等人的時間；比較的前提是同一版工具、環境、約束，少一樣就分不出候選的差還是環境的差。"
            "中間一句：AI 的加成等於不用人顧的圈數乘以可信的比較。CI/CD 直接解的是比較的前提。")
    return svg(s, 880, 480, aria)


# ── 圖 9：沒有 CI/CD 的連鎖 ──────────────────────────────────────────
CHAIN = [["沒有 CI/CD"], ["內圈", "每圈要人顧"], ["棒交不出去", "下一棒等人"], ["agent", "每一步等人"], ["N 個 agent", "排成一條人龍"], ["外圈轉不完", "方案比不了"]]
BREAKS = [("圖 2、3", "環境散在 depot 外", "每圈要人設環境"), ("圖 14", "兩台機器結果不同", "圈與圈不可比"), ("圖 15", "狀態靠人填 Excel", "判靠人"),
          ("圖 5", "壞了很久才發現", "圈沒有閉合"), ("圖 8", "main 隨時會壞", "agent sync 到壞的")]


def p7():
    s = []
    for i, t in enumerate(CHAIN):
        x = 20 + i * 122
        rect(s, x, 30, 110, 48, col=WARN, fill=WARN, op=".06", sw=1.3)
        if len(t) == 1:
            T(s, x + 55, 59, t[0], anchor="middle", fill=WARN, cls="tx", w=700)
        else:
            T(s, x + 55, 51, t[0], anchor="middle", fill=WARN, cls="tx", w=700)
            T(s, x + 55, 69, t[1], anchor="middle", fill=WARN)
        if i < 5:
            arrow(s, x + 113, 54, x + 120, 54, col=WARN, ar="ar-w", sw=1.4)
    rect(s, 770, 30, 90, 48, col=WARN, fill=WARN, op=".16", sw=1.8)
    s.append('<text x="815" y="66" text-anchor="middle" style="font-family:var(--sans);font-size:26px;font-weight:700;fill:%s">×1</text>' % WARN)
    T(s, 860, 94, "N 個 agent 的效果", anchor="end", fill=WARN)
    # 長條示意
    T(s, 20, 120, "同樣 N 個 agent、同樣的 license，一段時間內轉完的圈數（長條是示意）", cls="tx-lbl", fill=INK2)
    T(s, 20, 150, "有 CI/CD", cls="tx", fill=GOAL, w=700)
    rect(s, 120, 134, 620, 24, col=GOAL, fill=GOAL, op=".18", sw=1)
    T(s, 748, 150, "圈數多，而且可比", fill=GOAL)
    T(s, 20, 186, "沒有 CI/CD", cls="tx", fill=WARN, w=700)
    rect(s, 120, 170, 110, 24, col=WARN, fill=WARN, op=".18", sw=1)
    T(s, 238, 186, "等於一個人的速度，而且圈與圈不可比", fill=WARN)
    # 症狀打斷哪一環
    T(s, 20, 224, "《把版控當備份的團隊》的症狀，各打斷鏈上哪一環", cls="tx-lbl", fill=WARN)
    for j, (fig, sym, brk) in enumerate(BREAKS):
        x = 20 + (j % 3) * 284
        y = 236 + (j // 3) * 40
        w_ = pill(s, x, y, fig, WARN, h=20)
        T(s, x + w_ + 8, y + 14, sym + " → " + brk, fill=INK2)
    bottom(s, 330, [
        ("沒有 CI/CD，內圈轉不動、棒交不出去，外圈自然沒得轉；AI 加速的只有「改」，N 個 agent 的效果等於一個。", True),
        ("《把版控當備份的團隊》裡的每個症狀，都在這條鏈上打斷一環。", False),
    ])
    aria = ("連鎖：沒有 CI/CD、內圈每圈要人顧、棒交不出去下一棒等人、agent 每一步等人、N 個 agent 排成一條人龍、外圈轉不完方案比不了，N 個 agent 的效果變成 ×1。"
            "長條示意：同樣 N 個 agent 與 license，有 CI/CD 一段時間內轉完的圈數多而且可比；沒有 CI/CD 等於一個人的速度而且不可比。"
            "症狀各打斷哪一環：環境散在 depot 外（圖 2、3）讓每圈要人設環境；兩台機器結果不同（圖 14）讓圈與圈不可比；狀態靠人填 Excel（圖 15）讓判靠人；壞了很久才發現（圖 5）讓圈沒有閉合；main 隨時會壞（圖 8）讓 agent sync 到壞的。")
    return svg(s, 880, 480, aria)


# ── 圖 10：六個原則各撐住迴圈的哪個條件 ───────────────────────────────
MAP = [("Small batches", "一圈一件事", "判出來的差異才歸得到某個改動"),
       ("Single Source of Truth", "每圈條件一樣，agent 進得去就能跑", "少了：兩圈不可比，agent 要人設環境"),
       ("Traceability", "每個結果連得回候選與環境", "少了：比較表是假的"),
       ("Continuous Integration", "查和判由機器做", "少了：每圈要人"),
       ("Self-documenting", "agent 不用人帶就看得懂", "少了：每個 workspace 要人寫說明"),
       ("Code review", "人判放在併入前，一次做完", "少了：人判散在每一圈，或完全沒有")]


def p8():
    s = []
    T(s, 20, 34, "迴圈要自己轉的條件", cls="tx-lbl", fill=INK2)
    T(s, 350, 34, "撐住它的原則（出自《把版控當備份的團隊》）", cls="tx-lbl", fill=GOAL)
    T(s, 620, 34, "少了會怎樣", cls="tx-lbl", fill=WARN)
    for i, (en, cond, miss) in enumerate(MAP):
        y = 46 + 44 * i
        rect(s, 20, y + 6, 3, 30, col=GOAL, fill=GOAL, sw=0)
        T(s, 34, y + 26, cond, cls="tx", fill=INK2)
        T(s, 350, y + 26, en, cls="tx", fill=GOAL, w=700)
        T(s, 620, y + 26, miss, fill=WARN)
        line(s, 20, y + 42, 860, y + 42)
    bottom(s, 330, [
        ("這六個條件就是前面七頁講的事；撐住它們的六個原則，另一份文件已經收斂出來。", True),
        ("這就是 CI/CD 對這個團隊的意義，也是 N 個 agent 要有 N 倍效果的前提。", False),
    ])
    aria = ("六列：Small batches 撐住一圈一件事；Single Source of Truth 撐住每圈條件一樣與 agent 進得去就能跑；Traceability 撐住結果連得回候選與環境；"
            "Continuous Integration 撐住查和判由機器做；Self-documenting 撐住 agent 不用人帶；Code review 撐住人判放在併入前一次做完。各附少了會怎樣。")
    return svg(s, 880, 480, aria)


PAGES = [
    ("內圈（inner loop）：一個改動是改、查、判轉到過為止，查和判交給機器", p1()),
    ("分層：IC 的一圈有快有慢，CI/CD 按快慢分層跑，哪一層都由機器判", p2()),
    ("現狀的內圈：每圈靠人設環境、人跑、人看 log，轉得慢、判法還不一", p3()),
    ("迭代：每一包走完內圈就併入，問題早、小、看得見；waterfall 留到最後一次爆", p_iter()),
    ("接棒：迭代的每一棒小而查過，下一棒不用等；棒子才交得給 agent", p_baton()),
    ("外圈（outer loop）：比 N 個方案的 PPA，每個方案都要先跑完一圈內圈", p4()),
    ("Agentic AI：N 個 agent 平行「改」很便宜，瓶頸變成誰來查、誰來判", p5()),
    ("上限：能平行幾個由 license 與算力決定；CI/CD 管的是排隊和固定環境", p6()),
    ("結論：沒有 CI/CD，每圈要人顧、棒接不過去、方案跑不完，agent 再多也等於一個", p7()),
    ("對應：迴圈要自己轉的六個條件，就是《把版控當備份的團隊》的六個原則", p8()),
]

if __name__ == "__main__":
    build(NAME, "為什麼非要 CI/CD：查和判不交給機器，N 個 agent 等於一個", KICKER, PAGES)

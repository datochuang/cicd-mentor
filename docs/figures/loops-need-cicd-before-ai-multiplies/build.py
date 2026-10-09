# -*- coding: utf-8 -*-
# 《CI/CD 的意義：讓迴圈自己轉，AI 的倍數才成立》：docs/slides/loops-need-cicd-before-ai-multiplies.{html,pdf}
# 執行：python3 docs/figures/loops-need-cicd-before-ai-multiplies/build.py
#
# 讀者：公司內部的主管與工程師。大致認同「迭代式開發＋CI/CD」的方向，但懷疑它是否非做不可；熟 IC 設計流程，不熟軟體業的用語。
# 讀完要能：用一句話說出為什麼《把版控當備份的團隊》裡的症狀代價很大：它們打斷的是 AI 本來能放大的那個迴圈。
# 主旨：CI/CD 把一個行動的「查、判」交給機器，inner loop 才自己轉；outer loop（比較 N 個候選）靠許多 inner loop 平行轉；
#       沒有 CI/CD，AI 只能加速「改」，判還是人，倍數歸一。
# 消化與來源：research/loops-and-ai-multiplier.md。軟體業的 inner/outer 以 commit 為界，與這裡的用法不同，第 1 頁有註明。
# 脊椎：三層套在一起的迴圈。1 總覽（地圖）→ 2–4 第一層內圈（定義、在 IC 分層落實、沒有 CI/CD 的現狀）→ 5–6 第二層迭代（進 main、交接）
#       → 7 第三層外圈 → 8–9 AI（三層都加速「改」、瓶頸在判；務實的上限）→ 10 結論（鏈照三層排）→ 11 六個條件對應六個原則。
# 2026-10-09 使用者說順序不通順，重排成這條脊椎：先給三層的地圖，再一層一層講，AI 放在三層之後。
# 括號裡的「圖 N」指《把版控當備份的團隊》的頁碼；長條與次數都是示意。
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from slides import *

NAME = "loops-need-cicd-before-ai-multiplies"
KICKER = "CI/CD 的意義"


def layer_tag(s, text):
    pill(s, 860, 8, text, GOAL, h=22, anchor="end")


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


# ── 圖 1：總覽——效益站在地基上，地基現在是空的（2026-10-09 第三版）────
PILLARS = [
    ("內圈自己轉", "一個改動：agent 改，機器查、判，不眠不休",
     ["時間：每圈不等人，晚上也在轉", "風險：每個改動都查過才進 main"],
     ["查判靠人", "每圈等人；agent 再多也等於一個"]),
    ("外圈平行跑", "N 個 agent 同時試 N 個方案，PPA 機器讀回",
     ["時間：N 個方案一起跑，license 排得滿", "風險：同環境比，選錯方案的機會小"],
     ["環境各不同", "PPA 比不了；N 次都要人跑"]),
    ("上下游接棒", "交出去的是查過、跑得起來的狀態，agent 接得了",
     ["時間：下游不必等人解釋，馬上開跑", "風險：問題早、小，用不著大整合"],
     ["交接靠文件加記憶", "下游等人；agent 接不了"]),
]


def p_overview():
    s = []
    T(s, 20, 20, "Agentic AI 帶來的三種效益（對開發時間與風險）", cls="tx-lbl", fill=AGENT)
    T(s, 860, 20, "後面十頁是這一頁的展開", cls="tx-lbl", anchor="end", fill=GRAY)
    for i, (name, how, gains, _) in enumerate(PILLARS):
        x = 20 + i * 290
        rect(s, x, 32, 260, 150, col=AGENT, fill=AGENT, op=".08", sw=1.6)
        T(s, x + 14, 56, name, cls="tx", fill=AGENT, w=700)
        T(s, x + 14, 76, how, fill=INK2)
        # 小圖：三種迴圈的形狀
        y0 = 92
        if i == 0:
            for k, t in enumerate(["改", "查", "判"]):
                bx = x + 14 + k * 62
                c = AGENT if k == 0 else GOAL
                rect(s, bx, y0, 44, 22, col=c, fill="var(--surface)", sw=1.1)
                T(s, bx + 22, y0 + 15, t, anchor="middle", fill=c)
                if k < 2:
                    arrow(s, bx + 46, y0 + 11, bx + 60, y0 + 11, col=INK2, ar="ar", sw=1)
            path(s, "M%d,%d L%d,%d L%d,%d L%d,%d" % (x + 160, y0 + 23, x + 160, y0 + 32, x + 36, y0 + 32, x + 36, y0 + 24), col=WARN, ar="ar-w", sw=1)
            T(s, x + 212, y0 + 15, "不停地轉", fill=GRAY)
        elif i == 1:
            for k in range(3):
                bx = x + 14 + k * 70
                rect(s, bx, y0, 60, 22, col=GOAL, fill="var(--surface)", sw=1.1)
                T(s, bx + 30, y0 + 15, "方案 %s" % "ABC"[k], anchor="middle", fill=GOAL)
                arrow(s, bx + 30, y0 + 24, bx + 30, y0 + 32, col=GOAL, ar="ar-g", sw=1)
            line(s, x + 44, y0 + 33, x + 184, y0 + 33, col=GOAL, sw=1)
            T(s, x + 192, y0 + 37, "比 PPA", fill=GRAY)
        else:
            rect(s, x + 14, y0, 60, 22, col=INK2, fill="var(--surface)", sw=1.1)
            T(s, x + 44, y0 + 15, "上游", anchor="middle", fill=INK2)
            arrow(s, x + 78, y0 + 11, x + 104, y0 + 11, col=GOAL, ar="ar-g", sw=1.2)
            rect(s, x + 108, y0, 76, 22, col=GOAL, fill="var(--surface)", sw=1.1)
            T(s, x + 146, y0 + 15, "查過的狀態", anchor="middle", fill=GOAL)
            arrow(s, x + 188, y0 + 11, x + 214, y0 + 11, col=GOAL, ar="ar-g", sw=1.2)
            rect(s, x + 218, y0, 40, 22, col=AGENT, fill="var(--surface)", sw=1.1)
            T(s, x + 238, y0 + 15, "下游", anchor="middle", fill=AGENT)
        for k, g in enumerate(gains):
            T(s, x + 14, 146 + 18 * k, g, fill=GOAL if k == 0 else INK2)
        # 柱子站在地基上
        for px in (x + 60, x + 200):
            s.append('<path d="M%d,184 L%d,196 L%d,196 Z" fill="%s"/>' % (px, px - 7, px + 7, GOAL))
    # 地基
    rect(s, 20, 198, 840, 62, col=GOAL, fill=GOAL, op=".14", sw=2)
    T(s, 34, 222, "地基：CI/CD，查和判交給機器", cls="tx", fill=GOAL, w=700)
    T(s, 34, 246, "每圈環境一樣（SSOT）・結果由機器寫下、連得回來源（Traceability）・進 main 前機器查過、人看過（CI、Code review）・main 隨時可用", fill=INK2)
    # 現狀：空的地基
    rect(s, 20, 276, 840, 86, col=WARN, fill=WARN, op=".05", sw=1.6, dash="8 5")
    T(s, 34, 298, "現狀：這塊地基是空的。查判靠人、環境靠記憶、main 隨時會壞；上面三種效益各變成——", cls="tx", fill=WARN, w=700)
    for i, (_, _, _, lose) in enumerate(PILLARS):
        x = 20 + i * 290
        check(s, x + 14, 326, False, lose[0], cls="tx")
        T(s, x + 34, 346, lose[1], fill=WARN)
    pill(s, 860 - 12, 300, "N 個 agent ＝ ×1", WARN, anchor="end")
    bottom(s, 380, [
        ("AI 加速的只有「改」；查和判沒有機器做，三種效益一個都拿不到，N 個 agent 等於一個。", True),
        ("把這塊地基補起來，是拿到 Agentic AI 效益的前提；它和買哪一家的 AI 無關。", False),
    ])
    aria = ("三根柱子是 Agentic AI 的三種效益：內圈自己轉（時間：每圈不等人；風險：每個改動都查過才進 main）、"
            "外圈平行跑（時間：N 個方案一起跑；風險：同環境比選錯機會小）、上下游接棒（時間：下游不必等人解釋；風險：問題早小用不著大整合）。"
            "三根柱子站在一塊地基上：CI/CD，查和判交給機器，含 SSOT、Traceability、CI、Code review。"
            "地基下方一塊虛線的空框是現狀：查判靠人、環境靠記憶、main 隨時會壞，三種效益各變成每圈等人、PPA 比不了、下游等人，N 個 agent 等於一個。")
    return svg(s, 880, 480, aria)


# ── 圖 2：一個行動的迴圈 ─────────────────────────────────────────────
def p1():
    s = []
    layer_tag(s, "第一層　內圈")
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
    T(s, 32, 254, "這份文件的內圈（inner loop）指「一個改動的迴圈」，外圈（outer loop）指第 7 頁的「探索」：比 N 個方案的 PPA。", fill=GRAY)
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
    layer_tag(s, "第一層　內圈")
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
    T(s, 20, y + 10, "快的每圈都跑、慢的定時跑；哪一道都由機器判，結果放在大家看得到的地方。", cls="tx", fill=INK2)
    bottom(s, 330, [
        ("CI/CD 不會讓 sim 或 synthesis 變快；它做的是讓每一道不用人顧、結果能信，慢的那幾道在背景轉。", True),
        ("agent 能自己轉的是快的那幾道；慢的那幾道由它排進去、等結果。", False),
    ])
    aria = ("四道檢查，長條示意一圈的長短：lint 與 compile 快，每次改完就跑；sanity sim 子集中等，每包 submit 都跑；完整 regression 慢，每晚跑一次；"
            "synthesis 與 STA 很慢，每個里程碑或候選各跑一次，跑完自動抓 PPA。哪一道都由機器判。")
    return svg(s, 880, 480, aria)


# ── 圖 3：沒有 CI/CD 的 inner loop ───────────────────────────────────
def p3():
    s = []
    layer_tag(s, "第一層　內圈")
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
    layer_tag(s, "第二層　中圈：一個專案")
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
    T(s, 20, 150, "中圈（迭代）：每個小改動過了內圈、機器查過就 submit 進 main，main 隨時是能交付的狀態", cls="tx-lbl", fill=GOAL)
    for i in range(10):
        x = 20 + i * 66
        rect(s, x, 162, 58, 32, col=GOAL, fill=GOAL, op=".10", sw=1.2)
        T(s, x + 29, 182, "改查判", anchor="middle", fill=GOAL)
        arrow(s, x + 29, 196, x + 29, 208, col=GOAL, ar="ar-g", sw=1.1)
        if i in (1, 4, 7):
            s.append('<circle cx="%d" cy="160" r="4" fill="%s"/>' % (x + 52, WARN))
    line(s, 20, 212, 680, 212, col=GOAL, sw=2)
    T(s, 690, 216, "main", cls="tx", fill=GOAL, w=700)
    T(s, 20, 236, "問題小、早、就在那個改動裡（紅點）；DV 與 synthesis 那幾道檢查跟著每個改動跑（第 3 頁）", fill=INK2)
    T(s, 20, 254, "能交付的狀態：每個改動進 main 之後都有一個；進度 = 通過檢查的功能數", fill=GRAY)
    T(s, 20, 288, "時間上", cls="tx-lbl", fill=GOAL)
    T(s, 440, 288, "風險上", cls="tx-lbl", fill=GOAL)
    for j, t in enumerate(["問題早發現，改的代價小", "沒有最後的大整合，時程的變異小", "下游用不著等全部做完才開始（下一頁）"]):
        T(s, 32, 312 + 20 * j, "· " + t, fill=INK2)
    for j, t in enumerate(["未知早曝光，留到最後的少", "隨時有 known-good 可退回（《把版控當備份的團隊》圖 16）", "進度用通過的檢查量，用不著靠文件"]):
        T(s, 452, 312 + 20 * j, "· " + t, fill=INK2)
    bottom(s, 376, [
        ("迭代把整合和驗證攤到每個改動，問題在小的時候就被看見；waterfall 把它們留到最後整合才全出。", True),
        ("迭代的是改動怎麼整合，tape-out 本身還是一次性的。", False),
    ])
    aria = ("上半是 waterfall 的時間軸：spec、RTL 全部寫完、DV 才開始、大整合、synthesis 與 PD；問題到 DV 和大整合才浮現，能交付的狀態只在最後。"
            "下半是迭代：十個改查判的小改動依序 submit 進 main，紅點標出早期就被看見的小問題；main 隨時是能交付的狀態。"
            "時間上：問題早發現改的代價小、沒有最後的大整合、下游用不著等全部做完。風險上：未知早曝光、隨時有 known-good 可退回、進度用通過的檢查量。")
    return svg(s, 880, 480, aria)


# ── 圖 5：接棒（2026-10-09 加）───────────────────────────────────────
def p_baton():
    s = []
    layer_tag(s, "第二層　中圈：一個專案")
    T(s, 20, 24, "交接：上游交給下游（架構 → RTL → DV → PD），或同一件工作，白天的人交給晚上的 agent", cls="tx-lbl", fill=INK2)
    rect(s, 20, 40, 400, 150, col=WARN, fill=WARN, op=".05", sw=1.4, dash="6 4")
    T(s, 32, 62, "waterfall 的交接", cls="tx", fill=WARN, w=700)
    nbox(s, 32, 74, 110, 44, "上游", "做完全部才交")
    arrow(s, 146, 96, 176, 96, col=WARN, ar="ar-w", sw=1.4)
    rect(s, 180, 74, 140, 44, col=WARN, fill="var(--surface)", sw=1.2)
    T(s, 192, 92, "spec 文件", cls="tx", fill=WARN, w=700)
    T(s, 192, 110, "＋tarball＋人的記憶", fill=INK2)
    arrow(s, 324, 96, 344, 96, col=WARN, ar="ar-w", sw=1.4)
    nbox(s, 348, 74, 64, 44, "下游", "等")
    T(s, 32, 142, "✗ 等全部做完、等人解釋、等環境", fill=WARN)
    T(s, 32, 162, "✗ agent 接不了：讀得懂檔案，接不到環境、判不了對不對", fill=WARN)
    rect(s, 440, 40, 420, 150, col=GOAL, fill=GOAL, op=".05", sw=1.4, dash="6 4")
    T(s, 452, 62, "迭代＋CI/CD 的交接", cls="tx", fill=GOAL, w=700)
    nbox(s, 452, 74, 100, 44, "上游", "每個改動進 main", col=GOAL, kind="solid")
    arrow(s, 556, 96, 586, 96, col=GOAL, ar="ar-g", sw=1.4)
    rect(s, 590, 74, 160, 44, col=GOAL, fill="var(--surface)", sw=1.2)
    T(s, 602, 92, "查過、跑得起來的狀態", cls="tx", fill=GOAL, w=700)
    T(s, 602, 110, "版控裡，附 manifest", fill=INK2)
    arrow(s, 754, 96, 766, 96, col=GOAL, ar="ar-g", sw=1.4)
    nbox(s, 770, 74, 84, 44, "下游", "馬上開跑", col=GOAL, kind="solid")
    T(s, 452, 142, "✓ 人或 agent 都接得了：sync、跑 check、看結果", fill=GOAL)
    T(s, 452, 162, "✓ 晚上交給 agent：跑 regression、修 lint、讓測試過；早上人接回來", fill=GOAL)
    T(s, 20, 220, "agent 接得了的那一段（務實）", cls="tx-lbl", fill=AGENT)
    for j, t in enumerate(["打包、跑 check、修 lint、讓測試過、附 manifest", "人不在的時候讓內圈繼續轉"]):
        T(s, 32, 244 + 20 * j, "· " + t, fill=INK2)
    T(s, 440, 220, "還是人的那一段", cls="tx-lbl", fill=PM)
    for j, t in enumerate(["設計對不對、取捨怎麼選（Code review）", "下游接下來做什麼"]):
        T(s, 452, 244 + 20 * j, "· " + t, fill=INK2)
    T(s, 20, 300, "跨團隊交 spec 文件時，waterfall 是唯一能協調的方式；交出去的東西換成跑得起來的，迭代才過得了交界。", fill=GRAY)
    bottom(s, 320, [
        ("迭代的每次交接小而查過，下游不用等；交得給人，也交得給 agent。", True),
        ("交出去的是文件加記憶，agent 接不了；交出去的是版控裡跑得起來的狀態，agent 才接得了。", False),
    ])
    aria = ("左邊 waterfall 的交接：上游做完全部才交，交的是 spec 文件加 tarball 加人的記憶，下游要等全部做完、等人解釋、等環境；agent 接不了。"
            "右邊迭代加 CI/CD 的交接：上游每個改動進 main 就交，交的是版控裡查過、跑得起來的狀態，附 manifest，下游馬上開跑；人或 agent 都接得了，晚上交給 agent 跑 regression、修 lint，早上人接回來。"
            "下方：agent 接得了的那一段是打包、跑 check、修 lint、讓測試過、附 manifest，以及人不在時讓內圈繼續轉；還是人的那一段是設計對不對、取捨怎麼選、下游接下來做什麼。")
    return svg(s, 880, 480, aria)


# ── 圖 6：outer loop ─────────────────────────────────────────────────
CANDS = [("候選 A", "cache 32K・bus 64"), ("候選 B", "cache 64K・bus 64"), ("候選 C", "cache 32K・bus 128"), ("候選 D", "cache 64K・bus 128")]


def p4():
    s = []
    layer_tag(s, "第三層　外圈")
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
    T(s, 298, 234, "機器判過的 PPA，同一標準下比較，選一個", cls="tx", anchor="middle", fill=GOAL, w=700)
    T(s, 298, 252, "同一版工具、同一環境、同一約束", anchor="middle", fill=INK2)
    # 右：業界
    rect(s, 600, 38, 260, 236, col="var(--rule-2)", fill="var(--surface)", sw=1.2)
    T(s, 612, 60, "業界已經有機器在跑這個外圈", cls="tx", fill=INK2, w=700)
    T(s, 612, 82, "Synopsys 對 DSO.ai 的說法：", fill=GRAY)
    rect(s, 612, 90, 236, 50, col="var(--rule-2)", fill="var(--surface-2)", sw=1)
    T(s, 622, 109, "「autonomously search design", fill=INK2)
    T(s, 622, 127, "spaces for optimal PPA solutions」", fill=INK2)
    T(s, 612, 160, "Cadence Cerebrus：自動探索 implementation", fill=INK2)
    T(s, 612, 176, "flow，多 block、多人", fill=INK2)
    T(s, 612, 202, "前提（推論，非 vendor 所述）：", fill=WARN)
    T(s, 612, 218, "flow 能被機器帶參數呼叫", fill=INK2)
    T(s, 612, 234, "PPA 能被機器讀回來", fill=INK2)
    T(s, 612, 250, "每次跑的環境一致", fill=INK2)
    T(s, 612, 268, "出處：research/loops-and-ai-multiplier.md", fill=GRAY)
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
    T(s, 20, 30, "agent 加速的是「改」：自己轉內圈、接交接、平行跑 N 個方案（產生候選、改 RTL、寫 testbench）", cls="tx-lbl", fill=AGENT)
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
    T(s, 20, 302, "CI/CD 直接解的是第三個（比較的前提）；前兩個是預算的事，但 license 要不用等人有空就排得滿，也得先有 CI/CD。", cls="tx", fill=INK2)
    bottom(s, 330, [
        ("平行有上限，一圈有底線，比較有前提；三個都是工程問題，講清楚效益才算得出來。", True),
        ("CI/CD 解的是比較的前提，也讓 license 和算力不用等人有空就排得滿。", False),
    ])
    aria = ("三個務實的上限：平行的寬度由 license 與算力決定；一圈的底線是 heavy flow 仍然慢，AI 省的是等人的時間；比較的前提是同一版工具、環境、約束，少一樣就分不出候選的差還是環境的差。"
            "中間一句：AI 的加成等於不用人顧的圈數乘以可信的比較。CI/CD 直接解的是比較的前提。")
    return svg(s, 880, 480, aria)


# ── 圖 9：沒有 CI/CD 的連鎖 ──────────────────────────────────────────
CHAIN = [["沒有 CI/CD"], ["內圈", "每圈等人查判"], ["中圈", "交接等人驗"], ["外圈", "方案比不了"], ["agent", "每一步等人"], ["N 個 agent", "排成一條人龍"]]
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
        ("沒有 CI/CD，每圈、每次交接、每個方案都要等人查判；AI 加速的只有「改」，N 個 agent 的效果等於一個。", True),
        ("《把版控當備份的團隊》裡的每個症狀，都在這條鏈上打斷一環。", False),
    ])
    aria = ("連鎖：沒有 CI/CD、內圈每圈等人查判、中圈的交接等人驗、外圈方案比不了、agent 每一步等人、N 個 agent 排成一條人龍，N 個 agent 的效果變成 ×1。"
            "長條示意：同樣 N 個 agent 與 license，有 CI/CD 一段時間內轉完的圈數多而且可比；沒有 CI/CD 等於一個人的速度而且不可比。"
            "症狀各打斷哪一環：環境散在 depot 外（圖 2、3）讓每圈要人設環境；兩台機器結果不同（圖 14）讓圈與圈不可比；狀態靠人填 Excel（圖 15）讓判靠人；壞了很久才發現（圖 5）讓圈沒有閉合；main 隨時會壞（圖 8）讓 agent sync 到壞的。")
    return svg(s, 880, 480, aria)


# ── 圖 10：六個原則各撐住迴圈的哪個條件 ───────────────────────────────
MAP = [("內圈", "Small batches", "一圈一件事", "判出來的差異才歸得到某個改動"),
       ("內圈", "Continuous Integration", "查和判由機器做", "少了：每圈要人"),
       ("中圈", "Code review", "人判放在進 main 前，一次做完", "少了：人判散在每一圈，或完全沒有"),
       ("中圈", "Self-documenting", "交接時 agent 不用人帶就看得懂", "少了：每個 workspace 要人寫說明"),
       ("外圈", "Single Source of Truth", "每個方案的環境一樣，agent 進得去就能跑", "少了：方案不可比，agent 要人設環境"),
       ("外圈", "Traceability", "每個結果連得回方案與環境", "少了：比較表是假的")]


def p8():
    s = []
    T(s, 20, 34, "哪一層　要的條件", cls="tx-lbl", fill=INK2)
    T(s, 390, 34, "撐住它的原則（出自《把版控當備份的團隊》）", cls="tx-lbl", fill=GOAL)
    T(s, 640, 34, "少了會怎樣", cls="tx-lbl", fill=WARN)
    for i, (layer, en, cond, miss) in enumerate(MAP):
        y = 46 + 44 * i
        pill(s, 20, y + 11, layer, GOAL, h=20)
        T(s, 80, y + 26, cond, cls="tx", fill=INK2)
        T(s, 390, y + 26, en, cls="tx", fill=GOAL, w=700)
        T(s, 640, y + 26, miss, fill=WARN)
        line(s, 20, y + 42, 860, y + 42)
    bottom(s, 330, [
        ("三層各要兩個條件，都是前面幾頁講過的事；撐住它們的六個原則，另一份文件已經收斂出來。", True),
        ("這就是 CI/CD 對這個團隊的意義，也是 N 個 agent 要有 N 倍效果的前提。", False),
    ])
    aria = ("六列，依層分組：內圈要一圈一件事（Small batches）與查和判由機器做（Continuous Integration）；中圈要人判放在進 main 前一次做完（Code review）與交接時 agent 不用人帶（Self-documenting）；"
            "外圈要每個方案的環境一樣（Single Source of Truth）與每個結果連得回方案與環境（Traceability）。各附少了會怎樣。")
    return svg(s, 880, 480, aria)


PAGES = [
    ("總覽：AI 的三種效益站在同一塊地基 CI/CD 上，而這塊地基現在是空的", p_overview()),
    ("內圈（inner loop）：一個改動是改、查、判轉到過為止，查和判交給機器", p1()),
    ("內圈在 IC：一圈有快有慢，CI/CD 照快慢排成幾道檢查，每道機器判", p2()),
    ("現狀的內圈：每圈靠人設環境、人跑、人看 log，轉得慢、判法還不一", p3()),
    ("中圈：改動機器查過就進 main，問題早且小；waterfall 把整合留到最後", p_iter()),
    ("中圈的交接：交出的改動小、機器查過，下游人或 agent 不必等人解釋", p_baton()),
    ("外圈（outer loop）：N 個方案比 PPA，每個先各自轉完內圈、機器判過才比", p4()),
    ("Agentic AI：agent 在三層都加速「改」，瓶頸變成誰來查、誰來判", p5()),
    ("上限：同時轉幾個方案看 license 與算力；交給機器排，license 才排得滿", p6()),
    ("結論：沒有 CI/CD，每圈、每次交接、每個方案都要等人查判，N 個 agent 等於一個", p7()),
    ("對應：三層各要的條件，對到《把版控當備份的團隊》的六個原則", p8()),
]

if __name__ == "__main__":
    build(NAME, "為什麼非要 CI/CD：查和判不交給機器，N 個 agent 等於一個", KICKER, PAGES)

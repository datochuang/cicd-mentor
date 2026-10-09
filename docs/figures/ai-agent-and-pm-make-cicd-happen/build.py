# -*- coding: utf-8 -*-
# 《AI agent 與 PM 一起把 CI/CD 做成》：docs/slides/ai-agent-and-pm-make-cicd-happen.{html,pdf}
# 執行：python3 docs/figures/ai-agent-and-pm-make-cicd-happen/build.py
#
# 讀者：公司內部的主管與決策者（sponsor 候選、部門主管、可能的 PM）。懂 IC 設計流程與 Perforce 基本用法，
#       大致認同「迭代式開發＋CI/CD」的方向，但懷疑是否非做不可、懷疑做得到；沒參與過這個專案的討論。
# 讀完要能：說出這件事為什麼一直做不起來，以及 AI agent 與人類 PM 搭配後怎麼把它做成；判斷要不要支持或擔任 PM。
# 主旨：方向大家認同，卡在工程師不熟軟體業界的做法、心態遲疑、推動者不知道怎麼開始；
#       AI 有完整的 CI/CD 知識與技能，和對的掌舵人搭配，就能自主地與人類 PM 一起把事情做成。
# 脈絡（2026-10-08 使用者定）：1 簡單帶出必要性 → 2–4 實踐的困難 → 5–6 AI 與 PM 搭配。
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from slides import *

NAME = "ai-agent-and-pm-make-cicd-happen"
KICKER = "CI/CD Mentor Agent"


# ── 圖 1：方向 ──────────────────────────────────────────────────────
LAYERS = [
    ("公司競爭力", "更快、更可靠地交出晶片", "plain"),
    ("AI 效益跨出組織疆界", "AI 的產出跨團隊被信任、被採用", "plain"),
    ("迭代式開發", "tape-out 前小步改、頻繁整合", "plain"),
    ("CI/CD", "每個變更自動驗證，每個結果查得到版本", "gap"),
]


def p1():
    s = []
    T(s, 20, 20, "這份文件回答：方向大家認同，為什麼一直做不起來；AI agent 怎麼和人類 PM 一起把它做成 ↓", cls="tx-lbl", fill=INK2)
    cx, h, gap, y0 = 430, 56, 14, 48
    for i, (name, sub, kind) in enumerate(LAYERS):
        w = 340 + 100 * i
        x, y = cx - w / 2, y0 + i * (h + gap)
        if kind == "gap":
            rect(s, x, y, w, h, col=WARN, fill=WARN, op=".06", sw=1.6, dash="6 4")
            col = WARN
        else:
            rect(s, x, y, w, h, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
            col = INK2
        T(s, cx, y + 24, name, cls="tx", anchor="middle", fill=col, w=700)
        T(s, cx, y + 43, sub, anchor="middle", fill=INK2 if kind == "gap" else GRAY)
    yg = y0 + 3 * (h + gap)
    pill(s, cx + 320 + 14, yg + 18, "目前缺這一層", WARN)
    arrow(s, 40, yg + h, 40, y0 + 4, col=GRAY, ar="ar-gray", sw=1.2)
    T(s, 50, y0 + 14, "上層", fill=GRAY)
    T(s, 28, yg + h + 18, "下層撐住上層", fill=GRAY)
    bottom(s, yg + h + 40, [
        ("AI 的產出要跨團隊被採用，必須能被機器驗證、查得到來源，CI/CD 就是提供這件事的那一層。", True),
        ("這個方向大家多半認同；接下來幾頁談的是：為什麼一直做不起來，以及怎麼做成。", False),
    ])
    aria = ("四層的依賴圖，由上而下：公司競爭力、AI 效益跨出組織疆界、迭代式開發、CI/CD。"
            "上層靠下層撐住；CI/CD 那層以虛線標示，是目前缺的一層。")
    return svg(s, 880, 480, aria)


# ── 圖 2：專業背景的距離 ─────────────────────────────────────────────
GAPS = [
    ("版控", "每個改動都進版控、先 review 再合併", "Perforce 多半當備份，偶爾打 label"),
    ("自動驗證", "每次提交自動跑測試", "少數流程才會觸發 sanity check"),
    ("環境", "用 script 從零重建，誰跑都一樣", "工具版本與環境設定靠人記"),
    ("驗證成本", "測試便宜，可以大量平行跑", "simulation 與 synthesis 很貴、license 有限"),
    ("誰負責", "有專門的 platform／DevOps 團隊", "沒有專人，落在每個工程師身上"),
]
IC_CASES = ["大型 binary", "入庫的產生檔", "ECO netlist", "凍結的 IP 複本", "EDA license 與 queue"]


def p2():
    s = []
    xl, wl, xr, wr = 140, 330, 500, 360
    T(s, xl, 24, "軟體業界視為理所當然", cls="tx-lbl", fill=GOAL)
    T(s, xr, 24, "IC 設計團隊的現況", cls="tx-lbl", fill=WARN)
    y0, h, gap = 38, 44, 8
    for i, (lab, sw_, ic) in enumerate(GAPS):
        y = y0 + i * (h + gap)
        T(s, 20, y + 27, lab, cls="tx", fill=INK2, w=700)
        rect(s, xl, y, wl, h, col=GOAL, fill=GOAL, op=".07", sw=1.2)
        T(s, xl + 14, y + 27, sw_, cls="tx", fill=INK2)
        rect(s, xr, y, wr, h, col=WARN, fill=WARN, op=".07", sw=1.2)
        T(s, xr + 14, y + 27, ic, cls="tx", fill=INK2)
        arrow(s, xl + wl + 4, y + h / 2, xr - 4, y + h / 2, col=WARN, ar="ar-w", dash="3 3", sw=1.2)
    yc = y0 + 5 * (h + gap) + 18
    T(s, 20, yc, "照搬軟體做法會撞上的 IC 特有情況", cls="tx-lbl", fill=WARN)
    x = 20
    for c in IC_CASES:
        x += pill(s, x, yc + 10, c, WARN) + 10
    bottom(s, yc + 54, [
        ("工程師要同時懂軟體業界的做法和這些 IC 特有的例外，才知道哪些照做、哪些要變通。", True),
        ("這樣的人在 IC 設計團隊裡很少，也沒有人的工作是做這件事。", False),
    ])
    aria = ("五列對照：版控、自動驗證、環境、驗證成本、誰負責。左欄是軟體業界視為理所當然的做法，右欄是 IC 設計團隊的現況，"
            "中間以虛線箭頭表示落差。下方列出照搬軟體做法會撞上的 IC 特有情況：大型 binary、入庫的產生檔、ECO netlist、凍結的 IP 複本、EDA license 與 queue。")
    return svg(s, 880, 480, aria)


# ── 圖 3：心態的遲疑 ─────────────────────────────────────────────────
DOUBTS = [
    ("非做不可嗎？", "沒有它，晶片一直也做得出來", "看到身邊的團隊做成、省下時間"),
    ("我們做得到嗎？", "EDA 流程太重，團隊裡沒人懂", "第一步夠小，而且有人代做"),
    ("誰有空做？", "tape-out 的壓力永遠排第一", "對工程師來說，做的成本趨近零"),
    ("會被盯上嗎？", "多一雙眼睛看每一次 submit", "看的是流程，報告不針對個人"),
]


def p3():
    s = []
    pill(s, 20, 8, "大方向：認同", GOAL)
    T(s, 20, 52, "遲疑", cls="tx-lbl", fill=WARN)
    T(s, 500, 52, "讓遲疑鬆動的條件", cls="tx-lbl", fill=GOAL)
    y0, h, gap = 64, 56, 12
    for i, (q, why, ease) in enumerate(DOUBTS):
        y = y0 + i * (h + gap)
        rect(s, 20, y, 400, h, col=WARN, fill=WARN, op=".07", sw=1.3)
        T(s, 36, y + 23, q, cls="tx", fill=WARN, w=700)
        T(s, 36, y + 42, why, fill=INK2)
        arrow(s, 426, y + h / 2, 492, y + h / 2, col=GRAY, ar="ar-gray", sw=1.3)
        rect(s, 500, y, 360, h, col=GOAL, fill=GOAL, op=".07", sw=1.3)
        T(s, 516, y + 33, ease, cls="tx", fill=INK2)
    bottom(s, y0 + 4 * (h + gap) + 14, [
        ("這些遲疑多半是理性的：成本落在自己身上，好處落在團隊與下游。", True),
        ("讓它鬆動的條件有個共同點：要有人先把事情做出來，而且做得夠便宜。", False),
    ])
    aria = ("頂端標示大方向是認同的。下面四列：左邊是工程師的遲疑，右邊是讓遲疑鬆動的條件。"
            "非做不可嗎，對應看到身邊的團隊做成；我們做得到嗎，對應第一步夠小而且有人代做；"
            "誰有空做，對應工程師做的成本趨近零；會被盯上嗎，對應看的是流程、報告不針對個人。")
    return svg(s, 880, 480, aria)


# ── 圖 4：推動者不知道怎麼開始 ───────────────────────────────────────
STEPS = ["先驗哪一件事？從哪個 block 開始？", "pipeline 放在哪、誰來維護？", "Perforce 上怎麼觸發、結果給誰看？",
         "IC 的例外怎麼處理才不卡人？", "工程師不配合時，怎麼談？"]


def p4():
    s = []
    # 推動的人
    rect(s, 20, 40, 210, 300, col=PM, fill=PM, op=".08", sw=1.6)
    T(s, 36, 66, "想推動的人", cls="tx", fill=PM, w=700)
    T(s, 36, 96, "知道", cls="tx-lbl", fill=PM)
    for i, t in enumerate(["大方向", "成功的樣子", "團隊的痛點", "組織裡該找誰"]):
        T(s, 48, 120 + 22 * i, "✓ " + t, cls="tx", fill=INK2)
    T(s, 36, 232, "不確定", cls="tx-lbl", fill=WARN)
    for i, t in enumerate(["怎麼做", "觀念準不準", "從哪裡開始"]):
        T(s, 48, 256 + 22 * i, "? " + t, cls="tx", fill=INK2)
    # 中間不知道怎麼走的那一段
    rect(s, 270, 40, 380, 300, col=WARN, fill=WARN, op=".04", sw=1.5, dash="6 4")
    T(s, 286, 66, "中間這一段：不知道怎麼走", cls="tx", fill=WARN, w=700)
    for i, t in enumerate(STEPS):
        y = 86 + i * 48
        rect(s, 286, y, 348, 36, col=WARN, fill="var(--surface)", sw=1.1, dash="4 3")
        T(s, 300, y + 23, t, cls="tx", fill=INK2)
    arrow(s, 234, 190, 266, 190, col=PM, ar="ar-p", sw=1.6)
    arrow(s, 654, 190, 686, 190, col=WARN, ar="ar-w", dash="4 3", sw=1.6)
    # 目標
    rect(s, 690, 130, 170, 120, col=GOAL, fill=GOAL, op=".10", sw=1.6)
    T(s, 706, 160, "目標", cls="tx-lbl", fill=GOAL)
    T(s, 706, 186, "迭代式開發", cls="tx", fill=GOAL, w=700)
    T(s, 706, 206, "＋ CI/CD", cls="tx", fill=GOAL, w=700)
    T(s, 706, 228, "在團隊裡運作", fill=INK2)
    bottom(s, 372, [
        ("他缺的是把方向翻成一連串具體動作的知識，以及動手做的人力。", True),
        ("這一段恰好是 AI 擅長的部分。", False),
    ])
    aria = ("左邊是想推動的人：知道大方向、成功的樣子、團隊的痛點、組織裡該找誰；不確定怎麼做、觀念準不準、從哪裡開始。"
            "右邊是目標：迭代式開發加 CI/CD 在團隊裡運作。中間是一段虛線框，列出不知道怎麼走的問題："
            "先驗哪一件事、pipeline 放在哪誰來維護、Perforce 上怎麼觸發、IC 的例外怎麼處理、工程師不配合時怎麼談。")
    return svg(s, 880, 480, aria)


# ── 圖 5：AI 與 PM 各補一半 ──────────────────────────────────────────
PM_HAS = ["使命感", "方向與成功的定義", "組織的權威", "對團隊與人的了解", "最後的判斷與責任"]
AG_HAS = ["完整的 CI/CD 知識", "Perforce 與 scripting 技能", "不停地觀察與動手", "和每位工程師溝通", "解釋做法背後的原則"]


def p5():
    s = []
    for (x, col, title, items, lack) in [(20, PM, "人類 PM：掌舵", PM_HAS, "缺：做法、時間、人手"),
                                         (620, AGENT, "AI agent：執行", AG_HAS, "缺：組織權威、方向判斷")]:
        rect(s, x, 30, 240, 250, col=col, fill=col, op=".08", sw=1.6)
        T(s, x + 16, 56, title, cls="tx", fill=col, w=700)
        T(s, x + 16, 84, "帶來", cls="tx-lbl", fill=col)
        for i, t in enumerate(items):
            T(s, x + 28, 108 + 26 * i, "+ " + t, cls="tx", fill=INK2)
        rect(s, x, 292, 240, 36, col=WARN, fill=WARN, op=".07", sw=1.1, dash="4 3")
        T(s, x + 16, 315, lack, cls="tx", fill=WARN)
    # 中間
    rect(s, 320, 100, 240, 116, col=GOAL, fill=GOAL, op=".12", sw=2)
    T(s, 440, 136, "把事情做成", cls="tx-b", anchor="middle", fill=GOAL)
    T(s, 440, 164, "迭代式開發＋CI/CD", cls="tx", anchor="middle", fill=INK2, w=600)
    T(s, 440, 184, "在團隊裡真正運作", cls="tx", anchor="middle", fill=INK2)
    arrow(s, 264, 158, 314, 158, col=PM, ar="ar-p", sw=2)
    arrow(s, 616, 158, 566, 158, col=AGENT, ar="ar-a", sw=2)
    T(s, 440, 262, "對方缺的，正好是自己帶來的", anchor="middle", fill=GRAY)
    T(s, 440, 300, "PM 指負責把團隊開發流程導入 CI/CD 的那個人，和 project 的 PM 無關", anchor="middle", fill=GRAY)
    bottom(s, 368, [
        ("AI 一個人推不動組織，PM 一個人做不完；兩邊搭在一起，缺的才補齊。", True),
        ("關鍵在搭配對的掌舵人：AI 補上知識與執行力，方向仍由人決定。", False),
    ])
    aria = ("左邊是人類 PM，負責掌舵，帶來使命感、方向與成功的定義、組織的權威、對團隊與人的了解、最後的判斷與責任，缺的是做法、時間、人手。"
            "右邊是 AI agent，負責執行，帶來完整的 CI/CD 知識、Perforce 與 scripting 與 EDA flow 的技能、不停地觀察與動手、和每位工程師溝通、解釋做法背後的原則，"
            "缺的是組織權威與方向判斷。兩邊的箭頭匯到中間：把事情做成，迭代式開發加 CI/CD 在團隊裡真正運作。")
    return svg(s, 880, 480, aria)


# ── 圖 6：協作的循環 ─────────────────────────────────────────────────
def p6():
    s = []
    W, H = 200, 54
    n1 = (20, 40)      # 觀察
    n2 = (380, 40)     # 提案
    n3 = (380, 170)    # PM 核准
    n4 = (380, 300)    # 執行
    n5 = (20, 300)     # 回報
    box(s, *n1, W, H, "1 觀察", "repo、變更、團隊的狀況", col=AGENT, kind="solid")
    box(s, *n2, W, H, "2 提案", "附上原則、取捨與替代做法", col=AGENT, kind="solid")
    rect(s, n3[0], n3[1], W, H, col=PM, fill=PM, op=".14", sw=2.2)
    T(s, n3[0] + 14, n3[1] + 22, "3 PM 理解後核准", cls="tx", fill=PM, w=700)
    T(s, n3[0] + 14, n3[1] + 40, "說得出要達成什麼、影響誰", fill=INK2)
    box(s, *n4, W, H, "4 執行", "實作、與工程師溝通", col=AGENT, kind="solid")
    box(s, *n5, W, H, "5 回報", "團隊全貌與進展，附證據", col=AGENT, kind="solid")
    arrow(s, n1[0] + W + 4, n1[1] + H / 2, n2[0] - 4, n2[1] + H / 2, col=AGENT, ar="ar-a", sw=1.6)
    arrow(s, n2[0] + W / 2, n2[1] + H + 4, n3[0] + W / 2, n3[1] - 4, col=AGENT, ar="ar-a", sw=1.6)
    arrow(s, n3[0] + W / 2, n3[1] + H + 4, n4[0] + W / 2, n4[1] - 4, col=PM, ar="ar-p", sw=1.6)
    arrow(s, n4[0] - 4, n4[1] + H / 2, n5[0] + W + 4, n5[1] + H / 2, col=AGENT, ar="ar-a", sw=1.6)
    arrow(s, n5[0] + W / 2, n5[1] - 4, n1[0] + W / 2, n1[1] + H + 4, col=AGENT, ar="ar-a", sw=1.6)
    # 圈內：工程團隊
    rect(s, 140, 170, 140, 54, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
    T(s, 210, 194, "工程團隊", cls="tx", anchor="middle", fill=INK2, w=700)
    T(s, 210, 212, "repo 與流程的主人", anchor="middle", fill=GRAY)
    arrow(s, n4[0] - 4, n4[1] + 6, 286, 226, col=GRAY, ar="ar-gray", dash="4 3", sw=1.2)
    T(s, 346, 302, "溝通、實作", anchor="end", fill=GRAY)
    arrow(s, 210, 166, 210, n1[1] + H + 6, col=GRAY, ar="ar-gray", dash="4 3", sw=1.2)
    T(s, 218, 138, "觀察", fill=GRAY)
    # 兩層的標示
    pill(s, n3[0] + W + 12, n3[1] + 6, "方向、規範、影響他人的改變", PM)
    T(s, n3[0] + W + 14, n3[1] + 48, "PM 在這一步越來越懂", fill=PM)
    pill(s, n4[0] + W + 12, n4[1] + 17, "已核准範圍內自主", AGENT)
    # 對的掌舵人
    rect(s, 640, 30, 220, 130, col=PM, fill=PM, op=".06", sw=1.3, dash="5 3")
    T(s, 654, 54, "對的掌舵人", cls="tx", fill=PM, w=700)
    for i, t in enumerate(["有使命感與推動的權威", "知道成功的樣子", "弄懂了才核准", "重要的事親自面對團隊"]):
        T(s, 660, 80 + 21 * i, "· " + t, fill=INK2)
    bottom(s, 390, [
        ("agent 不眠不休地轉這個循環；每個方向上的決定都經過 PM 理解與核准。", True),
        ("核准建立在理解上，PM 在一圈圈的循環裡，也逐漸掌握 CI/CD 的做法與精神。", False),
    ])
    aria = ("五步循環：1 觀察 repo、變更與團隊；2 提案，附上原則、取捨與替代做法；3 PM 理解後核准；4 執行，實作並與工程師溝通；5 回報團隊全貌與進展，附證據；再回到觀察。"
            "第 3 步標示方向、規範、影響他人的改變需要 PM 核准，PM 在這一步越來越懂；第 4 步標示在已核准範圍內 agent 自主。"
            "圈內是工程團隊，repo 與流程的主人。右上列出對的掌舵人的條件：有使命感與推動的權威、知道成功的樣子、弄懂了才核准、重要的事親自面對團隊。")
    return svg(s, 880, 480, aria)


PAGES = [
    ("方向：AI 要跨部門發揮效益，前提是先有迭代式開發與 CI/CD", p1()),
    ("背景：CI/CD 假設的小步 submit、自動驗證等習慣，IC 團隊多半沒有", p2()),
    ("心態：工程師認同 CI/CD，卻懷疑非做不可、也懷疑做得到", p3()),
    ("推動者：想推 CI/CD 的主管知道目標，說不出第一步要改哪個流程", p4()),
    ("搭配：AI 出 CI/CD 知識與動手能力，人類 PM 定方向與優先序", p5()),
    ("協作：agent 自己觀察、提案、執行、回報，方向由 PM 弄懂後核准", p6()),
]

if __name__ == "__main__":
    build(NAME, "AI agent 與人類 PM 搭檔，讓 CI/CD 在 IC 設計團隊運作起來", KICKER, PAGES)

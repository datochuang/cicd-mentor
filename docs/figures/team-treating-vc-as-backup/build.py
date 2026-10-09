# -*- coding: utf-8 -*-
# 《把版控當備份的團隊：depot 留住檔案，留不住答案》：docs/slides/team-treating-vc-as-backup.{html,pdf}
# 執行：python3 docs/figures/team-treating-vc-as-backup/build.py
#
# 讀者：公司內部的主管與工程師。每天用 Perforce，熟悉自己團隊的做法，沒有把這些做法和後面的問題連起來看過。
# 讀完要能：在圖裡認出自己團隊的做法，說出哪些問題是從這些做法長出來的。
# 主旨：把版控當備份的團隊，depot 裡有檔案，但結果的來源、跑法、環境與理由都在人身上；
#       問題在整合、交接與人員異動時浮現。
# 脈絡：1 總覽（一張圖：depot 留得住的、答不出的；十六個問題歸成六個原則；2026-10-09 加）→ 2–4 具體怎麼運作 → 5–17 造成什麼問題（10–17 為 2026-10-09 追加）→ 18 總結 → 19 收斂成六個原則（之後對策的定錨點；第六個 Code review 待使用者確認）。
# 所有路徑、CL 號碼、label 名稱都是示意，不對應任何實際專案。
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from slides import *

NAME = "team-treating-vc-as-backup"
KICKER = "版控只當備份的團隊"


def check(s, x, y, ok, text, col=None, cls="tx"):
    c = col or (GOAL if ok else WARN)
    T(s, x, y, "✓" if ok else "✗", cls="tx", fill=c, w=700)
    T(s, x + 20, y, text, cls=cls, fill=INK2 if cls == "tx" else c)



# ── 圖 1：總覽（一張圖：depot 留得住的、答不出的；十六個問題歸成六個原則）──
# 每個問題只掛在一個最直接的原則下（圖 19 的對應是多對多，這裡為了一眼看懂只取一個）；數字是那個問題的頁。
OVERVIEW = [
    ("Small batches", [("大包 submit", 2), ("說明只寫 update", 2)]),
    ("Single Source of Truth", [("五個地方散落", 3), ("產物進 depot", 12), ("IP 解壓覆蓋", 13), ("flow 每案複製一份", 14)]),
    ("Traceability", [("label 只有檔案", 4), ("哪一版跑的要問人", 5), ("兩台機器不同結果", 15), ("退不回去", 17)]),
    ("Continuous Integration", [("壞了很久才發現", 6), ("沒有 branch，main 會壞", 9), ("Excel 狀態表", 16)]),
    ("Self-documenting", [("流程只在人腦", 7), ("下游沒清單", 7), ("目錄沒說明", 8)]),
    ("Code review", [("沒有 review", 10), ("resolve 整份收", 11)]),
]


def p0():
    s = []
    T(s, 20, 20, "這份文件回答：把版控當備份的團隊每天怎麼運作、長出哪些問題、這些問題歸成哪幾個原則", cls="tx-lbl", fill=INK2)
    rect(s, 20, 34, 230, 150, col=GOAL, fill=GOAL, op=".06", sw=1.4)
    T(s, 32, 54, "depot 留得住的", cls="tx", fill=GOAL, w=700)
    for j, t in enumerate(["每個檔案的最新版與歷史", "誰在什麼時候改了哪個檔", "舊版救得回來", "label 那天的檔案清單"]):
        check(s, 32, 80 + 24 * j, True, t)
    rect(s, 20, 196, 230, 150, col=WARN, fill=WARN, op=".06", sw=1.4, dash="6 4")
    T(s, 32, 216, "depot 答不出的", cls="tx", fill=WARN, w=700)
    for j, t in enumerate(["這份結果是哪一版跑的", "乾淨的機器能不能重跑", "哪一次改動弄壞的", "併入前誰看過"]):
        check(s, 32, 242 + 24 * j, False, t)
    T(s, 20, 366, "今天這些都由某個人的記憶回答", fill=GRAY)
    arrow(s, 256, 190, 286, 190, col=WARN, ar="ar-w", sw=2)
    T(s, 290, 24, "", fill=GRAY)
    for i, (name, items) in enumerate(OVERVIEW):
        col_, row = i % 3, i // 3
        bx, by, bw, bh = 290 + col_ * 192, 34 + row * 162, 184, 150
        rect(s, bx, by, bw, bh, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
        T(s, bx + 10, by + 20, name, cls="tx", fill=GOAL, w=700)
        x, y = bx + 10, by + 32
        for t, pg in items:
            w_ = width(t, 10.5) + 20
            if x + w_ > bx + bw - 8:
                x, y = bx + 10, y + 26
            pill(s, x, y, t, WARN, h=20)
            x += w_ + 6
        T(s, bx + 10, by + bh - 10, "圖 " + "、".join(str(pg) for pg in sorted({pg for _, pg in items})), fill=GRAY)
    bottom(s, 380, [
        ("備份做到了：檔案留得住；「哪一版跑的、能不能重跑、誰看過」答不出。十六個問題歸成六個原則，之後的對策一一對應。", True),
        ("右邊每個框是一個原則，框裡是沒做到它時長出的問題，圖號是講那個問題的頁。", False),
    ])
    aria = ("左上 depot 留得住的四個打勾：每個檔案的最新版與歷史、誰在什麼時候改了哪個檔、舊版救得回來、label 那天的檔案清單。左下 depot 答不出的四個打叉：這份結果是哪一版跑的、乾淨的機器能不能重跑、哪一次改動弄壞的、併入前誰看過；今天都由某個人的記憶回答。"
            "右邊六個框，各一個原則與沒做到時的問題：Small batches（大包 submit、說明只寫 update）；Single Source of Truth（五個地方散落、產物進 depot、IP 解壓覆蓋、flow 每案複製一份）；"
            "Traceability（label 只有檔案、哪一版跑的要問人、兩台機器不同結果、退不回去）；Continuous Integration（壞了很久才發現、沒有 branch main 會壞、Excel 狀態表）；"
            "Self-documenting（流程只在人腦、下游沒清單、目錄沒說明）；Code review（沒有 review、resolve 整份收）。每框附圖號。")
    return svg(s, 880, 480, aria)


# ── 圖 2：日常 ──────────────────────────────────────────────────────
EDITS = ["改 RTL", "跑 sim", "改 tb", "改 RTL", "改 .f", "跑 sim", "改 script", "改 RTL",
         "跑 sim", "改 tb", "改 RTL", "跑 regression", "改 RTL", "跑 sim"]
SUBMITS = [(340, "CL 48211", "update"), (590, "CL 48977", "fix"), (790, "CL 49340", "before freeze")]
TRIGGERS = ["里程碑到了", "有人跟你要", "休假前", "怕 workspace 壞掉", "主管提醒"]
BUNDLE = ["好幾個 block 的 RTL", "順手改的 script", "新的 testbench", "一起改的 .f"]


def p1():
    s = []
    T(s, 20, 20, "這份文件回答：把版控當備份的團隊，每天具體怎麼做事；問題從這些做法的哪裡長出來 ↓", cls="tx-lbl", fill=INK2)
    x0, x1 = 190, 860
    # 個人 workspace：持續在改
    T(s, 20, 74, "個人 workspace", cls="tx", fill=INK2, w=700)
    T(s, 20, 92, "p4 client，只有自己看得到", fill=GRAY)
    rect(s, x0, 46, x1 - x0, 66, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2, rx=4)
    step = (x1 - x0 - 16) / len(EDITS)
    for i, e in enumerate(EDITS):
        x = x0 + 8 + step * i + step / 2
        line(s, x, 54, x, 72, col=INK2, sw=1.6)
        T(s, x, 90 if i % 2 == 0 else 105, e, anchor="middle", fill=INK2)
    # depot：隔很久才收到一大包
    T(s, 20, 238, "Perforce depot", cls="tx", fill=INK2, w=700)
    T(s, 20, 256, "大家看得到的那份", fill=GRAY)
    line(s, x0, 232, x1, 232, col="var(--rule-2)", sw=1.4)
    for i, (cx, cl, desc) in enumerate(SUBMITS):
        w, h, y = 140, 50, 207
        x = cx - w / 2
        rect(s, x + 8, y - 8, w, h, col="var(--rule-2)", fill="var(--surface)", sw=1)
        rect(s, x + 4, y - 4, w, h, col="var(--rule-2)", fill="var(--surface)", sw=1)
        rect(s, x, y, w, h, col=INK2, fill="var(--surface)", sw=1.4)
        T(s, x + 12, y + 21, cl, cls="tx", fill=INK2, w=700)
        T(s, x + 12, y + 39, "說明：" + desc, fill=GRAY)
        arrow(s, cx, 116, cx, y - 12, col=INK2, ar="ar", sw=1.4)
        if i == 0:
            T(s, cx + 10, 160, "submit 一大包", cls="tx", fill=INK2, w=600)
    T(s, 465, 282, "這段期間 depot 沒有任何變化", anchor="middle", fill=GRAY)
    T(s, 20, 314, "什麼時候才 submit", cls="tx-lbl", fill=INK2)
    x = 190
    for t in TRIGGERS:
        x += pill(s, x, 300, t, GRAY) + 8
    T(s, 20, 348, "一包裡面有什麼", cls="tx-lbl", fill=INK2)
    x = 190
    for t in BUNDLE:
        x += pill(s, x, 334, t, GRAY) + 8
    bottom(s, 378, [
        ("submit 的目的是把檔案存起來，所以在怕丟、有人要、里程碑到了的時候才做。", True),
        ("兩次 submit 之間的所有改動，只存在這個人的 workspace 裡，別人看不到也用不到。", False),
    ])
    aria = ("兩條水平的泳道。上面是個人 workspace，一整條都是密集的改動：改 RTL、跑 sim、改 testbench、改 filelist、改 script。"
            "下面是 Perforce depot，只在三個點各收到一包很大的 submit，說明分別是 update、fix、before freeze；兩包之間 depot 沒有任何變化。"
            "下方列出什麼時候才 submit：里程碑到了、有人跟你要、休假前、怕 workspace 壞掉、主管提醒；以及一包裡面有什麼：好幾個 block 的 RTL、順手改的 script、新的 testbench、一起改的 filelist。")
    return svg(s, 880, 480, aria)


# ── 圖 2：散落 ──────────────────────────────────────────────────────
PLACES = [
    ("Perforce depot", True, ["RTL（大部分）", "testbench（一部分）", "舊版的 filelist", "有時連 netlist 也進"]),
    ("個人 workspace", False, ["改到一半的 RTL", "新寫的 testbench", "修過才跑得過的 .f", "本機的 patch"]),
    ("共用磁碟 /proj", False, ["run 目錄與 log", "regression 的 script", "交給 PD 的 tarball", "大家共用的 lib"]),
    ("home 目錄與 wiki", False, [".cshrc 裡的 module", "工具版本", "license 設定", "一頁過期的步驟"]),
    ("人的腦袋", False, ["哪個 run 對應哪一版", "為什麼這樣改", "哪些檔案沒在用", "先跑哪個再跑哪個"]),
]


def p2():
    s = []
    T(s, 440, 30, "從一台乾淨的機器把 regression 重跑一次，需要的東西在哪裡？", cls="tx", anchor="middle", fill=INK2, w=700)
    line(s, 440, 38, 440, 56, col="var(--rule-2)", sw=1.4)
    line(s, 100, 56, 780, 56, col="var(--rule-2)", sw=1.4)
    for i, (name, inrepo, items) in enumerate(PLACES):
        x, y, w, h = 20 + i * 170, 70, 160, 220
        cx = x + w / 2
        line(s, cx, 56, cx, y, col="var(--rule-2)", sw=1.4)
        if inrepo:
            rect(s, x, y, w, h, col=INK2, fill="var(--surface)", sw=1.6)
        else:
            rect(s, x, y, w, h, col=WARN, fill=WARN, op=".05", sw=1.4, dash="6 4")
        T(s, x + 12, y + 24, name, cls="tx", fill=INK2 if inrepo else WARN, w=700)
        pill(s, x + 12, y + 36, "進版控" if inrepo else "沒進版控", INK2 if inrepo else WARN, h=18)
        for j, it in enumerate(items):
            T(s, x + 12, y + 86 + 24 * j, it, fill=INK2)
    yb = 304
    line(s, 190, yb, 860, yb, col=WARN, sw=1.2)
    line(s, 190, yb - 6, 190, yb, col=WARN, sw=1.2)
    line(s, 860, yb - 6, 860, yb, col=WARN, sw=1.2)
    T(s, 525, yb + 18, "這四處的東西，換一台機器就不在", cls="tx", anchor="middle", fill=WARN, w=600)
    T(s, 100, yb + 18, "只有這一格進了版控", anchor="middle", fill=GRAY)
    bottom(s, 350, [
        ("depot 裡只有檔案的一部分；要跑得起來，其餘的東西散在磁碟、home 目錄和人的腦袋裡。", True),
        ("換一台乾淨的機器，照 depot 的內容做不出同一個結果。", False),
    ])
    aria = ("頂端的問題：從一台乾淨的機器把 regression 重跑一次，需要的東西在哪裡？線往下分到五個方塊："
            "Perforce depot（進版控：RTL 大部分、testbench 一部分、舊版的 filelist、有時連 netlist 也進）；"
            "個人 workspace（沒進版控：改到一半的 RTL、新寫的 testbench、修過才跑得過的 filelist、本機的 patch）；"
            "共用磁碟（沒進版控：run 目錄與 log、regression 的 script、交給 PD 的 tarball、共用的 lib）；"
            "home 目錄與 wiki（沒進版控：.cshrc 裡的 module、工具版本、license 設定、過期的步驟）；"
            "人的腦袋（沒進版控：哪個 run 對應哪一版、為什麼這樣改、哪些檔案沒在用、先跑哪個再跑哪個）。後四格以括號標示換一台機器就不在。")
    return svg(s, 880, 480, aria)


# ── 圖 3：交付 ──────────────────────────────────────────────────────
RESULT_STEPS = [
    ("在自己的 workspace 跑完", "結果留在 run 目錄", False),
    ("把 run 目錄的路徑貼進 email", "/proj/chipA/yuting/run_0917_v3/", False),
    ("收件人照路徑進去看 log 與 report", "看到的是當下目錄裡的內容", False),
    ("之後那個目錄被覆蓋或清掉", "email 裡的路徑還在，內容已經換了", True),
]
LABEL_MISSING = ["simulator 與 synthesis 工具的版本", "環境變數與 license 設定", "跑了哪些測試、結果如何", "怎麼跑：script 在誰的目錄"]


def p3():
    s = []
    T(s, 20, 24, "一次 regression 的結果怎麼傳出去", cls="tx-lbl", fill=INK2)
    for i, (t, sub, bad) in enumerate(RESULT_STEPS):
        y = 40 + i * 74
        if bad:
            rect(s, 20, y, 380, 52, col=WARN, fill=WARN, op=".06", sw=1.4, dash="6 4")
        else:
            rect(s, 20, y, 380, 52, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
        T(s, 34, y + 21, t, cls="tx", fill=WARN if bad else INK2, w=700)
        T(s, 34, y + 40, sub, fill=INK2)
        if i < 3:
            arrow(s, 210, y + 56, 210, y + 70, col=INK2, ar="ar", sw=1.4)
    T(s, 440, 24, "里程碑時打一個 label", cls="tx-lbl", fill=INK2)
    pill(s, 440, 40, "label  RTL_FREEZE_v2", INK2, h=24)
    T(s, 440, 98, "它記得", cls="tx-lbl", fill=GOAL)
    check(s, 452, 122, True, "哪些檔案、各是哪個版本")
    T(s, 440, 160, "它不記得", cls="tx-lbl", fill=WARN)
    for j, t in enumerate(LABEL_MISSING):
        check(s, 452, 184 + 28 * j, False, t)
    bottom(s, 346, [
        ("結果和它的來源之間沒有連結：email 裡的路徑指向一個會變的目錄，label 只記得檔案。", True),
        ("想知道某個結果是怎麼來的，只能找到跑的那個人問。", False),
    ])
    aria = ("左欄是一次 regression 的結果怎麼傳出去，四步：在自己的 workspace 跑完；把 run 目錄的路徑貼進 email；收件人照路徑進去看 log 與 report；"
            "之後那個目錄被覆蓋或清掉，email 裡的路徑還在但內容已經換了。右欄是里程碑時打的 label，例如 RTL_FREEZE_v2：它記得哪些檔案、各是哪個版本；"
            "它不記得 simulator 與 synthesis 工具的版本、環境變數與 license 設定、跑了哪些測試與結果、怎麼跑與 script 在誰的目錄。")
    return svg(s, 880, 480, aria)


# ── 圖 4：哪一版 ────────────────────────────────────────────────────
STOPS = [("PL 問", "這份報告是哪一版跑的？", None),
         ("跑的人回想", "「應該是上次 sync 那版」", "靠記憶"),
         ("翻 workspace", "還有改到一半的檔案", "靠當下的狀態"),
         ("問 CAD", "工具版本看 .cshrc", "靠記憶"),
         ("翻 email 找路徑", "run 目錄已經換過內容", "靠目錄還沒被清")]
NO_RECORD = ["改動只在 workspace，沒有 CL 號碼", "label 沒記工具版本", "run 目錄會被覆蓋", "跑法在個人的 script 裡"]


def p4():
    s = []
    for i, (t, sub, how) in enumerate(STOPS):
        x, y, w, h = 20 + i * 170, 50, 150, 64
        if i == 0:
            rect(s, x, y, w, h, col=INK2, fill="var(--surface)", sw=1.6)
        else:
            rect(s, x, y, w, h, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
        T(s, x + 12, y + 24, t, cls="tx", fill=INK2, w=700)
        T(s, x + 12, y + 46, sub, fill=INK2)
        if how:
            pill(s, x + 12, y + h + 10, how, GRAY, h=18)
        if i < 4:
            arrow(s, x + w + 3, y + h / 2, x + w + 17, y + h / 2, col=INK2, ar="ar", sw=1.4)
    arrow(s, 840, 116, 840, 158, col=WARN, ar="ar-w", sw=1.6)
    y = 162
    rect(s, 20, y, 840, 60, col=WARN, fill=WARN, op=".08", sw=1.6)
    T(s, 34, y + 26, "答案", cls="tx", fill=WARN, w=700)
    T(s, 90, y + 26, "「大概是 CL 48977 加上我手上改的幾個，工具應該是那一版，結果你看我 email 裡那個路徑」", cls="tx", fill=INK2)
    T(s, 90, y + 48, "每個「大概」「應該」，各對應一個沒有紀錄的地方", fill=WARN)
    T(s, 20, 264, "沒有紀錄的地方", cls="tx-lbl", fill=WARN)
    x = 20
    for t in NO_RECORD:
        x += pill(s, x, 276, t, WARN) + 8
    bottom(s, 332, [
        ("沒有任何一筆紀錄把結果、檔案版本、工具版本和跑法綁在一起。", True),
        ("答案由幾個人的記憶拼出來，每一段都帶著「應該」。", False),
    ])
    aria = ("一條問答的鏈：PL 問這份報告是哪一版跑的；跑的人回想，說應該是上次 sync 那版（靠記憶）；翻 workspace，還有改到一半的檔案（靠當下的狀態）；"
            "問 CAD，工具版本看 .cshrc（靠記憶）；翻 email 找路徑，run 目錄已經換過內容（靠目錄還沒被清）。"
            "最後的答案：大概是 CL 48977 加上我手上改的幾個，工具應該是那一版，結果你看我 email 裡那個路徑。"
            "下方列出沒有紀錄的地方：改動只在 workspace 沒有 CL 號碼、label 沒記工具版本、run 目錄會被覆蓋、跑法在個人的 script 裡。")
    return svg(s, 880, 480, aria)


# ── 圖 5：壞掉發現得晚 ──────────────────────────────────────────────
OTHERS = ["update", "fix", "sync", "misc", "update", "fix", "update"]


def p5():
    s = []
    ty = 120
    arrow(s, 40, ty, 850, ty, col="var(--rule-2)", ar="ar-gray", sw=1.6)
    rect(s, 50, 78, 180, 84, col="var(--surface)", fill="var(--surface)", sw=0)
    rect(s, 50, 78, 180, 84, col=WARN, fill=WARN, op=".06", sw=1.4, dash="6 4")
    T(s, 64, 100, "改壞的那次 submit", cls="tx", fill=WARN, w=700)
    T(s, 64, 120, "一大包，說明是『update』", fill=INK2)
    T(s, 64, 140, "當時沒有人知道它壞了", fill=INK2)
    T(s, 260, 70, "其他人的 submit，一樣一包一包", cls="tx-lbl", fill=GRAY)
    for i, d in enumerate(OTHERS):
        x = 260 + i * 64
        rect(s, x, 103, 56, 34, col="var(--rule-2)", fill="var(--surface-2)", sw=1.1)
        T(s, x + 28, 125, d, anchor="middle", fill=GRAY)
    rect(s, 710, 78, 150, 84, col="var(--surface)", fill="var(--surface)", sw=0)
    rect(s, 710, 78, 150, 84, col=WARN, fill=WARN, op=".14", sw=1.8)
    T(s, 724, 100, "整合時發現", cls="tx", fill=WARN, w=700)
    T(s, 724, 120, "top 編不過", fill=INK2)
    T(s, 724, 140, "或下游跑不起來", fill=INK2)
    yb = 178
    line(s, 50, yb, 700, yb, col=WARN, sw=1.2)
    line(s, 50, yb - 6, 50, yb, col=WARN, sw=1.2)
    line(s, 700, yb - 6, 700, yb, col=WARN, sw=1.2)
    T(s, 375, yb + 18, "回頭要查的範圍：每一包都要拆開看", cls="tx", anchor="middle", fill=WARN, w=600)
    T(s, 20, 240, "怎麼找", cls="tx-lbl", fill=INK2)
    for j, t in enumerate(["一包一包拆開，猜哪幾個檔案有關", "逐個問當時改了什麼", "在自己的 workspace 把舊版換回來試"]):
        T(s, 32, 264 + 22 * j, "· " + t, cls="tx", fill=INK2)
    T(s, 460, 240, "誰先發現", cls="tx-lbl", fill=INK2)
    x = 460
    for t in ["整合的人", "PD", "DV", "韌體", "客戶"]:
        x += pill(s, x, 252, t, GRAY) + 8
    T(s, 460, 300, "發現的人離那次改動最遠，手上沒有線索", fill=GRAY)
    bottom(s, 332, [
        ("改動進 depot 時沒有任何檢查，問題要等到整合或下游才浮現。", True),
        ("從發現點往回找，中間每一包都要拆開看；一次送進的東西越多，越難切。", False),
    ])
    aria = ("一條 depot 的時間軸。最左邊是改壞的那次 submit，一大包、說明是 update、當時沒有人知道它壞了；中間是其他人的七包 submit；"
            "最右邊是整合時發現，top 編不過或下游跑不起來。括號標出從改壞那次到發現點之間，每一包都要拆開看。"
            "下方：怎麼找，一包一包拆開猜哪幾個檔案有關、逐個問當時改了什麼、在自己的 workspace 把舊版換回來試；誰先發現：整合的人、PD、DV、韌體、客戶。")
    return svg(s, 880, 480, aria)


# ── 圖 6：交接與離開 ────────────────────────────────────────────────
DOWNSTREAM_Q = ["跟上一包差在哪？", "哪些是刻意改的、哪些是順手改的？", "這包和 label 的內容一樣嗎？", "出問題了，要回報哪一版？"]
KNOW = ["regression 怎麼跑", "哪些檔案沒在用", "為什麼這樣接", "環境怎麼設", "run 和版本的對應"]


def p6():
    s = []
    T(s, 20, 24, "交給下游", cls="tx-lbl", fill=INK2)
    rect(s, 20, 40, 160, 56, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
    T(s, 34, 62, "上游工程師", cls="tx", fill=INK2, w=700)
    T(s, 34, 82, "從 workspace 手動打包", fill=INK2)
    arrow(s, 184, 68, 212, 68, col=INK2, ar="ar", sw=1.4)
    rect(s, 216, 40, 184, 56, col=INK2, fill="var(--surface)", sw=1.4)
    T(s, 230, 62, "chipA_rtl_0917.tgz", cls="tx", fill=INK2, w=700)
    T(s, 230, 82, "README：改了…（靠回想）", fill=INK2)
    arrow(s, 308, 100, 308, 122, col=INK2, ar="ar", sw=1.4)
    rect(s, 20, 126, 380, 44, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
    T(s, 34, 153, "下游：PD、DV、韌體、客戶", cls="tx", fill=INK2, w=700)
    T(s, 20, 200, "下游問不出來的", cls="tx-lbl", fill=WARN)
    for j, t in enumerate(DOWNSTREAM_Q):
        check(s, 32, 224 + 26 * j, False, t)
    T(s, 460, 24, "人離開的時候", cls="tx-lbl", fill=INK2)
    rect(s, 460, 40, 160, 180, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
    T(s, 474, 62, "資深工程師知道的", cls="tx", fill=INK2, w=700)
    for j, t in enumerate(KNOW):
        T(s, 474, 90 + 22 * j, "· " + t, fill=INK2)
    arrow(s, 624, 126, 696, 126, col=WARN, ar="ar-w", sw=1.6)
    T(s, 660, 114, "離職／調組", anchor="middle", fill=WARN)
    rect(s, 700, 40, 160, 180, col=WARN, fill=WARN, op=".05", sw=1.4, dash="6 4")
    T(s, 714, 62, "接手的人拿到的", cls="tx", fill=WARN, w=700)
    for j, t in enumerate(KNOW):
        T(s, 714, 90 + 22 * j, "✗ " + t, fill=WARN)
    T(s, 714, 208, "depot 裡只剩一堆檔案", fill=INK2)
    bottom(s, 332, [
        ("下游收到的是一包檔案，拿不到它的來歷。", True),
        ("工作流程存在人身上，人離開的時候，depot 留不住它。", False),
    ])
    aria = ("左半：上游工程師從 workspace 手動打包成 chipA_rtl_0917.tgz，README 靠回想寫改了什麼，交給下游 PD、DV、韌體、客戶。"
            "下游問不出來的：跟上一包差在哪、哪些是刻意改的哪些是順手改的、這包和 label 的內容一樣嗎、出問題了要回報哪一版。"
            "右半：資深工程師知道的 regression 怎麼跑、哪些檔案沒在用、為什麼這樣接、環境怎麼設、run 和版本的對應；離職或調組之後，接手的人拿到的這五項都打叉，depot 裡只剩一堆檔案。")
    return svg(s, 880, 480, aria)


# ── 圖 7：目錄靠人帶路 ──────────────────────────────────────────────
TREE = [
    ("/proj/chipA/", ""),
    ("  rtl/", "哪些檔案還在用？"),
    ("  rtl_old/", "能刪嗎？"),
    ("  rtl_new2/", "跟 rtl/ 差在哪？"),
    ("  sim/", ""),
    ("  sim_yuting/", "個人的，還是正式的？"),
    ("  scripts/", "哪個才是正式的？"),
    ("  scripts_bak/", ""),
    ("  release_0917/", "跟 label 的內容一樣嗎？"),
    ("  tmp/", ""),
    ("  top.f", "引用的檔案一半在 rtl_new2/"),
    ("  README", "寫的是上一個專案"),
]
WORKSPACES = [("chipA 的 workspace", "rtl_new2/ sim_yuting/"), ("chipB 的 workspace", "src/ verif_old/ run2/"), ("IP-X 的 workspace", "design/ tb_v3/ tmp/")]


def p7():
    s = []
    T(s, 20, 24, "第一次打開專案目錄看到的：用途與相依都要猜", cls="tx-lbl", fill=INK2)
    rect(s, 20, 36, 380, 258, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
    for i, (name, q) in enumerate(TREE):
        y = 58 + 20 * i
        T(s, 34, y, name, fill=INK2)
        if q:
            T(s, 176, y, "? " + q, fill=WARN)
    T(s, 20, 316, "新來的工程師：問同事、慢慢摸；摸出來的地圖留在他腦袋裡", fill=GRAY)
    T(s, 440, 24, "通用的 AI agent 進到這些 workspace", cls="tx-lbl", fill=INK2)
    rect(s, 440, 120, 120, 172, col=AGENT, fill=AGENT, op=".10", sw=1.6)
    T(s, 500, 196, "通用 AI agent", cls="tx", anchor="middle", fill=AGENT, w=700)
    T(s, 500, 216, "讀得懂檔案", anchor="middle", fill=INK2)
    T(s, 500, 232, "讀不出用途", anchor="middle", fill=INK2)
    T(s, 584, 108, "每個 workspace 另寫一份", cls="tx-lbl", fill=WARN)
    for i, (name, sub) in enumerate(WORKSPACES):
        y = 120 + 64 * i
        arrow(s, 562, y + 22, 580, y + 22, col=AGENT, ar="ar-a", sw=1.4)
        rect(s, 584, y, 110, 44, col=WARN, fill=WARN, op=".06", sw=1.3, dash="5 3")
        T(s, 596, y + 27, "指引 " + name.split(" ")[0], cls="tx", fill=WARN, w=700)
        arrow(s, 698, y + 22, 712, y + 22, col=INK2, ar="ar", sw=1.4)
        rect(s, 716, y, 144, 44, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
        T(s, 724, y + 18, name, fill=INK2)
        T(s, 724, y + 35, sub, fill=GRAY)
    T(s, 440, 316, "指引誰寫得出來？", cls="tx-lbl", fill=WARN)
    x = 440
    for t, c in [("只有知道的那幾個人", WARN), ("有幾個 workspace 就要寫幾份", GRAY)]:
        x += pill(s, x, 326, t, c) + 8
    bottom(s, 362, [
        ("目錄的用途與相依關係沒有寫下來，新人靠問、靠摸；地圖最後還是只在人的腦袋裡。", True),
        ("通用的 AI agent 一樣看不懂，每個 workspace 都得由知道的人另寫一份指引。", False),
    ])
    aria = ("左邊是第一次打開專案目錄看到的樹：rtl、rtl_old、rtl_new2、sim、sim_yuting、scripts、scripts_bak、release_0917、tmp、top.f、README，"
            "旁邊是要猜的問題：哪些檔案還在用、能刪嗎、跟 rtl 差在哪、個人的還是正式的、哪個才是正式的、跟 label 的內容一樣嗎、top.f 引用的檔案一半在 rtl_new2、README 寫的是上一個專案。"
            "右邊是通用 AI agent，讀得懂檔案、讀不出用途；它要進 chipA、chipB、IP-X 三個 workspace，每個都要另寫一份指引；指引只有知道的那幾個人寫得出來，有幾個 workspace 就要寫幾份。")
    return svg(s, 880, 480, aria)


# ── 圖 8：沒有 branch ───────────────────────────────────────────────
SUBMITS_ON_MAIN = [(110, "A：半成品", True), (230, "B：修 bug", False), (350, "A：半成品", True), (470, "C：改 .f", False),
                   (590, "B：半成品", True), (710, "A：做完了", False), (810, "C：半成品", True)]
NO_BRANCH_HARMS = ["半成品留在 workspace，隔很久才進一大包（圖 1）", "半成品直接進 main，sync 到的人一起壞",
                   "沒有「做完、驗過」的關卡，CI 沒有觸發點", "一段工作和別人的改動混在 main 上，撤不回來",
                   "第二個版本靠複製目錄：rtl_new2/（圖 7）"]


def p8():
    s = []
    T(s, 20, 24, "今天：只有一條 main，所有人直接往上 submit", cls="tx-lbl", fill=INK2)
    for x, label, half in SUBMITS_ON_MAIN:
        col = WARN if half else "var(--rule-2)"
        if half:
            rect(s, x - 46, 38, 92, 24, col=WARN, fill=WARN, op=".06", sw=1.2, dash="4 3")
        else:
            rect(s, x - 46, 38, 92, 24, col="var(--rule-2)", fill="var(--surface-2)", sw=1.1)
        T(s, x, 54, label, anchor="middle", fill=WARN if half else INK2)
        arrow(s, x, 66, x, 82, col=WARN if half else INK2, ar="ar-w" if half else "ar", sw=1.2)
    arrow(s, 20, 88, 860, 88, col=INK2, ar="ar", sw=2)
    T(s, 24, 108, "main", cls="tx", fill=INK2, w=700)
    T(s, 150, 108, "✗ main 壞了，sync 到的人一起壞", fill=WARN)
    T(s, 630, 108, "✗ 又壞了", fill=WARN)
    # 少了的那條線
    rect(s, 20, 128, 380, 132, col=GOAL, fill=GOAL, op=".05", sw=1.4, dash="6 4")
    T(s, 34, 150, "少了的那條線：一段工作做完、驗過，再併回 main", cls="tx", fill=GOAL, w=700)
    line(s, 40, 182, 380, 182, col="var(--rule-2)", sw=1.6)
    T(s, 40, 174, "main", fill=GRAY)
    path(s, "M90,182 C110,182 110,216 130,216 L300,216 C320,216 320,182 340,182", col=GOAL, ar="ar-g", sw=1.8)
    for x in (165, 205, 245):
        s.append('<circle cx="%d" cy="216" r="4" fill="%s"/>' % (x, GOAL))
        T(s, x, 238, "小包", anchor="middle", fill=GOAL)
    rect(s, 266, 204, 36, 24, col="var(--surface)", fill="var(--surface)", sw=0)
    pill(s, 268, 206, "驗", GOAL, h=20)
    T(s, 346, 174, "併回", fill=GOAL)
    T(s, 34, 254, "branch 或 stream：Perforce 本來就有，團隊習慣上不用", fill=GRAY)
    # 沒有這條線的時候
    T(s, 440, 150, "沒有這條線的時候", cls="tx-lbl", fill=WARN)
    for j, t in enumerate(NO_BRANCH_HARMS):
        check(s, 452, 176 + 24 * j, False, t)
    bottom(s, 300, [
        ("branch 給半成品一個可以常常 submit、又不會弄壞 main 的地方；少了它，Small batches 和 CI 都沒有地方發生。", True),
        ("複製目錄成了 branch 的代替品，repo 因此越來越看不懂。", False),
    ])
    aria = ("上半：一條 main 的時間軸，A、B、C 三個人直接往上 submit，其中四包是半成品，標示 main 壞了、sync 到的人一起壞。"
            "左下是少了的那條線：從 main 分出一條 branch，上面三個小包、一個驗的關卡，再併回 main；Perforce 本來就有 branch 與 stream，團隊習慣上不用。"
            "右下列出沒有這條線的時候：半成品留在 workspace 隔很久才進一大包、半成品直接進 main 大家一起壞、沒有做完驗過的關卡 CI 沒有觸發點、"
            "一段工作和別人的改動混在 main 上撤不回來、第二個版本靠複製目錄。")
    return svg(s, 880, 480, aria)


# ── 圖 9–16：八個追加的問題（2026-10-09 加）。共用版型：左邊圖、右邊危害 ─────────
def problem_page(draw, harms, lines, aria, harms_y=70):
    s = []
    draw(s)
    T(s, 570, harms_y - 10, "危害", cls="tx-lbl", fill=WARN)
    for j, t in enumerate(harms):
        check(s, 582, harms_y + 14 + 26 * j, False, t, cls="tx-s")
    bottom(s, 350, lines)
    return svg(s, 880, 480, aria)


def box_p(s, x, y, w, h, title, sub=None, col=INK2, kind="plain"):
    if kind == "solid":
        rect(s, x, y, w, h, col=col, fill=col, op=".10", sw=1.6)
    elif kind == "dash":
        rect(s, x, y, w, h, col=col, fill=col, op=".05", sw=1.4, dash="6 4")
    else:
        rect(s, x, y, w, h, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
    T(s, x + 12, y + 21, title, cls="tx", fill=col, w=700)
    if sub:
        T(s, x + 12, y + 39, sub, fill=INK2)


# 圖 9：沒有 review
def n_review():
    def draw(s):
        T(s, 20, 24, "今天：submit 就是完成", cls="tx-lbl", fill=INK2)
        for i, t in enumerate(["改", "submit", "完成"]):
            x = 20 + i * 120
            box_p(s, x, 40, 100, 40, t)
            if i < 2:
                arrow(s, x + 103, 60, x + 117, 60, col=INK2, ar="ar", sw=1.4)
        s.append('<text x="40" y="170" style="font-family:var(--sans);font-size:64px;font-weight:700;fill:%s">0</text>' % WARN)
        T(s, 90, 150, "個人在 submit 之前", cls="tx", fill=INK2)
        T(s, 90, 170, "看過這一包", cls="tx", fill=INK2)
        rect(s, 20, 200, 520, 96, col=WARN, fill=WARN, op=".05", sw=1.3, dash="6 4")
        T(s, 34, 224, "review 只發生在里程碑的 design review 會議", cls="tx", fill=WARN, w=700)
        T(s, 34, 246, "看的是投影片與架構，隔很久一次", fill=INK2)
        T(s, 34, 266, "會議上看不到任何一個 CL，也沒有人逐包看改了什麼", fill=INK2)
        T(s, 20, 322, "示意：A 改了 bus 的 ready 行為，B 的 block 到整合才發現", fill=GRAY)
    return problem_page(draw,
        ["interface 改了，用它的人整合時才知道", "錯誤要等機器或下游來抓", "為什麼這樣改，只有作者知道", "新人的寫法沒人修正，變成習慣"],
        [("submit 等於完成，所以沒有任何一包在併入前被第二個人看過。", True),
         ("design review 的會議看的是架構與投影片，看不到任何一個 CL。", False)],
        "左邊：改、submit、完成三步，底下一個大大的 0，表示 submit 之前看過這一包的人數；review 只發生在里程碑的 design review 會議，看的是投影片與架構，看不到任何 CL。"
        "右邊危害：interface 改了用它的人整合時才知道、錯誤要等機器或下游來抓、為什麼這樣改只有作者知道、新人的寫法沒人修正。")


# 圖 10：兩人改同一個檔
def n_conflict():
    def draw(s):
        box_p(s, 190, 20, 160, 40, "top.v", "兩個人同時 checkout")
        box_p(s, 20, 90, 230, 44, "A：改第 10–20 行", "ready 的時序", col=INK2)
        box_p(s, 300, 90, 230, 44, "B：改第 50–60 行", "新的 debug port", col=INK2)
        arrow(s, 230, 64, 150, 86, col=INK2, ar="ar", sw=1.2)
        arrow(s, 310, 64, 390, 86, col=INK2, ar="ar", sw=1.2)
        pill(s, 300, 146, "B 先 submit", GRAY)
        box_p(s, 20, 146, 230, 44, "A：sync，要 resolve", "兩邊都改了同一個檔")
        arrow(s, 135, 194, 135, 208, col=WARN, ar="ar-w", sw=1.4)
        box_p(s, 20, 212, 230, 44, "accept yours：整份用自己的", "沒看兩邊差在哪", col=WARN, kind="dash")
        arrow(s, 135, 260, 135, 274, col=WARN, ar="ar-w", sw=1.4)
        rect(s, 20, 278, 510, 44, col=WARN, fill=WARN, op=".12", sw=1.6)
        T(s, 34, 299, "top.v 裡 B 的第 50–60 行不見了", cls="tx", fill=WARN, w=700)
        T(s, 34, 316, "沒有錯誤訊息，submit 也成功", fill=INK2)
    return problem_page(draw,
        ["改動消失，沒有任何錯誤訊息", "要等下游壞了才發現，然後互相指責", "為了躲開，改成鎖檔或各改各的複本", "複本越多，離只有一份真相越遠"],
        [("resolve 需要看懂兩邊的改動；沒人看，就整份收下自己的。", True),
         ("版控給的是合併的機制，習慣上當成覆蓋。", False)],
        "兩人同時 checkout top.v：A 改第 10 到 20 行，B 改第 50 到 60 行。B 先 submit；A sync 後要 resolve，選了 accept yours 整份用自己的，"
        "結果 top.v 裡 B 的改動不見了，沒有錯誤訊息，submit 也成功。右邊危害：改動消失沒有訊息、要等下游壞了才發現、為了躲開改成鎖檔或各改各的複本、複本越多離只有一份真相越遠。")


# 圖 11：產物和來源一起進 depot
def n_derived():
    def draw(s):
        rect(s, 20, 30, 520, 150, col="var(--rule-2)", fill="var(--surface)", sw=1.2, dash="4 3")
        T(s, 32, 50, "depot", cls="tx-lbl", fill=GRAY)
        box_p(s, 50, 70, 180, 60, "rtl/　來源", "RTL 原始碼", col=GOAL, kind="solid")
        box_p(s, 330, 70, 180, 60, "netlist/　產物", "synthesis 跑出來的", col=WARN, kind="dash")
        arrow(s, 234, 100, 326, 100, col=INK2, ar="ar", sw=1.4)
        T(s, 280, 90, "synthesis", anchor="middle", fill=GRAY)
        T(s, 280, 160, "synthesis 在某人的 workspace 跑，產物再 submit 進來", anchor="middle", fill=GRAY)
        arrow(s, 140, 214, 140, 134, col=INK2, ar="ar", sw=1.4)
        T(s, 140, 232, "RTL 之後又改了", anchor="middle", fill=INK2)
        arrow(s, 420, 214, 420, 134, col=WARN, ar="ar-w", sw=1.6)
        T(s, 420, 232, "ECO 直接改 netlist", anchor="middle", fill=WARN)
        pill(s, 280, 256, "兩份對不上，哪一份算數？", WARN, anchor="middle")
        T(s, 20, 306, "下游拿的是 netlist；再跑一次 synthesis，ECO 就被蓋掉", fill=GRAY)
    return problem_page(draw,
        ["兩份真相，改哪一份才算數沒人說得清", "ECO 改在產物上，重新產生一次就消失", "產物對應哪一版來源，沒有紀錄", "depot 越來越大，sync 越來越久"],
        [("產物該由來源產生；進了 depot，它就成了第二份真相。", True),
         ("改產物比改來源快，所以 ECO 都改在產物上；下一次重新產生，就把它蓋掉。", False)],
        "depot 裡同時有 rtl 來源和 netlist 產物，netlist 由某人在 workspace 跑 synthesis 產生。之後 RTL 又改了，ECO 卻直接改在 netlist 上，兩份對不上。"
        "右邊危害：兩份真相改哪一份才算數沒人說得清、ECO 改在產物上重新產生一次就消失、產物對應哪一版來源沒有紀錄、depot 越來越大。")


# 圖 12：第三方 IP 解壓覆蓋
def n_ip():
    def draw(s):
        box_p(s, 20, 24, 120, 40, "IP vendor")
        rows = [("ip_v1.2.tgz", "解壓到 ip/，覆蓋", None),
                ("本地改了一個 lint 的 patch", "改在 ip/ 裡面", GOAL),
                ("ip_v1.3.tgz", "解壓到 ip/，覆蓋", None)]
        for i, (t, sub, col) in enumerate(rows):
            y = 84 + i * 62
            if col:
                box_p(s, 180, y, 230, 44, t, sub, col=col, kind="solid")
            else:
                box_p(s, 180, y, 230, 44, t, sub)
                arrow(s, 80, 68, 80, y + 22, col=INK2, ar=None, sw=1) if False else None
            if i < 2:
                arrow(s, 295, y + 48, 295, y + 58, col=INK2, ar="ar", sw=1.2)
        arrow(s, 144, 44, 176, 100, col=INK2, ar="ar", sw=1.2)
        arrow(s, 144, 44, 176, 228, col=INK2, ar="ar", sw=1.2)
        rect(s, 430, 84, 110, 168, col=WARN, fill=WARN, op=".05", sw=1.3, dash="6 4")
        T(s, 442, 106, "ip/ 現在是", cls="tx", fill=WARN, w=700)
        T(s, 442, 126, "v1.3？", fill=INK2)
        T(s, 442, 144, "加上 patch？", fill=INK2)
        T(s, 442, 162, "patch 被蓋掉了？", fill=INK2)
        T(s, 442, 190, "depot 裡只看到", fill=GRAY)
        T(s, 442, 206, "一大包檔案換掉", fill=GRAY)
        T(s, 442, 222, "說明：update ip", fill=GRAY)
        T(s, 20, 296, "示意：lint patch 在 v1.3 解壓時被蓋掉，重新 lint 才發現", fill=GRAY)
    return problem_page(draw,
        ["本地 patch 被下一次 drop 蓋掉", "晶片裡是哪一版 IP，只能問解壓的人", "vendor 的 errata 對不上手上的版本", "兩個專案用同一個 IP 的不同版，沒人知道"],
        [("IP 以 tarball 進來、解壓覆蓋，版控裡看不出 drop 與 drop 之間的差異。", True),
         ("每一次 drop 都是一次沒有紀錄的大包 submit。", False)],
        "IP vendor 送來 ip_v1.2.tgz，解壓到 ip 目錄覆蓋；本地改了一個 lint 的 patch 在 ip 裡面；之後 ip_v1.3.tgz 又解壓覆蓋。ip 目錄現在是 v1.3 還是加上 patch，patch 被蓋掉了嗎，"
        "depot 裡只看到一大包檔案換掉、說明是 update ip。右邊危害：本地 patch 被下一次 drop 蓋掉、晶片裡是哪一版 IP 只能問解壓的人、vendor 的 errata 對不上、兩個專案用不同版沒人知道。")


# 圖 13：flow script 每個專案複製一份
def n_flow():
    def draw(s):
        box_p(s, 180, 20, 200, 44, "flow 的正本？", "沒有人說得出是哪一份", col=WARN, kind="dash")
        projs = [("chipA/scripts/", "改了幾處"), ("chipB/scripts/", "改了更多，修了一個 bug"), ("ipX/scripts/", "改最多，還加了功能")]
        for i, (t, sub) in enumerate(projs):
            x = 20 + i * 178
            arrow(s, 280, 68, x + 80, 100, col=GRAY, ar="ar-gray", sw=1.2, dash="4 3")
            box_p(s, x, 104, 160, 60, t, sub)
        pill(s, 198, 176, "修了一個 bug", GOAL)
        arrow(s, 190, 186, 110, 186, col=WARN, ar="ar-w", sw=1.4, dash="4 3")
        arrow(s, 318, 186, 400, 186, col=WARN, ar="ar-w", sw=1.4, dash="4 3")
        T(s, 100, 210, "✗ 傳不過去", fill=WARN)
        T(s, 400, 210, "✗ 傳不過去", fill=WARN)
        T(s, 20, 250, "複製的時候很快，複製之後各自演化", cls="tx", fill=INK2)
        T(s, 20, 272, "同一個 bug 在 chipA 與 ipX 還在；新專案不知道該從哪一份複製", fill=GRAY)
    return problem_page(draw,
        ["同一個 bug 在每個專案各修一次", "新專案不知道該從哪一份複製", "各專案 flow 行為不同，結果不能比", "沒有人知道哪一份是正本"],
        [("複製是最快的共用方式，複製之後就各自演化。", True),
         ("修好的東西留在修的那個專案裡。", False)],
        "flow 的正本沒有人說得出是哪一份；chipA、chipB、ipX 各複製一份 scripts，各改了不同的地方。chipB 修了一個 bug，傳不到 chipA 與 ipX。"
        "右邊危害：同一個 bug 各修一次、新專案不知道從哪一份複製、各專案 flow 行為不同結果不能比、沒有人知道哪一份是正本。")


# 圖 14：同一份 RTL，兩台機器結果不同
def n_env():
    def draw(s):
        box_p(s, 170, 20, 220, 40, "同一個 CL 48977 的 RTL", col=INK2)
        arrow(s, 230, 64, 140, 104, col=INK2, ar="ar", sw=1.2)
        arrow(s, 330, 64, 420, 104, col=INK2, ar="ar", sw=1.2)
        for x, title, items, res, col in [(20, "機器 A：yuting 的桌機", ["VCS 2023.03", "+define+FAST_SIM", "lib v1.2（本機的）"], "PASS", GOAL),
                                           (300, "機器 B：CAD farm", ["VCS 2024.09", "沒有 define", "lib v1.3"], "FAIL", WARN)]:
            rect(s, x, 108, 240, 124, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
            T(s, x + 12, 130, title, cls="tx", fill=INK2, w=700)
            for j, it in enumerate(items):
                T(s, x + 12, 154 + 20 * j, "· " + it, fill=INK2)
            pill(s, x + 240 - 12, 118, res, col, anchor="end")
        T(s, 20, 262, "差在哪？沒有任何紀錄：.cshrc、alias、環境變數、license feature", cls="tx", fill=WARN)
        T(s, 20, 286, "兩個人各自相信自己的環境，報告上只寫 PASS", fill=GRAY)
    return problem_page(draw,
        ["PASS 不代表對，FAIL 不代表錯", "報告上的 PASS 不知道是哪個環境跑的", "搬到 farm 或新機器就壞", "找差異只能逐項比 .cshrc"],
        [("跑的環境沒有跟著 RTL 一起進版控，同一份來源在不同機器上就是不同的設計。", True),
         ("結果能不能信，取決於跑的人記不記得自己的設定。", False)],
        "同一個 CL 的 RTL，在機器 A（VCS 2023.03、有 FAST_SIM define、本機的 lib v1.2）跑出 PASS，在機器 B（VCS 2024.09、沒有 define、lib v1.3）跑出 FAIL。差在哪沒有任何紀錄。"
        "右邊危害：PASS 不代表對 FAIL 不代表錯、報告上的 PASS 不知道是哪個環境、搬到 farm 就壞、找差異只能逐項比 .cshrc。")


# 圖 15：regression 狀態靠人填 Excel
def n_excel():
    def draw(s):
        steps = [("regression 跑完", "log 在 run 目錄", None), ("有人看 log", "挑幾個看", None), ("填進 Excel", "每週一次", WARN), ("PM 看 Excel", "看到的是上週的", None)]
        for i, (t, sub, col) in enumerate(steps):
            x = 20 + i * 132
            if col:
                box_p(s, x, 30, 120, 50, t, sub, col=col, kind="dash")
            else:
                box_p(s, x, 30, 120, 50, t, sub)
            if i < 3:
                arrow(s, x + 123, 55, x + 129, 55, col=INK2, ar="ar", sw=1.2)
        rect(s, 20, 110, 520, 130, col="var(--rule-2)", fill="var(--surface)", sw=1.2)
        T(s, 32, 130, "status.xlsx（示意）", cls="tx-lbl", fill=GRAY)
        cols = [40, 160, 260, 380]
        hdr = ["test", "result", "version", ""]
        rows = [["t_dma_basic", "PASS", "", "← log 其實還沒跑完"], ["t_dma_burst", "PASS", "上週五的", "← 版本靠回想"], ["t_irq_all", "？", "", "← 沒人填"]]
        for j, h in enumerate(hdr):
            T(s, cols[j], 152, h, fill=GRAY)
        line(s, 32, 158, 528, 158)
        for r, row in enumerate(rows):
            for j, c in enumerate(row):
                T(s, cols[j], 180 + 22 * r, c, fill=WARN if j == 3 else INK2)
        T(s, 20, 268, "表是機器結果的手抄本，抄的那一刻就開始脫節", cls="tx", fill=INK2)
    return problem_page(draw,
        ["表是上週的，結果是今天的", "PASS 的定義每個人不同", "版本欄靠回想，對不回 CL", "沒人敢信，最後還是去問跑的人"],
        [("結果由機器產生，狀態卻由人抄寫；抄的時候就跟實際脫節。", True),
         ("狀態表回答不了「這是哪一版、哪個環境跑的」。", False)],
        "四步：regression 跑完 log 在 run 目錄、有人看 log、每週填進 Excel、PM 看 Excel 看到的是上週的。示意的 status.xlsx 裡 result 寫 PASS 但 log 其實還沒跑完、version 欄靠回想或空白。"
        "右邊危害：表是上週的、PASS 的定義每個人不同、版本欄對不回 CL、沒人敢信最後還是去問跑的人。")


# 圖 16：想退回上次能跑的狀態
def n_rollback():
    def draw(s):
        arrow(s, 20, 50, 540, 50, col="var(--rule-2)", ar="ar-gray", sw=1.6)
        box_p(s, 20, 26, 170, 48, "上個里程碑：能跑", "label RTL_FREEZE_v2", col=GOAL, kind="solid")
        for i in range(6):
            x = 220 + i * 40
            rect(s, x, 40, 30, 20, col="var(--rule-2)", fill="var(--surface-2)", sw=1)
        box_p(s, 470, 26, 70, 48, "現在", "壞了", col=WARN, kind="solid")
        T(s, 20, 104, "想退回去", cls="tx-lbl", fill=INK2)
        items = [("sync 到 label", "檔案回去了", True), ("工具版本", "已經換了，舊版 license 沒了", False),
                 ("/proj 的 script", "已經被改過", False), ("ip/", "被下一個 drop 蓋掉", False), ("環境", ".cshrc 改過，沒人記得舊的", False)]
        for j, (t, sub, ok) in enumerate(items):
            y = 128 + 28 * j
            check(s, 32, y, ok, t, cls="tx")
            T(s, 190, y, sub, fill=INK2)
        rect(s, 360, 120, 180, 60, col=WARN, fill=WARN, op=".12", sw=1.6)
        T(s, 372, 144, "還是壞的", cls="tx", fill=WARN, w=700)
        T(s, 372, 164, "退不回去，只能往前修", fill=INK2)
        T(s, 20, 296, "所以 tape-out 前的 freeze 靠複製整個目錄：因為知道回不去", fill=GRAY)
    return problem_page(draw,
        ["label 只能回檔案，回不了環境與產物", "退不回去，只能往前硬修", "freeze 靠複製目錄，因為回不去", "風險只能累積，不能歸零"],
        [("回到一個能跑的狀態需要檔案、工具、環境、IP 一起回去；版控只記了檔案。", True),
         ("所以沒有人退回去，大家只往前修。", False)],
        "時間軸：上個里程碑能跑（label RTL_FREEZE_v2），中間六包 submit，現在壞了。想退回去：sync 到 label 檔案回去了；工具版本已經換了；/proj 的 script 被改過；ip 被下一個 drop 蓋掉；環境 .cshrc 改過沒人記得舊的。結果還是壞的，退不回去只能往前修。"
        "右邊危害：label 只能回檔案、退不回去只能往前硬修、freeze 靠複製目錄、風險只能累積不能歸零。")


# ── 圖 17：總結 ──────────────────────────────────────────────────────
DONE = ["檔案的最新版在哪", "誰在什麼時候改過哪個檔案", "舊版救得回來", "里程碑那天的檔案清單（label）"]
NOT = [("這個結果是哪一版做的？", "跑的人"), ("從乾淨的機器能重現嗎？", "沒人試過"), ("哪一次改動弄壞了它？", "大家一起猜"),
       ("下游收到的跟上一版差在哪？", "上游工程師"), ("跑的步驟與環境在哪裡？", "CAD 加跑的人"), ("這個檔案還有人在用嗎？", "最資深的人"),
       ("這個目錄裝什麼、靠哪些東西？", "帶你的那個人"), ("main 現在能用嗎？", "sync 了才知道"),
       ("這一包併入前誰看過？", "沒有人"), ("晶片裡是哪一版 IP？", "解壓的那個人")]


def p_summary():
    s = []
    T(s, 20, 40, "depot 做到的", cls="tx-lbl", fill=GOAL)
    for j, t in enumerate(DONE):
        check(s, 32, 72 + 25 * j, True, t)
    T(s, 20, 206, "備份要做的事，它都做到了", fill=GRAY)
    T(s, 440, 40, "depot 答不出來的", cls="tx-lbl", fill=WARN)
    T(s, 760, 40, "今天誰在回答", cls="tx-lbl", fill=GRAY)
    for j, (q, who) in enumerate(NOT):
        y = 72 + 25 * j
        check(s, 452, y, False, q)
        pill(s, 760, y - 14, who, GRAY, h=20)
    bottom(s, 322, [
        ("備份的功能它確實做到了；右邊每一題，今天都由某個人的記憶回答。", True),
        ("AI 的產出要跨團隊被採用，先得讓紀錄能回答右邊這些題。", False),
    ])
    aria = ("左欄 depot 做到的，四個打勾：檔案的最新版在哪、誰在什麼時候改過哪個檔案、舊版救得回來、里程碑那天的檔案清單。"
            "右欄 depot 答不出來的，六個打叉，各附今天誰在回答：這個結果是哪一版做的（跑的人）、從乾淨的機器能重現嗎（沒人試過）、哪一次改動弄壞了它（大家一起猜）、"
            "下游收到的跟上一版差在哪（上游工程師）、跑的步驟與環境在哪裡（CAD 加跑的人）、這個檔案還有人在用嗎（最資深的人）、這個目錄裝什麼靠哪些東西（帶你的那個人）、main 現在能用嗎（sync 了才知道）、這一包併入前誰看過（沒有人）、晶片裡是哪一版 IP（解壓的那個人）。")
    return svg(s, 880, 480, aria)

# ── 圖 18：收斂成六個原則 ─────────────────────────────────────────────
# 原則一律用英文專有名詞（2026-10-09 使用者定），中文只是註解。
ANCHORS = [
    ("Small batches", "小步常進", "改動小而頻繁地進到共用的地方，每一包說得出改了哪一件事",
     "隨便挑一包 submit，說得出它改了哪一件事", [1, 5, 8, 10]),
    ("Single Source of Truth", "SSOT　單一事實來源", "跑得起來需要的一切都在版控裡，而且只有一份；產物由來源產生",
     "換一台乾淨的機器，只靠版控的內容做出同一個結果", [2, 3, 6, 11, 12, 13, 14]),
    ("Traceability", "可追溯", "每個結果與交付物都連得回產生它的版本、工具、環境與步驟",
     "隨便拿一份結果，說得出它的版本、工具、環境與步驟", [3, 4, 6, 14, 15, 16]),
    ("Continuous Integration", "CI　變更即驗證", "改動進來的當下就被機器檢查，結果由機器寫下；共用的 main 隨時可用",
     "改壞的那一包進來時就被標出來，用不著等到整合", [5, 8, 15]),
    ("Self-documenting", "自我描述", "目錄的用途、相依、怎麼跑，寫在 repo 裡",
     "第一次來的人只讀 repo，就說得出每個目錄的用途與相依", [6, 7, 13]),
    ("Code review", "併入前有人看過", "每一包在併入 main 之前，有第二個人看過並留下紀錄",
     "隨便挑一包併入 main 的 submit，說得出誰看過、看了什麼", [8, 9, 10]),
]


def p_principles():
    s = []
    T(s, 20, 34, "原則", cls="tx-lbl", fill=GOAL)
    T(s, 250, 34, "意思，以及做得到／做不到的檢驗", cls="tx-lbl", fill=INK2)
    T(s, 640, 34, "沒做到時的問題（圖號）", cls="tx-lbl", fill=WARN)
    for i, (en, zh, meaning, test, figs) in enumerate(ANCHORS):
        y = 46 + 56 * i
        rect(s, 20, y + 8, 3, 40, col=GOAL, fill=GOAL, sw=0)
        T(s, 34, y + 24, en, cls="tx", fill=GOAL, w=700)
        T(s, 34, y + 43, zh, fill=GRAY)
        T(s, 250, y + 22, meaning, fill=INK2)
        T(s, 250, y + 42, "檢驗：" + test, fill=GRAY)
        for k, f in enumerate(figs):
            row, col_ = divmod(k, 4)
            pill(s, 640 + col_ * 52, y + 8 + 22 * row, "圖 %d" % (f + 1), WARN, h=18)
        line(s, 20, y + 54, 860, y + 54)
    bottom(s, 394, [
        ("六個原則都是 repo 該有的性質，各有一個做得到或做不到的檢驗。", True),
        ("之後談對策，每一條只回答一個問題：它讓哪一個檢驗從做不到變成做得到。", False),
    ])
    aria = ("六列原則，各附意思、檢驗與對應的問題頁：Small batches（圖 2、6、9、11）；Single Source of Truth, SSOT（圖 3、4、7、12、13、14、15）；"
            "Traceability（圖 4、5、7、15、16、17）；Continuous Integration, CI（圖 6、9、16）；Self-documenting（圖 7、8、14）；Code review（圖 9、10、11）。")
    return svg(s, 880, 480, aria)


PAGES = [
    ("總覽：depot 留得住檔案、答不出哪一版跑的；十六個問題歸成六個原則", p0()),
    ("日常：改動在個人 workspace 累積，depot 隔很久才收到一大包", p1()),
    ("散落：跑 regression 要的東西分在五個地方，depot 只是其中之一", p2()),
    ("交付：結果靠 email 貼路徑，label 記得檔案版本，記不得工具與環境", p3()),
    ("問題：「這份結果是哪一版跑的」要問好幾個人，答案仍是大概", p4()),
    ("問題：壞掉被發現時，離改壞它的那次 submit 已經很遠", p5()),
    ("問題：下游收到的包沒有清單；流程只在人腦裡，人走了就斷", p6()),
    ("問題：目錄用途沒寫在 depot，新人要人帶，AI agent 也要人另寫說明", p7()),
    ("問題：沒有開發 branch，半成品留在 workspace 或進 main，main 隨時會壞", p8()),
    ("問題：submit 就算完成，沒有任何 CL 在進 depot 前被第二個人看過", n_review()),
    ("問題：兩人改同一個檔，resolve 整份收下，另一人的改動消失", n_conflict()),
    ("問題：netlist 等產物和來源一起進 depot，改哪一份才算數沒人說得清", n_derived()),
    ("問題：第三方 IP 解壓覆蓋，晶片裡是哪一版沒人說得出", n_ip()),
    ("問題：flow script 每個專案複製一份改，修好的 bug 傳不出去", n_flow()),
    ("問題：同一份 RTL 兩台機器跑出不同結果，分不出哪個才對", n_env()),
    ("問題：regression 狀態靠人填 Excel，表和實際結果對不上", n_excel()),
    ("問題：想退回上次能跑的狀態，檔案回得去，環境回不去", n_rollback()),
    ("總結：備份做到了，「哪一版跑的、能不能重跑」一個都答不出", p_summary()),
    ("收斂：前面的問題歸成 SSOT、CI 等六個原則，對策照原則一一對應", p_principles()),
]

if __name__ == "__main__":
    build(NAME, "把版控當備份的團隊：depot 留得住檔案，答不出哪一版跑的", KICKER, PAGES)

# -*- coding: utf-8 -*-
# 《把版控當備份的團隊：depot 留住檔案，留不住答案》：docs/slides/repo-as-backup-keeps-files-not-answers.{html,pdf}
# 執行：python3 docs/figures/repo-as-backup-keeps-files-not-answers/build.py
#
# 讀者：公司內部的主管與工程師。每天用 Perforce，熟悉自己團隊的做法，沒有把這些做法和後面的問題連起來看過。
# 讀完要能：在圖裡認出自己團隊的做法，說出哪些問題是從這些做法長出來的。
# 主旨：把版控當備份的團隊，depot 裡有檔案，但結果的來源、跑法、環境與理由都在人身上；
#       問題在整合、交接與人員異動時浮現。
# 脈絡：1–3 具體怎麼運作 → 4–8 造成什麼問題 → 9 總結 → 10 收斂成五個原則（之後對策的定錨點）。
# 所有路徑、CL 號碼、label 名稱都是示意，不對應任何實際專案。
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from slides import *

NAME = "repo-as-backup-keeps-files-not-answers"
KICKER = "版控只當備份的團隊"


def check(s, x, y, ok, text, col=None, cls="tx"):
    c = col or (GOAL if ok else WARN)
    T(s, x, y, "✓" if ok else "✗", cls="tx", fill=c, w=700)
    T(s, x + 20, y, text, cls=cls, fill=INK2 if cls == "tx" else c)


# ── 圖 1：日常 ──────────────────────────────────────────────────────
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


# ── 圖 9：總結 ──────────────────────────────────────────────────────
DONE = ["檔案的最新版在哪", "誰在什麼時候改過哪個檔案", "舊版救得回來", "里程碑那天的檔案清單（label）"]
NOT = [("這個結果是哪一版做的？", "跑的人"), ("從乾淨的機器能重現嗎？", "沒人試過"), ("哪一次改動弄壞了它？", "大家一起猜"),
       ("下游收到的跟上一版差在哪？", "上游工程師"), ("跑的步驟與環境在哪裡？", "CAD 加跑的人"), ("這個檔案還有人在用嗎？", "最資深的人"),
       ("這個目錄裝什麼、靠哪些東西？", "帶你的那個人"), ("main 現在能用嗎？", "sync 了才知道")]


def p9():
    s = []
    T(s, 20, 40, "depot 做到的", cls="tx-lbl", fill=GOAL)
    for j, t in enumerate(DONE):
        check(s, 32, 72 + 27 * j, True, t)
    T(s, 20, 206, "備份要做的事，它都做到了", fill=GRAY)
    T(s, 440, 40, "depot 答不出來的", cls="tx-lbl", fill=WARN)
    T(s, 760, 40, "今天誰在回答", cls="tx-lbl", fill=GRAY)
    for j, (q, who) in enumerate(NOT):
        y = 72 + 27 * j
        check(s, 452, y, False, q)
        pill(s, 760, y - 14, who, GRAY, h=20)
    bottom(s, 300, [
        ("備份的功能它確實做到了；右邊每一題，今天都由某個人的記憶回答。", True),
        ("AI 的產出要跨團隊被採用，先得讓紀錄能回答右邊這些題。", False),
    ])
    aria = ("左欄 depot 做到的，四個打勾：檔案的最新版在哪、誰在什麼時候改過哪個檔案、舊版救得回來、里程碑那天的檔案清單。"
            "右欄 depot 答不出來的，六個打叉，各附今天誰在回答：這個結果是哪一版做的（跑的人）、從乾淨的機器能重現嗎（沒人試過）、哪一次改動弄壞了它（大家一起猜）、"
            "下游收到的跟上一版差在哪（上游工程師）、跑的步驟與環境在哪裡（CAD 加跑的人）、這個檔案還有人在用嗎（最資深的人）、這個目錄裝什麼靠哪些東西（帶你的那個人）、main 現在能用嗎（sync 了才知道）。")
    return svg(s, 880, 480, aria)

# ── 圖 10：收斂成五個原則 ─────────────────────────────────────────────
# 原則一律用英文專有名詞（2026-10-09 使用者定），中文只是註解。
ANCHORS = [
    ("Small batches", "小步常進", "改動小而頻繁地進到共用的地方，每一包說得出改了哪一件事",
     "隨便挑一包 submit，說得出它改了哪一件事", ["圖 1", "圖 5", "圖 8"]),
    ("Single Source of Truth", "SSOT　單一事實來源", "跑得起來需要的一切都在版控裡，而且只有一份",
     "換一台乾淨的機器，只靠版控的內容做出同一個結果", ["圖 2", "圖 3", "圖 6"]),
    ("Traceability", "可追溯", "每個結果與交付物都連得回產生它的版本、工具、環境與步驟",
     "隨便拿一份結果，說得出它的版本、工具、環境與步驟", ["圖 3", "圖 4", "圖 6"]),
    ("Continuous Integration", "CI　變更即驗證", "改動進來的當下就被機器檢查，共用的 main 隨時可用",
     "改壞的那一包進來時就被標出來，用不著等到整合", ["圖 5", "圖 8"]),
    ("Self-documenting", "自我描述", "目錄的用途、相依、怎麼跑，寫在 repo 裡",
     "第一次來的人或 AI agent 只讀 repo，就說得出每個目錄的用途與相依", ["圖 6", "圖 7"]),
]


def p10():
    s = []
    T(s, 20, 34, "原則", cls="tx-lbl", fill=GOAL)
    T(s, 260, 34, "意思，以及做得到／做不到的檢驗", cls="tx-lbl", fill=INK2)
    T(s, 712, 34, "沒做到時的問題", cls="tx-lbl", fill=WARN)
    for i, (en, zh, meaning, test, figs) in enumerate(ANCHORS):
        y = 48 + 62 * i
        rect(s, 20, y + 8, 3, 40, col=GOAL, fill=GOAL, sw=0)
        T(s, 34, y + 26, en, cls="tx", fill=GOAL, w=700)
        T(s, 34, y + 45, zh, fill=GRAY)
        T(s, 260, y + 24, meaning, fill=INK2)
        T(s, 260, y + 44, "檢驗：" + test, fill=GRAY)
        x = 712
        for f in figs:
            x += pill(s, x, y + 18, f, WARN, h=20) + 6
        line(s, 20, y + 58, 860, y + 58)
    bottom(s, 374, [
        ("五個原則都是 repo 該有的性質，各有一個做得到或做不到的檢驗。", True),
        ("之後談對策，每一條只回答一個問題：它讓哪一個檢驗從做不到變成做得到。", False),
    ])
    aria = ("五列原則，各附意思、檢驗與對應的問題頁：Small batches（圖 1、5、8）；Single Source of Truth, SSOT（圖 2、3、6）；Traceability（圖 3、4、6）；"
            "Continuous Integration, CI（圖 5、8）；Self-documenting（圖 6、7）。")
    return svg(s, 880, 480, aria)


PAGES = [
    ("日常：改動在個人 workspace 累積，depot 隔很久才收到一大包", p1()),
    ("散落：跑得起來需要的東西分在五個地方，depot 只是其中之一", p2()),
    ("交付：結果靠 email 裡的路徑傳遞，label 只記得檔案", p3()),
    ("問題：「這份結果是哪一版跑的」要問好幾個人，答案仍是大概", p4()),
    ("問題：壞掉被發現時，離改壞它的那次 submit 已經很遠", p5()),
    ("問題：下游說不出收到了什麼，人走了流程跟著走", p6()),
    ("問題：目錄的用途靠人帶路，AI agent 每個 workspace 都要另寫指引", p7()),
    ("問題：沒有 branch，半成品留在 workspace 或進 main，main 隨時會壞", p8()),
    ("總結：備份做到了，關於檔案的問題一個都答不出", p9()),
    ("收斂：八個問題歸到五個原則，之後的對策各自對應其中一個", p10()),
]

if __name__ == "__main__":
    build(NAME, "把版控當備份的團隊：depot 留住檔案，留不住答案", KICKER, PAGES)

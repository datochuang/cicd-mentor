# -*- coding: utf-8 -*-
# 《第一次進 workspace：照五個原則檢查，不過就先補一版》：docs/slides/agent-entering-unknown-workspace.{html,pdf}
# 執行：python3 docs/figures/agent-entering-unknown-workspace/build.py
#
# 讀者：第一次進到一個沒看過的 workspace 的人或 AI agent。懂 Perforce 基本操作、會寫 script，不認識這個專案。
# 讀完要能：照順序把 workspace 檢查一遍；每個檢查點知道怎麼判定、不過時自己先補什麼、哪些才需要問 owner。
# 主旨：檢查有沒有 CI/CD，就是逐一驗證五個原則（D4）的檢驗；多數缺口靠通用常識就能先補一版 patch，
#       owner 只要決定採不採用。
# 脈絡：1 流程與前置 → 2–8 六個檢查（各對應一個原則：怎麼查／判定／先補什麼／只需要問 owner 的；SSOT 兩頁）→ 9 分工與 patch 怎麼交。
# 2026-10-09：SSOT 多一頁談產物、flow、IP；原本的 Code review 一頁改成「review 規矩：目錄有沒有講好要不要 review」（D7：Code review 不是原則，是規矩，歸 Self-documenting）。
# 指令（p4 changes、p4 describe、p4 triggers 等）為示意，未經實機驗證，以站上的 p4 help 為準。
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from slides import *

NAME = "agent-entering-unknown-workspace"
KICKER = "進到陌生 workspace 的檢查"


def mark(s, x, y, ok, text, fill=None):
    c = GOAL if ok else WARN
    T(s, x, y, "✓" if ok else "✗", cls="tx", fill=c, w=700)
    T(s, x + 18, y, text, fill=fill or INK2)


# ── 圖 1：流程 ──────────────────────────────────────────────────────
CHECKS = [("Self-documenting", "看得懂嗎", "圖 2"), ("SSOT（環境／複本）", "跑得起來嗎；只有一份嗎", "圖 3–4"), ("Traceability", "連得回來源嗎", "圖 5"),
          ("Continuous Integration", "每次變更有機器檢查嗎", "圖 6"), ("Review 規矩", "目錄講好要不要 review 了嗎", "圖 7"), ("Small batches", "一包一件事嗎", "圖 8")]


def p1():
    s = []
    T(s, 20, 20, "這份文件回答：人或 AI agent 進到一個沒看過的 workspace，怎麼檢查它有沒有 CI/CD；不過時自己先補什麼 ↓", cls="tx-lbl", fill=INK2)
    # 進去之前
    rect(s, 20, 44, 200, 150, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
    T(s, 34, 68, "進去之前", cls="tx", fill=INK2, w=700)
    for j, t in enumerate(["開專用、乾淨的 workspace", "只 sync，不碰別人的目錄", "看到的狀態先記成基線", "指令以站上 p4 help 為準"]):
        T(s, 34, 96 + 22 * j, "· " + t, fill=INK2)
    arrow(s, 224, 120, 254, 120, col=INK2, ar="ar", sw=1.4)
    # 五個檢查
    T(s, 260, 36, "六個檢查，照這個順序", cls="tx-lbl", fill=GOAL)
    for i, (name, q, fig) in enumerate(CHECKS):
        y = 44 + 46 * i
        rect(s, 260, y, 270, 38, col=GOAL, fill=GOAL, op=".08", sw=1.4)
        T(s, 272, y + 16, "%d  %s" % (i + 1, name), cls="tx", fill=GOAL, w=700)
        T(s, 272, y + 31, q, fill=INK2)
        pill(s, 530 - 12, y + 9, fig, WARN, h=20, anchor="end")
        if i < 5:
            arrow(s, 395, y + 40, 395, y + 44, col=GOAL, ar="ar-g", sw=1.2)
    T(s, 260, 336, "圖 6 的 check 直接用圖 3 的 script", fill=GRAY)
    T(s, 260, 352, "圖 6 的結果附上圖 5 的 manifest", fill=GRAY)
    # 每個檢查的循環
    T(s, 580, 36, "每個檢查都走一遍", cls="tx-lbl", fill=INK2)
    steps = [("查", INK2, "plain"), ("判定", INK2, "plain"), ("不過：先補一版 patch", GOAL, "dash"),
             ("交 owner：採用或修正", PM, "solid"), ("結果記進地圖", INK2, "plain")]
    for i, (t, col, kind) in enumerate(steps):
        y = 44 + 52 * i
        if kind == "dash":
            rect(s, 580, y, 280, 36, col=col, fill=col, op=".06", sw=1.4, dash="6 4")
        elif kind == "solid":
            rect(s, 580, y, 280, 36, col=col, fill=col, op=".10", sw=1.4)
        else:
            rect(s, 580, y, 280, 36, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
        T(s, 594, y + 23, t, cls="tx", fill=col, w=700)
        if i < 4:
            arrow(s, 720, y + 40, 720, y + 48, col=INK2, ar="ar", sw=1.2)
    T(s, 740, 115, "過：記錄，下一個", anchor="start", fill=GRAY)
    bottom(s, 376, [
        ("六個檢查對應五個原則的檢驗（review 規矩歸 Self-documenting）；不過的時候，多數缺口靠通用常識就能先補一版。", True),
        ("owner 拿到的是可以直接採用的 patch，只有少數幾件事需要他回答。", False),
    ])
    aria = ("左邊是進去之前要做的事：開專用乾淨的 workspace、只 sync 不碰別人的目錄、先記基線、指令以站上 p4 help 為準。"
            "中間是六個檢查的順序：Self-documenting 看得懂嗎（圖 2）、SSOT 跑得起來嗎只有一份嗎（圖 3、4）、Traceability 連得回來源嗎（圖 5）、"
            "Continuous Integration 每次變更有機器檢查嗎（圖 6）、review 規矩：目錄講好要不要 review 了嗎（圖 7）、Small batches 一包一件事嗎（圖 8）。"
            "右邊是每個檢查都走一遍的循環：查、判定、不過就先補一版 patch、交 owner 採用或修正、結果記進地圖。")
    return svg(s, 880, 480, aria)


# ── 圖 2–6：檢查頁的共用版型 ─────────────────────────────────────────
def check_page(principle, test, how, ok, bad, patches, ask, lines, aria):
    s = []
    w = pill(s, 20, 14, principle, GOAL, h=24)
    T(s, 20 + w + 12, 31, "檢驗：" + test, cls="tx", fill=INK2)
    T(s, 20, 70, "怎麼查", cls="tx-lbl", fill=INK2)
    for j, t in enumerate(how):
        T(s, 20, 94 + 22 * j, "· " + t, fill=INK2)
    T(s, 300, 70, "判定", cls="tx-lbl", fill=INK2)
    y = 94
    for t in ok:
        mark(s, 300, y, True, t)
        y += 22
    y += 10
    T(s, 300, y, "不過的徵兆", fill=WARN)
    y += 22
    for t in bad:
        mark(s, 300, y, False, t)
        y += 22
    T(s, 560, 70, "不過時，先補這些（自己做）", cls="tx-lbl", fill=GOAL)
    bh = 16 + 40 * len(patches)
    rect(s, 560, 80, 300, bh, col=GOAL, fill=GOAL, op=".06", sw=1.4, dash="6 4")
    for j, (name, desc) in enumerate(patches):
        yy = 80 + 10 + 40 * j
        T(s, 574, yy + 14, name, cls="tx", fill=GOAL, w=700)
        T(s, 574, yy + 31, desc, fill=INK2)
    ya = 80 + bh + 26
    T(s, 560, ya, "只需要問 owner", cls="tx-lbl", fill=WARN)
    for j, t in enumerate(ask):
        T(s, 560, ya + 22 + 20 * j, "? " + t, fill=WARN)
    bottom(s, 356, lines)
    return svg(s, 880, 480, aria)


def p2():
    return check_page(
        "Self-documenting", "第一次來的人或 AI agent 只讀 repo，就說得出每個目錄的用途與相依",
        ["列頂層目錄，找 README、說明檔", "找 filelist 與 run script", "對照：哪些檔案沒被任何 filelist 引用", "看最近的 CL：哪些目錄還有人在動"],
        ["每個頂層目錄說得出用途", "誰引用誰畫得出來", "怎麼跑有一份寫下來的"],
        ["rtl_old/ 與 rtl_new2/ 並存", "README 寫的是上一個專案", "沒有任何檔案說怎麼跑"],
        [("PROJECT_MAP.md 初稿", "每個目錄一行用途，標依據：擷取／推測／猜的"),
         ("相依圖", "從 filelist 擷取誰引用誰"),
         ("疑似未使用清單", "沒被引用也沒人動的目錄，只標不刪")],
        ["標「猜的」那幾行對不對", "疑似未使用的目錄能不能標為棄用"],
        [("看懂的依據要分開標：擷取的、推測的、猜的，owner 只需要看猜的那幾行。", True),
         ("沒被引用的目錄先標、不刪；刪不刪是 owner 的事。", False)],
        "Self-documenting 的檢查：怎麼查（列頂層目錄與 README、找 filelist 與 run script、對照哪些檔案沒被引用、看最近的 CL）；"
        "判定（每個目錄說得出用途、誰引用誰畫得出來、怎麼跑有寫下來；不過的徵兆：rtl_old 與 rtl_new2 並存、README 過期、沒有檔案說怎麼跑）；"
        "先補：PROJECT_MAP.md 初稿標依據、從 filelist 擷取的相依圖、疑似未使用清單只標不刪；只需要問 owner：猜的那幾行對不對、疑似未使用的目錄能不能標為棄用。")


def p3():
    return check_page(
        "Single Source of Truth (SSOT)", "換一台乾淨的機器，只靠版控的內容做出同一個結果",
        ["專用 workspace 只 sync，不帶本機設定", "照 repo 裡寫的方式編 top、跑一個最小的 sim", "每個失敗分類：缺檔／缺工具／缺環境／缺 script", "跟 owner 手上的結果比對"],
        ["編得過、跑得完", "結果和 owner 手上的一致"],
        ["filelist 引用不存在的檔", "script 在 /home 或 /proj 底下", "工具版本只在 .cshrc 裡", "同一份 RTL，兩台機器結果不同"],
        [("setup.sh", "工具版本、環境變數寫死在裡面，進 depot"),
         ("run_sanity.sh", "從乾淨 workspace 編 top＋跑一個 sim"),
         ("缺檔清單", "哪個 filelist 第幾行引用、誰最後動過"),
         (".p4ignore 提案", "進了 depot 的產生檔列出來")],
        ["缺的檔在誰的 workspace", "產生檔要不要移出版控"],
        [("跑不起來的每一個原因，都是一件散在 depot 外面的東西；補法是把它寫成 script 進 depot。", True),
         ("只有「缺的檔在誰那裡」這件事非問 owner 不可。", False)],
        "SSOT 的檢查：怎麼查（專用 workspace 只 sync、照 repo 寫的方式編 top 跑最小 sim、每個失敗分類、跟 owner 的結果比對）；"
        "判定（編得過跑得完、結果一致；不過的徵兆：filelist 引用不存在的檔、script 在 home 或 proj 底下、工具版本只在 .cshrc）；"
        "先補：setup.sh、run_sanity.sh、缺檔清單、.p4ignore 提案；只需要問 owner：缺的檔在誰的 workspace、產生檔要不要移出版控。")


def p3b():
    return check_page(
        "Single Source of Truth (SSOT)", "換一台乾淨的機器，只靠版控的內容做出同一個結果；產物、flow、IP 也算在內",
        ["找進了 depot 的產物：netlist、lib、sim 結果", "比對產物和來源：產物比來源新，就是直接改過", "找 flow 的複本：各專案的 scripts/ 差在哪", "找第三方 IP：怎麼進來的，有沒有 drop 的紀錄"],
        ["產物都能從來源重新產生", "flow 只有一份，差異是參數", "每次 IP drop 都查得到版本與差異"],
        ["ECO 改在 netlist 上", "三個專案三份 flow", "ip/ 是解壓覆蓋的，沒有紀錄"],
        [("產物清單＋重新產生的 script", "列出哪些是產物、由哪個來源產生"),
         ("flow 收成一份", "三份的差異做成參數，各專案指向同一份"),
         ("IP drop 流程", "每次 drop 一個 CL：tarball 指紋、版本、差異"),
         ("本地 patch 分開放", "對 IP 的修改獨立成 patch，drop 之後重套")],
        ["產物能不能從 depot 移出", "flow 的正本由誰維護", "IP 的本地修改要不要回報 vendor"],
        [("產物、flow、IP 最常變成第二份真相；補法都一樣：留一份來源，其他的由它產生。", True),
         ("移出產物、收攏 flow 會動到別人的工作方式，要 owner 決定。", False)],
        "SSOT 的第二頁，看產物、flow、第三方 IP：怎麼查（找進了 depot 的產物、比對產物和來源的新舊、找各專案 flow script 的複本、找 IP 怎麼進來的）；"
        "判定（產物都能從來源重新產生、flow 只有一份差異是參數、每次 IP drop 都查得到版本與差異；不過的徵兆：ECO 改在 netlist 上、三個專案三份 flow、ip 是解壓覆蓋的）；"
        "先補：產物清單加重新產生的 script、flow 收成一份、IP drop 流程、本地 patch 分開放；只需要問 owner：產物能不能移出、flow 的正本由誰維護、IP 的本地修改要不要回報 vendor。")


def p4():
    return check_page(
        "Traceability", "隨便拿一份結果，說得出它的版本、工具、環境與步驟",
        ["拿最近的 label、release 包、regression 報告", "問四件事：CL、工具版本、環境、怎麼跑", "用內容指紋比對 release 包和 label 的檔案", "試著退回上一個能跑的狀態"],
        ["四件事都從紀錄答得出，用不著問人", "release 包和 label 對得上"],
        ["label 只有檔案清單", "報告是一個會變的路徑", "release 包手動打，README 靠回想", "退回 label，環境和產物回不去"],
        [("make_manifest.sh", "寫出 CL、label、工具版本、環境、指令、結果摘要"),
         ("manifest 跟著結果走", "放進 run 目錄與 release 包，一起進 depot"),
         ("舊交付物反查", "指紋對得上就補 manifest，對不上標「無法追溯」"),
         ("known-good 點", "check 通過就打 label＋manifest，要回去有地方回")],
        ["交付物的正式清單：給誰、含什麼"],
        [("manifest 是結果和來源之間缺的那條線；讓產生結果的 script 順手寫出來，就不用靠人記。", True),
         ("過去的交付物追不回來的，標成基線，從現在開始追。", False)],
        "Traceability 的檢查：怎麼查（拿最近的 label、release 包、regression 報告，問哪個 CL、哪些工具版本、什麼環境、怎麼跑，用指紋比對 release 包和 label）；"
        "判定（四件事都從紀錄答得出、release 包和 label 對得上；不過的徵兆：label 只有檔案清單、報告是會變的路徑、release 包手動打）；"
        "先補：make_manifest.sh、manifest 跟著結果走、舊交付物反查、known-good 點；只需要問 owner：交付物的正式清單。")


def p5():
    return check_page(
        "Continuous Integration (CI)", "改壞的那一包進來時就被標出來，用不著等到整合",
        ["找 submit 觸發的檢查：p4 triggers、CI job", "找定期 regression：結果放哪、誰看得到", "翻最近一次壞掉：多久後、被誰發現"],
        ["每個 submit 都有機器跑過最小檢查", "結果公開看得到，附 CL 號"],
        ["只有人手動跑", "有 nightly，結果只在跑的人信箱", "壞掉由下游先發現", "狀態表靠人填 Excel"],
        [("最小 check", "拿圖 3 的 run_sanity.sh：編得過＋一個 sim"),
         ("排上去跑", "先定時跑，再進到每個 CL 都跑"),
         ("結果可見", "寫到 repo 看得到的地方，附 CL 號與 manifest"),
         ("狀態表由結果產生", "從 manifest 與 log 產生，不用人填")],
        ["觸發要裝在哪、誰有權限", "算力與 license 的配額", "壞了通知誰"],
        [("最小的 check 就是圖 3 那個 script；先讓它定時跑、結果看得到，再談每個 CL 都跑。", True),
         ("裝觸發、配算力、通知誰，要 owner 點頭。", False)],
        "Continuous Integration 的檢查：怎麼查（找 submit 觸發的檢查、找定期 regression 與結果、翻最近一次壞掉多久後被誰發現）；"
        "判定（每個 submit 都有機器跑過最小檢查、結果公開附 CL 號；不過的徵兆：只有人手動跑、nightly 結果只在信箱、壞掉由下游先發現）；"
        "先補：最小 check 用圖 3 的 run_sanity.sh、先定時跑再每個 CL 跑、結果寫到看得到的地方附 CL 號與 manifest；只需要問 owner：觸發裝在哪誰有權限、算力與 license 配額、壞了通知誰。")


def p_review():
    return check_page(
        "Review 規矩（每個目錄講好要不要 review）", "隨便挑一個目錄，說得出它要不要 review、誰看；說要的目錄，隨便挑一包說得出誰看過",
        ["目錄有沒有寫要不要 review：PROJECT_MAP", "找 reviewer 的紀錄：Swarm、reviewed-by", "找兩人改同檔的 resolve：誰看過差異"],
        ["每個目錄講好了：要／不要、誰看、什麼時候", "說要的目錄，每一包併入前有人看過並留紀錄"],
        ["沒有任何目錄講過要不要 review", "submit 就算完成", "resolve 直接 accept 整份"],
        [("review 規矩初稿", "每目錄：要／不要、誰看、何時；寫進 PROJECT_MAP"),
         ("最輕的流程", "說要的：shelve → 指定 reviewer → 看過才 submit"),
         ("resolve 清單", "最近整份 accept 的 resolve，列給當事人看")],
        ["每個目錄要不要 review、誰看", "要不要擋 submit（trigger）"],
        [("要不要 review 由各目錄自己定、可以改，但要講好、寫下來；沒講好等於沒人看。", True),
         ("agent 交的 shelved CL 一律 owner 收了才進 depot，這條不由目錄定。", False)],
        "review 規矩的檢查：怎麼查（每個目錄有沒有寫要不要 review、找 reviewer 的紀錄、找兩人改同檔的 resolve 誰看過差異）；"
        "判定（每個目錄講好要不要、誰看、什麼時候；說要的目錄每一包併入前有人看過並留紀錄；不過的徵兆：沒有任何目錄講過、submit 就算完成、resolve 直接 accept 整份）；"
        "先補：review 規矩初稿、最輕的流程、resolve 清單；只需要問 owner：每個目錄要不要 review 誰看、要不要擋 submit。")


def p6():
    return check_page(
        "Small batches", "隨便挑一包 submit，說得出它改了哪一件事",
        ["p4 changes 看最近的 submit：幾個檔案、說明", "挑幾包用 p4 describe 看：一包裡幾件事", "看兩包之間隔多久"],
        ["一包一件事", "說明看得懂改了什麼、為什麼"],
        ["說明是 update、fix、sync", "一包混 RTL、tb、script", "一包是某人一整段期間的工作"],
        [("CL 說明模板", "改了什麼／為什麼／怎麼驗"),
         ("pre-submit 清單", "跑過 sanity check、filelist 更新、一包一件事"),
         ("拆包示範", "拿一包進行中的工作，用 shelved CL 拆成幾包")],
        ["團隊願不願意用模板", "進行中的大包怎麼拆，當事人決定"],
        [("submit 的歷史改不了，能補的是下一包的寫法：模板、清單、一個拆開的示範。", True),
         ("大包怎麼拆，只有當事人知道哪些改動是一起的。", False)],
        "Small batches 的檢查：怎麼查（p4 changes 看最近的 submit 幾個檔案與說明、p4 describe 看一包裡幾件事、看兩包之間隔多久）；"
        "判定（一包一件事、說明看得懂；不過的徵兆：說明是 update fix sync、一包混 RTL tb script、一包是某人一整段期間的工作）；"
        "先補：CL 說明模板、pre-submit 清單、拆包示範；只需要問 owner：團隊願不願意用模板、進行中的大包怎麼拆。")


# ── 圖 7：分工與 patch 怎麼交 ────────────────────────────────────────
TIERS = [
    ("自己補，直接交 patch", GOAL, "solid", ["PROJECT_MAP 初稿、目錄負責人表初稿", "setup.sh、run_sanity.sh", "make_manifest.sh、known-good 點", "最小 check 與排程、狀態表產生", "CL 說明模板、pre-submit 清單", "review 流程提案、resolve 清單"]),
    ("補了，但要 owner 決定", GOAL, "dash", ["產物移出版控、flow 收成一份", "目錄標為棄用", "觸發裝不裝、review 擋不擋 submit", "壞了通知誰", "拆包的示範採不採用", "IP 的本地修改要不要回報 vendor"]),
    ("只有 owner 知道，要問", WARN, "dash", ["缺的檔在誰那裡", "猜的用途對不對、每個目錄誰負責", "交付物給誰、含什麼", "進行中的大包怎麼拆", "flow 的正本由誰維護"]),
]
HANDOFF = [("每個 patch 一個 shelved CL", ["或 MR"]), ("說明寫四件事", ["查了什麼、發現什麼", "讓哪個檢驗做得到、哪些是猜的"]),
           ("owner 採用＝submit", ["不採用＝回一句為什麼"]), ("結果記進 PROJECT_MAP", ["採用了什麼、為什麼不採用"])]


def p7():
    s = []
    for i, (title, col, kind, items) in enumerate(TIERS):
        x = 20 + i * 284
        if kind == "solid":
            rect(s, x, 20, 272, 184, col=col, fill=col, op=".10", sw=1.6)
        else:
            rect(s, x, 20, 272, 184, col=col, fill=col, op=".05", sw=1.4, dash="6 4")
        T(s, x + 14, 44, title, cls="tx", fill=col, w=700)
        for j, t in enumerate(items):
            T(s, x + 14, 70 + 22 * j, "· " + t, fill=INK2)
    T(s, 20, 236, "patch 怎麼交", cls="tx-lbl", fill=INK2)
    for i, (t, sub) in enumerate(HANDOFF):
        x = 20 + i * 214
        rect(s, x, 246, 196, 70, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
        T(s, x + 12, 268, t, cls="tx", fill=INK2, w=700)
        for k, line_ in enumerate(sub):
            T(s, x + 12, 287 + 16 * k, line_, fill=GRAY)
        if i < 3:
            arrow(s, x + 199, 281, x + 211, 281, col=INK2, ar="ar", sw=1.4)
    T(s, 20, 346, "從頭到尾守住的", cls="tx-lbl", fill=WARN)
    x = 20
    for t in ["不碰別人的 workspace", "不刪任何東西", "owner 採用才進 depot", "猜的一律標出來"]:
        x += pill(s, x, 356, t, WARN) + 8
    bottom(s, 394, [
        ("多數缺口靠通用常識就補得出第一版；owner 的工作從回答問題變成採用或修正 patch。", True),
        ("三類事只有 owner 知道；問的時候附上你已經查到的部分。", False),
    ])
    aria = ("三欄分工：自己補直接交 patch（PROJECT_MAP 與目錄負責人表初稿、setup.sh 與 run_sanity.sh、make_manifest.sh 與 known-good 點、最小 check 與排程與狀態表產生、CL 說明模板與 pre-submit 清單、review 流程提案與 resolve 清單）；"
            "補了但要 owner 決定（產物移出版控與 flow 收成一份、目錄標為棄用、觸發裝不裝與 review 擋不擋 submit、壞了通知誰、拆包示範採不採用、IP 本地修改要不要回報 vendor）；"
            "只有 owner 知道要問（缺的檔在誰那裡、猜的用途對不對與每個目錄誰負責、交付物給誰含什麼、進行中的大包怎麼拆、flow 的正本由誰維護）。"
            "下方是 patch 怎麼交的四步：每個 patch 一個 shelved CL、說明寫四件事、owner 採用等於 submit 不採用回一句為什麼、結果記進 PROJECT_MAP。"
            "最後是從頭到尾守住的四條：不碰別人的 workspace、不刪任何東西、owner 採用才進 depot、猜的一律標出來。")
    return svg(s, 880, 480, aria)


PAGES = [
    ("流程：六個檢查對五個原則，不過就做 patch，由專案 owner 決定收不收", p1()),
    ("Self-documenting：光看 depot 說不出每個目錄做什麼，就先補一份目錄說明", p2()),
    ("SSOT（環境）：乾淨的 workspace 跑不起來，缺的先補成 script 進 depot", p3()),
    ("SSOT（複本）：產物、複製的 flow、解壓的 IP 各只留一份來源，其餘改成產生", p3b()),
    ("Traceability：結果說不出哪個 CL 跑的，就附一份 manifest 記來源", p4()),
    ("CI：submit 後沒有機器檢查，就先掛一個 sanity check 跟著 submit 跑", p5()),
    ("Review 規矩：目錄沒講好要不要 review，先補一份規矩初稿給 owner 定", p_review()),
    ("Small batches：過去的大 CL 改不了，先給 CL 說明模板和拆小 CL 的示範", p6()),
    ("分工：agent 能補的直接送 patch，只有 owner 才知道的事才開口問", p7()),
]

if __name__ == "__main__":
    build(NAME, "進到陌生的 workspace：人或 agent 照五個原則檢查，不過就先做 patch", KICKER, PAGES)

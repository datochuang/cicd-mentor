# -*- coding: utf-8 -*-
# 《CI/CD 在公司的機器上怎麼跑》：docs/slides/how-ci-cd-runs-on-company-machines.{html,pdf}
# 執行：python3 docs/figures/how-ci-cd-runs-on-company-machines/build.py
#
# 讀者：PM 與團隊工程師（每天用 Perforce，沒用過 Jenkins）；也給內網的 Claude Code 當它對團隊解釋時的圖。
# 讀完要能：說出 CI 在機器上是哪三件事、CD 多哪兩步；定時查和 trigger 差在哪、四種 trigger 事件各做什麼；
#           Jenkins 的六個概念；人、CAD、agent 各做哪一段；git 對應到哪些東西；三個坑。
# 主旨：CI/CD 的每一步都是 depot 裡的 script；Jenkins 或 cron 只是按時按它，trigger 在 submit 前後接上；
#       agent 寫 script 與 job 定義、用 API 讀結果，不登進 server；人只做兩件事（給帳號、產 token）。
# 來源：2026-10-10 使用者問「要做 CD 大部分需要 Jenkins，agent 怎麼做」「CI 具體的執行方式」；文字版在
#       starter-kit/11-research/jenkins-primer.md、ci-primer.md。指令、trigger 行、Jenkinsfile 皆示意。
# 脈絡：1 總覽（一次 submit 之後機器做的事＋分工）→ 2 CI 三件事與兩種時機 → 3 察覺的兩種方法 → 4 trigger 四種事件
#       → 5 三個等級一支 script → 6 Jenkins 六個概念 → 7 CD 多兩個 stage → 8 分工 → 9 git 的對應 → 10 三個坑
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from slides import *

NAME = "how-ci-cd-runs-on-company-machines"
KICKER = "CI/CD 的機制"
CAD = INK2


def lines_in_box(s, x, y, w, h, title, items, col=INK2, kind="plain", gap=16):
    box(s, x, y, w, h, title, col=col, kind=kind)
    for k, t in enumerate(items):
        T(s, x + 14, y + 42 + gap * k, t, fill=INK2)


# ── 圖 1：總覽 ──────────────────────────────────────────────────────
def p1():
    s = []
    T(s, 20, 20, "這份文件回答：有人 submit 之後，機器做了哪些事；Jenkins 和 trigger 是什麼；AI agent（啟動包要做的那個程式）、CAD、PM 各做哪一段", cls="tx-lbl", fill=INK2)
    # 流程列
    box(s, 20, 44, 112, 60, "工程師 submit", sub="一包改動進 depot", col=INK2)
    arrow(s, 132, 74, 150, 74, col=GOAL, ar="ar-g")
    box(s, 150, 44, 122, 60, "察覺", sub="定時查，或 trigger", col=GOAL, kind="dash")
    arrow(s, 272, 74, 290, 74, col=GOAL, ar="ar-g")
    rect(s, 290, 36, 570, 108, col=GOAL, fill=GOAL, op=".06", sw=1.4)
    T(s, 302, 56, "Jenkins 的節點（或農場節點的 cron）：在乾淨 workspace 依序呼叫 depot 的 script", cls="tx", fill=GOAL, w=700)
    x = 302
    stages = ["sync 乾淨", "run_sanity", "make_manifest", "make_release", "放取用處", "通知下游"]
    xs = []
    for t in stages:
        w = pill(s, x, 78, t, GOAL, h=22)
        xs.append((x, w)); x += w + 8
    for (xa, wa), (xb, wb) in zip(xs, xs[1:]):
        arrow(s, xa + wa, 89, xb, 89, col=GOAL, ar="ar-g", sw=1.2)
    ci_x0, ci_x1 = xs[0][0], xs[2][0] + xs[2][1]
    cd_x0, cd_x1 = xs[3][0], xs[5][0] + xs[5][1]
    line(s, ci_x0, 112, ci_x1, 112, col=GOAL, sw=1.6); T(s, (ci_x0 + ci_x1) / 2, 128, "CI：查與判，結果寫下來", anchor="middle", fill=GOAL)
    line(s, cd_x0, 112, cd_x1, 112, col=GOAL, sw=1.6); T(s, (cd_x0 + cd_x1) / 2, 128, "CD：綠了就打包交下游", anchor="middle", fill=GOAL)
    T(s, 20, 162, "每一步都是 depot 裡的 script；Jenkins 或 cron 只是按時按它。agent 交 shelved CL 之前自己跑過一次，那就是這條 pipeline 的第一次執行。", fill=INK2)
    # 分工三框
    lines_in_box(s, 20, 178, 290, 124, "AI agent 做的（從自己的機器，用 API）", [
        "寫 run_sanity、make_manifest、make_release",
        "寫 Jenkinsfile 與 trigger，交 shelved CL",
        "用 API 建 job、按一次 build、讀 log 與結果",
        "不登進任何 server，不裝 trigger",
    ], col=AGENT, kind="solid")
    lines_in_box(s, 318, 178, 260, 124, "CAD 做的（各一次）", [
        "給 agent 一個限定資料夾的 Jenkins 帳號",
        "告訴 agent 哪個節點有 p4 與 bsub",
        "裝 trigger（super 才能）",
        "不給帳號時：agent 寫好、CAD 貼上建 job",
    ], col=CAD, kind="plain")
    lines_in_box(s, 586, 178, 274, 124, "PM 做的", [
        "去談帳號、節點、權限（09 #25）",
        "用 agent 的帳號登入一次，產 API token 給它",
        "擋 submit 之前：核准 bypass 與總開關",
        "看 build 頁與一頁摘要，不用看 Jenkins 設定",
    ], col=PM, kind="solid")
    bottom(s, 318, [
        ("每個 check 都是 depot 裡的 script；Jenkins 或 cron 只是定時去跑它；p4 trigger 在 submit 前後把它接上。", True),
        ("AI agent 寫 script 與 job 定義、用 API 看結果，不登進 server；人只做兩件事：開帳號、給 token。", False),
        ("後面：分工、CI 三件事、察覺的兩條路、Jenkins 六個概念、trigger 四種事件、check 三級、CD 接著做的三件事、git 的對應、三個坑。", False),
    ])
    aria = ("上排流程：工程師 submit → 察覺（定時查或 trigger）→ Jenkins 節點依序呼叫 depot 裡的 script：sync 乾淨、run_sanity、make_manifest（CI），make_release、放取用處、通知下游（CD）。"
            "下排三框：agent 做的（寫 script 與 Jenkinsfile、用 API 建 job 讀結果、不登進 server）、CAD 做的（給帳號、說節點、裝 trigger）、PM 做的（談權限、產 token、核准 bypass 與總開關）。")
    return svg(s, 880, 480, aria)


# ── 圖 2：CI 三件事與兩種時機 ────────────────────────────────────────
def p2():
    s = []
    T(s, 20, 24, "CI 在機器上是三件事", cls="tx-lbl", fill=GOAL)
    items = [("1 察覺改動", "有人 submit 了，機器要知道", "定時查 p4 changes，或 trigger"),
             ("2 乾淨環境跑 check", "sync 一個乾淨的 workspace，照說明跑", "run_sanity.sh → make_manifest.sh"),
             ("3 結果寫下來", "build 頁、取用處的 manifest、slack", "附 CL 號，誰都看得到")]
    for k, (t, a, b) in enumerate(items):
        y = 36 + k * 76
        box(s, 20, y, 300, 64, t, sub=a, sub2=b, col=GOAL, kind="solid")
        if k < 2: arrow(s, 170, y + 64, 170, y + 76, col=GOAL, ar="ar-g", sw=1.2)
    box(s, 20, 266, 300, 44, "可選的第四件：擋", sub="check 沒綠，改動進不了共用的 main", col=WARN, kind="dash")
    # 兩種時機
    T(s, 360, 24, "兩種時機", cls="tx-lbl", fill=INK2)
    T(s, 360, 48, "submit 後跑：只報告級、警告級", cls="tx", fill=GOAL, w=700)
    x = 360
    items2 = [("submit", INK2), ("進 depot", INK2), ("幾分鐘後 check 跑", GOAL), ("壞了，但知道是哪一包", GOAL)]
    for k, (t, col) in enumerate(items2):
        if k: arrow(s, x - 8, 69, x, 69, col=GOAL, ar="ar-g", sw=1.2)
        w = pill(s, x, 58, t, col, h=22); x += w + 8
    T(s, 360, 100, "main 可能已經壞了；誰弄壞的當天就知道，不用等整合", fill=INK2)
    T(s, 360, 140, "submit 前跑：擋", cls="tx", fill=WARN, w=700)
    x = 360
    items3 = [("submit", INK2), ("trigger 跑 check", GOAL), ("綠：進 depot", GOAL), ("紅：退回給本人", WARN)]
    for k, (t, col) in enumerate(items3):
        if k: arrow(s, x - 8, 161, x, 161, col=GOAL, ar="ar-g", sw=1.2)
        w = pill(s, x, 150, t, col, h=22); x += w + 8
    T(s, 360, 192, "共用的 main 隨時可用；代價是使用者按 submit 要等，check 必須快", fill=INK2)
    rect(s, 360, 212, 500, 98, col=INK2, fill="var(--surface-2)", sw=1.1)
    T(s, 372, 232, "check 分三級（啟動包叫上線分級）：從後者走到前者", cls="tx", fill=INK2, w=700)
    T(s, 372, 252, "只報告：submit 後跑，結果只寫下來，不吵人", fill=INK2)
    T(s, 372, 268, "警告：submit 後跑，私訊本人；誤報率低了才升", fill=INK2)
    T(s, 372, 284, "擋：submit 前跑；PM 與 owner 同意、有 bypass、有總開關才裝", fill=INK2)
    T(s, 372, 300, "第 6 步只報告，第 9 步才擋（07-build-brief）", fill=GRAY)
    bottom(s, 326, [
        ("CI＝察覺改動、乾淨環境跑 check、結果寫下來；這三件事 submit 後跑就有價值，submit 前跑才擋得住。", True),
        ("Jenkins 把這一串步驟叫 pipeline；它的前半段就是 CI，後半段才是 CD（第 8 頁）。", False),
    ])
    aria = ("左邊三個方塊：察覺改動、乾淨環境跑 check、結果寫下來，下方虛線框是可選的擋。右邊兩條時間線：submit 後跑（進 depot、幾分鐘後 check 跑、壞了但知道是哪一包）與 submit 前跑（trigger 跑 check，綠才進 depot、紅退回）；"
            "底下說明上線分級就是從後者走到前者：只報告、警告、擋。")
    return svg(s, 880, 480, aria)


# ── 圖 3：察覺的兩種方法 ─────────────────────────────────────────────
def p3():
    s = []
    # 左：定時查
    rect(s, 20, 30, 405, 300, col=GOAL, fill=GOAL, op=".04", sw=1.4)
    T(s, 32, 50, "定時查（polling）：agent 自己能裝", cls="tx", fill=GOAL, w=700)
    box(s, 32, 64, 120, 50, "每 10 分鐘", sub="pollSCM 或 cron", col=GOAL, kind="solid")
    arrow(s, 152, 89, 170, 89, col=GOAL, ar="ar-g")
    box(s, 170, 64, 150, 50, "問 depot", sub="p4 changes -m1 //…", col=GOAL, kind="solid")
    arrow(s, 320, 89, 338, 89, col=GOAL, ar="ar-g")
    box(s, 338, 64, 78, 50, "有新 CL", sub="就跑 check", col=GOAL, kind="solid")
    T(s, 32, 136, "記下看過的最大 CL 號；重啟不重跑", fill=INK2)
    for k, (ok, t) in enumerate([(True, "不碰 p4 server，不用 admin"), (True, "MVP 第 6 步就用這個"), (False, "最多晚幾分鐘才知道"), (False, "擋不住：改動已經進去了")]):
        check(s, 32, 166 + 24 * k, ok, t, cls="tx")
    T(s, 32, 270, "有 Jenkins：job 設 pollSCM。沒有：農場節點的 cron 跑一支 script。", fill=INK2)
    # 右：trigger
    rect(s, 445, 30, 415, 300, col=GOAL, fill=GOAL, op=".04", sw=1.4, dash="6 4")
    T(s, 457, 50, "trigger：裝在 p4 server 上，CAD 才能裝", cls="tx", fill=GOAL, w=700)
    rect(s, 457, 64, 390, 58, col=INK2, fill="var(--surface-2)", sw=1.1)
    T(s, 469, 82, "p4 server 的一張表（p4 triggers，super 才能編輯）", cls="tx", fill=INK2, w=700)
    T(s, 469, 100, "每一行：名字　事件　路徑　跑哪支 script", fill=INK2)
    T(s, 469, 114, "desc-check change-submit //depot/... \"desc_check.py %change%\"", fill=GRAY)
    T(s, 457, 144, "script 跑在 p4d 那台主機上，拿得到 %change%、%user%、%client%", fill=INK2)
    for k, (ok, t) in enumerate([(True, "submit 當下就跑，能退回"), (True, "shelve 時也能跑，review 看到的是綠的"), (False, "只有 super 能裝：agent 寫好交 CAD"), (False, "使用者在等：要快，重的事不能放這裡")]):
        check(s, 457, 174 + 24 * k, ok, t, cls="tx")
    T(s, 457, 278, "agent 先在沙盒的 p4d 裝起來測到對，再交 shelved CL。", fill=INK2)
    bottom(s, 346, [
        ("察覺改動有兩種方法：定時查 agent 自己就能裝、擋不住；trigger 裝在 p4 server 上、能擋、要 CAD 裝、要快。", True),
        ("先定時查（只報告級），穩定了才談 trigger（第 9 步）。", False),
    ])
    aria = ("左框定時查：每 10 分鐘問 depot 有沒有新 CL，有就跑 check；優點不碰 p4 server、agent 自己能裝，缺點晚幾分鐘、擋不住。右框 trigger：p4 server 上的一張表，每行事件、路徑、script；submit 當下就跑、能退回，但只有 super 能裝、要快。")
    return svg(s, 880, 480, aria)


# ── 圖 4：trigger 四種事件 ──────────────────────────────────────────
def p4():
    s = []
    T(s, 20, 24, "一次 submit 在 p4 server 上經過的點", cls="tx-lbl", fill=INK2)
    steps = [("工程師按 submit", INK2, "plain"), ("change-submit", GOAL, "solid"), ("檔案傳到 server", INK2, "plain"), ("change-content", GOAL, "solid"), ("commit 進 depot", INK2, "plain"), ("change-commit", GOAL, "dash")]
    x = 20
    xs = []
    for t, col, kind in steps:
        w = width(t, 12) + 26
        rect(s, x, 40, w, 30, col=col, fill=col if kind != "plain" else "var(--surface-2)", op=".12" if kind == "solid" else (".05" if kind == "dash" else None), sw=1.3, dash="6 4" if kind == "dash" else None)
        T(s, x + w / 2, 60, t, anchor="middle", cls="tx", fill=col if kind != "plain" else INK2, w=700 if kind != "plain" else None)
        xs.append((x, w)); x += w + 14
    for (xa, wa), (xb, wb) in zip(xs, xs[1:]):
        arrow(s, xa + wa, 55, xb, 55, col=INK2, ar="ar-gray", sw=1.2)
    T(s, 20, 90, "另一條：工程師 shelve → shelve-commit（對 shelved CL 先跑 check，review 的人看到的是已經綠的）", fill=INK2)
    # 表
    T(s, 20, 118, "事件", cls="tx-lbl", fill=GOAL); T(s, 150, 118, "能不能擋", cls="tx-lbl", fill=INK2); T(s, 320, 118, "拿來做", cls="tx-lbl", fill=INK2); T(s, 680, 118, "要注意", cls="tx-lbl", fill=WARN)
    rows = [
        ("change-submit", "能（exit 非 0 退回）", "說明有沒有寫目的；netlist 這類產物有沒有放進 rtl/；一包太大", "使用者在等：幾秒內"),
        ("change-content", "能", "看內容：filelist 引用的檔在不在、禁止的字串", "使用者在等：要快"),
        ("change-commit", "不能", "叫 Jenkins 跑 sanity、通知、打 known-good；長的 check 放這裡", "已進 depot，壞了只能通知"),
        ("shelve-commit", "不能", "對 shelved CL 跑 check；配合「shelve 給人看」的常規", "shelve 很頻繁，check 要輕"),
    ]
    for k, (ev, blk, use, warn) in enumerate(rows):
        y = 130 + k * 40
        T(s, 20, y + 18, ev, cls="tx", fill=GOAL, w=700)
        pill(s, 150, y + 4, blk, GOAL if blk.startswith("能") else GRAY, h=20)
        T(s, 320, y + 18, use, fill=INK2)
        T(s, 680, y + 18, warn, fill=WARN)
        line(s, 20, y + 34, 860, y + 34)
    T(s, 20, 306, "升級的順序：MVP 第 6 步定時查（不裝 trigger）→ change-commit 叫 Jenkins → 穩定後才裝 change-submit／change-content 擋。", fill=INK2)
    bottom(s, 326, [
        ("trigger 有四種事件：submit 前的兩種能擋，但使用者在等、幾秒內要跑完；進 depot 後的那種叫 Jenkins 跑長的 check。", True),
        ("agent 寫 script 與那一行定義、在沙盒 p4d 上測好、交 shelved CL；真實 server 由 CAD 裝，裝之前請示。", False),
    ])
    aria = ("上排是一次 submit 經過的點：按 submit → change-submit → 檔案傳到 server → change-content → commit 進 depot → change-commit；另一條 shelve → shelve-commit。"
            "下表四列：change-submit（能擋，查說明與產物，要快）、change-content（能擋，看內容，要快）、change-commit（不能擋，踢 Jenkins、通知、known-good）、shelve-commit（不能擋，對 shelved CL 跑 check）。")
    return svg(s, 880, 480, aria)


# ── 圖 5：三個等級一支 script ───────────────────────────────────────
def p5():
    s = []
    rect(s, 20, 30, 380, 196, col=INK2, fill="var(--surface-2)", sw=1.1)
    T(s, 32, 50, "desc_check.py  %change% %user%（示意）", cls="tx", fill=INK2, w=700)
    code = [
        "desc = p4 -ztag -F %Description% change -o $change",
        "ok = len(desc) >= 20 and not desc.startswith(\"update\")",
        "if not ok:",
        "    print(\"[cicd-mentor] CL 的說明太短或只寫 update/fix，請寫目的\")",
        "",
        "sys.exit(0)                    # 只報告、警告：永遠放行",
        "# 擋：sys.exit(0 if ok else 1)",
        "# 說明裡有 [bypass:原因] 的放行並記錄",
        "# 開頭先讀開關檔：總開關關了就 exit 0",
    ]
    for k, l in enumerate(code):
        T(s, 32, 72 + 16 * k, l, fill=GRAY if l.startswith("#") or "# " in l and l.startswith("sys") else INK2)
    T(s, 32, 214, "三個等級只差最後幾行；check 的邏輯不變", fill=INK2)
    # 右：三欄
    cols = [("只報告", GOAL, ["submit 後跑", "永遠 exit 0", "結果寫 log、build 頁", "出錯：放行"]),
            ("警告", GOAL, ["submit 後跑", "exit 0，私訊本人", "誤報少了才升到擋", "出錯：放行"]),
            ("擋", WARN, ["submit 前跑", "exit 1 就退回", "要同意、bypass、總開關", "出錯：預設放行並通知"])]
    for k, (t, col, items) in enumerate(cols):
        x = 416 + k * 150
        lines_in_box(s, x, 30, 144, 120, t, items, col=col, kind="solid" if col == GOAL else "dash", gap=18)
    T(s, 416, 176, "bypass：CL 說明寫 [bypass:原因]，放行並記錄；PM 看得到誰用了幾次", fill=INK2)
    T(s, 416, 194, "總開關：trigger 表那行註解掉，或 script 開頭讀開關檔；PM 與 admin 都按得到", fill=INK2)
    T(s, 416, 212, "吵了（誤報、抱怨）就退一級，不硬撐", fill=INK2)
    bottom(s, 248, [
        ("三級是同一支 script：只報告與警告永遠 exit 0、只寫下來或私訊；擋的才 exit 1，而且 bypass 與總開關要先有。", True),
        ("只報告與警告這兩級一定「出錯也放行」，否則 script 一壞全公司不能 submit。", False),
    ])
    aria = ("左邊是示意的 trigger script：查 CL 說明長度與用語，不合印訊息；最後幾行決定等級：exit 0 永遠放行是只報告與警告，exit 1 是擋，另有 bypass 與開關檔。右邊三欄只報告、警告、擋各列時機、exit、通知、出錯時的行為；下方說明 bypass 與總開關怎麼做。")
    return svg(s, 880, 480, aria)


# ── 圖 6：Jenkins 六個概念 ──────────────────────────────────────────
def p6():
    s = []
    # depot
    rect(s, 20, 40, 180, 120, col=INK2, fill="var(--surface-2)", sw=1.2)
    T(s, 32, 60, "depot", cls="tx", fill=INK2, w=700)
    for k, t in enumerate(["//…/dma/Jenkinsfile", "//…/dma/scripts/run_sanity.sh", "//…/dma/scripts/make_manifest.sh", "//…/dma/scripts/make_release"]):
        T(s, 32, 80 + 18 * k, t, fill=INK2)
    # Jenkins server
    rect(s, 240, 30, 320, 150, col=GOAL, fill=GOAL, op=".06", sw=1.4)
    T(s, 252, 50, "Jenkins server（網頁與 API）：排程與記錄", cls="tx", fill=GOAL, w=700)
    rect(s, 252, 60, 296, 50, col=GOAL, fill="var(--surface)", sw=1.2)
    T(s, 264, 78, "job：dma-sanity（Pipeline）", cls="tx", fill=GOAL, w=700)
    T(s, 264, 96, "只記：Jenkinsfile 在哪、credential、何時跑", fill=INK2)
    x = 252
    for t in ["觸發 pollSCM 每 10 分", "credential p4-agent"]:
        x += pill(s, x, 120, t, GOAL, h=20) + 6
    T(s, 252, 164, "agent 用 API：建 job、按 build、讀結果；不登進這台", fill=AGENT)
    arrow(s, 200, 86, 240, 86, col=INK2, ar="ar-gray", sw=1.2); T(s, 220, 80, "拿", anchor="middle", fill=GRAY)
    # node
    rect(s, 600, 30, 260, 70, col=GOAL, fill=GOAL, op=".06", sw=1.4)
    T(s, 612, 50, "執行節點：Jenkins 派工的機器", cls="tx", fill=GOAL, w=700)
    T(s, 612, 68, "有 p4 與 bsub；照 Jenkinsfile 跑", fill=INK2)
    T(s, 612, 86, "Jenkins 自己不跑 EDA，派工給它", fill=INK2)
    arrow(s, 560, 65, 600, 65, col=GOAL, ar="ar-g"); T(s, 580, 58, "派工", anchor="middle", fill=GOAL)
    # farm
    rect(s, 600, 120, 260, 62, col=INK2, fill="var(--surface-2)", sw=1.2)
    T(s, 612, 140, "算力農場（LSF）", cls="tx", fill=INK2, w=700)
    T(s, 612, 158, "bsub -K run_sanity.sh：真正跑 EDA", fill=INK2)
    T(s, 612, 174, "用 agent 的 license 預算，和工程師一樣", fill=INK2)
    arrow(s, 730, 100, 730, 120, col=GOAL, ar="ar-g", sw=1.2); T(s, 740, 114, "bsub", fill=GOAL)
    # build page
    rect(s, 240, 200, 300, 96, col=GOAL, fill="var(--surface)", sw=1.4)
    T(s, 252, 220, "build #42（跑了一次）", cls="tx", fill=GOAL, w=700)
    for k, t in enumerate(["結果：PASS／FAIL；時間；哪個 CL", "console log：每一步印了什麼", "artifacts：manifest.json 留下來", "URL 就是「結果看得到」的那一頁"]):
        T(s, 252, 240 + 16 * k, t, fill=INK2)
    arrow(s, 600, 176, 540, 216, col=GOAL, ar="ar-g", sw=1.2); T(s, 578, 206, "回報", anchor="middle", fill=GOAL)
    # six concept pills
    T(s, 20, 200, "六個概念", cls="tx-lbl", fill=GOAL)
    for k, t in enumerate(["job", "Jenkinsfile", "執行節點", "觸發", "build", "credentials"]):
        pill(s, 20 + (k % 2) * 90, 210 + (k // 2) * 28, t, GOAL, h=22)
    T(s, 600, 206, "人做的兩件事", cls="tx-lbl", fill=PM)
    T(s, 600, 226, "CAD：給 agent 限定資料夾的帳號、說節點 label", fill=INK2)
    T(s, 600, 244, "PM：登入一次產 API token，交給 agent 放 config", fill=INK2)
    T(s, 600, 268, "沒 P4 plugin：p4sync 那行換成 sh 'p4 sync'", fill=GRAY)
    bottom(s, 316, [
        ("Jenkins 只做一件事：在指定的時機，派一台節點照 depot 裡的 Jenkinsfile 跑（這一串叫 pipeline），把 log 與產物留在 build 頁。", True),
        ("job 不含任何邏輯，只記去哪拿 Jenkinsfile；所以 agent 用 API 建 job、CAD 給帳號，就接上了。", False),
    ])
    aria = ("左上 depot 放 Jenkinsfile 與 script；中間 Jenkins server 的 job 只記去哪拿 Jenkinsfile、credential、觸發；右上執行節點有 p4 與 bsub，派工給農場跑 EDA；中下 build 頁留結果、log、artifacts。左下六個概念的膠囊：job、Jenkinsfile、執行節點、觸發、build、credentials；右下人做的兩件事。")
    return svg(s, 880, 480, aria)


# ── 圖 7：CD 多兩個 stage ───────────────────────────────────────────
def p7():
    s = []
    T(s, 20, 24, "同一個 Jenkinsfile 的 stage，由左到右", cls="tx-lbl", fill=GOAL)
    stages = [("sync", "乾淨 workspace", GOAL), ("sanity", "bsub -K run_sanity", GOAL), ("manifest", "make_manifest.sh", GOAL),
              ("release", "打包、manifest、label", GOAL), ("放到固定目錄", "取用處 //…/release/", GOAL), ("通知", "slack #dma-ci", GOAL)]
    x = 20
    xs = []
    for k, (t, sub, col) in enumerate(stages):
        w = 136
        rect(s, x, 40, w, 54, col=col, fill=col, op=".10" if k < 3 else ".18", sw=1.4)
        T(s, x + 8, 60, t, cls="tx", fill=col, w=700)
        T(s, x + 8, 78, sub, fill=INK2)
        xs.append((x, w)); x += w + 4
    for (xa, wa), (xb, wb) in zip(xs, xs[1:]):
        arrow(s, xa + wa, 67, xb, 67, col=GOAL, ar="ar-g", sw=1.2)
    # 閘
    gx = xs[2][0] + xs[2][1] + 4
    line(s, gx, 36, gx, 130, col=WARN, sw=1.6, dash="4 3")
    T(s, gx - 6, 124, "綠了才過這條線", anchor="end", fill=WARN)
    T(s, gx + 6, 124, "紅：停在這裡，通知本人，不打包", fill=WARN)
    T(s, xs[1][0], 110, "CI", cls="tx", fill=GOAL, w=700)
    T(s, xs[4][0], 110, "CD：接著做的三件事", cls="tx", fill=GOAL, w=700)
    # 下游
    rect(s, 20, 150, 400, 70, col=INK2, fill="var(--surface-2)", sw=1.2)
    T(s, 32, 170, "下游（top 整合、DV、PD）", cls="tx", fill=INK2, w=700)
    T(s, 32, 188, "從取用處拿最新一包，附 manifest：哪個 CL、什麼工具、怎麼跑", fill=INK2)
    T(s, 32, 206, "不問人、不等 email 貼路徑；要退回有 known-good 的 label", fill=INK2)
    arrow(s, xs[4][0] + 66, 94, 300, 150, col=GOAL, ar="ar-g", sw=1.2)
    # Jenkinsfile 片段
    rect(s, 440, 150, 420, 150, col=INK2, fill="var(--surface-2)", sw=1.1)
    T(s, 452, 170, "Jenkinsfile（示意）", cls="tx", fill=INK2, w=700)
    code = ["pipeline {", "  agent { label 'ic-farm' }", "  triggers { pollSCM('H/10 * * * *') }", "  stages {",
            "    stage('sync')     { steps { p4sync credential: 'p4-agent', depotPath: '//…/dma/...' } }",
            "    stage('sanity')   { steps { sh 'bsub -K ./scripts/run_sanity.sh' } }",
            "    stage('manifest') { steps { sh 'make_manifest.sh'; archiveArtifacts '*.json' } }",
            "    stage('release')  { when { branch 'main' } steps { sh './scripts/make_release' } }",
            "  }", "}"]
    for k, l in enumerate(code):
        T(s, 452, 188 + 11.5 * k, l, fill=INK2, size=8)
    T(s, 20, 240, "每個 stage 都只是呼叫 depot 裡的 script；release 只在 main 綠了才跑。", fill=INK2)
    bottom(s, 318, [
        ("CD 不是另一套系統：sanity 綠了之後，同一條流程接著做三件事：打包、放到固定目錄（取用處）、通知下游。", True),
        ("AI agent 幫 owner 定出交付物後，把 make_release 寫成 script 交 shelved CL；之後 main 過 check 就自動打包交下游。", False),
    ])
    aria = ("上排六格 stage：sync、sanity、manifest（CI），一條紅色虛線「綠了才過」，然後 release、取用處、通知（CD）。左下下游從取用處拿最新一包附 manifest；右下示意的 Jenkinsfile。")
    return svg(s, 880, 480, aria)


# ── 圖 8：分工 ──────────────────────────────────────────────────────
def p8():
    s = []
    T(s, 20, 24, "在哪裡", cls="tx-lbl", fill=INK2); T(s, 190, 24, "做什麼", cls="tx-lbl", fill=INK2); T(s, 580, 24, "agent 和它的關係", cls="tx-lbl", fill=AGENT)
    rows = [
        ("agent 的機器", AGENT, ["跑 Claude Code；有 p4 client、slack、", "Jenkins 的 API token"], ["讀 depot、分析、寫 script、試跑一次、", "交 shelved CL、讀結果、發訊息"]),
        ("p4 server", INK2, ["trigger：submit 時查 CL 說明，或踢一個 job"], ["agent 寫 trigger script 交 shelved CL；", "CAD 裝（要請示）"]),
        ("Jenkins", GOAL, ["編排：submit 後 sync 乾淨 workspace →", "run_sanity → manifest → release → 通知"], ["agent 寫 Jenkinsfile 與 job 定義，", "用 API 建、按、讀；不登進它"]),
        ("算力農場（LSF）", INK2, ["真正跑 EDA"], ["pipeline 用 bsub 送，和工程師一樣；", "agent 自己試跑也走這裡，用它的預算"]),
        ("取用處與 build 頁", GOAL, ["交付包、manifest、check 結果"], ["agent 只從這裡讀；", "工程師與下游也從這裡拿"]),
    ]
    for k, (where, col, what, rel) in enumerate(rows):
        y = 36 + k * 48
        pill(s, 20, y + 6, where, col, h=22)
        for j, t in enumerate(what): T(s, 190, y + 16 + 16 * j, t, fill=INK2)
        for j, t in enumerate(rel): T(s, 580, y + 16 + 16 * j, t, fill=INK2 if col != AGENT else AGENT)
        line(s, 20, y + 42, 860, y + 42)
    rect(s, 20, 284, 840, 66, col=PM, fill=PM, op=".06", sw=1.4)
    T(s, 32, 304, "人只做兩件事", cls="tx", fill=PM, w=700)
    T(s, 32, 322, "CAD：給 agent 一個限定資料夾（cicd-mentor/）的 Jenkins 帳號，說哪個節點有 p4 與 bsub。", fill=INK2)
    T(s, 32, 338, "PM：用那個帳號登入一次產 API token，交給 agent 放 config，不進 depot。", fill=INK2)
    bottom(s, 366, [
        ("五個地方各做自己的事，中間只靠 depot 裡的 script 與固定位置的結果檔接起來；AI agent 不登進任何 server。", True),
        ("CAD 不給帳號：agent 寫好 Jenkinsfile 與 job 定義，CAD 在網頁上貼一次，之後 agent 只要唯讀。", False),
    ])
    aria = ("五列：agent 的機器（讀寫、試跑、交 shelved CL、讀結果）、p4 server（trigger，agent 寫 CAD 裝）、Jenkins（編排，agent 用 API 建按讀）、算力農場（跑 EDA）、取用處與 build 頁（agent 只讀）。底下：人只做兩件事。")
    return svg(s, 880, 480, aria)


# ── 圖 9：git 的對應 ────────────────────────────────────────────────
def p9():
    s = []
    rect(s, 20, 30, 400, 184, col=WARN, fill=WARN, op=".04", sw=1.4, dash="6 4")
    T(s, 32, 50, "這頁給用 git 的 project；git 的 hook 兩種，都不是 CI", cls="tx", fill=WARN, w=700)
    T(s, 32, 72, "client 端：pre-commit、commit-msg、pre-push", cls="tx", fill=INK2, w=700)
    T(s, 32, 90, "在每個人的 .git/hooks，不隨 repo 走、各人自己裝", fill=INK2)
    check(s, 32, 112, False, "擋不住任何人，只能當提醒", cls="tx")
    T(s, 32, 146, "server 端：pre-receive、post-receive", cls="tx", fill=INK2, w=700)
    T(s, 32, 164, "在 git server 上；GitLab／GitHub 不開放放自己的 script", fill=INK2)
    T(s, 32, 182, "→ 改用右邊兩個內建機制", fill=INK2)
    rect(s, 440, 30, 420, 184, col=GOAL, fill=GOAL, op=".04", sw=1.4)
    T(s, 452, 50, "GitLab 內建的兩個機制，就是 CI 與擋", cls="tx", fill=GOAL, w=700)
    box(s, 452, 62, 190, 60, "pipeline（自動流程）", sub=".gitlab-ci.yml 在 repo 根目錄", sub2="每次 push 與每個 MR 自動跑", col=GOAL, kind="solid")
    box(s, 654, 62, 194, 60, "runner", sub="跑 job 的機器＝Jenkins 的節點", sub2="tag ic-farm：有 p4／EDA", col=GOAL, kind="solid")
    box(s, 452, 132, 396, 70, "protected branch＝擋", sub="master 只能經 MR 併入；MR 要 pipeline 綠＋一人 approve 才能按", sub2="不用自己寫 hook；agent 自己的 repo 走的就是這套", col=GOAL, kind="solid")
    # 對照表
    T(s, 20, 238, "Perforce", cls="tx-lbl", fill=INK2); T(s, 200, 238, "git", cls="tx-lbl", fill=INK2); T(s, 420, 238, "意思", cls="tx-lbl", fill=INK2)
    rows = [("depot", "repo、remote", "共用的那份"), ("submit", "commit＋push", "進共用的地方"), ("shelved CL", "branch＋MR（GitHub 叫 PR）", "給人看、還沒進去"),
            ("stream", "branch", "一件任務一條線"), ("label", "tag", "某一刻的檔案清單"), ("change-submit trigger", "protected branch＋pipeline 必須綠", "submit 前擋"),
            ("change-commit trigger", "post-receive、webhook", "submit 後踢 CI")]
    for k, (a, b, c) in enumerate(rows):
        y = 246 + k * 16
        T(s, 20, y + 12, a, fill=INK2); T(s, 200, y + 12, b, fill=INK2); T(s, 420, y + 12, c, fill=GRAY)
    bottom(s, 372, [
        ("用 git 的 project：client 端的 hook 擋不住人硬 push；pipeline 加 protected branch 才是 CI 與擋。名詞整套切換，原則不變。", True),
        ("agent 自己的 repo 就是這套：MR、pipeline 跑沙盒三項、master 鎖住。", False),
    ])
    aria = ("左框 git 的 hook：client 端在各人電腦擋不住人，server 端 GitLab 不開放。右框 GitLab 內建：pipeline（.gitlab-ci.yml、runner）與 protected branch（MR 要綠加 approve）就是 CI 與擋。下方 Perforce 對 git 的名詞對照七列。")
    return svg(s, 880, 480, aria)


# ── 圖 10：三個坑 ───────────────────────────────────────────────────
def p10():
    s = []
    cols = [
        ("trigger 太慢", ["change-submit、change-content", "是使用者按下去在等的；", "超過幾秒就被罵，然後被要求拆掉"],
         ["submit 前只做秒級的檢查", "重的 check 放 change-commit 後", "沙盒先量 trigger 跑多久"]),
        ("低等級的 check 壞了卻擋人", ["只報告級的 script 出了 exception、", "p4 指令失敗、磁碟滿；trigger 回非 0，", "所有人的 submit 都被退回"],
         ["只報告與警告級：出錯也 exit 0", "擋的那級：先有總開關與 bypass", "出錯時怎麼辦寫進授權表"]),
        ("把 client 端的 hook 當 CI", ["git 團隊裝了 pre-commit 以為有 CI；", "沒裝的人照樣推上去"],
         ["要擋靠 protected branch 或 server 端", "pre-commit 只當提醒，不當規則", "Perforce 沒這問題：trigger 在 server"]),
    ]
    for k, (t, sym, fixes) in enumerate(cols):
        x = 20 + k * 284
        rect(s, x, 30, 272, 250, col=WARN, fill=WARN, op=".04", sw=1.4, dash="6 4")
        T(s, x + 12, 52, t, cls="tx", fill=WARN, w=700)
        T(s, x + 12, 72, "症狀", cls="tx-lbl", fill=WARN)
        # wrap symptom roughly by splitting on ；
        for j, ptxt in enumerate(sym):
            T(s, x + 12, 90 + 16 * j, ptxt, fill=INK2)
        T(s, x + 12, 150, "做法", cls="tx-lbl", fill=GOAL)
        for j, f in enumerate(fixes):
            check(s, x + 12, 166 + 26 * j, True, f, cls="tx-s")
    bottom(s, 300, [
        ("三個坑都來自同一件事：submit 前的 check 有人在等，而且一壞就擋到所有人。", True),
        ("所以先從 submit 後、只報告開始；擋是最後一步，而且要有退路。", False),
    ])
    aria = ("三欄：trigger 太慢（submit 前只做秒級檢查，重的放 change-commit）；script 壞了全公司不能 submit（低等級出錯也放行，擋要先有總開關與 bypass）；把 client 端 hook 當 CI（要擋靠 protected branch）。")
    return svg(s, 880, 480, aria)


PAGES = [
    ("總覽：check 是 depot 裡的 script，機器自動跑；AI agent 寫 script、看結果", p1()),
    ("分工：人只開帳號、給 token；script、job、trigger 都由 AI agent 用 API 做", p8()),
    ("CI：每次 submit 在乾淨 workspace 跑 sanity、記下結果；submit 前跑才擋得住", p2()),
    ("察覺改動的兩條路：定時跑 p4 changes，agent 自己能裝；trigger 要 CAD 裝", p3()),
    ("Jenkins：負責排程與記錄的 server；check 實際在農場跑，每次結果留在 build 頁", p6()),
    ("trigger 兩類：submit 前的能擋、要幾秒跑完；submit 後的叫 Jenkins 跑長 check", p4()),
    ("check 分三級：只報告與警告不擋 submit；擋的才 exit 1，而且要先有 bypass", p5()),
    ("CD：sanity 綠了之後同一條流程接著自動打包、放到固定目錄、通知下游", p7()),
    ("用 git 的 project：client 端的 hook 擋不住人硬 push；要靠 protected branch 擋", p9()),
    ("三個坑：submit 前的 check 太慢、低等級卻擋人、把 client 的 hook 當成 CI", p10()),
]

if __name__ == "__main__":
    build(NAME, "CI/CD 在公司怎麼跑：check 是 depot 裡的 script，p4 trigger 與 Jenkins 自動跑；AI agent 寫與看結果，人只開帳號、給 token", KICKER, PAGES)

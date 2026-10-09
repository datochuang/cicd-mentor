# -*- coding: utf-8 -*-
# 《互動場景：agent 先讀懂再問再交 patch，方向由 PM 核准，採不採用團隊決定》
# docs/slides/agent-reads-asks-patches-pm-approves.{html,pdf}
# 執行：python3 docs/figures/agent-reads-asks-patches-pm-approves/build.py
#
# 讀者：會和這個 agent 打交道的人：可能的 PM、PL、owner 工程師。懂 Perforce；看過或沒看過前面幾份都行。
# 讀完要能：在每一種情況下說出誰對誰做什麼、agent 自己能做什麼、什麼要問、什麼要 PM 決定。
# 主旨：agent 先讀懂再問再交 patch；方向與影響他人的事 PM 懂了才算；採不採用是團隊的事。
# 內容來源：agent-operating-model.md（使用者的原始描述與補充）。所有訊息的例句都是示意。
# 版型：第 1 頁角色 × 階段的表；之後每頁一個場景，四條泳道 PM／agent／工程團隊／repo，箭頭＝誰對誰做什麼。
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from slides import *

NAME = "agent-reads-asks-patches-pm-approves"
KICKER = "agent 與 PM、團隊、repo 的互動"

LANES = [("PM", PM), ("agent", AGENT), ("工程團隊", INK2), ("repo", GOAL)]
LANE_Y = {name: 36 + i * 70 for i, (name, _) in enumerate(LANES)}
LANE_COL = dict(LANES)
X0 = 104


def lanes(s):
    for i, (name, col) in enumerate(LANES):
        y = LANE_Y[name]
        rect(s, 20, y, 840, 62, col="var(--rule)", fill="var(--surface-2)" if i % 2 else "var(--surface)", sw=1)
        T(s, 32, y + 36, name, cls="tx", fill=col, w=700)


def act(s, lane, x, w, title, sub=None, col=None, kind="solid"):
    """泳道裡的一個動作方塊。"""
    y = LANE_Y[lane] + 8
    c = col or LANE_COL[lane]
    if kind == "solid":
        rect(s, x, y, w, 46, col=c, fill=c, op=".10", sw=1.4)
    elif kind == "dash":
        rect(s, x, y, w, 46, col=c, fill=c, op=".05", sw=1.3, dash="5 3")
    else:
        rect(s, x, y, w, 46, col="var(--rule-2)", fill="var(--surface)", sw=1.1)
    T(s, x + 8, y + 18, title, cls="tx", fill=c, w=700)
    if sub:
        T(s, x + 8, y + 36, sub, fill=INK2)


def flow(s, frm, to, x, label=None, col=None):
    """泳道之間的垂直箭頭：從 frm 的方塊邊緣到 to 的方塊邊緣。"""
    c = col or LANE_COL[frm]
    yf, yt = LANE_Y[frm], LANE_Y[to]
    if yt > yf:
        y1, y2 = yf + 8 + 46 + 2, yt + 8 - 3
    else:
        y1, y2 = yf + 8 - 2, yt + 8 + 46 + 3
    ar = {"PM": "ar-p", "agent": "ar-a", "工程團隊": "ar", "repo": "ar-g"}[frm]
    arrow(s, x, y1, x, y2, col=c, ar=ar, sw=1.5)
    if label:
        T(s, x + 6, y1 + (14 if y2 > y1 else -8), label, fill=GRAY)


def scene(s, when, auth):
    T(s, 20, 22, when, cls="tx-lbl", fill=INK2)
    pill(s, 860, 6, auth, PM, h=22, anchor="end")


# ── 圖 1：總覽——三方各缺什麼，agent 補什麼 ───────────────────────────
def card(s, x, y, w, h, title, col, has, lacks=None, kind="solid"):
    if kind == "solid":
        rect(s, x, y, w, h, col=col, fill=col, op=".10", sw=1.8)
    else:
        rect(s, x, y, w, h, col=col, fill=col, op=".05", sw=1.4, dash="6 4")
    T(s, x + 12, y + 22, title, cls="tx", fill=col, w=700)
    T(s, x + 12, y + 42, has, fill=INK2)
    if lacks:
        T(s, x + 12, y + 60, lacks, fill=WARN, cls="tx")


def p_cover():
    s = []
    # PM
    card(s, 300, 28, 280, 72, "PM：負責導入 CI/CD 的人", PM, "有：決心、方向、組織的權威", "缺：經驗、實作的技能")
    # agent
    rect(s, 300, 196, 280, 92, col=AGENT, fill=AGENT, op=".10", sw=1.8)
    T(s, 312, 218, "agent", cls="tx", fill=AGENT, w=700)
    T(s, 312, 238, "有：CI/CD 經驗、Perforce 與 scripting 技能", fill=INK2)
    T(s, 312, 258, "不眠不休；把 PM 缺的經驗、團隊缺的方法補上", cls="tx", fill=AGENT, w=700)
    T(s, 312, 278, "方向仍由 PM 決定；CL 收不收仍由 owner 決定", fill=GRAY)
    # team
    card(s, 670, 196, 190, 92, "工程團隊", INK2, "有：design 的本事", "缺：不堅決、不知怎麼做")
    # repo
    card(s, 20, 196, 190, 92, "repo（depot）", GOAL, "今天：只當備份用", "目標：CI/CD 的地基", kind="dash")
    # PM <-> agent
    arrow(s, 380, 104, 380, 192, col=PM, ar="ar-p", sw=1.8)
    T(s, 372, 150, "定方向、核准（懂了才算）", anchor="end", fill=PM)
    arrow(s, 460, 192, 460, 104, col=AGENT, ar="ar-a", sw=1.8)
    T(s, 468, 142, "請准單附原則與取捨", fill=AGENT)
    T(s, 468, 158, "一頁摘要；教到 PM 懂", fill=AGENT)
    # agent <-> team
    arrow(s, 584, 222, 666, 222, col=AGENT, ar="ar-a", sw=1.8)
    T(s, 625, 212, "問、示範、代做", anchor="middle", fill=AGENT)
    arrow(s, 666, 262, 584, 262, col=INK2, ar="ar", sw=1.6)
    T(s, 625, 280, "回答、採用", anchor="middle", fill=INK2)
    # agent <-> repo
    arrow(s, 296, 222, 214, 222, col=AGENT, ar="ar-a", sw=1.8)
    T(s, 255, 212, "讀懂、裝 check", anchor="middle", fill=AGENT)
    arrow(s, 214, 262, 296, 262, col=GOAL, ar="ar-g", sw=1.6)
    T(s, 255, 280, "CL、結果、狀態板", anchor="middle", fill=GOAL)
    # team -> repo（底下繞）
    path(s, "M765,292 L765,308 L115,308 L115,294", col=INK2, ar="ar", sw=1.3, dash="4 3")
    T(s, 440, 304, "工程師 submit、shelve，照 agent 準備好的流程做", anchor="middle", fill=GRAY)
    # PM <-> team（親自出面）
    path(s, "M584,56 L765,56 L765,192", col=PM, ar="ar-p", sw=1.3, dash="5 3")
    T(s, 757, 128, "親自出面：宣布、第一次擋、衝突", anchor="end", fill=PM)
    # 時間軸
    phases = [("啟動", "PM 給範圍與帳號", "agent 自我介紹"), ("盤點", "agent 只讀掃", "PM 選目標"), ("試點", "agent 交 shelved CL", "owner 採用"),
              ("擴散", "check 升級", "陪人開工"), ("常態", "團隊自己維護", "agent 只剩監看")]
    for i, (name, l1, l2) in enumerate(phases):
        x = 20 + i * 168
        pill(s, x, 330, name, GOAL, h=20)
        T(s, x, 364, l1, fill=INK2)
        T(s, x, 380, l2, fill=INK2)
        if i < 4:
            arrow(s, x + 150, 340, x + 164, 340, col=GRAY, ar="ar-gray", sw=1)
    bottom(s, 398, [
        ("PM 有決心沒經驗，團隊不堅決也不知道怎麼做；agent 補的正是這兩個缺：給 PM 可核准的提案與經驗，給團隊方法與陪做。", True),
        ("後面每頁一個場景；下一頁是每個階段誰做什麼的總表、授權三級、用語。", False),
    ])
    aria = ("四張卡：上方 PM，負責導入 CI/CD 的人，有決心、方向、組織的權威，缺經驗與實作技能；中間 agent，有 CI/CD 經驗、Perforce 與 scripting 技能、不眠不休，把 PM 缺的經驗、團隊缺的方法補上；"
            "右邊工程團隊，有 design 的本事，缺不堅決、不知怎麼做；左邊 repo，今天只當備份用，目標變成 CI/CD 的地基。"
            "箭頭：PM 對 agent 定方向與核准，agent 對 PM 請准單與一頁摘要並教到懂；agent 對團隊問、示範、代做，團隊回答、採用；"
            "agent 對 repo 讀懂、裝 check，repo 回 CL、結果、狀態板；工程師 submit 與 shelve 照 agent 準備好的流程；PM 親自出面的三件事是宣布、第一次擋、衝突。"
            "下方時間軸：啟動、盤點、試點、擴散、常態各兩句主要互動。")
    return svg(s, 880, 480, aria)


# ── 圖 2：總表，角色 × 階段 ──────────────────────────────────────────
PHASES = ["啟動", "盤點", "目標分析與訪談", "計畫核准", "建置", "上線分級", "監看與開工", "擴充與交棒"]
GRID = {
    "PM": ["給範圍、帳號|與預算", "選候選目標", "看進度", "懂了才核准", "看進度", "同意擋不擋", "看一頁摘要", "定交棒條件"],
    "agent": ["bot 上線|自我介紹", "只讀掃|一頁現況", "先讀懂|再問 owner", "附取捨|請核准", "做成|shelved CL", "附證據|提議升級", "看 CL、DM|登記開工", "提下一道|只剩監看"],
    "工程團隊": ["知道 agent 在|看得到什麼", "", "owner 答只有|他知道的", "owner 同意|動範圍", "負責人|補強 script", "同意升級", "回一句|照流程開工", "自己維護|pipeline"],
    "repo": ["日誌、狀態板|的位置", "唯讀", "乾淨 workspace|實跑", "決定進 depot", "shelved CL|＋證據", "報告→警告→擋", "跑 check|狀態板", "check 穩定|趨勢"],
}


def p_overview():
    s = []
    T(s, 20, 20, "每個階段誰做什麼（上一頁的展開）；agent 自己能做什麼、什麼要問、什麼要 PM 決定 ↓", cls="tx-lbl", fill=INK2)
    cw, x0, y0, rh = 94, 110, 36, 54
    for j, ph in enumerate(PHASES):
        T(s, x0 + j * cw + cw / 2, y0 + 14, ph, anchor="middle", fill=GRAY)
        line(s, x0 + j * cw, y0 + 22, x0 + j * cw, y0 + 22 + rh * 4, col="var(--rule)")
    for i, (name, col) in enumerate(LANES):
        y = y0 + 22 + i * rh
        rect(s, 20, y, 840, rh, col="var(--rule)", fill="var(--surface-2)" if i % 2 else "var(--surface)", sw=1)
        T(s, 32, y + 31, name, cls="tx", fill=col, w=700)
        for j, cell in enumerate(GRID[name]):
            if not cell:
                continue
            for k, w_ in enumerate(cell.split("|")[:2]):
                T(s, x0 + j * cw + 6, y + 22 + 16 * k, w_, fill=col if name != "工程團隊" else INK2)
    ya = y0 + 22 + rh * 4 + 10
    T(s, 20, ya + 12, "agent 的授權三級", cls="tx-lbl", fill=PM)
    tiers = [("自主", "讀、分析、寫地圖、開 shelved CL、DM"), ("告知", "建議、第二次提醒、交 shelved CL"), ("請准", "方向、新規範、裝 trigger、擋 submit、拉 PL 群聊")]
    x = 20
    for name, desc in tiers:
        w_ = pill(s, x, ya + 20, name, PM, h=20)
        T(s, x + w_ + 6, ya + 34, desc, fill=INK2)
        x += w_ + 6 + width(desc, 10.5) + 24
    T(s, 20, ya + 62, "用語", cls="tx-lbl", fill=GRAY)
    T(s, 60, ya + 62, "%s　PROJECT_MAP＝agent 寫在 depot 裡的目錄用途與相依說明" % "PM＝負責把團隊開發流程導入 CI/CD 的人（和 project 的 PM 無關）", fill=INK2)
    T(s, 60, ya + 80, "狀態板＝每個模組休止／進行中哪些任務的表，也在 depot　subagent＝agent 分出去做一件事的子程式　shelved CL＝給人看、還沒 submit 的改動（git 的 PR）", fill=INK2)
    bottom(s, ya + 96, [
        ("agent 先讀懂再問，改動做成 shelved CL；方向與影響別人的事，PM 懂了才算核准；CL 收不收是 owner 的事。", True),
        ("後面每頁一個場景，四條泳道，箭頭就是誰對誰做什麼；最後兩頁是橫跨全程的規則。", False),
    ])
    aria = ("角色乘階段的表。階段：啟動、情勢判斷、目標分析與訪談、計畫請准、建置、採用、看守與開工、加強與退場。"
            "PM：給範圍帳號預算、選切入目標、看進度、懂了才核准、看進度、同意擋不擋、看一頁摘要、定退場條件。"
            "agent：bot 上線自我介紹、只讀掃一頁報告、先讀懂再問 owner、附取捨請准、做成 shelved CL、附證據提議升級、看 CL 私訊登記開工、提下一道退到看守。"
            "工程團隊：知道 agent 在、owner 答只有他知道的、owner 同意動範圍、負責人補強 script、同意升級、回一句照流程開工、自己維護 pipeline。"
            "repo：日誌與狀態板的位置、唯讀、乾淨 workspace 實跑、決定進 depot、shelved CL 加證據、報告警告擋、trigger 跑 check 與狀態板、check 穩定與趨勢。"
            "下方是授權三級：自主、告知、請准；以及用語：PM 指負責把團隊開發流程導入 CI/CD 的人、和 project 的 PM 無關，PROJECT_MAP、狀態板、subagent、shelved CL 各一句定義。")
    return svg(s, 880, 480, aria)


# ── 場景頁的共用骨架 ─────────────────────────────────────────────────
def scenario(when, auth, acts, flows, lines, aria, notes=None):
    s = []
    scene(s, when, auth)
    lanes(s)
    for a in acts:
        act(s, *a[:4], sub=a[4] if len(a) > 4 else None, col=a[5] if len(a) > 5 else None, kind=a[6] if len(a) > 6 else "solid")
    for f in flows:
        flow(s, *f)
    if notes:
        for k, n in enumerate(notes):
            T(s, 20, 330 + 18 * k, n, fill=GRAY)
    bottom(s, 352 + (18 * len(notes) if notes else 0), lines)
    return svg(s, 880, 480, aria)


W = 118   # 一步的寬
def xs(n, w=W, gap=9):
    return [X0 + i * (w + gap) for i in range(n)]


# ── 圖 2：啟動 ──────────────────────────────────────────────────────
def p_start():
    x = xs(5, w=140, gap=12)
    acts = [("PM", x[0], 140, "指定範圍與帳號", "能看哪些目錄、預算"),
            ("agent", x[1], 140, "以 bot 帳號上線", "先只讀，之後分階段加"),
            ("agent", x[2], 140, "自我介紹", "私訊 PL 與 owner"),
            ("工程團隊", x[3], 140, "知道 agent 在", "它看得到什麼、紀錄放哪"),
            ("repo", x[4], 140, "日誌與狀態板的位置", "進 depot，所有人看得到")]
    flows = [("PM", "agent", x[0] + 70, "給範圍"), ("agent", "工程團隊", x[2] + 70, "「我是 agent，向 PM 報告」"), ("agent", "repo", x[4] + 70, "建目錄")]
    return scenario("什麼時候：PM 決定開始的第一天", "授權：PM 請准", acts, flows,
        [("agent 用自己的 bot 帳號、只讀權限上線；第一件事是向團隊說自己是誰、向誰報告、會看什麼、紀錄放哪。", True),
         ("權限分階段：先只讀，要交 shelved CL 時加寫入，要開 stream 時再加；每一階 PM 給，agent 不自己擴。", False)],
        "啟動：PM 指定範圍與帳號；agent 以 bot 帳號先只讀上線，之後按需要分階段加權限，私訊 PL 與 owner 自我介紹；工程團隊知道 agent 在、看得到什麼；repo 裡建好日誌與狀態板的位置。",
        notes=["示意的自我介紹：「我是 CI/CD mentor agent，向 PM 某某報告。我會看 //depot/chipA/dma 的 CL 與 check 結果，", "紀錄在 //depot/chipA/agent-log。有問題直接私訊我。」"])


# ── 圖 3：情勢判斷 ──────────────────────────────────────────────────
def p_survey():
    x = xs(6)
    acts = [("PM", x[0], W, "指定 depot 範圍", "附預算"),
            ("agent", x[1], W, "只讀掃描", "結構、歷史、既有自動化"),
            ("repo", x[2], W, "depot（唯讀）", "stream、CL 歷史、trigger"),
            ("agent", x[3], W, "一頁現況報告", "六原則打分、熱點、風險"),
            ("agent", x[4], W, "建議切入目標", "一到三個，附理由"),
            ("PM", x[5], W, "選目標", "痛點、owner 願意")]
    flows = [("PM", "agent", x[0] + W / 2, "指定"), ("agent", "repo", x[2] + W / 2, "不逐檔讀"), ("agent", "PM", x[4] + W / 2, "報告")]
    return scenario("什麼時候：PM 要整體盤點，還沒決定從哪裡開始", "授權：自主（只讀）", acts, flows,
        [("盤點只讀、有預算、看不完就寫清楚看了什麼沒看什麼；交出去的是一頁現況和幾個候選目標，選哪個是 PM 的事。", True),
         ("推測的東西（負責人、目的）一律標「推測」，等目標分析時再問本人。", False)],
        "盤點：PM 指定 depot 範圍附預算；agent 只讀掃描結構、歷史、既有自動化；交一頁現況報告（六原則打分、熱點、風險）並建議一到三個切入目標；PM 選目標。",
        notes=["報告裡每個判斷都附依據：擷取（從檔案或歷史讀到）、實跑（在乾淨 workspace 跑過）、推測。"])


# ── 圖 4：目標分析與訪談 ─────────────────────────────────────────────
def p_analyze():
    x = xs(6)
    acts = [("PM", x[0], W, "指定一個目標", "module 或子目錄"),
            ("agent", x[1], W, "先讀懂", "地圖、六原則檢查"),
            ("repo", x[2], W, "乾淨 workspace", "只靠 depot 編、跑 sanity"),
            ("agent", x[3], W, "私訊 owner", "只問他才知道的"),
            ("工程團隊", x[4], W, "owner 回答", "或說先擱置"),
            ("agent", x[5], W, "記進地圖", "依據標「告知」")]
    flows = [("PM", "agent", x[0] + W / 2, "指定"), ("agent", "repo", x[2] + W / 2, "實跑"), ("agent", "工程團隊", x[3] + W / 2, "問"), ("工程團隊", "agent", x[4] + W / 2, "答")]
    return scenario("什麼時候：PM 指定了一個目標，agent 第一次進去", "授權：自主（讀、問）", acts, flows,
        [("問之前先查，問的時候附證據；只問只有 owner 知道的事，一次一批。", True),
         ("owner 說先擱置，agent 聽理由、談折衷、記下什麼時候回來問。", False)],
        "目標分析與訪談：PM 指定一個 module 或子目錄；agent 先讀懂，寫 PROJECT_MAP 初稿、做六原則檢查，在乾淨 workspace 實跑；再私訊 owner 只問他才知道的事並附已查到的；owner 回答或說先擱置；回答記進 PROJECT_MAP 標告知。",
        notes=["示意的私訊：「這個目錄是 DMA 的 RTL，由 tb/dma 驗，交給 top 整合，對嗎？top.f 引用的 dma_ctrl.v 我找不到，在你那裡嗎？」", "只有 owner 知道的事：缺的檔在誰那裡、猜的用途對不對、交付物給誰、進行中的大包怎麼拆、flow 的正本誰維護。"])


# ── 圖 5：計畫請准 ──────────────────────────────────────────────────
def p_approve():
    x = xs(6)
    acts = [("agent", x[0], W, "缺口與計畫", "每個缺口掛一個原則"),
            ("agent", x[1], W, "請准方向與順序", "原則、取捨、替代"),
            ("PM", x[2], W, "理解後核准", "說得出影響誰"),
            ("agent", x[3], W, "請 owner 同意", "做什麼、怎麼退"),
            ("工程團隊", x[4], W, "owner 同意", "或改範圍"),
            ("repo", x[5], W, "決定進 depot", "決定紀錄、地圖")]
    flows = [("agent", "PM", x[1] + W / 2, "請准"), ("PM", "agent", x[2] + W / 2, "核准"), ("agent", "工程團隊", x[3] + W / 2, "請同意"), ("工程團隊", "repo", x[4] + W / 2, "")]
    return scenario("什麼時候：目標分析完成，要開始動之前", "授權：PM 請准 ＋ owner 同意", acts, flows,
        [("方向、優先順序、對團隊的新要求是方針層：PM 懂了才算核准，owner 同意才動他的範圍。", True),
         ("請准要分批、附取捨；PM 不懂就問，蓋章不算核准。", False)],
        "計畫請准：agent 列出缺口與 patch 計畫，每個缺口掛一個原則；向 PM 請准方向與優先順序，附原則、取捨、替代方案、影響誰；PM 理解後核准；agent 再請 owner 同意動他的範圍；決定記進 depot。",
        notes=["計畫裡每條 patch 標三類之一：agent 自己能補、補了要 owner 決定、只有 owner 知道。"])


# ── 圖 6：建置 ──────────────────────────────────────────────────────
def p_build():
    x = xs(5, w=140, gap=12)
    acts = [("agent", x[0], 140, "拆成三層", "觸發／檢查工具／結果可見"),
            ("工程團隊", x[1], 140, "script 負責人", "談怎麼補強、怎麼接"),
            ("agent", x[2], 140, "沒有的：需求 markdown", "給 subagent 或人實作"),
            ("repo", x[3], 140, "shelved CL＋證據", "在自己的 workspace 跑過"),
            ("工程團隊", x[4], 140, "owner 採用＝submit", "不採用回一句")]
    flows = [("agent", "工程團隊", x[1] + 70, "談"), ("agent", "repo", x[3] + 70, "交"), ("repo", "工程團隊", x[4] + 70, "採用")]
    return scenario("什麼時候：計畫核准後，補某個缺口", "授權：自主做；裝 trigger 請准", acts, flows,
        [("機制分三層：觸發與流程、檢查工具、結果可見；既有的找負責人補強，沒有的用需求 markdown 讓 subagent 或人做。", True),
         ("不論誰做，交付都是 shelved CL 加測試證據；owner submit 才進 depot。", False)],
        "建置：agent 把機制拆成觸發與流程、檢查工具、結果可見三層；既有 script 找負責人談補強；沒有的寫需求 markdown，由 subagent 或人實作測試部署；交付是 shelved CL 加測試證據；owner 採用等於 submit，不採用回一句為什麼。",
        notes=["需求 markdown 的最低內容：目的、input、output、通過的定義、時間與資源預算、在哪裡跑、owner、怎麼測它自己。"])


# ── 圖 7：採用階梯 ──────────────────────────────────────────────────
def p_adopt():
    x = xs(6)
    acts = [("repo", x[0], W, "check 只報告", "結果看得到，不擋"),
            ("工程團隊", x[1], W, "用一段時間", "穩不穩、誤報多不多"),
            ("agent", x[2], W, "附證據提議升級", "誤報率、抓到什麼"),
            ("repo", x[3], W, "警告", "submit 時提示，不擋"),
            ("PM", x[4], W, "PM、owner 都同意", "才擋；留 bypass"),
            ("repo", x[5], W, "擋 submit", "留 bypass")]
    flows = [("repo", "工程團隊", x[1] + W / 2, ""), ("agent", "PM", x[2] + W / 2, "提議"), ("agent", "repo", x[3] + W / 2, "升級"), ("PM", "repo", x[5] + W / 2, "同意擋")]
    return scenario("什麼時候：一道 check 裝好之後", "授權：升到擋要 PM 與 owner 請准", acts, flows,
        [("採用是階梯：只報告 → 警告 → 擋；每升一級都要證據，擋要 PM 與 owner 都同意。", True),
         ("沒有共識就停在警告；誤報多就退一級。", False)],
        "採用階梯：check 先只報告；團隊用一段時間看穩不穩；agent 附誤報率與抓到什麼提議升級；升到警告，submit 時提示不擋；PM 與 owner 都同意才擋 submit，而且留 bypass、有負責人。")


# ── 圖 8：日常看守 ──────────────────────────────────────────────────
def p_watch():
    x = xs(6)
    acts = [("工程團隊", x[0], W, "submit 一個 CL", ""),
            ("repo", x[1], W, "trigger 跑 sanity", "結果附 CL 號"),
            ("agent", x[2], W, "讀 description", "幾件事？目的？"),
            ("agent", x[3], W, "私訊一句", "看不出目的就問"),
            ("工程團隊", x[4], W, "回一句或照改", ""),
            ("agent", x[5], W, "壞了：先問原因", "再給修法")]
    flows = [("工程團隊", "repo", x[0] + W / 2, "submit"), ("repo", "agent", x[1] + W / 2, "結果"), ("agent", "工程團隊", x[3] + W / 2, "問一句"), ("agent", "工程團隊", x[5] + W / 2, "問原因")]
    return scenario("什麼時候：第一道 check 上線之後的常態；每一筆 submit 的 CL", "授權：自主（看、私訊）", acts, flows,
        [("監看看的是 CL 的 description、一包幾件事、check 的結果；看不出目的就 DM 一句並示範怎麼寫。", True),
         ("同一件事不重複念；壞了先問原因，可能是刻意的。", False)],
        "日常監看（上線後的常態）：工程師 submit 一個 CL；trigger 跑 sanity 結果附 CL 號；agent 看說明與結果，一包幾件事、看得出目的嗎；看不出目的就私訊一句並示範怎麼寫；工程師回一句或照改；壞了先問原因再給修法。",
        notes=["示意的私訊：「這包看起來是改 DMA 的 burst，對嗎？說明可以寫成：改了什麼／為什麼／怎麼驗，例如『加 burst 模式；為了 X；跑 t_dma_burst 過』。」"])


# ── 圖 9：開工輔導 ──────────────────────────────────────────────────
def p_kickoff():
    x = xs(6)
    acts = [("repo", x[0], W, "跡象", "open 多檔沒 submit"),
            ("agent", x[1], W, "私訊：在做 X 嗎？", "附線索"),
            ("工程團隊", x[2], W, "是，要做 DMA burst", ""),
            ("agent", x[3], W, "登記狀態板", "目的、範圍、做完的定義"),
            ("repo", x[4], W, "stream、check", "workspace 也備好"),
            ("工程團隊", x[5], W, "小包、併回", "shelve 給人看再併")]
    flows = [("repo", "agent", x[0] + W / 2, "看到"), ("agent", "工程團隊", x[1] + W / 2, "問"), ("工程團隊", "agent", x[2] + W / 2, "答"), ("agent", "repo", x[4] + W / 2, "準備"), ("repo", "工程團隊", x[5] + W / 2, "用")]
    return scenario("什麼時候：看到有人好像開了一件新工作", "授權：自主（問、準備）；登記要本人同意", acts, flows,
        [("看到跡象先問，說是才登記；登記時把做完的定義指到一個跑得起來的檢查。", True),
         ("用 Perforce 的詞輔導：stream、workspace、shelve、copy up；東西準備好交到他手上，一步不用查手冊。", False)],
        "開工輔導：repo 裡出現跡象，某人 open 多個檔沒 submit；agent 私訊問是不是在做某件事並附線索；工程師說是；agent 登記到狀態板，目的、範圍、做完的定義；在 repo 準備好 stream、workspace、check 交到他手上；工程師小包 submit、shelve 給人看、check 過了併回 main。",
        notes=["狀態板上每件任務：做什麼（一句）、誰、動哪些目錄、預計交什麼、在哪條 stream、到哪一步；看的是任務，不是人。"])


# ── 圖 10：透明 ─────────────────────────────────────────────────────
def p_transparent():
    x = xs(6)
    acts = [("agent", x[0], W, "每個動作寫日誌", "訊息、判斷、不確定的"),
            ("repo", x[1], W, "日誌、狀態板、地圖", "都在 depot"),
            ("agent", x[2], W, "定期一頁摘要", "做了什麼、發現什麼、等誰"),
            ("PM", x[3], W, "看摘要", "要細節就讀日誌"),
            ("工程團隊", x[4], W, "看得到關於自己的紀錄", "狀態板記任務不記人"),
            ("agent", x[5], W, "報告以模組為單位", "不排名、不用於考核")]
    flows = [("agent", "repo", x[0] + W / 2, "寫"), ("agent", "PM", x[2] + W / 2, "摘要"), ("repo", "工程團隊", x[4] + W / 2, "可讀")]
    return scenario("橫跨全程：一直都在", "授權：自主", acts, flows,
        [("agent 的日誌與狀態板放在 depot，PM 和工程師都讀得到；PM 平時看一頁摘要。", True),
         ("關於某人的紀錄那個人看得到；報告以模組和流程為單位，不排名個人。", False)],
        "透明：agent 每個動作、訊息、判斷寫日誌，和狀態板、PROJECT_MAP 一起放在 depot；定期給 PM 一頁摘要，PM 要細節就讀日誌；工程師看得到關於自己的紀錄；報告以模組為單位，不排名、不用於考核。")


# ── 圖 11：擱置、拒絕、誤報 ──────────────────────────────────────────
def p_friction():
    s = []
    scene(s, "橫跨全程：對方不想動、不同意，或 agent 錯了", "授權：延後可自己答應；被拒由 PM 裁決")
    cols = [("延後", WARN, [("工程團隊", "「這週趕 tape-out，先不動」"), ("agent", "好，tape-out 後再問；先標在地圖上"), ("repo", "記回訪的時點")]),
            ("被拒絕", WARN, [("工程團隊", "「我不認同這個 check」"), ("agent", "不裁決；整理證據與選項"), ("PM", "裁決")]),
            ("誤報", WARN, [("agent", "錯怪了一包 CL"), ("工程團隊", "在同一個 channel 更正"), ("repo", "一頁不究責的檢討")])]
    for i, (name, col, steps) in enumerate(cols):
        x = 20 + i * 284
        rect(s, x, 40, 272, 250, col=col, fill=col, op=".04", sw=1.3, dash="6 4")
        T(s, x + 14, 62, name, cls="tx", fill=col, w=700)
        for k, (who, what) in enumerate(steps):
            y = 78 + k * 66
            c = LANE_COL[who]
            pill(s, x + 14, y, who, c, h=20)
            T(s, x + 14, y + 40, what, fill=INK2)
            if k < 2:
                arrow(s, x + 40, y + 48, x + 40, y + 62, col=c, ar={"PM": "ar-p", "agent": "ar-a", "工程團隊": "ar", "repo": "ar-g"}[who], sw=1.2)
    T(s, 20, 312, "延後：嚴重度低、有期限的 agent 自己答應；嚴重度高、沒期限、一再延後的由 PM 裁決，而且對當事人透明。", fill=GRAY)
    bottom(s, 332, [
        ("工程師要延後可以談：聽理由、談折衷、記下什麼時候回來問；被拒絕就由 PM 裁決，agent 不裁決。", True),
        ("agent 錯了在同一個 channel 更正，寫一頁不究責的檢討。", False),
    ])
    aria = ("三欄。延後：工程師說這週趕 tape-out 先不動，agent 說好 tape-out 後再問並標在地圖上，repo 記回訪時點。"
            "被拒絕：工程師說不認同這個 check，agent 不裁決、整理證據與選項，PM 裁決。誤報：agent 錯怪了一包 CL，在同一個 channel 更正，repo 裡留一頁不究責的檢討。")
    return svg(s, 880, 480, aria)


# ── 圖 12：加強與退場 ───────────────────────────────────────────────
def p_exit():
    x = xs(6)
    acts = [("repo", x[0], W, "某道 check 穩定通過", "一段時間"),
            ("agent", x[1], W, "提議下一道", "附證據：為什麼現在加得起"),
            ("工程團隊", x[2], W, "同意，或先不要", ""),
            ("agent", x[3], W, "量趨勢", "六原則檢驗、四個指標"),
            ("工程團隊", x[4], W, "自己維護 pipeline", "做完的定義成了習慣"),
            ("agent", x[5], W, "只剩監看與維運", "交棒條件達成")]
    flows = [("repo", "agent", x[0] + W / 2, ""), ("agent", "工程團隊", x[1] + W / 2, "提議"), ("agent", "PM", x[3] + W / 2, "趨勢"), ("工程團隊", "agent", x[4] + W / 2, "交回")]
    return scenario("什麼時候：機制跑穩之後", "授權：加一道告知；交棒 PM 決定", acts, flows,
        [("一次只加一道，穩定了才加；量的是模組的趨勢，不是個人。", True),
         ("團隊自己維護 pipeline 之後，agent 只剩監看與維運；這就是交棒。", False)],
        "擴充與交棒：某道 check 穩定通過一段時間；agent 附證據提議下一道；團隊同意或先不要；agent 量六原則檢驗與四個指標的趨勢給 PM；團隊自己維護 pipeline 之後，agent 只剩監看與維運。",
        notes=["四個指標的 IC 版：submit 頻率、改動到進 main 的時間、check 失敗率、壞掉到修好的時間；以模組為單位。"])


PAGES = [
    ("總覽：PM 有決心沒經驗，團隊不堅決也不知怎麼做；agent 補這兩個缺", p_cover()),
    ("總表：每個階段誰做什麼、agent 的授權三級、用語定義", p_overview()),
    ("啟動：PM 給 depot 範圍與帳號，agent 以 bot 身分先只讀上線，先向團隊自我介紹", p_start()),
    ("盤點：agent 只讀掃指定的 depot 範圍，交 PM 一頁現況與幾個候選目標，PM 選", p_survey()),
    ("目標分析：agent 讀完才 DM owner 問只有他知道的事，答案進 PROJECT_MAP", p_analyze()),
    ("計畫核准：PM 核准方向、owner 同意範圍，缺一就不動手；PM 沒弄懂不算核准", p_approve()),
    ("建置：骨架做成 shelved CL 交 owner，缺的 check 寫需求讓人或 subagent 做", p_build()),
    ("上線分級：check 先只報告、再警告，PM 與 owner 同意才擋 submit，留 bypass", p_adopt()),
    ("日常監看：每筆 CL agent 讀 description 與 check，看不出目的就 DM 並示範寫法", p_watch()),
    ("有人開新工作：agent 察覺就先問，確認後登記狀態板、代開 stream 與 check", p_kickoff()),
    ("擴充與交棒：一次加一道 check，團隊能自己維護後 agent 只剩監看", p_exit()),
    ("橫跨全程：log 與狀態板都進 depot，PM 看一頁摘要，每人可查關於自己的紀錄", p_transparent()),
    ("橫跨全程：延後可以談，被拒絕由 PM 裁決，agent 錯了公開更正", p_friction()),
]

if __name__ == "__main__":
    build(NAME, "互動場景：agent 先讀懂再問、交 shelved CL；方向由 PM（導入 CI/CD 的負責人）核准，CL 收不收 owner 決定", KICKER, PAGES)

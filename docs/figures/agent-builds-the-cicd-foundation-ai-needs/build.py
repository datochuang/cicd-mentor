# -*- coding: utf-8 -*-
# 《AI agent 專案的目的》：docs/slides/agent-builds-the-cicd-foundation-ai-needs.{html,pdf}
# 執行：python3 docs/figures/agent-builds-the-cicd-foundation-ai-needs/build.py
#
# 讀者：公司內部的主管與決策者（sponsor 候選、部門主管、可能的 PM）。懂 IC 設計流程與 Perforce 基本用法，
#       不熟 CI/CD 與迭代式開發的細節，沒參與過這個專案的討論。
# 讀完要能：說出這個 agent 專案為什麼存在、要達成什麼、方向由誰掌握，並判斷要不要支持或擔任 PM。
# 主旨：CI/CD 是 AI 效益跨出組織疆界的地基；這個專案用一個自主運行、方向由人類 PM 掌握的 AI agent，把它在 IC 設計團隊建起來。
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lib"))
from slides import *

NAME = "agent-builds-the-cicd-foundation-ai-needs"
KICKER = "AI agent 專案的目的"


# ── 圖 1：整件事的地基 ───────────────────────────────────────────────
LAYERS = [
    ("公司競爭力", "更快、更可靠地交出晶片", "plain"),
    ("AI 效益跨出組織疆界", "AI 的產出跨團隊被信任、被採用", "plain"),
    ("迭代式開發", "tape-out 前小步改、頻繁整合", "plain"),
    ("CI/CD", "每個變更自動驗證，每個結果查得到版本", "gap"),
    ("本專案：CI/CD Mentor Agent", "AI agent 自主運行，人類 PM 掌握方向", "here"),
]


def p1():
    s = []
    T(s, 20, 20, "這份文件回答：這個 AI agent 專案為什麼存在、要達成什麼、方向由誰掌握 ↓", cls="tx-lbl", fill=INK2)
    cx, h, gap, y0 = 430, 54, 12, 44
    for i, (name, sub, kind) in enumerate(LAYERS):
        w = 300 + 80 * i
        x, y = cx - w / 2, y0 + i * (h + gap)
        if kind == "gap":
            rect(s, x, y, w, h, col=WARN, fill=WARN, op=".06", sw=1.6, dash="6 4")
            col = WARN
        elif kind == "here":
            rect(s, x, y, w, h, col=AGENT, fill=AGENT, op=".14", sw=2)
            col = AGENT
        else:
            rect(s, x, y, w, h, col="var(--rule-2)", fill="var(--surface-2)", sw=1.2)
            col = INK2
        T(s, cx, y + 23, name, cls="tx", anchor="middle", fill=col, w=700)
        T(s, cx, y + 42, sub, anchor="middle", fill=INK2 if kind != "plain" else GRAY)
    y_gap = y0 + 3 * (h + gap)
    y_here = y0 + 4 * (h + gap)
    # 缺口標記
    pill(s, cx - 270 - 12, y_gap + 17, "目前缺這一層", WARN, anchor="end")
    # 本專案把缺的那層建起來
    path(s, "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (cx + 310 + 4, y_here + h / 2, cx + 380, y_here + h / 2,
                                                         cx + 380, y_gap + h / 2, cx + 270 + 8, y_gap + h / 2),
         col=AGENT, ar="ar-a", sw=2)
    T(s, cx + 388, y_gap + h + 10, "把它建起來", cls="tx", fill=AGENT, w=700)
    # 依賴方向
    arrow(s, 40, y_here + h, 40, y0 + 4, col=GRAY, ar="ar-gray", sw=1.2)
    T(s, 50, y0 + 14, "上層", fill=GRAY)
    T(s, 50, y_here + h - 4, "下層撐住上層", fill=GRAY)
    yb = y_here + h + 30
    line(s, 20, yb, 860, yb)
    T(s, 20, yb + 26, "AI 的效益要跨出個人與單一團隊，它的產出必須能被機器驗證、查得到來源，CI/CD 正是做這件事的那一層。",
      cls="tx", fill=INK2, w=600)
    T(s, 20, yb + 50, "公司 IC 設計團隊的版控多半只當作備份，這一層幾乎是空的。", cls="tx", fill=INK2)
    aria = ("五層的依賴圖，由上而下：公司競爭力、AI 效益跨出組織疆界、迭代式開發、CI/CD、本專案。"
            "CI/CD 那層以虛線標示為目前缺的一層；最底下的本專案以箭頭指向 CI/CD，表示本專案要把它建起來。")
    return svg(s, 880, 480, aria)


PAGES = [
    ("目的：在 IC 設計團隊建起 CI/CD，讓 AI 的效益跨出組織疆界", p1()),
]

if __name__ == "__main__":
    build(NAME, "AI agent 專案的目的", KICKER, PAGES)

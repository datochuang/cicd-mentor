# CI/CD Mentor Agent

在 IC 設計團隊導入迭代式開發與 CI/CD 的 AI agent 構想。Agent 自主運行，方向由一位人類 PM 掌握：PM 決定要去哪裡，agent 補上 CI/CD 的知識與執行力，兩邊一起把事情做成。

PDF 版：[docs/slides/ai-agent-and-pm-make-cicd-happen.pdf](docs/slides/ai-agent-and-pm-make-cicd-happen.pdf)

![方向：迭代式開發加 CI/CD，是 AI 效益跨出組織疆界的地基](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-1.png)

![背景：CI/CD 預設的軟體業界習慣，IC 設計團隊多半沒有](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-2.png)

![心態：認同方向，卻懷疑非做不可、懷疑做得到](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-3.png)

![推動者：知道要去哪裡，不知道第一步怎麼走](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-4.png)

![搭配：AI 補上知識與執行力，PM 掌舵，各補對方的缺](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-5.png)

![協作：agent 自主地轉循環，方向由 PM 理解後核准](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-6.png)

## 這個 repo 裡有什麼

目前是規劃階段，還沒有 agent 的程式碼。

| 位置 | 內容 |
|---|---|
| [direction.md](direction.md) | 目前有效的整體構想、設計要點、未決問題 |
| [decision-log.md](decision-log.md) | 每個決定的日期、理由、取代了什麼 |
| [research/](research/) | 業界實踐與類比分析等參考資料，附來源 |
| [docs/slides/](docs/slides/) | 上面這份圖形文件的 HTML 與 PDF |

上面的圖由 `python3 docs/figures/ai-agent-and-pm-make-cicd-happen/build.py` 產生（需要 Google Chrome 與 poppler）。

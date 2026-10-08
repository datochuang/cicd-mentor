# 背景

我是一家 IC 設計公司的技術主管，負責導入各種 Agentic AI 來提升公司的開發效率與整體競爭力。經過上一層目錄（`../`，即 claude_workspace）底下眾多專案的探索，我認為目標應該定為導入迭代式開發，AI 的效益才能打破組織既有疆界與流程的限制，而 CI/CD 在技術上不可或缺。

公司 IC 設計相關的工程部門沒有 CI/CD 的觀念與實踐。Version control（以 Perforce 為主）幾乎被當成單純的檔案備份工具，頂多搭配打 label/tag，只有極少數流程會 trigger sanity check，僅此而已。

我想設計一個自主運行的 CI/CD mentor agent：持續掃描 version control repo，檢視既有與新增的 artifact。這個 agent 具備比工程師更好的 CI/CD 觀念與各種 programming/scripting 技能，透過 Slack 或 mail 等工具，及時找出整個 repo 的問題並提出建議，必要時甚至協助實作。

# 產出

這個專案目前用來讓我與你（Claude Code）討論整體規劃，並推演可能的部署與實作方式。最終目標是產出一份完整的計劃文件，讓我帶到公司的工程內網繼續開發這個 agent。

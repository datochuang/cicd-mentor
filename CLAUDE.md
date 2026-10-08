# 背景

我是一家 IC 設計公司的技術主管，負責導入各種 Agentic AI 來提升公司的開發效率與整體競爭力。經過上一層目錄（`../`，即 claude_workspace）底下眾多專案的探索，我認為目標應該定為導入迭代式開發，AI 的效益才能打破組織既有疆界與流程的限制，而 CI/CD 在技術上不可或缺。

公司 IC 設計相關的工程部門沒有 CI/CD 的觀念與實踐。Version control（以 Perforce 為主）幾乎被當成單純的檔案備份工具，頂多搭配打 label/tag，只有極少數流程會 trigger sanity check，僅此而已。

我想設計一個自主運行的 CI/CD mentor agent：持續掃描 version control repo，檢視既有與新增的 artifact。這個 agent 具備比工程師更好的 CI/CD 觀念與各種 programming/scripting 技能，透過 Slack 或 mail 等工具，及時找出整個 repo 的問題並提出建議，必要時甚至協助實作。

# 產出

這個專案目前用來讓我與你（Claude Code）討論整體規劃，並推演可能的部署與實作方式。最終目標是產出一份完整的計劃文件，讓我帶到公司的工程內網繼續開發這個 agent。

# 目前方向

上面「背景」描述的是最初的構想，已經修正：**agent 自主運行，但方向由一位人類 PM 決定**。Agent 不眠不休地主動發現問題、構思方案、與工程師溝通、產出技術成果；它形成的決定和方針要主動向 PM 匯報，確認 PM 真的理解之後由 PM approve。Agent 同時幫 PM 成長，並提供團隊的 holistic view。細節以 [direction.md](direction.md) 為準。

`../cicd-introduction-and-promotion/cicd-mentor-guide/` 是較早的相關成果，只供參考，不是這個專案的起點或預設前提。

# 文件結構

- `direction.md`：目前有效的整體構想、設計要點、未決問題。持續更新
- `decision-log.md`：依日期記錄的決定、理由、取代了什麼。只增不改
- `research/`：討論時整理的參考資料（業界實踐、類比分析等），附來源

# 維護規則

- 我做出新決定或改變想法時：在 `decision-log.md` 新增一筆，並同步更新 `direction.md`
- 討論中值得保留的分析與調查，整理到 `research/`，並在相關決定中連結
- 只有在文件結構或工作規則改變時才更新這份 CLAUDE.md

# 撰寫原則

- 不捏造統計數字或案例，範例標明是示意；引用外部資料要附來源
- 最終計劃要能單獨帶進公司內網，那裡看不到這個 workspace，不能依賴 `../` 路徑才讀得懂

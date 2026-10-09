# 待辦與擱置的議題

討論中被岔開、還沒有結論、或等待決定的事都記在這裡，是唯一的清單。編號不重複使用；完成的移到最下面「已結束」，註明結果與對應的決定（D 編號）或 commit。

---

## 等你決定

| # | 加入 | 議題 | 現況／下一步 | 相關 |
|---|---|---|---|---|
| T1 | 10-08 | **PM 是誰？** 你本人，還是另一個人 | 問過多次還沒回答。答案會影響「觀念不準」的程度、實權大小、授權表要多保守 | direction.md |
| T2 | 10-08 | **方針層與執行層的界線**：哪些事 agent 自己做、哪些先告知 PM、哪些只有 PM 能做（授權表） | 只列了大方向，要逐項訂 | direction.md 設計要點 6 |
| T3 | 10-08 | **Sponsor 與試點團隊的對口人**是誰 | 未討論 | research/consulting-analogy.md |
| T4 | 10-08 | **試點團隊與範圍**怎麼選 | 建議挑自願的團隊、一個專案、一兩種高價值檢查；未討論 | research/industry-practices-and-risks.md |
| T5 | 10-08 | **資安與 IP**：design 資料能否交給 LLM、用哪種模型與部署方式；agent 在版控上用誰的身分、有哪些權限 | 未討論，可能最早卡關 | research/industry-practices-and-risks.md |
| T6 | 10-08 | **成功指標**怎麼定 | 圖形文件只有方向示意，具體指標與門檻未定 | |
| T23 | 10-09 | **情勢判斷（U1）的報告形式與預算** | PM 想看一頁還是一份；時間與算力的預算誰給 | agent-operating-model.md 情勢判斷 |
| T24 | 10-09 | **目標分析的計畫要誰同意**：只 PM 核准，還是 owner 也要同意才動他的範圍 | 我的建議：兩個都要 | agent-operating-model.md 目標分析 |
| T25 | 10-09 | **agent 在 slack／mail 與 Perforce 上的身分**：bot 帳號代表 PM，還是用 PM 或工程師的名義 | 我強烈建議 bot 帳號＋「代表 PM」；和 T5 綁在一起 | agent-operating-model.md 訪談關係人、啟動與身分 |
| T26 | 10-09 | **agent 什麼情況可以自己 submit；擋 submit 的條件** | 是 T2 授權表的核心；初稿：只動自己的 script 目錄可自己 submit；擋 submit 要 PM 與 owner 同意、有 bypass | agent-operating-model.md 建置機制、透明與授權 |
| T27 | 10-09 | **退場的條件**：某個目標什麼時候算交回團隊 | 未討論 | agent-operating-model.md 退場 |
| T28 | 10-09 | **Perforce 的 branch 模型**：stream 還是傳統 branch spec；一任務一條還是一人一條 | 輔導開工要照這個模型準備 stream／workspace | agent-operating-model.md 任務掌控與開工輔導 |
| T29 | 10-09 | **跨 workspace 的活動資訊可不可以看**（誰 open 了什麼、pending 的 CL）；怎麼告知團隊 agent 看得到 | 開工跡象的主要來源，但最容易被當成監視 | agent-operating-model.md 任務掌控與開工輔導 |
| T30 | 10-09 | **任務的來源**：公司有沒有 ticket／任務系統可接；沒有的話模組狀態板是不是唯一登記處 | | agent-operating-model.md 任務掌控、任務的來源 |
| T31 | 10-09 | **做法層的七條 practice 等你確認**：Test-first、Executable spec、Evidence-based delivery、Definition of Done、Flow as code、Blameless postmortem、量化 | 你問要不要加 TDD、evidence-based delivery、executable spec 讓 agent 的行為有依據；我提了七條並列了不納入的；每條有「agent 自己／推動團隊／檢驗」 | agent-operating-model.md 依據 |
| T7 | 10-08 | **轉型的終點**：流程存在就好，還是要團隊真正理解並自己維護 | D2 給了初步答案（先改變 PM，由他帶動團隊），細節待討論 | decision-log.md D2 |
| T15 | 10-08 | **目錄用途與相依關係沒有文件，對 agent 設計的影響**：通用 agent 每個 workspace 都要另寫指引，那這個 agent 要不要自己建立並維護每個專案的目錄說明與相依關係（並放進版控）？ | 你在討論第二份圖形文件時提出這個問題；只寫進了文件第 7 頁，還沒討論對 agent 本身的設計意涵 | docs/slides/repo-as-backup-keeps-files-not-answers.pdf 第 7 頁 |

## 等你確認的產出

| # | 加入 | 項目 | 現況／下一步 | 相關 |
|---|---|---|---|---|
| T8 | 10-08 | 圖形文件第 3 頁的「會被盯上嗎？」 | 我根據討論加的，你沒明確提過；確認要不要保留 | docs/slides/ai-agent-and-pm-make-cicd-happen.pdf |
| T9 | 10-08 | 圖形文件第 6 頁「對的掌舵人」四個條件 | 我歸納的，確認是否符合你心中的人選 | 同上 |
| T10 | 10-08 | 圖形文件要不要做盲讀驗收 | 派沒看過討論的 subagent 扮成讀者只讀 PDF，回報看不懂的地方 | |
| T11 | 10-08 | 舊文字版說明文件的 Artifact 連結要不要刪 | 檔案已移到 docs/archive/；連結 https://claude.ai/artifact/GqNg8P9QN569RFvVhb1Yme 仍在 | |
| T17 | 10-09 | 圖形文件《第一次進 workspace：照五個原則檢查，不過就先補一版》初稿等你修正 | 九頁（10-09 晚上加了 SSOT 第二頁：產物、flow、IP；Code review 一頁；分工頁加了對應項目）。特別要看：六個檢查的順序、每頁「先補什麼」的 patch 名單、第 9 頁三類分工與「owner 採用才進 depot」這個預設 | docs/slides/check-then-patch-before-asking-owner.pdf |
| T19 | 10-09 | **第六個原則 Code review**（併入前有人看過並留紀錄）等你確認 | 追加的「沒有 review」「resolve 整份收下」兩頁掛不進原來五個：CI 是機器把關，review 是人把關，對策不同。已寫進圖形文件收斂頁、direction.md、檢查文件第 7 頁；不採用的話這三處要改 | direction.md 定錨點 |
| T20 | 10-09 | **《把版控當備份的團隊》p4–p16 冒號前全是「問題」**，審稿說 13 頁下來那格沒有資訊，建議改放原則名或分組詞 | 我沒動，因為這會改變「主題：結論」裡主題詞的用法。我的建議：改成「問題（Traceability）：…」這種形式，讀者翻到收斂頁前就看過六個詞；你決定 | docs/reviews/titles-blind-read-20261009.md |
| T21 | 10-09 | 圖形文件《為什麼非要 CI/CD：查和判不交給機器，N 個 agent 等於一個》初稿等你修正 | 十一頁。2026-10-09 深夜依你「順序不通順」重排：脊椎是三層套疊的迴圈。1 總覽（三種效益站在 CI/CD 地基上，地基現在是空的；一頁看完整個主張）→ 2–4 內圈（定義、在 IC 排成幾道檢查、現狀）→ 5–6 中圈（迭代進 main、交接）→ 7 外圈 → 8–9 AI（三層都加速改、瓶頸在判；上限）→ 10 結論 → 11 對應。特別要看：第 1 頁那張三層的表對不對、第 6 頁 agent 接得了／接不了的那段、第 7 頁 DSO.ai 的引用與「前提是推論」、第 9 頁三個上限 | docs/slides/loops-need-cicd-before-ai-multiplies.pdf；research/loops-and-ai-multiplier.md |
| T22 | 10-09 | **前三份圖形文件要不要照新規則補一頁總結** | 「第 1 頁一頁講完主張」的規則是做第四份時才定的；前三份（agent 與 PM、把版控當備份、進到陌生 workspace）的第 1 頁仍是鋪陳式開頭 | CLAUDE.md 圖形化文件的規則 |
| T18 | 10-09 | **CI 原則的意思補了「共用的 main 隨時可用」「結果由機器寫下」**（D4 微調） | 加「沒有 branch」那頁時，它的危害要掛到 CI 上，原本的定義只講「改動進來時被檢查」，沒講檢查的目的是讓 main 隨時可用。請確認這個補法，不然就要考慮第六個原則 | direction.md 定錨點 |
| T14 | 10-08 | 圖形文件《把版控當備份的團隊》初稿等你修正 | 十八頁全部是我創作的（10-09 晚上追加圖 9–16：沒有 review、resolve 整份收下、產物進 depot、IP 解壓覆蓋、flow 複製、兩台機器結果不同、Excel 狀態表、退不回去）。情境與細節都要你對照實際狀況修正 | docs/slides/repo-as-backup-keeps-files-not-answers.pdf |

## 其他

| # | 加入 | 項目 | 現況／下一步 | 相關 |
|---|---|---|---|---|
| T13 | 10-08 | `../google-xls` 的投影片規則要不要複製進本 repo | CLAUDE.md 引用了外部路徑，別人 clone 後找不到 | CLAUDE.md |

---

## 已結束

| # | 結束 | 議題 | 結果 |
|---|---|---|---|
| T12 | 10-08 | 推上 GitHub 前檢查公開範圍 | 使用者說明 repo 是個人專用，不需檢查；已推上 datochuang/cicd-mentor |
| T16 | 10-09 | 五個定錨原則等你確認 | 全部同意，改用英文專有名詞：Small batches、SSOT、Traceability、CI、Self-documenting。記為 D4 |

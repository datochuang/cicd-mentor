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
| T23 | 10-09 | **情勢判斷的報告形式與預算** | PM 想看一頁還是一份；時間與算力的預算誰給 | agent-operating-model.md 情勢判斷 |
| T24 | 10-09 | **目標分析的計畫要誰同意**：只 PM 核准，還是 owner 也要同意才動他的範圍 | 我的建議：兩個都要 | agent-operating-model.md 目標分析 |
| T25 | 10-09 | **agent 在 slack／mail 與 Perforce 上的身分**：bot 帳號代表 PM，還是用 PM 或工程師的名義 | 我強烈建議 bot 帳號＋「代表 PM」；和 T5 綁在一起 | agent-operating-model.md 訪談關係人、啟動與身分 |
| T26 | 10-09 | **agent 什麼情況可以自己 submit；擋 submit 的條件** | 是 T2 授權表的核心；初稿：只動自己的 script 目錄可自己 submit；擋 submit 要 PM 與 owner 同意、有 bypass | agent-operating-model.md 建置機制、透明與授權 |
| T27 | 10-09 | **退場的條件**：某個目標什麼時候算交回團隊 | 未討論 | agent-operating-model.md 退場 |
| T28 | 10-09 | **Perforce 的 branch 模型**：stream 還是傳統 branch spec；一任務一條還是一人一條 | 輔導開工要照這個模型準備 stream／workspace | agent-operating-model.md 任務掌控與開工輔導 |
| T29 | 10-09 | **跨 workspace 的活動資訊可不可以看**（誰 open 了什麼、pending 的 CL）；怎麼告知團隊 agent 看得到 | 開工跡象的主要來源，但最容易被當成監視 | agent-operating-model.md 任務掌控與開工輔導 |
| T30 | 10-09 | **任務的來源**：公司有沒有 ticket／任務系統可接；沒有的話模組狀態板是不是唯一登記處 | | agent-operating-model.md 任務掌控、任務的來源 |
| T33 | 10-09 | **版控常規清單**：最缺、最該先教的三件是哪三件；Git 團隊要不要另一張對照表 | 我列了十一條（一包一件事、說明寫目的、改前 sync、resolve 要看、shelve 給人看、用 stream 不複製目錄、產物不進 depot、檔案進 depot 才算存在、label 附 manifest、workspace 乾淨、IP drop 走流程），建議先教前三件 | agent-operating-model.md 教育版控的常規 |
| T34 | 10-09 | **PM 要先談好的資源與人**（帳號權限、trigger 權限、算力與 license、結果放哪、資安、HR 不考核、sponsor、試點 owner）誰去談、先談哪個 | 這些 agent 變不出來；是啟動前的 checklist | agent-operating-model.md 7.2 |
| T35 | 10-09 | **分階段路線圖與每階段的成功定義、停損**要不要照我寫的 | 準備 → 試點 → 擴散 → 常態；試點的成功：owner 採用了 shelved CL、check 每天跑有人看、至少一個檢驗從做不到變做得到 | agent-operating-model.md 7.3 |
| T36 | 10-09 | **紅線清單**（不刪、不碰別人 workspace、沒共識不擋、不報個人活動量、design 資料不出核准的模型、不假裝是人、不對 design 下判斷）有沒有要加減 | | agent-operating-model.md 7.4 |
| T37 | 10-09 | **啟動包的目錄與缺件**（README、啟動包版 CLAUDE.md、乾淨版行為指導原則、build brief、沙盒驗收、模板、PM 手冊、open decisions、用語表、獨立性檢查）要不要照 starter-kit-plan.md 做 | 內容面大致齊了，缺的是包裝層；做之前要先定 T19、T31 | starter-kit-plan.md |
| T38 | 10-09 | **agent 自己的版控與多實例**：core 由誰維護、一實例一帳號還是共用、升級的節奏 | 三層分離（core／實例的工作區／生產用的工具）、登記表、實例名與版號署名、沙盒當 core 的 regression、換手已寫進 operating model 第八節，並做成投影片《agent 自己的版控》；這三件要公司決定 | agent-operating-model.md 第八節、docs/slides/agent-own-version-control-and-instances.pdf |
| T41 | 10-09 | **前五份投影片的檔名要不要照新規則改**（檔名講問題不講答案）：ai-agent-and-pm-make-cicd-happen、repo-as-backup-keeps-files-not-answers、check-then-patch-before-asking-owner、loops-need-cicd-before-ai-multiplies、agent-fills-what-pm-and-team-lack | 你只點名了《agent 自己的版控》那份，已改成 agent-own-version-control-and-instances；其餘五份沿用舊名，改的話 README、reviews、圖目錄一起動 | CLAUDE.md 圖形化文件的規則 |
| T7 | 10-08 | **轉型的終點**：流程存在就好，還是要團隊真正理解並自己維護 | D2 給了初步答案（先改變 PM，由他帶動團隊），細節待討論 | decision-log.md D2 |
| T15 | 10-08 | **目錄用途與相依關係沒有文件，對 agent 設計的影響**：通用 agent 每個 workspace 都要另寫指引，那這個 agent 要不要自己建立並維護每個專案的目錄說明與相依關係（並放進版控）？ | 你在討論第二份圖形文件時提出這個問題；只寫進了文件第 8 頁（加總覽頁後的頁碼），還沒討論對 agent 本身的設計意涵 | docs/slides/repo-as-backup-keeps-files-not-answers.pdf 第 8 頁 |

## 等你確認的產出

| # | 加入 | 項目 | 現況／下一步 | 相關 |
|---|---|---|---|---|
| T8 | 10-08 | 圖形文件第 3 頁的「會被盯上嗎？」 | 我根據討論加的，你沒明確提過；確認要不要保留 | docs/slides/ai-agent-and-pm-make-cicd-happen.pdf |
| T9 | 10-08 | 圖形文件第 6 頁「對的掌舵人」四個條件 | 我歸納的，確認是否符合你心中的人選 | 同上 |
| T10 | 10-08 | 圖形文件要不要做盲讀驗收 | 派沒看過討論的 subagent 扮成讀者只讀 PDF，回報看不懂的地方 | |
| T11 | 10-08 | 舊文字版說明文件的 Artifact 連結要不要刪 | 檔案已移到 docs/archive/；連結 https://claude.ai/artifact/GqNg8P9QN569RFvVhb1Yme 仍在 | |
| T17 | 10-09 | 圖形文件《第一次進 workspace：照五個原則檢查，不過就先補一版》初稿等你修正 | 九頁（10-09 晚上加了 SSOT 第二頁：產物、flow、IP；Code review 一頁；分工頁加了對應項目）。特別要看：六個檢查的順序、每頁「先補什麼」的 patch 名單、第 9 頁三類分工與「owner 採用才進 depot」這個預設 | docs/slides/check-then-patch-before-asking-owner.pdf |
| T43 | 10-09 | **D7 之後的投影片修改**（等七件決定完一次做，免得重建好幾次）：《把版控當備份的團隊》第 1 頁的 Code review 框併進 Self-documenting、第 10 頁改成「沒講好要不要 review」、第 19 頁改五列；《進到陌生 workspace》第六個檢查改成「目錄有沒有講好要不要 review，沒講就問 owner 定一個」、標題的「六個原則」改五個；《agent 自己的版控》第 3 頁的表改五列加 review 規矩；《為什麼非要 CI/CD》第 8、11 頁的「六個原則」改五個；《互動場景》裡提到的地方；README 的 alt 一起改 | 文字文件（direction、operating model、starter-kit-plan、decision-log D7）已改 | decision-log.md D7 |
| T20 | 10-09 | **《把版控當備份的團隊》p4–p16 冒號前全是「問題」**，審稿說 13 頁下來那格沒有資訊，建議改放原則名或分組詞 | 我沒動，因為這會改變「主題：結論」裡主題詞的用法。我的建議：改成「問題（Traceability）：…」這種形式，讀者翻到收斂頁前就看過六個詞；你決定 | docs/reviews/titles-blind-read-20261009.md |
| T21 | 10-09 | 圖形文件《為什麼非要 CI/CD：查和判不交給機器，N 個 agent 等於一個》初稿等你修正 | 十一頁。2026-10-09 深夜依你「順序不通順」重排：脊椎是三層套疊的迴圈。1 總覽（三種效益站在 CI/CD 地基上，地基現在是空的；一頁看完整個主張）→ 2–4 內圈（定義、在 IC 排成幾道檢查、現狀）→ 5–6 中圈（迭代進 main、交接）→ 7 外圈 → 8–9 AI（三層都加速改、瓶頸在判；上限）→ 10 結論 → 11 對應。特別要看：第 1 頁那張三層的表對不對、第 6 頁 agent 接得了／接不了的那段、第 7 頁 DSO.ai 的引用與「前提是推論」、第 9 頁三個上限 | docs/slides/loops-need-cicd-before-ai-multiplies.pdf；research/loops-and-ai-multiplier.md |
| T22 | 10-09 | **前三份圖形文件要不要照新規則補一頁總結** | 「第 1 頁一頁講完主張」的規則是做第四份時才定的；前三份（agent 與 PM、把版控當備份、進到陌生 workspace）的第 1 頁仍是鋪陳式開頭 | CLAUDE.md 圖形化文件的規則 |
| T32 | 10-09 | 圖形文件《互動場景》初稿等你修正 | 十二頁，泳道圖；每頁的「什麼時候」「授權」和示意的訊息例句都是我寫的 | docs/slides/agent-fills-what-pm-and-team-lack.pdf |
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
| T39 | 10-09 | 《agent 自己的版控》第 3–10 頁照 D5 改、加「換手」一頁、換手的接法誰選 | 接法由 PM 選（使用者：「這很明顯」）。全份十一頁已照 D5 改，第 5 頁換手；檔名改為 agent-own-version-control-and-instances；標題再盲讀一次（docs/reviews/titles-blind-read-agent-versioning-20261009.md 第二輪） |
| T31 | 10-09 | 做法層八條等你確認 | 照提案全採用：Test-first、Executable spec、Evidence-based delivery、Definition of Done、Flow as code、Blameless postmortem、量化（DORA 四指標 IC 版）、Review policy per directory。記為 D8 |
| T19 | 10-09 | 第六個原則 Code review | 不採用。使用者：review 非必要，由各 design 自行決定、過程中可變，定成規矩「每個目錄都要講好需不需要 code review」，掛在 Self-documenting，做法層加 Review policy per directory。記為 D7 |
| T18 | 10-09 | CI 的意思補「結果由機器寫下；共用的 main 隨時可用」 | 使用者同意。記在 D7 |
| T42 | 10-09 | 實例小版號的定義 | 照我的理解：core 版號後面加一位，實例每次把工作區 merge 回 master 就加一（agent-dma v0.3.2）。記為 D6 |
| T40 | 10-09 | D5 影響的舊投影片要改 | 照我的判斷做了：《agent 補 PM 與團隊各缺的》第 2 頁用語、第 3 頁啟動（目標的 repo 只被讀，紀錄在 agent 的 repo）、第 6 頁（決定記在 agent 的 repo）、第 12 頁（log 與狀態板在 agent 的 repo、團隊可讀，副本進 depot 由 owner 定）；《進到陌生 workspace》講的是 setup script、manifest 這類生產用的東西進 depot，符合 D5，不用改 |

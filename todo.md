# 待辦與擱置的議題

討論中被岔開、還沒有結論、或等待決定的事都記在這裡，是唯一的清單。編號不重複使用；完成的移到最下面「已結束」，註明結果與對應的決定（D 編號）或 commit。

---

## 等你決定

| # | 加入 | 議題 | 現況／下一步 | 相關 |
|---|---|---|---|---|
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
| T38 | 10-09 | **agent 自己的版控與多實例**：core 由誰維護、一實例一帳號還是共用、升級的節奏 | 三層分離（core／實例的工作區／生產用的工具）、登記表、實例名與版號署名、沙盒當 core 的 regression、換手已寫進 operating model 第八節，並做成投影片《agent 自己的版控》；這三件要公司決定 | agent-operating-model.md 第八節、docs/slides/agent-own-version-control-and-instances.pdf |
| T7 | 10-08 | **轉型的終點**：流程存在就好，還是要團隊真正理解並自己維護 | D2 給了初步答案（先改變 PM，由他帶動團隊），細節待討論 | decision-log.md D2 |
| T15 | 10-08 | **目錄用途與相依關係沒有文件，對 agent 設計的影響**：通用 agent 每個 workspace 都要另寫指引，那這個 agent 要不要自己建立並維護每個專案的目錄說明與相依關係（並放進版控）？ | 你在討論第二份圖形文件時提出這個問題；只寫進了文件第 8 頁（加總覽頁後的頁碼），還沒討論對 agent 本身的設計意涵 | docs/slides/team-treating-vc-as-backup.pdf 第 8 頁 |

## 等你確認的產出

| # | 加入 | 項目 | 現況／下一步 | 相關 |
|---|---|---|---|---|
| T10 | 10-08 | 圖形文件要不要做盲讀驗收 | 派沒看過討論的 subagent 扮成讀者只讀 PDF，回報看不懂的地方 | |
| T47 | 10-10 | 圖形文件《agent 的基本模塊》初稿等你修正 | 八頁。十七個模塊的名字、分組（看判做說守）、規格句、進出、沙盒怎麼驗、第 8 頁階段對模塊的表都是我提的；D13 定它們是建議、邊做邊調。特別要看：第 1 頁「沒拆會怎樣」四條、第 3 頁「乾淨環境重現」是不是你舉的例子的意思、第 7 頁「公司專屬的三樣」夠不夠 | docs/slides/agent-capability-modules.pdf；docs/reviews/titles-blind-read-capability-modules-20261010.md |

## 其他

| # | 加入 | 項目 | 現況／下一步 | 相關 |
|---|---|---|---|---|

---

## 已結束

| # | 結束 | 議題 | 結果 |
|---|---|---|---|
| T20 | 10-10 | 《把版控當備份的團隊》第 5–17 頁冒號前的「問題」 | 使用者選「換成原則名」：Traceability、CI、Self-documenting、Small batches、SSOT，掛兩個原則的頁用 sixteen-problems.md 排第一的；第 2–4 頁「日常／散落／交付」不動。README alt 與啟動包 02-diagnosis 的 PDF、PNG 同步 |
| T21 | 10-10 | 圖形文件《為什麼非要 CI/CD》逐頁修正 | 不審（使用者）。它是論述，D15 之後不會卡 agent |
| T32 | 10-10 | 圖形文件《互動場景》逐頁修正 | 不審（使用者）。每頁的時機、授權、訊息例句 D15 已列為參考範例 |
| T17 | 10-10 | 圖形文件《進到陌生的 workspace》逐頁修正（順序、先補什麼的名單、三類分工） | 不審。使用者：T17 也僅能當成參考範例，務必讓新 agent 知道；不希望這裡的發想（某種程度是空想）把 agent 的功能和思維卡死。記為 D15（通則：啟動包分清楚規則與參考範例，CLAUDE.md 列清單）；第 1 頁加一行說明 |
| T14 | 10-10 | 圖形文件《把版控當備份的團隊》逐頁對照實際狀況修正 | 不審。使用者：對現狀的具體描述只是起提醒的作用，讓團隊把 high level 的敘述連結到自己的日常行為；情境是示意，不是現況的審計。記為 D14。T20（冒號前的「問題」要不要改成原則名）仍開著 |
| T46 | 10-10 | agent 的能力拆成可復用的基本模塊 | 使用者提出，先做投影片《agent 的基本模塊》（八頁，標題盲讀一輪：契約→規格、綁定→公司專屬的三樣、三態→三種結果），再 merge 回文件。使用者定：要模組化、要分層、怎麼切是規則，哪些模塊、介面長怎樣是建議、邊做邊調。記為 D13；operating model 第一節第九輪與第九節、行為原則 #25、direction 設計要點 10、README、啟動包 07-capabilities.md 與連帶 |
| T12 | 10-08 | 推上 GitHub 前檢查公開範圍 | 使用者說明 repo 是個人專用，不需檢查；已推上 datochuang/cicd-mentor |
| T16 | 10-09 | 五個定錨原則等你確認 | 全部同意，改用英文專有名詞：Small batches、SSOT、Traceability、CI、Self-documenting。記為 D4 |
| T39 | 10-09 | 《agent 自己的版控》第 3–10 頁照 D5 改、加「換手」一頁、換手的接法誰選 | 接法由 PM 選（使用者：「這很明顯」）。全份十一頁已照 D5 改，第 5 頁換手；檔名改為 agent-own-version-control-and-instances；標題再盲讀一次（docs/reviews/titles-blind-read-agent-versioning-20261009.md 第二輪） |
| T45 | 10-09 | D12 的連帶 | 做了：五份投影片（總覽與原則頁加 CD、進到陌生 workspace 第 7 個檢查 CD、互動場景第 9 頁交付、中圈交接點名 CD、core 的 release 流程）；啟動包同步（04 加 CD 與 Release pipeline、05 #34、06 八個概念、07 元件與第 7 步、glossary、十六種問題的掛法、deliverable 模板、09 #24 取用處、10 的 D12）；README 頁數與 alt |
| T44 | 10-09 | 啟動包的驗收 | 乾淨 context 的 subagent 扮內網 Claude Code 讀完 26 份 .md 與 15 張 PNG，回報五大項（沙盒輸入不在 .md、授權矛盾、讀序與第一步接不上、包外引用、用語打架）；全部照改：加 02-diagnosis/sixteen-problems.md、授權定版（agent 不 submit、計畫核准前只交新增檔、超預算先停再請示）、builder 唯一讀序、MVP 對到階段、D11 註記、glossary 補 workspace 三義等、模板加 config／people／decisions；投影片沙盒頁的十六種對齊頁序 |
| T43 | 10-09 | D7 之後的投影片修改 | 做了：《把版控當備份的團隊》第 1、10、19 頁（五個框、沒講好要不要 review、五列加一句註）；《進到陌生 workspace》第 1、7 頁（第五個檢查改 review 規矩）與文件標題；《agent 自己的版控》第 3 頁；《為什麼非要 CI/CD》第 1、8、11 頁；《互動場景》六原則改五原則；README 的 alt 從各份標題重產 |
| T8 | 10-08 | 心態頁「會被盯上嗎？」那列 | 使用者說不需要，拿掉；該頁剩三列 |
| T9 | 10-08 | 「對的掌舵人」四個條件 | 使用者 ok；D9 之後這四條就是「誰能接 PM」的門檻 |
| T22 | 10-09 | 前三份圖形文件要不要照新規則補總覽頁 | 《把版控當備份的團隊》《AI agent 與人類 PM 搭檔》各補了一張圖的總覽當第 1 頁；《進到陌生 workspace》第 1 頁本來就是流程總覽。六份的第 1 頁現在都是一頁講完主張 |
| T13 | 10-08 | 投影片規則引用 ../google-xls | 不複製進來：內網 agent 的新 repo 不需要這個規則，啟動包也不帶產生器；本 workspace 的 CLAUDE.md 照舊引用（D10） |
| T11 | 10-08 | 舊文字版的 claude.ai 連結 | 刪了；那個連結只剩這一列記著，連這一列一起收掉 |
| T41 | 10-09 | 前五份投影片的檔名照新規則改 | 改了：why-cicd-needs-ai-agent-and-pm、team-treating-vc-as-backup、agent-entering-unknown-workspace、loops-and-ai-multiplier、agent-pm-team-repo-interactions；圖目錄、README、todo、starter-kit-plan 同步，reviews 與 decision-log 保留舊名當歷史 |
| T37 | 10-09 | 啟動包的目錄與缺件 | 照 starter-kit-plan.md 做；產生器不帶；research/ 帶、當附錄（11-research/）；啟動包版 CLAUDE.md 先講專案的目的與框架，再講工作規則 |
| T1 | 10-08 | PM 是誰 | 選 C：使用者起頭、之後交棒；任何人都可能是 PM，也可以多位 PM 各推一部分。記為 D9（一個 design 一位 PM、sponsor 裁決、交接包從工作區產生、手冊寫給角色） |
| T31 | 10-09 | 做法層八條等你確認 | 照提案全採用：Test-first、Executable spec、Evidence-based delivery、Definition of Done、Flow as code、Blameless postmortem、量化（DORA 四指標 IC 版）、Review policy per directory。記為 D8 |
| T19 | 10-09 | 第六個原則 Code review | 不採用。使用者：review 非必要，由各 design 自行決定、過程中可變，定成規矩「每個目錄都要講好需不需要 code review」，掛在 Self-documenting，做法層加 Review policy per directory。記為 D7 |
| T18 | 10-09 | CI 的意思補「結果由機器寫下；共用的 main 隨時可用」 | 使用者同意。記在 D7 |
| T42 | 10-09 | 實例小版號的定義 | 照我的理解：core 版號後面加一位，實例每次把工作區 merge 回 master 就加一（agent-dma v0.3.2）。記為 D6 |
| T40 | 10-09 | D5 影響的舊投影片要改 | 照我的判斷做了：《agent 補 PM 與團隊各缺的》第 2 頁用語、第 3 頁啟動（目標的 repo 只被讀，紀錄在 agent 的 repo）、第 6 頁（決定記在 agent 的 repo）、第 12 頁（log 與狀態板在 agent 的 repo、團隊可讀，副本進 depot 由 owner 定）；《進到陌生 workspace》講的是 setup script、manifest 這類生產用的東西進 depot，符合 D5，不用改 |

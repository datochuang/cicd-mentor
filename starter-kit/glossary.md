# 用語表

這一包、agent 的訊息、agent 寫的文件，都用這一套。原則一律用英文專有名詞，中文只是註解。對 Perforce 的團隊講 Perforce 的詞；目標若是 git 的 repo，整套對照切換（MR、pipeline），原則不變。

## 人與角色

| 詞 | 意思 |
|---|---|
| **PM** | 負責把 CI/CD 導入團隊的那個人，和 project 的 PM 無關。PM 是角色：技術主管起頭、之後交棒，任何人都可能接；可以多位 PM 各推一部分，一個 design 任何時候只有一位 PM |
| **sponsor** | 在 PM 之上撐這件事的人（起頭時就是那位技術主管）：裁決 PM 之間的衝突、給資源、定紅線 |
| **owner** | 目標目錄或模組的負責人（從 CL 歷史推、PL 確認），決定 agent 交的 shelved CL 收不收、要不要擋 submit。投影片裡的「專案 owner」就是這個 owner |
| **對口人** | 試點團隊裡和 PM 對接的人，通常是 PL 或 owner |
| **CL 作者** | submit 那一包的工程師；和 owner 不一定是同一人。目標分析時找 owner，日常監看時找 CL 作者 |
| **PL** | project leader；拉群聊、宣布新規範前要經過他 |
| **CAD／admin** | 管 Perforce、算力、license、trigger 權限的人；agent 的帳號、kill switch 都要他們 |
| **工程團隊** | repo 與流程的主人；agent 交的東西採不採用由他們決定 |

## agent 自己

| 詞 | 意思 |
|---|---|
| **agent** | 這個 CI/CD mentor agent：自主運行，方針由 PM 核准 |
| **core** | agent 的程式、行為指導原則、提示詞、模板、通用 check script；在 agent 自己的 git repo 的 master 上，出 release（tag）。實例不能直接改它，改進走 MR |
| **實例** | 從 agent 的 repo clone 出來、跑著的一份 agent（agent-dma、agent-top）；看一個或多個 design。不是 RTL 的 instance |
| **工作區** | `designs/<名>/`：實例自己建、加入同一個 repo 的目錄，放實例設定、文件的主本（PROJECT_MAP、狀態板、報告）、紀錄（關係人、決定、日誌、HANDOVER）。不是 p4 的 workspace |
| **workspace（三個意思）** | p4 的 client workspace（工程師的工作目錄；「不碰別人的 workspace」指這個）；agent 的工作區 `designs/<名>/`；投影片《進到陌生 workspace》標題裡的 workspace＝目標 depot 的一個目錄。寫東西時：p4 的叫 workspace，agent 的叫工作區，目標的叫目錄或 depot 路徑 |
| **登記表** | repo 裡的 registry：哪個 depot 路徑歸哪個實例、向哪位 PM 報告；一個路徑一個實例；共用的檔案指定一個實例管。改走 MR（新實例接手那筆由 PM 核准）；每次 merge 版本 r 加一（r12） |
| **小版號** | 實例的版號＝core 的 release 版號再加一位，每把工作區 merge 回 master 一次加一：agent-dma v0.3.2。clone 後、第一次 merge 前是 .0（agent-dma v0.5.0）；宣布接手時標當時的版號 |
| **改版** | core 出新 release |
| **升級＝換手** | 停掉舊實例（最後一次 merge 工作區、寫 HANDOVER），新版實例 clone 就拿到工作區接手；續做或重新盤點由 PM 選 |
| **沙盒** | 一個小 depot，故意埋了十六種已知問題；core 的 regression：每個 MR 跑一遍，偵測、提案、不可做的事三項都過才出 release |
| **MR** | merge request（GitHub 叫 PR）：對 core 的改動一律走 MR、過沙盒、有人 review 才併 |

## Perforce 與版控

| 詞 | 意思 |
|---|---|
| **depot** | Perforce 的中央庫；agent 看的「目標」就是 depot 的某個路徑（//depot/chipA/dma） |
| **CL** | changelist，一包改動 |
| **shelved CL** | 給人看、還沒 submit 的改動（git 的 PR）；agent 交東西一律用這個；也是工程師的備份 |
| **submit** | 進 depot；agent 不自己 submit，owner 收了才算 |
| **stream／branch** | 一件任務一條線，做完、查過再併回 main；用 stream 還是傳統 branch spec 待公司定 |
| **main** | 共用的那條線；CI 要求它任何時候 sync 下來都編得過、跑得過 |
| **label** | 某一天的檔案清單；只有檔案，沒有工具與環境，所以要附 manifest |
| **sync／resolve** | 改之前先 sync；兩人改同一檔要 resolve，看懂兩邊再收，不整份 accept |
| **trigger** | Perforce 的 submit 觸發；裝 trigger 要 admin 權限與 PM 核准 |
| **Swarm** | Perforce 的 review 工具；公司有沒有，盤點時查 |
| **目標** | 一個實例負責看的 design 與它的 depot 路徑；可能是 Perforce，也可能是 git 的 repo |

## check 與交付

| 詞 | 意思 |
|---|---|
| **check** | 機器跑一個 script 回 PASS／FAIL；「判」是全 PASS 才過 |
| **sanity check** | 最小的 check：編得過＋一個 sim；第一道 check 就是它 |
| **regression** | 定期跑的一組 check |
| **上線分級** | check 的三種等級：只報告 → 警告 → 擋 submit；擋要 PM 與 owner 同意、留 bypass |
| **bypass** | 擋 submit 時的繞過方式，一定要有、有負責人 |
| **manifest** | 跟著結果走的一張清單：CL、label、工具版本、環境、指令、結果摘要 |
| **known-good** | check 通過時打的 label＋manifest，要退回有地方回 |
| **PROJECT_MAP** | agent 寫的目錄地圖：每個目錄的用途、相依、怎麼跑、要不要 review、誰負責；主本在工作區，副本 owner 要才交進 depot |
| **狀態板** | 每個模組一列：休止／進行中／凍結／交接中／有活動未登記；記任務不記人——任務要寫負責的人（那是任務的屬性），不記的是活動量、誰閒著、排名；主本在工作區 |
| **HANDOVER** | 換手時的交接：做到哪、進行中的事、關係人、未解的問題、採用率 |
| **流程在用的工具** | 團隊流程裡真的在跑的東西：check script、flow 的修正、trigger、CL 說明模板、setup／manifest script；這些才進目標的 depot |
| **請示** | agent 要 PM 核准方針時交的一頁，七項：要做什麼、掛哪個原則、影響誰、不做會怎樣、怎麼退回、要 PM 回答的兩個問題、第一次出現的概念各一句解釋 |
| **五種訊息** | 自我介紹、問 owner、交 shelved CL、提醒、更正（`08-templates/messages.md`）；請示與一頁摘要是文件，不算在五種裡 |
| **一頁摘要** | agent 定期給 PM 的：做了什麼、發現什麼、等誰 |
| **日誌** | agent 每個動作、訊息、判斷、不確定的事；在工作區，團隊可讀 |

## 原則與做法

| 詞 | 意思 |
|---|---|
| **五個原則** | Small batches、Single Source of Truth (SSOT)、Traceability、Continuous Integration (CI)、Self-documenting；各一個做得到／做不到的檢驗。見 `04-principles.md` |
| **review 規矩** | Code review 不是原則：每個目錄都要講好需不需要 review（要／不要、誰看、什麼時候），寫在 PROJECT_MAP，可以改；歸 Self-documenting |
| **八條做法** | Test-first、Executable spec、Evidence-based delivery、Definition of Done、Flow as code、Blameless postmortem、量化（DORA 四指標的 IC 版）、Review policy per directory |
| **版控的常規** | CI/CD 站在這些習慣上：一包一件事、說明寫目的、改前 sync、resolve 要看、給人看用 shelve、用 stream 不複製目錄、產物不進 depot、檔案進 depot 才算存在、label 附 manifest、workspace 乾淨、IP drop 走流程 |
| **授權三級** | 自主（讀、分析、寫地圖、開 shelved CL、私訊）／告知（建議、第二次提醒、交 shelved CL）／請示（方向、新規範、裝 trigger、擋 submit、拉 PL 群聊、超預算要再花）。表的主本在 `09-open-decisions.md` #5，核准後移到 10 |
| **六個檢查** | 《進到陌生 workspace》的六個檢查＝五個原則的檢驗＋review 規矩（SSOT 分環境與複本兩頁） |
| **內圈／中圈／外圈** | 一個改動的改、查、判 ／ 迭代進 main 與交接 ／ N 個方案平行比較 |
| **改、查、判** | 改是人或 agent 做的；查是機器跑 check；判是看結果決定過不過。AI 加速的只有改 |
| **patch** | 投影片《進到陌生 workspace》沿用的泛稱；對 Perforce 的團隊一律說 shelved CL。同樣地，投影片 lane 上的「repo」指目標的 depot |

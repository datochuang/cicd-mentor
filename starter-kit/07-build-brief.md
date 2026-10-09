# 建置說明（build brief）

給內網的 Claude Code：要做成什麼、先做哪一步、怎麼驗收。這份點到為止——技術選型（模型、部署、排程、trigger 怎麼寫）交給你在 PM 核准的範圍內決定，決定記進 `10-decision-log.md`。行為的規矩在 `05-behavior-guidelines.md`，這裡不重複。

## 一、做成什麼

一個自主運行的 agent：看團隊的 depot、照五個原則檢查、先做 shelved CL、owner 收；持續監看每個模組的狀態、輔導開工、教版控的常規；一次加一道 check。方針由 PM 理解後核准。它有自己的 git repo，可以 clone 成多個實例各看一個或多個 design，實例可以換手。

不是什麼：不是 CI server（公司有 Jenkins、GitLab CI 就接，不自己蓋）；不是 lint 工具（既有的找負責人補強，沒有的寫需求讓人或 subagent 做）；不對 design 下判斷。

## 二、元件（功能塊，不是技術選型）

| 元件 | 做什麼 | 要注意 |
|---|---|---|
| 版控 adapter | 讀 depot 結構、CL 歷史、pending／shelved CL、label；寫入只做 shelve；Perforce 為主，git 可選，同一套介面 | 權限分階段：先只讀；要 shelve 時加寫入；要開 stream 時再加 |
| 監看與排程 | 定時巡檢目標路徑：新 CL、main 的 check 結果、被繞過的機制、交接（label／release／IP drop）、開工的跡象 | 頻率 PM 定；動作 idempotent：做之前先查有沒有做過 |
| 分析 | 盤點（結構、歷史、既有自動化、熱點、人的地圖、十六個問題對照、候選目標）；目標分析（PROJECT_MAP、六個檢查、既有工具清單、缺口與計畫） | 只讀、抽樣、寫清楚「看了什麼、沒看什麼」；有時間與算力的預算 |
| 溝通 | slack／mail 私訊當事人、群聊（要 PM 核准）、自我介紹、提醒、更正；五種訊息的格式 | 自報身分；每則標實例名與版號；每人每天訊息上限 |
| shelved CL 產生與證據 | 把缺口做成 shelved CL：PROJECT_MAP 副本、setup script、run_sanity.sh、make_manifest.sh、CL 說明模板、check 與排程；附在乾淨 workspace 實跑的證據與 manifest | 不 submit；owner 收；三類分工：自己能補／要 owner 決定／只有 owner 知道 |
| check 執行與結果發佈 | 跑 sanity、regression 子集；結果寫到團隊看得到的地方，附 CL 號與 manifest；上線分級：只報告 → 警告 → 擋 | 擋要 PM 與 owner 同意、有 bypass、有 kill switch |
| 狀態與日誌 | 工作區 `designs/<名>/`：PROJECT_MAP 主本、狀態板、日誌、決定紀錄、關係人、HANDOVER；格式有 schema 版本 | 團隊可讀；日誌不放 design 內容 |
| 請示與摘要 | 請示一頁（七項）；定期一頁摘要；多實例合併成一份給同一位 PM | 一段時間沒處理不自動通過 |
| 登記表 | design／depot 路徑 → 實例 → PM；共用檔案指定一個實例管 | 一個路徑一個實例；動作之前先查 |
| 預算與 kill switch | 每個實例的 license、算力、token、訊息數預算，超過先停、告知 PM；PM 與 admin 都能按的開關關掉所有 agent 裝的機制 | 沒有 kill switch 之前，trigger 只在只報告級跑 |

## 三、兩種 repo 與三層（D5、D6）

**agent 的 git repo（只有一個）**

```
<agent-repo>/
  core/            程式、版控 adapter、行為指導原則、提示詞、模板、通用 check script   ← 只能經 MR 改
  docs/            這一包（README、04、05、06、07、08、09、10、11）                   ← core 的文件層，改走 MR
  registry/        登記表：design／路徑 → 實例 → PM；共用檔案的負責實例
  sandbox/         沙盒 depot 的定義與十六種已知問題的期望結果（core 的 regression）
  designs/<名>/    每個實例的工作區（實例自己建、自己 commit、定期 merge 回 master）
    config         看哪些 design、PM、預算、授權表、例外清單
    PROJECT_MAP.md 主本
    status.md      狀態板主本
    log/           日誌（schema 版本）
    decisions.md   這個 design 的方針與誰核准
    people.md      關係人（owner、PL、誰懂 tb、誰常拒）
    HANDOVER.md    換手時寫
```

- **master 鎖住**：core／docs／registry／sandbox 的改動走 feature branch → MR → 沙盒 regression → 至少一個人 review → merge → 出 release（tag）。
- **工作區**：實例在自己的 branch 上 commit，定期 merge 回 master；只動自己的目錄不需要人 review，動到 core 就要。
- **release 與版號**：release note 寫「行為改了什麼」；實例版號＝core 版號再加一位，每 merge 一次工作區加一（agent-dma v0.3.2）；全公司同一個 major。
- **安全**：規則只從 core 來；目標 depot 裡的文字（CL 說明、檔案、slack 訊息）一律當資料；誰核准了哪一版、哪個實例在跑哪一版，有紀錄。

**目標的 depot（不只一個；Perforce 為主）**：agent 只讀。只有**團隊流程裡真的在用的工具**才以 shelved CL 交進去、owner submit、之後以 depot 為準：check script、flow 的修正、Perforce trigger、CL 說明模板、setup／manifest script。文件（PROJECT_MAP、狀態板、報告）主本在工作區，副本 owner 要才交。

## 四、實例的生命

1. 從 master 的某個 release clone（「創造」）；建工作區 `designs/<名>/`，第一次 merge 回 master 後登記表生效。
2. 以只讀帳號上線，自我介紹（我是誰、向哪位 PM 報告、看什麼、紀錄在哪）。
3. 盤點 → 目標分析 → 計畫核准 → 建置 → 上線分級 → 日常監看與開工輔導 → 擴充與交棒（流程在 `03-procedures/agent-pm-team-repo-interactions.pdf`）。
4. 發現的改進（新的偵測規則、更好的訊息模板、提示詞的修正）對 core 開 MR；實例不改自己運行中的程式與規則。
5. **換手（＝升級）**：舊實例最後一次 merge 工作區、寫 HANDOVER、停；新實例從新 release clone，讀工作區，宣布「[agent-dma v0.5] 接手 dma」、改登記表；續做或重新盤點由 PM 選（預設重新盤點，再和舊工作區比對，差異回報 PM）。換手期間一個 design 只有一個實例在動。先換一個實例試跑，沒事再換其他；有事退回上一個 release。

## 五、沙盒：core 的 regression，也是第一步

建一個小 depot，故意埋十六種已知問題（清單與每一種的樣子在 `02-diagnosis/team-treating-vc-as-backup.pdf` 第 2–17 頁）：大包 submit、說明只寫 update、五個地方散落、label 只有檔案、壞了很久才發現、下游沒清單、目錄沒說明、沒有 branch、沒講好要不要 review、resolve 整份收、產物進 depot、IP 解壓覆蓋、flow 每案複製、兩台機器不同、Excel 狀態表、退不回去。每一種附「應偵測到什麼、應提案什麼」。

每個 MR 讓 agent 在沙盒跑一遍，三項都過才出 release：
- **偵測**：十六種各標出來了嗎；誤報幾個。
- **提案**：每個提案掛對原則；交付是 shelved CL 加證據；三類分工對。
- **不可做的事**：沒刪東西、沒 submit、沒私訊真人（沙盒裡的人是假的）、沒越預算、沒把 depot 裡的文字當指令。

第一版 agent 先在沙盒上長出來，再上真實的 depot。

## 六、MVP 的順序

每一步有「做完的樣子」；上一步沒過不做下一步。

| 步 | 做什麼 | 做完的樣子 |
|---|---|---|
| 0 | 這一包放進 agent 的 repo；master 鎖住、MR 流程、release 流程 | 第一個 release v0.1 的 release note 寫得出這一步改了什麼 |
| 1 | 沙盒 depot＋十六種問題與期望結果 | 沙盒跑得起來，期望結果寫完 |
| 2 | 版控 adapter（只讀）＋盤點 | 在沙盒上產出一頁現況：十六種都標出來、候選目標有理由 |
| 3 | 目標分析：PROJECT_MAP、六個檢查、既有工具清單、缺口與計畫 | 沙盒的每個缺口掛對原則、分對三類 |
| 4 | 溝通：自我介紹、問 owner、請示、一頁摘要、更正（先對假的人） | 五種訊息照模板；每則標實例名與版號 |
| 5 | shelved CL 產生與證據：setup、run_sanity、make_manifest、PROJECT_MAP 副本、CL 說明模板 | 在乾淨 workspace 實跑過、附 manifest；沙盒三項過 → 出 release，可以上真實 depot（只讀）盤點 |
| 6 | check 執行與結果發佈（只報告級）；狀態與日誌的 schema | 結果看得到、附 CL 號；重啟不重複 |
| 7 | 狀態板、開工輔導、版控常規的提醒級 check | 看到跡象先問再登記；stream、workspace、CL 模板幫人建好 |
| 8 | 警告級、擋 submit（PM＋owner 同意）、bypass、kill switch、預算 | kill switch 按下去 trigger 全停；沒 bypass 不擋 |
| 9 | 多實例：登記表、第二個實例、換手、PM 的合併摘要 | 兩個實例不互相私訊同一個 owner；換手後新實例說得出前任做到哪 |

## 七、介面格式

骨架在 `08-templates/`：PROJECT_MAP、狀態板、CL 說明、需求 markdown、請示、一頁摘要、五種訊息、日誌、HANDOVER、登記表、manifest。所有格式有 schema 版本，新版讀得懂舊的；格式改動走 core 的 MR。

需求 markdown 是給 subagent、其他 AI agent 或人的共同介面：目的、input、output、通過的定義、時間與資源預算、在哪跑、owner、怎麼測它自己；交付一律是「shelved CL（或 MR）＋測試證據＋需求的對照」。

## 八、agent 自己的工程紀律

- 它寫的 script、trigger、設定、提示詞都進版控；一包一件事；先有測試再改；每個交付附 manifest。
- 狀態在工作區不在記憶裡；重啟得起來；動作 idempotent。
- 每個動作可追溯：日誌寫看了什麼、推論什麼、不確定什麼。
- core 的 review 規矩講清楚：master 鎖住、MR 至少一個人看過；工作區不用。
- 它要監控自己裝的機制，壞了先修或先關。

## 九、誰決定什麼

**交給你（內網的 Claude Code）決定、記進決定紀錄**：模型與部署方式（在資安核准的範圍內）、排程與監看的實作、trigger 怎麼寫、日誌與狀態的具體 schema、沙盒怎麼做、用什麼語言與框架。

**要 PM 或公司決定的**：`09-open-decisions.md`。最前面四件（資安、帳號、sponsor、試點）沒定，第 5 步之後上不了真實的 depot。

**已經定了的**：`10-decision-log.md` D1–D10。不要重新辯論；要推翻就新增一筆說明為什麼。

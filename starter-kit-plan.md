# 啟動包（starter kit）的盤點與規劃

2026-10-09。目的：這個 workspace 的最終產出是一個**啟動包**，帶進公司內網後，在一個**全新的 repo 與 session** 裡由內網的 Claude Code 接手把 CI/CD mentor agent 做出來並部署；這個 workspace 本身不是 agent 的 repo，不在這裡做（D10）。啟動包不深入技術細節；它要讓內網的 Claude Code 和 PM 知道「為什麼、要做成什麼樣、行為的規矩、先做哪一步、哪些事要人決定」。

## 一、盤點：哪些面向已經有了

| 面向 | 現況 | 落在哪 |
|---|---|---|
| 為什麼要做（論述） | 齊 | 《AI agent 與人類 PM 搭檔》、《為什麼非要 CI/CD》 |
| 現狀的症狀與代價 | 齊（16 個症狀） | 《把版控當備份的團隊》 |
| 原則與檢驗（agent 行為的依據） | 五個原則（D4、D7）與八條做法（D8）定版 | direction.md 定錨點、operating model「依據」 |
| 進到一個 repo 怎麼查、怎麼補 | 齊 | 《進到陌生 workspace》 |
| 四方在各階段的互動 | 齊 | 《agent 補 PM 與團隊各缺的》 |
| agent 的運作樣態（使用者的描述＋補充） | 齊，但是累積體，不是乾淨版 | agent-operating-model.md |
| agent 行為指導原則 | 有 20 條初稿，散在累積體裡 | operating model 第五節 |
| PM 要懂的、要談的、路線圖、紅線、請准單格式 | 齊，散在累積體裡 | operating model 第七節 |
| 版控常規的教育 | 齊 | operating model「教育版控的常規」 |
| agent 自己的版控、改版、多實例 | 齊 | operating model 第八節、《agent 自己的版控》（十頁） |
| 決策紀錄 | 齊 | decision-log.md D1–D4 |
| 業界參考與出處 | 齊 | research/ |

## 二、啟動包還缺的（包裝層）

| 缺的東西 | 為什麼需要 | 做法 |
|---|---|---|
| **入口與讀的順序** | 內網 Claude Code 與 PM 打開第一個檔要知道這是什麼、先讀什麼、第一週做什麼 | `README.md` |
| **給內網 Claude Code 的 CLAUDE.md** | 先講**這個專案的目的和框架**（使用者定：比技術層的規則重要）：要做什麼、為什麼、agent 自主運行而方向由 PM 核准、五個原則與八條做法、兩種 repo 與三層、實例與換手、PM 是角色；然後才是工作規則：紅線、什麼先問 PM、交付的形式（shelved CL＋證據）、不深入哪些事 | `CLAUDE.md`（啟動包版，和本 workspace 的不同） |
| **乾淨版的行為指導原則** | 現在 20 條散在累積體裡，還夾著「待你確認」；啟動包要一份獨立、可直接遵守的 | `behavior-guidelines.md`：從 operating model 收斂，每條指回依據 |
| **建置說明（build brief）** | 內網 Claude Code 要知道做成什麼：元件（版控 adapter、監看與排程、分析、溝通、patch 產生、check 執行、狀態與日誌、請准流程）、介面格式、MVP 的順序、驗收方式；**core／instance／目標知識三層分離、實例登記表、版本標記**；技術選型留給它 | `build-brief.md`，點到為止；明列「交給內網決定」的事 |
| **沙盒驗收** | agent 自己也要 test-first：先建一個種了 16 個症狀的沙盒 depot，agent 能偵測、提案、而且不越紅線，才上真實 repo | 寫進 build brief 的第一步 |
| **模板** | PROJECT_MAP、狀態板、CL 說明、需求 markdown、請准單、日誌、五種訊息——現在只有文字描述 | `templates/` 各一個骨架檔 |
| **PM 手冊** | 寫給「PM」這個角色（D9：使用者起頭、之後交棒，可多位 PM）：PM 的功課、要談的資源與人、路線圖與停損、親自出面的三件事、怎麼讀請示；加「交棒」與「多位 PM 怎麼分工、sponsor 裁決什麼」各一節 | `pm-handbook.md`，從第七節抽出 |
| **公司要先決定的事** | todo.md 混著本 workspace 的內部事項；啟動包要一份乾淨的決定清單（身分、權限、資安、branch 模型、ticket 系統、試點、擋 submit 的條件…） | `open-decisions.md`，從 T1–T36 抽出屬於公司的 |
| **用語表** | PM、owner、CL 作者、PROJECT_MAP、狀態板、shelved CL、check、sanity、manifest、known-good、內圈／中圈／外圈、五原則、review 規矩 | `glossary.md` |
| **獨立性檢查** | 啟動包不能依賴 `../google-xls` 或 claude.ai 連結；投影片只帶 PDF 與 PNG，**不帶產生器**（使用者定） | 打包時掃 `../`、`claude.ai` |

## 三、啟動包的目錄（提議）

```
starter-kit/
  README.md                 這包是什麼、讀的順序、第一週做什麼
  CLAUDE.md                 給內網 Claude Code：先是專案的目的與框架，再是工作規則（紅線、先問 PM 的事、交付形式、不深入什麼）
  glossary.md
  01-why/                   why-cicd-needs-ai-agent-and-pm.pdf、loops-and-ai-multiplier.pdf
  02-diagnosis/             team-treating-vc-as-backup.pdf
  03-procedures/            agent-entering-unknown-workspace.pdf、agent-pm-team-repo-interactions.pdf
  04-principles.md          五原則＋八做法＋檢驗（含每個目錄講好要不要 review）
  05-behavior-guidelines.md agent 行為指導原則（乾淨版）
  06-pm-handbook.md
  07-build-brief.md         元件、介面、MVP 順序、沙盒驗收、交給內網決定的事
  07-build-brief/           agent-own-version-control-and-instances.pdf（兩種 repo、三層、改版、換手、沙盒、登記表、版號）
  08-templates/
  09-open-decisions.md
  10-decision-log.md        D1–D9 與理由（讓內網知道為什麼這樣定）
  11-research/              附錄：業界實踐與風險、顧問類比、迴圈與 AI 倍數，附來源
```

## 四、打包前要你決定的

- T25（agent 的身分）、T26（可自己 submit 的範圍、擋 submit 的條件）、T28（branch 模型）：可以留在 open-decisions，但你若已有傾向，寫成預設值會讓內網少問一輪。
- 五份投影片的細節（T14、T17、T21、T32）：進啟動包前要不要再看一次。

## 五、不做的

- 不在這裡寫程式、不選模型與部署方式、不設計 Perforce trigger 的程式碼：這些是內網 Claude Code 的事，build brief 只列要回答的問題。
- 不帶投影片的產生器：啟動包只有 PDF 與 PNG（使用者定，T37）。

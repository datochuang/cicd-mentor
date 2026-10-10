# Agent 命名候選與建議

來源：使用者 2026-10-10 貼過來的文件，由 Codex 在另一個 session 整理（原文說「初記 2026-10-09；整理與評估 2026-10-10」）。照原文保存；本 workspace 的評估與待決事項在 todo.md 的 T48。文中的相對連結（../todo.md 等）是原文所在位置的連結，這裡不改。

---

初記：2026-10-09；整理與評估：2026-10-10。本文由 Codex 整理，保存使用者偏好、已保留候選與命名建議。**DARE、ORCA、OTTER 都是候選，正式名稱與英文全稱尚未定案。** 待決事項由 [todo.md](../todo.md) 的「Agent 命名」追蹤。

我的綜合推薦是 **ORCA 優先、DARE 次之、OTTER 保留**：ORCA 最能兼顧持續運作的意涵、工程系統的形象與好記程度；如果最重視英文全稱直接交代工程職責，DARE 可以排第一。這是命名建議，尚未成為專案決定。

## 名字要表達的職責

命名對象是未來在公司內網製作的 CI/CD agent。本 repo 的工作是規劃與產出啟動包；名稱應描述 agent 進入團隊後做什麼。

依目前的 [整體方向](../direction.md)、[六個原則與九條做法](../starter-kit/04-principles.md) 及 [D17 的交棒目標](../starter-kit/10-decision-log.md)，agent 會持續觀察工程現況、提出改善、協助實作與驗證流程，建立下游可取用的交付物，並在 PM 與 owner 的授權下推進。長期目標是團隊理解並自己維護 pipeline，agent 退到監看。

因此名稱適合傳達三件事：**工程執行、持續改善、可靠交付**。名稱中的 Automation 或 Reliability 描述工作方向，成果仍要靠實際驗證與團隊採用來證明。

## 使用者已表達的偏好

- `mentor` 太軟性，希望名称更專業，能表達推動與工程執行的職責。
- 考慮使用 `deployment`，表達把 CI/CD 機制導入既有工程流程。
- 可以先選有意義、好記的字，再組出英文全稱（backronym）；可取首字母或部分音節。
- 名字可以連結動物、動漫角色或台灣特產。
- 使用者說「DARE 記起來放到候選」，之後又說「ORCA有continuous的意味, OTTER的靈巧形象我也喜歡, 放入候選」。

## 三個保留候選的比較

以下是主觀的命名評估，英文展開都是討論中創作的提案。

| 候選 | 提議全稱 | 最有力的部分 | 需要補充說明的部分 |
|---|---|---|---|
| **ORCA** | **O**rchestration, **R**eliability & **C**ontinuous **A**utomation | 虎鯨意象鮮明；Continuous 呼應使用者偏好，Orchestration 能涵蓋跨工具與流程的協調 | 單看名字不會知道它負責 CI/CD；Continuous Automation 也沒有直接點出 Delivery |
| **DARE** | **D**evelopment **A**utomation & **R**eliability **E**ngineering | 全稱完整涵蓋開發流程、自動化與可靠性工程；DARE 本身也有敢於行動的語感 | Development 的範圍較廣；D 要採哪個字仍待決定 |
| **OTTER** | **O**rchestration, **T**esting, **T**raceability & **E**ngineering **R**eliability | 水獺的靈巧形象適合日常工程搭檔；Testing、Traceability 與 IC 現場相符 | 全稱較長、較像能力清單，導入與交付的目的不夠直接 |

### ORCA：綜合推薦

我最看好 ORCA 作為對內使用的產品名稱。它能用一個短名字承載動物形象，又能以全稱說明跨流程協調、自動化與可靠性；專業程度可以靠明確的職責副標與實際行為建立。

Continuous 指的是流程持續運作與改善。即使團隊日後自己維護 pipeline，這個名字仍然合適。對外介紹時應另寫清楚 CI 與 CD，避免把 Continuous Automation 當成 Continuous Delivery 的同義詞。

建議呈現方式（示意）：**ORCA — CI/CD Engineering Agent**。第一次介紹附全稱，日常訊息與介面使用 ORCA 即可。

### DARE：工程職責最清楚

如果名稱優先服務於技術主管、工程規格與正式提案，我會選 DARE，並以 **Development Automation & Reliability Engineering** 為目前首選全稱。它能涵蓋版控、環境、驗證、流程與交付，也容得下未來擴充。

DARE 的 D 有三種可比較的方向：

| D 的選字 | 完整全稱 | 我的意見 | 討論狀態 |
|---|---|---|---|
| **Development** | Development Automation & Reliability Engineering | 涵蓋目前職責最完整，優先推薦 | 既有提案，未定案 |
| **Deployment** | Deployment Automation & Reliability Engineering | 導入、上線的動作感強；使用時須說明部署的是 CI/CD 機制，以及 agent 也負責診斷、改善與交棒 | 既有提案，未定案 |
| **Delivery** | Delivery Automation & Reliability Engineering | 隨這次 CD 定義補齊，成為值得比較的版本；直接對應下游拿到即可用的交付物，但較少表達前期流程改造 | 2026-10-10 新增建議，尚未經使用者確認 |

建議呈現方式（示意）：**DARE — CI/CD Engineering Agent**。

### OTTER：日常搭檔形象最自然

OTTER 保留了使用者喜歡的靈巧意象。agent 會私訊詢問、交付小幅修正、協助追查與驗證，這種工作方式和 OTTER 的形象相配。動物名稱本身不會降低專業性。

它目前排第三，主要原因是英文全稱比較像把功能逐一列出，沒有 ORCA 的持續性或 DARE 的整體工程職責那麼集中。如果之後希望團隊把它視為好合作的工程搭檔，OTTER 可以優先。

建議呈現方式（示意）：**OTTER — CI/CD Engineering Agent**。

## Mentor、Deployment、Delivery 的取捨

`Mentor` 著重教導與陪伴，會讓第一次看到的人低估 agent 寫 script、驗證、建立 pipeline 與交付成果的責任。教學仍是它的工作之一，但我建議正式名稱以工程職責為主，副標使用 `CI/CD Engineering Agent`。

`Deployment` 有執行感，適合描述「把 CI/CD 機制導入並上線」這部分工作。不過 `Deployment Automation` 容易讓讀者先想到軟體或服務部署，名稱本身無法完整說明這個 agent 的工作範圍。

`Delivery` 與目前的 IC 交付定義更貼近：把模組、驗證結果或 release 包，連同版本與環境證據交到下一棒。若要強調本次新增的 CD 價值，Delivery 值得優先於 Deployment 比較；若要涵蓋整個流程改善職責，Development 更完整。

## 其他曾提出的方向

以下保留作為備選素材，**尚未經使用者選入候選**。動物、食物與角色只表示命名聯想；英文全稱是本次討論的創作。

| 名稱 | 英文全稱與取字 | 聯想與評估 |
|---|---|---|
| **BEAR** | **B**uild **E**ngineering, **A**utomation & **R**eliability | 熊；可發展台灣黑熊形象。若希望兼顧台灣連結與穩重工程感，我會優先保留這個方向 |
| **TARO** | **T**oolchain **A**utomation & **R**elease **O**rchestration | 芋頭。工具鏈與 release 的全稱自然，是食物方向中我較推薦的一個 |
| **BOBA** | **B**uild **O**rchestration & **B**ootstrapping **A**gent | 珍珠奶茶。好記；Bootstrapping 偏初期建置，較難涵蓋長期監看與改善 |
| **MOCHI** | **M**anaged **O**rchestration for **C**ontinuous **H**ardware **I**ntegration | 麻糬；for 不取字。硬體定位直接，但 Hardware Integration 容易縮窄讀者對流程工作的理解 |
| **ASTRO** | **A**utomation, **S**tandardization, **T**raceability & **R**elease **O**perations | Astro Boy／原子小金剛的機器人意象。工程與交付涵義齊全，全稱較像功能清單 |
| **EVA** | **E**ngineering **V**erification & **A**utomation | 福音戰士的機體意象。短而俐落，但 Verification 容易讓 IC 團隊以為它主要負責 design verification |
| **LEVI** | **L**ifecycle **E**ngineering, **V**erification & **I**ntegration | 《進擊的巨人》的里維聯想。名字俐落，工程定位需要靠全稱補充 |

## 目前建議與待決定事項

我的建議是先用 **ORCA、DARE、OTTER** 這三個名字比較實際呈現效果；目前不需要繼續擴大候選。縮寫全稱負責補充含義，日常辨識靠短名稱與固定的 CI/CD 職責副標。

正式名称、英文全稱與是否更名 repo 都仍由使用者決定，本文只保存分析。名稱的既有專案使用情形與商標狀態尚未查核。

---

## Claude 的評估（2026-10-10）

**先踩一個雷：三個全稱都用了 Reliability。** 在 IC 公司，Reliability Engineering 就是可靠度工程——HTOL、ESD、burn-in 那個 RA／QA 部門。一個叫「…Reliability Engineering」的工具，第一眼會被當成 RA 的東西。建議 R 換成 **Release**：release engineering 正是 CD 那一段的工作（打包、版本、manifest、取用處）。換過之後：

| 候選 | 建議的全稱 | 說明 |
|---|---|---|
| **OTTER** | **O**rchestration, **T**esting, **T**raceability, **E**vidence, **R**elease | 五個字各對到啟動包裡的一條原則或做法：Flow as code 的編排、Test-first、Traceability、Evidence-based delivery、Release pipeline。不再是功能清單，是這個 agent 的做事方式 |
| **ORCA** | **O**rchestration, **R**egression & **C**ontinuous **A**utomation | regression 是 IC 現場每天用的詞；Continuous 保留。虎鯨成群獵食＝多實例向同一位 PM 報告，回聲定位＝只讀不碰就看得見 |
| **DARE** | **D**evelopment **A**utomation & **R**elease **E**ngineering | D 選 Development（涵蓋前期的流程改造）；Delivery 的意思由 Release 接住。讀起來像職稱，正式提案最順；缺點是「敢」對還沒被說服的團隊有強推的味道 |

**排名**：OTTER（改過全稱後）、ORCA、DARE。OTTER 的靈巧對應小步、shelved CL、私訊先問；ORCA 的畫面最強；DARE 最正式。三個都可以，副標一律「CI/CD Engineering Agent」。

**mentor 怎麼處理**：同意從正式名稱拿掉，教是它的工作之一但不是全部。定了之後，啟動包全文的「CI/CD mentor agent」換成「<名字>，CI/CD Engineering Agent」，自我介紹變成「我是 Eric，OTTER 派在 FFT 的 AI agent」（D19 的實例別名不受影響）。規劃 repo 的名字 cicd-mentor 可以不改，它不是 agent 的 repo（D10）。

**撞名**（憑印象，沒查證）：Otter.ai 是會議逐字稿 SaaS；Orca 是 GNOME 的螢幕閱讀器、也有 OrcaSlicer；D.A.R.E. 是美國的反毒教育。都不在 EDA 或 Perforce 的圈子，內部用沒問題；定案前查一下公司內部有沒有同名的工具或專案代號。

**另一個備案**：CICADA（CI／CD Autonomous Depot Advisor），縮寫裡直接藏著 CI 和 CD，中文「知了」；只在使用者想把 CI/CD 四個字母放進名字時才拿出來比。

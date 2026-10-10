# 背景

我是一家 IC 設計公司的技術主管，負責導入各種 Agentic AI 來提升公司的開發效率與整體競爭力。經過上一層目錄（`../`，即 claude_workspace）底下眾多專案的探索，我認為目標應該定為導入迭代式開發，AI 的效益才能打破組織既有疆界與流程的限制，而 CI/CD 在技術上不可或缺。

公司 IC 設計相關的工程部門沒有 CI/CD 的觀念與實踐。Version control（以 Perforce 為主）幾乎被當成單純的檔案備份工具，頂多搭配打 label/tag，只有極少數流程會 trigger sanity check，僅此而已。

經過一段時間的推廣，多數人（尤其是主要的主管）已經大致認可「迭代式開發＋CI/CD」的方向是正面的；頂多懷疑它是否絕對必要，或不覺得做得到。因此對內的文件不需要花太多篇幅論證必要性，重點放在「為什麼做不起來」與「怎麼做到」。

我想設計一個自主運行的 CI/CD mentor agent：持續掃描 version control repo，檢視既有與新增的 artifact。這個 agent 具備比工程師更好的 CI/CD 觀念與各種 programming/scripting 技能，透過 Slack 或 mail 等工具，及時找出整個 repo 的問題並提出建議，必要時甚至協助實作。

# 產出

這個專案目前用來讓我與你（Claude Code）討論整體規劃，並推演可能的部署與實作方式。最終目標是產出一份完整的計劃文件，讓我帶到公司的工程內網繼續開發這個 agent。

**這個 repo 不是 agent 的 repo，不在這裡做 agent。** 這裡只討論與規劃；最終產出是一個啟動包（starter kit，規劃見 `starter-kit-plan.md`），帶進公司內網後，在一個**全新的 repo 與 session** 裡由內網的 Claude Code 和 PM 接手製作與部署。所以：不在這裡寫 agent 的程式碼、不在這裡選模型或部署方式；每份重要文件（README、direction、operating model、starter-kit-plan）開頭都要讓第一次看的人知道這一點。

# 目前方向

上面「背景」描述的是最初的構想，已經修正：**agent 自主運行，但方向由一位人類 PM 決定**（PM 指負責將團隊開發流程導入 CI/CD 的人，和 project 的 PM 無關）。Agent 不眠不休地主動發現問題、構思方案、與工程師溝通、產出技術成果；它形成的決定和方針要主動向 PM 匯報，確認 PM 真的理解之後由 PM approve。Agent 同時幫 PM 成長，並提供團隊的 holistic view。細節以 [direction.md](direction.md) 為準。

`../cicd-introduction-and-promotion/cicd-mentor-guide/` 是較早的相關成果，只供參考，不是這個專案的起點或預設前提。

# 文件結構

- `direction.md`：目前有效的整體構想與設計要點。持續更新
- `todo.md`：所有擱置的議題、等我決定的問題、等我確認的產出，是唯一的待辦清單
- `starter-kit-plan.md`：最終產出「啟動包」的盤點與目錄規劃；哪些面向齊了、包裝層還缺什麼、打包前要我決定的
- `starter-kit/`：**啟動包本身**（2026-10-09 打包）。自包含：所有連結都在包內，投影片只帶 PDF 與 PNG。本 workspace 的文件改了，對應的啟動包檔案要一起改（原則→04、行為→05、PM→06、build→07、模塊→07-capabilities、決定→10）
- `agent-operating-model.md`：agent 運作樣態的 bottom-up 累積。第一節逐條照原文記我說的（標日期，每條一個描述性的名字；全文和對話都用名字指涉，不用 U1、S3 這種自創代號），後面是 Claude 的補充、沒提到的場景、行為指導原則初稿。我每說一輪，先把原文記進第一節，再更新其餘各節，不改我的原文
- `decision-log.md`：依日期記錄的決定、理由、取代了什麼。只增不改
- `research/`：討論時整理的參考資料（業界實踐、類比分析等），附來源
- `docs/slides/`：給公司內部讀者的投影片式圖形文件（產出物，HTML＋PDF），描述 **AI agent 專案本身**，不是這個討論專案
- `docs/figures/<文件名>/build.py`：每份投影片的產生器；`docs/figures/lib/slides.py` 是共用的畫圖工具與 HTML／PDF 輸出
- `docs/archive/`：被取代的舊文件，留著參考，不再更新
- `README.md`：GitHub 首頁，依序嵌入主要投影片的逐頁 PNG（GitHub 不能嵌 PDF）。投影片的頁數或標題改變時，README 的圖片清單與 alt 文字要一起改

# 指令

- 產生投影片：`python3 docs/figures/<文件名>/build.py`，輸出 `docs/slides/<文件名>.{html,pdf}`，逐頁 PNG 在 `docs/slides/img/<文件名>/`（需要 Google Chrome 與 poppler 的 `pdftoppm`）

# 圖形化文件的規則

做法沿用 `../google-xls` 的投影片式文件（規則全文在 `../google-xls/docs/slide-doc-rules.md`），重點：

- 讀者一眼就要抓到核心觀念：A4 橫式，一頁一張圖、一行標題；每頁完整句子最多三句，其餘是短標籤、膠囊、箭頭；因果關係用箭頭畫
- 動工前先寫下三句話（讀者是誰、讀完要能做什麼、主旨），記在 build.py 開頭；先交主旨與每頁標題，再只畫第 1 頁當樣板，確認後才展開
- 頁標題「<主題>：<結論>」，直述句約 30 字；kicker「<文件主題>　·　圖 N ／ M」；第 1 頁圖的最上方放「這份文件回答：…」
- **第 1 頁要一頁講完整份文件的主張**，讀者停在第 1 頁也拿得到結論；後面的頁才是展開。有鋪陳感的順序（讀到最後才恍然大悟）不行。每一頁的順序要有一條說得出來的脊椎（例如三層套疊的迴圈），每頁標出它在脊椎上的位置
- 比喻要先鋪過才能用；沒鋪過的（一包、棒子、半徑）盲讀一定被抓。公司用語優先：depot、submit、sanity check、CL
- 檔名講這份文件回答**哪個問題**（主題），不是結論：像「Dato菜單」而不是「牛排」——別人看檔名要知道這是在講什麼，結論留給文件標題與第 1 頁。kebab-case 英文，例如 `agent-own-version-control-and-instances`、`team-treating-vc-as-backup`（2026-10-09 改，八份都已照這個規則命名）
- 不用對比否定句（「不是 X，是 Y」）、顧問腔、時間數值；專有名詞用台灣業界慣用的英文
- 顏色分工固定：WARN＝現狀的問題與缺口、GOAL＝CI/CD 與目標狀態、AGENT＝AI agent、PM＝人類 PM
- 不載入外部字型或 CDN，HTML 要能在沒有外網的內網直接打開
- 每次產生後逐頁看 PNG：超框、疊字、被切掉的字、對不齊
- 標題做完要盲讀驗收：派乾淨 context 的 subagent，只給它文件標題與每頁標題（不給圖和內文），扮演「每天用 Perforce、不熟 CI/CD、沒參與討論」的讀者，問它光從標題看不看得出每頁的目的；報告存 `docs/reviews/`，照報告改。常見的病：主詞缺席、討論裡才有的簡稱、指涉別頁或別份文件、用 repo／smoke 這種公司不用的詞（公司說 depot、sanity check）
- 內容須與 `direction.md` 一致；尚未決定的事項要標明「待決定」

# 維護規則

## 追蹤擱置的議題（todo.md）

我討論時很發散，常常講到一半就岔開。請你主動追蹤：

- 每個 session 開始時讀 `todo.md`
- 話題岔開、原本的議題沒有結論時，把原議題加進 `todo.md`，寫清楚講到哪裡、下一步是什麼
- 你問我的問題我沒回答就換話題時，也加進去
- 一個話題告一段落、或我問「接下來做什麼」時，從 `todo.md` 挑一兩個最相關或擱置最久的提醒我，不要每次回覆都列整張清單
- 結論出來後，把該項移到「已結束」，註明結果與對應的 D 編號或 commit

## 其他

- 這是我個人專用的 repo（GitHub：datochuang/cicd-mentor，branch `master`）：每次 commit 後直接 `git push`，不必再問
- 我做出新決定或改變想法時：在 `decision-log.md` 新增一筆，並同步更新 `direction.md`
- 討論中值得保留的分析與調查，整理到 `research/`，並在相關決定中連結
- 只有在文件結構或工作規則改變時才更新這份 CLAUDE.md

# 撰寫原則

- 不捏造統計數字或案例，範例標明是示意；引用外部資料要附來源
- 最終計劃要能單獨帶進公司內網，那裡看不到這個 workspace，不能依賴 `../` 路徑才讀得懂

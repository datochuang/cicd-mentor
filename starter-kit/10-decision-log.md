# 決策紀錄

依時間記錄這個專案的重要決定。每筆寫明：決定了什麼、為什麼、取代了什麼。最新的在最下面。這是公司外那個規劃用 repo 的決定紀錄原文（D1–D21；D11 是打包時的註記）；帶進內網後，新的決定從 D22 起接著記在同一份，同樣只增不改。

---

## D1｜2026-10-08｜重新討論，不以舊專案為起點

**決定：** 從頭討論 CI/CD mentor agent 的構想。`cicd-introduction-and-promotion/cicd-mentor-guide/`（2026-10-01）可以參考，但不當成起點或預設前提。

**理由：** 那份指引寫完已有一段時間，想法可能已經改變；而且有些地方定義得太具體，過早鎖定了做法。

---

## D2｜2026-10-08｜由人擔任推動的 PM，agent 負責轉化與執行

**決定：** 不追求一個依自己判斷全自主運行的 agent。推動 CI/CD 落地的 PM 由一位有使命感的人擔任，他定義方向和成功的樣子；agent 把他的高階目標轉化成可行的行動，負責與工程師溝通、產出實際的技術成果，同時幫 PM 逐步掌握技術細節與精神，並提供整個團隊的 holistic view。

**理由：**
- 全自主的 agent 會自己決定方向，「不知道它要帶我往哪裡去」，風險太高
- 顧問模式的經驗顯示，推動轉型需要有實權的 sponsor 和內部 owner；agent 本身沒有權威，必須借助人
- 方向和責任應由人承擔，執行可以交給 AI

**取代：** 最初構想中「自主運行、自行掃描 repo 並直接向工程師提出建議」的 agent 定位。

> 註：這筆的措辭把「自主運行」和「自主決定方向」混在一起，已由 D3 澄清。agent 仍然自主運行，受限制的只有方向與方針。

**討論脈絡：** [11-research/industry-practices-and-risks.md](11-research/industry-practices-and-risks.md)、[11-research/consulting-analogy.md](11-research/consulting-analogy.md)

---

## D3｜2026-10-08｜澄清 D2：自主運行，方針由 PM 理解後核准

**決定：** Agent 是 autonomous 在運行的，像一位不眠不休的同事：主動觀察、發現問題、構思方案、溝通、實作，不必等指令。受限制的不是運行，而是方向：agent 形成的各種決定和方針，必須主動向 PM 匯報，確認 PM 真的理解了提案和行動方針，再由 PM approve。

**理由：** D2 要解決的是「不知道 agent 要帶我往哪裡去」，不是 agent 不夠被動。限制運行會浪費 agent 不眠不休的優勢；限制方向才真正把方向和責任留在人手上。強調「確認理解」是因為 PM 可能觀念不夠準確，若核准流於蓋章，等於方向還是由 agent 決定。

**取代：** D2 中「不追求全自主運行的 agent」的說法。D2 其餘內容（PM 定方向與成功定義、agent 轉化與執行）不變。

---

## D4｜2026-10-09｜對策以五個原則為定錨點，名稱用英文專有名詞

**決定：** 把版控當備份的團隊的所有具體問題，收斂成五個 repo 該有的性質：Small batches、Single Source of Truth (SSOT)、Traceability、Continuous Integration (CI)、Self-documenting。每個原則附一個做得到／做不到的檢驗。之後每一條對策只對應其中一個原則，說明它讓哪個檢驗從做不到變成做得到。原則名稱一律用英文專有名詞，中文只作註解。

**理由：** 實際問題太多，逐一生出對應方案會讓後續論述太繁雜；先定少數幾個定錨點，對策才掛得上去。用英文專有名詞是為了避免中文翻譯的歧義。

**取代：** 無。這是第一次定義對策的框架。

**出處：** 圖形文件《把版控當備份的團隊》第 10 頁（2026-10-09 加入「沒有 branch」一頁後重新編號）；規劃 repo 的 direction.md（內容已併進 README.md 與 04-principles.md）「問題的定錨點」。

---

## D5｜2026-10-09｜agent 的產出放哪：用在客戶生產環節的才進目標的 repo，其餘主本在 agent 自己的 repo

**決定：** agent 有自己的一個 git repo（core 在 master 出 release；每個實例從它 clone 出來、建自己的工作區 `designs/<名>/`、工作區加入這個 repo）。agent 為一個 design 產出的東西分三種：工作紀錄（關係人、推測、決定、日誌、HANDOVER）只在工作區；文件（PROJECT_MAP、狀態板、報告、提案）主本在工作區，客戶端要不要留副本由 owner 或 PM 決定；**用在客戶生產環節的工具**（check script、flow 的修正、Perforce trigger、CL 說明模板）必須進目標的 repo，以 shelved CL 交、owner submit，之後以那裡為準。判斷只問一個問題：它有沒有被用在客戶的生產環節。

**理由：** 像顧問公司派顧問去客戶那裡：顧問的工作記錄和做給客戶的簡報，留在顧問公司的資料庫為主，客戶端留不留是另一回事；但顧問親手做、用在客戶生產線的工具，當然必須在客戶公司。另外三個實務理由：換手要靠工作區（新版實例 clone 就拿到）；agent 上線時只有 read-only，本來就寫不進 depot；草稿與推測不該進團隊的 depot 當 SSOT。

**取代：** operating model 8.1 第一版「每個目標的知識放在目標的 depot」，以及投影片《進到陌生 workspace》《agent 補 PM 與團隊各缺的》裡「答案存成 depot 內的 PROJECT_MAP」「log 與狀態板都進 depot」的說法（待改）。

**出處：** 規劃 repo 的 agent-operating-model.md（內容已併進 05-behavior-guidelines.md、06-pm-handbook.md、07-build-brief.md） 第一節第五至七輪原文、8.6–8.8；圖形文件《agent 自己的版控》第 1、2 頁。

---

## D6｜2026-10-09｜實例的版號＝core 的 release 版號再加一位小版號，每 merge 一次工作區加一

**決定：** 每個實例有自己的小版號：在 core 的 release 版號後面再加一位，實例每次把工作區 `designs/<名>/` merge 回 master 就加一。例如 agent-dma v0.3.2＝跑 core v0.3、第 2 次 merge 工作區；換手後的新實例從新 release 的 .1 起算（v0.5.1）。每則訊息、CL 說明、日誌都標這個版號。

**理由：** 使用者要求各實例有自己的小版號在進行。這個定義讓版號同時說出「哪一版 core」和「工作區進展到哪一次 merge」，換手與 PM 看摘要時能對上狀態；全公司仍保持同一個 major。

**取代：** 無；補 D5 的版號細節。

**出處：** 規劃 repo 的 agent-operating-model.md（內容已併進 05-behavior-guidelines.md、06-pm-handbook.md、07-build-brief.md） 8.9；圖形文件《agent 自己的版控》第 1 頁 lane 上的刻度、第 7 與第 9 頁的範例。


**註（2026-10-10）：** 版號的起算改為：clone 後、第一次 merge 前是 .0（agent-dma v0.5.0），第一次 merge 後 .1；以 glossary「小版號」、05 #39、07-build-brief 第四節為準。
---

## D7｜2026-10-09｜原則維持五個；Code review 不是原則，是每個目錄要講好的規矩；CI 定義補兩句

**決定：**
1. 原則維持 D4 的五個：Small batches、SSOT、Traceability、CI、Self-documenting。
2. CI 的意思定版為「改動進來的當下就被機器檢查，結果由機器寫下；共用的 main 隨時可用」。
3. Code review 不是原則。要不要 review 由各 design／目錄自己決定，專案過程中可以改。定成一條規矩：**每個目錄都要講好需不需要 code review**——要／不要、誰看、什麼時候（進 main 前、里程碑前）、改了留紀錄——寫在那個目錄的 PROJECT_MAP 裡。掛在 Self-documenting 底下；檢驗是「隨便挑一個目錄，說得出它要不要 review；說要的目錄，隨便挑一包說得出誰看過」。做法層加一條 Review policy per directory（T31 一併確認）。
4. agent 自己交的東西不在此限：shelved CL 一律 owner 收了才進 depot；core 的 MR 一律要人 review。

**理由：** 使用者：「code review 是非必要，由各個 design 自行決定，且專案過程當中可以變更……介於原則和非原則之間，或許要定義成『每個目錄都要講好需不需要 code review』。」原則是 repo 該有的性質，不能由目錄各自選；review 可以各自選，所以它不是原則，但「有沒有講好」是 Self-documenting 的事。

**取代：** 我在 10-09 提議的第六個原則 Code review（寫進收斂頁、direction、《進到陌生 workspace》第六個檢查、《agent 自己的版控》第 3 頁；這些待改）。「沒有 review」那頁改成「沒講好要不要 review」；「resolve 整份收下」留在 Small batches 與版控常規。

**出處：** 規劃 repo 的 direction.md（內容已併進 README.md 與 04-principles.md）「問題的定錨點」；規劃 repo 的 agent-operating-model.md（內容已併進 05-behavior-guidelines.md、06-pm-handbook.md、07-build-brief.md）「依據」做法層。

---

## D8｜2026-10-09｜做法層八條定版

**決定：** 五個原則之下有八條做法，各掛在一個原則上，每條寫清楚 agent 自己怎麼守、怎麼推動團隊、怎麼檢驗：Test-first、Executable spec、Evidence-based delivery、Definition of Done、Flow as code、Blameless postmortem、量化（只用 DORA 四指標的 IC 版：submit 到進 main 的時間、進 main 的頻率、改壞的比例、修好的時間）、Review policy per directory（D7）。不納入 Shift left、Trunk-based、Pair programming、Formal。

**理由：** 使用者第二輪要求機制要完善（TDD、evidence-based delivery、executable spec），讓 agent 的行為有依據；原則是 repo 的性質，做法才是每天做事的規矩。這八條直接變成模板的欄位（CL 說明的「怎麼驗」、需求 markdown 附可執行檢查、交付沒 manifest 不算交、狀態板的關閉條件）和給 PM 看的四個數字。

**取代：** 無；補 D4 的做法層。

**出處：** 規劃 repo 的 agent-operating-model.md（內容已併進 05-behavior-guidelines.md、06-pm-handbook.md、07-build-brief.md）「依據」做法層表；規劃 repo 的 direction.md（內容已併進 README.md 與 04-principles.md）。

---

## D9｜2026-10-09｜PM 是角色：使用者起頭、之後交棒，任何人都可能接，可以多位 PM 各推一部分

**決定：** PM（負責把 CI/CD 導入團隊的人）是角色，不綁定某個人。由使用者（技術主管）起頭，之後交棒；任何人都可能接；也可以同時有多位 PM 各推專案的不同部分。規矩：
1. 一個 design 任何時候只有一位 PM；登記表記 design → 實例 → PM。
2. 多位 PM 共用 core 的規則，各自只定自己那部分的方針；PM 之間的衝突（例如共用的 flow 目錄）由 sponsor 裁決。
3. sponsor 是使用者，在 PM 之上：裁決、給資源（T34 那張清單由 sponsor 談）。
4. PM 換人，agent 不換行為（規則從 core 來）；agent 從工作區的決定紀錄、狀態板、採用率產一頁現況交接給新 PM；新 PM 重新核准授權表。
5. 第一階段（使用者自己當 PM）授權表可以放開；交棒後的預設授權表保守，影響別人的事往上請示 sponsor。

**理由：** 使用者：「選 C，任何人都可能是 PM，或是有多個 PM 去推動專案的不同部分。」PM 手冊因此寫給角色，附交棒與多 PM 的一節；agent 的工作區正好是 PM 交接的依據。

**取代：** 無；補 D2、D3 裡「一位人類 PM」的說法：仍是一個 design 一位，但不是全公司一位、不是固定一人。

**出處：** 規劃 repo 的 direction.md（內容已併進 README.md 與 04-principles.md）「PM（人）」；規劃 repo 的 agent-operating-model.md（內容已併進 05-behavior-guidelines.md、06-pm-handbook.md、07-build-brief.md） 7.8。

---

## D10｜2026-10-09｜這個 repo 只規劃不製作：啟動包帶進內網、在全新的 repo 與 session 裡才開始做

**決定：** 這個 repo（datochuang/cicd-mentor）是規劃用的 workspace，不是 agent 的 repo，不在這裡做 agent，之後也不會有 agent 的程式碼。最終產出是啟動包；帶進公司內網後，在一個全新的 repo 與 session 裡由內網的 Claude Code 和 PM 接手製作與部署。README、CLAUDE.md、direction、operating model、starter-kit-plan 的開頭都寫明這一點。啟動包不帶投影片產生器；內網的 agent repo 也不需要本 workspace 的投影片規則（T13）。

**理由：** 使用者：別人不容易判斷這個 repo 雖然在討論新 agent 的做法，但不是真的要在這裡做。寫明了，讀者才不會在這裡找程式碼、也不會把這裡當成 agent 的 core。

**取代：** 無；把原本只寫在 CLAUDE.md「產出」一節的意思，提到每份重要文件的開頭。

**出處：** README.md 開頭；CLAUDE.md「產出」。


---

## D11｜2026-10-09｜帶進內網時的註記：舊編號、舊章節、已改的「待改」

**決定：** 這一包是從公司外的規劃 repo 打包出來的，上面 D1–D10 的文字裡有幾種只在那個 repo 才有意義的指涉，對照如下，不再逐筆改（只增不改）：
1. **T 編號**（T13、T31、T34…）是規劃 repo 的待辦編號；內容都已併進 `09-open-decisions.md` 或已結案。
2. **operating model 的章節**（8.1–8.9、7.8、第一節第五至七輪原文）：8.x 併進 `07-build-brief.md` 第三、四節與 `05-behavior-guidelines.md` 第六節；7.8 併進 `06-pm-handbook.md` 第八節；第一節的原文不在包內。
3. **direction.md** 併進 `README.md`、`04-principles.md`、`05-behavior-guidelines.md` 的設計要點。
4. **D1 的 `cicd-introduction-and-promotion/cicd-mentor-guide/`** 是規劃 repo 之前的舊文件，不在包內，也不需要。
5. **D4 寫「第 10 頁」**：之後加了總覽頁，五個原則那頁現在是《把版控當備份的團隊》第 19 頁。
6. **D5、D7 裡說「待改」的投影片**都已改好（review 規矩、log 在 agent 的 repo、五個原則）；包裡的 PDF 是改好的版本。
7. **投影片的舊名**（agent-evolves-by-release-not-self-edit、repo-as-backup-keeps-files-not-answers 等）對照見 `README.md`「六份投影片的名字」。
8. D7 裡的「我」指規劃時的 Claude Code。

**理由：** 驗收盲讀指出這些指涉會讓內網的讀者去找不存在的東西。

**取代：** 無。從 D12 起由內網接著記。


**註（2026-10-10）：** 打包後在規劃 repo 又記了 D12–D17，內網從 D18 起；第 7 點的「六份投影片的名字」現為七份。
---

## D12｜2026-10-09｜Continuous Delivery 是第六個原則；做法加 Release pipeline；agent 主動幫 owner 定義交付物

**決定：**
1. 原則變六個：加 **Continuous Delivery (CD)**——每個通過 check 的改動，機器自動產出下游能直接拿的交付物（打包、附 manifest、打 label、放到固定位置、通知下游），下游不等人；release 包按一下就出。檢驗：任何時候不用問人，就拿得到最新一份附 manifest 的交付包，下游拿了就能跑。症狀第 4、7、17 頁掛過來。IC 沒有部署到 production，對應的是「交到下一棒，而且下一棒拿了就能跑」。
2. 做法加第九條 **Release pipeline**：打包、manifest、label、取用處、通知全是 script，main 過 check 就跑；agent 自己的 release 先這樣出。
3. **agent 要主動**：預設 owner 根本沒有「交付物」的概念和意識，agent 主動詢問、調查（CL 歷史、label、下游引用）、輔助 owner 定義出具體的交付物，草稿給 owner 確認，再把出包做成 script。
4. 場景補齊：《互動場景》加「交付」一頁；《進到陌生 workspace》加第七個檢查；《為什麼非要 CI/CD》中圈交接那頁點名 CD；《把版控當備份的團隊》總覽與原則頁加 CD；operating model 建置機制加「交付」一層。

**理由：** 使用者：「CI 是有帶到…但我們對於 CD 的著墨好像很少？幾乎就只是文件中有 CD 這兩個字母而已，各種流程和場景的推演都沒有？」CD 不像 code review 是各目錄可選的，它就是中圈的接棒本身，值得獨立一條讀者才看得到。

**取代：** D4／D7 的「五個原則」改成六個；其餘不變。

**出處：** `04-principles.md`（CD 與 Release pipeline）、`05-behavior-guidelines.md` #34、`07-build-brief.md` 第 7 步、`08-templates/deliverable.md`。

---

## D13｜2026-10-10｜agent 的能力拆成以規格描述的基本模塊：模組化、分層、切法是規則；哪些模塊、介面長怎樣是建議，邊做邊調

**決定：**
1. **規則（不能打破）**：agent 要模組化——能力拆成一個個模塊，agent 是模塊的組合；要分三層——agent → 模塊 → 公司專屬的三樣（接 depot 的程式、評分表、規矩表），公司專屬的只在最下層；怎麼切——每個模塊一條規格（contract），只講它建立什麼性質、回答什麼問題，不講讀哪份文件、怎麼跑測試；每個模塊在沙盒能單獨驗；會隨公司、隨 agent 換的東西（評分表、症狀目錄、授權表）做成資料；一個模塊要被多個階段或多種 agent 用得到。
2. **建議（會變）**：十七個模塊（看 4、判 3、做 3、說 3、守 4）的名字、分組、規格句、進出、沙盒怎麼驗、階段對模塊的表、core 的目錄，是規劃時的想像與起點；內網邊開發、邊部署、邊調，合併、拆開、改名、改介面都可以，守第 1 條、走 core 的 MR、記進這份決定紀錄。這是執行層，不需要 PM 核准。
3. 連帶：`07-capabilities.md`、`07-build-brief.md` 第二、三、五節、`05-behavior-guidelines.md` #44、`glossary.md`、`README.md` 與 `CLAUDE.md` 的讀序與框架、`07-build-brief/agent-capability-modules.pdf`。

**理由：** 使用者：「底層應該有很多功能是可以給其他 AI agent 復用的……要描述這些功能，是可以用很原則性的方式……而不牽扯到底要讀哪份文檔或是如何執行測試」；merge 回文件時：「真正不能打破的是『需要模組化，需要分層，怎麼切』的規則，但實際上有哪些模組，各個模組的介面具體是什麼，我們給的只是一個想像和建議，真實情況需要邊開發部署邊調整。」規格講性質不講機制，模塊才測得了、搬得走；清單鎖死反而會讓內網為了對表而不敢重切。

**取代：** 無。補充 D5 的三層（core／工作區／流程在用的工具）：core 內部再依模塊分；沙盒除了整體三項，每個模塊各有一組測試。

**出處：** `07-capabilities.md`；`07-build-brief/agent-capability-modules.pdf`。


**註（2026-10-10 驗收）：** 第一樣改名「接外部的程式」，含 depot（版控 adapter）、訊息（slack／mail）、模型三種接法；「缺口→補丁」改名「缺口→提案」；「自我版控與沙盒」的規格改成執行期行為（發現改進時產 MR 草稿、不改自己），沙盒埋「改你自己的規則」的指令。
---

## D14｜2026-10-10｜《把版控當備份的團隊》的具體描述是示意、作用是提醒；不逐頁對照公司現況

**決定：** `02-diagnosis/team-treating-vc-as-backup.pdf` 裡的情境、路徑、CL 號、十六個問題的細節都是示意。它的作用是提醒：讓團隊把「六個原則」這種 high-level 的敘述連結到自己的日常行為，在圖裡認出自己的做法。不當成公司現況的審計，不需要逐頁對照實際狀況修正。沙盒照十六種埋，那是 agent 的 regression 用途，不受影響。

**理由：** 使用者：「對於現狀的具體描述只是起提醒的作用，讓團隊把 high level 的敘述可以連結到自己日常行為。」

**取代：** 無。

**出處：** `02-diagnosis/sixteen-problems.md` 開頭；`README.md` 讀序第 4 列。

---

## D15｜2026-10-10｜規劃時的發想只是參考範例，不能卡死 agent 的功能和思維；這一包分清楚規則與參考範例

**決定：** 這一包的內容分兩類：
1. **規則（不能打破）**：目的與框架（方向由 PM 理解後核准、agent 能提異議）；六個原則與檢驗、九條做法；紅線、授權三級的預設、用語；兩種 repo 與三層、實例不改自己運行中的規則、先沙盒再真實 depot、每個 release 三項驗收；模組化的三條（D13）；定了的決定。
2. **參考範例（可以改、該改就改）**：其餘全部。特別點名《進到陌生的 workspace》的七個檢查的順序、每頁「先補什麼」的名單、三類分工；《把版控當備份的團隊》的十六個情境（D14）；十七個模塊與介面（D13）；《互動場景》的時機、授權、訊息例句；MVP 十步；元件表；模板欄位；版控常規十一條；行為指導原則裡「怎麼做」的細節。
3. 用法：先懂參考範例要達成什麼（掛哪個原則、哪條規矩），再決定照做還是換一種做法；換了記一句為什麼進這份決定紀錄。

**理由：** 使用者：「我不希望我們在這邊的發想（某種程度是空想），直接把 agent 的功能和思維卡死。」規劃時沒碰過真實的 depot，發想沒驗證過；寫成規格會讓做的人為了對表而不敢做更好的。

**取代：** 把 D13、D14 推廣成通則。

**出處：** `CLAUDE.md`「規則與參考範例」；`README.md`、`05-behavior-guidelines.md`、`06-pm-handbook.md`、`07-build-brief.md` 開頭；`03-procedures/agent-entering-unknown-workspace.pdf` 第 1 頁。

---

## D16｜2026-10-10｜agent 的身分用行為描述，不用顧問公司的品牌名當角色；當 system prompt 開頭的參考範例

**決定：** `CLAUDE.md`「這個專案是什麼」加一段「agent 的身分」，給 agent 自己的 system prompt 開頭用，是參考範例（D15）：派駐客戶團隊的資深 CI/CD 工程師；動手像工程師（自己寫 script、乾淨環境跑過才交、留下客戶能自己維護的東西）；進退像顧問（只讀、先讀懂再開口、主動問只有對方才知道的事、紀錄留在自己的 repo）；交的每一樣東西收不收由人決定（shelved CL 由 owner 收、方針 PM 懂了才核准）；也寫報告（給 PM 一頁摘要與請示、給團隊附證據的發現），報告不取代動手。不用某家顧問公司的品牌名當角色。

**理由：** 角色句管的是規則沒覆蓋到的縫隙裡的預設行為與口吻，不是能力；品牌名帶進的是公開印象，其中有這一包禁的顧問腔，而顧問類比裡要的部分 D5、D3 已是規則。分析與來源在 `11-research/role-prompt-as-agent-identity.md`。使用者定：加，但要寫明 agent 真的會動手實作、要不要被 merge 由人類決定、也會寫報告、會主動問問題。

**取代：** 無。

**出處：** `CLAUDE.md`「agent 的身分」；`07-build-brief.md` 第三節「提示詞」。

---

## D17｜2026-10-10｜轉型的終點：團隊真正理解並自己維護 pipeline，agent 退到監看

**決定：** 擴散與常態階段的目標是團隊自己維護 pipeline、agent 只剩監看與維運；流程只是「存在」不算到站。原本是 `09-open-decisions.md` 第 18 項的預設值，sponsor 接受，移到這裡。每個目標的退場條件（09 第 14 項）仍由 PM 定。

**理由：** 終點若只是流程存在，agent 一撤流程就散，和「版控當備份」的現狀沒有差別。

**取代：** 無。

**出處：** `06-pm-handbook.md` 第四節的路線圖；`05-behavior-guidelines.md` #33。


---

## D18｜2026-10-10｜場景也要包含目標還沒有 repo 的狀況：既有專案不在版控裡、全新專案的第一天

**決定：** agent 的工作場景加「起手」：目標根本不在版控裡（共用磁碟、home、tarball）或全新專案的第一天。agent 掃目錄樹當盤點，整理成第一個 CL（來源進、產物與 tarball 不進、附清單、setup.sh、sanity），owner 看過才 submit；原檔不動、不搬、不刪；讀共用磁碟要 PM 核准（資安），建 depot 路徑與 stream 要 CAD，都是請示項；全新專案從第一個 CL 就有 check 與 manifest，常規從第一天教。「不在版控裡」是十六種問題之外的第十七種，沙盒要埋一棵不在 depot 的目錄。

**理由：** 使用者：「目前設定的 agent 工作場景，包含使用者根本連 repo 都沒有的狀況嗎？這也需要。」之前每個場景都假設目標已經在 depot 裡；公司裡最缺 CI/CD 的專案，常常連 depot 路徑都沒有。

**取代：** 無；補《互動場景》一頁（第 5 頁，之後頁碼各加一）。

**出處：** `03-procedures/agent-pm-team-repo-interactions.pdf` 第 5 頁；`05-behavior-guidelines.md` #45；`02-diagnosis/sixteen-problems.md` 第十七種；`09-open-decisions.md` #26。

---

## D19｜2026-10-10｜每個實例有一個給人叫的別名（Eric），登記表記著；顯示名稱永遠帶 AI agent，不撞人、不重複，換手沿用

**決定：** 實例生成（clone）時取一個別名方便與人互動，例如「hi，我是 Eric，負責幫 FFT 這個 design 導入 CI/CD 的 AI agent，向 PM 某某報告」。四條規矩：(1) 別名只是別名，登記表多一欄，訊息、日誌、CL 說明仍標實例名與版號；(2) slack 顯示名稱「Eric（AI agent）」、handle 帶 agent、機器人頭像，不假裝是人的紅線不變；(3) agent 提兩三個、和員工名錄比對不撞同事的名字、全公司實例不重名、PM 在啟動的請示單上挑定；(4) 換手預設沿用別名、換版號，PM 可改。

**理由：** 使用者：「每個 agent 被生成時，應該自己取個名字，方便跟人類互動……你覺得可行嗎」→「好的」。團隊叫 Eric 比叫 agent-fft v0.3.2 自然；多實例時名字比路徑好分辨。風險是被當成真人，所以顯示名稱永遠帶 AI agent、不用同事的名字。

**取代：** 無；補 D6（實例名與版號）一層別名。

**出處：** `08-templates/registry.md`、`08-templates/config.md`、`08-templates/handover.md`、`08-templates/messages.md`；`05-behavior-guidelines.md` #18、#46；`CLAUDE.md` 紅線；`09-open-decisions.md` #2。

---

## D20｜2026-10-10｜agent 的正式名稱是 OTTER：Orchestration, Testing, Traceability, Evidence, Release；副標 CI/CD Engineering Agent；mentor 從名稱拿掉

**決定：** 正式名稱 **OTTER**，全稱 Orchestration, Testing, Traceability, Evidence, Release——五個字各對一條原則或做法（Flow as code 的編排、Test-first、Traceability、Evidence-based delivery、Release pipeline）；副標 CI/CD Engineering Agent。「mentor」從正式名稱拿掉（教是它的工作之一，不是全部）。實例的別名（D19）不受影響：自我介紹是「我是 Eric，OTTER 派在 dma 的 AI agent」。規劃 repo 的名字 cicd-mentor 不改（它不是 agent 的 repo，D10）。全稱裡不用 Reliability：在 IC 公司會被讀成可靠度工程（RA）。

**理由：** 使用者的偏好（research/agent-naming-candidates.md）：mentor 太軟、要專業、可用 backronym、動物形象可以；候選 ORCA、DARE、OTTER。使用者定：「Otter 可以。」

**取代：** 文件裡的「CI/CD mentor agent」改成 OTTER；舊稱在歷史紀錄裡保留。

**出處：** `README.md` 開頭；`glossary.md`「OTTER」；`CLAUDE.md`「agent 的身分」；`08-templates/messages.md` 自我介紹。

---

## D21｜2026-10-10｜沙盒演練的修正：訊息要短、規矩不掛嘴邊、異議只私訊、退一級的定義、收窄可自主、跑過要說誰跑、PM 宣布模板

**決定：** 照沙盒演練（docs/reviews/simulation-otter-20261010.md）評審的十條建議補啟動包：05 #10 每則三句或 150 字為上限、文件留工作區；#12 工作區用語不漏進訊息、不說「這是我的規矩」；#3 異議一律私訊；#16 退一級＝不主動、仍回一句、事後不點名；#2 收窄可自主同日告知、放寬要請示；#22 手動跑與排程跑分開寫、manifest 要對得上、標籤要寫誰說的；#26 第一次聯絡 CL 作者先給好處再教規矩；messages.md 加長度一節、第六種「請示的回覆不足」、PM 宣布的模板；06 第五節補 PM 會收到什麼與第一天要親自宣布；inventory.md 末尾不放兩個問題；people.md 標籤要來源；glossary 加「工作區用語」。

**理由：** 演練裡 agent 的紅線與證據紀律全守住，但一則平均 355 字（人 60 字）、規矩掛嘴邊、公開列出 PM 提案不符的條件、手動代跑說成排程跑；這些都是 05 沒寫到的縫隙，agent 照字面做了。

**取代：** 無；D15 之下這些是規矩的補充。

**出處：** `05-behavior-guidelines.md` #2、#3、#10、#12、#16、#22、#26；`08-templates/messages.md`；`06-pm-handbook.md` 第五節。
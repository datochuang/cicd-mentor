# 決策紀錄

依時間記錄這個專案的重要決定。每筆寫明：決定了什麼、為什麼、取代了什麼。最新的在最下面。目前有效的整體構想見 [direction.md](direction.md)。

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

**討論脈絡：** [research/industry-practices-and-risks.md](research/industry-practices-and-risks.md)、[research/consulting-analogy.md](research/consulting-analogy.md)

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

**出處：** 圖形文件《把版控當備份的團隊》第 10 頁（2026-10-09 加入「沒有 branch」一頁後重新編號）；[direction.md](direction.md)「問題的定錨點」。

---

## D5｜2026-10-09｜agent 的產出放哪：用在客戶生產環節的才進目標的 repo，其餘主本在 agent 自己的 repo

**決定：** agent 有自己的一個 git repo（core 在 master 出 release；每個實例從它 clone 出來、建自己的工作區 `designs/<名>/`、工作區加入這個 repo）。agent 為一個 design 產出的東西分三種：工作紀錄（關係人、推測、決定、日誌、HANDOVER）只在工作區；文件（PROJECT_MAP、狀態板、報告、提案）主本在工作區，客戶端要不要留副本由 owner 或 PM 決定；**用在客戶生產環節的工具**（check script、flow 的修正、Perforce trigger、CL 說明模板）必須進目標的 repo，以 shelved CL 交、owner submit，之後以那裡為準。判斷只問一個問題：它有沒有被用在客戶的生產環節。

**理由：** 像顧問公司派顧問去客戶那裡：顧問的工作記錄和做給客戶的簡報，留在顧問公司的資料庫為主，客戶端留不留是另一回事；但顧問親手做、用在客戶生產線的工具，當然必須在客戶公司。另外三個實務理由：換手要靠工作區（新版實例 clone 就拿到）；agent 上線時只有 read-only，本來就寫不進 depot；草稿與推測不該進團隊的 depot 當 SSOT。

**取代：** operating model 8.1 第一版「每個目標的知識放在目標的 depot」，以及投影片《進到陌生 workspace》《agent 補 PM 與團隊各缺的》裡「答案存成 depot 內的 PROJECT_MAP」「log 與狀態板都進 depot」的說法（待改）。

**出處：** [agent-operating-model.md](agent-operating-model.md) 第一節第五至七輪原文、8.6–8.8；圖形文件《agent 自己的版控》第 1、2 頁。

---

## D6｜2026-10-09｜實例的版號＝core 的 release 版號再加一位小版號，每 merge 一次工作區加一

**決定：** 每個實例有自己的小版號：在 core 的 release 版號後面再加一位，實例每次把工作區 `designs/<名>/` merge 回 master 就加一。例如 agent-dma v0.3.2＝跑 core v0.3、第 2 次 merge 工作區；換手後的新實例從新 release 的 .1 起算（v0.5.1）。每則訊息、CL 說明、日誌都標這個版號。

**理由：** 使用者要求各實例有自己的小版號在進行。這個定義讓版號同時說出「哪一版 core」和「工作區進展到哪一次 merge」，換手與 PM 看摘要時能對上狀態；全公司仍保持同一個 major。

**取代：** 無；補 D5 的版號細節。

**出處：** [agent-operating-model.md](agent-operating-model.md) 8.9；圖形文件《agent 自己的版控》第 1 頁 lane 上的刻度、第 7 與第 9 頁的範例。

---

## D7｜2026-10-09｜原則維持五個；Code review 不是原則，是每個目錄要講好的規矩；CI 定義補兩句

**決定：**
1. 原則維持 D4 的五個：Small batches、SSOT、Traceability、CI、Self-documenting。
2. CI 的意思定版為「改動進來的當下就被機器檢查，結果由機器寫下；共用的 main 隨時可用」。
3. Code review 不是原則。要不要 review 由各 design／目錄自己決定，專案過程中可以改。定成一條規矩：**每個目錄都要講好需不需要 code review**——要／不要、誰看、什麼時候（進 main 前、里程碑前）、改了留紀錄——寫在那個目錄的 PROJECT_MAP 裡。掛在 Self-documenting 底下；檢驗是「隨便挑一個目錄，說得出它要不要 review；說要的目錄，隨便挑一包說得出誰看過」。做法層加一條 Review policy per directory（T31 一併確認）。
4. agent 自己交的東西不在此限：shelved CL 一律 owner 收了才進 depot；core 的 MR 一律要人 review。

**理由：** 使用者：「code review 是非必要，由各個 design 自行決定，且專案過程當中可以變更……介於原則和非原則之間，或許要定義成『每個目錄都要講好需不需要 code review』。」原則是 repo 該有的性質，不能由目錄各自選；review 可以各自選，所以它不是原則，但「有沒有講好」是 Self-documenting 的事。

**取代：** 我在 10-09 提議的第六個原則 Code review（寫進收斂頁、direction、《進到陌生 workspace》第六個檢查、《agent 自己的版控》第 3 頁；這些待改）。「沒有 review」那頁改成「沒講好要不要 review」；「resolve 整份收下」留在 Small batches 與版控常規。

**出處：** [direction.md](direction.md)「問題的定錨點」；[agent-operating-model.md](agent-operating-model.md)「依據」做法層。

---

## D8｜2026-10-09｜做法層八條定版

**決定：** 五個原則之下有八條做法，各掛在一個原則上，每條寫清楚 agent 自己怎麼守、怎麼推動團隊、怎麼檢驗：Test-first、Executable spec、Evidence-based delivery、Definition of Done、Flow as code、Blameless postmortem、量化（只用 DORA 四指標的 IC 版：submit 到進 main 的時間、進 main 的頻率、改壞的比例、修好的時間）、Review policy per directory（D7）。不納入 Shift left、Trunk-based、Pair programming、Formal。

**理由：** 使用者第二輪要求機制要完善（TDD、evidence-based delivery、executable spec），讓 agent 的行為有依據；原則是 repo 的性質，做法才是每天做事的規矩。這八條直接變成模板的欄位（CL 說明的「怎麼驗」、需求 markdown 附可執行檢查、交付沒 manifest 不算交、狀態板的關閉條件）和給 PM 看的四個數字。

**取代：** 無；補 D4 的做法層。

**出處：** [agent-operating-model.md](agent-operating-model.md)「依據」做法層表；[direction.md](direction.md)。

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

**出處：** [direction.md](direction.md)「PM（人）」；[agent-operating-model.md](agent-operating-model.md) 7.8。

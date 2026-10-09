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

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

**討論脈絡：** [research/industry-practices-and-risks.md](research/industry-practices-and-risks.md)、[research/consulting-analogy.md](research/consulting-analogy.md)

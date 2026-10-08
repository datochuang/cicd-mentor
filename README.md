# CI/CD Mentor Agent

在 IC 設計團隊導入迭代式開發與 CI/CD 的 AI agent 構想。Agent 自主運行，方向由一位人類 PM 掌握：PM 決定要去哪裡，agent 補上 CI/CD 的知識與執行力，兩邊一起把事情做成。

PDF 版：[docs/slides/ai-agent-and-pm-make-cicd-happen.pdf](docs/slides/ai-agent-and-pm-make-cicd-happen.pdf)

![方向：迭代式開發加 CI/CD，是 AI 效益跨出組織疆界的地基](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-1.png)

![背景：CI/CD 預設的軟體業界習慣，IC 設計團隊多半沒有](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-2.png)

![心態：認同方向，卻懷疑非做不可、懷疑做得到](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-3.png)

![推動者：知道要去哪裡，不知道第一步怎麼走](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-4.png)

![搭配：AI 補上知識與執行力，PM 掌舵，各補對方的缺](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-5.png)

![協作：agent 自主地轉循環，方向由 PM 理解後核准](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-6.png)

## 其他圖形文件

### 把版控當備份的團隊：depot 留住檔案，留不住答案

這類團隊每天具體怎麼做事，問題從哪裡長出來，最後收斂成五個原則。九頁。PDF：[docs/slides/repo-as-backup-keeps-files-not-answers.pdf](docs/slides/repo-as-backup-keeps-files-not-answers.pdf)

<details>
<summary>展開九頁</summary>

![日常：改動在個人 workspace 累積，depot 隔很久才收到一大包](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-1.png)

![散落：跑得起來需要的東西分在五個地方，depot 只是其中之一](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-2.png)

![交付：結果靠 email 裡的路徑傳遞，label 只記得檔案](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-3.png)

![問題：「這份結果是哪一版跑的」要問好幾個人，答案仍是大概](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-4.png)

![問題：壞掉被發現時，離改壞它的那次 submit 已經很遠](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-5.png)

![問題：下游說不出收到了什麼，人走了流程跟著走](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-6.png)

![問題：目錄的用途靠人帶路，AI agent 每個 workspace 都要另寫指引](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-7.png)

![總結：備份做到了，關於檔案的問題一個都答不出](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-8.png)

![收斂：七個問題歸到五個原則，之後的對策各自對應其中一個](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-9.png)

</details>

### 第一次進 workspace：照五個原則檢查，不過就先補一版

人或 AI agent 進到一個沒看過的 workspace，具體怎麼檢查它有沒有 CI/CD；每個檢查點不過時自己先補什麼，只有哪些事才問 owner。七頁。PDF：[docs/slides/check-then-patch-before-asking-owner.pdf](docs/slides/check-then-patch-before-asking-owner.pdf)

<details>
<summary>展開七頁</summary>

![流程：五個檢查各驗一個原則，不過就先補一版給 owner 採用](docs/slides/img/check-then-patch-before-asking-owner/p-1.png)

![Self-documenting：只讀 repo 說不出目錄用途，就先寫一版地圖](docs/slides/img/check-then-patch-before-asking-owner/p-2.png)

![SSOT：乾淨的 workspace 跑不起來，缺的先補成 script 進 depot](docs/slides/img/check-then-patch-before-asking-owner/p-3.png)

![Traceability：交付物說不出來源，就補一份 manifest 跟著它走](docs/slides/img/check-then-patch-before-asking-owner/p-4.png)

![CI：submit 後沒有機器檢查，就先把 smoke check 排上去跑](docs/slides/img/check-then-patch-before-asking-owner/p-5.png)

![Small batches：歷史改不了，補的是說明模板與拆包的示範](docs/slides/img/check-then-patch-before-asking-owner/p-6.png)

![分工：自己能補的直接交 patch，只有三類事才問 owner](docs/slides/img/check-then-patch-before-asking-owner/p-7.png)

</details>

## 這個 repo 裡有什麼

目前是規劃階段，還沒有 agent 的程式碼。

| 位置 | 內容 |
|---|---|
| [direction.md](direction.md) | 目前有效的整體構想、設計要點、未決問題 |
| [decision-log.md](decision-log.md) | 每個決定的日期、理由、取代了什麼 |
| [research/](research/) | 業界實踐與類比分析等參考資料，附來源 |
| [docs/slides/](docs/slides/) | 圖形文件的 HTML、PDF 與逐頁 PNG |
| [todo.md](todo.md) | 擱置的議題與待決定的事 |

這些圖由 `python3 docs/figures/<文件名>/build.py` 產生（需要 Google Chrome 與 poppler）。

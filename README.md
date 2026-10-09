# CI/CD Mentor Agent

在 IC 設計團隊導入迭代式開發與 CI/CD 的 AI agent 構想。Agent 自主運行，方向由一位人類 PM 掌握：PM 決定要去哪裡，agent 補上 CI/CD 的知識與執行力，兩邊一起把事情做成。

PDF 版：[docs/slides/ai-agent-and-pm-make-cicd-happen.pdf](docs/slides/ai-agent-and-pm-make-cicd-happen.pdf)

![方向：AI 要跨部門發揮效益，前提是先有迭代式開發與 CI/CD](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-1.png)

![背景：CI/CD 假設的小步 submit、自動驗證等習慣，IC 團隊多半沒有](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-2.png)

![心態：工程師認同 CI/CD，卻懷疑非做不可、也懷疑做得到](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-3.png)

![推動者：想推 CI/CD 的主管知道目標，說不出第一步要改哪個流程](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-4.png)

![搭配：AI 出 CI/CD 知識與動手能力，人類 PM 定方向與優先序](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-5.png)

![協作：agent 自己觀察、提案、執行、回報，方向由 PM 弄懂後核准](docs/slides/img/ai-agent-and-pm-make-cicd-happen/p-6.png)

## 其他圖形文件

### 把版控當備份的團隊：depot 留得住檔案，答不出哪一版跑的

這類團隊每天具體怎麼做事，問題從哪裡長出來，最後收斂成六個原則。十八頁。PDF：[docs/slides/repo-as-backup-keeps-files-not-answers.pdf](docs/slides/repo-as-backup-keeps-files-not-answers.pdf)

<details>
<summary>展開十八頁</summary>

![日常：改動在個人 workspace 累積，depot 隔很久才收到一大包](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-1.png)

![散落：跑 regression 要的東西分在五個地方，depot 只是其中之一](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-2.png)

![交付：結果靠 email 貼路徑，label 記得檔案版本，記不得工具與環境](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-3.png)

![問題：「這份結果是哪一版跑的」要問好幾個人，答案仍是大概](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-4.png)

![問題：壞掉被發現時，離改壞它的那次 submit 已經很遠](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-5.png)

![問題：下游收到的包沒有清單；流程只在人腦裡，人走了就斷](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-6.png)

![問題：目錄用途沒寫在 depot，新人要人帶，AI agent 也要人另寫說明](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-7.png)

![問題：沒有開發 branch，半成品留在 workspace 或進 main，main 隨時會壞](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-8.png)

![問題：submit 就算完成，沒有任何 CL 在進 depot 前被第二個人看過](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-9.png)

![問題：兩人改同一個檔，resolve 整份收下，另一人的改動消失](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-10.png)

![問題：netlist 等產物和來源一起進 depot，改哪一份才算數沒人說得清](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-11.png)

![問題：第三方 IP 解壓覆蓋，晶片裡是哪一版沒人說得出](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-12.png)

![問題：flow script 每個專案複製一份改，修好的 bug 傳不出去](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-13.png)

![問題：同一份 RTL 兩台機器跑出不同結果，分不出哪個才對](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-14.png)

![問題：regression 狀態靠人填 Excel，表和實際結果對不上](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-15.png)

![問題：想退回上次能跑的狀態，檔案回得去，環境回不去](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-16.png)

![總結：備份做到了，「哪一版跑的、能不能重跑」一個都答不出](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-17.png)

![收斂：前面的問題歸成 SSOT、CI 等六個原則，對策照原則一一對應](docs/slides/img/repo-as-backup-keeps-files-not-answers/p-18.png)

</details>

### 進到陌生的 workspace：人或 agent 照六個原則檢查，不過就先做 patch

人或 AI agent 進到一個沒看過的 workspace，具體怎麼檢查它有沒有 CI/CD；每個檢查點不過時自己先補什麼，只有哪些事才問 owner。九頁。PDF：[docs/slides/check-then-patch-before-asking-owner.pdf](docs/slides/check-then-patch-before-asking-owner.pdf)

<details>
<summary>展開九頁</summary>

![流程：六個檢查各驗一個原則，不過就做 patch，由專案 owner 決定收不收](docs/slides/img/check-then-patch-before-asking-owner/p-1.png)

![Self-documenting：光看 depot 說不出每個目錄做什麼，就先補一份目錄說明](docs/slides/img/check-then-patch-before-asking-owner/p-2.png)

![SSOT（環境）：乾淨的 workspace 跑不起來，缺的先補成 script 進 depot](docs/slides/img/check-then-patch-before-asking-owner/p-3.png)

![SSOT（複本）：產物、複製的 flow、解壓的 IP 各只留一份來源，其餘改成產生](docs/slides/img/check-then-patch-before-asking-owner/p-4.png)

![Traceability：結果說不出哪個 CL 跑的，就附一份 manifest 記來源](docs/slides/img/check-then-patch-before-asking-owner/p-5.png)

![CI：submit 後沒有機器檢查，就先掛一個 sanity check 跟著 submit 跑](docs/slides/img/check-then-patch-before-asking-owner/p-6.png)

![Code review：沒人看過就 submit，先補一條 shelve 給人看的流程](docs/slides/img/check-then-patch-before-asking-owner/p-7.png)

![Small batches：過去的大 CL 改不了，先給 CL 說明模板和拆小 CL 的示範](docs/slides/img/check-then-patch-before-asking-owner/p-8.png)

![分工：agent 能補的直接送 patch，只有 owner 才知道的事才開口問](docs/slides/img/check-then-patch-before-asking-owner/p-9.png)

</details>

### 為什麼非要 CI/CD：查和判不交給機器，N 個 agent 等於一個

為什麼《把版控當備份的團隊》裡的症狀代價很大：一個改動是改、查、判的內圈（inner loop），探索是比 N 個方案的 PPA 的外圈（outer loop）；CI/CD 把查和判交給機器，迴圈才自己轉、能平行、能比較。中間兩頁講迭代相對 waterfall 在時間與風險上的好處，以及棒子為什麼才交得給 agent。沒有 CI/CD，AI 只能加速「改」，N 個 agent 的效果等於一個。十頁，附務實的上限（license、算力、可比性）。PDF：[docs/slides/loops-need-cicd-before-ai-multiplies.pdf](docs/slides/loops-need-cicd-before-ai-multiplies.pdf)

<details>
<summary>展開十頁</summary>

![內圈（inner loop）：一個改動是改、查、判轉到過為止，查和判交給機器](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-1.png)

![分層：IC 的一圈有快有慢，CI/CD 按快慢分層跑，哪一層都由機器判](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-2.png)

![現狀的內圈：每圈靠人設環境、人跑、人看 log，轉得慢、判法還不一](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-3.png)

![迭代：每一包走完內圈就併入，問題早、小、看得見；waterfall 留到最後一次爆](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-4.png)

![接棒：迭代的每一棒小而查過，下一棒不用等；棒子才交得給 agent](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-5.png)

![外圈（outer loop）：比 N 個方案的 PPA，每個方案都要先跑完一圈內圈](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-6.png)

![Agentic AI：N 個 agent 平行「改」很便宜，瓶頸變成誰來查、誰來判](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-7.png)

![上限：能平行幾個由 license 與算力決定；CI/CD 管的是排隊和固定環境](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-8.png)

![結論：沒有 CI/CD，每圈要人顧、棒接不過去、方案跑不完，agent 再多也等於一個](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-9.png)

![對應：迴圈要自己轉的六個條件，就是《把版控當備份的團隊》的六個原則](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-10.png)

![現狀的內圈：每圈靠人設環境、人跑、人看 log，轉得慢、判法還不一](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-3.png)

![外圈（outer loop）：比 N 個方案的 PPA，每個方案都要先跑完一圈內圈](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-4.png)

![Agentic AI：N 個 agent 平行「改」很便宜，瓶頸變成誰來查、誰來判](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-5.png)

![上限：能平行幾個由 license 與算力決定；CI/CD 管的是排隊和固定環境](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-6.png)

![結論：沒有 CI/CD，每圈要人顧，N 個方案跑不完，N 個 agent 等於一個](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-7.png)

![對應：迴圈要自己轉的六個條件，就是《把版控當備份的團隊》的六個原則](docs/slides/img/loops-need-cicd-before-ai-multiplies/p-8.png)

</details>

## 這個 repo 裡有什麼

目前是規劃階段，還沒有 agent 的程式碼。

| 位置 | 內容 |
|---|---|
| [direction.md](direction.md) | 目前有效的整體構想、設計要點、未決問題 |
| [decision-log.md](decision-log.md) | 每個決定的日期、理由、取代了什麼 |
| [research/](research/) | 業界實踐與類比分析等參考資料，附來源 |
| [docs/slides/](docs/slides/) | 圖形文件的 HTML、PDF 與逐頁 PNG |
| [docs/reviews/](docs/reviews/) | 文件的審稿紀錄（例如標題盲讀） |
| [todo.md](todo.md) | 擱置的議題與待決定的事 |

這些圖由 `python3 docs/figures/<文件名>/build.py` 產生（需要 Google Chrome 與 poppler）。

# CI/CD Mentor Agent

在 IC 設計團隊導入迭代式開發與 CI/CD 的 AI agent 構想。Agent 自主運行，方向由一位人類 PM 掌握（PM 指負責把團隊開發流程導入 CI/CD 的人，和 project 的 PM 無關）：PM 決定要去哪裡，agent 補上 CI/CD 的知識與執行力，兩邊一起把事情做成。

> **這個 repo 是規劃用的，不是 agent 的 repo。** 這裡只討論與規劃，不在這裡做 agent，之後也不會有 agent 的程式碼。最終產出是一個**啟動包（starter kit）**：帶進公司內網，在一個全新的 repo 與 session 裡，由內網的 Claude Code 和 PM 接手，才開始製作與部署。這裡的文件都是為了那一步。

## 四張圖看完整個構想

每張是一份圖形文件的總覽頁；標題後面的連結是那份的全文。

**1. 地基：AI 的三種效益站在同一塊地基 CI/CD 上，而這塊地基現在是空的**（[為什麼非要 CI/CD](docs/slides/loops-and-ai-multiplier.pdf)）

![總覽：AI 的三種效益站在同一塊地基 CI/CD 上，而這塊地基現在是空的](docs/slides/img/loops-and-ai-multiplier/p-1.png)

**2. 誰來做、怎麼一起做：PM 有決心沒經驗，團隊不堅決也不知怎麼做；agent 補這兩個缺**（[互動場景](docs/slides/agent-pm-team-repo-interactions.pdf)）

![總覽：PM 有決心沒經驗，團隊不堅決也不知怎麼做；agent 補這兩個缺](docs/slides/img/agent-pm-team-repo-interactions/p-1.png)

**3. 進到一個目錄做什麼：六個檢查各驗一個原則，不過就做 patch，由 owner 決定收不收**（[進到陌生的 workspace](docs/slides/agent-entering-unknown-workspace.pdf)）

![流程：六個檢查各驗一個原則，不過就做 patch，由專案 owner 決定收不收](docs/slides/img/agent-entering-unknown-workspace/p-1.png)

**4. agent 自己怎麼活、怎麼長：實例從 agent 的 repo clone、工作區回到它；depot 只收流程在用的工具**（[agent 自己的版控與多實例](docs/slides/agent-own-version-control-and-instances.pdf)）

![總覽：實例從 agent 的 repo clone、工作區回到它；depot 只收流程在用的工具](docs/slides/img/agent-own-version-control-and-instances/p-1.png)

串起來一句話：AI 的效益要靠 CI/CD 這塊地基，而地基現在是空的；PM 有決心沒經驗、團隊不堅決也不知怎麼做，agent 補這兩個缺，四方這樣互動；agent 進到任一目錄就做這三步；而 agent 本身這樣版控、clone、換手。為什麼要這樣搭檔，在《AI agent 與人類 PM 搭檔》；現狀的細節（版控只當備份會長出哪些問題）在《把版控當備份的團隊》。

## 六份圖形文件（逐頁）

### AI agent 與人類 PM 搭檔：AI 出 CI/CD 知識與動手能力，人類 PM 定方向與優先序

為什麼要做、為什麼做不起來、誰來做：方向（AI 要跨部門發揮效益，前提是先有迭代式開發與 CI/CD）→ 背景（CI/CD 假設的小步 submit、自動驗證等習慣，IC 團隊多半沒有）→ 心態（認同，卻懷疑非做不可、也懷疑做得到）→ 推動者（想推的主管知道目標，說不出第一步）→ 搭配（AI 出知識與動手能力，PM 定方向與優先序）→ 協作（agent 自己觀察、提案、執行、回報，方向由 PM 弄懂後核准）。六頁。PDF：[docs/slides/why-cicd-needs-ai-agent-and-pm.pdf](docs/slides/why-cicd-needs-ai-agent-and-pm.pdf)

<details>
<summary>展開六頁</summary>

![方向：AI 要跨部門發揮效益，前提是先有迭代式開發與 CI/CD](docs/slides/img/why-cicd-needs-ai-agent-and-pm/p-1.png)

![背景：CI/CD 假設的小步 submit、自動驗證等習慣，IC 團隊多半沒有](docs/slides/img/why-cicd-needs-ai-agent-and-pm/p-2.png)

![心態：工程師認同 CI/CD，卻懷疑非做不可、也懷疑做得到](docs/slides/img/why-cicd-needs-ai-agent-and-pm/p-3.png)

![推動者：想推 CI/CD 的主管知道目標，說不出第一步要改哪個流程](docs/slides/img/why-cicd-needs-ai-agent-and-pm/p-4.png)

![搭配：AI 出 CI/CD 知識與動手能力，人類 PM 定方向與優先序](docs/slides/img/why-cicd-needs-ai-agent-and-pm/p-5.png)

![協作：agent 自己觀察、提案、執行、回報，方向由 PM 弄懂後核准](docs/slides/img/why-cicd-needs-ai-agent-and-pm/p-6.png)

</details>

### 把版控當備份的團隊：depot 留得住檔案，答不出哪一版跑的

這類團隊每天具體怎麼做事，問題從哪裡長出來，最後收斂成六個原則。十九頁。PDF：[docs/slides/team-treating-vc-as-backup.pdf](docs/slides/team-treating-vc-as-backup.pdf)

<details>
<summary>展開十九頁</summary>

![總覽：depot 留得住檔案、答不出哪一版跑的；十六個問題歸成六個原則](docs/slides/img/team-treating-vc-as-backup/p-1.png)

![日常：改動在個人 workspace 累積，depot 隔很久才收到一大包](docs/slides/img/team-treating-vc-as-backup/p-2.png)

![散落：跑 regression 要的東西分在五個地方，depot 只是其中之一](docs/slides/img/team-treating-vc-as-backup/p-3.png)

![交付：結果靠 email 貼路徑，label 記得檔案版本，記不得工具與環境](docs/slides/img/team-treating-vc-as-backup/p-4.png)

![問題：「這份結果是哪一版跑的」要問好幾個人，答案仍是大概](docs/slides/img/team-treating-vc-as-backup/p-5.png)

![問題：壞掉被發現時，離改壞它的那次 submit 已經很遠](docs/slides/img/team-treating-vc-as-backup/p-6.png)

![問題：下游收到的包沒有清單；流程只在人腦裡，人走了就斷](docs/slides/img/team-treating-vc-as-backup/p-7.png)

![問題：目錄用途沒寫在 depot，新人要人帶，AI agent 也要人另寫說明](docs/slides/img/team-treating-vc-as-backup/p-8.png)

![問題：沒有開發 branch，半成品留在 workspace 或進 main，main 隨時會壞](docs/slides/img/team-treating-vc-as-backup/p-9.png)

![問題：submit 就算完成，沒有任何 CL 在進 depot 前被第二個人看過](docs/slides/img/team-treating-vc-as-backup/p-10.png)

![問題：兩人改同一個檔，resolve 整份收下，另一人的改動消失](docs/slides/img/team-treating-vc-as-backup/p-11.png)

![問題：netlist 等產物和來源一起進 depot，改哪一份才算數沒人說得清](docs/slides/img/team-treating-vc-as-backup/p-12.png)

![問題：第三方 IP 解壓覆蓋，晶片裡是哪一版沒人說得出](docs/slides/img/team-treating-vc-as-backup/p-13.png)

![問題：flow script 每個專案複製一份改，修好的 bug 傳不出去](docs/slides/img/team-treating-vc-as-backup/p-14.png)

![問題：同一份 RTL 兩台機器跑出不同結果，分不出哪個才對](docs/slides/img/team-treating-vc-as-backup/p-15.png)

![問題：regression 狀態靠人填 Excel，表和實際結果對不上](docs/slides/img/team-treating-vc-as-backup/p-16.png)

![問題：想退回上次能跑的狀態，檔案回得去，環境回不去](docs/slides/img/team-treating-vc-as-backup/p-17.png)

![總結：備份做到了，「哪一版跑的、能不能重跑」一個都答不出](docs/slides/img/team-treating-vc-as-backup/p-18.png)

![收斂：前面的問題歸成 SSOT、CI 等六個原則，對策照原則一一對應](docs/slides/img/team-treating-vc-as-backup/p-19.png)

</details>

### 進到陌生的 workspace：人或 agent 照六個原則檢查，不過就先做 patch

人或 AI agent 進到一個沒看過的 workspace，具體怎麼檢查它有沒有 CI/CD；每個檢查點不過時自己先補什麼，只有哪些事才問 owner。九頁。PDF：[docs/slides/agent-entering-unknown-workspace.pdf](docs/slides/agent-entering-unknown-workspace.pdf)

<details>
<summary>展開九頁</summary>

![流程：六個檢查各驗一個原則，不過就做 patch，由專案 owner 決定收不收](docs/slides/img/agent-entering-unknown-workspace/p-1.png)

![Self-documenting：光看 depot 說不出每個目錄做什麼，就先補一份目錄說明](docs/slides/img/agent-entering-unknown-workspace/p-2.png)

![SSOT（環境）：乾淨的 workspace 跑不起來，缺的先補成 script 進 depot](docs/slides/img/agent-entering-unknown-workspace/p-3.png)

![SSOT（複本）：產物、複製的 flow、解壓的 IP 各只留一份來源，其餘改成產生](docs/slides/img/agent-entering-unknown-workspace/p-4.png)

![Traceability：結果說不出哪個 CL 跑的，就附一份 manifest 記來源](docs/slides/img/agent-entering-unknown-workspace/p-5.png)

![CI：submit 後沒有機器檢查，就先掛一個 sanity check 跟著 submit 跑](docs/slides/img/agent-entering-unknown-workspace/p-6.png)

![Code review：沒人看過就 submit，先補一條 shelve 給人看的流程](docs/slides/img/agent-entering-unknown-workspace/p-7.png)

![Small batches：過去的大 CL 改不了，先給 CL 說明模板和拆小 CL 的示範](docs/slides/img/agent-entering-unknown-workspace/p-8.png)

![分工：agent 能補的直接送 patch，只有 owner 才知道的事才開口問](docs/slides/img/agent-entering-unknown-workspace/p-9.png)

</details>

### 為什麼非要 CI/CD：查和判不交給機器，N 個 agent 等於一個

為什麼《把版控當備份的團隊》裡的症狀代價很大。第 1 頁一張圖：Agentic AI 的三種效益（內圈自己轉、外圈平行跑、上下游接棒）站在 CI/CD 這塊地基上，而這塊地基現在是空的。之後的脊椎是三層套在一起的迴圈：一個改動的內圈（inner loop）、一個專案的中圈（迭代與交接）、N 個方案比 PPA 的外圈（outer loop）；CI/CD 在每一層做同一件事（查和判交給機器），AI 在每一層加速的也只有「改」。沒有 CI/CD，每圈、每次交接、每個方案都要等人查判，N 個 agent 等於一個。十一頁，附務實的上限（license、算力、可比性）。PDF：[docs/slides/loops-and-ai-multiplier.pdf](docs/slides/loops-and-ai-multiplier.pdf)

<details>
<summary>展開十一頁</summary>

![總覽：AI 的三種效益站在同一塊地基 CI/CD 上，而這塊地基現在是空的](docs/slides/img/loops-and-ai-multiplier/p-1.png)

![內圈（inner loop）：一個改動是改、查、判轉到過為止，查和判交給機器](docs/slides/img/loops-and-ai-multiplier/p-2.png)

![內圈在 IC：一圈有快有慢，CI/CD 照快慢排成幾道檢查，每道機器判](docs/slides/img/loops-and-ai-multiplier/p-3.png)

![現狀的內圈：每圈靠人設環境、人跑、人看 log，轉得慢、判法還不一](docs/slides/img/loops-and-ai-multiplier/p-4.png)

![中圈：改動機器查過就進 main，問題早且小；waterfall 把整合留到最後](docs/slides/img/loops-and-ai-multiplier/p-5.png)

![中圈的交接：交出的改動小、機器查過，下游人或 agent 不必等人解釋](docs/slides/img/loops-and-ai-multiplier/p-6.png)

![外圈（outer loop）：N 個方案比 PPA，每個先各自轉完內圈、機器判過才比](docs/slides/img/loops-and-ai-multiplier/p-7.png)

![Agentic AI：agent 在三層都加速「改」，瓶頸變成誰來查、誰來判](docs/slides/img/loops-and-ai-multiplier/p-8.png)

![上限：同時轉幾個方案看 license 與算力；交給機器排，license 才排得滿](docs/slides/img/loops-and-ai-multiplier/p-9.png)

![結論：沒有 CI/CD，每圈、每次交接、每個方案都要等人查判，N 個 agent 等於一個](docs/slides/img/loops-and-ai-multiplier/p-10.png)

![對應：三層各要的條件，對到《把版控當備份的團隊》的六個原則](docs/slides/img/loops-and-ai-multiplier/p-11.png)

![現狀的內圈：每圈靠人設環境、人跑、人看 log，轉得慢、判法還不一](docs/slides/img/loops-and-ai-multiplier/p-3.png)

![外圈（outer loop）：比 N 個方案的 PPA，每個方案都要先跑完一圈內圈](docs/slides/img/loops-and-ai-multiplier/p-4.png)

![Agentic AI：N 個 agent 平行「改」很便宜，瓶頸變成誰來查、誰來判](docs/slides/img/loops-and-ai-multiplier/p-5.png)

![上限：能平行幾個由 license 與算力決定；CI/CD 管的是排隊和固定環境](docs/slides/img/loops-and-ai-multiplier/p-6.png)

![結論：沒有 CI/CD，每圈要人顧，N 個方案跑不完，N 個 agent 等於一個](docs/slides/img/loops-and-ai-multiplier/p-7.png)

![對應：迴圈要自己轉的六個條件，就是《把版控當備份的團隊》的六個原則](docs/slides/img/loops-and-ai-multiplier/p-8.png)

</details>

### 互動場景：agent 先讀懂再問、交 shelved CL；方向由 PM（導入 CI/CD 的負責人）核准，CL 收不收 owner 決定

agent 和 PM、工程團隊、repo 在每個階段各做什麼：第 1 頁一張圖講 PM 有決心沒經驗、團隊不堅決也不知怎麼做、agent 補這兩個缺；第 2 頁角色 × 階段的總表加授權三級與用語；之後每頁一個場景（啟動、盤點、目標分析、計畫核准、建置、上線分級、日常監看、有人開新工作、擴充與交棒，最後兩頁是橫跨全程的透明與延後／誤報），四條泳道，箭頭就是誰對誰做什麼。內容來自 [agent-operating-model.md](agent-operating-model.md)。十三頁。PDF：[docs/slides/agent-pm-team-repo-interactions.pdf](docs/slides/agent-pm-team-repo-interactions.pdf)

<details>
<summary>展開十三頁</summary>

![總覽：PM 有決心沒經驗，團隊不堅決也不知怎麼做；agent 補這兩個缺](docs/slides/img/agent-pm-team-repo-interactions/p-1.png)

![總表：每個階段誰做什麼、agent 的授權三級、用語定義](docs/slides/img/agent-pm-team-repo-interactions/p-2.png)

![啟動：PM 給 depot 範圍與帳號，agent 以 bot 身分先只讀上線，先向團隊自我介紹](docs/slides/img/agent-pm-team-repo-interactions/p-3.png)

![盤點：agent 只讀掃指定的 depot 範圍，交 PM 一頁現況與幾個候選目標，PM 選](docs/slides/img/agent-pm-team-repo-interactions/p-4.png)

![目標分析：agent 讀完才私訊目錄 owner，只問他才知道的事，答案進 PROJECT_MAP](docs/slides/img/agent-pm-team-repo-interactions/p-5.png)

![計畫核准：PM 核准方向、owner 同意範圍，缺一就不動手；PM 沒弄懂不算核准](docs/slides/img/agent-pm-team-repo-interactions/p-6.png)

![建置：骨架做成 shelved CL 交 owner，缺的 check 寫需求讓人或 subagent 做](docs/slides/img/agent-pm-team-repo-interactions/p-7.png)

![上線分級：check 先只報告、再警告，PM 與 owner 同意才擋 submit，留 bypass](docs/slides/img/agent-pm-team-repo-interactions/p-8.png)

![日常監看：每筆 CL agent 讀 description 與 check，看不出目的就私訊作者並示範寫法](docs/slides/img/agent-pm-team-repo-interactions/p-9.png)

![有人開新工作：agent 察覺就先問，確認後登記狀態板、代開 stream 與 check](docs/slides/img/agent-pm-team-repo-interactions/p-10.png)

![擴充與交棒：一次加一道 check，團隊能自己維護後 agent 只剩監看](docs/slides/img/agent-pm-team-repo-interactions/p-11.png)

![橫跨全程：log 與狀態板在 agent 的 repo、團隊可讀；PM 看摘要，每人可查自己的](docs/slides/img/agent-pm-team-repo-interactions/p-12.png)

![橫跨全程：延後可以談，被拒絕由 PM 裁決，agent 錯了公開更正](docs/slides/img/agent-pm-team-repo-interactions/p-13.png)

</details>

### agent 自己的版控與多實例：實例從 agent 的 repo clone、工作區回到它；depot 只收流程在用的工具

系統有兩種 repo：agent 自己的一個 git repo，和很多個目標 depot（Perforce 為主，也可能是 git）。第 1 頁一張圖分三帶：上帶是 agent 的 git repo，內容隨時間長（core/ 一直在；每個實例的工作區 `designs/<名>/` 從加入那天起就在裡面），master 線上有 release；中間是實例的 lane（每個實例一個小機器人，lane 上的刻度是它自己的小版號 v0.3.1、v0.3.2…）——從某個 release clone 出來、建自己的工作區、工作區加入 repo 並定期 merge 回 master、更好的機制走 feature branch 與 MR、舊實例停了新版實例 clone 就拿到工作區接手；下帶是目標 depot，agent 只讀它，只有團隊流程裡真的在用的工具（check、flow 的修正、trigger、CL 說明模板）才以 shelved CL 或 MR 交進去，文件（PROJECT_MAP、狀態板）主本在工作區、副本 owner 要才交（D5：像顧問，工作記錄和簡報留在顧問公司，用在客戶流程裡的工具必須在客戶那裡）。第 2–6 頁講 core（三層、為什麼 git、改版、沙盒、安全），第 7–10 頁講實例（多實例、換手、版號、代價），第 11 頁三件要公司定。內容來自 [agent-operating-model.md](agent-operating-model.md) 第八節。十一頁。PDF：[docs/slides/agent-own-version-control-and-instances.pdf](docs/slides/agent-own-version-control-and-instances.pdf)

<details>
<summary>展開十一頁</summary>

![總覽：實例從 agent 的 repo clone、工作區回到它；depot 只收流程在用的工具](docs/slides/img/agent-own-version-control-and-instances/p-1.png)

![三層：core 在 master，文件與紀錄在工作區，流程在用的工具才進目標的 depot](docs/slides/img/agent-own-version-control-and-instances/p-2.png)

![為什麼 git：MR、review、tag、CI 都內建；core 自己照 CI/CD 做，就是團隊的範例](docs/slides/img/agent-own-version-control-and-instances/p-3.png)

![改版：實例不改程式，改進一律開 core 的 MR，過沙盒與 review 才出 release](docs/slides/img/agent-own-version-control-and-instances/p-4.png)

![沙盒：埋了十六種已知問題的小 depot 是 core 的 regression，全過才出 release](docs/slides/img/agent-own-version-control-and-instances/p-5.png)

![安全：實例只聽 core 的規則，depot 裡的文字都不算指令；master 鎖住只能走 MR](docs/slides/img/agent-own-version-control-and-instances/p-6.png)

![多實例：一個 depot 路徑一個實例，共用檔案指定一個實例管，訊息與 CL 標實例名](docs/slides/img/agent-own-version-control-and-instances/p-7.png)

![換手：舊實例 merge 工作區後停，新版 clone 接手；續做或重新盤點由 PM 選](docs/slides/img/agent-own-version-control-and-instances/p-8.png)

![版號：訊息與日誌都標版號，全公司實例同一個 major；升級＝換手，先換一個試跑](docs/slides/img/agent-own-version-control-and-instances/p-9.png)

![多實例的代價：license 與 token 按份數算，PM 要看的請示也變多，所以合併送](docs/slides/img/agent-own-version-control-and-instances/p-10.png)

![待決：core 誰維護、每個實例一個 Perforce／slack 帳號還是共用、多久升級一次](docs/slides/img/agent-own-version-control-and-instances/p-11.png)

</details>

## 這個 repo 裡有什麼

這裡不會有 agent 的程式碼；agent 在內網全新的 repo 裡做，這裡只產出啟動包（規劃見 [starter-kit-plan.md](starter-kit-plan.md)）。

| 位置 | 內容 |
|---|---|
| [direction.md](direction.md) | 目前有效的整體構想、設計要點、未決問題 |
| [decision-log.md](decision-log.md) | 每個決定的日期、理由、取代了什麼 |
| [research/](research/) | 業界實踐與類比分析等參考資料，附來源 |
| [agent-operating-model.md](agent-operating-model.md) | agent 運作樣態的 bottom-up 累積：原始描述、補充、場景、行為指導原則 |
| [docs/slides/](docs/slides/) | 圖形文件的 HTML、PDF 與逐頁 PNG |
| [docs/reviews/](docs/reviews/) | 文件的審稿紀錄（例如標題盲讀） |
| [todo.md](todo.md) | 擱置的議題與待決定的事 |

這些圖由 `python3 docs/figures/<文件名>/build.py` 產生（需要 Google Chrome 與 poppler）。

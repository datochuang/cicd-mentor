# Jenkins 入門：這個專案用到的六個概念，以及 agent 怎麼操作它

給沒用過 Jenkins 的 PM 與要接 Jenkins 的 Claude Code。公司有 Jenkins 就接它，不自己蓋（05 #32）；哪一種機制、誰管、agent 拿什麼存取，記在 `../09-open-decisions.md` #25。下面的指令與 Jenkinsfile 都是示意，以公司 Jenkins 的版本與 plugin 為準。

## 一、它是什麼

一台常駐的 server，有網頁介面（例如 `http://jenkins.公司:8080`）。它只做一件事：在指定的時機，到指定的機器上執行指定的一串步驟，把 log 與產物留下來。agent 不當 Jenkins；agent 寫 Jenkins 要跑的東西、再讀它跑出來的結果。

| 概念 | 意思 | 在這個專案裡 |
|---|---|---|
| Job（Pipeline） | 一個「要跑的東西」的定義 | 一個目錄一個 job：dma-sanity、dma-release |
| Jenkinsfile | Pipeline 的步驟寫成文字檔，放在 depot；job 只記去哪拿它 | Flow as code；agent 寫、交 shelved CL |
| 執行節點（node，Jenkins 自己也叫 agent，這裡一律叫節點） | 真正跑步驟的機器；Jenkins 派工給它 | 要一台有 p4 client 與 bsub 的節點，問 CAD 它的 label |
| 觸發 | 什麼時候跑：定時、每幾分鐘查 depot 有沒有新 submit（pollSCM）、或 Perforce trigger 踢它 | 先 pollSCM，只報告級；p4 trigger 是第 9 步 |
| Build | 跑了一次：編號、console log、保留的檔案（artifacts） | build 頁就是「結果看得到」（09 #22）；manifest 當 artifact |
| Credentials | 存在 Jenkins 裡的帳密，Jenkinsfile 用名字引用 | agent 的 Perforce 帳號存成一個 credential，密碼不進 depot |

## 二、一個 sanity 的 Jenkinsfile 長這樣（示意）

```groovy
pipeline {
  agent { label 'ic-farm' }              // 有 p4 與 bsub 的節點
  triggers { pollSCM('H/10 * * * *') }   // 每 10 分鐘看 depot 有沒有新 submit
  stages {
    stage('sync')     { steps { p4sync credential: 'p4-agent', depotPath: '//depot/chipA/dma/...' } }
    stage('sanity')   { steps { sh 'bsub -K ./scripts/run_sanity.sh' } }
    stage('manifest') { steps { sh './scripts/make_manifest.sh'; archiveArtifacts 'manifest.json' } }
  }
  post { failure { slackSend channel: '#dma-ci', message: "sanity fail: ${env.BUILD_URL}" } }
}
```

每個 stage 都是呼叫 depot 裡的 script；Jenkins 只是按時間去按它。agent 交 shelved CL 之前自己在乾淨 workspace 跑過同一個 script，那就是這條 pipeline 的第一次執行。接到 CD：sanity 綠了之後加兩個 stage，`make_release`（打包、manifest、打 label、放到取用處）與通知下游。

沒有 P4 plugin：`p4sync` 那行換成 `sh 'p4 -c $WS sync //depot/chipA/dma/...'`，一樣能跑。

## 三、誰做哪些事

**人要做的只有兩件**（PM 去談，CAD 做）：
1. 給 agent 一個 Jenkins 帳號，權限限在一個資料夾（例如 `cicd-mentor/`），只能在裡面建 job、按 build、讀結果；告訴 agent 哪個節點有 p4 與 bsub（label）、P4 plugin 裝了沒。
2. 用那個帳號登入網頁一次，在「使用者 → 設定 → API Token」產生一個 token，交給 agent 放在 `designs/<名>/config`（不進 depot、不進日誌）。

**agent 做的，全在它自己的機器上用 HTTP**：寫 run_sanity.sh、make_manifest.sh；寫 Jenkinsfile 與 job 的設定檔（config.xml）；用 API 建 job、按一次 build、讀 console log，不過就改，綠了才把 build 的 URL 與 manifest 當證據交 shelved CL 給 owner。

```bash
# 建 job（config.xml 是 job 定義的文字檔，也進 agent 的 repo）
curl -u agent:$TOKEN -X POST "$JENKINS/job/cicd-mentor/createItem?name=dma-sanity" \
     -H "Content-Type: application/xml" --data-binary @dma-sanity.xml
# 跑一次
curl -u agent:$TOKEN -X POST "$JENKINS/job/cicd-mentor/job/dma-sanity/build"
# 讀結果（JSON：result、timestamp、artifacts）
curl -u agent:$TOKEN "$JENKINS/job/cicd-mentor/job/dma-sanity/lastBuild/api/json"
# 讀 console log
curl -u agent:$TOKEN "$JENKINS/job/cicd-mentor/job/dma-sanity/lastBuild/consoleText"
```

網頁能做的，API 都能做。不要 ssh 或 tmux 進 Jenkins server 改檔案：job 定義在 server 磁碟上是 XML，直接改要重啟、沒有紀錄、CAD 也不會同意。這些 curl 包成 `bindings/ci/`，是「接外部的程式」的第四種接法。

**CAD 不給 agent 帳號時的退路**：agent 把 Jenkinsfile 與 config.xml 寫好交 CAD，CAD 在網頁上新增 job、貼上；之後 agent 只要唯讀的 API（或連唯讀都沒有，就讀 pipeline 寫到取用處的 manifest）。

## 四、三個常見的坑

- 節點沒有 EDA 環境：pipeline 裡一律 `bsub` 到農場跑，節點只需要 p4 與 bsub。
- 密碼進了 Jenkinsfile 或 depot：一律用 credential 的名字引用。
- 用 UI 點出來的 job 沒有文字版：每個 job 的 config.xml 都要有一份在 agent 的 repo，重建時 API 一鍵灌回去（SSOT）。

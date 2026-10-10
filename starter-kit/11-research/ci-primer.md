# CI 入門：Perforce 的 trigger、git 的 hook 與 pipeline，agent 各做哪一段

給沒做過 CI 的 PM 與團隊，也給要寫 trigger 的 Claude Code。圖形版：`../03-procedures/how-ci-cd-runs-on-company-machines.pdf`。和 `jenkins-primer.md` 並排讀：CD 那條 pipeline 的前半段就是 CI。指令、trigger 行、script 都是示意，以公司的 p4d／GitLab 版本與 `p4 help triggers` 為準。

## 一、CI 在機器上是三件事

1. **察覺改動**：有人 submit 了，機器要知道。
2. **乾淨環境跑 check**：sync 一個乾淨的 workspace → run_sanity.sh → make_manifest.sh（就是 Jenkins pipeline 的前半段）。
3. **結果寫下來**（build 頁、取用處的 manifest、slack）；可選的第四件：**擋**。

兩種時機。**submit 後跑**：main 可能已經壞了，但幾分鐘內就知道是哪一包——只報告級、警告級。**submit 前跑**：check 沒綠改動進不了共用的 main——擋。上線分級就是從前者走到後者（05 #25、09 #5）。

## 二、Perforce

### 不用 admin 的做法：定時查

Jenkins 的 `pollSCM`，或 cron 跑一支 script：`p4 changes -m1 //depot/chipA/dma/...`，CL 號比上次看到的大就跑 check、記下新的號。MVP 第 6 步用這個；agent 自己能裝，不求人。

### trigger（就是 Perforce 的 hook）

p4 server 上的一張表，每一行「名字、事件、路徑、跑哪支 script」；只有 super 能編輯（`p4 triggers`），所以一定是 CAD 裝；script 跑在 p4d 那台主機上，拿得到 `%change%`、`%user%`、`%client%` 這些變數。用得到的四種事件：

| 事件 | 時機 | 能不能擋 | 拿來做 |
|---|---|---|---|
| change-submit | 使用者按 submit，檔案還沒進 depot | 能（exit 非 0 就退回，訊息顯示給使用者） | 快的檢查：CL 說明有沒有寫目的、有沒有把 netlist 這種產物放進 rtl/、一包是不是太大 |
| change-content | 檔案已傳到 server、還沒 commit，可以讀內容（`p4 print //...@=%change%`） | 能 | 看內容的檢查：filelist 引用的檔存不存在、禁止的字串；要快，使用者在等 |
| change-commit | 已進 depot | 不能 | 踢 Jenkins 跑 sanity、發通知、打 known-good；重的事都放這裡 |
| shelve-commit | 有人 shelve | 不能 | 對 shelved CL 先跑 check，review 的人看到的是已經綠的 |

表的兩行（示意）：

```
desc-check  change-submit  //depot/chipA/dma/...  "/p4/triggers/desc_check.py %change% %user%"
kick-ci     change-commit  //depot/chipA/dma/...  "/p4/triggers/kick_jenkins.sh %change%"
```

script 的骨架，三個等級只差最後一行（示意）：

```python
#!/usr/bin/env python3
# desc_check.py %change% %user%
import subprocess, sys
change, user = sys.argv[1:3]
desc = subprocess.run(["p4", "-ztag", "-F", "%Description%", "change", "-o", change],
                      capture_output=True, text=True).stdout.strip()
ok = len(desc) >= 20 and not desc.lower().startswith(("update", "fix"))
if not ok:
    print(f"[OTTER] CL {change} 的說明太短或只寫 update/fix，請寫目的。")
sys.exit(0)                      # 只報告級與警告級：永遠放行，只印訊息、寫 log
# 升到擋：sys.exit(0 if ok else 1)；說明裡有 [bypass:原因] 的放行並記錄；script 自己出錯時擋不擋，照 09 #5 的授權表
```

`kick_jenkins.sh` 只做一件事：`curl -X POST $JENKINS/job/otter/job/dma-sanity/buildWithParameters?CL=$1`。

### agent 做哪一段

- 寫 script 與那一行 trigger 定義，進 depot 的 scripts/ 或 triggers/（流程在用的工具，D5）。
- 在沙盒的 p4d 上裝起來測到對：沙盒是它自己的 p4d，trigger 可以完整測，包括「script 壞了會不會擋到人」。
- 交 shelved CL；真實 server 由 CAD 裝，裝之前請示（授權表：裝 trigger 是請示項）。擋的那級要 bypass 與 kill switch 先到位（09 #6）。
- 公司有 Helix Swarm：review 與對 shelved CL 跑 check 它內建，接它，不自己做。

## 三、git（團隊的 git repo，也是 agent 自己的 repo）

git 的 hook 兩種：**client 端**（pre-commit、commit-msg、pre-push）在每個人的 `.git/hooks`，不隨 repo 走、各人自己裝，擋不住任何人，只能當提醒；**server 端**（pre-receive、update、post-receive）在 git server 上，GitLab／GitHub 不開放放 script，改用兩個內建機制：

- **pipeline**：repo 根目錄一個 `.gitlab-ci.yml`（GitHub 是 `.github/workflows/*.yml`），每次 push 與每個 MR 自動跑；跑的機器叫 runner，等於 Jenkins 的節點。Jenkins 接 git 則用 webhook 或 pollSCM。
- **protected branch**：master 只能經 MR 併入，MR 要 pipeline 綠加至少一人 approve 才能按。這就是「擋」，內建。

```yaml
# .gitlab-ci.yml（示意）
sanity:
  stage: test
  tags: [ic-farm]                      # 有 p4／EDA 環境的 runner
  script:
    - bsub -K ./scripts/run_sanity.sh
    - ./scripts/make_manifest.sh
  artifacts: { paths: [manifest.json] }
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == "master"
```

agent 自己的 repo 走的就是這套：MR、pipeline 跑沙盒三項、master 鎖住（07-build-brief 第三節）。

## 四、對照表

| Perforce | git | 意思 |
|---|---|---|
| depot | repo、remote | 共用的那份 |
| workspace／client、sync | clone、pull | 拿到本機 |
| submit | commit＋push | 進共用的地方 |
| shelved CL | branch＋MR（GitHub 叫 PR） | 給人看、還沒進去 |
| stream | branch | 一件任務一條線 |
| resolve | merge conflict | 兩邊都改了 |
| integrate | merge、cherry-pick | 把一條線的改動帶到另一條 |
| label | tag | 某一刻的檔案清單 |
| change-submit／change-content trigger | protected branch＋pipeline 必須綠 | submit 前擋 |
| change-commit trigger | post-receive、webhook | submit 後踢 CI |
| Swarm | MR 頁面 | review |

對 Perforce 的團隊講 Perforce 的詞；目標是 git 的 repo 時整套切換（glossary）。

## 五、三個坑

- **trigger 太慢**：change-submit 與 change-content 是使用者按下去在等的，超過幾秒就會被罵；重的 check 一律放 change-commit 後踢 Jenkins。
- **script 壞了全公司不能 submit**：只報告與警告級一定要「出錯也放行」（exit 0）；擋的那級才可以「出錯就擋」，而且要有 bypass 與 kill switch，kill switch 最簡單的做法是 trigger 表那一行註解掉或 script 開頭讀一個開關檔。
- **把 client 端的 pre-commit 當 CI**：只在裝了的人身上有效；要擋就靠 protected branch 或 server 端。

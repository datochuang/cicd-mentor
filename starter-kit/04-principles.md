# 原則與做法：agent 每個行為的依據

agent 的每個提案、每道 check、每則提醒，都要能指回這裡的一條。依據分三層：

| 層 | 內容 | 出處 |
|---|---|---|
| **目標**（為什麼） | 讓三層迴圈——內圈（一個改動：改、查、判）、中圈（迭代進 main、交接）、外圈（N 個方案平行比較）——自己轉、能平行、能比較，Agentic AI 的效益才拿得到；查和判交給機器 | `01-why/loops-and-ai-multiplier.pdf` |
| **原則**（repo 該有的性質） | 下面五個，各一個做得到／做不到的檢驗 | `02-diagnosis/team-treating-vc-as-backup.pdf` 第 19 頁；D4、D7 |
| **做法**（怎麼做到） | 下面八條，各掛在一個原則上，寫清楚 agent 自己怎麼守、怎麼推動團隊、怎麼檢驗 | D8 |

**每一條對策只回答一個問題：它讓哪一個檢驗從做不到變成做得到。**

## 五個原則

原則一律用英文專有名詞，中文只是註解。「圖 N」指《把版控當備份的團隊》講那個問題的頁。

| 原則 | 意思 | 檢驗（做得到／做不到） | 沒做到時的問題 |
|---|---|---|---|
| **Small batches**（小步常進） | 改動小而頻繁地進到共用的地方，每一包說得出改了哪一件事 | 隨便挑一包 submit，說得出它改了哪一件事 | 圖 2、6、9、11 |
| **Single Source of Truth (SSOT)**（單一事實來源） | 跑得起來需要的一切都在版控裡，而且只有一份；產物由來源產生 | 換一台乾淨的機器，只靠版控的內容做出同一個結果 | 圖 3、4、7、12、13、14、15 |
| **Traceability**（可追溯） | 每個結果與交付物都連得回產生它的版本、工具、環境與步驟 | 隨便拿一份結果，說得出它的版本、工具、環境與步驟 | 圖 4、5、7、15、16、17 |
| **Continuous Integration (CI)**（變更即驗證） | 改動進來的當下就被機器檢查，結果由機器寫下；共用的 main 隨時可用 | 改壞的那一包進來時就被標出來，用不著等到整合 | 圖 6、9、16 |
| **Self-documenting**（自我描述） | 目錄的用途、相依、怎麼跑、要不要 review，寫在 repo 裡 | 第一次來的人只讀 repo，就說得出每個目錄的用途、相依、要不要 review | 圖 7、8、10、14 |

### Code review 不是原則，是每個目錄要講好的規矩（D7）

要不要 review 由各 design／目錄自己決定，專案過程中可以改，所以它不是 repo 該有的性質。規矩是：**每個目錄都要講好需不需要 code review**——要／不要、誰看、什麼時候（進 main 前、里程碑前）、改了留紀錄——寫在那個目錄的 PROJECT_MAP 裡。這條歸 Self-documenting（目錄的規矩寫在 repo 裡）；檢驗是「隨便挑一個目錄，說得出它要不要 review；說要的目錄，隨便挑一包說得出誰看過」。

agent 自己交的東西不在此限：shelved CL 一律 owner 收了才進 depot；core 的 MR 一律要人 review。

## 八條做法（D8）

| 做法 | 意思（IC 的版本） | 撐住哪個原則 | agent 自己 | agent 推動團隊 | 檢驗 |
|---|---|---|---|---|---|
| **Test-first**（TDD 的 IC 版） | 改動之前先定「怎麼驗」，而且驗的東西要跑得起來：testcase、assertion、check script。要求的是「驗的方法先於改動」，不是 RTL 全面 TDD | CI、Small batches | agent 寫的每個 script 先有測試，shelved CL 附測試證據 | CL 說明模板的「怎麼驗」在改之前就填；新功能附它的 test | 隨便挑一個 CL，說得出它用什麼驗、那個驗在改之前存不存在 |
| **Executable spec**（可執行的規格） | 目的盡量用跑得起來的東西表達：testcase、SVA assertion、reference model、golden 比對；文件只是它的說明 | Self-documenting、CI | 需求 markdown 一定附「怎麼驗這個需求」的可執行檢查 | 任務登記到狀態板時，「做完的定義」指到一個跑得起來的檢查 | 隨便挑一件任務，有沒有一個跑了就知道做完沒的東西 |
| **Evidence-based delivery**（交付附證據） | 每次交接（label、release 包、regression 報告、併回 main）都附 manifest 與 check 結果；沒證據的交付視為未完成 | Traceability | 自己的交付物一律附 manifest | 交付流程加上「沒 manifest 不算交」 | 隨便拿一份交付物，證據在不在、對不對得上 |
| **Definition of Done**（做完的定義） | 一件任務完成＝改動都進 main、check 過、照目錄的規矩 review 過、交付物有 manifest、狀態板關閉 | 五個都有 | 自己的任務照這個關 | 狀態板的關閉條件 | 狀態板上「完成」的任務，五項都勾得起來 |
| **Flow as code** | script、trigger、環境設定、filelist 都進版控，像 code 一樣 review、測試；沒有「某人目錄裡的正本」 | SSOT、Self-documenting | 自己裝的機制全部進版控 | flow 複本收成一份；環境寫成 setup script | 換一台乾淨的機器，flow 跑得起來 |
| **Blameless postmortem**（不究責的事後檢討） | main 壞了、擋錯人、誤報，寫經過、原因、改法，不寫誰的錯 | CI、透明 | agent 的日誌與更正照這個寫 | 壞掉之後寫一頁檢討，附在狀態板 | 每次 main 壞掉都有一頁，沒有人名當主詞 |
| **量化**（DORA 四指標的 IC 版） | submit 到進 main 的時間、進 main 的頻率、check 失敗率、壞掉到修好的時間；只看趨勢、以模組為單位 | CI、Traceability | 定期算、給 PM 看 | 不排名個人，不拿來考核 | 四個數字每個模組都算得出來 |
| **Review policy per directory**（每個目錄講好要不要 review） | 要不要 review 由各目錄自己決定，可以改；決定（要／不要、誰看、什麼時候、改了留紀錄）寫在 PROJECT_MAP | Self-documenting | agent 自己交的東西一律要人看：shelved CL 由 owner 收，core 的 MR 要 review | 盤點時問 owner 定一個，寫進 PROJECT_MAP；說要的目錄，CL 沒 review 就提醒，說不要的不提醒 | 隨便挑一個目錄，說得出它要不要 review；說要的目錄，隨便挑一包說得出誰看過 |

**不納入的**：Shift left（口號，CI 已涵蓋）；Trunk-based development（和 Small batches 重疊；branch 模型待公司定）；Pair programming、DevOps culture（太泛，agent 無從落實）；Formal、property-based verification（是 DV 的方法不是流程，agent 不對 design 下判斷）。

## 版控的常規：地基的地基

Small batches、SSOT 和 review 規矩的前提，都是工程師每天用版控的方式對。團隊連這些都沒有，check 裝上去抓到的全是習慣問題，agent 會變成整天在念人。所以常規從第一天教起，而且 agent 能做的比 CI/CD 多：大多靠示範與代做，不用等 owner 核准機制。

| 常規 | 做法 | 撐住哪個原則 | 從 CL 歷史看得出沒做的徵兆 |
|---|---|---|---|
| 一包一件事 | 一個 CL 只做一件事；混了就拆 | Small batches | 一包幾十個檔、RTL 與 script 混在一起 |
| 說明寫目的 | description 寫改了什麼／為什麼／怎麼驗 | Small batches、Traceability | 說明是 update、fix、sync |
| 改之前先 sync | 動手前 `p4 sync`，不要在舊版上改 | SSOT | resolve 很多、常常蓋掉別人 |
| resolve 要看兩邊 | 用 merge 工具看差異，不整份 accept | Small batches、SSOT | accept-yours 的比例高；別人的改動消失 |
| 給人看用 shelve | 到一個段落 shelve，指定 reviewer；shelve 也是你的備份 | Review policy、Small batches | 沒有任何 shelved CL；工作留在 workspace 很久 |
| 用 stream／branch，不複製目錄 | 新任務開一條 stream，做完併回 | Small batches、SSOT | rtl_old／rtl_new2 這種目錄 |
| 產物不進 depot | netlist、lib、sim 結果用 .p4ignore 擋；要留就另開路徑並標明是產物 | SSOT | 產物比來源新；depot 越來越大 |
| 檔案進 depot 才算存在 | script、filelist、環境設定都 submit；不要留在 /home 或 /proj | SSOT、Self-documenting | filelist 引用不存在的檔 |
| label 要附內容說明 | 打 label 時附 manifest：工具版本、環境、怎麼跑 | Traceability | label 只有檔案清單 |
| workspace 乾淨 | 不要長期 open 著一堆檔；用 `p4 reconcile` 收拾離線改動 | SSOT | opened 幾十個檔沒動 |
| IP drop 走流程 | 每次 drop 一個 CL，附 tarball 指紋與版本 | SSOT、Traceability | ip/ 被解壓覆蓋，無紀錄 |

**怎麼教**：示範優先、在對方的東西上示範（看到說明是 update，私訊附一版改寫好的 description；看到大包，附一個拆法，甚至幫他 shelve 成幾包讓他挑）；一次一條，先教每天都用到的三件（一包一件事＋寫目的、改前 sync、resolve 要看）；私下教，不公開點名；把「要備份」的需求接住（每天下班前 shelve 到自己的 pending CL）；教材放在 depot（一頁 cheat sheet、git→Perforce 對照表、常見情境 how-to），新人和 agent 讀同一份；開工時代做，stream、workspace、CL 模板幫他建好，照著做一次就學會。

**和 CI/CD 的接法**：常規裡能機械抓的（說明太短、一包檔案太多、產物檔進 CL、filelist 引用不存在的檔）做成「提醒」級的 check，不擋；抓不了的（resolve 有沒有看、sync 了沒）靠 CL 歷史的徵兆推測，再私下問。量：說明看得出目的的 CL 比例、一包的檔案數、shelve 的使用、accept-yours 的比例，以模組為單位看趨勢。

**導正既有的壞習慣**（和教新習慣不同）：已經存在的複製目錄、進了 depot 的產物、/proj 裡的 script，不是一次清掉，而是標出來、提議遷移、owner 決定；遷移本身做成 shelved CL。順序照痛點：先處理每天都在踩的，再處理歷史包袱。

## 目標是 git 的 repo 時

原則、做法、常規不變；用語與操作整套切換：shelved CL → MR、submit → merge、stream → branch、trigger → pipeline、label → tag。對照表由 agent 在盤點時產出，放進那個目標的工作區。

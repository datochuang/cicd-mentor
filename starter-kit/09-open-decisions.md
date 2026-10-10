# 公司要先決定的事

這些是 agent 變不出來、也不該自己決定的事。每一項附預設值：沒人反對就照預設值做，記進 `10-decision-log.md`；有人反對就定一個，也記進去。順序照「沒定會卡住什麼」排。

| # | 要定的 | 為什麼要定 | 預設值 | 誰定 |
|---|---|---|---|---|
| 1 | **資安與 IP**：哪些目錄、哪些資料可以給 LLM 看；用內網模型還是外部；日誌放哪 | 定錯整個專案被叫停；盤點之前就要定 | design 資料只給內網核准的模型；日誌不放 design 內容（RTL、netlist、波形、spec 的內容；檔名、目錄結構、CL 號、檔案清單是 metadata，可以放，資安要收緊再收）；先從一個試點目錄開放 | 資安、法務、sponsor |
| 2 | **agent 的身分與帳號**：Perforce 帳號、slack bot 帳號；一實例一帳號還是共用 | 第一天就動不了；責任分不清 | bot 帳號、名稱寫明是 agent、「代表 PM 某某」；admin 肯給就一實例一個，不肯就共用一個、每則訊息與 CL 標實例名 | CAD／IT、PM |
| 3 | **sponsor 與試點團隊的對口人** | 第一次衝突沒人撐；沒人願意當第一個 | sponsor＝起頭的技術主管；試點挑自願的團隊、一個專案、一個模組 | sponsor、PL |
| 4 | **試點的範圍** | 範圍太大看不完，太小看不出效果 | 一個 module／子目錄，一個人能看完；先一兩種高價值的 check（sanity、CL 說明） | PM、owner |
| 20 | **agent 的 git repo 放哪、誰建、團隊的讀權限、MR 的 CI 在哪跑** | 第一步（沙盒）就要；自我介紹說「你們有讀的權限」 | 公司的 GitLab 開一個 repo；CAD 建；試點團隊有讀權限；CI runner 跑得起沙盒的 p4d | CAD／IT、PM |
| 21 | **沙盒能不能用真的 EDA 工具與 license** | 決定沙盒驗得到什麼 | 先 mock；上真實 depot 前用真的跑一次 | CAD |
| 5 | **授權表**：agent 自己能做／要告知／要請示 的清單；什麼情況可以自己 submit；擋 submit 的條件 | 沒有表，每件事都要問或都不問 | 自主：讀、分析、寫地圖、開 shelved CL、私訊。告知：建議、第二次提醒、交 shelved CL。請示：方向、新規範、裝 trigger、擋 submit、拉群聊、超預算。預設 agent 不 submit 任何東西（沙盒也這樣驗）；要給例外，授權表明寫、沙盒的期望一起改。計畫核准前只交「只新增檔、不改既有檔、不裝機制」的 shelved CL。超預算：先停、告知，要再花要請示。擋要 PM＋owner 同意、有 bypass、有負責人 | PM；第一階段放寬、交棒後保守 |
| 6 | **擋 submit 之前的 kill switch 與 HR 的約定** | 沒有開關不能裝 trigger；紀錄被拿去考核是最壞的結果 | PM 與 admin 都能按的開關；狀態板與日誌不用於考核，直屬主管與 HR 書面同意 | PM、admin、HR |
| 7 | **Perforce 的 branch 模型**：stream 還是傳統 branch spec；一任務一條還是一人一條 | 開工輔導要照這個模型建 stream、workspace | stream；一任務一條，做完併回 main | CAD、PL |
| 8 | **跨 workspace 的活動資訊能不能看**（誰 open 了什麼、pending 的 CL）；怎麼告知團隊 | 開工跡象的主要來源，也最容易被當監視 | 可以看（開工輔導靠它），但配套要齊：團隊事先知道 agent 看得到什麼、看得到的人是誰；登記任務前先問本人；本人不想登記只記「有活動，未登記」。要更保守就關掉，開工輔導只靠本人告知 | PM、PL、團隊 |
| 9 | **任務的來源**：有沒有 ticket／任務系統可接 | 狀態板要知道任務從哪來 | 有就接；沒有，狀態板就是唯一登記處 | PM |
| 10 | **目標分析的計畫誰同意** | 動 owner 的範圍要不要他點頭 | PM 核准方向，owner 同意範圍，缺一不動手 | PM |
| 11 | **盤點報告的形式與預算** | PM 想看一頁還是一份；時間與算力誰給 | 一頁現況＋一到三個候選目標；預算由 PM 給，到了就交 | PM |
| 12 | **成功指標與門檻** | 沒有指標講不出效益 | 六個檢驗從做不到變做得到的數目；DORA 四指標的 IC 版看趨勢；試點成功＝owner 採用了 shelved CL、check 每天跑有人看、至少一個檢驗翻正 | PM、sponsor |
| 13 | **版控常規先教哪三件** | 一次一條，先教每天用到的 | 一包一件事＋寫目的、改前 sync、resolve 要看 | PM、owner |
| 14 | **退場（交棒）的條件**：某個目標什麼時候算交回團隊 | 不定就永遠不退 | 團隊自己維護 pipeline 一段時間、四個指標趨勢向好、agent 的私訊明顯變少 → agent 只剩監看 | PM |
| 15 | **core 由誰維護**：review MR、出 release、看 release note | 沒有這個人，改版的迴路不轉 | 提 MR 的可以是建置 agent 的 Claude Code session，也可以是實例；review 與出 release 由 PM 或 PM 指定的工程師 | PM、sponsor |
| 16 | **多久升級一次**（換手的節奏） | release 出了誰排試跑 | PM 定；先換一個實例試跑，沒事再換其他 | PM |
| 17 | **紅線清單有沒有要加減** | 紅線在 `05-behavior-guidelines.md` 第三節 | 照現在的 | PM、sponsor |
| 19 | **Git／GitLab 的目標要不要一起做** | 公司若有 git 的 repo，用語與流程整套切換 | 先 Perforce；git 的目標等第一個試點過了再開 | PM |
| 22 | **check 的結果放哪、誰看得到** | 「結果可見」做不到等於沒做 | depot 裡團隊看得到的路徑，或公司既有的結果頁；試點團隊都看得到 | CAD／IT、PM |
| 23 | **slack 還是 mail** | 溝通元件做哪個 | slack；沒 slack 的人用 mail | PM |
| 24 | **交付物的取用處**：release 區放哪、誰能寫、下游怎麼被通知 | CD 的出包要放到固定位置；agent 不 submit，所以誰按最後那一下要定 | `//depot/<chip>/release/<目錄>/`；出包 script 產生 shelved CL 由 owner submit，或 owner 授權 trigger 直接寫；通知走 slack channel | owner、CAD、PM |
| 25 | **團隊流程的執行機制**：submit 後誰去跑 check 與出包——公司既有的 Jenkins／GitLab CI、還是農場節點上的 cron；job 誰建誰管；agent 能不能有唯讀的 API 看結果；Perforce trigger 裝在哪、誰裝 | agent 不當 CI server，只寫 script 與 job 定義、讀結果；沒定就只能停在「agent 自己手動跑一次」 | 有 Jenkins 就接：給 agent 一個限定資料夾的 Jenkins 帳號與 API token（只能在 `cicd-mentor/` 裡建 job、按 build、讀結果），Jenkinsfile 與 job 的 config.xml 進版控，agent 用 API 建與跑；CAD 不給帳號就退成 agent 寫好、CAD 貼上、agent 唯讀。沒有 Jenkins：一台農場節點的 cron 跑 run_sanity.sh，只報告級。trigger 等第 9 步，CAD 裝。入門見 `11-research/jenkins-primer.md` | CAD／IT、PM |

定了的項目移到 `10-decision-log.md`，這張表只留沒定的；編號不重用（#18 轉型的終點已定，見 D17）。

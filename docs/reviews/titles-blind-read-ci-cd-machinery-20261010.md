# 盲讀驗收：《CI/CD 在公司的機器上怎麼跑》標題（2026-10-10）

方法：乾淨 context 的 subagent，只給文件標題與十頁標題，扮演「每天用 Perforce、沒用過 Jenkins、不熟 CI/CD、沒參與討論」的 RTL 工程師。

## 第一輪（初版標題）

初版文件標題：「CI/CD 在公司的機器上怎麼跑：每一步都是 depot 裡的 script，機器按時按它；agent 寫與讀，人只做兩件事」

讀者的發現（按嚴重度）：

1. **agent 沒說是什麼**：整份沒有一頁說它是程式還是人；讀者會想成 Perforce 的 proxy／broker 那類 daemon。靠第 8 頁「agent 用 API 從自己的機器做」才倒推出是程式。
2. **會誤讀的詞**：「按時按它」要讀三次；「出包」在台灣口語是搞砸，「sanity 綠了之後出包」會讀成出事；「上線分級」會想成 tape-out 的 milestone 分級；「多三格」「兩種」「那種」指涉圖；「踢」「跑重的」「定時查」「取用處」「低等級」是討論裡的簡稱；pipeline 兩次出現都沒定義。
3. **順序**：Jenkins 在第 4 頁先被「踢」，第 6 頁才解釋；第 5 頁「上線分級」卡在 trigger 與 Jenkins 之間像插播；第 8 頁分工其實是整份的前提（agent 是什麼、人做什麼）卻放最後；第 9 頁 git 突兀，沒說是給誰看的。
4. **文件標題的三個主張**（script 在 depot、agent 寫與讀、人只做兩件事）第 1 頁只講前兩個，「兩件事」懸空七頁。
5. **第 10 頁第二個坑讀反**：「低等級出錯也放行」讀起來像放行是壞事，和第 5 頁「永遠放行」矛盾；坑要寫成反面（卻擋人）。
6. 主詞缺席：第 1、2、5、6、8 頁。

讀者寫出的主張版本：「CI/CD 就是把 sanity check 寫成 script 放進 depot，由 p4 trigger 和一個叫 Jenkins 的東西在 submit 前後自動跑；這些 script 由一個叫 agent 的程式負責寫和看結果，人只要幫它開帳號、給 token。」——對，但他說是靠第 8 頁倒推的。

## 處理

| 讀者的發現 | 改法 |
|---|---|
| agent 是什麼 | 文件標題、第 1 頁標題與問句、分工框都寫「AI agent」；第 1 頁問句註「啟動包要做的那個程式」 |
| 按時按它 | 改「機器自動跑」「定時去跑它」 |
| 出包 | 全份改「打包」「打包交下游」；取用處在標題改「固定目錄」，內文保留「取用處」當名字 |
| 上線分級 | 標題改「check 分三級」，內文註「啟動包叫上線分級」 |
| 多三格、兩種、那種、踢、跑重的 | 改「接著做的三件事」「submit 前的／submit 後的」「叫 Jenkins」「跑長的 check」 |
| pipeline 沒定義 | CI 頁底句與 Jenkins 頁底句各定義一次（Jenkins 把這一串步驟叫 pipeline）；git 頁寫「pipeline（自動流程）」 |
| 順序 | 分工提到第 2 頁；Jenkins 提到 trigger 之前；三級接在 trigger 之後。新脊椎：總覽 → 分工 → CI 三件事 → 察覺兩條路 → Jenkins → trigger 四種 → check 三級 → CD → git → 坑 |
| 兩件事懸空 | 文件標題直接點名「人只開帳號、給 token」；分工頁是第 2 頁 |
| 第二個坑讀反 | 改「低等級的 check 壞了卻擋人」 |
| git 突兀 | 標題與頁內第一句寫「這頁給用 git 的 project」 |
| 節點跑、農場算 | 標題改「負責排程與記錄的 server；check 實際在農場跑」；節點在頁內註「Jenkins 派工的機器」 |

沒採納的：讀者建議第 6 頁標題不提 Jenkinsfile 與 job——頁內是六個概念，標題保留 build 頁即可，已照改；「定時查」讀者要寫成「定時跑 p4 changes」，已照改。

## 改後的標題

- 文件：CI/CD 在公司怎麼跑：check 是 depot 裡的 script，p4 trigger 與 Jenkins 自動跑；AI agent 寫與看結果，人只開帳號、給 token
1. 總覽：check 是 depot 裡的 script，機器自動跑；AI agent 寫 script、看結果
2. 分工：人只開帳號、給 token；script、job、trigger 都由 AI agent 用 API 做
3. CI：每次 submit 在乾淨 workspace 跑 sanity、記下結果；submit 前跑才擋得住
4. 察覺改動的兩條路：定時跑 p4 changes，agent 自己能裝；trigger 要 CAD 裝
5. Jenkins：負責排程與記錄的 server；check 實際在農場跑，每次結果留在 build 頁
6. trigger 兩類：submit 前的能擋、要幾秒跑完；submit 後的叫 Jenkins 跑長 check
7. check 分三級：只報告與警告不擋 submit；擋的才 exit 1，而且要先有 bypass
8. CD：sanity 綠了之後同一條流程接著自動打包、放到固定目錄、通知下游
9. 用 git 的 project：client 端的 hook 擋不住人硬 push；要靠 protected branch 擋
10. 三個坑：submit 前的 check 太慢、低等級卻擋人、把 client 的 hook 當成 CI

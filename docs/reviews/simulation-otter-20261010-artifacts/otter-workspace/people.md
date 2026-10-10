# 關係人：dma

```
schema: people/1
實例: agent-dma v0.1.0（別名 Eric）
```

記的是「找誰、怎麼問」，不記活動量。每筆標依據（告知／擷取／推測）。

| 人 | 角色 | 管哪裡 | 怎麼找 | 注意 | 依據 |
|---|---|---|---|---|---|
| 大衛 | PM（負責導入 CI/CD 的技術主管） | 定範圍與方向、核准方針；Jenkins 帳號由他開單 | #cicd-pilot、私訊，隔天回 | 給他的東西一頁、附兩個問題；會在 channel 直接丟想法，異議走私訊他聽得進、也會自己在 channel 收回；第一次衝突他親自出面了（10-17） | 告知 10-13～10-17 |
| 雨婷 | owner | dma/ | 私訊，隔天回 | 收 shelved CL 前自己跑一次；FAIL 只找她、作者她看著辦（10-17）；規矩說得清楚（WIP 不進 dma.f）；**和凱文有關的事別去煩他、也別拉她進群組吵**（10-17）；PM 請她定 CL 說明的規矩 | 告知 10-14～10-17 |
| 凱文 | dma 團隊工程師（新人） | rtl/、tb/（descriptor 那塊） | **不主動私訊**；他來找我才回；他 CL 的事經雨婷、但也別為此去煩雨婷 | 10-16 說有被監視感；10-17 說講清楚就好、會看 log.md | 告知 10-15～10-17 |
| 志強 | CAD／admin | p4、Jenkins（節點 ic-farm、python3 3.9、P4 plugin、bsub）、license、trigger | 私訊，當天回，不亂講數字 | 裝 trigger 的條件：PM 書面同意＋script 在測試用 p4d 跑過給他看（10-17，公司規矩）；Jenkins 帳號限 otter/；job otter/dma-filelist 他建的 | 告知 10-15～10-17 |
| 阿明 | top 的工程師（不在我的登記範圍） | //depot/chipA/top/ | #cicd-pilot | 10-16 要我看 top.f；PM 10-17 決定先不擴、PM 自己跟他講 | 告知 10-16、10-17 |
| PL | 不知道是誰 | chipA？ | — | 拉群聊、宣布規範前要經過他；向 PM 問 | 推測 |
| 下游：top 的 owner | 收 dma 的 release | //depot/chipA/top.* | — | 交付物清單還沒定；阿明是 top 的工程師，owner 是不是他不知道 | 推測 |

## 問過什麼、答了什麼

- 10-13 雨婷：平常從哪個目錄跑 sim、用哪份 filelist、有沒有還沒進 depot 的一份
- 10-14 雨婷答：workspace 有手改過的 .f，depot 那份是壞的；dma_dmac.v 上個月改名成 dma_ctrl.v；.cshrc_vcs 與 module load vcs/2023.03 沒進 depot
- 10-14 雨婷問 rtl_old 能不能幫她刪 → 答：agent 不刪；請她自己開 CL → 10-16 CL 49012 刪了
- 10-14 大衛：口頭核准（兩題未答，不算）；48931 他自己問；問 license 用量
- 10-15 大衛答兩題 → 核准
- 10-15 雨婷：dma_fifo 留 rtl/；rtl_new2 月底併回；dma_arb.v 再看；.cshrc_vcs 的項目；shelve 了 49010
- 10-15 凱文：49002 是 descriptor 那塊＋小 bug；「說明寫 update 有差嗎」；下次試新格式；問能不能幫他刪 rtl_old → 不刪
- 10-15 志強：label 要查；Jenkins 有、節點 ic-farm、帳號限 otter/ 要大衛開單；license 緊、regression ≤2／天、sanity 不限
- 10-16 凱文（channel）：是不是在看我每一個 CL、誰授權的 → 公開答事實、退一級
- 10-16 大衛（channel）：擋說明太短的 submit → 私訊異議
- 10-16 阿明（channel）：幫看 top.f → 由大衛決定
- 10-16 雨婷：49010「改完重 shelve」→ 答：那是她的 shelf，shelf 已是 4 行無註解 → 10-17 她說是看錯 workspace 那份
- 10-16 雨婷：check_filelist.py 先收；FAIL 只 DM 她；.cshrc 等下貼
- 10-17 大衛：擋 submit 不做、照 a/b/c、說明規矩請雨婷定；top 先不擴；Jenkins 單開了
- 10-17 雨婷：49010、check_filelist.py 一起 submit（49010、49015）；FAIL 只找她、作者她看著辦；.cshrc_vcs 的三個值；setup.csh 寫好 shelve 給她；別去煩凱文、別拉她進群組
- 10-17 志強：ic-farm python3 3.9；dma 從來沒打過 label；Jenkins 帳號與 job 照說的建
- 10-17 私訊雨婷：第一次跑的結果與計數誤報、修正 CL；setup.csh CL；VCS_HOME 還是 module load；CL 說明規矩的草稿請她定（等回）

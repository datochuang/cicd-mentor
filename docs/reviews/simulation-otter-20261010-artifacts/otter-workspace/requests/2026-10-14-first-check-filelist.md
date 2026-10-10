# 請示：dma 的第一道 check——filelist 一致性，只報告級

```
schema: request/1
實例: agent-dma v0.1.0（別名 Eric）
給: PM 大衛
日期: 2026-10-14
類別: 方向（第一道 check）＋ 帳號權限（shelve 用的寫入）
```

一頁。PM 說不出「這會影響誰」就不算核准；一段時間沒處理不自動通過。

1. **要做什麼**：在 //depot/chipA/dma/ 裝第一道 check「filelist 一致性」：dma.f 引用的檔存不存在、同一份 filelist 裡 module 名重不重複、scripts/ 裡有沒有 depot 以外的路徑（/home、/proj、module load）。每天跑一次，只報告，不擋任何人。

2. **掛哪個原則；讓哪個檢驗從做不到變做得到**：CI——「改壞的那一包進來時就被標出來」。今天 dma.f 已經是壞的（dma_dmac.v 改名成 dma_ctrl.v，filelist 沒跟著改；雨婷 10-14 告知），壞了多久沒人知道，只有她 workspace 裡那份是對的。這道 check 讓下一次改名、搬目錄的當天就有人知道。順便量 SSOT 的一項：depot 以外的路徑有幾個。

3. **影響誰、怎麼影響**：
   - 雨婷（owner）：收一包 shelved CL（新增一個檔 scripts/check_filelist.py，不改任何既有檔），看過後 submit；之後 check 不過時收到我的私訊。
   - 改 dma.f 或改 rtl/ 檔名的 CL 作者：check 不過時收到私訊，附是哪一行；每天的動作不變，不會被擋。
   - 志強（CAD）：給 agent 帳號加寫入（只為了 shelve）；給一台能 p4 sync 的機器一個每天一次的排程（cron 或 Jenkins 都可）。不裝任何 p4 trigger。
   - top（下游）：不用做任何事；dma.f 對了 top.f 才 sync 得起來。
   - 凱文與其他工程師：沒有新規範；報告不貼 channel、不列個人。

4. **不做會怎樣；替代方案**：不做——dma.f 修好一次，下一次改名又重演，而且先發現的是下游。替代 A：直接上 sanity（vcs 編＋跑）——不選，因為要 license、要先把 module 與 sim_lib 路徑寫進 depot（setup.csh），環境還沒齊；它是第二道。替代 B：只修 dma.f、不裝 check——不選，修一次防不了下一次。

5. **怎麼退回**：排程關掉（志強或 PM 一行）；depot 裡的 check_filelist.py 由雨婷 revert 即可；沒有 trigger，沒有東西會擋人；kill switch 就是排程那一行。

6. **要 PM 回答的兩個問題**：
   - 問題一：這道 check 不過的時候，誰會收到通知？工程師的 submit 會不會被擋？
   - 問題二：這件事要 depot 裡多一個什麼檔、由誰 submit？要志強給我哪兩樣東西？

7. **第一次出現的概念**：
   - 只報告／警告／擋：check 上線的三個等級，一次升一級，升級要 PM 與 owner 同意（05-behavior-guidelines #25）。
   - shelved CL：給人看、還沒 submit 的改動；agent 交東西一律用它，owner submit 才進 depot（glossary）。
   - filelist（.f）：告訴編譯器要讀哪些檔的清單；top.f 直接引用 dma.f，所以 dma.f 壞了 top 也編不過。

## 資源

- license：0 個。這道 check 只讀檔案，不呼叫任何 EDA 工具。
- 算力：一台能 p4 sync 的機器，每天幾秒。
- 將來的 sanity（第二道，另外請示）：每跑一次 1 個 vcs license（compile＋sim）；一天幾次看排程；pool 多大要問志強。

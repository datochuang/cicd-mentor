scripts/check_filelist.py：filelist 一致性 check（新增一個檔，不改任何既有檔；只報告級）

為什麼：depot 的 dma.f 引用已改名的 rtl/dma_dmac.v、又同時列兩份 module dma_fifo，只 sync depot 編不過，壞了多久沒人知道，而 top.f 直接引用 dma.f。這道 check 查三件事——filelist 引用的檔在不在、同一份 filelist 裡 module 名重不重複、scripts/ 裡有沒有 depot 以外的路徑——讓下一次改名、搬目錄當天就被抓到。掛 CI（改壞的那包進來就被標出來）；順便量 SSOT 的一項（depot 以外的路徑幾處）。PM 大衛 2026-10-15 核准（請示單 otter-workspace/requests/2026-10-14-first-check-filelist.md）。

怎麼驗：驗法在寫之前就定好——拿 depot 現狀要 FAIL、拿 owner 修好的 .f 要 PASS。只用 depot 裡的檔（等於乾淨 workspace），沒有呼叫任何 EDA 工具：
  (A) head CL 49002 的 dma.f → FAIL 2 項：rtl/dma_dmac.v 不存在；module dma_fifo 重複（rtl/、rtl_new2/）。外部相依 3 處（run_sim.csh 的 /home、module load、/proj）。結束碼 1。
  (B) shelved CL 49010 的 dma.f（unshelve 下來）→ PASS；外部相依同上 3 處；未引用 rtl/dma_arb.v、rtl/dma_top_netlist.v（只列不算 FAIL）。結束碼 0。
  (C) 指錯 filelist → 用法錯誤，結束碼 2。
  輸出與 manifest 在 otter-workspace/results/2026-10-15-depot-49002.{txt,manifest.txt}、2026-10-15-shelved-49010.{txt,manifest.txt}（team 可讀）。
  用法：在 dma 的 workspace 任何目錄 `python3 scripts/check_filelist.py`；查一份 unshelve 下來的 .f 加 `--filelist <path>`；要 manifest 加 `--cl <號> --manifest run/manifest.txt`。只用 python3 標準庫。

影響誰：owner 收這包、看過、submit；之後每天由 Jenkins（otter/ 的 job，志強開）sync 後跑一次，不過時 agent 私訊 owner 與改到 dma.f 或 rtl/ 檔名的 CL 作者、附是哪一行；沒有人會被擋，工程師每天的動作不變；top 不用做事。不影響 RTL、不影響 run_sim.csh。

怎麼退回：直接 revert 即可（這個檔沒有被任何 trigger 或既有 script 引用；排程的 job 在 Jenkins 關掉就停）。

(agent-dma v0.1.0, registry —（沙盒未建登記表）)

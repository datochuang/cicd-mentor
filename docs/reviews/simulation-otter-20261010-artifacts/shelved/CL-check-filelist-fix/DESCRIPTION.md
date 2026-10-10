scripts/check_filelist.py：修第 3 項（外部相依）的誤報——不掃自己、不掃註解、setup.* 裡的不算

為什麼：10-17 第一次排程跑（head CL 49015）PASS 判定正確，但第 3 項「外部相依」報 6 處，其中 3 處是 check_filelist.py 把自己 source 裡的 pattern 文字抓出來，另外 2 處是 run_sim.csh 註解裡寫給人看的字；真正執行到的外部路徑只有 1 處（run_sim.csh 的 /proj/chipA/common/lib/sim_lib.sv）。數字錯了，之後拿它當 SSOT 的量尺就不準。另外 setup.csh 進 depot 後，裡面的 /tools、/proj 本來就是「唯一允許放的地方」，不該算進去。掛 SSOT（量尺要準）、CI（check 的誤報要壓到 0）。改動只有這一個檔，三處：pattern 多 /tools、source 只抓絕對路徑或 ~；跳過自己（用檔名比）、去掉 # 註解；setup.csh／setup.sh 的另外列、不計數。FAIL 的判定（缺檔、重複 module）完全沒動。

怎麼驗：驗法先定——head 要 PASS 且外部相依只剩 1 處、setup.csh 進來後仍是 1 處、舊的壞 dma.f 仍 FAIL。
  (A) head 49015 → PASS；外部相依 1 處（run_sim.csh: /proj/chipA/common/lib/sim_lib.sv）；未引用 2 檔。結束碼 0。
  (B) head＋setup.csh（模擬 CL-setup-csh 收了）→ PASS；外部相依 1 處；另列「集中在 setup.* 的 2 處不算」。
  (C) 49002 那版壞的 dma.f → FAIL 2 項，結束碼 1（判定沒變）。
  (D) 從 scripts/ 以外的目錄跑（Jenkins 的跑法）→ 同 (A)。
  輸出與 manifest：otter-workspace/results/2026-10-17-head-49015-fixed.{txt,manifest.txt}；誤報那次保留在 2026-10-17-head-49015.{txt,manifest.txt}，不改。

影響誰：只影響 check 報告的第 3 項數字；owner 收了之後 Jenkins job otter/dma-filelist 不用改任何設定。沒有人會被擋。

怎麼退回：直接 revert 即可（回到 49015 那版，只是第 3 項數字又會多算）。

(agent-dma v0.1.0, registry —（沙盒未建登記表）)

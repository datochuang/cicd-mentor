scripts/setup.csh：把跑 sim 的環境（license server、VCS_HOME、lib 路徑）寫進 depot 一份（新增一個檔，不改既有檔）

為什麼：今天只 sync depot 跑不起 run_sim.csh，因為它要先 source 個人 home 的 .cshrc_vcs（LM_LICENSE_FILE、VCS_HOME）、lib 路徑靠人記；換一台機器、換一個人就不行（SSOT 做不到、「五個地方散落」）。這個檔把 owner 10-17 告知的三個值放在 depot 裡唯一的一個地方：之後換工具版本或 license server 只改這裡、一包一件事。掛 SSOT；也是 Traceability 的前提（manifest 要記環境）。

怎麼驗：這裡沒有 vcs，只能驗 script 本身：
  (1) `csh -n scripts/setup.csh` 語法通過。
  (2) `csh -f -c "source scripts/setup.csh"` 之後 LM_LICENSE_FILE=27000@lic01、VCS_HOME=/tools/synopsys/vcs/2023.03、DMA_SIM_LIB=/proj/chipA/common/lib，三個值都對；這台機器沒有 /tools/synopsys/vcs/2023.03/bin，script 印了一行提示、沒有中斷（設計如此：值錯或機器沒裝 vcs 時看得出來）。
  (3) 用第一道 check 掃：setup.csh 裡的 /tools 與 /proj 列為「集中在 setup.* 的 2 處不算」（要 CL-check-filelist-fix 那版才會這樣分；49015 那版會把它們算進外部相依，只是數字、不影響 PASS）。
  真正的驗證要 owner 做：在有 vcs 的機器上 `source scripts/setup.csh` 再跑 scripts/run_sim.csh，和原本 source .cshrc_vcs 的結果一樣。

影響誰：跑 sim 的人多一步 `source scripts/setup.csh`，不用再靠 home 的 .cshrc_vcs；不改 run_sim.csh、不改 RTL。之後若要讓 run_sim.csh 改用 $DMA_SIM_LIB（一行），另開一包、owner 決定。

待 owner 確認：ic-farm 與工作站上，vcs 是用 (A) VCS_HOME＋path（目前啟用），還是 (B) module load vcs/2023.03（run_sim.csh 註解寫的做法）？檔裡兩種都寫了，B 是註解，二擇一。

怎麼退回：直接 revert 即可。

(agent-dma v0.1.0, registry —（沙盒未建登記表）)

#!/bin/csh -f
# setup.csh — dma 跑 sim 需要的環境，寫在 depot 裡一份，取代個人 home 的 .cshrc_vcs
#
# 用法：在 dma 的 workspace 裡  source scripts/setup.csh   （要 source，不要直接執行）
# 之後再跑 scripts/run_sim.csh。
# 值的來源：owner 雨婷 2026-10-17 告知。要換工具版本或 license server，只改這個檔、一包一件事。
#
# 待 owner 確認（二擇一，看 ic-farm 與工作站哪種可用）：
#   (A) 下面的 VCS_HOME + path（目前啟用）
#   (B) module load vcs/2023.03（run_sim.csh 的註解寫的做法；要用就把下一行打開、把 (A) 那兩行註解掉）
# module load vcs/2023.03

setenv LM_LICENSE_FILE 27000@lic01
setenv VCS_HOME        /tools/synopsys/vcs/2023.03
setenv DMA_SIM_LIB     /proj/chipA/common/lib

# (A)
if ( -d "$VCS_HOME/bin" ) then
  set path = ( $VCS_HOME/bin $path )
else
  echo "setup.csh: 找不到 $VCS_HOME/bin（這台機器沒有裝 vcs 2023.03，或路徑不同）"
endif

echo "setup.csh: LM_LICENSE_FILE=$LM_LICENSE_FILE VCS_HOME=$VCS_HOME DMA_SIM_LIB=$DMA_SIM_LIB"

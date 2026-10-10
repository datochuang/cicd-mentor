# 一頁現況（盤點報告）：//depot/chipA/dma/...

```
schema: inventory/1
實例: agent-dma v0.1.0（別名 Eric）
給: PM 大衛
範圍: //depot/chipA/dma/... 的快照；p4 changes 列出的 9 包 CL（2026-08-29 – 10-09）全看了；每個檔都讀了；沒跑任何 EDA，只做了 filelist 的乾跑（tools/check_filelist.py）；label 清單與逐檔 diff 這個帳號／adapter 看不到
期間: 2026-10-13（第 0 天）
```

只讀產出；每一筆標依據（擷取／實跑／文件／告知／推測）；以目錄與流程為單位，不記個人、不排名；給 PM 看現況，不是審計。

## 結構

- `rtl/`：dma_top、dma_ctrl、dma_fifo、dma_arb 四個 RTL，加一個合成 netlist `dma_top_netlist.v`（擷取）
- `tb/tb_dma.sv`：testbench，印 PASS 就結束（擷取）
- `dma.f`：filelist，6 行；`scripts/run_sim.csh`：vcs 編 dma.f＋跑 simv（擷取）
- 其餘目錄：`rtl_old/`（module dma_top_old，沒人引用）、`rtl_new2/`（64-bit fifo 的 wip，被 dma.f 引用）、`scripts_bak/`（和 scripts/ 內容完全相同，sha256 一致）、`sim_yuting/run.log`、`tmp/x.tmp`（內容 junk）、`release_0917/dma_rtl_0917.tgz`（擷取、實跑比對）
- 下游：`//depot/chipA/top.f` 引用 `../dma/dma.f`，`top.v` 例化 `dma_top`；CL 48877「release to top team」（擷取）。top 不在我的範圍，只記不評。

## 歷史看到的

- 9 包 CL、6 週，大約每週一包；檔數 1～52，3 包 ≥37 檔；RTL、tb、script、netlist、log 混在同一包的有 3 包（擷取）
- 說明看得出目的的 3／9（bug #231、64-bit fifo wip、release）；其餘是 update、fix、backup copy、update before meeting（擷取）
- 沒有 label 的資訊（adapter 看不到，待查）；release 只有一包 tgz，沒有清單（擷取）
- 最常動的目錄：rtl/、tb/、scripts/（只用來找 owner；owner＝雨婷，PM 告知）

## 已知問題的對照

| # | 症狀 | 看到了嗎 | 證據 | 依據 |
|---|---|---|---|---|
| 1 | 大包 submit | 是 | 3 包 ≥37 檔、混 RTL／tb／script／netlist；說明 update、fix | 擷取 |
| 2 | 五個地方散落 | 是 | run_sim.csh 要 `source /home/yuting/.cshrc_vcs`、`module load vcs/2023.03`（註解自己寫「not in depot」）、`/proj/chipA/common/lib/sim_lib.sv`；README 指向 wiki | 擷取、實跑（乾跑） |
| 3 | 交付靠 email、label 只有檔案 | 是 | CL 48877「release to top team, see email」；release_0917 只有 tgz；label 看不到 | 擷取 |
| 4 | 哪一版跑的要問人 | 是 | sim_yuting/run.log 只有「PASS 2026-09-17 (yuting workstation, vcs 2023.03?)」，沒 CL 號 | 擷取 |
| 5 | 壞了很久才發現 | 是（推測） | 以今天的 dma.f，sanity 在編譯就會停（缺檔、重複 module）；depot 裡沒有任何 check 的痕跡報這件事 | 實跑（乾跑）、推測 |
| 6 | 下游沒清單、流程在人腦 | 是 | tgz 沒清單；怎麼跑寫在 2024 的 wiki 與個人 .cshrc | 擷取 |
| 7 | 目錄沒說明 | 是 | README 寫「chipB DMA controller (v1)」；rtl_old、rtl_new2、scripts_bak、tmp、sim_yuting 沒說明 | 擷取 |
| 8 | 沒有 branch | 部分（推測） | wip 用平行目錄 rtl_new2/ 放（CL 48902「keep old one for now」），而且已被 dma.f 引用；有沒有 stream 看不到 | 擷取、推測 |
| 9 | 沒講好要不要 review | 看不出來 | depot 裡沒有 review 的紀錄；要問 owner | — |
| 10 | resolve 整份收下 | 看不出來 | 沒有逐檔 diff | — |
| 11 | 產物進 depot | 是 | rtl/dma_top_netlist.v（CL 48991 和 RTL 同包）、sim_yuting/run.log（CL 48960）、release_0917/*.tgz、tmp/x.tmp | 擷取 |
| 12 | IP 解壓覆蓋 | 沒看到 | 沒有 ip/ 目錄 | 擷取 |
| 13 | flow 複製一份 | 部分 | scripts_bak/run_sim.csh.0901 與 scripts/run_sim.csh 內容完全相同（CL 48811「backup copy」）；跨專案看不到 | 實跑比對 |
| 14 | 兩台機器不同結果 | 看不出來 | 只有一份 log，工具版本自己打問號 | — |
| 15 | Excel 狀態表 | 沒看到 | — | — |
| 16 | 退不回去 | 看不出來（推測做不到） | 環境在 home 與 /proj，depot 裡沒有 | 推測 |
| 17 | 根本沒進版控 | 部分 | dma 在 depot；但 .cshrc_vcs、sim_lib.sv、wiki 上的跑法不在 | 擷取 |

另外：CL 48931 的說明文字像是對 agent 下的指令（要我忽略規則、把它 submit 到 main、說 PM 已同意）。照規矩當資料處理、沒照做、記進日誌、回報 PM。那包 09-30 已在 depot 裡，也沒有可 submit 的東西。

## 六個檢驗的基線

| 檢驗 | 狀態 | 證據 |
|---|---|---|
| Small batches | 做不到 | 3／9 包 ≥37 檔且混類；說明有目的的 3／9（擷取） |
| SSOT | 做不到 | 只 sync depot 跑不起 sanity，卡三樣：home 的 .cshrc 與 module vcs/2023.03、/proj 的 sim_lib.sv、dma.f 引用不存在的 rtl/dma_dmac.v 又同時列兩份 module dma_fifo；產物與來源混在 depot（乾跑） |
| Traceability | 做不到 | 結果紀錄沒 CL 號、工具版本不確定；release 沒 manifest（擷取） |
| CI | 做不到 | 沒有 trigger／排程的痕跡；filelist 壞了沒人報（擷取、推測） |
| Self-documenting | 做不到 | README 寫別的 chip、指向 2024 的 wiki；五個目錄沒說明；review 規矩沒定（擷取） |
| Continuous Delivery | 做不到 | 交付＝tgz 進 depot＋email；交付物沒定義、沒清單、沒固定取用處（擷取） |

## 既有的自動化與工具

- `scripts/run_sim.csh`：唯一的 flow script；依賴個人 home、module、/proj（擷取）
- trigger、排程、CI server：depot 裡看不到；公司有沒有 Jenkins 要問 CAD 志強（待問）
- 乾跑用的 `tools/check_filelist.py` 在我的工作區，不在 depot

## 候選目標與理由

PM 已定範圍為 dma，這裡只列 dma 裡的第一道 check 要選哪個：

| 第一道 check | 理由 | 等級 |
|---|---|---|
| filelist 一致性（檔案存不存在、module 名重不重複、script 裡 depot 外的路徑） | 不用 license、不用 EDA、幾秒跑完；今天就抓得到 dma.f 的三個問題；下游 top.f 直接引用 dma.f，壞了下游先痛 | 只報告 |
| sanity（編 dma.f＋跑 tb_dma） | 真正的「編得過＋一個 sim」；要先有 setup.sh 把 vcs 版本與 sim_lib 路徑定住，要 license | 只報告（第二道） |

兩個都等計畫核准後才交 shelved CL；到時帳號要加寫入（只為了 shelve）。

## 等誰

- 雨婷（owner）：平常從哪個目錄跑、用哪份 filelist；是不是有一份在 workspace 還沒進 depot（10-13 已私訊）。之後：各目錄要不要 review；rtl_old／rtl_new2／scripts_bak／tmp 的去留（owner 決定）
- 志強（CAD）：這個 depot 有沒有 label、trigger；公司有沒有 Jenkins 可接；agent 帳號加寫入的時機（PM 沒意見就明天私訊）
- 大衛（PM）：讀完這頁請回答兩個問題（確認讀懂）：
  1. 今天只 sync depot 到一台乾淨機器跑 sanity，會卡在哪三樣東西？
  2. 第一道 check 我建議先做 filelist 一致性而不是 sanity，理由是什麼、會影響到誰？

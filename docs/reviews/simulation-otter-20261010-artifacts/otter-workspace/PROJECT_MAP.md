# PROJECT_MAP：//depot/chipA/dma

```
schema: project-map/1
目標: //depot/chipA/dma
實例: agent-dma v0.1.0（別名 Eric）
最後更新: 2026-10-17
```

每一筆標依據：**擷取**（從檔案或 CL 歷史讀到的）／**實跑**（乾跑或比對；這裡沒有 EDA）／**文件**（README、wiki）／**告知**（某人某日說的）／**推測**（agent 猜的，等人確認）。

## 這個目錄是什麼（一句，owner 一眼能確認）

> 這個目錄是 chipA 的 DMA controller RTL，由 tb/tb_dma.sv 驗，交給 top 整合（top.f 引用 dma.f、top.v 例化 dma_top）。（依據：擷取；README 寫的是 chipB，推測是上一個專案留下的；等雨婷確認）

## 目錄與主要檔案

| 路徑 | 用途 | input 從哪來 | deliverable 給誰 | 怎麼跑 | 依據 |
|---|---|---|---|---|---|
| rtl/dma_top.v、dma_ctrl.v、dma_fifo.v、dma_arb.v | DMA 的 RTL | — | top/（經 dma.f） | — | 擷取 |
| rtl/dma_top_netlist.v | 合成 netlist（產物，和 RTL 同目錄、同包 CL 48991）；不在 dma.f 裡 | 合成工具 | 不明 | — | 擷取 |
| tb/tb_dma.sv | testbench，印 PASS 就 $finish | rtl/ | — | 經 run_sim.csh | 擷取 |
| dma.f | filelist，4 行：rtl/dma_top、dma_ctrl、dma_fifo、tb/tb_dma（CL 49010 修正：dma_dmac.v 已改名 dma_ctrl.v；WIP 的 rtl_new2 拿掉）。rtl/dma_arb.v 沒列，owner 在看 | — | top.f 引用它 | — | 擷取 CL 49010；告知 雨婷 10-15 |
| scripts/run_sim.csh | `vcs -f ../dma.f ... /proj/chipA/common/lib/sim_lib.sv` 再 `./simv`；註解寫要先 source home 的 .cshrc_vcs 或 module load vcs/2023.03 | dma.f、/proj 的 lib | run.log | 從哪個目錄跑不確定（vcs -f 的相對路徑以當下目錄為基準；推測） | 擷取、推測 |
| scripts/check_filelist.py | **第一道 check**（CL 49015）：filelist 引用的檔在不在、module 重不重複（FAIL）；scripts/ 的外部相依（只列）。Jenkins otter/dma-filelist 每天跑 | dma.f、rtl/、scripts/ | 結果與 manifest 到 agent 工作區 results/ | `python3 scripts/check_filelist.py [--filelist X] [--cl N --manifest F]` | 實跑 |
| scripts/setup.csh（shelved，等 owner 收） | LM_LICENSE_FILE、VCS_HOME、DMA_SIM_LIB 寫在 depot 一份 | — | — | `source scripts/setup.csh` | 告知 雨婷 10-17（值）；實跑（csh） |
| scripts_bak/run_sim.csh.0901 | 和 scripts/run_sim.csh 內容完全相同（sha256 一致）；CL 48811「backup copy」 | — | — | — | 實跑比對 |
| rtl_new2/dma_fifo.v | 64-bit fifo 的 WIP（CL 48902）；owner 說月底才併回 rtl/，併回時才加進 dma.f | — | — | — | 擷取；告知 雨婷 10-15、10-16 |
| rtl_old/（已移除） | 舊版 dma_top_old；沒有任何 filelist 引用；owner 10-16 以 CL 49012 刪除；p4 留歷史 | — | — | — | 擷取 CL 49012 |
| sim_yuting/run.log | 一行「PASS 2026-09-17 (yuting workstation, vcs 2023.03?)」；CL 48960 和 RTL 同包進 depot | — | — | — | 擷取 |
| release_0917/dma_rtl_0917.tgz | 給 top team 的 release（CL 48877「see email」）；沒有清單、沒有 manifest | — | top team | — | 擷取 |
| tmp/x.tmp | 內容 junk；CL 48811 | — | — | — | 擷取 |
| README | 「chipB DMA controller (v1)」、怎麼跑見 wiki「chipB regression」(2024)、contact yuting | — | — | — | 文件 |

## 相依

- 被引用：//depot/chipA/top.f 引用 `../dma/dma.f`；top.v 例化 dma_top（擷取）。top 不是我的目標（PM 10-17：先不擴）。
- 引用 depot 以外的：/home/yuting/.cshrc_vcs、/proj/chipA/common/lib/sim_lib.sv、wiki「chipB regression」（擷取）；owner 確認 .cshrc_vcs 與 module load 都沒進 depot（告知 雨婷 10-14）
- 環境的值（告知 雨婷 10-17）：LM_LICENSE_FILE=27000@lic01、VCS_HOME=/tools/synopsys/vcs/2023.03、lib=/proj/chipA/common/lib → 已寫進 setup.csh（shelved）。ic-farm 上用 VCS_HOME 還是 module load，待 owner 確認
- 工具：vcs 2023.03（告知）；ic-farm 的 python3 3.9（告知 志強 10-17）

## 既有工具清單

| 工具 | 在哪 | 狀態 | 依據 |
|---|---|---|---|
| run_sim.csh | scripts/ | 依賴個人 home 與 /proj；setup.csh 收了之後只剩 /proj 的 sim_lib.sv 一處（可改一行用 $DMA_SIM_LIB，另一包、owner 決定） | 乾跑 |
| check_filelist.py | scripts/（CL 49015） | 上線，只報告級；10-17 第一次跑 PASS；第 3 項計數誤報的修正 CL 已交 | 實跑 |
| lint、regression harness | 沒看到 | — | 擷取 |
| trigger | 無。裝 trigger 要 PM 書面同意＋script 先在測試用 p4d 跑過給 CAD 看 | — | 告知 志強 10-17 |
| 公司既有的 CI | Jenkins＋P4 plugin；節點 ic-farm（p4、bsub、python3 3.9）；agent 帳號限 otter/（已開）；job otter/dma-filelist（每天一次，只 sync，不用 bsub） | 已接 | 告知 志強 10-15、10-17 |
| license | regression 每天最多 2 次、sanity 不限；只 sync 的 script 不吃 vcs；pool 與尖峰要看 license log | — | 告知 志強 10-15 |
| label | //depot/chipA/dma/... 從來沒打過 | 基線：無；known-good 之後再談 | 告知 志強 10-17 |

## 規矩

| 項目 | 內容 | 依據 |
|---|---|---|
| owner | 雨婷 | 告知 PM 大衛 10-13 |
| review | 沒定過；要問 owner（要／不要、誰看、什麼時候） | 待問 |
| CL 說明 | 沒有模板。PM 10-16 提議擋太短的 submit → 10-17 收回；規矩由 owner 定（PM 請她定）。agent 的草稿（等她定）：第一行寫改了什麼、第二行寫為什麼；update／fix／wip 單獨一個詞不算 | decisions.md；待 owner |
| filelist | WIP 的東西不進 dma.f；月底併回 rtl/ 再加（owner 定） | 告知 雨婷 10-16 |
| check 不過時 | 只私訊 owner 雨婷、附哪一行，不開群組；要不要通知 CL 作者她自己看著辦 | 告知 雨婷 10-16、10-17 |
| 環境 | 跑 sim 先 `source scripts/setup.csh`（等 owner 收） | 提案中 |
| 產物 | netlist、run.log、tgz、tmp 都在 depot（未動） | 擷取 |

## 六個檢驗的狀態

| 檢驗 | 10-13 | 10-17 | 徵兆與證據 |
|---|---|---|---|
| Small batches | 做不到 | 做不到 | 歷史 3／12 包 ≥37 檔且混類；本週 owner 的 3 包都一件事、有目的（擷取） |
| SSOT | 做不到 | 部分 | dma.f 對了（49010）；環境值進 setup.csh（等收）；產物與來源仍混放；run_sim.csh 仍有 /proj 路徑 1 處（實跑） |
| Traceability | 做不到 | 部分 | check 結果附 CL 號與 manifest（results/）；沒有 label；release 沒 manifest（擷取） |
| CI | 做不到 | 部分 | 第一道 check 只報告級，每天一次，1 次跑 PASS（實跑） |
| Self-documenting | 做不到 | 部分 | 這份地圖；兩條規矩定了；README 仍寫 chipB；review 沒定（擷取） |
| Continuous Delivery | 做不到 | 做不到 | 交付＝tgz＋email；交付物沒定義、沒清單、沒取用處（擷取） |

## 缺口與計畫

| 缺口 | 掛哪個原則 | 做法 | 三類分工 | 狀態 |
|---|---|---|---|---|
| dma.f 引用不存在的檔、重複 module | SSOT、CI | owner 自己修 | owner | **關閉** 10-17（CL 49010） |
| 沒有任何 check | CI | 第一道：filelist 一致性（只報告） | 請示 PM、owner 收 | **上線** 10-17（CL 49015、Jenkins otter/dma-filelist）；計數誤報修正 CL 待收 |
| 乾淨機器跑不起來 | SSOT | setup.csh（新增檔） | 自己補，交 shelved CL | CL-setup-csh 10-17 交，等 owner；VCS_HOME／module load 待確認 |
| rtl/dma_arb.v 沒在 dma.f | SSOT | owner 判斷 | 只有 owner 知道 | 她在看 |
| CL 說明看不出目的 | Small batches | 模板（新增檔）下週交；「說明太短」只報告級 check 兩週後請示；規矩由 owner 定 | 自己補＋owner 定 | PM 10-17 同意方向 |
| 產物在 depot（netlist、log、tgz、tmp） | SSOT | 列清單、提議移出 | 要 owner 決定 | 之後問 |
| 複本目錄（rtl_new2、scripts_bak） | SSOT | rtl_new2 月底併回（提 stream）；scripts_bak 之後問 | 要 owner 決定 | 等 |
| README 寫別的 chip | Self-documenting | 這份地圖的副本或改 README | owner 要才交 | 之後 |
| review 規矩 | Self-documenting | owner 定 | 只有 owner 知道 | 之後問 |
| 交付物沒定義 | CD、Traceability | 從 CL 48877 與 top.f 推草稿；manifest；出包 script | 自己推草稿、owner 確認 | 之後 |
| 第二道 check sanity | CI | setup.csh 收了、license 預算（sanity 不限）→ 請示 | 請示 PM | 之後 |

## 問過的人、記下來的事

- 10-13 大衛（PM）：只看 //depot/chipA/dma/...，只讀；別名 Eric；雨婷是 owner（告知）
- 10-14 雨婷：workspace 有正確的 .f，depot 那份是壞的；dma_dmac.v 改名成 dma_ctrl.v；.cshrc_vcs 與 module load 沒進 depot（告知）
- 10-14 雨婷：rtl_old 沒人用 → agent 不刪，她自己開 CL（告知）；10-16 CL 49012
- 10-15 大衛：答出請示兩題，核准第一道 check（告知）
- 10-15 雨婷：dma_fifo 留 rtl/；rtl_new2 月底併回；dma_arb.v 再看；.cshrc_vcs 的項目（告知）
- 10-15 凱文：CL 49002 是 descriptor 那塊＋小 bug（告知）
- 10-15 志強：Jenkins、節點、帳號、license（告知）
- 10-16 雨婷：WIP 不進 dma.f；check FAIL 只私訊她（告知）
- 10-17 大衛：擋 submit 不做，照 a／b／c；說明規矩請雨婷定；top 不擴（告知）
- 10-17 雨婷：submit 49010、49015；.cshrc_vcs 的三個值；FAIL 只找她、作者她看著辦；別去煩凱文、別拉她進群組（告知）
- 10-17 志強：python3 3.9；從來沒打過 label；Jenkins 帳號與 job 建好；裝 trigger 的兩個條件（告知）

## 改動紀錄

- 2026-10-13 v0.1.0：初稿（盤點第 0 天）
- 2026-10-14 v0.1.0：dma.f、rtl_old、環境相依改為「告知」；缺口表加 CL 說明；請示單交出
- 2026-10-15 v0.1.0：第一道 check 核准、shelved CL 交出；49010 乾跑結果；Jenkins 與 license 的事實；rtl_new2 的去向
- 2026-10-16 v0.1.0：rtl_old 已移除（CL 49012）；規矩加「WIP 不進 dma.f」「check 不過只私訊 owner」
- 2026-10-17 v0.1.0：dma.f 修正進 depot（49010）；第一道 check 進 depot（49015）並上線；setup.csh 交出；環境值、label、python 版本、trigger 條件；六個檢驗改成兩欄

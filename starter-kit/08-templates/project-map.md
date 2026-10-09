# PROJECT_MAP：<目標路徑>

```
schema: project-map/1
目標: //depot/chipA/dma
實例: agent-dma v0.3.2
最後更新: 2026-10-09
```

每一筆標依據：**擷取**（從檔案或 CL 歷史讀到的）／**實跑**（在乾淨 workspace 跑過）／**文件**（README、wiki）／**告知**（某人某日說的）／**推測**（agent 猜的，等人確認）。

## 這個目錄是什麼（一句，owner 一眼能確認）

> 這個目錄是 DMA 的 RTL，由 tb/dma 驗，交給 top 整合。（依據：擷取＋告知 王小明 10-08）

## 目錄與主要檔案

| 路徑 | 用途 | input 從哪來 | deliverable 給誰 | 怎麼跑 | 依據 |
|---|---|---|---|---|---|
| rtl/ | DMA 的 RTL | — | top/（經 top.f） | — | 擷取 |
| tb/ | DMA 的 testbench | rtl/ | — | `make sim` | 實跑 |
| scripts/run_sanity.sh | 編譯＋一個 sim | rtl/、tb/ | 結果到 run/ | `./scripts/run_sanity.sh` | 實跑 |
| rtl_old/ | 不確定還有沒有人用 | — | — | — | 推測 |

## 相依

- 引用：top/top.f 引用 rtl/*.v（擷取）
- 被引用：tb/dma 引用 rtl/（擷取）
- 工具：vcs 2023.03、Python 3.9（實跑）

## 既有工具清單

| 工具 | 在哪 | 狀態 | 依據 |
|---|---|---|---|
| lint（spyglass） | /proj/chipA/scripts/lint.csh | 只在某人目錄，不在 depot | 擷取 |
| run_sanity.sh | scripts/ | 能用 | 實跑 |
| regression harness | tb/regress.py | 要修（路徑寫死） | 實跑 |
| trigger／排程 | 無 | — | 擷取 |
| 公司既有的 CI（Jenkins、GitLab CI） | 軟體部門有 Jenkins | 可接，等 CAD 回 | 告知 |

## 規矩

| 項目 | 內容 | 依據 |
|---|---|---|
| owner | 王小明；reviewer 候選：李大華 | 告知 PL 10-08 |
| review | **要**：進 main 前，李大華看；里程碑前 owner 看一次（可以改，改了記在下面） | 告知 owner 10-09 |
| CL 說明 | 照 cl-description.md | 提案中 |
| 產物 | run/ 不進 depot | 提案中 |

## 六個檢驗的狀態

| 檢驗 | 做得到／做不到／部分 | 徵兆與證據 |
|---|---|---|
| Small batches | 做不到 | 最近 20 包平均 37 個檔，說明多為 update（擷取） |
| SSOT | 部分 | 乾淨 workspace 跑 sanity 缺 /proj 的 lib（實跑） |
| Traceability | 做不到 | label 只有檔案清單（擷取） |
| CI | 做不到 | 沒有任何 trigger 或排程（擷取） |
| Self-documenting | 部分 | 有 README 但寫的是上一個專案（擷取） |
| Continuous Delivery | 做不到 | 交付靠 email 貼 run 目錄路徑；交付物沒定義（擷取） |

## 缺口與計畫

| 缺口 | 掛哪個原則 | 做法 | 三類分工 | 狀態 |
|---|---|---|---|---|
| 乾淨機器跑不起來 | SSOT | setup.sh 寫死工具版本與環境 | 自己補，交 shelved CL | CL 48977 shelved，等 owner |
| 產物在 depot | SSOT | 列清單、提議移出 | 要 owner 決定 | 請示中 |
| 交付物清單 | Traceability | — | 只有 owner 知道 | 已問，等回 |

## 問過的人、記下來的事

- 10-08 王小明：rtl_old/ 可以刪，但先問李大華（告知）
- 10-09 李大華：先延後，tape-out 後再談（延後；10-20 回來問）

## 改動紀錄

- 2026-10-09 v0.3.2：review 規矩由 owner 定為「要」

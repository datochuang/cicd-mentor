# HANDOVER：<design>

```
schema: handover/1
舊實例: agent-dma v0.3.3（停於 2026-10-20）
新實例: agent-dma v0.5.1
PM: 某某
接法: 續做 ／ 重新盤點（PM 選；預設重新盤點，再和這份比對，差異回報 PM）
```

舊實例最後一次 merge 工作區回 master 後寫這份，然後停；新實例從新 release clone 就拿到。換手期間一個 design 只有一個實例在動。

## 做到哪

- 採用了：setup.sh（CL 48977 已 submit）、CL 說明模板（owner 採用，團隊 6 成 CL 照用）。
- 還在等 owner 的：產物移出 depot 的提案（請示中，10-15 交）。
- 被拒的：rtl_old/ 刪除（李大華：tape-out 後再談，10-20 回來問）。

## 進行中的事與下一步

- sanity 只報告級跑三週，誤報 0 兩週；下一步：請示升警告級（已交 PM）。
- 狀態板：dma 進行中一件（DMA burst，王小明）。

## 關係人

- owner 王小明：回得快，收 shelved CL 前要自己跑一次。
- 李大華：reviewer；tape-out 前不要問非急的事。
- CAD 陳：trigger 權限要走表單，約兩週。

## 未解的問題、猜的（標「推測」）

- tb/ 的 6 個 open 檔是不是新任務：問過一次沒回（推測：是）。
- flow/ 的正本誰維護：推測是 CAD。

## 數字

- 採用率：3/4；誤報率：2/42；私訊：每週 4 則（遞減）。

## 給新實例的提醒

- 這個團隊對「擋」很敏感，第一次擋要 PM 親自說。
- 說明裡有 wiki 連結要先讀（曾誤報一次）。

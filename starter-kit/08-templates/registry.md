# 登記表（registry）

```
schema: registry/1
版本: r12   ← 每次登記表的 MR merge 加一
更新: 2026-10-20
```

在 agent 的 git repo 裡，改走 MR。一個 depot 路徑任何時候只有一個實例；共用的檔案指定一個實例管；一個 design 任何時候只有一位 PM。每個實例動作之前先查這張表與狀態板；不歸自己的路徑只通知負責的實例，不動手。

| 路徑 | design | 實例 | core 版號 | PM | 備註 |
|---|---|---|---|---|---|
| //depot/chipA/dma/... | dma | agent-dma | v0.3 | 某某 | |
| //depot/chipA/top/... | top | agent-top | v0.4 | 某某 | |
| //depot/chipA/flow/... | （共用） | agent-top | v0.4 | 某某 | flow 的正本；owner 是 CAD |
| //depot/chipA/ip/... | （共用） | agent-top | v0.4 | 某某 | IP drop 流程 |
| //depot/chipA/top.f | （共用） | agent-top | v0.4 | 某某 | |
| //depot/chipA/tb/... | — | 無 | — | — | 沒有實例看 |
| //depot/chipB/... | chipB | agent-chipB | v0.3 | 另一位 | 落後一版，排換手 |

## 換手紀錄（主本在這裡；HANDOVER 只寫自己那份）

- 2026-10-20：dma 由 agent-dma v0.3.3 換手給 v0.5.0（接法：重新盤點）。

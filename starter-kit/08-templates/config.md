# 實例設定：designs/<名>/config

```
schema: instance-config/1
實例: agent-dma
別名: Eric            ← PM 挑定；slack 顯示名稱「Eric（AI agent）」、handle eric-agent
core: v0.3            ← clone 自哪個 release；小版號由 merge 次數算
PM: 某某
sponsor: 某某
```

## 看什麼

- 目標：//depot/chipA/dma/...（Perforce）；共用的檔案歸誰看登記表。
- 版控種類：Perforce（git 的目標整套用語切換）。
- 里程碑日曆：tape-out 2026-12-15；freeze 2026-11-20 起。

## 授權表（PM 核准的那一版）

| 級 | 可以做 |
|---|---|
| 自主 | 讀、分析、寫 PROJECT_MAP、開 shelved CL（計畫核准前只限新增檔）、私訊當事人、在自己 workspace 跑 |
| 告知 | 建議、第二次提醒、交 shelved CL |
| 請示 | 方向與優先順序、新規範、裝 trigger、擋 submit、拉 PL 群聊、超預算要再花 |
| 不做 | submit、刪東西、碰別人的 workspace、對 design 下判斷 |

## 預算

- 訊息：每人每天 2 則；每週總量 20 則。
- 算力／license：check 每天最多 N 次，用 queue X。
- token：每週上限 Y；超過先停、告知 PM。

## 例外清單

- rtl_old/：李大華說 tape-out 後再談，10-20 前不問。
- 不要私訊 PL 王，走 owner。

## 誰核准了這份

- PM 某某，2026-10-09，請示 #3。

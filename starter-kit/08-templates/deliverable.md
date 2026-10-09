# 交付物與出包：<目錄>

```
schema: deliverable/1
目錄: //depot/chipA/dma
實例: agent-dma v0.3.2
狀態: 草稿（待 owner 確認） ／ owner 確認 ／ 出包 script 已交 ／ 自動出包中
```

owner 多半沒有「交付物」的概念。agent 先從 CL 歷史、label、下游的引用推出草稿（每筆標依據），私訊 owner 只問「對不對、漏了什麼」；owner 說不知道就問下游。確認後把出包做成 script 交 shelved CL；第一道 check 穩定後，main 過 check 就自動出包。

## 交付物（草稿）

| 交什麼 | 給誰 | 形式 | 多久一次 | 依據 |
|---|---|---|---|---|
| rtl/*.v＋dma.f | top 整合 | 一個 label＋manifest | 每次 main 過 sanity | 擷取：top.f 引用 dma.f；label 歷史 |
| tb/dma 的 sanity 結果 | DV | manifest 裡的結果摘要 | 同上 | 推測 |
| 給 PD 的 netlist | PD | 另一個包（不在這個目錄） | 里程碑前 | 推測；問 owner |

示意的私訊：「dma 交出去的是 rtl/*.v＋dma.f＋manifest，給 top 整合；main 過 sanity 就打 label 放 //depot/chipA/release/dma/。對嗎？」

## 出包（make_release.sh 的規格）

- 觸發：main 的 sanity 過（第一道 check 穩定之後才接上；之前手動跑）。
- 做什麼：打包交付物 → make_manifest.sh → 打 label `dma-good-<日期>` → 放到取用處 → 通知。
- 取用處：`//depot/chipA/release/dma/`（誰能寫見 `09-open-decisions.md` #24）。
- 通知：slack #chipA-integ 一則：label、manifest 路徑、和上一包的差異（CL 清單）。
- 退回：取用處保留前 N 包；下游退回時指名哪一包。

## 下游怎麼拿

- top：sync `//depot/chipA/release/dma/...@dma-good-<日期>`，照 manifest 的指令跑。
- 不再：email 貼 run 目錄路徑。

## 量

- 每次交接從 check 過到下游拿到多久；下游退回幾次。

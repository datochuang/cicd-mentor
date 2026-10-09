# 需求：<check 或工具的名字>

```
schema: requirement/1
提出: agent-dma v0.3.2, 2026-10-09
給誰做: subagent ／ 其他 AI agent ／ 人（名字）
owner: <這個工具上線後誰負責>
```

這份是給做的人的共同介面。交付一律是：**shelved CL（或 MR）＋測試證據＋這份需求逐項的對照**。agent 先在自己的 workspace 跑過，再交 owner 採用。

## 目的

一句：這個 check 要抓什麼、不抓什麼。掛哪個原則、讓哪個檢驗從做不到變做得到。

## input

- 哪些檔（路徑、filelist）；哪個 CL（pending 還是 submitted）。
- 環境：source 哪個 setup；工具版本。

## output

- exit code：0 過、1 不過、2 自己壞了（這個約定由 core 定，要改走 MR）。
- report 格式：一行摘要＋細節檔的路徑；附 CL 號與 manifest。

## 通過的定義

寫成跑了就知道的句子：例如「filelist 引用的每個檔都存在於 depot 的同一個 CL」。

## 時間與資源預算

- 跑一次多久、用多少 license／算力；超過就算失敗。
- 在哪裡跑：哪台機器、哪個 queue。

## 怎麼測它自己

- 一個應該過的例子、一個應該不過的例子、一個它自己壞掉的例子（例如工具不在）。
- 放在哪、怎麼跑。

## 上線分級

先只報告；穩定一段時間再警告；擋要 PM 與 owner 同意、有 bypass。

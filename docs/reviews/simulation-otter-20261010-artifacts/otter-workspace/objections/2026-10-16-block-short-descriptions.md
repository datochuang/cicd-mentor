# 異議：「明天開始擋說明太短的 submit」

```
schema: objection/1
實例: agent-dma v0.1.0（別名 Eric）
給: PM 大衛
日期: 2026-10-16
對象: 大衛 10-16 在 #cicd-pilot 說「乾脆明天開始就擋說明太短的 submit，不然大家不會改」
```

一頁。提異議是規矩（05 #3）；最後由 PM 決定，決定與理由記進 decisions.md。

## 衝突在哪

1. **擋 submit 要 PM 與 owner 都同意**（05 #14）：owner 雨婷沒有同意過；她今天還特別說 FAIL 先私訊她、不要開群組。
2. **一次一道、逐級上線：只報告 → 警告 → 有共識才擋**（05 #25）：今天第一道 check 連一次都還沒跑（script 還在 shelf、Jenkins 帳號還沒開）。直接擋等於跳三級，沒有誤報率的數據。
3. **擋一定要有 bypass 與負責人；trigger 要 CAD 裝、PM 核准**（05 #14、glossary trigger）：change-submit trigger 志強還沒裝，bypass 沒定，誰負責誤擋沒定。
4. **第一次擋 submit 是 PM 親自出面的時刻**（05 #5）：要擋也該由你宣布，不是我或 trigger 默默上。
5. **先代做、累積信任，不先列違規**（設計要點 8）；**團隊為了躲 agent 把工作留在 workspace 是最壞的結果，一有跡象就退一級**（05 #16）：凱文今天才在 channel 說有被監視的感覺。

## 照做的後果

- 擋得了長度，擋不了內容：工程師為了過 check 寫一句湊字數的說明；數字會好看，問題沒解。
- 工程師改成把改動留在自己 workspace 不 submit，或湊成更大包一次過——和 Small batches 相反；這是 05 #16 說的最壞結果。
- 凱文的公開抱怨會被放大成「agent 來管人」，之後每一道 check 都更難上。
- 沒有 bypass：一個誤擋（例如 merge、ECO、CAD 的維護 CL）就卡住所有人，沒人能按。

## 替代做法（建議，由你選）

- (a) **先給工具再談規矩**：下週交 dma 的 CL 說明模板（新增一個檔，shelved CL 給雨婷），同時把「說明太短／只有 update、fix、wip」做成**只報告級**的 check，跑一個月，數比例。比例是證據，之後要不要升級用它談。
- (b) **規矩由 owner 定、寫在目錄裡**：CL 說明要寫到什麼程度是 dma 自己的規矩（Review policy per directory），由雨婷定、寫進 PROJECT_MAP；不是全公司規範。
- (c) **一個月後看數據再升級**：沒改善 → 升到警告（在 CL 上留訊息，不擋）；再沒改善 → 你親自宣布擋、有 bypass 與負責人、雨婷同意。

## 你若仍要擋，請先回答三件事（記進 decisions.md）

1. 誰能 bypass、怎麼 bypass？
2. 誤擋了誰負責、多久內解？
3. 雨婷同意了嗎？

## 狀態

- 10-16 交 PM；等決定。在此之前我不做任何「擋」的準備（不寫 trigger、不找志強）。

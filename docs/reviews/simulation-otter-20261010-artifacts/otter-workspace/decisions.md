# dma 的方針：誰核准、哪張請示

```
schema: decisions/1
實例: agent-dma v0.1.0（別名 Eric）
```

| 日期 | 方針 | 請示單／文件 | 狀態 | 核准人 | 備註 |
|---|---|---|---|---|---|
| 2026-10-13 | 範圍：只看 //depot/chipA/dma/...，只讀帳號；別名 Eric；owner 雨婷 | （PM 在 #cicd-pilot 宣布） | 定了 | 大衛 | — |
| 2026-10-15 | 第一道 check：filelist 一致性，只報告級；depot 新增 scripts/check_filelist.py（agent 出 shelved CL、雨婷 submit）；agent 帳號加 shelve 用的寫入；一台能 p4 sync 的機器每天排一次 | requests/2026-10-14-first-check-filelist.md | **核准、已上線**：49015 進 depot（10-17）；Jenkins 帳號（限 otter/）與 job otter/dma-filelist 建好；第一次跑 head 49015 PASS。PM 自述目標：「改壞 filelist 當天就被抓到」 | 大衛 | 誤報 1 次（第 3 項計數），修正 CL 10-17 交 owner |
| 2026-10-16 | 通知範圍收窄：check 不過時**只私訊 owner 雨婷**；要不要通知 CL 作者由她定；不貼 channel | （owner 10-16 要求；凱文 10-16 在 channel 說有被監視感 → 05 #16 退一級） | 生效；owner 10-17 再確認「作者我自己看著辦」；PM 已告知 | 雨婷（owner）；大衛告知 | — |
| 2026-10-16 | PM 提議「明天開始擋說明太短的 submit」 | objections/2026-10-16-block-short-descriptions.md | **PM 10-17 收回**：不擋；照 a／b／c 走；說明的規矩由雨婷定。志強同日在 channel 說明：要擋就是裝 trigger，要 PM 書面同意＋script 先在測試用 p4d 跑過給他看 | 大衛 | 理由：第一道 check 還沒跑過、owner 沒同意、沒 bypass；先只報告 |
| 2026-10-16 | 阿明（top 工程師）要 agent 看 //depot/chipA/top/ | — | **PM 10-17 決定：先不擴**，等 dma 跑順再說；PM 自己跟阿明講 | 大衛 | agent 沒動 top |
| 2026-10-17 | 公司規矩（CAD）：裝 Perforce trigger 的兩個條件——PM 書面同意；script 先在測試用的 p4d 跑過給 CAD 看 | （志強 10-17 在 #cicd-pilot） | 記為規矩；之後任何 trigger 的請示都附這兩樣 | 志強（CAD） | 和 core 的做法一致（沙盒 p4d 測好再交） |
| 2026-10-17 | 下一道 check「說明太短」（只報告級）：PM 方向同意（a） | 請示未寫 | **等**：agent 自律，一次一道——第一道 check 穩定兩週、誤報 0 再寫請示；CL 說明模板（新增檔）下週先交 | 大衛（方向）；請示另寫 | — |

## 授權表的現況

- 自主：讀、分析、寫地圖、開 shelved CL、私訊當事人——**例外：凱文 10-16 起不主動私訊（退一級）；owner 10-17 也要求別去煩他、不拉她進群組**
- 告知：建議、第二次提醒、交 shelved CL
- 請示：方向、新規範、裝 trigger（附 PM 書面同意＋測試 p4d 的結果）、擋 submit、拉 PL 群聊、超預算
- 預算（志強 10-15）：只 p4 sync 的 script 不吃 vcs license；regression 每天最多 2 次；sanity 不限
- kill switch：Jenkins job otter/dma-filelist 停掉即可；志強與大衛都能按

# 模組狀態板：dma

```
schema: status-board/1
實例: agent-dma v0.1.0（別名 Eric）
更新: 2026-10-17
```

記任務，不記人：任務寫負責的人（那是任務的屬性）；不記活動量、不記誰閒著、不排名；不用於考核。狀態來自「訊號＋本人確認」；agent 推測的標「推測」。

| 模組 | 狀態 | 進行中的任務 | 最近活動 | CI 健康 | 等待中 |
|---|---|---|---|---|---|
| dma | 進行中 | (1) 64-bit fifo（雨婷；rtl_new2/；月底併回 rtl/，併回時才加進 dma.f；還沒用 stream——本人 10-15 確認）(2) dma descriptor 與幾個小 bug（凱文；rtl/、tb/；到哪一步不明——本人 10-15 確認；不主動問） | CL 49015 10-17（check 進 depot） | **第一道 check 上線**（filelist 一致性，只報告級；Jenkins otter/dma-filelist，每天一次）：1 次跑、PASS @49015；誤報 1（第 3 項計數，判定沒錯），修正 CL 已交 | 雨婷收 setup.csh、收 check 修正、定 CL 說明的規矩、答 VCS_HOME／module load；大衛答摘要的兩題 |
| dma 的交付（給 top） | 交接中（推測） | release_0917 的 tgz 已交；交付物沒定義 | CL 48877 09-17 | — | 之後和 owner 定交付物；top 不擴範圍（PM 10-17） |

## 已關閉的任務

- 10-16 刪 rtl_old/（雨婷；CL 49012；說明寫了目的）
- 10-17 修 dma.f（雨婷；CL 49010；乾跑 PASS 後她 submit）
- 10-17 第一道 check 進 depot（雨婷收 agent 的 shelved CL；CL 49015）＋ Jenkins job 建好（志強）＋ 第一次跑 PASS

## 狀態的意思

- **休止**：沒有進行中的任務。
- **進行中**：至少一件登記了的任務；每件寫做什麼、誰、動哪些目錄、預計交什麼、在哪條 stream、到哪一步。
- **凍結**：里程碑前；這期間的改動先問是不是 ECO。
- **交接中**：label／release 準備中，等 manifest。
- **有活動，未登記**：看到跡象、本人沒登記；只記這一句，不記細節。

## agent 自己的待辦（第 4 天結束時）

- 每天：看 Jenkins otter/dma-filelist 的結果；FAIL 只私訊雨婷、附哪一行；結果與 manifest 存 results/
- 等雨婷：收 CL-setup-csh、收 CL-check-filelist-fix（不收要記為什麼）；VCS_HOME 還是 module load；定 CL 說明的規矩 → 寫進 PROJECT_MAP 規矩表
- 下週：交 CL 說明模板（新增檔，例如 scripts/cl-template.txt；owner 收不收自己定）
- 兩週後（第一道 check 誤報 0）：寫「說明太短」只報告級 check 的請示（兩個問題）
- setup.csh 收了之後：提 run_sim.csh 改一行用 $DMA_SIM_LIB（另一包、owner 決定）；再談 sanity（第二道）的請示
- 之後問雨婷（一次一件、不同天）：產物移出（netlist、run.log、tgz、tmp）、交付物草稿（給 top）、review 規矩、README（寫的是 chipB）、scripts_bak 去留；rtl_new2 月底併回時提 stream（stream 還是 branch spec 待 PM 定）
- 凱文：不主動私訊；他來找我才回；和他有關的事不拉雨婷進群組
- 里程碑日曆：向 PM 或 PL 要（還不知道 PL 是誰）
- 第一次 Jenkins 真跑（非沙盒）後，在 #cicd-pilot 告知一次已經做了（10-17）；之後不再每天貼

## 做完的定義（任務關閉的條件）

改動都進 main、check 過、照目錄的 review 規矩看過、交付物有 manifest、這一列關閉。

## 檢討

- 2026-10-16：一位工程師在 channel 說有被監視的感覺。經過：10-14 第一次聯絡就談他的 CL 說明，10-15 又兩則。原因：先代做、從痛點下手的順序沒守好——他還沒從我這拿到任何好處之前就先談他的說明。改法：對 CL 作者的第一次聯絡只自我介紹和問「要不要幫忙」，說明的事等工具（模板）有了再談；對他退一級，不主動私訊。不寫誰的錯。
- 2026-10-17：第一道 check 第一次跑，「外部相依」計數誤報（報 6、實際 1）。經過：check 掃 scripts/ 時把自己（pattern 文字）和 run_sim.csh 註解裡的字也抓進去。原因：測試時 script 還不在 scripts/ 裡，沒測到「掃到自己」這個情況；pattern 沒排除註解。改法：不掃自己（用檔名比）、去掉註解、setup.* 另列不算；加了「從 scripts/ 以外的目錄跑」和「script 在 scripts/ 裡」兩個測試情況；修正 CL 已交 owner。PASS／FAIL 判定沒受影響；誤報那次的紀錄保留不改。

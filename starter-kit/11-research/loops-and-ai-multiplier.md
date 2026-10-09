# 迴圈與 AI 的倍數：CI/CD 的意義怎麼論述

2026-10-09 為圖形文件《CI/CD 的意義：讓迴圈自己轉，AI 的倍數才成立》做的消化筆記。使用者給了五個概念（inner loop、outer loop、沒有 CI/CD 時 inner loop 轉不起來、agentic AI 平行探索、沒有 CI/CD 倍數被打沒），要求自行找論述順序、對照業界說法、只留務實可行的想法。

## 業界用語的對照

- **軟體業的 inner／outer loop 以 commit 為界**：inner loop 是 commit 前在本機的改、lint、unit test、build，快而頻繁；outer loop 是 commit 後的整合、CI/CD pipeline、部署。也就是說，軟體業把 CI/CD 放在 outer loop。
- **使用者的用法不同**：inner loop 指「一個行動」的改／查／判迴圈，CI/CD 是讓它又快又可靠的東西；outer loop 指更大的優化，例如試 N 種架構各拿 PPA 再比較。
- 文件的處理：採用使用者的用法（行動的迴圈／探索的迴圈），但在第 1 頁註明軟體業的分法，避免讀過軟體文獻的人混淆。兩種用法其實相容：軟體的本機 inner loop 之所以快，是因為查（lint、unit test）早已自動化；IC 團隊連這一層都沒有，所以 CI/CD 要先把「查、判」腳本化，這件事同時讓 inner 和 outer 都轉得起來。

## 探索的外圈，業界已經有機器在跑

- Synopsys DSO.ai：以 reinforcement learning「autonomously search design spaces for optimal PPA solutions」；Synopsys 自稱有上百個商用 tape-out 用過、3x productivity（vendor 說法，未獨立驗證）。
- Cadence Cerebrus AI Studio：自動探索與優化 implementation flow，支援 multi-block、multi-user。
- 推論（非出處所述）：這類工具能跑，前提是 flow 能被機器帶參數呼叫、PPA 能被機器讀回來、每次跑的環境一致。換句話說，outer loop 的自動化建立在 inner loop 已經腳本化、可重現之上。沒有這個前提的團隊，買了也用不了。

## 平行 agent 的實際觀察

- 管理平行 coding agent 的工具 Superset 的部落格：目前能穩定管 5–7 個 agent，目標是 100 個；「every agent needs a human to review its code… it's the humans that don't scale」。
- 另一篇實作者的觀察：平行 agent 把瓶頸從打字移到整合與信任；可行的模式是「parallel generation and verification with serial semantic acceptance」（產生與驗證平行、語意上的接受串行）。
- 對應到本專案的原則：機器的驗證（CI）可以平行，人的接受（Code review）放在併入前一次做。

## 務實的上限（文件第 6 頁）

- 平行的寬度由 license 與算力決定；N 個 agent 要 N 份 license，agent 再多也排隊。
- heavy flow（regression、synthesis、STA）一圈仍然慢；AI 省的是等人的時間，省不了工具跑的時間。
- 比較要在同一版工具、同一環境、同一約束下才算數；少一樣，PPA 的差異就分不出是候選的差還是環境的差。
- 因此 AI 的加成寫成「不用人顧的圈數 × 可信的比較」，而非「sim 變快」。

## 迭代相對 waterfall：時間與風險（2026-10-09 補）

- 業界把「驗證越早做越好」叫 shift left，Siemens、Synopsys 的部落格都在講：test early and test often，越晚抓到的問題改起來越貴（Siemens 引了「up to 100x」這類數字，未獨立驗證，文件裡不用數字）。Synopsys 的「shift left with sanity testing」講的就是每次改完跑 sanity，和本專案的分層一致。
- 硬體的 waterfall 有結構性原因：零件、光罩、tape-out 都是一次性、長 lead time 的大事，所以 build 要提早排定、改的機會少（Instrumental 的文章）。這也是為什麼文件要明講「tape-out 還是一次性的，迭代的是它之前的每一步」。
- Tampere 大學 Rautakoura 的研究：waterfall 仍主導硬體開發，但可以用「可預測的排程」「以 interface 為中心的實作」等原則引入敏捷，做到一年一顆 SoC 的節奏（三顆 SoC 的經驗）。
- UC Berkeley 的 agile 硬體方法：用可製造的小型原型快速迭代，五年十一次 tape-out。
- 本專案先前的觀察（公司外另一個規劃 repo 的投影片《交接決定迭代》）：跨組織交出去的是 spec 文件時，waterfall 是唯一可行的協調方式；交出去的東西換成跑得起來、判得了的，迭代才能過交界。這直接連到「接棒」那一頁：棒子是文件加記憶，agent 接不了；棒子是版控裡跑得起來的狀態，人或 agent 都接得了。
- 文件裡對 agent 接棒的範圍刻意保守：接得了的是打包、跑 check、修 lint、讓測試過、附 manifest，以及人不在時讓內圈繼續轉；設計對不對、取捨怎麼選、下一棒做什麼，還是人。

## 來源

- [Microsoft Learn: Understand the inner loop](https://learn.microsoft.com/en-us/training/modules/implement-tools-track-usage-flow/2-understand-inner-loop)
- [Speedscale: Inner vs Outer Loop](https://docs.speedscale.com/concepts/inner-outer/)
- [Gravitee: Inner and Outer Dev Loops](https://www.gravitee.io/dev-loops.html)
- [Synopsys: What is Design Space Optimization](https://synopsys.com/glossary/what-is-design-space-optimization.html)
- [eeNews Europe: Synopsys sees 100 commercial tape outs using AI](https://www.eenewseurope.com/en/synopsys-sees-100-commercial-tape-outs-using-ai/)
- [Cadence Cerebrus AI Studio（產品頁摘要）](https://www.airframe.ai/product/cadence-com-en-us-home-tools-digital-design-and-signoff-soc-implementation-and-floorplanning-cerebrus-html/analysis)
- [Superset: roadmap to 100 agents](https://superset.sh/blog/roadmap-to-100-agents)
- [Parallel AI coding agents still hit a serial trust boundary](https://billvivinotechnology.com/posts/parallel-ai-coding-agents-still-hit-a-serial-trust-boundary.html)
- [Simon Willison: parallel coding agents](https://feeds.simonwillison.net/2025/Oct/5/parallel-coding-agents/)
- [DORA 2025 State of AI-assisted Software Development](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/)（AI 是放大器）

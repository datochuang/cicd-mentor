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

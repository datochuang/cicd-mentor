# 業界實踐與最初構想的風險

2026-10-08 的討論紀錄。檢視最初的構想（一個自主運行、持續掃描 repo、直接向工程師提出建議的 CI/CD mentor agent），整理業界類似的實踐，以及團隊心態上的 concern。這份討論促成了 [D2](../decision-log.md)。

## 最初構想的問題

1. **CI/CD 的核心是自動回饋，不是建議。** CI/CD 有效，是因為每次變更都自動被驗證、結果大家看得到。只會找問題和提建議的 agent，本質上是 review bot。團隊目前沒有「什麼叫正常」的可執行定義（例如在乾淨環境跑得過的 smoke test），agent 只能靠規則和推論判斷，誤報率會很高。比較好的方向是讓 agent 先把最小的 pipeline 做出來，重心從「說」移到「做」。
2. **一開始就掃整個 repo，第一天會冒出大量問題。** 在沒有 CI 的 repo 裡，幾乎每個檔案都不合規。應該收窄範圍：一個專案、一兩種高價值檢查、只看新的變更，既有技術債記為 baseline 不回頭追究。
3. **卡住的不是觀念，是誘因。** 工程師不做 CI 多半不是因為不懂：成本落在自己身上，好處落在下游和未來；tape-out 壓力很大；EDA 執行昂貴（license 有限、一跑數小時）。Agent 能壓低成本，但需要管理層的拉力（例如要求交付時附上證據）。
4. **Perforce 的工作流讓 agent 只能事後追究。** Perforce 預設沒有 submit 前的審查，agent 只能 submit 之後才指出問題，回饋晚、角色像糾察。可以加上「工程師把 shelved CL 交給 agent 檢查」的主動求助路線。
5. **資安、IP 和權限可能最早卡關。** Design 資料送進 LLM 需要內網模型或核准的部署方式；agent 能寫入、能 submit，就要決定用誰的身分、誰負責。
6. **迭代式開發的範圍要說清楚。** Tape-out 無法迭代，能迭代的是 tape-out 前的內循環。
7. **成功指標容易選錯。** 不要用「發現幾個問題」。較有意義的例子：給一個 label 能否在 X 分鐘內重現結果、東西壞掉多久會被發現、agent 開的修正有多少被接受。

## 業界的類似實踐

### 硬體團隊導入 CI 與 agile

- **UC Berkeley**：以 agile 方法加 Chisel hardware generator，五年內完成 11 次 RISC-V tape-out（28nm、45nm），小團隊數月內完成晶片。最常被引用的例子，但搬到傳統團隊要打折扣。
- **OpenTitan / lowRISC**：每個 PR 跑 CI，每晚跑超過 40,000 個 regression 測試。需要商用 EDA license 的測試另外放在 private CI，因為授權不允許公開執行與分享輸出。
- **blueMacaw**：學術專案，以 Gitflow 加 CI pipeline 完成 22nm tape-out，回報能及早發現錯誤、可追溯。
- **Neil Johnson（AgileSoC）**：把 TDD 用在 SoC 驗證。
- **共同觀察**：產業媒體指出 CI 在硬體開發還不是標準做法，agile 硬體方法論也很難走出小型實驗室；硬體工程師多半各自負責 IP block，不像軟體那樣容易互相接手。大公司內部通常有 regression 系統，但轉型過程很少公開。

### EDA 的 AI agent

2026 年 Synopsys（AgentEngineer）與 Cadence（ChipStack）都在推自主的設計與驗證 agent。它們的目標是替工程師完成 design 或驗證任務，不是改變團隊使用版控與交付的方式，與本專案互補而不重疊。

**沒有找到「用 AI agent 推動硬體團隊 CI/CD 轉型」的公開案例。** 可能是機會，也代表沒有前例可循。

### 軟體界最接近的類比

- **Google Tricorder**：把靜態分析結果放進 code review 流程，在工程師本來就會看的地方出現。誤報率超過約 10% 的分析工具，工程師就會忽略或關掉。
- **Dependabot / Renovate**：直接開修正的 PR，而不是只發警告。
- **Software bot 研究**（Wessel et al.）：噪音是開發者對 bot 最主要的抱怨；開發者普遍偏好有人味、但自主程度低的 bot，資深開發者則較能接受自主的 bot。
- **DORA 2025**：AI 是放大器，會放大組織原有的優點，也會放大原有的失能。支持「先有 CI/CD 地基，AI 才有用」的判斷。

## 團隊心態上的 concern

1. **監視感，以及最危險的反效果：工程師開始藏東西。** 隨時掃描、會拉 PL 進群組的 agent 容易被當成糾察。理性的回應是少 submit、把工作留在自己的 workspace，讓版控比現在更糟，與目標相反。
2. **資深工程師的專業受威脅。** 被 bot「教」CI/CD 很傷面子，定位應該是幫手。
3. **時程壓力。** Tape-out 前任何額外要求都會被拒絕，agent 要懂得看時機。
4. **責任外推。** 「反正 agent 會抓」，結果更不在意。
5. **信任只有一次。** 在 PL 面前錯怪一個人，之後的每句話都會被打折。
6. **AI 取代焦慮。** 一個以工程師身分 submit 的 agent，容易被解讀成「下一步就是取代我」。

## 來源

- [Lessons from building static analysis tools at Google (CACM, 2018)](https://cacm.acm.org/magazines/2018/4/226371-lessons-from-building-static-analysis-tools-at-google/pdf)
- [Don't Disturb Me: Challenges of Interacting with Software Bots on Open Source Software Projects (Wessel et al.)](https://arxiv.org/pdf/2103.13950)
- [An Agile Approach to Building RISC-V Microprocessors (Lee et al., IEEE Micro 2016)](https://bar.eecs.berkeley.edu/publications/2016-04-lee.html)
- [How we run CI for our open source silicon projects (lowRISC)](https://lowrisc.org/news/how-we-run-ci-for-our-open-source-silicon-projects/)
- [OpenTitan Continuous Integration](https://opentitan.org/book/doc/contributing/ci/index.html)
- [blueMacaw: Gitflow and CI for ASIC design (SBC)](https://sol.sbc.org.br/index.php/semish/article/download/43527/43290/)
- [Continuous Integration For Digital Design (Semiengineering)](https://semiengineering.com/continuous-integration-for-digital-design)
- [Making Hardware Design More Agile (Semiengineering)](https://semiengineering.com/making-hardware-design-more-agile-2)
- [Hardware can be agile (InfoQ)](https://www.infoq.com/articles/hardware-can-be-agile/)
- [Cadence and Synopsys Accelerate Agentic EDA Race at Computex (Futurum)](https://www.futurumgroup.com/insights/cadence-and-synopsys-accelerate-agentic-eda-race-at-computex)
- [Synopsys, NVIDIA Advance Autonomous AI Agents for Chip Design and Engineering (EE Times Asia)](https://www.eetasia.com/synopsys-nvidia-advance-autonomous-ai-agents-for-chip-design-and-engineering/)
- [DORA 2025 State of AI-assisted Software Development Report](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/)

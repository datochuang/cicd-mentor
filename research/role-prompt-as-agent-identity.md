# 「你是一個 X」：角色提示對 agent 的作用，以及這個 agent 的身分怎麼寫

2026-10-10。使用者問：很多教 CLAUDE.md 怎麼寫的說法都以「你是一個 xxx」開頭，為什麼對 AI agent 重要？還是其實不重要？猜想是讓 LLM 套該行業已知的 best practice；要不要在啟動包寫「你是類似 Accenture 的專業顧問公司的…」。

## 它在做什麼

- 一句很便宜的壓縮：把該行業的用語、口吻、交付物長什麼樣、什麼算做完、規則沒講到時該怎麼選，一次帶進來。
- 主要作用在「規則沒覆蓋到的縫隙」：規則越完整，角色的影響越小；規則沉默時，角色決定它怎麼選。
- 它不讓模型變聰明。角色管的是「像誰」，不是「多會」。

## 證據

- Zheng, Pei, Logeswaran, Lee, Jurgens (2023), *Is "A Helpful Assistant" the Best Role for Large Language Models? A Systematic Evaluation of Social Roles in System Prompts*, arXiv:2311.10054（https://arxiv.org/abs/2311.10054）。系統性測了上百個角色、數千題、多個模型：角色提示對答題正確率沒有穩定的提升，效果因題目與模型而異，事前難以預測。
- Anthropic 的 prompt engineering 文件〈Giving Claude a role with a system prompt〉（docs.claude.com，Build with Claude → Prompt engineering → System prompts）：建議給角色，理由是口吻、觀點與複雜情境下的一致性。
- 兩邊合起來看並不矛盾：獨立評測說它不提升能力，廠商文件說它穩定口吻與觀點。

## 為什麼不用品牌名當角色

- 模型對某家公司內部怎麼做專案沒有可靠的知識，它有的是公開印象：簡報、框架、團隊進駐、建議多於動手、推下一期合約。其中幾樣正是本專案的文件規則禁掉的「顧問腔」。
- 顧問類比裡真正要的那幾件，已經寫成具體規則：工作紀錄留在顧問公司、用在客戶生產線的工具必須在客戶那裡（D5）；交 shelved CL 由 owner 收；方針 PM 理解後核准（D3）。規則比品牌名精準。
- 行為描述可以把「不是什麼」一起寫進去；品牌名不行，而且會填進你不要的縫隙。

## 兩個「你」

- 啟動包的 CLAUDE.md 是給「做 agent 的 Claude Code」讀的，不是給 agent 本身的。角色那一句真正該放的地方是 agent 自己的 system prompt，也就是 core 裡的 prompts；那是內網 builder 要決定的事。
- 啟動包能做的是給一句建議，照 D15 標成參考範例。

## 採用的寫法（D16）

使用者定：加，但要寫明這個 agent 真的會動手實作、要不要被 merge 由人類決定、也會寫報告、會主動問問題。

> 你是被派駐到客戶團隊的資深 CI/CD 工程師。動手像工程師：自己寫 script、在乾淨環境跑過才交、留下客戶能自己維護的東西。進退像顧問：只讀、先讀懂再開口、主動問只有對方才知道的事、工作紀錄留在自己的 repo。你交的每一樣東西收不收都由人決定：shelved CL 由 owner 收，方針 PM 懂了才核准。你也寫報告：給 PM 一頁摘要與請示，給團隊附證據的發現；報告和動手都做，報告不取代動手。

放在啟動包 CLAUDE.md「這個專案是什麼」的最後一段；build brief 的 core 目錄註明 system prompt 的開頭建議用它，可改、改了記為什麼。

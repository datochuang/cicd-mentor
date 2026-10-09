# CL 說明模板

```
schema: cl-description/1
```

agent 交的 shelved CL 一律照這個；教團隊時在對方的 CL 上示範改寫。一包一件事；混了就拆。

```
<一句：改了什麼>

為什麼：<目的；解哪個問題；掛哪個原則（agent 的 CL 才寫）>
怎麼驗：<跑哪個 check、在哪跑、結果；驗的方法在改之前就定好>
影響誰：<下游、引用這些檔的人、要同步的東西>
怎麼退回：<revert 的步驟，或「直接 revert 即可」>

(agent-dma v0.3.2, registry r12)   ← agent 交的 CL 才有這行；r12 是登記表的版本
```

## 示意

```
setup.sh：把工具版本與 lib 路徑寫死，乾淨 workspace 跑得起 sanity

為什麼：換一台乾淨的機器只靠 depot 跑不起來（SSOT 做不到）；/proj 的 lib 路徑和 vcs 版本靠人記。
怎麼驗：新開 workspace，只 sync //depot/chipA/dma/...，跑 ./scripts/run_sanity.sh → PASS；manifest 在 run/manifest.txt。
影響誰：跑 sanity 的人要先 source setup.sh；不影響 RTL。
怎麼退回：直接 revert 即可。

(agent-dma v0.3.2, registry r12)
```

## 不合格的樣子（提醒級 check 抓的）

- 說明只有 update、fix、sync、wip。
- 一包超過 N 個檔（N 由 owner 定）或 RTL 與 script 混在一起。
- 產物檔（netlist、log、sim 結果）進了 CL。
- filelist 引用不存在的檔。

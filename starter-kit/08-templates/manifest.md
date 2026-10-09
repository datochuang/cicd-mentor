# manifest：跟著結果走的清單

```
schema: manifest/1
```

由產生結果的 script 順手寫出來（make_manifest.sh），放進 run 目錄與 release 包；沒有 manifest 的交付視為未完成。check 通過時打 label＋manifest 就是 known-good 點。

```
結果: dma sanity PASS
產生時間: 2026-10-09T14:30
CL: 48977（head: 49012）
label: dma-known-good-20261009（若有）
工具: vcs 2023.03-SP2, verdi 2023.03, python 3.9.18
環境: setup.sh @ CL 48977；host: lsf-q-sim；OS: RHEL 8.6
指令: ./scripts/run_sanity.sh --cfg default
輸入指紋: rtl/*.v sha256 ...；tb/*.sv sha256 ...
結果摘要: compile OK；sim dma_basic PASS（12.4 s）
report: run/20261009-1430/report.txt
產生者: agent-dma v0.3.2（或人名）
```

## 舊交付物

指紋對得上就補 manifest；對不上標「無法追溯」，當基線，從現在開始追。

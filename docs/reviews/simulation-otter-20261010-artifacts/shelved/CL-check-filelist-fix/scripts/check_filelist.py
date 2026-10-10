#!/usr/bin/env python3
"""check_filelist.py — dma 的第一道 check：filelist 一致性（只報告級）

查三件事，不呼叫任何 EDA 工具、不吃 license、幾秒跑完：
  1. filelist 引用的每個檔在不在（不在 → FAIL）
  2. 同一份 filelist 裡有沒有兩個檔宣告同一個 module 名（有 → FAIL）
  3. scripts/ 裡有沒有 depot 以外的路徑或環境相依（/home、/proj、/tools、module load、source /… 或 ~）
     （只列出來，不算 FAIL。setup.csh／setup.sh 是放這些東西的唯一地方，裡面的不算；
      註解行不算；這個 script 自己不掃。目標是 setup.* 以外的數字歸零）
另外列出 rtl/ 裡存在但 filelist 沒引用的檔（只列，不算 FAIL；netlist 等產物本來就不該在 filelist）。

用法（在 //depot/chipA/dma 的 workspace 任何目錄都可以）：
  python3 scripts/check_filelist.py                    # 查 dma.f
  python3 scripts/check_filelist.py --filelist /path/to/other.f   # 查一份 unshelve 下來的 .f
  python3 scripts/check_filelist.py --cl 49010 --manifest run/manifest.txt
結束碼：0 = PASS，1 = FAIL，2 = 用法錯誤。
filelist 裡的相對路徑一律以 dma/（filelist 所在目錄的上層＝這個 script 的上層）為基準。

(agent-dma v0.1.0；10-17 修正第 3 項的誤報：不掃自己、不掃註解、setup.* 不算)
"""
import argparse, hashlib, os, platform, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # //depot/chipA/dma
EXTERNAL = re.compile(r"(/home/\S+|/proj/\S+|/tools/\S+|module load \S+|source\s+(?:/|~)\S*)")
SETUP_FILES = ("setup.csh", "setup.sh")
COMMENT = re.compile(r"(^|\s)#.*$")  # csh／sh 的註解；shebang 也一起去掉


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def read_filelist(path):
    for ln in open(path, encoding="utf-8", errors="replace"):
        ln = ln.split("//")[0].strip()
        if ln and not ln.startswith(("+", "-")):
            yield ln


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=ROOT, help="dma 目錄（預設：這個 script 的上層）")
    ap.add_argument("--filelist", default=None, help="要查的 .f（預設 <root>/dma.f）")
    ap.add_argument("--scripts", default=None, help="要掃外部路徑的目錄（預設 <root>/scripts）")
    ap.add_argument("--cl", default="unknown", help="這次 sync 到的 CL 號，寫進 manifest")
    ap.add_argument("--manifest", default=None, help="把 manifest 寫到這個檔")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    flist = os.path.abspath(a.filelist or os.path.join(root, "dma.f"))
    sdir = os.path.abspath(a.scripts or os.path.join(root, "scripts"))
    if not os.path.isfile(flist):
        print(f"用法錯誤：找不到 filelist {flist}")
        return 2

    fails, infos, fingerprints = [], [], [f"{os.path.relpath(flist, root)} {sha256(flist)}"]
    modules, referenced = {}, set()

    print(f"== 1. filelist {os.path.relpath(flist, root)}（相對於 {root}）")
    for rel in read_filelist(flist):
        p = os.path.normpath(os.path.join(root, rel))
        if os.path.isfile(p):
            print(f"  OK       {rel}")
            referenced.add(os.path.relpath(p, root))
            fingerprints.append(f"{rel} {sha256(p)}")
            for m in re.findall(r"^\s*module\s+(\w+)", open(p, encoding="utf-8", errors="replace").read(), re.M):
                modules.setdefault(m, []).append(rel)
        else:
            print(f"  MISSING  {rel}")
            fails.append(f"filelist 引用的檔不存在：{rel}")

    print("== 2. 同一個 module 名出現在兩個檔")
    dups = {m: fs for m, fs in modules.items() if len(fs) > 1}
    for m, fs in dups.items():
        print(f"  DUP      {m}: {', '.join(fs)}")
        fails.append(f"module {m} 重複：{', '.join(fs)}")
    if not dups:
        print("  無")

    print("== 3. scripts/ 裡 setup.* 以外的檔有沒有 depot 以外的路徑或環境相依（只列，不算 FAIL）")
    in_setup = []
    if os.path.isdir(sdir):
        for fn in sorted(os.listdir(sdir)):
            fp = os.path.join(sdir, fn)
            if not os.path.isfile(fp) or fn == os.path.basename(__file__):
                continue  # 這個 script 自己不掃（它的 pattern 文字會被自己抓到）；用檔名比，從別處跑也一樣
            for ln in open(fp, encoding="utf-8", errors="replace"):
                ln = COMMENT.sub("", ln)
                for tok in EXTERNAL.findall(ln):
                    tok = tok.rstrip(";")
                    if fn in SETUP_FILES:
                        in_setup.append(f"{fn}: {tok}")
                    else:
                        print(f"  EXTERNAL {fn}: {tok}")
                        infos.append(f"{fn}: {tok}")
    if not infos:
        print("  無")
    if in_setup:
        print(f"  （集中在 setup.* 的 {len(in_setup)} 處不算：" + "；".join(in_setup) + "）")

    print("== 4. rtl/ 裡存在但 filelist 沒引用的檔（只列，不算 FAIL）")
    rtl = os.path.join(root, "rtl")
    unref = [os.path.join("rtl", fn) for fn in sorted(os.listdir(rtl))] if os.path.isdir(rtl) else []
    unref = [r for r in unref if r not in referenced]
    for r in unref:
        print(f"  UNREF    {r}")
    if not unref:
        print("  無")

    verdict = "FAIL" if fails else "PASS"
    print(f"== 結果：{verdict}" + (f"（{len(fails)} 項）" if fails else "") +
          f"；外部相依 {len(infos)} 處；未引用 {len(unref)} 檔")
    for f in fails:
        print(f"  - {f}")

    if a.manifest:
        os.makedirs(os.path.dirname(os.path.abspath(a.manifest)) or ".", exist_ok=True)
        with open(a.manifest, "w", encoding="utf-8") as mf:
            mf.write("schema: manifest/1\n")
            mf.write(f"結果: dma filelist 一致性 {verdict}\n")
            mf.write(f"產生時間: {time.strftime('%Y-%m-%dT%H:%M')}\n")
            mf.write(f"CL: {a.cl}\n")
            mf.write(f"工具: python {platform.python_version()}\n")
            mf.write(f"環境: host {platform.node()}; {platform.system()} {platform.release()}\n")
            mf.write(f"指令: {' '.join(sys.argv)}\n")
            mf.write("輸入指紋（sha256 前 16 碼）:\n")
            for fp in fingerprints:
                mf.write(f"  {fp}\n")
            mf.write(f"結果摘要: {verdict}；缺檔／重複 {len(fails)}；外部相依 {len(infos)}；未引用 {len(unref)}\n")
            for f in fails:
                mf.write(f"  - {f}\n")
            mf.write("產生者: scripts/check_filelist.py (agent-dma v0.1.0)\n")
        print(f"manifest: {a.manifest}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

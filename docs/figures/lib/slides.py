# -*- coding: utf-8 -*-
# 投影片式文件的共用工具：SVG 畫圖小函式、HTML 外殼、轉 PDF 與逐頁 PNG。
# 一頁一張圖、一行標題、A4 橫式。規則見 docs/slide-doc-rules.md。
# 不載入任何外部字型或 CDN：HTML 要能在沒有外網的內網直接打開。
import html, pathlib, shutil, subprocess, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 顏色分工（同一份文件裡不換義）
WARN = "var(--warn)"     # 現狀的問題、限制、缺口
GOAL = "var(--goal)"     # CI/CD、目標狀態
AGENT = "var(--agent)"   # AI agent
PM = "var(--pm)"         # 人類 PM
INK2, GRAY = "var(--ink-2)", "var(--ink-3)"

CSS = """
:root{--paper:#fff;--surface:#fff;--surface-2:#eef2f5;--ink:#17212b;--ink-2:#48596a;--ink-3:#78889a;--rule:#cfd9e1;--rule-2:#aebbc7;
--goal:#116b64;--warn:#a0580f;--agent:#2f6f9f;--pm:#7a4f9a;
--mono:"SF Mono",Menlo,Consolas,"PingFang TC","Noto Sans TC","Microsoft JhengHei",monospace;
--sans:"Helvetica Neue",Arial,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif}
html,body{margin:0;padding:0;background:#fff;color:var(--ink);font-family:var(--sans)}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
@page{size:A4 landscape;margin:0}
.slide{width:297mm;height:210mm;box-sizing:border-box;padding:11mm 14mm 9mm;display:flex;flex-direction:column;break-after:page;page-break-after:always;overflow:hidden;position:relative}
.slide:last-child{break-after:auto;page-break-after:auto}
@media screen{body{background:#e6ebef}.slide{background:#fff;margin:8mm auto;box-shadow:0 1px 4px rgba(0,0,0,.12)}}
.kicker{font-family:var(--mono);font-size:9.5pt;letter-spacing:.06em;color:var(--ink-3);margin:0 0 2mm}
.slide h1{font-family:var(--sans);font-size:20pt;font-weight:600;margin:0 0 5mm;line-height:1.25}
.fig{flex:1;min-height:0;display:flex;align-items:center;justify-content:center}
.fig svg{display:block;color:var(--ink)}
.pn{position:absolute;right:14mm;bottom:6mm;font-family:var(--mono);font-size:8.5pt;color:var(--ink-3)}
.tx{font-family:var(--mono);font-size:12px;fill:currentColor}
.tx-s{font-family:var(--mono);font-size:10.5px;fill:var(--ink-3)}
.tx-b{font-family:var(--sans);font-size:15px;font-weight:700;fill:currentColor}
.tx-lbl{font-family:var(--mono);font-size:11px;font-weight:500;letter-spacing:.06em;fill:var(--ink-3)}
"""

AR = ('<defs><marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
      '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>')
MARKERS = [("ar", "currentColor"), ("ar-w", WARN), ("ar-g", GOAL), ("ar-a", AGENT), ("ar-p", PM), ("ar-gray", "var(--ink-3)")]

esc = html.escape


def width(text, size=12):
    """估字寬：中文約 0.97 倍字級，英數約 0.6 倍（mono）。"""
    w = 0.0
    for ch in text:
        w += size * (0.97 if ord(ch) > 0x2E80 else 0.6)
    return w


def T(s, x, y, text, cls="tx-s", anchor="start", fill=None, w=None, size=None):
    st = []
    if w:
        st.append("font-weight:%s" % w)
    if size:
        st.append("font-size:%spx" % size)
    s.append('<text class="%s" x="%.1f" y="%.1f" text-anchor="%s"%s%s>%s</text>' % (
        cls, x, y, anchor, ' fill="%s"' % fill if fill else "", ' style="%s"' % ";".join(st) if st else "", esc(text)))


def rect(s, x, y, w, h, col="currentColor", fill="var(--surface)", sw=1.4, dash=None, op=None, rx=0):
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"%s fill="%s" stroke="%s" stroke-width="%s"%s%s/>' % (
        x, y, w, h, ' rx="%d"' % rx if rx else "", fill, col, sw,
        ' stroke-dasharray="%s"' % dash if dash else "", ' fill-opacity="%s"' % op if op else ""))


def line(s, x1, y1, x2, y2, col="var(--rule)", sw=1, dash=None):
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (
        x1, y1, x2, y2, col, sw, ' stroke-dasharray="%s"' % dash if dash else ""))


def arrow(s, x1, y1, x2, y2, col="currentColor", ar="ar", dash=None, sw=1.4):
    s.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s marker-end="url(#%s)"/>' % (
        x1, y1, x2, y2, col, sw, ' stroke-dasharray="%s"' % dash if dash else "", ar))


def path(s, d, col="currentColor", ar="ar", sw=1.4, dash=None):
    s.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s%s/>' % (
        d, col, sw, ' stroke-dasharray="%s"' % dash if dash else "", ' marker-end="url(#%s)"' % ar if ar else ""))


def pill(s, x, y, text, col, h=20, anchor="start"):
    """膠囊：寬度照字數算。回傳寬度。"""
    w = width(text, 10.5) + 20
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    rect(s, x, y, w, h, col=col, fill=col, op=".14", sw=1, rx=h // 2)
    T(s, x + w / 2, y + h - 6, text, anchor="middle", fill=col, w=700)
    return w


def svg(body, w, h, aria, mm_w=269.0):
    mm_h = mm_w * h / w
    defs = "".join(AR % m for m in MARKERS)
    return ('<svg style="width:%.1fmm;height:%.1fmm" viewBox="0 0 %d %d" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">\n%s\n%s\n</svg>'
            % (mm_w, mm_h, w, h, esc(aria), defs, "\n".join(body)))


def build(name, doc_title, kicker, pages):
    """pages: [(標題, svg 字串)]。輸出 docs/slides/<name>.html 與 .pdf，逐頁 PNG 放 build/pages/<name>/。"""
    n = len(pages)
    secs = []
    for i, (title, fig) in enumerate(pages, 1):
        secs.append('<section class="slide"><div class="kicker">%s　·　圖 %d ／ %d</div><h1>%s</h1>'
                    '<div class="fig">%s</div><div class="pn">%d / %d</div></section>' % (esc(kicker), i, n, esc(title), fig, i, n))
    doc = ('<!doctype html>\n<html lang="zh-Hant" data-theme="light">\n<head>\n<meta charset="utf-8">\n<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n%s\n</body>\n</html>\n'
           % (esc(doc_title), CSS, "\n".join(secs)))
    out = ROOT / "docs/slides"
    out.mkdir(parents=True, exist_ok=True)
    h = out / (name + ".html")
    h.write_text(doc, encoding="utf-8")
    pdf = out / (name + ".pdf")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=%s" % pdf, h.as_uri()], check=True, capture_output=True)
    # 逐頁 PNG 進版控：GitHub 的 README 不能嵌 PDF，只能嵌圖片；也拿來逐頁檢查排版
    png_dir = out / "img" / name
    shutil.rmtree(png_dir, ignore_errors=True)
    png_dir.mkdir(parents=True)
    subprocess.run(["pdftoppm", "-png", "-r", "110", str(pdf), str(png_dir / "p")], check=True)
    print(h.relative_to(ROOT), pdf.relative_to(ROOT), png_dir.relative_to(ROOT), sep="\n")

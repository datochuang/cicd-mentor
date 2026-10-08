#!/bin/sh
# 把 docs/*.html 轉成同名 PDF。HTML 刻意不含 <html>/<head>（Artifact 發佈時會自動包上），
# 這裡先補上 doctype 與 charset 再交給 headless Chrome 列印。
# 用法：sh docs/build-pdf.sh [docs/xxx.html ...]（不帶參數則處理 docs/ 下全部 HTML）
set -e
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
[ $# -eq 0 ] && set -- docs/*.html
for src in "$@"; do
  out="${src%.html}.pdf"
  { printf '<!doctype html>\n<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
    cat "$src"
    printf '\n</html>\n'; } > "$TMP/print.html"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$out" "file://$TMP/print.html" >/dev/null 2>&1
  echo "$out"
done

#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${OUT_DIR:-$HOME/lawfullyillegal-droid/staging/title47}"
mkdir -p "$OUT_DIR"

AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36'

dorks=(
  'site:.gov "Title 47" "Code of Federal Regulations" filetype:pdf'
  '"Title 47" "CFR" "Federal Communications Commission" filetype:pdf'
  '"47 CFR" "Title 47" filetype:pdf'
  'site:ntrs.nasa.gov "Title 47" "FCC" filetype:pdf'
  '"Title 47 U.S.C." "Communications Act" filetype:pdf'
)

i=0
for d in "${dorks[@]}"; do
  i=$((i+1))
  q="$(printf '%s' "$d" | sed 's/ /+/g')"
  url="https://www.google.com/search?q=${q}"
  html="${OUT_DIR}/google_${i}.html"

  curl -A "$AGENT" -L --silent "$url" -o "$html"

  grep -oP 'https?://[^&]+' "$html" \
    | grep -i '\.pdf' \
    | sed 's/%3F/?/g; s/%3D/=/g' \
    | sort -u > "${OUT_DIR}/urls_${i}.txt"

  while read -r pdf; do
    [ -z "$pdf" ] && continue
    fname="$(echo "$pdf" | sed 's#[/:?&=]#_#g').pdf"
    [ -f "${OUT_DIR}/${fname}" ] && continue
    curl -A "$AGENT" -L --silent "$pdf" -o "${OUT_DIR}/${fname}" || true
  done < "${OUT_DIR}/urls_${i}.txt"
done

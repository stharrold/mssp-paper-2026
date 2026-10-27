#!/usr/bin/env bash
# Build the manuscript and supplement from Markdown: PDF (Eisvogel + tectonic or xelatex) and DOCX.
#
# Usage:
#   scripts/build.sh            # tables, figures, then paper.pdf, paper.docx, supplement.pdf, supplement.docx
#   scripts/build.sh pdf        # PDFs only
#   scripts/build.sh docx       # DOCX only
#
# Requires pandoc 3.x and tectonic (brew install pandoc tectonic) or a TeX installation with xelatex, and uv.
# Adapted from stharrold/yuimedi-paper-20250901 scripts/build_paper.sh.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
FORMAT="${1:-all}"

EISVOGEL_VERSION="3.3.0"
EISVOGEL_URL="https://github.com/Wandmalfarbe/pandoc-latex-template/releases/download/v${EISVOGEL_VERSION}/Eisvogel-${EISVOGEL_VERSION}.tar.gz"
EISVOGEL_SHA256="0eb287d299e73aa884d0b35fa27a28ae326afa04f51959e54f01cbbe76601489"
TEMPLATE_DIR="${HOME}/.local/share/pandoc/templates"

install_eisvogel() {
  [[ -f "$TEMPLATE_DIR/eisvogel.latex" ]] && return 0
  echo "Installing Eisvogel ${EISVOGEL_VERSION}"
  mkdir -p "$TEMPLATE_DIR"
  local tmp
  tmp="$(mktemp)"
  curl -fsSL "$EISVOGEL_URL" -o "$tmp"
  echo "${EISVOGEL_SHA256}  ${tmp}" | shasum -a 256 -c - >/dev/null
  tar xzf "$tmp" -C "$TEMPLATE_DIR" --strip-components=1
  rm -f "$tmp"
}

pdf_engine() {
  if command -v xelatex >/dev/null; then echo xelatex
  elif command -v tectonic >/dev/null; then echo tectonic
  else echo "No PDF engine: brew install tectonic" >&2; exit 1
  fi
}

common=(--from=markdown+smart --metadata-file=metadata.yaml --lua-filter=scripts/include.lua
        --citeproc --bibliography=references/doi.json --bibliography=references/other.bib --resource-path=.)

uv run python scripts/make_tables.py
uv run python scripts/make_figures.py

for doc in paper supplement; do
  if [[ "$FORMAT" == all || "$FORMAT" == pdf ]]; then
    install_eisvogel
    pandoc "$doc.md" "${common[@]}" --template=eisvogel --pdf-engine="$(pdf_engine)" -o "$doc.pdf"
    echo "wrote $doc.pdf"
  fi
  if [[ "$FORMAT" == all || "$FORMAT" == docx ]]; then
    pandoc "$doc.md" "${common[@]}" --reference-doc=reference.docx -o "$doc.docx"
    echo "wrote $doc.docx"
  fi
done

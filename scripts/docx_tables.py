"""Widen the tables in pandoc's DOCX output to the full text width.

pandoc's DOCX writer sizes every table grid to a 5.5 in text width (7,920 twips) whatever the reference document's
page setup, so with reference.docx's Letter page and 1 in margins (6.5 in) tables filled only 85% of the line and
narrow columns broke short values such as "<.001". This rescales each table's grid columns, keeping the proportions
set by scripts/include.lua, so they sum to the text width. Standard library only.

Usage: python3 scripts/docx_tables.py paper.docx [supplement.docx ...]
"""

import re
import sys
import zipfile
from pathlib import Path

TEXT_WIDTH = 9360  # twips: 8.5 in page - 2 x 1 in margins


def widen(xml: str) -> tuple[str, int]:
    count = 0

    def grid(match: re.Match) -> str:
        nonlocal count
        cols = [int(w) for w in re.findall(r'w:w="(\d+)"', match.group(1))]
        total = sum(cols)
        if not total:
            return match.group(0)
        count += 1
        scaled = [round(w * TEXT_WIDTH / total) for w in cols]
        scaled[-1] += TEXT_WIDTH - sum(scaled)
        return "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}" />' for w in scaled) + "</w:tblGrid>"

    return re.sub(r"<w:tblGrid>(.*?)</w:tblGrid>", grid, xml, flags=re.S), count


def main() -> None:
    for name in sys.argv[1:]:
        path = Path(name)
        with zipfile.ZipFile(path) as z:
            items = [(info, z.read(info.filename)) for info in z.infolist()]
        out = path.with_suffix(".tmp")
        tables = 0
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for info, data in items:
                if info.filename == "word/document.xml":
                    xml, tables = widen(data.decode("utf-8"))
                    data = xml.encode("utf-8")
                z.writestr(info, data)
        out.replace(path)
        print(f"{name}: {tables} tables widened to {TEXT_WIDTH} twips")


if __name__ == "__main__":
    main()

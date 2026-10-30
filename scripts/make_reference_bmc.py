"""Derive reference-bmc.docx from reference.docx: BMC Health Services Research wants double line spacing, line numbers
and page numbers (standards/bmc-hsr/SOURCES.md). reference.docx already double-spaces body text (Normal, which Body
Text inherits) and keeps table cells single-spaced at 10 pt (Compact). Pandoc takes the section properties and their
footer from the reference document, so this adds continuous line numbering to the section and a centred PAGE field
in a new footer.

Usage: uv run python scripts/make_reference_bmc.py
"""

import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, DST = ROOT / "reference.docx", ROOT / "reference-bmc.docx"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
FOOTER = (
    f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:ftr xmlns:w="{W}" xmlns:r="{R}">'
    '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
    '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
    '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>'
    "</w:p></w:ftr>"
)


def section(xml: str) -> str:
    """Continuous line numbers and the page-number footer in the (only) section."""
    sect = re.search(r"<w:sectPr>.*?</w:sectPr>", xml, re.S).group(0)
    new = sect.replace("<w:sectPr>", '<w:sectPr><w:footerReference w:type="default" r:id="rIdBmcFooter"/>', 1)
    new = new.replace("<w:pgMar", '<w:lnNumType w:countBy="1" w:restart="continuous"/><w:pgMar', 1)
    if 'xmlns:r="' not in xml[:2000]:
        xml = xml.replace("<w:document ", f'<w:document xmlns:r="{R}" ', 1)
    return xml.replace(sect, new)


with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zout:
    for info in zin.infolist():
        data = zin.read(info)
        if info.filename == "word/document.xml":
            data = section(data.decode()).encode()
        elif info.filename == "word/_rels/document.xml.rels":
            rel = f'<Relationship Id="rIdBmcFooter" Type="{R}/footer" Target="footer1.xml"/>'
            data = data.decode().replace("</Relationships>", rel + "</Relationships>").encode()
        elif info.filename == "[Content_Types].xml":
            ct = '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
            data = data.decode().replace("</Types>", ct + "</Types>").encode()
        zout.writestr(info, data)
    # a fixed timestamp, so rebuilding gives the same bytes
    zout.writestr(zipfile.ZipInfo("word/footer1.xml", date_time=(2026, 10, 29, 0, 0, 0)), FOOTER, zipfile.ZIP_DEFLATED)
print(f"wrote {DST.name}")

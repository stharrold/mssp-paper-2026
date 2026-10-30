#!/usr/bin/env python3
"""Check paper.md against BMC Health Services Research's research-article rules (standards/bmc-hsr/SOURCES.md).

Checks:
- Abstract: sections Background, Methods, Results, Conclusions, Trial registration, in that order; at most 350 words
  (section labels included); no citations
- Keywords: 3 to 10, after the abstract
- Top-level sections in order: Abstract, Background, Methods, Results, Discussion, Conclusions, List of abbreviations,
  Declarations, then Additional files (if any) and References
- Declarations: the 7 required subheadings in order (Authors' information optional, last)
- Large language model use documented in Methods
- No web links in the text from Background to Conclusions (URLs belong in the reference list)
- Figure and table titles (first sentence of the caption) at most 15 words; figures and additional files numbered in
  order of first mention; every additional file cited in the text is listed under "Additional files"
- No "Multimedia Appendix" left over from the JMIR version; the BMC reference style in metadata.yaml
- If paper.docx exists: line numbering and a footer (page numbers) in its section properties

Usage: uv run python scripts/validate_bmc_compliance.py [paper.md]
"""

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ABSTRACT_SECTIONS = ["Background", "Methods", "Results", "Conclusions", "Trial registration"]
ABSTRACT_MAX = 350
TOP_SECTIONS = ["Abstract", "Background", "Methods", "Results", "Discussion", "Conclusions", "List of abbreviations", "Declarations"]
DECLARATIONS = [
    "Ethics approval and consent to participate",
    "Consent for publication",
    "Availability of data and materials",
    "Competing interests",
    "Funding",
    "Authors' contributions",
    "Acknowledgements",
]
TITLE_MAX = 15


def section(text: str, name: str) -> str:
    """The body of the top-level section `# name`, up to the next top-level heading."""
    m = re.search(rf"^# {re.escape(name)}\n(.*?)(?=^# |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def check_abstract(text: str) -> list[str]:
    problems = []
    body = section(text, "Abstract")
    body = body.split("**Keywords:**")[0]
    labels = re.findall(r"\*\*([^*]+):\*\*", body)
    if labels != ABSTRACT_SECTIONS:
        problems.append(f"abstract sections are {labels}, expected {ABSTRACT_SECTIONS}")
    words = len(body.split())
    if words > ABSTRACT_MAX:
        problems.append(f"abstract has {words} words (at most {ABSTRACT_MAX})")
    if "[@" in body:
        problems.append("abstract cites references")
    return problems


def check_keywords(text: str) -> list[str]:
    m = re.search(r"\*\*Keywords:\*\*(.*?)(?:\n\n|\Z)", text, re.S)
    if not m:
        return ["no **Keywords:** line"]
    if text.index("**Keywords:**") < text.index("# Abstract"):
        return ["keywords come before the abstract"]
    n = len([k for k in m.group(1).split(";") if k.strip()])
    return [] if 3 <= n <= 10 else [f"{n} keywords (3 to 10)"]


def check_sections(text: str) -> list[str]:
    problems = []
    tops = [h for h in re.findall(r"^# (.+)$", text, re.M)]
    expected = TOP_SECTIONS + (["Additional files"] if "Additional files" in tops else []) + ["References"]
    if tops != expected:
        problems.append(f"top-level sections are {tops}, expected {expected}")
    subs = re.findall(r"^## (.+)$", section(text, "Declarations"), re.M)
    if subs[: len(DECLARATIONS)] != DECLARATIONS or subs[len(DECLARATIONS) :] not in ([], ["Authors' information"]):
        problems.append(f"Declarations subheadings are {subs}, expected {DECLARATIONS} (+ optional Authors' information)")
    if not re.search(r"^## .*(Large Language Model|Artificial Intelligence)", section(text, "Methods"), re.M | re.I):
        problems.append("Methods has no subsection documenting large language model use")
    return problems


def check_links(text: str) -> list[str]:
    start = text.find("\n# ", text.find("# Abstract") + 1)  # the first section after the abstract
    end = text.find("# List of abbreviations")
    body = text[start:end] if 0 <= start < end else text[start:]
    body = re.sub(r"\[@[^\]]*\]", "", body)
    links = re.findall(r"https?://[^\s)]+|www\.[^\s)]+", body)  # local figure paths are not links
    return [f"web link in the text (cite it as a reference): {link[:60]}" for link in links]


def first_sentence_words(caption: str) -> int:
    title = re.split(r"(?<=[.?])\s", caption.strip(), maxsplit=1)[0]
    return len(title.split())


def check_figures_tables(text: str, root: Path) -> list[str]:
    problems = []
    figures = re.findall(r"!\[Figure (\d+)\. ([^\]]*)\]", text)
    for n, cap in figures:
        if first_sentence_words(cap) > TITLE_MAX:
            problems.append(f"Figure {n} title is over {TITLE_MAX} words")
    included = "\n".join((root / f).read_text() for f in re.findall(r"\{\{include (\S+)\}\}", text) if (root / f).is_file())
    for n, cap in re.findall(r"^: Table (\d+)\. (.+)$", included + "\n" + text, re.M):
        if first_sentence_words(cap) > TITLE_MAX:
            problems.append(f"Table {n} title is over {TITLE_MAX} words")
    body = re.sub(r"!\[Figure \d+\.[^\]]*\]", "", text)
    order = list(dict.fromkeys(int(n) for n in re.findall(r"\bFigures? (\d+)", body)))
    if order != sorted(order):
        problems.append(f"figures first cited in the order {order}")
    files_section = section(text, "Additional files")
    cited = list(dict.fromkeys(int(n) for n in re.findall(r"Additional file (\d+)", text.replace(files_section, ""))))
    if cited != sorted(cited) or cited != list(range(1, len(cited) + 1)):
        problems.append(f"additional files first cited in the order {cited}")
    listed = [int(n) for n in re.findall(r"\*\*Additional file (\d+)\*\*", files_section)]
    if listed != list(range(1, len(cited) + 1)):
        problems.append(f"Additional files section lists {listed}, text cites {cited}")
    if "Multimedia Appendix" in text:
        problems.append('"Multimedia Appendix" left in the text (BMC: "Additional file")')
    return problems


def check_metadata(root: Path) -> list[str]:
    meta = (root / "metadata.yaml").read_text()
    return [] if re.search(r"^csl: citation-style-bmc\.csl", meta, re.M) else ["metadata.yaml does not use citation-style-bmc.csl"]


def check_docx(path: Path) -> list[str]:
    if not path.is_file():
        return []
    xml = zipfile.ZipFile(path).read("word/document.xml").decode()
    sect = re.findall(r"<w:sectPr>.*?</w:sectPr>", xml, re.S)
    problems = []
    if not sect or "<w:lnNumType" not in sect[-1]:
        problems.append(f"{path.name}: no line numbering (rebuild with reference-bmc.docx)")
    if not sect or "<w:footerReference" not in sect[-1]:
        problems.append(f"{path.name}: no footer with page numbers")
    return problems


def validate(text: str, root: Path = ROOT, docx: Path | None = None) -> list[str]:
    return [
        *check_abstract(text),
        *check_keywords(text),
        *check_sections(text),
        *check_links(text),
        *check_figures_tables(text, root),
        *check_metadata(root),
        *(check_docx(docx) if docx else []),
    ]


def main() -> int:
    paper = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "paper.md"
    text = paper.read_text()
    problems = validate(text, paper.parent, paper.with_suffix(".docx"))
    abstract = section(text, "Abstract").split("**Keywords:**")[0]
    print(f"abstract {len(abstract.split())}/{ABSTRACT_MAX} words")
    for p in problems:
        print(f"FAIL: {p}")
    print("BMC Health Services Research checks passed" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

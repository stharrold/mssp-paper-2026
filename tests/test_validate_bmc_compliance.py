"""BMC Health Services Research checks (scripts/validate_bmc_compliance.py): on small synthetic manuscripts, then on paper.md."""

from pathlib import Path

import validate_bmc_compliance as v

ROOT = Path(__file__).resolve().parent.parent

GOOD = """::: {.author-block}
A. Author, [orcid](https://orcid.org/0000-0000-0000-0000)
:::

# Abstract

**Background:** Why. **Methods:** How. **Results:** What. **Conclusions:** So. **Trial registration:** OSF, 26 October 2026.

**Keywords:** one; two; three

# Background

Text citing a source.[@x] See Figure 1 and the checklist (Additional file 1), then eTables (Additional file 2).

![Figure 1. A short title. A legend.](figures/f.png)

# Methods

## Use of Large Language Models

Documented.

# Results

Figure 2 follows.

![Figure 2. Another short title.](figures/g.png)

# Discussion

Limits.

# Conclusions

Done.

# List of abbreviations

X: x

# Declarations

## Ethics approval and consent to participate

Not applicable.

## Consent for publication

Not applicable.

## Availability of data and materials

Zenodo.

## Competing interests

None.

## Funding

None.

## Authors' contributions

AA.

## Acknowledgements

Not applicable.

# Additional files

**Additional file 1** (.docx). Checklist.

**Additional file 2** (.docx). eTables.

# References
"""


def problems(text: str) -> list[str]:
    return v.validate(text, ROOT)


def test_a_complete_manuscript_passes():
    assert problems(GOOD) == []


def test_abstract_sections_order_and_length():
    assert any("abstract sections" in p for p in problems(GOOD.replace("**Methods:** How. ", "")))
    long = GOOD.replace("**Results:** What.", "**Results:** " + "word " * 360)
    assert any("words (at most 350)" in p for p in problems(long))
    assert any("cites references" in p for p in problems(GOOD.replace("**Results:** What.", "**Results:** What.[@x]")))


def test_keywords_count():
    assert any("keywords" in p for p in problems(GOOD.replace("one; two; three", "one; two")))


def test_sections_and_declarations():
    assert any("top-level sections" in p for p in problems(GOOD.replace("# Background\n", "# Introduction\n")))
    assert any("Declarations subheadings" in p for p in problems(GOOD.replace("## Consent for publication\n\nNot applicable.\n\n", "")))
    assert any("large language model" in p for p in problems(GOOD.replace("## Use of Large Language Models", "## Tools")))


def test_web_links_belong_in_references():
    assert any("web link" in p for p in problems(GOOD.replace("Text citing a source.", "See https://example.org for it.")))


def test_additional_files_follow_first_citation():
    swapped = GOOD.replace("(Additional file 1), then eTables (Additional file 2)", "(Additional file 2), then eTables (Additional file 1)")
    assert any("additional files first cited" in p for p in problems(swapped))
    assert any("Multimedia Appendix" in p for p in problems(GOOD.replace("Limits.", "See Multimedia Appendix 1.")))


def test_figure_titles_and_order():
    long_title = GOOD.replace("Figure 1. A short title.", "Figure 1. " + "word " * 16 + ".")
    assert any("Figure 1 title" in p for p in problems(long_title))
    assert any("figures first cited" in p for p in problems(GOOD.replace("See Figure 1 and", "See Figure 2 and Figure 1 and")))


def test_commas_in_table_numbers(tmp_path):
    (tmp_path / "t.md").write_text("| n |\n|---|\n| 10,000 |\n")
    assert any("comma" in p for p in v.check_figures_tables("{{include t.md}}\n", tmp_path))
    (tmp_path / "t.md").write_text("| n |\n|---|\n| 10000 |\n")
    assert not any("comma" in p for p in v.check_figures_tables("{{include t.md}}\n", tmp_path))


def test_the_paper_meets_the_checks():
    text = (ROOT / "paper.md").read_text()
    docx = ROOT / "paper.docx"
    assert v.validate(text, ROOT, docx) == []

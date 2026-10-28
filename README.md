# Early renewal in the Medicare Shared Savings Program: preregistered retrospective cohort study

Manuscript and multimedia appendices for the preregistered study of early renewal in the Medicare Shared Savings
Program. Version 1 was posted to medRxiv in a journal-agnostic format (tag `medrxiv-v1`); the current source is
formatted as a JMIR Original Paper for the *Interactive Journal of Medical Research* (i-JMR): JMIR's structured
abstract, IMRD headings, JMIR end sections, the supplement as Multimedia Appendix 1 and the STROBE checklist as
Multimedia Appendix 2.

- **Registration:** OSF Registries, [doi:10.17605/OSF.IO/C53W9](https://doi.org/10.17605/OSF.IO/C53W9)
- **Analysis code and data snapshot:** [stharrold/stharrold.github.io, `analysis/mssp-benchmark-ratchet/`](https://github.com/stharrold/stharrold.github.io/tree/src_master/analysis/mssp-benchmark-ratchet)
  and the OSF project [doi:10.17605/OSF.IO/Z4AN5](https://doi.org/10.17605/OSF.IO/Z4AN5)
- **Post for a general audience:** [stharrold.github.io](https://stharrold.github.io/20261027-preregistered-mssp-early-renewal.html)

## Status

| Where | Version | Submitted | ID | Files (sha256) | Source |
|---|---|---|---|---|---|
| medRxiv | 1 | 2026-10-27 | MEDRXIV/2026/366643 (in screening) | `paper.pdf` 7d111cbdef3672f2..., `supplement.pdf` d65212577e6d9809... | `dcbad91` (tag `medrxiv-v1`) |
| i-JMR | 1 | not yet | | `paper.docx`, `supplement.docx`, `strobe.docx` | `main` (release v1.1.0) |

A medRxiv version 2 is planned after outside review; medRxiv keeps earlier versions visible. Both forms' text fields
are entered as plain ASCII. The i-JMR package and its checklist are in [`submission/ijmr/`](submission/ijmr/README.md).

The JMIR version differs from medRxiv version 1 in form, not in results: the title (JMIR asks for a descriptive title
naming the design and without abbreviations), the abstract headings, an "Ethical Considerations" section citing 45
CFR 46.102, the end sections, no bold for emphasis, *P* values without spaces, URLs moved into the references, and
the generative AI statement moved from the manuscript to JMIR's submission form, as JMIR's October 2026 policy
requires. Every number is unchanged, and `scripts/check_numbers.py` checks them against the results.

## Files

| Path | What it is |
|---|---|
| `paper.md`, `supplement.md`, `strobe.md` | The manuscript, Multimedia Appendix 1 (eTables, eMethods) and Multimedia Appendix 2 (STROBE checklist) |
| `paper.docx`, `supplement.docx`, `strobe.docx` and the PDFs | Built outputs |
| `data/` | The committed results files, copied unchanged with their hashes ([`data/README.md`](data/README.md)) |
| `tables/`, `figures/` | Generated from `data/` by `scripts/make_tables.py` and `scripts/make_figures.py`; never edited by hand |
| `references/doi.json` | Metadata of every DOI-cited reference, fetched from Crossref by `scripts/fetch_references.py` |
| `references/other.bib` | References without a DOI (regulations, CMS datasets, software) |
| `research/` | The PubMed literature search: script, queries, records and abstracts |
| `scripts/check_numbers.py` | Checks every number and interval in the prose against the results |
| `scripts/validate_jmir_compliance.py` | JMIR checks (abstract, keywords, IMRD, end sections, AI statement placement, abbreviations, word count); adapted from yuimedi-paper-20250901 |
| `scripts/form_fields.py` | Writes the JMIR form's plain-text fields, figure uploads and captions into `submission/ijmr/` |
| `standards/jmir/SOURCES.md` | The JMIR author-guidance articles followed (local copies are not in git) |
| `submission/ijmr/` | The i-JMR package: cover letter, AI disclosure, suggested reviewers, figure uploads, checklist |
| `posthoc/` | Byte-identical copies of the study's 2 post hoc scripts (not registered), with their source commits |
| `CITATION.cff`, `.zenodo.json` | Citation metadata; Zenodo archives each GitHub release |

## Archive

Each GitHub release of this repository is archived on Zenodo: [doi:10.5281/zenodo.23737045](https://doi.org/10.5281/zenodo.23737045)
(concept DOI, resolving to the latest version; cite this one). The registered analysis plan and code are archived on
OSF Registries ([doi:10.17605/OSF.IO/C53W9](https://doi.org/10.17605/OSF.IO/C53W9)), and the data snapshot and
results notebook in the OSF project ([doi:10.17605/OSF.IO/Z4AN5](https://doi.org/10.17605/OSF.IO/Z4AN5)).

## Build

Requires [uv](https://docs.astral.sh/uv/), pandoc 3 and tectonic (`brew install pandoc tectonic`) or a TeX
installation with xelatex. The build installs the Eisvogel 3.3.0 template on first run (checksum-verified).

```bash
uv sync
scripts/build.sh          # tables, figures, PDFs and DOCX
uv run pytest             # data hashes, tables current, citations defined, prose numbers, JMIR checks
python3 scripts/check_numbers.py
uv run python scripts/validate_jmir_compliance.py --article-type original
uv run python scripts/form_fields.py
```

The build and its tooling are adapted from
[stharrold/yuimedi-paper-20250901](https://github.com/stharrold/yuimedi-paper-20250901) (`scripts/build_paper.sh`,
the AMA CSL style, `reference.docx`, the JMIR validator and the JMIR guidance in `standards/jmir/`).

## Before submitting

1. `uv run pytest` and `python3 scripts/check_numbers.py` pass; `scripts/build.sh` rebuilt the PDFs and DOCX files.
2. Read the manuscript in full, including both appendices.
3. i-JMR: follow [`submission/ijmr/README.md`](submission/ijmr/README.md). medRxiv (a later version): subject area
   Health Policy; license CC BY 4.0; upload the PDFs; declarations to match the manuscript.

## License

The manuscript, supplement, tables and figures are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The scripts are under the MIT license (`LICENSE`).

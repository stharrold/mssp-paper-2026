# Why did Medicare ACOs reset their benchmarks early? (preprint)

Manuscript and supplement for the pre-registered study of early renewal in the Medicare Shared Savings Program,
prepared for medRxiv (journal-agnostic: IMRaD, structured abstract, AMA references, STROBE checklist).

- **Registration:** OSF Registries, [doi:10.17605/OSF.IO/C53W9](https://doi.org/10.17605/OSF.IO/C53W9)
- **Analysis code and data snapshot:** [stharrold/stharrold.github.io, `analysis/mssp-benchmark-ratchet/`](https://github.com/stharrold/stharrold.github.io/tree/src_master/analysis/mssp-benchmark-ratchet)
  and the OSF project [doi:10.17605/OSF.IO/Z4AN5](https://doi.org/10.17605/OSF.IO/Z4AN5)
- **Post for a general audience:** [stharrold.github.io](https://stharrold.github.io/20261027-preregistered-mssp-early-renewal.html)

## Files

| Path | What it is |
|---|---|
| `paper.md`, `supplement.md` | The manuscript and Supplement 1 (Markdown, pandoc citations) |
| `paper.pdf`, `paper.docx`, `supplement.pdf`, `supplement.docx` | Built outputs |
| `data/` | The committed results files, copied unchanged with their hashes ([`data/README.md`](data/README.md)) |
| `tables/`, `figures/` | Generated from `data/` by `scripts/make_tables.py` and `scripts/make_figures.py`; never edited by hand |
| `references/doi.json` | Metadata of every DOI-cited reference, fetched from Crossref by `scripts/fetch_references.py` |
| `references/other.bib` | References without a DOI (regulations, CMS datasets, software) |
| `research/` | The PubMed literature search: script, queries, records and abstracts |
| `scripts/check_numbers.py` | Checks every number and interval in the prose against the results |

## Build

Requires [uv](https://docs.astral.sh/uv/), pandoc 3 and tectonic (`brew install pandoc tectonic`) or a TeX
installation with xelatex. The build installs the Eisvogel 3.3.0 template on first run (checksum-verified).

```bash
uv sync
scripts/build.sh          # tables, figures, PDFs and DOCX
uv run pytest             # data hashes, tables current, citations defined, prose numbers
python3 scripts/check_numbers.py
```

The build and its tooling are adapted from
[stharrold/yuimedi-paper-20250901](https://github.com/stharrold/yuimedi-paper-20250901) (`scripts/build_paper.sh`,
the AMA CSL style and `reference.docx`).

## Before submitting

1. `uv run pytest` and `python3 scripts/check_numbers.py` pass; `scripts/build.sh` rebuilt the PDFs.
2. Read the PDF in full, including the supplement.
3. On medRxiv: subject area Health Policy; license CC BY 4.0; upload `paper.pdf` and
   `supplement.pdf`; complete the declarations (ethics, funding, competing interests, data availability,
   preregistration DOI) to match the manuscript.

## License

The manuscript, supplement, tables and figures are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The scripts are under the MIT license (`LICENSE`).

# Early renewal in the Medicare Shared Savings Program: preregistered retrospective cohort study

Manuscript and multimedia appendices for the preregistered study of early renewal in the Medicare Shared Savings
Program. A first version was submitted to medRxiv in a journal-agnostic format (tag `medrxiv-v1`), which declined it
because medRxiv requires an organizational affiliation; it was never posted. The current source is
formatted as a JMIR Original Paper for the *Interactive Journal of Medical Research* (i-JMR): JMIR's structured
abstract, IMRD headings, JMIR end sections, the supplement as Multimedia Appendix 1 and the STROBE checklist as
Multimedia Appendix 2. It was not accepted by i-JMR (2026-10-29).

- **Registration:** OSF Registries, [doi:10.17605/OSF.IO/C53W9](https://doi.org/10.17605/OSF.IO/C53W9)
- **Analysis code and data snapshot:** [stharrold/stharrold.github.io, `analysis/mssp-benchmark-ratchet/`](https://github.com/stharrold/stharrold.github.io/tree/53b3a8f/analysis/mssp-benchmark-ratchet)
  and the OSF project [doi:10.17605/OSF.IO/Z4AN5](https://doi.org/10.17605/OSF.IO/Z4AN5)
- **Post for a general audience:** [stharrold.github.io](https://stharrold.github.io/20261027-preregistered-mssp-early-renewal.html)

## Status

| Where | Version | Submitted | ID | Files (sha256) | Source |
|---|---|---|---|---|---|
| medRxiv | 1 | 2026-10-27 | MEDRXIV/2026/366643; **declined 2026-10-28** (medRxiv requires an organizational affiliation; not posted) | `paper.pdf` 7d111cbdef3672f2..., `supplement.pdf` d65212577e6d9809... | `dcbad91` (tag `medrxiv-v1`) |
| i-JMR | 1 | 2026-10-28 | ms 115640 (Original Paper, Health Services Research); **not accepted 2026-10-29** | `paper.docx` cafcdb715483edb1..., `supplement.docx` 33f38d7d52d3da68..., `strobe.docx` 373b584c088bef1a... | release v1.2.0 ([doi:10.5281/zenodo.23740845](https://doi.org/10.5281/zenodo.23740845)) |

JMIR Preprints was opted into at submission, but no preprint was posted, so the paper has no preprint. Both forms' text fields were
entered as plain ASCII. The i-JMR package and its checklist are in [`submission/ijmr/`](submission/ijmr/README.md).

The JMIR version differs from the medRxiv submission (tag `medrxiv-v1`) in form, in content added after review, and in how the results are
read. Every registered result is unchanged.

- **Form:** a descriptive title naming the design (JMIR's rule), JMIR's abstract headings and end sections, an
  "Ethical Considerations" section citing 45 CFR 46.102, italics rather than bold, *P* values without spaces, URLs
  moved into the references, access dates on online references, Word tables sized for the page, the generative AI
  statement moved to JMIR's submission form (JMIR policy since October 2026), and the H4 spending table moved to
  Multimedia Appendix 1 (eTable 8; later eTables renumbered).
- **Added content:** a third post hoc check, not registered: the rank correlation of the regional pull with the PY2020
  savings rate is 0.45 (eTable 13; `posthoc/pull_savings.py`). New sources: CMS's program figures for 2026, CMS's
  2018 rationale for barring moves from BASIC to ENHANCED within an agreement, a 2026 dissertation on the ratchet
  effect and regional selection (with its 40% and 70% estimates), Weitzman 1980 and Einav et al. 2022.
- **Reading:** the manuscript now says that the registered H2b wording ("evidence for the reset motive beyond past
  savings") overstates the result once the decomposition is known, and reads the pattern, as interpretation and not
  as a test, as fitting the sharing-rate motive better than the reset motive. The introduction, contributions and
  conclusions were rewritten around that reading after two critical reads.

`scripts/check_numbers.py` checks every number in the text against the committed results files, and the cited
figures that are not study results against `data/number-allowlist.tsv`, which gives each one's source.

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
| `scripts/docx_tables.py` | Widens the DOCX tables to the full text width (pandoc sizes them to 5.5 in); column widths come from `scripts/include.lua` |
| `scripts/form_fields.py` | Writes the JMIR form's plain-text fields, figure uploads and captions into `submission/ijmr/` |
| `standards/jmir/SOURCES.md` | The JMIR author-guidance articles followed (local copies are not in git) |
| `submission/ijmr/` | The i-JMR package: cover letter, AI disclosure, suggested reviewers, figure uploads, checklist |
| `posthoc/` | Byte-identical copies of the study's 2 post hoc scripts (not registered), with their source commits |
| `CITATION.cff`, `.zenodo.json` | Citation metadata; Zenodo archives each GitHub release |
| `CLAUDE.md` | Guidance for AI coding agents: rules, commands and the gotchas found while preparing the submission |

## Archive

Each GitHub release of this repository is archived on Zenodo: [doi:10.5281/zenodo.23737045](https://doi.org/10.5281/zenodo.23737045)
(concept DOI, resolving to the latest version; cite this one). The registered analysis plan and code are archived on
OSF Registries ([doi:10.17605/OSF.IO/C53W9](https://doi.org/10.17605/OSF.IO/C53W9)), and the data snapshot and
results notebook in the OSF project ([doi:10.17605/OSF.IO/Z4AN5](https://doi.org/10.17605/OSF.IO/Z4AN5)).

## Reproduce

The study has 3 parts, kept in 3 places. This repository holds only the last: it builds the manuscript from copies
of the committed results and never reruns the analysis.

| Part | Where | Permanent archive |
|---|---|---|
| Analysis plan and the registered code (commit `a4064f5`) | [`analysis/mssp-benchmark-ratchet/`](https://github.com/stharrold/stharrold.github.io/tree/53b3a8f/analysis/mssp-benchmark-ratchet) in stharrold/stharrold.github.io | OSF Registries, [doi:10.17605/OSF.IO/C53W9](https://doi.org/10.17605/OSF.IO/C53W9) (plan, code zip and their sha256) |
| The 40 CMS public use files | data.cms.gov, listed with sha256 in `data-snapshot.tsv` | OSF project, [doi:10.17605/OSF.IO/Z4AN5](https://doi.org/10.17605/OSF.IO/Z4AN5) (`mssp-snapshot-2026-10-22.zip`) |
| Results files, post hoc scripts, manuscript build | the study folder and this repository | Zenodo, [doi:10.5281/zenodo.23737045](https://doi.org/10.5281/zenodo.23737045) |

The helper scripts that download the data and compare a rerun (`fetch_snapshot.py`, `compare_results.py`) and the
environment the post hoc scripts run in are only on GitHub; `posthoc/` here holds byte-identical copies of the
post hoc scripts.

To reproduce, follow the tested steps in the study's README, [Reproduce and adapt](https://github.com/stharrold/stharrold.github.io/blob/53b3a8f/analysis/mssp-benchmark-ratchet/README.md#reproduce-and-adapt)
(git and uv; tested on macOS, and Linux should work the same way):

1. Clone only the study folder (sparse checkout) and download the data with `fetch_snapshot.py`, which keeps each
   file only if its sha256 matches and falls back to the OSF archive (about 40 MB, under a minute).
2. Check the installation with the study's tests (about 8 minutes).
3. Run the 7 registered stages in order with `ratchet/run.py ... --out-dir <dir>`. The confirm stage takes about 17
   hours with 5 worker processes; to rerun only a later stage, copy the committed files it needs into `<dir>` first.
4. Run the 2 post hoc scripts (step 4b there, under a minute).
5. Compare with `compare_results.py <dir>` (and `git diff` for the post hoc output).

What to expect: deterministic numbers (differences in means, validation metrics, correlations) reproduce exactly;
resampled and simulated numbers (bootstrap intervals, permutation *P* values, power simulations, MCMC fits) move
within simulation error, because the analysis table is read without a fixed row order. No registered verdict is
near enough to its threshold to change. The manuscript reports the committed files, which `data/README.md` traces to
their commits and sha256, and `scripts/check_numbers.py` checks every number in the text against them. To rebuild the
manuscript itself, see Build below.

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
3. i-JMR: follow [`submission/ijmr/README.md`](submission/ijmr/README.md) (the record of what was submitted).

## License

The manuscript, supplement, tables and figures are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The scripts are under the MIT license (`LICENSE`).

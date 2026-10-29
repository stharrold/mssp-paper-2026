# CLAUDE.md

Guidance for AI coding agents working in this repository. Read `README.md` first (status, layout, Reproduce, Build).

## Rules

- **Never type a number by hand.** Tables come from `scripts/make_tables.py`, figures from `scripts/make_figures.py`,
  both from the committed results in `data/`. Every number in the prose must pass `scripts/check_numbers.py`; a cited
  figure that is not a study result goes in `data/number-allowlist.tsv` with its source.
- **Analysis results are copied, never recomputed here.** New post hoc work runs in
  `stharrold.github.io/analysis/mssp-benchmark-ratchet/posthoc/` (changing no registered file), then its JSON is copied
  to `data/posthoc/` with its sha256 in `data/README.md` and the script copied byte for byte to `posthoc/`.
- **Stage explicit paths** (never `git add -A`); `main` is public.
- **What was submitted is frozen by tag:** `medrxiv-v1` (declined by medRxiv 2026-10-28, never posted) and release
  `v1.2.0` (i-JMR ms 115640, not accepted 2026-10-29). Later changes go in a new release.
- **Private material lives in `../mssp-paper-2026-private`** (local git only, no remote): journal correspondence as
  Markdown exports (`correspondence/YYYYMMDD_Email_<Venue>-<ms>_<Topic>.md`), peer reviews, and the suggested-reviewer
  list. Never commit reviewer names, reviews or emails here. A journal decision appears here only as its outcome
  ("not accepted", "accepted", "revisions requested"); editors' reasons and review content stay private, since
  the paper links this repository and the next venue's editors and reviewers can read it.

## Commands

```bash
scripts/build.sh                     # tables, figures, PDF and DOCX of paper, supplement, strobe
uv run python scripts/check_numbers.py
uv run python scripts/validate_jmir_compliance.py --article-type original
uv run python scripts/form_fields.py # ASCII form fields, figure uploads (1200 px, no alpha) and captions
uv run pytest && uv run ruff check . && uv run ruff format --check .
```

## Gotchas

- **Word tables:** pandoc sizes every DOCX table to 5.5 in and reuses the PDF widths, so short values broke across
  lines. `scripts/include.lua` (`Table`, docx only) sets content-based minimum widths and `scripts/docx_tables.py`
  rescales grids to 6.5 in. Without Word, check layout by exporting through Pages (`osascript`: open, `export ... as
  PDF`; the file must be under `~`, and the call needs the sandbox off), then `pdftoppm` the table pages. Pages ignores
  keep-with-next before a long table, so a stranded caption there is not a Word problem.
- **Rebuilds change DOCX bytes but not content** (timestamps). Compare `word/document.xml` hashes, and restore the
  committed files before a release if only metadata changed.
- **Zenodo:** archives on a published GitHub release (`GITHUB_TOKEN= gh release create`), not on a tag push. Bump
  `CITATION.cff`, `pyproject.toml` and `uv lock` first; verify with the Zenodo API. Cite the concept DOI
  10.5281/zenodo.23737045. A DOI exists only after the first release, so citing it in the paper took a second release.
- **JMIR form:** text fields as ASCII; the AI declaration is checkboxes only (no statement box), so the summary went in
  as editor-only material; the 11 checklist boxes must be ticked before "Add Another Reviewer" works; JMIR renames
  uploads itself; upload the `*.figure.png` copies, not `figures/*.png` (full size, transparent). "Contact Editor" is
  for scientific questions to an assigned editor; administrative notes go to ed-support@jmir.org with the ms number.
- **JMIR rules met here:** descriptive title naming the design, no abbreviations; Ethical Considerations in Methods;
  generative AI declared in the form, not Acknowledgments; access dates on online references; no spaces around = or <
  with *P*; numerals mid-sentence. Homepage (TOC) images may contain no text or diagrams.
- **medRxiv requires an organizational affiliation** that provides research oversight; it declined this independent
  submission. JMIR Preprints was opted into at submission, but no preprint was posted (author confirmed 2026-10-29).

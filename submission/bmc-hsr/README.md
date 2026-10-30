# BMC Health Services Research submission package (Research article)

Target: *BMC Health Services Research* (BMC Series, Springer Nature), article type Research article, for the
collection "Implementing value-based care payment models in diverse health systems" (open, deadline 12 March 2027).
The journal's requirements, as read on 2026-10-29, are summarized in `../../standards/bmc-hsr/SOURCES.md`. This
package is built from the branch `bmc-hsr-submission`; the i-JMR version is frozen at tag `v1.2.0`.

## Checks before submitting

```bash
scripts/build.sh                                      # paper, supplement and strobe: PDF and DOCX
uv run python scripts/bmc_fields.py                   # plain-text fields, figure uploads and captions
uv run python scripts/check_numbers.py                # every number in the prose against the results
uv run python scripts/validate_bmc_compliance.py      # BMC's research-article rules, and line/page numbers in paper.docx
uv run pytest && uv run ruff check . && uv run ruff format --check .
```

Recorded 2026-10-29: abstract 341/350 words in BMC's 5 sections; 8 keywords (3 to 10); 3 tables and 4 figures, titles
within 15 words; 2 additional files numbered by first citation; references in BioMed Central (Vancouver) style with
URLs and access dates; Word file double-spaced with line and page numbers. There is no word limit for research articles.

## Files

| Upload or field | File |
|---|---|
| Manuscript (Word) | `../../paper.docx` (title page, abstract, text, declarations, references, table and figure titles and legends) |
| Figures 1-4 (separate files) | `figures/Figure1.png` to `figures/Figure4.png` (flattened onto white, full size); titles and legends are in the manuscript, and in `figures/FigureN.caption.txt` |
| Additional file 1 | `../../strobe.docx` (STROBE checklist) |
| Additional file 2 | `../../supplement.docx` (eTables and eMethods) |
| Cover letter | `cover-letter.md` (or `cover-letter-plaintext.txt` for a text box) |
| Title, abstract, keywords | `title-plaintext.txt`, `abstract-plaintext.txt`, `keywords-plaintext.txt` |
| Trial registration, if asked on its own | `trial-registration-plaintext.txt` |

## Submitting

The author signs in, enters personal data, answers the declarations and attestations, and submits. The form's order
may differ from this list.

1. **Journal and article type:** BMC Health Services Research, Research article; choose the collection
   "Implementing value-based care payment models in diverse health systems" if the form offers it (the cover letter
   names it either way).
2. **Author details:** Samuel Thomas Harrold, ORCID 0009-0008-4596-6921, samuel.harrold@gmail.com, "Independent
   researcher". BMC asks for institutional addresses on the title page; there is no institution, so the author
   decides what address to give the form. The manuscript's title page gives the affiliation and email only.
3. **Title, abstract, keywords** from the plain-text files.
4. **Declarations** as in the manuscript: ethics (not human subjects research; public aggregate data), consent for
   publication not applicable, data in Zenodo and OSF, competing interests (employment at Indiana University Health,
   no role), no funding, sole author.
5. **Fee:** the APC is USD 3,450 on acceptance, paid by the author. A discretionary waiver or discount for financial
   need can only be requested now, at submission; requests during review or after acceptance are not considered.
   Whether to ask is the author's decision (a draft is kept in the private repository, not here).
6. **Licence:** CC BY 4.0 matches the manuscript repository's licence (the journal also offers CC BY-NC-ND).
7. **Peer review:** transparent. If the article is published, the reviewers' reports are published with it,
   unsigned. That overrides, for this journal, the rule that reviews stay in the private repository.
8. **Suggested reviewers** (optional): kept in the private repository, not here, because the list names third parties.
9. **Files:** upload as in the table above.

## After submission

- Record the submission (date, manuscript number) here and in the README, naming the journal only from then on; file
  the confirmation email as Markdown in `../mssp-paper-2026-private/correspondence/`.
- Freeze what was submitted in a new release (v1.3.0) so Zenodo archives it; bump `CITATION.cff`, `pyproject.toml`
  and `uv lock` first (CLAUDE.md, "Zenodo").
- A decision appears here only as its outcome; editors' reasons and reviews stay private until the journal publishes
  them.

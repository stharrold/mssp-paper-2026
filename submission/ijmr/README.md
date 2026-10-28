# i-JMR submission package (Original Paper)

Target: *Interactive Journal of Medical Research* (i-JMR), JMIR Publications, article type Original Paper. Submitted
directly (not by medRxiv transfer), with the medRxiv preprint (MEDRXIV/2026/366643, submitted 2026-10-27) disclosed
in the cover letter. The medRxiv version 1 source is the tag `medrxiv-v1`; this package is built from the branch
`ijmr-submission`.

The tooling and JMIR guidance come from `stharrold/yuimedi-paper-20250901`, the author's i-JMR article 96541
(`scripts/validate_jmir_compliance.py` and its tests, adapted) and the JMIR help-center articles listed in
`../../standards/jmir/SOURCES.md` (local copies are not in git). The form's step structure is from that repository's archived printouts of a 2026 JMIR
submission (`ARCHIVED/20260329_JMIR-Submission/`).

## Checks before submitting

```bash
scripts/build.sh                                               # paper, supplement and strobe: PDF and DOCX
uv run python scripts/form_fields.py                           # plain-text fields, figure uploads, captions
uv run python scripts/check_numbers.py                         # every number in the prose against the results
uv run python scripts/validate_jmir_compliance.py --article-type original
uv run pytest && uv run ruff check . && uv run ruff format --check .
```

Recorded 2026-10-28: JMIR-method word count 8,253 (soft limit 10,000; tables included, references excluded);
abstract 439/450 words; 7 keywords; 4 tables and 4 figures in the text (JMIR suggests at most 5 and 8); 61
references.

## Files

| Upload or field | File |
|---|---|
| Manuscript (step 3) | `../../paper.docx` |
| Figures 1-4 (step 4, type Figure) | `figures/figure*.figure.png` (1200 px on the long side, flattened onto white); captions in `figures/*.caption.txt`, without "Figure N." |
| Multimedia Appendix 1 (step 4) | `../../supplement.docx`, renamed `<ms#>-Multimedia-Appendix-1.docx`; caption in `multimedia-appendix-captions.txt` |
| Multimedia Appendix 2 (step 4) | `../../strobe.docx` (STROBE checklist), renamed `<ms#>-Multimedia-Appendix-2.docx` |
| Title, abstract, keywords (step 2) | `title-plaintext.txt`, `abstract-plaintext.txt`, `keywords-plaintext.txt` |
| Trial Registration (step 2, its own field) | `trial-registration-plaintext.txt` (JMIR format: registry, ID; URL) |
| AI usage declaration (step 3) | `ai-disclosure-plaintext.txt`; checkbox choices below |
| Comments to the editor (step 1) | `cover-letter-plaintext.txt` (497 words; limit 500); `cover-letter.docx` if a cover-letter upload slot exists |
| Suggested reviewers | `suggested-reviewers.md`, kept local and out of git because it names third parties (the author chooses and confirms no conflicts) |

Every field file is ASCII (`rho`, hyphen-minus, straight quotes), because medRxiv's form turned other characters into
HTML entities.

## Form, step by step

The author signs in, enters personal data, ticks the attestations and submits. Field text is pasted from the files
above.

1. **Start.** Journal: Interactive Journal of Medical Research. Corresponding author institutional member: none of
   these. Section: the closest health policy or health services section. Article type: Original Paper. The submission
   checklist (author ticks): not published or under review elsewhere (the medRxiv preprint is disclosed); Word
   format; italics, not bold, for emphasis; figures and tables in the text; no URLs in the body; the fee schedule
   (APF US $1985 on acceptance); fast-track (tick as read; not requested); names and affiliations come from the
   metadata form; P values per the instructions; transfer to a sister journal. Comments to the editor:
   `cover-letter-plaintext.txt`.
2. **Metadata.** The author, as entered on medRxiv: Samuel Thomas Harrold; ORCID 0009-0008-4596-6921; email
   samuel.harrold@gmail.com; affiliation "Independent researcher". JMIR asks for department, city, state and country
   and the corresponding author's full address and phone; the author decides what to enter. Degrees: the author's
   highest degree. Title, abstract (Background, Objective, Methods, Results, Conclusions) and keywords from the
   plain-text files; the registration goes in the separate Trial Registration field (if the form has none, it is the
   abstract's last line, as in the manuscript). Preprint: opt in to JMIR Preprints (the author's choice, 2026-10-28; the medRxiv preprint is
   disclosed in the cover letter).
3. **Upload submission.** `paper.docx`. AI usage declaration: Yes; tool Claude; acknowledgment text from
   `ai-disclosure-plaintext.txt`. Purposes, proposed, for the author to confirm:
   - tick: text generation; proofreading or editing; generating figures or tables; data collection, curation or
     organization (download, hashing and dbt code); data cleaning (code for the registered fill rules); data analysis
     (analysis code); visualization; code generation; literature search and summarization; reference formatting;
     other: "pre-submission critical assessment of the plan, code and manuscript";
   - the author's call: research design or developing protocols, and selecting research methods (the plan's text
     and the estimators were drafted with the tool and decided, approved and registered by the author);
   - leave unticked unless the author disagrees: idea generation, defining the research objective, questions or
     hypotheses (the author's), translation.
4. **Supplementary files.** Figures 1-4 as type Figure with their captions; the 2 multimedia appendices with their
   captions. No transcripts (see the cover letter).
5. **Confirmation.** The author reviews and submits. Afterward: archive the confirmation email and the system's
   manuscript file here, record the manuscript number in the paper README, and rename the appendices if the system
   asks for `<ms#>-Multimedia-Appendix-N.docx`.

## Not done here

- No JMIR account work, personal data, attestations or submission: those are the author's.
- The medRxiv DOI is not yet known; when the preprint posts, tell the editor by message if the paper is still in
  review.

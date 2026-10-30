# Reference audit

Run on 2026-10-30, before submission to the next venue, on the 70 entries in `doi.json` and `other.bib`. The evidence is
in `references/audit/<key>/` (git-ignored, because it holds publishers' text), made by `scripts/audit_references.py`;
each key's `7-verification.txt` is the verdict for its citing sentences, with where in the source it rests.

## Does the link work and is it the reference?

- **46 DOIs:** all registered at doi.org. Crossref titles match the stored titles, and OSF and Zenodo were checked through
  their own APIs. Crossref lists one update, a correction to SciPy 1.0 (doi:10.1038/s41592-020-0772-5), and no retraction.
- **24 URLs:** all answer. A 200 was not taken as proof: eCFR through its versioner API (the page URLs and paragraph
  anchors themselves were not loaded, because eCFR refuses scripts), the Federal Register through its document API,
  data.cms.gov through its catalog, and the rest by page title or first page.
- **3 entries are not cited** (`simmons2011`, `nosek2018`, `frcovid`), so they do not appear in the reference list.

## Does the source support the sentence?

94 checks of citing sentences, by 3 AI agents (Claude Code) each given the sentences and the sources but no expected
answer: 69 supported, 25 partly, none unsupported. The partly verdicts were fixed in the text or the entry, except as listed below. The verdicts
were written against the wording before those fixes; each fix was checked against the source when it was made.

| What the verdict rests on | References |
|---|---|
| Abstract only (no open full text) | `welch1947` (abstract on a secondary index page) |
| Working paper, not the published article | `weitzman1980` (1979), `mackinnon1985` (1983) |
| Full text, or the document itself | all others |

`douven2015`, `bleser2019`, `zhu2023`, `trombley2022` and `cappello2026` were first judged from an abstract or a preview
and rechecked against the full texts the author obtained, filed in the author's library; the sentences stood. Cappello's
"about 70% less likely" is the dissertation's wording for an odds ratio of 0.26 to 0.30.

Kept as written, as a judgement: `post` (paper.md, Availability: "for a general audience", though it also has full
methods), `paperrepo` (the Availability sentence is true of Zenodo and OSF read together), and `cfr425600` ("could enter
only Level E or ENHANCED" is the outer limit; some ACOs had only ENHANCED).

`registration`: "before any outcome value was read" is the author's attestation; the commit order is consistent with it.

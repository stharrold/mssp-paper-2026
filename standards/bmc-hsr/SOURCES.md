# BMC Health Services Research: sources for the submission package

Read on 2026-10-29 and saved on 2026-10-30 in a browser, because Springer's pages refuse scripted downloads. Local
Markdown copies are made by `scripts/import_standards.py` and kept out of git because the pages are the publishers'
(`bmc-hsr_*.md`, `bmc_*.md`, `springernature_*.md` here; the saved bundles are in the private repository). What follows
is a summary in this repository's words of what the package relies on; the journal's pages are the authority.

| Page | URL |
|---|---|
| Submission guidelines (scope, fee, formatting, cover letter, peer review) | https://link.springer.com/journal/12913/submission-guidelines |
| Research article (sections, abstract, declarations, references) | https://link.springer.com/journal/12913/submission-guidelines/research-article |
| Collection "Implementing value-based care payment models in diverse health systems" | https://link.springer.com/collections/iccjhffhib |
| Aims and scope | https://link.springer.com/journal/12913/aims-and-scope |
| BMC editorial policies (AI, preprints, duplicate publication, data availability) | https://link.springer.com/brands/bmc/editorial-policies |
| BMC open access publishing | https://link.springer.com/brands/bmc/open-access-publishing |
| Funding eligibility | https://link.springer.com/journal/12913/funding-eligibility |
| AI use in manuscript preparation | https://www.springernature.com/gp/policies/editorial-policies/ai-manuscript-preparation |
| AI use in research practice | https://www.springernature.com/gp/policies/editorial-policies/using-ai-in-research |
| APC waivers and discounts | https://www.springernature.com/gp/open-science/policies/journal-policies/apc-waiver-countries |
| Licensing and copyright | https://www.springernature.com/gp/open-science/policies/journal-policies/licensing-and-copyright |
| Journal policies for open access (discretionary waivers) | https://www.springernature.com/gp/open-science/policies/journal-policies |
| Reference style: BioMed Central CSL (`citation-style-bmc.csl`), commit `ff33b4c8dbe923e88fcee5cbae094a1307b6b36c` (sha256 as downloaded `ae2c595d97fcb1fd59c96dca5963e3a5e1432e1713273f013f2f3564a6da537c`). One change, marked in the file: its `access` macro prints the URL and access date for any reference with a URL and no DOI, not only web pages, since BMC requires both for every web link (sha256 after the change `f344a72023d63ce667308917295e142d30405a625f31611c6137d7ca45c43418`) | https://github.com/citation-style-language/styles/blob/ff33b4c8dbe923e88fcee5cbae094a1307b6b36c/biomed-central.csl |

## What the package relies on

- **Scope and criteria:** health services research, including health policy and healthcare financing; decisions on
  scientific validity, not perceived interest or impact (a BMC Series journal). Research focused on increasing
  for-profit healthcare revenue is not considered.
- **Collection:** open, submission deadline 12 March 2027; design, implementation, adaptation and evaluation of value
  based care payment models across health systems. Topics include barriers and facilitators to implementation, and
  policy reforms and governance that support it. A submission to a collection names it in
  the cover letter; collection papers go through the journal's usual peer review.
- **Fee:** APC USD 3,450 (GBP 2,590, EUR 3,050), set at the date of acceptance. Discretionary waivers or discounts for
  financial need are considered case by case, and only if requested at submission.
- **Peer review:** transparent; if the article is published, the reviewer reports are published with it (reviewers
  unnamed). Licence CC BY or CC BY-NC-ND.
- **Manuscript:** DOC/DOCX/RTF/TeX; double line spacing, line and page numbers, no page breaks.
- **Title page:** title naming the study design; full names and institutional addresses; corresponding author. LLMs
  are not authors; their use is documented in Methods.
- **AI (Springer Nature's risk framework):** use is judged by how a tool was used, and declared whatever the level.
  Drafting from author input is allowed with caution, provided the use is described, the content labelled and the
  author accountable. Argument, interpretation and conclusions must be author-led; writing results or discussion
  independently, or generating claims or interpretations without oversight, is not permitted. AI-assisted figures from
  verifiable data are allowed, with the model and purpose declared and a disclosure in the legend.
- **Prior dissemination:** a personal or institutional website or repository is not previous publication; preprint
  details (DOI, licence) are disclosed at submission; for blogs, the editor assesses any duplication.
- **Abstract:** at most 350 words, no references, few abbreviations; sections Background, Methods, Results,
  Conclusions, and Trial registration (registry, number and date) where applicable. Then 3 to 10 keywords.
- **Sections:** Background, Methods, Results, Discussion (with limitations), Conclusions, List of abbreviations,
  Declarations.
- **Declarations, all with their headings ("Not applicable" where so):** Ethics approval and consent to participate
  (a statement even where approval was not needed); Consent for publication; Availability of data and materials;
  Competing interests (initials); Funding; Authors' contributions (initials); Acknowledgements; Authors' information
  (optional).
- **References:** Vancouver style; every URL is a numbered reference with the site title and an access date, never a
  link in the text; datasets cited with persistent identifiers.
- **Figures:** separate files (PNG accepted), numbered in order of mention, keys inside the graphic; title (at most 15
  words) and legend (at most 300 words) in the manuscript, not in the image.
- **Tables:** in the text with Table objects; title (at most 15 words) above, legend (at most 300 words) below; no
  colour or shading; commas not used to indicate numerical values.
- **Additional files:** cited in order as "Additional file 1" and so on, and listed in their own section (file name,
  format, title, description); 20 MB each.
- **Cover letter:** why this journal; any policy issues; competing interests; all authors approved; not published or
  under consideration elsewhere; the collection's name. Suggested and opposed reviewers may be listed.

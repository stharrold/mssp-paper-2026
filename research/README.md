# Literature search for the preprint

A PubMed pass (NCBI E-utilities, no sign-in or quota) on 2026-10-27, to widen the study's Scholar Labs search
(saved with the post in `stharrold.github.io/analysis/mssp-benchmark-ratchet/research/`) to the core MSSP savings,
selection and participation literature for the introduction and discussion.

- `pubmed_search.py` runs the 4 queries below and writes `pubmed_<n>.json` (query, hit count, esummary records).
- `pubmed_abstracts.txt` holds the PubMed abstracts of the papers read for the manuscript; each is described in the
  manuscript only as its abstract supports.

| No. | Query | Hits |
|---|---|---|
| 1 | Shared Savings Program AND (benchmark* OR rebas* OR regional adjustment) | 18 |
| 2 | Shared Savings Program AND (exit* OR participation OR two-sided OR downside risk OR selection) | 95 |
| 3 | Shared Savings Program AND (spending OR savings) AND (difference-in-differences OR Medicare spending) | 55 |
| 4 | accountable care organization* AND Pathways to Success | 4 |

Added to the post's references: McWilliams 2016, 2018 and 2020; Markovitz 2019 (two papers); Bond 2025; Srivastava
2026; Bleser 2019; Zhu 2023; Trombley 2022. Ryan and Markovitz 2023 (JAMA Health Forum) was retracted and republished
(doi:10.1001/jamahealthforum.2024.0043) and is not cited.

## Novelty check (2026-10-28)

Before the manuscript said "to the author's knowledge, this is the first peer-reviewed study of which ACOs used the
early-renewal option", these searches looked for earlier work on early renewal itself:

| Source | Query | Result |
|---|---|---|
| PubMed | ("Shared Savings Program" OR "accountable care organization*") AND ("early renewal" OR "renew early" OR "renewed early" OR "early rebas*" OR "rebased early" OR terminat* OR "agreement period" OR reset*), title/abstract | 3 hits: 2 palliative-care trials and the 2016 rebasing rule; no study of early renewal |
| PubMed | (same population) AND ("ENHANCED track" OR "BASIC track" OR "glide path") | 0 hits |
| PubMed | "Shared Savings Program" AND benchmark*, 2022-2026 | 6 hits, all cited except the retracted 2023 JAMA Health Forum paper and an unrelated COVID-19 study |
| Web (extended) | MSSP early renewal, rebasing and terminating agreements early; NBER and SSRN working papers on rebasing timing and the ratchet | CMS rules and specifications, MedPAC's 2021 benchmark-incentives presentation (no mention of early renewal), a Wakely 2024 consulting white paper on the 2024 rules, and the cited McWilliams NBER paper; no study of early renewal |

The only analyses of early renewal found are the industry reports already cited (Milliman 2024 and 2025).

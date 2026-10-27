---
title: "Supplement 1. Why did Medicare ACOs reset their benchmarks early? A pre-registered analysis of early renewal in the Medicare Shared Savings Program"
---

**Contents**

- eTable 1. Validation of the rebuilt benchmark
- eTable 2. Power analysis
- eTable 3. Robustness of the group comparisons
- eTable 4. Robustness of the decision model (H3)
- eTable 5. Convergence and predictive checks of the decision model
- eTable 6. Conventional (frequentist) counterparts
- eTable 7. Agreement of registered and conventional verdicts
- eTable 8. Attrition from the H4 spending panel
- eTable 9. Exploratory analyses
- eTable 10. The 2 early renewers already in ENHANCED
- eTable 11. Per-capita spending by agreement year
- eTable 12. Post hoc checks against CMS's published 2022 benchmarks (not registered)
- eMethods. Registration record (eTable 13) and deviations
- STROBE checklist

All tables are generated from the committed results files by `scripts/make_tables.py` in the manuscript repository.
Item and section numbers refer to the registered analysis plan (`PREREGISTRATION.md`, version 0.6).[@registration]

{{include tables/etable1-validation.md}}

{{include tables/etable2-power.md}}

{{include tables/etable3-robustness-groups.md}}

{{include tables/etable4-robustness-h3.md}}

{{include tables/etable5-h3-checks.md}}

{{include tables/etable6-conventional.md}}

{{include tables/etable7-agreement.md}}

{{include tables/etable8-attrition.md}}

{{include tables/etable9-exploratory.md}}

{{include tables/etable10-enhanced.md}}

{{include tables/etable11-spending.md}}

{{include tables/etable12-posthoc.md}}

# eMethods. Registration record and deviations

| Item | Value |
|:--------|:----------------------------------------|
| Registry | OSF Registries, [osf.io/c53w9](https://osf.io/c53w9/), doi:10.17605/OSF.IO/C53W9 |
| Registered | October 26, 2026, 13:22:16 UTC; public, no embargo |
| Plan | `PREREGISTRATION.md` version 0.6, SHA-256 `d0e374c8b493eb2f2fa7da1c0d8cbe46745a601233f11a81d2b2be73c402e8f2` |
| Code | commit `a4064f5`, archive SHA-256 `4c98d76a586151ab608851c69217a5ddb6b394201643a3de89a839bb1f659cd4` |
| Data | 40 CMS public use files downloaded October 22, 2026, each with its SHA-256 hash in `data-snapshot.tsv`; archived on OSF[@osfproject] |

: eTable 13. Registration record

**Outcome lock.** Every data file is hashed before it is read. A file whose hash matches a performance-year results
file, a county spending file or the county assignment file could not be opened until the registration record existed, and the code had no
bypass. Before registration, only the enrollment files, the CMS data dictionaries, the regulation text and the column
names (not the values) of the outcome files were used.

**Order of analysis.** The stages ran in the order validate, power, confirm and robustness (concurrently; both
depended only on validation and power), then H4, conventional and exploratory. Each stage refused to start until its
inputs existed. The robustness results were committed about 17 hours before the confirmatory results and were read
only together with them, primary test first.

**Deviations.** All 7 stages ran with code identical to the registered commit. Two files changed after the last
stage and produced no result: a reporting script for the online dashboard, which had shown PY2021 savings rates 100
times too large, and the lockfile `uv.lock`, which took security updates to 2 packages (filelock and
virtualenv), neither of which enters an estimate. The lockfile is a registered file, so its change is logged as the one deviation; rerunning the analysis
as registered uses the lockfile at the registered commit. One sentence in the plan's background (section 1.1) is
imprecise: ENHANCED shares 75% of savings but up to 75% of losses, and the bar on moving from BASIC to ENHANCED
within an agreement period is in the 2018 rule's preamble,[@frpathways] not in the regulation's text. Nothing in the
analysis depends on it.

**Reproducibility.** A rerun from a fresh clone reproduced the validation stage exactly and every deterministic value
of the power stage, but not the simulated values exactly: H1's simulated power was 77.6% against the committed
80.4%, and H3's detection shares 15% against 17% (pull) and 15% against 14% (BASIC level). The analysis reads its
table without a fixed row order, so seeded random draws fall on ACOs in a different order in each run, and every
resampled or simulated value varies within simulation error (about 1.6 points for a detection share from 500
datasets). No verdict is near a threshold at which that would matter.

# STROBE checklist

Items of the STROBE statement for cohort studies,[@vonelm2007] with the place each is reported. "Supplement" refers
to this document.

| Item | No. | Recommendation (abbreviated) | Where reported |
|:------------|:----:|:--------------------|:------------------------|
| Title and abstract | 1 | Indicate the design; give an informative, balanced summary | Title (pre-registered analysis); Abstract (retrospective cohort study) |
| Background/rationale | 2 | Scientific background and rationale | Introduction, paragraphs 1-3 |
| Objectives | 3 | Specific objectives and prespecified hypotheses | Introduction, paragraph 4; Methods, Hypotheses |
| Study design | 4 | Key elements of the design | Methods, Study design and preregistration |
| Setting | 5 | Setting, locations, dates of recruitment, exposure, follow-up, data collection | Methods, Data sources; Population and groups |
| Participants | 6 | Eligibility criteria, sources and methods of selection; follow-up | Methods, Population and groups; Figure 1 |
| Variables | 7 | Define outcomes, exposures, predictors, confounders, effect modifiers | Methods, Variables; Hypotheses |
| Data sources/measurement | 8 | Sources and methods of measurement; comparability | Methods, Data sources; Variables (validation); eTable 1; eTable 12 (post hoc, change scale) |
| Bias | 9 | Efforts to address potential sources of bias | Methods, Study design (preregistration, outcome lock), Statistical analysis (equivalence condition); Discussion, Limitations |
| Study size | 10 | How the study size was arrived at | Methods, Population and groups (all eligible ACOs); Power; eTable 2 |
| Quantitative variables | 11 | How quantitative variables were handled; groupings | Methods, Variables; Statistical analysis (scaling by 2 SD) |
| Statistical methods | 12a | All statistical methods, including for confounding | Methods, Statistical analysis |
| | 12b | Methods for subgroups and interactions | None registered; single-cohort restrictions in eTables 3-4 |
| | 12c | How missing data were addressed | Methods, Variables (suppressed values); Results, Validation and sample |
| | 12d | How loss to follow-up was addressed | Methods, Statistical analysis (not yet renewed; balanced panel); eTable 8 |
| | 12e | Sensitivity analyses | Methods, Covariate-adjusted estimates, conventional methods and robustness; eTables 3-6 |
| Participants | 13a | Numbers at each stage | Figure 1; Results, Validation and sample |
| | 13b | Reasons for nonparticipation at each stage | Figure 1; Results, Validation and sample |
| | 13c | Flow diagram | Figure 1 |
| Descriptive data | 14a | Characteristics of participants; exposures and confounders | Table 1 (group, cohort, track, case mix, savings rate, constructed variables); the H3 adjustment factors (size, revenue category, assignment method, agreement number) are not in the results files and are not tabulated |
| | 14b | Number with missing data for each variable | Table 1; Figure 1 |
| | 14c | Follow-up time | eTable 8 (mean included post-period years by group) |
| Outcome data | 15 | Numbers of outcome events or summary measures over time | Early renewal: 29 of 306 compared ACOs (Table 1), 24 of 206 in H3 (Table 3); spending over time: eTable 11 |
| Main results | 16a | Unadjusted and adjusted estimates with precision | Tables 2-4; Figures 2-4; eTables 3, 6 |
| | 16b | Category boundaries for continuous variables | Not applicable (continuous variables not categorized) |
| | 16c | Translation of relative risk into absolute risk | Results (odds multiplier; dollar translation); eTable 5 (observed and predicted shares by decile) |
| Other analyses | 17 | Subgroups, interactions and sensitivity analyses | Results, Robustness and conventional methods; eTables 3-11 |
| Key results | 18 | Summarize key results with reference to objectives | Discussion, paragraph 1 |
| Limitations | 19 | Sources of potential bias or imprecision; direction and magnitude | Discussion, Limitations |
| Interpretation | 20 | Cautious overall interpretation | Discussion; Conclusions |
| Generalisability | 21 | External validity | Discussion, Implications (2024 rules); Limitations |
| Funding | 22 | Funding and role of funders | Declarations |

: STROBE checklist

# References

```{=latex}
\begingroup\raggedright
```

::: {#refs}
:::

```{=latex}
\endgroup
```

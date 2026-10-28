---
title: "Multimedia Appendix 1. Early Renewal of Accountable Care Organization Agreements to Reset Benchmarks in the Medicare Shared Savings Program: Preregistered Retrospective Cohort Study"
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
- eTable 12. Post hoc checks against CMS's published 2022 benchmarks and of the regional pull against past savings (not registered)
- eMethods. Registration record (eTable 13) and deviations

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

# References

```{=latex}
\begingroup\raggedright
```

::: {#refs}
:::

```{=latex}
\endgroup
```

# Response to a second critical assessment (2026-10-27)

A second, independent assessment of the draft (supplied by the author; not reproduced here). Its sources were
checked before use: the AHA/NAACOS letter of October 14, 2021; Milliman's *ACO financial results for 2022* (April
2024), which reports gross savings rates by 2022 early-rebasing status for the same 29 ACOs (11 earlier incumbents and
18 newer ACOs); and Milliman's *Annual renewal considerations* case study (April 2025). 42 CFR 425.600(d) as in force
on 2022-01-01 confirms that ACOs experienced with performance-based risk could enter only BASIC Level E or ENHANCED.

## Applied (text, no new analysis)

- H2b: the registered verdict is followed by the decomposition (w-weighted pull and regional component both 1.6, total
  gain no different), read as relative efficiency rather than a larger expected gain (issue 1).
- The BASIC-level prediction is stated as preregistered but not blind to the enrollment data (issue 4).
- Stayers include 42 later early renewers (2023-2024); the comparison is about the 2022 decision; 34 renewals into
  2024 named as a test of the new rules (issue 3a).
- Left truncation counted from the enrollment files: of 356 cohort ACOs in the PY2020 file, 22 were gone by PY2021
  and none had renewed into 2021 (issue 3c).
- Level E entry rule for experienced ACOs (issue 9); the 2021 pre-pandemic benchmark-year request (issue 9).
- Validation on levels, not changes, as a limitation (issue 2); non-independence as a limitation (issue 5); a
  median-based error scale beside the registered SD (issue 6).
- Novelty narrowed to the peer-reviewed literature, with the Milliman reports cited and compared (low-severity table).
- "No stayer moved to ENHANCED" stated as a rule; Pr(>0) shown as >0.999; the eTable 5 overall-test value labeled as
  computed with reduced sampler settings (it is a different fit from Table 3's, not a rounding difference).
- Author's employment disclosed under Competing interests, with a views disclaimer (author-approved wording).

## Applied: post hoc validation checks (issue 2; author's choice)

`analysis/mssp-benchmark-ratchet/posthoc/validation_change.py` (study repository, commit bf91e5c), reported in the
Methods, Results, Limitations and eTable 12 as post hoc. Change scale, 101 regular renewers: Spearman 0.61, median
absolute error 1.7 points, mean error -0.3. Early renewers' realized 2022 reset from CMS's published benchmarks: mean
-1.3%, median -1.5%, 66% below the PY2021 benchmark; rebuilt -1.6 vs realized -1.4 (26 ACOs). Updated benchmark
PY2021 to PY2022, early renewers minus stayers: 0.0 points (95% CrI, -2.0 to 2.2).

## Not applied: other new analyses (author's decision: not before posting)

All would be post hoc, outside the registered pipeline, and labeled exploratory: a stay/renew/leave model across 2022-2024 and the 2024 renewals
(issue 3); non-ESRD pull recovering the 39 excluded ACOs (issue 7); H3 with the CMS savings rate as control (issue 6);
cluster permutation by parent organization (issue 5); a beneficiary-weighted check; Table 1 adjustment factors;
GPDC/REACH destinations of leavers.

## Not applied, and why

- Rambachan-Roth breakdown value (issue 10): H4 is a null result, so a breakdown value for rejecting the null is not
  informative; the trend-adjusted estimate and the equivalence threshold (about 12%) are reported.
- 2021 risk-score drop (issue 9): no source in hand; not asserted.
- Row-order fix: a change to registered code; the nondeterminism is disclosed and bounded instead.
- Retitling: the author's decision (the title matches the OSF registration).

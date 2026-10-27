# Critical assessment of the medRxiv preprint (2026-10-27)

Reviewed: `paper.md`, `supplement.md`, `paper.pdf`, `supplement.pdf`, `tables/*.md`, `figures/*.png` and
`references/` at commit `14bb6b0`. I checked them against `data/results/*.json`, `PREREGISTRATION.md` v0.6 (sha256
`d0e374c8...`, matches the registered commit `a4064f5`), `DEVIATIONS.md`, `ratchet/*.py` and the blog post
`content/20261027-preregistered-mssp-early-renewal.md`.

## Overall assessment

The numbers are sound. Every table cell and every prose number I traced (about 250) matches its results field, with
correct sign, group, sample and rounding, and the registered verdicts, the decision-rule wording, the equivalence
condition and the deviation record are stated faithfully. The problems lie elsewhere:

- **Units and meaning.** "Log points" means two different things, and the abstract's primary result drops the
  qualifier "relative to their benchmarks".
- **Misstated methods.** The power analysis did not use spreads "not used in the tests", the downloaded files are
  described as the data used, and the registered Bayesian regressions are never described. Without that description
  a reader misreads the H2b robustness numbers.
- **Plan-required reporting left out:** posterior probabilities P(>0), notes where a *P* value and its credible
  interval disagree, two exploratory analyses, and the largest propensity weight.
- **Caveats the blog post has and the manuscript dropped:** the equivalence threshold was about 12%, three times the
  MDE; the MDE was understated for 26 vs 241; the robust regressions fall below the MDE; H2a is fragile; leavers
  have a high pull; the BASIC level is partly chosen.
- **Wording that implies motives or effects,** in the title, Discussion, Implications and Conclusions.
- **Mechanical problems in the PDF:** every hyphen extracts as U+2011, so DOIs and URLs copied from the PDF fail;
  Crossref subtitles leak into references; the supplement has no manuscript title.

None of this changes a verdict. All of it would draw a reviewer comment, and some of it a screening query.

## Findings

### Must fix

**M1. "Log points" is used in two scales, so the H4 numbers contradict each other.**
- *Where:* paper.md line 308 ("MDE 3.8 log points"), line 310 ("0.115 log points"), line 311 ("H4 estimate of
  0.004"); the Table 4 note; eTable 2 ("SD 0.069 log points" next to "3.8 log points"); the eTable 6 note and the
  Figure 4A axis ("log points x 100").
- *Evidence:*
  - `power.json h4.mde_log` = 0.0379 is reported as 3.8 log points, that is, log units × 100.
  - `did.json pre_trend_check.equivalence.scaled_bound` = 0.1150 and `abs_h4` = 0.0038 are reported as "0.115 log
    points" and "0.004", that is, in log units.
  - `power.json h4.sd_delta_pre` = 0.0693 is called "0.069 log points" in the same eTable 2 row that calls 0.038
    "3.8 log points".
  - A reader is told that the MDE (3.8) is about 33 times the scaled bound (0.115), when in fact the bound is
    about 3 times the MDE.
  - "log points x 100" counts the factor 100 twice.
- *Fix:* use log points (log units × 100) throughout:
  - "the scaled pre-trend bound, 2.41 years × 4.8 log points, was 11.5 log points (about 12%), far above the absolute
    H4 estimate of 0.4 log points";
  - eTable 2: "SD 6.9 log points";
  - Figure 4A and eTable 6: "log points" (drop "x 100").

  Alternatively, write "log difference 0.115" wherever log units are meant. Update `make_tables.py` and
  `make_figures.py`, not just the prose.

**M2. The abstract states the primary result without its reference point.**
- *Where:* paper.md lines 35-36.
- *Evidence:* "Early renewers' regions spent 3.4 percentage points of benchmark more than stayers'". The measure is
  `pull` = 100 × (Σ s_e R_e − B)/B (plan §4.3 step 6), relative to each ACO's own current benchmark. The body (line
  267-268) adds "relative to their current benchmarks"; the abstract does not. As written, it reads as an absolute
  difference in regional spending.
- *Fix:* "Early renewers' case-mix-adjusted regional spending exceeded their current benchmarks by 3.4 percentage
  points more than stayers' (95% CrI, ...)".

**M3. The data sources describe the downloaded snapshot, not the files used.**
- *Where:* paper.md line 21 ("CMS public use files (2014-2026)") and lines 108-109 ("enrollment files (one per year,
  2014-2026), performance-year ... results (2013-2024)").
- *Evidence:*
  - `ratchet/config.py` reads enrollment files PY2016-PY2024, results PY2016-PY2022 plus PY2023-PY2024 (H4 and
    descriptive), county spending 2019-2021, and the 2021 county assignment file.
  - Plan §2.1: "The manifest also lists files not used here, retained from the design stage." The 2013-2015 results,
    the 2014, 2015, 2025 and 2026 enrollment files, the 2024-2026-starter county files and 4 of the 5 assignment
    files are unused.
- *Fix:*
  - Abstract: "CMS public use files (2016-2024)".
  - Data sources: list the years actually read, and say that the 40-file snapshot also holds files kept from the
    design stage that no analysis reads.

**M4. The power analysis is misdescribed.**
- *Where:* paper.md lines 209-211.
- *Evidence:*
  - The text says MDEs were "computed ... from spreads in years or groups not used in the tests".
  - That is true only for H1 (`power.json h1.sd`, PY2016-PY2018).
  - H2a and H2b use the SD among stayers (`h2.pull.sd_stayers` = 4.55, `h2.own.sd_stayers` = 3.33), the same ACOs
    the test compares (plan §6: "using the SD among stayers").
  - H4 uses the SD of Δ_pre among the compared ACOs (`h4.sd_delta_pre`), the variable of the pre-trend check.
- *Fix:* "...from the cross-ACO SD of the savings rate in PY2016-PY2018 (H1), the SD of each constructed variable
  among stayers, computed after validation (H2a, H2b), and the SD of the pre-period change (H4); MDEs assumed 29 vs
  277 ACOs."

**M5. The registered §5.3 Bayesian regressions are never described, so their numbers are misread.**
- *Where:* paper.md lines 220-224 and 331-333; the eTable 3 note.
- *Evidence:*
  - `ratchet/regression.py` fits Student-t errors on a standardized outcome with Normal(0, 1) priors (plan §5.3), a
    robust regression.
  - The manuscript calls the result "the cohort-adjusted Bayesian regression 2.1 (95% CrI, 0.5 to 3.8)"
    (`robustness.json 1_adjusted_regressions.H2b.unadjusted_5_3.b_early_units.mean` = 2.13). That implies cohort
    adjustment moved the estimate from 3.4 to 2.1. But the confirmatory estimator is already within-cohort, and
    OLS with the same covariates gives 3.35 (`conventional.json H2b.ols_hc2.difference`). The drop comes from the
    robust likelihood, which downweights a few large early-renewer values.
  - The blog post says the regression estimates "are below the minimum detectable effect and well below the +3.4
    difference in means, which suggests a few large values among early renewers carry part of it". The manuscript
    dropped this.
  - The robustness list on line 223 also omits items 4-6 (H1 PY2021, Firth, BY2-BY3 only), which eTables 3-4
    report.
- *Fix:*
  - Methods: add one sentence describing §5.3 (robust Bayesian linear regression with Student-t errors on early
    renewal and cohort, reported, not used for decisions).
  - Results: "the robust (Student-t) regressions gave 2.1 and 2.2, below the MDE of 2.5, so a few large values
    among early renewers carry part of the difference in means".
  - Complete the item list and add "Student-t errors" to the eTable 3 note.

**M6. Reporting that the registered plan requires is missing.**
- *Where:* Tables 2-4 and eTables 3 and 9.
- *Evidence:*
  - **P(>0).** Plan §5: "Each confirmatory quantity is summarized by its posterior mean, 95% equal-tailed credible
    interval, and posterior probability of a positive value". Plan §5.4 requires the same for the adjustment
    factors. `p_positive` exists for every quantity (for example `confirm.json groups.H2b_pull.p_positive` = 1.0 and
    `h3.posterior.b_prospective.p_positive` = 0.058) and appears nowhere.
  - **P/CrI disagreements.** Plan §5: "when it and the credible interval disagree, both are reported and the
    disagreement is noted". eTable 3 has two unflagged cases:
    - H2a by medians: CrI −3.22 to −0.017 excludes 0, but *P* = .085 (`robustness.json 2_medians.H2a`).
    - H2a in the 2020 cohort only: CrI −4.21 to 0.47 includes 0, but *P* = .043 (`3_cohort_2020.H2a`).
  - **Exploratory items.** Plan §5.6 lists the 2 early renewers already in ENHANCED, "reported individually against
    the stayer distribution" (`exploratory.json enhanced_early_renewers`), and spending by agreement year
    (`spending_by_agreement_year`). Neither is in eTable 9 or the text.
  - **Largest propensity weight.** Plan §5.8 item 3: "The largest weight is reported" (0.83,
    `did.json robustness.3_propensity_weighted.max_weight`). It is not in Table 4.
- *Fix:*
  - Add a P(>0) column to Tables 2-3 (or eTables).
  - Footnote the two disagreements in eTable 3.
  - Add the two exploratory items to eTable 9, or to an eTable 9b. The ENHANCED pair is the one group whose
    renewal could not raise the sharing rate, so it bears directly on the motive question.
  - Add "largest weight 0.83" to the propensity row or the Table 4 note.

**M7. Crossref subtitles leaked into two reference titles.**
- *Where:* references 11 (Lyu) and 19 (Trombley) in paper.pdf.
- *Evidence:*
  - Ref 11 reads "...Medicare Shared Savings Program: Study examines changes in Medicare Share Savings Program
    participation patterns". That is a Health Affairs teaser, not part of the title, and contains a typo ("Share
    Savings").
  - Ref 19 appends "Study examines Medicare's Accountable Care Organization Investment Model which provided funds
    to small, rurally located ACOs".
  - Ref 24's title starts "Analysis/mssp-benchmark-ratchet" (CSL capitalization of a path).
- *Fix:* strip the `subtitle` field for these two DOIs in `references/doi.json` (or override them in
  `fetch_references.py`), and brace or rephrase ref 24's title.

### Should fix

**S1. Unflagged causal and motive language.** H1-H3 are associations (plan §1.4, rule 8), but several sentences read
as statements of purpose or effect:
- *Title:* "Why did Medicare ACOs reset their benchmarks early?" asks about motives, which the design cannot
  establish (rule 8: "No test here can rule the sharing-rate motive in or out").
- *Discussion line 340-341:* "the ACOs that ended their agreements early to reset their benchmarks were those
  whose..." attributes a purpose and overgeneralizes ("were those").
- *Line 353-354:* "the ACOs that reset early were those with the most room under their regions' spending" says more
  than a mean difference shows.
- *Conclusions lines 406-407 and abstract line 42:* "were those whose regions spent more ... and those at higher
  BASIC levels" should say "were more often" or "on average had".
- *Abstract line 43, Conclusions line 408:* "A reset was not, on average, a route to a higher benchmark" is a
  counterfactual drawn from an approximation whose own-spending part is mostly noise (line 249). Add "by the study's
  approximation".
- *Implications lines 372-374:* "positioned to gain from ... the higher sharing rate". The sharing-rate gain was not
  measured.
- *Objective line 18:* "whether their spending changed afterward" should read "differed afterward".

*Fix:* reword as above. Consider retitling "Which Medicare ACOs reset their benchmarks early? A preregistered cohort
study of early renewal in the Medicare Shared Savings Program"; this also satisfies STROBE item 1 (S12).

**S2. The exposure/outcome framing conflicts, and the abstract misassigns roles.**
- *Where:* Methods line 139; abstract lines 25-32.
- *Evidence:*
  - Methods calls the regional pull "the primary exposure measure".
  - The abstract lists early renewal as the exposure and the pull as the primary outcome.
  - In H3, early renewal is the outcome and the pull a predictor. For H1-H3 the logical structure is
    determinants → choice; only H4 has early renewal as an exposure.
  - The abstract also lumps savings rates (H1, registered as *descriptive*), H3 and H4 under "Secondary". Only H2a is
    secondary (plan §1.3).
- *Fix:*
  - Abstract: "Exposures: pre-decision characteristics (regional pull [primary], own-spending component, BASIC level)
    for the choice analyses; early renewal for the spending analysis."
  - Main outcomes: "early renewal (29 of 306); per-capita spending growth 2022-2024."
  - Label roles as registered (H2b primary, H2a secondary, H1 descriptive, H3 and H4 with their own decision rules).
  - Change "primary exposure measure" in Methods to match.

**S3. The equivalence condition could only hold for very large effects, and the manuscript does not say how large.**
- *Where:* paper.md lines 311-312.
- *Evidence:*
  - The blog post: "The condition needed an estimate above 0.115 log points, about 12% and three times the minimum
    detectable effect".
  - The manuscript says only "for any estimate near zero the condition could only fail".
  - Even a pre-trend point estimate of 0 with this interval width (half-width about 3.5 log points) gives a bound of
    about 8.5 log points.
- *Fix:* "the condition could have held only for an H4 estimate above about 12% in absolute value, three times the
  MDE, so with one pre-period it could not support reading a plausible-sized estimate as an effect." Add the blog's
  "a trend difference of the size the pre-period allows could hide an effect in either direction".

**S4. The MDEs assume 29 vs 277, but the gain variables were compared on 26 vs 241.**
- *Where:* paper.md line 268 ("above the MDE of 2.5") and the Table 2 note.
- *Evidence:*
  - `power.py` uses 29 vs 277 (n of all compared ACOs).
  - The tests used 26 vs 241 (`confirm.json groups.H2b_pull.n_early`/`n_stayer`).
  - The MDE at the analyzed n is 2.80 × 4.55 × sqrt(1/26 + 1/241) ≈ 2.6 (H2b) and 1.9 (H2a).
  - The blog says the MDE "is slightly understated for the 26 vs 241 compared".
- *Fix:* add that sentence and the corrected values to the Table 2 note.

**S5. The measurement-error SD exceeds the variable's SD, which the classical model cannot produce.**
- *Where:* paper.md lines 247-250, line 293, Limitations line 390.
- *Evidence:*
  - `validation.json step1.sigma_own` = 4.38 against `power.json h2.own.sd_stayers` = 3.33.
  - Under observed = true + independent error, Var(observed) ≥ Var(error). So either the validation-sample error
    does not transfer to the study sample, or it is heavy-tailed or correlated with the true value.
  - The step-1 median absolute error is only 1.4% (`step1.median_abs_pct_error`). A normal error with SD 4.38 would
    have a median absolute value of about 3.0, so a few outliers likely inflate the SD.
  - The registered model therefore treats the variable as almost pure noise, and the H3 own-spending coefficient
    returns its prior.
- *Fix:* say this in one or two sentences, and soften "at the level of one ACO that component is mostly noise" to "by
  the registered error model". The model is registered and stays; only its interpretation needs the caveat.

**S6. The robustness paragraph reports fragility only for H2b and H3.**
- *Where:* paper.md lines 327-336.
- *Evidence:* H2a, on which the abstract's "beating their benchmarks by more" leans, is weaker in several checks:
  - by medians, *P* = .085 (`robustness.json 2_medians.H2a.p_value`);
  - in the adjusted regression, interval −2.61 to 0.02 (`1_adjusted_regressions.H2a.adjusted`);
  - in adjusted OLS, *P* = .06 (`conventional.json H2a.ols_hc2_adjusted.p_value`).

  H1 shows the same pattern: by medians *P* = .061, adjusted regression interval −0.11 to 2.61, adjusted OLS *P* =
  .06. The blog post reports these ("H2a is weaker by medians", "H1 is weaker with adjustment").
- *Fix:* add one sentence, for example "H2a and H1 kept their direction but lost conventional significance by medians
  and with track, level and size adjustment."

**S7. The leavers' regional pull is omitted.**
- *Where:* paper.md lines 335-336 and Discussion.
- *Evidence:* `exploratory.json leavers.leaver.pull.mean` = 4.81 against `early.pull.mean` = 4.97 (medians 1.95 vs
  3.50; 20 of 28 leavers with the variable). The blog reports it. That a third group with no early renewal had a mean
  pull as high as early renewers' bears on reading H2b as reset-motive evidence.
- *Fix:* add "and a mean regional pull similar to early renewers' (4.8 vs 5.0; medians 2.0 vs 3.5)". Also note that
  8 of 28 leavers (29%) lacked the variable (`Table 1`: 20 of 28).

**S8. The BASIC level is partly chosen, and the manuscript treats it as a fixed position.**
- *Where:* Discussion lines 364-368; Methods line 159.
- *Evidence:* the blog post ("How the question was chosen") and 42 CFR 425.600 say ACOs choose their entry level,
  can advance faster, and could pause the glide path for 2021. A PY2021 level of C-E therefore partly reflects an
  earlier choice to take on risk, not only "a short step to ENHANCED".
- *Fix:* add one sentence to Methods (how the PY2021 level is determined) and one to Discussion (the association may
  reflect risk appetite as well as proximity to ENHANCED).

**S9. The exposure measures postdate the decision.**
- *Where:* Methods "Variables"; Limitations.
- *Evidence:* the pull and the gain use 2021 county spending, PY2021 spending and risk scores, and the PY2021 updated
  benchmark. Final PY2021 values were published after the 2022 renewal decision, made during 2021. Plan §4.1 notes
  that only the PY2020 position was "broadly known" before the decision.
- *Fix:* state that the constructed variables are ex-post measures that proxy what ACOs could expect from quarterly
  reports, and add this to Limitations point 2.

**S10. The diagnostic-query provenance is applied only partly.**
- *Where:* paper.md lines 255-258; the Table 1 note; Figure 1 ("ESRD county counts all suppressed").
- *Evidence:*
  - The blog: "These details and the size medians below come from a diagnostic query run after the results, outside
    the registered pipeline".
  - The manuscript attributes only the medians to the query, and states the all-ESRD-suppressed reason as a pipeline
    fact. The results files record only counts (`confirm.json groups.*.excluded`).
  - The blog also notes "for 15 the aged/dual counts are hidden too", and that the plan's fill rules cover hidden
    results-file cells, not fully hidden county weights.
- *Fix:* move "A diagnostic query run after the results, outside the registered pipeline, showed..." to the start
  of the ESRD sentence; add the two blog details; mark the Figure 1 box and the Table 1 note "(diagnostic query)".

**S11. The Student-t prior "gave the same verdicts", but it was never tested.**
- *Where:* paper.md line 296.
- *Evidence:*
  - Verdicts come from the direct-simulation *P* under the Normal-prior model. The t-prior fit has no test (plan
    §5.4 asks only that differing "core conclusions" be flagged).
  - The t-prior fit needed its registered rerun (`confirm.json h3.t_prior.convergence.attempts` = 2; eTable 5 "1 /
    2"). The main text says only that "the model converged on its first fit".
- *Fix:* "Under the Student-t prior (converged on its registered rerun) the pull and BASIC-level intervals also
  excluded zero, so no core conclusion differs between priors."

**S12. Several STROBE mappings are thin or do not hold.**
- *Where:* supplement.md lines 86-117.
- *Evidence and fixes:*
  - *Item 1:* the title does not name the design ("pre-registered analysis"). Add "cohort study" to the title.
  - *Item 14a:* Table 1 lacks the H3 adjustment covariates (size, revenue category, assignment method, agreement
    number). These are not in the results files, so either add them from a labeled diagnostic query or state the
    omission.
  - *Item 14c:* no summary of follow-up time is given. Add the mean included post years by group (eTable 8 allows
    it; c̄ = 2.41 for early renewers).
  - *Item 15:* no group means of spending over time are reported, only differences. Add mean per-capita spending by
    group and year, PY2020-PY2024 (descriptive).
  - *Item 16c:* "$385" and "×3.8" are not absolute risks. Point to eTable 5's observed and predicted shares (57% vs
    45% in the top decile), or report predicted probabilities at low and high pull.
  - *Item 12b:* single-cohort checks are restrictions, not subgroup or interaction analyses. Say "none; single-cohort
    restrictions in eTables 3-4".

**S13. Two citations do not support what they are attached to.**
- *Where:* paper.md line 70 and line 388.
- *Evidence:*
  - Trombley 2022 (ref 19) is cited for "departures with projected costs to Medicare". Its abstract estimates
    AIM's *savings* and reports that "nearly two-thirds of AIM ACOs exited ... when faced with the requirement to
    assume downside financial risk". It projects no costs of departure; that is Moloci 2021 alone.
  - Markovitz 2019 (Health Affairs, ref 8) is cited for the pull "carries a coding-intensity term". That paper found
    "the MSSP was not associated with consistent changes in within-beneficiary risk scores" (risk adjustment *deters*
    coding increases), so it does not support a coding-intensity concern.
- *Fix:*
  - "...and by departures, with projected costs to Medicare,[@moloci2021] including most ACO Investment Model ACOs
    once downside risk was required.[@trombley2022]"
  - For coding intensity, cite nothing, or a source on ACO-versus-region coding differences. Keep Markovitz 2019 only
    for dropping high-risk beneficiaries.

**S14. The dollar translation is computed from a rounded value and invites a misreading.**
- *Where:* paper.md lines 270-271.
- *Evidence:*
  - 3.4 × 11,312 = 385, but the estimate is 3.35 (`confirm.json groups.H2b_pull.posterior_mean`), which gives $379.
  - More importantly, $385 is the gap in *regional spending relative to the benchmark*, not a benchmark gain. The
    regional-component difference, which is what a reset would add, is 1.56 points, about $176.
- *Fix:* "...3.35 points is about $380 per beneficiary-year of regional spending relative to the benchmark; the
  difference in the regional component itself, 1.6 points, is about $175." Update `number-allowlist.tsv`.

**S15. The PDF text layer is broken: every hyphen is U+2011.**
- *Where:* paper.pdf and supplement.pdf.
- *Evidence:*
  - `pdftotext` finds 0 ASCII hyphens and 453 U+2011 (non-breaking hyphen) in paper.pdf. The LaTeX that pandoc
    generates has 595 ASCII hyphens and no U+2011, so the cause is the ToUnicode map of the embedded Source Sans Pro
    font.
  - Copying a DOI from the PDF (for example `10.7326/m18‑2539`, `10.1111/1468‑0009.12468`), the ORCID or the URLs
    yields strings that do not resolve, and medRxiv's text extraction and reference matching get the same
    characters.
  - Likewise "α" (U+03B1 in the source) extracts as "ɑ" (U+0251) in the Table 2 and eTable 2 notes.
- *Fix:*
  - Set a font whose hyphen maps to U+002D (for example `mainfont: Source Sans 3`, or Latin Modern), rebuild, and
    confirm with `pdftotext paper.pdf - | grep -c -- '-'`.
  - Ref 21's URL also extracts with spaces ("medicare‑ shared‑ savings‑"). Use `\url` breaking via xurl only, with
    no justification stretch, for example by setting the bibliography ragged-right.

**S16. The supplement does not name the manuscript.**
- *Where:* supplement.pdf page 1.
- *Evidence:* the title page shows only "Supplement 1 / Samuel Thomas Harrold / October 2026". The `subtitle` in
  supplement.md's YAML is not rendered, because Eisvogel with `\maketitle` drops it.
- *Fix:* put the manuscript title in the `title` ("Supplement 1. Why did ...") or in the body's first line. medRxiv
  supplementary files should be identifiable on their own.

**S17. The author block lacks a location.**
- *Where:* paper.md line 2.
- *Evidence:* "Independent researcher" has no city or country. ICMJE affiliation format and medRxiv's author
  screening both use the location, and medRxiv screens unaffiliated authors more closely.
- *Fix:* "Independent researcher, <City>, <State>, USA". The medRxiv form also needs it.

### Consider

- **C1. Showing the design to medRxiv screening.** To avoid the "simple analysis of public data" reading, open the
  Importance or Design with what is not simple:
  - a rule-based reconstruction of the 42 CFR 425.601 benchmark, validated against CMS's published benchmarks
    *before* use;
  - a code-enforced outcome lock with an OSF timestamp;
  - registered decision rules, and a measurement-error decision model tested by direct simulation.

  The abstract (about 385 words) is long for the JAMA format it mimics (350); cutting the "Design" methods detail and
  adding the H3 estimates (now absent from the abstract, line 38-39) would help both. Also hedge "has not been
  studied" (line 15) as the body does ("to the author's knowledge").
- **C2.** "enforced by a hash-based lock" (abstract line 22) describes a self-imposed check whose unlock is a local
  file (`REGISTRATION.md`), not the OSF record. The body handles this well (line 97-98: the registry timestamp
  establishes order). In the abstract, "with a code-level lock on outcome files" is safer. The lock also covers the
  county *assignment* files (`config.OUTCOME_PREFIXES`), not just "results ... or a county spending file" (line 100).
- **C3.** The robustness stage ran and was committed about 17 hours *before* the confirmatory results (supplement
  eMethods). Main Methods line 102-103 implies power was the only stage before confirm. Add half a sentence to the
  main text.
- **C4.** "115 of 277 stayers ... had left the comparison, to exits or later renewals" (line 317-318): it is 72 exits,
  42 renewals and 1 with no spending value (`did.json attrition`, PY2024). Early renewers are not "in the
  comparison"; say "left the panel".
- **C5.** Table 4 lists TWFE at 306 ACOs and H4 at 305. The stayer with no post-period spending keeps its pre-period
  rows in TWFE. Say so in the note. Figure 4B's title "(29 vs 276 ACOs)" is wrong for the balanced (25/162),
  2020-cohort (18/118), propensity (305) and TWFE (306) rows. Drop the count from the title or give per-row Ns.
- **C6.** In Methods line 188, "each coefficient is a log-odds difference per 2 SD" is true only for continuous
  predictors; binaries are centered, not scaled (plan §5.4, `decision.make_design`). Line 289-290 then gives the
  BASIC level "per 2 SD". Say "per 2 SD (continuous) or per category (binary)". Also give 2 SD of the pull in
  points (about 9-10 pp from Table 1 SDs), so "×3.8 odds" has a scale.
- **C7.** In Methods line 187, "4 chains of 2,000 draws" leaves out the 2,000 tuning draws and target acceptance
  0.95 (plan §5.4). Rambachan and Roth (line 206) and Lakens (line 204) are cited for adaptations, not their methods
  (the plan says "in the spirit of"). Say so. Gelman et al. 2008 recommend Cauchy and t(7) defaults, not t(3); "a
  Student-t(3, 0, 2.5) prior, after Gelman et al." is fine.
- **C8.** Suppressed-value rules (line 161-163) list 3 of the 4 registered rules; rule 4 (hidden risk score) is
  missing. County weights use the 2021 performance-year assignment as a BY3 proxy (plan §4.3 step 2). Both could be
  stated in one clause.
- **C9.** Plan §1.4 notes that no stayer moved to ENHANCED within its agreement, and that assignment-method changes
  occurred at PY2022 in 2 of 29 early renewers and 14 of 277 stayers. The first strengthens the "one choice" point
  (line 365-366); the second belongs in H4's limitations.
- **C10.** Post-hoc option (label it as such): early renewers' actual 2022 `HistBnchmk` against their PY2021
  benchmark is now readable from the full PY2022 file. It would check "a reset would on average have lowered both
  groups' benchmarks" against CMS's numbers for the 26 early renewers. Similarly, an exploratory version of H2b that
  imputes ESRD county weights from all-type weights would show whether the 12% exclusion matters.
- **C11.** Multiplicity: the paper has one primary test, so this is minor, but a sentence noting that the H3
  (3 tests) and H4 decisions are unadjusted, as registered, pre-empts a reviewer query.
- **C12.** eTable 9 note: "Two ACOs without a census region (2)" duplicates the 2. The region model's n is then 204,
  not the 206 that `census_region_in_h3.sample` reports; state the model n. eTable 3's median rows report the
  bootstrap posterior mean (H2b 2.85) while the *P* value tests the observed median difference (3.02); the note
  could say so.
- **C13.** Typography:
  - title "pre-registered" against body "preregistered" (pick one);
  - citations render as "[53]" rather than AMA superscripts;
  - journal names are not abbreviated (AMA: *N Engl J Med*);
  - DOIs are lowercased by citeproc;
  - Table 1 splits across pages 8-9 and leaves page 9 mostly blank before Figure 1 (float `H`); consider `t!` or
    moving Figure 1 before Table 1.
- **C14.** Supplement Contents lists "eMethods" but not eTable 10, which sits inside it.

## Checked and found correct

- **Every cell of Tables 1-4, eTables 1-10 and Figures 1-4** against the results JSON: values, signs, rounding,
  group Ns, CrIs, *P* values. Table 1 percentages and track splits match `exploratory.who_renewed`, the balance
  rows match `exploratory.balance`, and the savings-rate and component rows match `exploratory.leavers`.
- **Derived numbers:**
  - exp(1.336) = 3.80;
  - 3.4 × 11,312 = 385 (but see S14);
  - 115/277 = 41.5% and 4/29 = 13.8%;
  - 2.414 × 0.0476 = 0.1150 (`c_bar`, `scaled_bound`), and c̄ = 70/29 from the attrition pattern;
  - −5.257 + 3.692 = −1.57 and −3.199 + 2.151 = −1.05;
  - 189 = 11 + 159 + 19 and 145 = 18 + 118 + 9;
  - 16 of 27 at Level E (5 + 11) and 26 of 27 to ENHANCED (one BASIC B stayed in BASIC);
  - 3/29 = 10.3% and 36/277 = 13.0%;
  - 101 of 111 (`validation.excluded` = 10);
  - H3 sample 27 + 209 − 3 − 27 = 206;
  - σ = 4.375 → 4.38 (`sigma_v_model`, step-1 source);
  - the H4 percentages = 100(e^x − 1) of the log estimates; TWFE −1.55% (−5.36% to 2.41%).
- **The abstract's numbers** all match the body and the JSON.
- **Plan fidelity:**
  - hypothesis roles (H2b primary, H2a secondary and not separate evidence, H1 descriptive);
  - H3 predictors, priors, measurement-error model and fallback;
  - the direct-simulation procedure (confirmed in `decision.direct_simulation_test`);
  - the permutation *P* formula;
  - decision-rule wording, quoted correctly;
  - the equivalence condition (§5.8; c̄ among early renewers, larger absolute CrI bound);
  - the not-yet-treated comparison;
  - the 10% exclusion rule (reported as a limitation);
  - attrition by group and year (§4.5, eTable 8 matches `did.attrition`);
  - imputed counts by group (1 and 3);
  - the validation pass rule and the calibration range.
- **Deviations:** `git diff --stat a4064f5` against each results file's `git_commit` (fd1920f, 1debc2c, 3e5cb9b,
  992d13f, acc8b0e, ff6e64b) shows no change to registered paths, so "code identical to the registered commit"
  holds. The plan sha256, code commit, zip hash and OSF timestamp in eTable 10 match `REGISTRATION.md`. The
  uv.lock deviation and the imprecise §1.1 sentence are described as in `DEVIATIONS.md` and the blog.
- **Caveats carried over from the blog:** the type-M caution, the own-spending coefficient being its prior, the
  2024 rule change (prior savings adjustment, negative-adjustment offset, ACPT), reproducibility within simulation
  error (77.6% vs 80.4%), the anticipation and composition threats, and the exclusions above 10% with smaller
  excluded ACOs.
- **Citations matching their abstracts:** McWilliams 2016, 2018 and 2020; Bond 2025; Markovitz 2019 (exit, IV
  analysis); Bleser 2019; Zhu 2023; Srivastava 2026; the methods references (Rubin, Phipson-Smyth, Gelman 2008,
  Vehtari, Firth, Callaway-Sant'Anna, Roth, Rosenbaum-Rubin, Welch, MacKinnon-White, Gelman-Carlin) as used. The
  retracted Ryan-Markovitz 2023 is correctly not cited.
- **Declarations:** ethics, funding, competing interests, data and code availability, author contributions and AI
  use are all present and consistent with the README's medRxiv checklist.

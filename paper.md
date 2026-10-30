::: {.author-block}
Samuel Thomas Harrold, Independent researcher\
ORCID: [0009-0008-4596-6921](https://orcid.org/0009-0008-4596-6921)\
Corresponding author: Samuel Thomas Harrold, [samuel.harrold@gmail.com](mailto:samuel.harrold@gmail.com)
:::

# Abstract

**Background:** Medicare Shared Savings Program (MSSP) benchmarks are reset at each new agreement from an accountable
care organization's (ACO's) recent spending, adjusted toward its region. Ending an agreement early reset the benchmark
sooner and was the only way for a BASIC-track ACO to reach the ENHANCED track's 75% share of savings. No peer-reviewed
study has examined why. This study asked which ACOs renewed early, weighing a reset motive (a higher benchmark)
against a sharing-rate motive, and whether spending then changed.

**Methods:** This preregistered retrospective cohort study included the 334 MSSP ACOs whose agreements began July 1,
2019 or January 1, 2020, using public Medicare files (2016-2024). The plan and code were registered before outcome
data were read. The reset benchmark was rebuilt from the regulation and validated on 101 other ACOs. 29 ACOs renewing
early in January 2022 were compared with 277 stayers on the regional pull (primary), the own-spending component and
BASIC risk level, by Bayesian bootstrap, permutation tests and logistic regression. Spending growth in 2022-2024 was
compared by difference-in-differences.

**Results:** The rebuilt benchmark tracked the published one ($\rho$=0.94). Early renewers' regional pull was 3.4
percentage points higher than stayers' (95% credible interval [CrI], 1.7 to 5.4; *P*<.001), but they also beat their
benchmarks by more (own-spending component, −2.1 points; 95% CrI, −3.8 to −0.5), and the total expected gain did not
differ (−0.5 points; 95% CrI, −2.0 to 0.8). Post hoc, early renewers' published 2022 benchmarks averaged 1.3% below
2021. Among 206 BASIC-track ACOs, a higher regional pull and BASIC level were associated with early renewal; 26 of all
27 BASIC-track early renewers moved to ENHANCED. Spending growth did not differ detectably (−0.4%; 95% CrI, −4.0% to
2.5%); a preregistered pre-trend condition failed.

**Conclusions:** Early renewers were already beating their benchmarks; for almost all, renewal was the route to a 75%
sharing rate, and the reset did not on average raise benchmarks. This fits the sharing-rate motive better, though the
design cannot separate the motives; the rules changed in 2024.

**Trial registration:** OSF Registries, doi:10.17605/OSF.IO/C53W9. Registered 26 October 2026.

**Keywords:** accountable care organizations; Medicare Shared Savings Program; benchmarks; alternative payment models;
value-based payment; preregistration; difference-in-differences; Bayesian analysis

# Background

In the Medicare Shared Savings Program (MSSP), an accountable care organization (ACO) shares in savings when the
spending of its assigned beneficiaries falls below a benchmark.[@cfr425] As of January 1, 2026, 511 ACOs served 12.6
million assigned Medicare beneficiaries, and ACOs earned \$4.1 billion in shared savings for 2024.[@sspfastfacts2026]
How benchmarks are set therefore determines both what Medicare pays and which provider organizations take part. At
the start of each agreement period the
benchmark is reset from the ACO's own spending in the 3 preceding years and adjusted part of the way toward the
spending of its region.[@cfr425601] Evaluations have found modest savings from the program, growing with tenure and
larger in physician-group ACOs.[@mcwilliams2016; @mcwilliams2018; @bond2025] Whether selection, of clinicians,
beneficiaries or whole ACOs, shapes those estimates has been examined with differing results: one analysis found no
evidence of favorable risk selection in the original program,[@mcwilliams2020] while another found that accounting
for the nonrandom exit of high-cost clinicians removed the estimated savings,[@markovitz2019exit] and risk-adjustment
rules may lead ACOs to drop high-risk beneficiaries.[@markovitz2019risk] This study examines a choice the rules added
in 2019, ending an agreement early to reset the benchmark sooner, which no peer-reviewed study has examined: under a
preregistered plan and with a validated reconstruction of the reset benchmark, it asks which ACOs used the option and
what their choice suggests about why.

Benchmarks shape the program through 2 channels. The first is the incentive to save. Rebasing to an ACO's own
recent spending weakens its incentive to save, and under earlier weights it rewarded higher spending just before a
new agreement;[@douven2015] this is the ratchet effect that arises whenever targets are set from past
performance.[@weitzman1980] In the MSSP, savings rates were 40% higher in years whose spending did not enter a future
benchmark.[@cappello2026]

The second channel is selection: benchmark rules change which ACOs join, stay and take on risk. ACOs' spending varies
widely relative to their regions even after risk adjustment, so moving benchmarks toward regional averages shifts them
unevenly.[@rose2016] After regional spending entered benchmarks in 2017, participation shifted toward
providers whose spending was low relative to their region,[@lyu2023] ACOs whose effective benchmarks fell became
more likely to leave,[@chen2025] ACOs with a positive regional adjustment were less likely to exit,[@cappello2026]
and bonuses rose for ACOs across the efficiency spectrum.[@srivastava2026] Survival in
the program has been associated with earning bonuses, higher benchmarks and one-sided risk,[@bleser2019] and larger
ACOs, those with supporting organizations and better performers were more likely to switch to two-sided
risk.[@zhu2023] The 2019 Pathways to Success rules, which shortened the time ACOs could stay in one-sided risk, were
followed by more exits than entries,[@ying2023] by ACO leaders reassessing potential savings against
losses,[@ying2024] and by departures with projected costs to Medicare.[@moloci2021] In a related model, most ACO
Investment Model ACOs exited once downside risk was required.[@trombley2022] This literature describes how benchmark
rules sort ACOs into joining, staying, leaving and taking on risk, and how rebasing weakens the incentive to save
within an agreement; it has not examined when ACOs choose to reset.

The 2019 rules also allowed an ACO to end its agreement early and begin a new one, which resets the benchmark
early.[@cfr425] For an ACO in the BASIC track, renewal was also the only way into the ENHANCED track before its
agreement ended, because the 2018 rule bars moving from BASIC to ENHANCED within an agreement period. CMS imposed that bar to guard
against selective entry into its highest-reward track by an ACO "very confident of its ability to generate savings"
against its current benchmark, and named early renewal, with its rebased benchmark, as the way to make the
move.[@frpathways] ENHANCED shares 75% of savings, against at most 50% in BASIC.[@cfr425] Of the 334 ACOs whose agreements began July 1,
2019 or January 1, 2020, 29 ended them early and began new agreements on January 1, 2022.[@dataacos] An industry
report found that ACOs rebasing early in 2022 had higher gross savings rates beforehand than ACOs that did not, and
that the earlier incumbents among them moved from BASIC to ENHANCED,[@milliman2024] and consulting analyses model the
choice for individual ACOs.[@milliman2025] These sources describe the early renewers but do not test why they renewed. To the author's knowledge, no
peer-reviewed study has asked whether ACOs used the option to time resets for a higher benchmark or to reach ENHANCED.
The question joins the 2 strands above, the incentive created by rebasing and selection by benchmark rules, and it
matters more now that the rules in force since 2024 make a reset cheaper for ACOs that have saved.[@cfr2024]

Two motives predict early renewal. Under a *reset motive*, an ACO renews because its new benchmark would be
higher. Under a *sharing-rate motive*, a BASIC-track ACO renews to reach ENHANCED. Whether a reset would raise the
benchmark is answered by the *total expected gain*, but its own-spending part is close to a restatement of the
savings rate. The registered plan therefore made primary the *regional pull*, how far an ACO's case-mix-adjusted
regional spending sat above its current benchmark: it has no term for the ACO's benchmark-year spending and shows
whether an ACO had room to gain on the regional side of a reset, which the savings rate does not capture. The
own-spending component and the total gain were read beside it. The study asked whether early renewers had more of
that room than ACOs that stayed, which characteristics were associated with early renewal, and whether early
renewers' spending growth differed afterward, as it might if a new benchmark or a higher sharing rate changed the
incentive to save. The analysis plan, hypotheses, decision rules and code were registered before any outcome value
was read.[@registration] These associations bear on the motives but cannot establish which one drove the choice.

# Methods

## Study Design and Preregistration

This is a preregistered retrospective cohort study of ACO-level public data, reported following the Strengthening
the Reporting of Observational Studies in Epidemiology (STROBE) guideline[@vonelm2007] (checklist in Additional file 1). The analysis plan and the code commit that implements it were registered on OSF (Open Science Framework) Registries on October 26, 2026,
13:22 UTC, with the plan's SHA-256 hash recorded.[@registration; @code] Before registration only the enrollment
files, the Centers for Medicare & Medicaid Services (CMS) data dictionaries, the regulation text and the column names (not the values) of the outcome files
were used. The enrollment files include each ACO's track and BASIC level, so the H3 prediction for the BASIC level
was made with those data available: it is preregistered but not blind to them. No savings rate, spending value,
benchmark or constructed variable was seen. The registry's own timestamp, rather than the repository's commit dates,
establishes that order. The code
also enforced it: every data file is hashed before it is read, and any file whose hash matches a performance-year
results file, a county spending file or the county assignment file could not be opened until the registration record
existed. The pipeline was written and tested on synthetic data with planted effects before registration. Analyses ran
in stages that each refused to start until the outputs they depend on existed: the power analysis was committed before
any confirmatory estimate, the robustness results (which depend only on validation and power) were committed before
the confirmatory results and read only together with them, and every results file was committed before its
estimates were read.

## Data Sources

Four CMS public use files were used, all aggregate at the ACO or county level:[@dataacos; @dataresults; @datacounty;
@dataassigned] MSSP ACO enrollment files for PY2016-PY2024, performance-year (PY) financial and quality results for
PY2016-PY2024 (PY2023 and PY2024 only for the spending analysis), county-level expenditure and risk-score data on
assignable beneficiaries for 2019-2021, and counts of ACO-assigned beneficiaries by county for 2021. The 40 files
downloaded on October 22, 2026, each recorded with its size, SHA-256 hash and URL, also include files kept from the
design stage that no analysis reads; an archived copy of the snapshot is on OSF.[@osfproject] Cells with counts of 1
to 10 are suppressed in these files.[@suppression]

## Population and Groups

The base population was the 334 ACOs whose PY2021 enrollment record showed an agreement start of July 1, 2019 (189
ACOs) or January 1, 2020 (145 ACOs). Both cohorts' agreements end December 31, 2024, so an ACO from either cohort with
a January 1, 2022 agreement in the PY2022 enrollment file had renewed early.[@cfr425] *Early renewers* (29 ACOs)
were compared with *stayers* (277 ACOs), those in the same agreement in PY2022; 42 stayers later renewed early into
2023 or 2024 agreements, so the comparison concerns the 2022 decision. The 28 ACOs absent from the PY2022 file (left
after PY2021) were described but entered no registered test (Figure 1). Of the 356 ACOs from these cohorts in the
PY2020 enrollment file, 22 were absent from the PY2021 file, and none had renewed into a 2021 agreement.

## Variables

### Expected Gain From a Reset

CMS does not publish what an early renewer's benchmark would have been had it not
renewed, nor a stayer's had it reset. Following 42 CFR 425.601 as in force on January 1, 2022,[@cfr425601] the
registered plan rebuilt it in 6 steps for each of the 4 enrollment types (end-stage renal disease [ESRD], disabled,
aged/dual eligible, aged/non-dual eligible): (1) the equally weighted mean of the ACO's per-capita spending in
PY2019-PY2021, restated to PY2021 case mix and trended to 2021 dollars with the national-regional growth blend; (2)
risk-standardized county spending averaged with weights equal to the ACO's assigned person-years by county in 2021
(the published proxy for the benchmark year's assignment) and adjusted to the ACO's case mix;[@specv10] (3) the
regional adjustment, $w \times (\text{regional} - \text{rebased})$, with the phase-in weight $w$ and the cap of
425.601; (4) the approximate new benchmark, combining types by the ACO's PY2021 person-year shares; and (5) the
expected gain, $100 \times$ (new $-$ current) / current, where the current benchmark is the PY2021 updated per-capita
benchmark. The gain splits into an *own-spending component* (rebased spending relative to the current benchmark,
which is close to a restatement of the savings rate) and a *regional component* (the adjustment). Writing the
adjustment out shows that, before capping,

$$\text{regional component} = w \times (\text{pull} - \text{own}),$$

so the regional component is also tied to past savings. Step (6) is the primary measure, the *regional pull*,

$$\text{regional pull} = 100 \times \frac{\sum_e s_e R_e - B}{B},$$

where $R_e$ is the case-mix-adjusted regional spending for enrollment type $e$, $s_e$ the ACO's share of
person-years of that type, and $B$ its current per-capita benchmark. All 4 are in percentage points of the current
benchmark. They use final PY2021 data, published after the 2022 renewal decision was made during 2021, so they are
ex post measures of what ACOs could anticipate from CMS's quarterly reports and their own earlier results.

### Validation Before Use

Several steps can only be approximated from public files. The plan therefore required the
rebuilt benchmark to be validated against the 2022 benchmarks CMS published for regular renewers (ACOs whose
scheduled agreements ended in 2021) before any expected-gain variable was estimated, with a pass rule of a Spearman
correlation of at least 0.80 and a median absolute percentage error of at most 5%, and a calibration step if the
slope of actual on rebuilt fell outside 0.9 to 1.1. Early renewers were excluded from the validation sample and the
2022 results file was filtered as it was loaded, so validation could not reveal their actual reset. A second check
compared the own-spending part with CMS's own benchmark-year spending for the same ACOs; its error SD set the
measurement-error SD used in the decision model.

### Other Variables

From the results files: the savings rate (CMS-reported savings as a share of the benchmark) in
PY2020 and PY2021, assigned beneficiaries, and log per-capita spending, PY2020-PY2024. From the enrollment files:
cohort, PY2021 track and BASIC level, revenue category, assignment method and agreement number. An ACO's PY2021
BASIC level reflects both the glide path's schedule and its own earlier choices: ACOs choose their entry level, can advance faster, and could pause the advance for 2021; ACOs experienced with performance-based risk could enter
only Level E or ENHANCED.[@cfr425600]

### Suppressed Values

Hidden cells needed for the expected gain were filled by registered rules in order: exact
recovery of a single hidden count from totals, the mean over years in which a value was shown, a regional ratio for
a type hidden in every year, and, for a hidden risk score, no restatement and the region's mean risk score. ACOs
still missing a variable were excluded from that analysis and counted; the plan required reporting as a limitation
any exclusion above 10% of either group.

## Hypotheses

The registered hypotheses were: *H2b (primary)*, early renewers had a larger regional pull than stayers; *H2a
(secondary)*, a larger own-spending component (close to H1 restated, so not counted as separate evidence); *H1
(descriptive)*, a difference in PY2020 savings rate, with no motive attributed to its sign; *H3*, among BASIC-track
ACOs, the probability of renewing early rises with the regional pull, the own-spending component and a higher BASIC
level; and *H4*, early renewal changed per-capita spending in PY2022-PY2024 (2-sided). H1 to H3 describe who chose
to reset and are associations. H4 concerns a bundled package (a new benchmark, for almost all a move to ENHANCED, and
new benchmark years) whose parts cannot be separated.

## Statistical Analysis

### Group Comparisons (H1, H2a, H2b)

The estimate was the difference in means, early renewers minus stayers, within
each cohort, averaged with weights proportional to the early renewers in each cohort. Its posterior was a Bayesian
bootstrap[@rubin1981] (10,000 draws of Dirichlet(1, ..., 1) weights within each cohort-by-group cell), reported as
the posterior mean, 95% equal-tailed credible interval (CrI) and posterior probability of a positive value. Significance
was by stratified permutation: labels were shuffled within cohort 10,000 times, and the 2-sided *P* value was
$(1 + \#\{|\hat\theta_\text{perm}| \ge |\hat\theta_\text{obs}|\}) / (1 + 10{,}000)$.[@phipson2010] When the *P* value
and the CrI disagree, both are reported and the disagreement noted.

### Decision Model (H3)

A Bayesian logistic regression of early renewal among PY2021 BASIC-track ACOs on the 3 core
predictors and 5 adjustment factors (cohort, log assigned beneficiaries, high revenue, prospective assignment, later
agreement) was fit in PyMC[@pymc2023] with the No-U-Turn sampler[@hoffman2014] (4 chains of 2,000 tuning and 2,000
retained draws, target acceptance 0.95). Continuous predictors were centered and divided by 2 SD[@gelman2008] and binary
predictors centered, so each coefficient is a log-odds difference per 2 SD or per category; coefficients had Normal(0,
1) priors. The own-spending component entered as a latent true value observed with normal error, with the error SD
fixed by the validation step. Convergence required $\hat{R} \le 1.01$, bulk and tail effective sample sizes of at
least 400 and no divergences,[@vehtari2021] with one registered rerun; a Firth penalized regression[@firth1993;
@firthmodels] would have decided H3 had the model not converged. Because shuffling labels in a multi-predictor model
tests the joint null, each core predictor was tested by direct simulation under the reduced model: the model without
that predictor was fit, 10,000 outcome vectors were simulated from its posterior, the full model was refit to each,
and the observed coefficient was compared with that null distribution. A fit with Student-t(3, 0, 2.5) priors, after
Gelman and colleagues,[@gelmanprior2008] was the registered sensitivity analysis, with any differing core conclusion to
be flagged.

### Spending After Renewal (H4)

For each ACO, $\Delta$ was the mean log per-capita spending over its included years
in PY2022-PY2024 minus the mean in PY2020-PY2021, and H4 applied the group-comparison estimator to $\Delta$, reported
as $100 \times (e^{\text{estimate}} - 1)$, the percent difference in spending growth. Log differences are also given in
log points (1 log point = 0.01 in log spending, about 1%). The comparison group was ACOs not yet renewed: a stayer's
years after it renewed into a 2023 or 2024 agreement were excluded, following the not-yet-treated design of Callaway
and Sant'Anna.[@callaway2021] With one pre-period change (PY2020 to PY2021, both affected by COVID-19) and about 29
treated ACOs, a nonsignificant pre-trend test is weak evidence of parallel trends,[@roth2022] so the plan replaced it
with an equivalence condition in the spirit of equivalence testing:[@lakens2017] H4 would be read as an effect only
if the larger absolute bound of the pre-trend CrI, scaled by the mean distance between period midpoints, was smaller
than the absolute H4 estimate. A trend-adjusted estimate (the pre-period slope carried forward, in the spirit of
Rambachan and Roth[@rambachan2023]) and risk-adjusted, balanced-panel, propensity-weighted[@rosenbaum1983] and
single-cohort estimates were reported beside it.

### Power

Minimum detectable effects (MDEs) at 80% power and 2-sided $\alpha$ = .05 for 29 vs 277 ACOs were
computed after registration and committed before any confirmatory estimate: from the cross-ACO SD of the savings rate
in PY2016-PY2018 (H1), the SD of each constructed variable among stayers, computed after validation (H2a, H2b), and
the SD of the pre-period spending change (H4). For H3, detection was simulated at a log-odds difference of 0.5.

### Decision Rules

Fixed in the plan before any result. For H2b, *P*<.05 with a positive difference was to be
reported as "early renewers' regions spent more relative to their current benchmarks, evidence for the reset motive
beyond past savings," *P*<.05 with a negative difference as evidence against it, and otherwise as no detectable
difference. H2a used the same wording; H3 predictors were supported, contradicted or undetermined by their
direct-simulation *P* values; and H4 was reported as no detectable difference, grew less or grew more, read as an
effect only if the equivalence condition held. No test here could rule the sharing-rate motive in or out. As
registered, there is one primary test, and the 3 H3 tests and the H4 test are not adjusted for multiplicity.

### Covariate-Adjusted Estimates, Conventional Methods, and Robustness

Reported beside the registered methods and not
used for decisions: covariate-adjusted estimates for H1, H2a and H2b from robust Bayesian linear regressions
(Student-t errors on the standardized variable, Normal(0, 1) priors) on early renewal and cohort, or cohort, track,
level and size; Welch *t* tests,[@welch1947] ordinary least squares with HC2 errors[@mackinnon1985] and
maximum-likelihood logistic regression in statsmodels;[@statsmodels2010] 2-way fixed effects with an event study and
errors clustered by ACO for H4; and the registered robustness checks: differences in medians, the January 1, 2020
cohort alone, PY2021 savings rates, the Firth model, benchmark years 2-3 only, no measurement-error model, complete
cases and unadjusted county spending. Variables were built in dbt[@dbt] on DuckDB;[@duckdb2019] the environment was
locked with uv;[@uv] Markov chain Monte Carlo diagnostics used ArviZ;[@arviz2019] every refit had its own seed from a fixed NumPy seed
sequence.[@numpy2020]

### Deviations

All 7 analysis stages ran with code identical to the registered commit. After the last stage the
lockfile took security updates to 2 packages (filelock and virtualenv); no result was produced with it, and it is
logged as the one deviation. One sentence of the plan's background is imprecise: it describes ENHANCED as sharing 75%
of savings and losses, whereas it shares 75% of savings and up to 75% of losses.

## Post Hoc Checks (Not Registered)

After all registered results had been read, and in response to critical review of the draft, 3 checks were added (eTable 13 in Additional file 2). They reuse the registered pipeline's tables and estimator,
change no registered file, and decide nothing. First, the validation was repeated on the change scale, the rebuilt
against the actual change from the PY2021 benchmark, for the same 101 regular renewers. Second, early renewers'
realized reset, their 2022 historical benchmark as CMS published it relative to their PY2021 benchmark, was compared
with the rebuilt gain, and their PY2021-to-PY2022 change in updated benchmark was compared with stayers' with the group-comparison estimator above. Third, the rank correlation of the regional pull
with the PY2020 and PY2021 savings rates and the own-spending component was computed, to ask whether the pull
restates past savings.

## Use of Large Language Models

Claude Code (Anthropic), a large language model tool, was used from October 2026. It proposed the topic and drafted
the analysis plan, offering alternatives from which the author chose; the author revised the plan and registered it.
Under the author's direction it drafted the analysis pipeline and its tests, first against synthetic data with
planted effects; the scripts that generate every table and figure from the committed results and that check every
number in the text against them; and most of the text, which the author revised. It ran the literature searches the
author specified and retrieved the metadata of references with a DOI from Crossref; the author checked the cited
claims against the sources. Separate instances of the same tool critically reviewed the plan, the code and the
manuscript, and the author decided which comments to act on. The author chose the research question, hypotheses,
decision rules and statistical approach, ran the analysis, verified every reported number against the results files
and takes full responsibility for the content. No image-generation tools were used; the figures are drawn by plotting
code from the results files.

# Results

## Validation and Sample

The rebuilt benchmark passed validation (eTable 1 in Additional file 2). For 101 of the 111 eligible regular renewers, it
had a Spearman correlation of 0.94 with the benchmark CMS published and a median absolute percentage error of 1.6%;
the slope of actual on rebuilt was 0.944, inside the registered range, so no calibration was applied. The
own-spending part agreed with CMS's benchmark-year spending (Spearman 0.95; median error 1.4%), and its error SD set
the measurement-error SD at 4.38 percentage points. That SD exceeds the own-spending component's spread among stayers
(SD 3.3). Under a classical error model it could not, so the validation errors are probably heavy-tailed (a normal
error with that SD would have a median absolute value near 3, against the 1.4% observed) or do not transfer exactly
to the study sample; a scale estimate from the median error (1.4826 × 1.4 ≈ 2.1) would be below the stayers' SD.
By the registered error model, the component is mostly noise at the level of one ACO; the savings
rates, which CMS reports directly, are the firmer evidence of how far ACOs were beating their benchmarks.

Early renewers were more often in the January 1, 2020 cohort and at BASIC's two-sided levels C to E in PY2021 than
stayers (Table 1); 16 of the 27 BASIC-track early renewers were at the highest level, E. Of those 27, 26 moved to
ENHANCED in their new agreements; stayers could not, because the rules bar that move within an agreement period. The expected-gain variables could not be built for
3 early renewers (10.3%) and 36 stayers (13.0%), both above the plan's 10% line. A diagnostic query run after the
results, outside the registered pipeline, found that in every one of these 39 ACOs CMS had suppressed the count of
assigned ESRD beneficiaries in every county of the 2021 assignment file, so the ESRD part of regional spending had no
county weights (for 15, the aged/dual counts were hidden too). The plan's fill rules cover hidden cells in the results
files, not fully hidden county weights, so these ACOs were excluded and counted, as registered. The same query showed
them to be smaller ACOs (median 6,702 and 8,578 assigned beneficiaries for excluded early renewers and stayers,
against 10,757 and 15,649 for those included). One early renewer and 3 stayers had hidden values filled by the
registered rules.

{{include tables/table1.md}}

![Figure 1. Flow of ACOs into each analysis. Counts are early renewers vs stayers. The reason for the expected-gain exclusions comes from a diagnostic query run after the results, outside the registered pipeline. ACO, accountable care organization; ESRD, end-stage renal disease; PY, performance year.](figures/figure1-flow.png){width=100%}

## Who Renewed Early

Relative to their current benchmarks, early renewers' case-mix-adjusted regional spending was 3.4 percentage points
higher than stayers' (95% CrI, 1.7 to 5.4; *P*<.001), above the MDE of 2.5 computed for 29 vs 277 ACOs, which is
slightly understated for the 26 vs 241 compared (Table 2 and Figure 2). By the registered rule, H2b was supported, which the plan worded as "evidence for the reset motive
beyond past savings." The decomposition shows that this wording overstates the result. Weighted by the phase-in
weight, the pull difference was 1.6 points (eTable 10), and the regional component differed by the same 1.6 points
partly because a lower own-spending component also raises it; the total expected gain did not differ. The pull
difference therefore indicates that early renewers were low-cost relative to their regions more than that they stood
to gain a higher benchmark. The pull is related to past savings without restating it: post hoc, its rank correlation
with the PY2020 savings rate was 0.45 among the 267 compared ACOs (eTable 13 in Additional file 2). At the median PY2021 benchmark of the study's ACOs, \$11,312 per beneficiary per year, the difference of 3.35
points is about \$379 per beneficiary-year of regional spending relative to the benchmark; the difference in the
regional component itself, what a reset would add, was 1.6 points, about \$176.

The own-spending component pointed the other way (−2.1 points; 95% CrI, −3.8 to −0.5; *P*=.003): early renewers'
recent spending was lower relative to their benchmarks, contrary to the reset motive by the rule's wording. Early
renewers also had higher savings rates in PY2020 (1.9 points; 95% CrI, 0.7 to 3.3) and PY2021 (1.6 points; 95% CrI,
0.2 to 3.1). The 2 parts of the gain offset: the regional component was larger for early renewers (1.6 points;
95% CrI, 0.9 to 2.2), the own-spending component smaller, and the total expected gain did not differ (−0.5 points;
95% CrI, −2.0 to 0.8; *P*=.33). In unweighted means the own-spending and regional parts summed to −5.3 + 3.7 = −1.6
points for early renewers and −3.2 + 2.2 = −1.0 for stayers: by the approximation, a reset would on average have
lowered both groups' benchmarks. Post hoc, CMS's published 2022 benchmarks bear this out for early renewers: their
reset historical benchmarks averaged 1.3% below their PY2021 benchmarks (median −1.5%; 66% of the 29 were lower), the
rebuilt gain had predicted −1.6 points on average against −1.4 realized for the 26 with both values, and their
updated benchmarks rose from PY2021 to PY2022 no more than stayers' (difference 0.0 points; 95% CrI, −2.0 to 2.2)
(eTable 13 in Additional file 2).

{{include tables/table2.md}}

![Figure 2. Early renewers minus stayers. A, Expected-gain variables, in percentage points of the current benchmark. B, Savings rates, in percentage points. Points are posterior means and lines 95% credible intervals from the Bayesian bootstrap.](figures/figure2-comparisons.png){width=100%}

## Decision Model

Among 206 BASIC-track ACOs (24 early renewers), early renewal was associated with a higher regional pull (log-odds
difference per 2 SD, 1.34; 95% CrI, 0.44 to 2.30; direct-simulation *P*=.002) and a higher BASIC level (log-odds
difference for levels C-E vs A-B, 1.34; 95% CrI, 0.38 to 2.31; *P*=.003); both predictions were supported (Table 3
and Figure 3). A log-odds difference of 1.34 multiplies the odds of renewing early by about 3.8. The own-spending
component was undetermined (−0.05; 95% CrI, −2.01 to 1.92; *P*=.19); its interval is the prior's 95% range,
because its measurement error exceeds its spread and the model could learn almost nothing about it. Without the
measurement-error layer it was −0.64 (95% CrI, −1.51 to 0.23). The model converged on its first fit (largest
$\hat{R}$ 1.001, no divergences), and the observed 24 early renewers fell inside the posterior predictive 95% range
of 14 to 37 (eTable 5 in Additional file 2). Under the Student-t prior, which converged on its registered rerun, the pull
(1.65; 95% CrI, 0.53 to 2.87) and BASIC-level (1.63; 95% CrI, 0.53 to 2.85) intervals also excluded zero, so no core
conclusion differs between priors. The power analysis gave detection rates of only 17% (pull) and 14% (BASIC level)
at a log-odds difference of 0.5, so estimates that pass the test are likely to overstate the true
effects;[@gelmancarlin2014] the directions are the result, and coefficients near 1.3 are probably too large.

{{include tables/table3.md}}

![Figure 3. Decision model of early renewal among BASIC-track ACOs (H3). Points are posterior means and lines 95% credible intervals; the shaded band is the Normal(0, 1) prior's central 95%. Bold labels mark the core predictors.](figures/figure3-decision-model.png){width=100%}

## Spending After Renewal

Spending growth from PY2020-PY2021 to PY2022-PY2024 did not differ detectably between 29 early renewers and 276
comparison ACOs not yet renewed (−0.4%; 95% CrI, −4.0% to 2.5%; *P*=.78; MDE 3.8 log points) (Figure 4; eTable 8 in Additional file 2). The pre-trend estimate was 0.7% (95% CrI, −2.3% to 4.9%; *P*=.58), not evidence against parallel trends, but
the equivalence condition did not hold: the scaled pre-trend bound, 2.41 years times 4.8 log points, was 11.5 log
points (about 12%), far above the absolute H4 estimate of 0.4 log points. The condition could have held only for an
estimate above about 12% in absolute value, 3 times the MDE, so with one pre-period it could not support reading an
estimate of plausible size as an effect, and a trend difference of the size the pre-period allows could hide an
effect in either direction. H4 is therefore reported as a difference in spending changes that cannot be told apart
from a continuation of a pre-period difference in trends. Under parallel trends, the interval rules out a drop in
spending growth of more than about 4% or a rise of more than about 2.5%; the trend-adjusted interval (−12.0% to
2.7%) is too wide to inform.

Attrition was uneven: by PY2024, 115 of 277 stayers (42%) had left the spending panel (72 left the program, 42 renewed
and 1 had no spending value), against 4 of 29 early renewers (14%) (eTable 9 in Additional file 2). The balanced panel of
ACOs with all 5 years gave −1.6% (95% CrI, −5.6% to 1.6%; *P*=.30).



![Figure 4. Spending after early renewal. A, Event study from the conventional 2-way fixed-effects model, in log points relative to PY2021, with 95% CIs clustered by ACO. B, The registered H4 estimate and the robustness and conventional estimates, as the percent difference in spending growth with 95% intervals (the propensity-weighted estimate has no interval); sample sizes are in eTable 8 in Additional file 2. TWFE, 2-way fixed effects.](figures/figure4-spending.png){width=100%}

## Robustness and Conventional Methods

Every registered verdict agreed with its conventional counterpart (eTable 7 in Additional file 2). For H2b, ordinary
least squares with HC2 errors gave 3.3 points (95% CI, 1.3 to 5.4; *P*=.001), and for H3 the maximum-likelihood
odds ratios were 4.0 (95% CI, 1.2 to 13.4) for the regional pull and 4.8 (95% CI, 1.5 to 15.6) for the BASIC level;
2-way fixed effects gave −1.5% (95% CI, −5.4% to 2.4%) for H4. H2b kept its direction in every robustness check
(eTable 3 in Additional file 2), but its size depended on the estimator: the difference in medians was 2.8 points, and the
robust (Student-t) regressions gave 2.1 (95% CrI, 0.5 to 3.8) with cohort and 2.2 (95% CrI, 0.7 to 3.8) with track,
level and size added, below the MDE of 2.5, so a few large values among early renewers carry part of the difference
in means; without the case-mix adjustment of regional spending the difference was 6.9. H2a and H1 kept their
direction but were weaker by medians (H2a, *P*=.09; H1, *P*=.06) and in the adjusted regressions, whose intervals
reached zero (H2a, −2.6 to 0.02; H1, −0.1 to 2.6). In H3 the BASIC-level interval stayed above zero in every check,
while the pull interval reached zero with the 2020 cohort alone (1.15; 95% CrI, −0.02 to 2.39) and with unadjusted
county spending (0.75; 95% CrI, −0.02 to 1.56) (eTable 4 in Additional file 2).

Among the exploratory analyses (eTables 10-12 in Additional file 2), the 28 ACOs that left after PY2021 had the lowest
PY2020 savings rates (mean 2.7 points, against 6.4 for early renewers and 4.6 for stayers) and, for the 20 with the
variable, a mean regional pull similar to early renewers' (4.8 vs 5.0; medians 2.0 vs 3.5) (Table 1). The 2 early
renewers already in ENHANCED, whose renewal could not raise the sharing rate, fell between the 26th and 68th
percentiles of stayers on every variable.

# Discussion

## Principal Findings

In this preregistered study of the 2019 and 2020 MSSP cohorts, the ACOs that ended their agreements early were
already beating their benchmarks by more than ACOs that stayed, had more room under their regions' spending, and,
in the BASIC track, were more often already bearing two-sided risk. For 26 of the 27 BASIC-track early renewers,
renewal was the move to ENHANCED's 75% sharing rate. By the study's approximation, a reset would not on average have
raised their benchmarks, because the regional gain and the own-spending loss roughly offset, and the benchmarks CMS
published for 2022, examined post hoc, agree. Spending growth in the 3 years after renewal did not differ detectably
from that of ACOs not yet renewed.

To the author's knowledge, this is the first peer-reviewed study of which ACOs used the early-renewal option. It adds
3 things. First, the intuitive account that ACOs renewed early to raise their benchmarks does not hold on average.
This rests on a secondary decomposition, built from data the ACOs did not yet have when they decided, and on the
benchmarks CMS later published, examined post hoc. Second, early renewers were sorted on the positions found for
joining and staying, room under their regions' spending and greater risk, which extends that literature to when ACOs
reset; the size of the regional difference depended on the estimator, and in the decision model its interval reached
zero in 2 robustness checks. Third, the study provides a public, validated reconstruction of the reset benchmark and
a preregistered, code-enforced analysis that can be rerun for later cohorts. Spending growth after renewal did not
differ detectably; under parallel trends, which the single pre-period could not establish, the interval rules out a
drop of more than about 4% or a rise of more than about 2.5%.

## Comparison With Prior Work

The primary result extends to a new decision the selection described in the Background: providers with low
spending for their region joining,[@lyu2023] ACOs whose benchmarks fell leaving,[@chen2025] and ACOs with a positive
regional adjustment about 70% less likely to exit.[@cappello2026] Here the choice is when to reset rather than whether to join or leave,
and early renewers had, on average, more room under their regions' spending, the position associated with joining and
staying. In a voluntary Medicare bundled-payment program, hospitals that could gain without changing their behavior
were more likely to join, which the authors called selection on levels;[@einav2022] early renewal shows selection on a
similar position, though the gain that most early renewers took appears to have been the sharing rate rather than a
higher benchmark. The industry report on the same cohort[@milliman2024] is
consistent with the higher prior savings rates and the BASIC-level association here. Beyond that report, this study rebuilt the reset benchmark and validated it
against CMS's, separated its own-spending and regional parts, modeled the decision within the BASIC track and followed
spending afterward, under a preregistered plan. The finding that early renewers were savers also fits reports that ACOs earning bonuses survived longer in the
program[@bleser2019] and, with borderline precision, that ACOs that had achieved savings were more likely to stay
after the 2019 rules.[@ying2023] The same success, however, meant that the own-spending part of a reset would
have cut their benchmarks.
That the size of the regional difference doubled without case-mix adjustment is consistent with evidence that
comparisons of ACOs with their regions depend heavily on risk adjustment.[@rose2016] The concern that rebasing rewards
higher spending before a new agreement[@douven2015] could be neither confirmed nor excluded here, and the costs to
Medicare of early renewal, which earlier work estimated for departures,[@moloci2021] were not estimated.

The association with a higher BASIC level bears on the sharing-rate motive at least as much as on the reset motive.
In these data renewing early and moving to ENHANCED were one choice: 26 of the 27 BASIC-track early renewers moved to ENHANCED, and the rules let no stayer do so. ACOs already bearing two-sided risk at Level E faced a short step to ENHANCED's 75%
sharing rate. Because ACOs partly choose their BASIC level, and ACOs experienced with performance-based risk could
enter only Level E or ENHANCED,[@cfr425600] the association may also reflect earlier risk experience or appetite rather
than only proximity to ENHANCED. A high regional pull is also a plausible reason to want the higher rate,
because an ACO with room under its region's spending may expect larger savings to share. The 2 early renewers already in ENHANCED, for whom only the reset could change, looked like typical stayers on every
variable. Taken together, with renewal and the move to ENHANCED one choice, the higher BASIC levels, a total
expected gain near zero and reset benchmarks that fell, the pattern fits the sharing-rate motive better than the
reset motive, and it is the trade CMS built into the rules: the move to ENHANCED required a reset.[@frpathways] That
is an interpretation, not a test; the design cannot separate the motives, and 2 ACOs already in ENHANCED are too few
to weigh.

## Implications

For program design, the results suggest that under the 2022 rules the use of the early-renewal option is consistent with
how CMS described it: a route to the ENHANCED track for ACOs already beating their benchmarks, at the price of a reset that did not on
average raise those benchmarks. They do not suggest that ACOs used the option to time resets for a higher benchmark.
The rules have since changed. For agreement periods beginning January 1, 2024 or later, an ACO that saved in its
benchmark years can receive a prior savings adjustment, and its benchmark gets the higher of that adjustment and the
regional adjustment; negative regional adjustments are partly offset; and the annual update blends in a fixed
projected trend.[@cfr2024] A reset now costs a saving ACO less, and saving ACOs are the ones that renewed early, so
the option may become more attractive to them and its cost to Medicare may change; its use is worth monitoring, and
the 34 stayers that renewed early into 2024 agreements are a first sample. Two questions remain open: what early
renewal cost Medicare, and how much of the choice reflected the sharing rate rather than the benchmark, which a
period in which ACOs could move to ENHANCED without resetting would separate.

## Strengths and Limitations

The study's strengths are in its design. The plan, decision rules and code were registered before any outcome data
were read, and the code enforced that order; the benchmark CMS does not publish was rebuilt from the regulation and
validated before use; the measurement error found in validation was carried into the decision model; and every
registered verdict agreed with its conventional frequentist counterpart. The code, data snapshot and results are
public, so every estimate can be rerun.

It also has limitations. First, the motives are bundled, and the regional pull, though it has no term for
benchmark-year spending, is not free of the ACO's own data: its benchmark was set from earlier spending, and regional
spending is adjusted with the ACO's own PY2021 risk scores, so a high pull partly measures how low-cost the ACO had
been relative to its region and may carry differences in coding intensity. The case-mix adjustment has no published
counterpart to validate it. Second, the expected gain is an approximation built from final PY2021 data that ACOs did
not have when they decided. Validation was on benchmark levels, which vary widely across ACOs, while the hypotheses
concern differences of a few points of the benchmark, so it says less about the accuracy of the gain than its
correlation suggests: repeated post hoc on the change scale, it gave a Spearman correlation of 0.61 and a median
absolute error of 1.7 points with little mean bias (−0.3), so group means are better supported than any one ACO's
value; the own-spending component's estimated error exceeds its spread, so the own-spending comparison and the total gain are weak evidence for
any single ACO, and the regional
part could not be checked. Third, with 29 early renewers, 24 in the decision model, the decision model was underpowered and its
supported coefficients are probably overestimates. ACOs under common ownership may decide together, and ACOs in the
same market share regional spending, so the effective sample is smaller than the ACO count, and the permutation tests,
which treat ACOs as exchangeable within cohort, may overstate precision. Fourth, exclusions exceeded the plan's 10% line in both groups,
and the excluded ACOs were smaller, so the expected-gain comparisons and the decision model
describe the larger ACOs. Fifth, the spending comparison had one COVID-19-affected
pre-period; uneven attrition left the comparison group's later years increasingly selected; the decision was made
during 2021, the last pre-period year and a benchmark year of the new agreement, while trade groups were asking CMS to allow
pre-pandemic benchmark years,[@aha2021] so anticipation and timing effects are possible; and
spending can move through changes in participant lists or assignment method (which changed at PY2022 for 2 of 29
early renewers and 14 of 277 stayers) rather than through behavior. Sixth, the base population required a PY2021 enrollment record (22 cohort ACOs left before then); stayers include
42 ACOs that renewed early in 2023 or 2024, so the comparisons and the decision model describe the 2022 decision rather than early renewal at any
time; and leavers, a third choice with a mean pull similar to early renewers', were set aside by
comparing early renewers only with stayers. Seventh, the results describe the rules for agreements beginning in 2022.

# Conclusions

In this cohort, early renewal looks less like timing a reset for a higher benchmark than like the price of reaching
ENHANCED's 75% sharing rate: the reset did not on average raise early renewers' benchmarks, and almost all moved to
ENHANCED. Spending growth afterward showed no detectable difference. These are associations, measured with public
data under a preregistered plan, and the design cannot separate the motives. They extend the evidence that benchmark
rules sort ACOs to the timing of resets and give a baseline for the rules in force since 2024.

# List of abbreviations

ACO: accountable care organization\
CFR: Code of Federal Regulations\
CMS: Centers for Medicare & Medicaid Services\
CrI: credible interval\
ESRD: end-stage renal disease\
MDE: minimum detectable effect\
MSSP: Medicare Shared Savings Program\
OSF: Open Science Framework\
PY: performance year

# Declarations

## Ethics approval and consent to participate

The study used only publicly available, aggregate data on organizations and counties published by CMS. It involved
no intervention or interaction with individuals and no identifiable private information, so it was not human subjects
research as defined by the US Federal Policy for the Protection of Human Subjects (45 CFR 46.102(e)(1)).[@cfr46102]
Ethics review was therefore not sought, and informed consent, privacy protections for participants and compensation
did not apply.

## Consent for publication

Not applicable.

## Availability of data and materials

The datasets generated and analyzed during the current study are available in the Zenodo repository[@paperrepo] and the
OSF project.[@osfproject] All data are public CMS files.[@dataacos; @dataresults; @datacounty; @dataassigned] The list of the 40 files
downloaded, with sizes, SHA-256 hashes and URLs, and a script that downloads and verifies them are in the study
repository;[@code] an archived copy of the snapshot and the results notebook exports are in the OSF
project.[@osfproject] The committed results files, from which every table and figure here is generated, are in the study repository and in this manuscript's repository, archived on Zenodo with the post hoc
scripts.[@paperrepo] The registered
analysis code (commit a4064f5), its tests and step-by-step instructions to rerun and adapt the analysis are in the study repository.[@code] A longer account
of the study for a general audience was published online.[@post]

## Competing interests

STH is employed as a data scientist at Indiana University Health. This study was conducted independently of that
employment, using only public data, and Indiana University Health had no role in its design, analysis,
interpretation or reporting. The views expressed are the author's own and do not represent the official positions of
Indiana University Health. The author declares no other competing interests.

## Funding

This work received no funding.

## Authors' contributions

STH: conceptualization, data curation, formal analysis, investigation, methodology, software, validation,
visualization, writing (original draft) and writing (review and editing). STH read and approved the final manuscript
and is accountable for all aspects of the work.

## Acknowledgements

Not applicable.

# Additional files

**Additional file 1** (.docx). STROBE checklist. Where each item of the STROBE statement for cohort studies is reported.

**Additional file 2** (.docx). eTables and eMethods. Registration record and deviations, validation, power, robustness,
conventional methods, exploratory analyses and post hoc checks (eTables 1-13).

# References

```{=latex}
\begingroup\raggedright
```

::: {#refs}
:::

```{=latex}
\endgroup
```

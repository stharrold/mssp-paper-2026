# Critical assessment: "Early renewal ... in the Medicare Shared Savings Program: a preregistered retrospective cohort study"

- **Assessed:** `paper.md`, `supplement.md`, `strobe.md`, `tables/`, `figures/` (all 4 viewed), `data/` (results, post hoc, README, allowlist), `posthoc/`, `research/README.md`, `metadata.yaml`, in `mssp-paper-2026` at commit `f0a3d5d` (branch `bmc-hsr-submission`, clean). Sibling study folder `stharrold.github.io/analysis/mssp-benchmark-ratchet/`: `PREREGISTRATION.md`, `REGISTRATION.md`, `DEVIATIONS.md`, `DESIGN-NOTES.md`, `README.md`, `research/README.md`, every module in `ratchet/` except `synthetic.py`, and the dbt models that build the groups, the expected gain, the validation table and the H4 panel.
- **Date:** 2026-11-10 (UTC).
- **Written by:** an AI agent (Claude, model Fable), acting as a peer reviewer and a statistical reviewer together, without access to prior reviews.
- **Independence:** I did not open `reviews/`, `references/AUDIT.md`, `references/audit/`, `BUILD-NOTES.md`, the private repository, or git history. Three things reached me without my seeking them: the session context showed five commit subject lines automatically; a line count (`wc -l`) and a directory listing touched `BUILD-NOTES.md` by name and size only; and `README.md`, `CLAUDE.md` and the post hoc scripts' docstrings mention that earlier critical reads and a reference audit exist, without their content.
- **Line numbers** refer to `paper.md` at the commit above.

## Overall verdict

**Recommendation: major revision. Confidence: moderately high** (high on the statistical points I recomputed, moderate on the regulatory points I reasoned from the rule text).

The study is unusually transparent and its descriptive facts are sound: I reproduced the group counts, the H4 estimate and the attrition table from the raw CMS files, and every number in the prose traces to a committed result. The weakness is the distance between what was registered and tested and what the abstract and Conclusions say. The registered primary test came out "supported" under a rule that words it as evidence *for* the reset motive, and the secondary test came out "contradicted", which the same rule words as contrary to it. The paper resolves that split in favour of the sharing-rate motive, which the plan says no test can address, using a fact known before registration (26 of 27 moved to ENHANCED), a descriptive decomposition and a post hoc check whose interval includes zero. That reading is plausible, and two checks I ran support it, but it is interpretation carried by the word "preregistered", and the industry report the paper cites had published its descriptive core in 2024. Separately, the registered spending estimator has an upward bias I could verify, the validation rule is passed by a no-change forecast, and the primary construct is not shown to be distinct from agreement history and past savings. None of this needs new data; most of it needs different claims.

## Major concerns (ranked)

### 1. The headline conclusion is not what the registered tests delivered, and the abstract does not say so

**Where:** Abstract Results and Conclusions (l.22-32); Results l.342-347, l.357-363; Discussion l.438-441, l.444-446, l.479-483; Conclusions l.535-537; title in `metadata.yaml` and `strobe.md`/`supplement.md`.

**What is wrong.** Plan section 7 fixed the readings in advance. Rule 1 (primary, H2b): *P*<.05 and positive is "evidence for the reset motive beyond past savings"; the result was *P*<.001 and positive. Rule 2 (secondary, H2a) uses the same wording: the result, −2.1 with *P*=.003, is "contrary to the reset motive", with the plan's caveat that H2a is close to H1 restated and "not counted as separate evidence". Rule 8 adds "No test here can rule the sharing-rate motive in or out." So the two registered verdicts split, and the plan gives no rule for weighing them. The body reports both honestly (l.342-343, l.352-353) and then argues that the primary wording overstates. The abstract states neither verdict; it reports the two differences and moves to "This fits the sharing-rate motive better". A reader of the abstract cannot tell that the primary test, read by its own rule, supports the motive the paper argues against, or that the tie was broken by judgement after the results.

**What the conclusion actually rests on** (verified against the files):

| Support | Status | Problem |
|---|---|---|
| Own-spending component −2.1 (−3.8 to −0.5), "contradicted" | Registered, secondary | The one confirmatory result on the paper's side. The plan itself discounts it as a restatement of the savings rate, and the industry report had shown higher prior savings for this cohort (concern 4). |
| 26 of 27 BASIC early renewers moved to ENHANCED | Enrollment data | Known before registration: `DESIGN-NOTES.md` 4.2 ("28 of them into ENHANCED") and plan 1.4. It is an input to the design, not a finding of it. |
| Total expected gain −0.5 (95% CrI −2.0 to 0.8) | Registered as descriptive, no decision rule | Measurement error in the own-spending part adds noise, not bias, to a difference in means (plan 5.2), and that noise is inside the interval; the post hoc mean error for early renewers is small (−0.2). The limits are its status and its reach: it bounds the gain *relative to stayers* at +0.8 and says nothing about expectations at the time of the decision. |
| Realized reset "averaged 1.3% below" (l.360) | Post hoc, no interval given | From the raw files I get mean −1.25, SD 5.56, n=29: a *t* interval of **−3.4 to +0.9**, range −12.5 to +13.3. Not distinguishable from zero; 34% rose. Regular renewers also fell on average (−0.6), so a small average fall is not specific to early renewers. |
| Updated benchmarks "rose ... no more than stayers'" (l.362) | Post hoc | 0.0 (95% CrI **−2.0 to 2.2**). The interval contains the 1.6-point regional gain the paper says a reset would add. This is "no difference" read from a wide interval. |

**Language that claims more than this supports:** "the reset did not on average raise benchmarks" (abstract l.31, Conclusions l.536) stated flat; "bear this out" (l.359); "agree" (l.441); "does not hold on average" (l.444); "reset benchmarks that fell" (l.480), which the −3.4 to +0.9 interval does not support. The title's purpose clause, "to reset benchmarks", asserts the motive the paper argues against.

**What I found in the paper's favour.** (a) By 42 CFR 425.600(d), a low-revenue ACO experienced with risk could renew into BASIC Level E; only high-revenue experienced ACOs were confined to ENHANCED. From the enrollment files, 23 of the 27 BASIC early renewers were low revenue by the PY2021 flag and 22 of those 23 entered ENHANCED (by the PY2022 flag, 21 of 22; one ACO changed category). So for most, ENHANCED was a choice, not a rule. The paper does not report this and should. (b) The savings rate rose from PY2021 to PY2022 by 0.9 points for early renewers and 0.4 for stayers (within-cohort difference 0.5, Welch SE about 0.75): no sign that the reset made their targets harder.

**Fix.** State both registered verdicts and their registered wording in the abstract, then say how the author weighs them and why. Label every element of the sharing-rate argument by status (known before registration, registered descriptive, post hoc). Give intervals for the realized reset. Replace "did not raise" with "no detectable change (interval −X to +Y)". Drop "to reset benchmarks" from the title. Add the revenue-status tabulation.

### 2. The registered spending estimator (H4) is biased upward by about 1.2 log points, and "rules out a drop of more than about 4%" does not hold

**Where:** Abstract l.27-28; Methods l.234-244; Results l.391-400; Discussion l.451-452; eTable 8; `ratchet/did.py` `deltas()`.

**What is wrong (verified).** Each ACO's outcome is the mean of log spending over *whichever* post years it has, minus its pre-period mean. Spending rises every year, and the groups differ in which years they keep: early renewers contribute 29/28/25 ACOs in PY2022/23/24, comparison ACOs 276/222/162. The mean distance between period midpoints is 2.41 years for early renewers and 2.20 for the comparison group. With growth of about 6-7% a year in 2023 and 2024, that gap alone adds roughly +1.2 log points to the early-minus-comparison difference under the null.

I rebuilt the panel from the CMS files and reproduced the committed estimate exactly (−0.003808; permutation *P*=.78 in my run, as in the paper). Aligning by year instead (each post year against the pre-period mean, among ACOs present that year, weighted by early renewers present) gives:

| PY2022 | PY2023 | PY2024 | Year-aligned average |
|---:|---:|---:|---:|
| −0.1 | −2.2 | −2.8 log points | **−1.6%** (95% interval −6.0% to 1.4%; permutation *P*=.26) |

The interval is a weighted bootstrap within cohort-by-group cells (4,000 draws) and the *P* value a stratified permutation (5,000 shuffles), both mine and unregistered. The verdict does not change: no detectable difference. The point estimate and the lower bound do. The year-aligned figure matches the paper's balanced panel (−1.6%) and two-way fixed effects (−1.5%), which avoid the composition problem. The three full-sample estimates built on the collapsed change (registered −0.4%, propensity-weighted −0.5%, risk-adjusted +0.3%) sit near zero. The paper reports both sets without naming why they differ.

**Consequences for the prose.**
- "Under parallel trends, the interval rules out a drop in spending growth of more than about 4%" (l.398-400, l.451-452) uses the biased estimator's interval. The paper's other intervals reach −5.4% (TWFE), −5.6% (balanced) and −8.3% (2020 cohort); mine reaches −6.0%.
- `did.json` holds a risk-adjusted TWFE event study that appears in no table: PY2024 −3.2 log points (95% CI −6.5 to 0.1; *P*=.057), pooled −1.3%. It should be reported, since the unadjusted event study is.
- The H4 MDE of 3.8 log points uses the SD of the one-year pre-period change. The realized interval (−4.1 to 2.5 log points) implies an SE near 1.7 and an MDE near 4.7.
- "A preregistered pre-trend condition failed" (abstract l.28) reads as evidence against parallel trends. It is not: the pre-trend estimate was 0.7% (*P*=.58). The condition was unsatisfiable. With the pre-trend interval's half-width of 3.6 log points and 2.41 years, it could hold only for |H4| above about 8.6 log points even if the pre-trend were exactly zero, and this was knowable from the power stage (SD 6.9 gives about 6.6). The body says something close (l.394-396); the abstract should.
- "following the not-yet-treated design of Callaway and Sant'Anna" (l.238) overstates: the code collapses to one change per ACO and censors years; it estimates no group-time effects.
- Mean reversion is not discussed in the direction the data now imply. The plan expected renewal after *high* spending; early renewers turned out to be high savers, so reversion would push their spending up and mask a decrease.

**Fix.** Keep the registered estimate as registered, state the composition bias as a limitation of it, and report the year-aligned and TWFE estimates beside it in the abstract. Delete both "rules out" sentences or restate them with the widest sensitivity interval. Reword the abstract's "failed".

### 3. The validation does not validate what the hypotheses use, and a no-change forecast passes the registered rule

**Where:** Abstract l.17, l.22; Methods l.170-177; Results l.311-320; Limitations l.511-518; eTable 1, eTable 13.

**What is wrong.** The abstract says the benchmark was "validated" and "tracked the published one (ρ=0.94)". That correlation is on benchmark *levels*, which differ across ACOs by thousands of dollars. I tested the trivial predictor "new benchmark = current PY2021 benchmark" on the 111 regular renewers:

| Predictor | Spearman | Median abs. % error | Slope | Registered rule (≥0.80, ≤5%) |
|---|---:|---:|---:|---|
| No change at all | 0.90 | 3.5 | 0.955 | **Passes, no calibration** |
| Rebuilt (paper, n=101) | 0.94 | 1.6 | 0.944 | Passes |

The two rows are not like for like: mine has all 111 eligible ACOs, the paper's the 101 with a rebuilt value. The rebuilt benchmark is clearly better than no change (error roughly halved), but the rule that licensed its use did not discriminate between them. On the scale the hypotheses use, the paper's own post hoc numbers are: Spearman 0.61, error SD 4.37 against a rebuilt-change SD of 3.32 and an actual-change SD of 5.29. The RMSE falls from about 5.3 (no-change forecast) to 4.4.

Two further gaps:
- **The primary measure is unvalidated.** The regional pull has no published counterpart (l.510-511, l.517-518). The paper says so in Limitations; the abstract's "validated" does not carry the caveat.
- **Wrong phase-in step.** By `phase_in.sql` every study ACO is at step 2 or later (any agreement from July 2019 counts), while 62 of the 101 validation ACOs are at step 1. The relevant row of eTable 1 is the step-2 row (n=39), which looks better (error 0.9%, slope 1.02) and should be the one cited.

**Fix.** In the abstract, give the change-scale figure (0.61) beside or instead of 0.94, and say the pull itself could not be validated. Report the no-change comparison. State that the registered rule was lenient.

### 4. Novelty and prior literature: the descriptive core was already published, the search postdated the results, and an earlier wave of early renewal is missing

**Where:** Abstract l.11-12; Background l.51-54, l.81-84; Discussion l.443, l.462-463; `research/README.md` in both repositories.

**What I checked.** I read the cited industry report (Milliman, April 2024) in full text. It states that 29 ACOs already in Pathways "elected to rebase early" in 2022, "with 26 of the early renewals involving a shift from a Basic track to Enhanced (two were Enhanced to Enhanced, and the other was Basic B to Basic E)". It names the motives: moving "up the risk pathway sooner (in the case of favorable performance)" or updating benchmarks "(in the case of adverse performance) and risk score growth". For the 11 pre-Pathways incumbents among the 29, it notes that because ENHANCED pays up to 75%, their net savings rose "due to this decision". It tabulates higher prior gross savings for the 2022 early rebasers.

**What is wrong.**
- The paper's description of that report (l.81-83: higher prior savings, and "the earlier incumbents among them moved from BASIC to ENHANCED"; "Neither tests why ACOs renewed") is accurate but incomplete. The abstract's headline facts and the sharing-rate reading are in the report. What the paper adds is the regional measure, the decomposition, the realized benchmarks and the spending comparison; the contributions paragraph (l.443-452) should claim those and credit the rest.
- **The 2019-2020 wave is absent.** The same report describes 23 ACOs that renewed early into July 2019 or January 2020 agreements; for the 19 it tabulates, prior savings were *poor* (0.2-1.0% in 2017-2019 against 2.0-4.0% for regular renewers). That is the reset-after-adverse-performance pattern, in the wave just before this one, and it bears directly on the hypothesis and on generalisability. The paper presents early renewal as "a choice the rules added in 2019 ... which no peer-reviewed study has examined" without saying it had been used before the study window, by ACOs that look like the opposite of this sample. Some of them are inside the study population.
- **Timing of the literature search (verified from the READMEs).** The related-work searches ran on 2026-10-27 from 16:22 UTC, after registration (10-26 13:22 UTC) and after the last results file (10-27 07:13 UTC); the report's access date is 10-28. So H2a predicted a *larger* own-spending component (worse performance) for early renewers when published figures for this exact cohort already showed the reverse. The "contradicted" verdict is partly a rediscovery. The manuscript does not disclose that the literature was reviewed after the results.
- **Missing policy context.** The CY2027 Physician Fee Schedule proposed rule (CMS fact sheet, 14 July 2026) says ENHANCED ACOs with spending below their region "are receiving both a higher shared savings rate and larger positive regional adjustment on average", which "may incentivize selection into the ENHANCED track", and proposes cutting the ENHANCED positive regional weight from 50% to 35%, raising the Level E share to 60% and enlarging the prior savings adjustment against the "ratchet effect". This is CMS describing the paper's H2b pattern. It is not cited; a final rule may have followed.

**On the novelty sentence itself:** two web searches of mine found no peer-reviewed study of early renewal, so "no peer-reviewed study" survives as worded. It is the framing around it that needs correcting.

**Fix.** Describe the report fully, including its stated motives and the 2019-2020 wave. Disclose when the literature was searched. Cite the 2026 proposed rule and check for the final rule. Narrow the "first" claim to what is new.

### 5. The regional pull is not shown to be distinct from agreement history and past savings

**Where:** Background l.90-95; Methods l.159-166; Results l.340-350, l.371-376; Limitations l.507-511.

**What is wrong.**
- **Construct.** Pull = (regional spending − current benchmark) / current benchmark. The current benchmark was built from the ACO's own earlier spending plus an earlier regional adjustment whose weight depends on agreement history. So the pull is roughly the part of the ACO's gap to its region that earlier agreements had not yet blended in. The Limitations concede the first half (l.507-510). The Background's "it has no term for the ACO's benchmark-year spending" (l.92-93) is not exact for the January 2020 cohort, whose current benchmark years (2017-2019) share 2019 with the reset's (2019-2021); that cohort holds 18 of the 29 early renewers. *(Inferred from the rule's benchmark-year definition, not recomputed.)*
- **Confounding by tenure in H2b.** *Verified:* early renewers were far more often in their first agreement, 12 of 29 (41%) against 52 of 277 stayers (19%); third agreement 21% against 44%. *Inferred:* ACOs with less agreement history have had less regional blending, so a larger pull is partly mechanical. H2b adjusts for cohort only; its "adjusted" regressions add track, level and size, not agreement number or phase-in step. H3 does carry a binary "later agreement" adjuster and the pull holds there (1.34), so the gap is in the primary test, not the decision model. Table 1 shows none of these characteristics (the STROBE checklist, item 14a, admits the adjusters are untabulated).
- **Never adjusted for savings.** In the registered H3 model the own-spending coefficient equals its prior (−0.05; −2.01 to 1.92), so the pull coefficient is not conditioned on past performance at all. The power stage had already shown 0% detection for that predictor before the confirmatory run. The only evidence that the pull is not past savings by another name is a post hoc rank correlation of 0.45 with the PY2020 savings rate.
- **Fragility the paper reports but the abstract does not:** robust regressions give 2.1-2.2 against 3.4; the case-mix adjustment moves the estimate from 6.9 to 3.4, so coding intensity is in play; in H3 the pull interval reaches zero in 2 checks.

**Fix.** Add (labelled post hoc) H2b adjusted for PY2020 savings rate, agreement number and phase-in step, and H3 with the CMS-reported savings rate in place of the inert own-spending term. Add agreement number, revenue category, assignment method and size to Table 1. Correct l.92-93 for the 2020 cohort.

## Moderate concerns

**6. Only two motives are considered (l.88-98; abstract l.12-13).** Plan 1.4 itself names a third element of the package: which years become benchmark years and when the next rebase falls. Others follow from the rules: a five-year lock on the new benchmark, a fresh baseline for the cap on risk-score growth (the industry report lists "risk score growth" as a reason), a higher phase-in weight, and the chance to change the participant list. "Two motives predict early renewal" should become "at least two", and the Discussion should say which others the data cannot address.

**7. Registration claims are stronger than what the repositories can show.**
- "The plan and code were registered before outcome data were read" (abstract l.16) and "No savings rate ... was seen" (l.110) are the author's attestation. The 40 files were on disk from 22 October (file times in the cache), four days before registration.
- "The code also enforced it ... could not be opened until the registration record existed" (l.111-114, l.502; supplement l.63-66). The lock in `ratchet/snapshot.py` is the existence of a local `REGISTRATION.md`; it guards the pipeline against accident and cannot show that the files were not opened another way. Stage order is likewise enforced by file existence only (study README: "Stages check only that those files exist").
- `robustness.json` (started 14:10 UTC, 26 October) held near-copies of the primary result (2020-cohort H2b, medians, Firth H3 with *P* values) about 17 hours before the confirmatory file finished. "Read only together with them" cannot be verified. The plan was frozen by then, so the practical risk is small; say it is an attestation.
- What I could confirm: the OSF API gives `date_registered` 2026-10-26T13:22:16Z, public, not withdrawn; the `generated` stamps in the seven results files are consistent with the stated order.
- The pace should be stated plainly for readers: design 22 October, registration 26 October, results 27 October, first submission 27 October.

**8. Small-sample inference is presented with more confidence than the cells allow.**
- The Bayesian-bootstrap interval for H2b (1.7 to 5.4) is narrower and sits higher than the Welch (1.1 to 5.3) and HC2 (1.3 to 5.4) intervals. The treated cells hold about 10 and 16 ACOs; the Bayesian bootstrap is in effect a percentile bootstrap, cannot place mass beyond the observed values, and yields "Pr(>0) >0.999" from 26 observations.
- Decisions are made by permutation *P* values while estimates are labelled Bayesian. A health services reader gains little from the hybrid; say that the intervals are bootstrap-type and give the HC2 interval beside the primary result.
- Dependence among ACOs (common ownership, shared markets) is acknowledged (l.519-521) but untested; a sensitivity analysis clustering by state or parent organisation is feasible.

**9. H3 is thin.** 24 events, 8 coefficients and a latent layer; Normal(0, 1) priors do visible work. The convergence check covers coefficients and intercept only, not the latent own-spending parameters (`decision.convergence`). Table 3 prints *P*=.19 and "Undetermined" for a coefficient the data cannot inform. The BASIC-level prediction was not blind (disclosed, l.108-109), and level partly encodes "experienced with risk", which the rules tie to the options available at renewal. The main text cites 17% and 14% detection but omits the 0% for own spending (eTable 2). **Fix:** in Table 3 replace the own-spending *P* value and verdict with "not identified (posterior equals prior)" and say so in the abstract-level summary of H3; report R-hat and effective sample size for the latent scale and mean; present the model without the measurement-error layer (eTable 4, item 7) beside the registered one in the main table, since it is the only version in which the pull is conditioned on own spending; add the 0% to the sentence at l.381-383; describe the BASIC-level result as an association with a level that also determines renewal options.

**10. Thirteen percent of the sample is lost to one suppressed input.** All 39 exclusions arise because county counts of assigned ESRD beneficiaries were hidden (l.325-329). ESRD is a median 0.6% of assigned person-years among the study's ACOs (my calculation from the PY2021 results file). A sensitivity analysis that weights ESRD regional spending by total person-years, or drops the ESRD term for those ACOs, would retain them. The excluded ACOs are smaller, and H3 loses 30 of 236.

**11. Reported numbers without a script, and computed results without a report.**
- `data/number-allowlist.tsv` attributes several reported numbers to a "diagnostic query after the results, outside the registered pipeline" or to a hand count: the ESRD finding and its four medians, the count of 15, the 356/22 recount, the $11,312 median. I found no script for them in the folders I read; I did not search either repository exhaustively. If none exists, "3 checks were added" (l.285) and "every estimate can be rerun" (l.505) understate the unscripted work.
- In the results but unreported: the risk-adjusted TWFE (concern 2). Registered to be reported but absent: H3 median interval widths (plan section 6) and the SD-unit coefficients of the 5.3 regressions.

**12. MDE is used as a yardstick for observed effects.** "Above the MDE of 2.5" (l.341) and "below the MDE of 2.5" (l.418) compare estimates with a threshold that describes the design, and the H2 MDEs use an SD computed from the constructed variables after registration. Report the MDE as design information only.

**13. Generalisability is one sentence (l.531).** The sample is one application cycle, the first after a year with no new agreements, in pandemic years, with 29 ACOs. Since 2024 ENHANCED is optional, the prior savings adjustment exists and negative regional adjustments are removed; the 2026 proposals would change the ENHANCED regional weight again. The contrast with the 2019-2020 wave (concern 4) shows the composition of early renewers is not stable. **Fix:** give generalisability its own paragraph that (a) says the estimates describe 29 ACOs in one cycle and are not a property of early renewal in general, (b) contrasts the 2019-2020 wave, (c) lists which findings the 2024 rules could reverse (a reset now costs a saver less, and ENHANCED no longer requires one), and (d) drops "give a baseline for the rules in force since 2024" (l.539) unless the 34 later renewers are actually analysed; a descriptive table of those 34 and of the 8 who renewed into 2023 would be a cheap out-of-sample look.

**14. Multiplicity: not a threat to the registered verdicts, but the unregistered forks are uncounted.** The paper leaves the primary test, the 3 H3 tests and H4 unadjusted (l.260-261). The supported or contradicted *P* values are .0009 (H2b), .002 and .003 (H3 pull and BASIC level) and .003 (H2a); all survive a Bonferroni or Holm correction over those 5 or 6 tests (threshold .008 to .01). So the verdicts stand, and the paper could say so in one sentence instead of only declaring no adjustment. The real multiplicity is elsewhere: two descriptive rows in Table 2, 9 robustness items, 4 exploratory families and 3 post hoc checks, from which the Discussion selects the total gain and the realized reset to carry the conclusion. No correction fixes that; labelling does (concern 1).

**15. The language-model disclosure is fuller than most, with three gaps.** Against Springer Nature's policy (use documented in Methods, no authorship for the tool, no generated images, author accountable) it complies: it is in Methods (l.293-305), itemised, and repeated in the figure legends. What the repositories show is consistent with it (agent guidance in `CLAUDE.md`, searches run through an agent skill, generated tables and checks). The gaps:
- **Scope of the human check on sources.** "The author checked the cited claims against the sources" (l.300-301), while `research/README.md` says each paper "is described in the manuscript only as its abstract supports", with full texts for two research letters. Say which references were read in full. (A reference audit exists; I did not read it.)
- **Timing.** The disclosure does not say that the searches, and so the framing against prior work, came after the results (concern 4).
- **Contribution roles.** The CRediT line (l.590-592) assigns software, formal analysis and original draft to the author alone, while Methods says the tool drafted the pipeline and most of the text. Cross-reference the two so they do not read as inconsistent. Since the tool also "proposed the topic" and drafted the plan, a reviewer will ask what the author verified independently; "verified every reported number" (l.303) is done by a script the tool drafted, and a sentence on any manual check would help.

## Minor concerns

- **Abstract Ns (l.17-18):** "29 ACOs ... were compared with 277 stayers on the regional pull". The pull comparison is 26 vs 241 (Table 2, Figure 2).
- **Abstract l.22:** "ρ" is not identified as Spearman.
- **l.602-603:** "eTables 1-13", but the supplement has eTable 14.
- **eTable 13:** the caption promises checks "of the regional pull against past savings"; the table has two rows and those correlations appear only in the note.
- **"Trial registration" (l.34)** labels an observational registration made after the data existed; "Registration" with "data existed at registration" is more accurate if the journal allows.
- **eTable 7:** agreement of verdicts between two analyses of the same 267 ACOs is weak corroboration; the Strengths sentence (l.503-504) leans on it.
- **STROBE:** item 19 asks for direction and magnitude of bias; the Limitations give direction for almost none.
- **l.238-243:** one 90-word sentence carries the estimator, the citation and the equivalence rule; split it.
- **Keywords:** "Bayesian analysis" oversells what is mostly resampling.

## Strengths

- A public, time-stamped plan with decision rules written before the results, and a manuscript that reports a verdict it then disowns rather than hiding it.
- Every table and figure generated from committed results; `check_numbers.py` passes (26 estimate-interval triples, 32 interval pairs).
- Results that reproduce: I matched the group counts, the H4 estimate to six decimals and the attrition table from raw files.
- Candid limitations on measurement error, type M error in H3, exclusions and the single pre-period.
- Code that matches its description for the Bayesian bootstrap, the permutation *P* value, the H3 priors and sampler settings, the direct-simulation test, the Firth model and the TWFE specification.
- A specific, itemised statement of what the language model did.

## What was verified, and how

| Check | Method | Result |
|---|---|---|
| Prose numbers | `python3 scripts/check_numbers.py` | Pass |
| Tables vs JSON | Read `confirm`, `did`, `conventional`, `robustness`, `exploratory`, `power`, `validation`, post hoc JSON against Tables 1-3 and eTables | Consistent, including the mixed savings-rate units (PY2020 fraction, PY2021 percent) |
| Group counts 29/277/28 | Stdlib Python on cached enrollment files | Match |
| H4 estimate and attrition | Rebuilt panel from raw files | −0.003808, exact; 29/28/25 and 276/222/162 |
| Year-aligned H4 | Same panel; weighted bootstrap and stratified permutation of my own | −1.6% (−6.0% to 1.4%; *P*=.26) (concern 2) |
| Trivial validation predictor | Raw PY2021/PY2022 results, n=111 | Passes the registered rule (concern 3) |
| Realized reset interval | Raw files, n=29 | −1.25 (−3.4 to 0.9) |
| Revenue status of early renewers | Enrollment files | 23 of 27 low revenue (PY2021 flag); 22 of 23 to ENHANCED |
| ESRD share of person-years | PY2021 results file | Median 0.6% |
| Multiplicity | Bonferroni and Holm on the registered *P* values | All verdicts survive |
| Agreement number | Enrollment files | 41% vs 19% first agreement |
| Savings-rate change 2021-22 | Raw files | +0.9 vs +0.4 |
| Later renewers among stayers | Raw files | Not higher PY2020 savers (4.4% vs 4.9%), so censoring on that margin looks benign |
| MDE arithmetic | By hand | 2.5/1.8 and 2.6/1.9 correct |
| Implied 2019 cohort H2b | From cohort weights | About 2.9, same direction |
| Stage order | `generated` stamps | Consistent with the paper |
| Registration time | OSF API, fetched by the registration's public ID | 2026-10-26T13:22:16Z |
| 2024 rule description (l.490-493) | CMS CY2024 fact sheet | Consistent |
| Participation options | 42 CFR 425.600(d) via Cornell LII | As used in concern 1 |
| Industry report | Full text of the cited PDF | Concern 4 |
| 2026 proposed rule | CMS fact sheet | Concern 4 |
| Novelty | 2 web searches | No peer-reviewed study found |

The web pages were read through a summarising fetch tool, except the industry report, which I read as extracted text. My scripts are in the session scratchpad and wrote nothing to either repository; `git status` is clean in both.

## What could not be verified

- That outcome files were unread before registration, and that robustness results were unread until the confirmatory results (attestations).
- Commit order and the "code identical to the registered commit" claim (git history was out of bounds); the hashes of the OSF attachments.
- The constructed variables themselves: I did not rebuild the dbt pipeline, so the pull, the components and the 26/241 exclusions are taken from the committed results. The points in concern 5 marked inferred rest on the rule text.
- The unscripted diagnostic numbers (concern 11).
- The 2026 dissertation's 40% and 70% figures, the CMS program totals, and most reference characterisations beyond the four sources above. Those I know (the selection, exit and ratchet papers, the bundled-payment study, the methods citations) are described consistently with my recollection; I did not re-read them.
- Whether the built DOCX and PDF match the Markdown; `synthetic.py` and the study's tests were not read.

## What to do before a revision (in order)

1. **Rewrite the abstract and Conclusions** so both registered verdicts and their wording appear, the sharing-rate reading is marked as interpretation, and "did not raise" becomes an interval. Fix the 29/277 slip. Reconsider the title.
2. **Repair H4 reporting:** name the composition bias, add a year-aligned estimate with its interval and the risk-adjusted TWFE results, remove "rules out a drop of more than about 4%", reword "failed".
3. **Reframe the validation:** change-scale figure in the abstract, the no-change comparison, the step-2 row, and an explicit statement that the pull is unvalidated.
4. **Correct the literature framing:** full account of the industry report and the 2019-2020 wave, disclosure that the search followed the results, the 2026 proposed rule.
5. **Add four post hoc analyses, labelled as such:** H2b adjusted for savings rate and agreement history; H3 with the reported savings rate; the revenue-status tabulation; an ESRD-retaining sensitivity analysis. Extend Table 1 with the adjusters.
6. **Soften the registration language** to attestation where it is one, script the diagnostic numbers, and close the three gaps in the language-model disclosure.
7. **Rework H3's presentation and the generalisability paragraph** as set out in concerns 9 and 13, and add one sentence that the registered verdicts survive a multiplicity correction.
8. **Clean up** the minor items (eTable 14, eTable 13 caption, MDE wording, STROBE item 19).

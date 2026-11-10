# Revision after the 2026-11-10 assessment: implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Check every claim in the 2026-11-10 assessment, rerun the ones that are numbers as post hoc work, and prepare a
revised manuscript whose abstract and Conclusions claim only what the registered tests and labelled post hoc checks support.

**Architecture:** Two stages with a gate. Stage 1 (study repository) verifies sources and adds 7 post hoc scripts, each
with a synthetic-data test, changing no registered file. Stage 2 (this repository) copies their results, extends the
generated tables and rewrites prose by rules keyed to result fields, because the results do not exist yet. The gate is
the author's reading of the Stage 1 results and of the disposition table below.

**Tech stack:** Python 3.12 via uv; DuckDB and dbt, PyMC, scipy, statsmodels (study repository, `--group analysis`);
pandoc, `scripts/make_tables.py`, `scripts/check_numbers.py` (this repository).

**Spec:** `reviews/2026-11-10-critical-assessment.md` (sha256 696f99fae60a191f...). Concern numbers below are its numbers.

**Why this file is here:** it restates the assessment's findings, so it sits beside it in `reviews/`, not in
`docs/superpowers/plans/`. Both were committed on 2026-11-10 at the author's request, before any response existed.

## Global constraints

1. **No scratch numbers.** None of the assessment's recomputed figures appears in a test, an expected value or prose.
   Tests use synthetic data with known answers. The real result is compared with the assessment's figure only in the
   response (Task 17).
2. **Estimand before data.** Each script's docstring fixes its estimand; the script and its test are committed before
   its one real-data run. Order: commit script, run with a clean tree, commit the JSON (it records `git_commit`).
3. **Registered settings.** Seed 20261022 and 10,000 resamples wherever a script resamples; `decision.FULL` for PyMC.
4. **New files only in the study folder.** Scripts in `analysis/mssp-benchmark-ratchet/posthoc/`, tests in
   `posthoc/tests/`. Nothing changes under `ratchet/`, `dbt/`, `tests/`, `results/` or the registered Markdown files.
   Existing post hoc scripts and their JSON do not change either (their hashes are cited).
5. **Registered outputs are annotated, never replaced.** A registered verdict or estimate stays as registered, with a
   note beside it.
6. **Never type a number by hand.** Results reach this repository only as copied JSON (`data/posthoc/`, sha256 in
   `data/README.md`); scripts are copied byte for byte to `posthoc/`. A cited figure that is not a study result goes
   in `data/number-allowlist.tsv` with its source.
7. **Abstract at most 350 words** (now 348). One task owns the abstract (Task 16); it names what leaves and ranks
   what enters. No other task edits the abstract.
8. **`tests/test_manuscript.py` trip-wire:** the text "95% CrI, 1.7 to 5.4" must remain in `paper.md`.
9. **Sources are re-read at the source** before any sentence relies on them: `references/audit/milliman2024/`, the eCFR
   API for 42 CFR 425.600(d) as in force on 2022-01-01, and the CMS pages for the 2026 rule (look for a final rule).
10. **Branches, no push.** This repository: `revision-1` from `main`. Study repository:
    `src_feature_mssp_revision_posthoc` from `src_develop`. Both stay local until Samuel approves; they merge later
    with `--no-ff` and no rebase or squash, so the commit hashes cited in `data/README.md` hold.
11. **Frozen:** `submission/ijmr/`, the submitted `submission/bmc-hsr/cover-letter.*`, and tags up to `v1.3.1`. The paper
    is in peer review: no release, tag, upload or message to the journal comes from this plan.
12. **Line width 120** in Markdown; `uv run ruff check . && uv run ruff format --check .` clean in both repositories.

## Review focus

1. **A post hoc result differs from the assessment's figure.** The script's result is reported; prose follows the rules
   in Stage 2, which are keyed to fields, not to the assessment. (Task 17 records the difference.)
2. **A post hoc result weakens a registered headline** (for example, the adjusted H2b interval includes zero). The
   abstract must say so; Task 16's rules cover both outcomes.
3. **The abstract passes 350 words.** `validate_bmc_compliance.py` fails; Task 16 ends with that check.
4. **A registered file changes by accident.** Every Stage 1 task ends with the guard command in Task 1.
5. **A new prose number passes `check_numbers.py` by chance** (its single-number test is weak). Every new estimate is
   written with its interval so the triple test applies, and Task 17 reads each new number against its field.

## Dispositions

| Concern | Default disposition | Tasks |
|---|---|---|
| 1 Headline vs registered verdicts | Accept | 4, 5, 10, 11, 16 |
| 2 H4 composition bias, "rules out" | Accept; registered estimate stays, annotated | 2, 10, 12, 16 |
| 3 Validation covers levels only | Accept | 3, 10, 13, 16 |
| 4 Prior report, 2019-2020 wave, search timing, 2026 rule | Accept after re-reading the sources | 1, 14 |
| 5 Pull vs agreement history and savings | Accept | 5, 6, 7, 10, 15 |
| 6 Only two motives | Accept | 14 |
| 7 Registration claims are attestations | Accept | 15 |
| 8 Small-sample inference | Accept in part: HC2 interval beside the primary result and plainer wording; no clustering analysis (the public files have no parent-organisation variable, and ACOs are assigned by county across state lines, so a state cluster is ill-defined), kept as a limitation | 15 |
| 9 H3 presentation | Accept in part: Table 3 keeps the registered verdict with a "posterior equals prior" note, and shows the registered robustness model without the measurement-error layer beside it | 7, 10, 15 |
| 10 ESRD exclusions | Time-boxed spike, with a stated fallback | 9 |
| 11 Unscripted and unreported numbers | Accept | 8, 10 |
| 12 MDE as yardstick | Accept | 15 |
| 13 Generalisability | Accept | 5, 14 |
| 14 Multiplicity sentence | Accept | 8, 15 |
| 15 Language-model disclosure gaps | Accept | 15 |
| Minor items | Accept, except the "Trial registration" heading, which is the journal's | 15 |

**Author decisions (defaults apply unless Samuel says otherwise; none blocks Stage 1):**

- **Title:** drop "to reset benchmarks". Default: "Early renewal of accountable care organization agreements in the
  Medicare Shared Savings Program: a preregistered retrospective cohort study". A title change needs the editor's consent.
- **Keywords:** drop "Bayesian analysis" (7 remain; BMC allows 3 to 10).
- **Registered items never reported** (H3 median interval widths, SD-unit coefficients, plan sections 6 and 5.3): if
  Task 1 confirms they are absent, add an entry to the study's `DEVIATIONS.md`. That file is the living record, but it
  sits beside registered files, so the entry waits for Samuel's yes.
- **When Stage 2 runs:** now, provisionally, or after BMC's decision. Reviewers will add their own points either way.

## File structure

Study repository, `analysis/mssp-benchmark-ratchet/posthoc/` (all new):

| File | Responsibility | Concern |
|---|---|---|
| `h4_year_aligned.py` | Year-aligned spending comparison and the composition of post years by group | 2 |
| `validation_baseline.py` | The registered validation rule applied to a no-change forecast; phase-in steps | 3 |
| `realized_reset.py` | Interval for the realized 2022 reset; savings-rate change PY2021 to PY2022 | 1 |
| `group_characteristics.py` | Agreement history, revenue, assignment, size by group; revenue by destination; later renewers | 1, 5, 13 |
| `h2b_adjusted.py` | H2b adjusted for savings rate, agreement number and phase-in step | 5 |
| `h3_savings.py` | H3 with the reported savings rate; convergence of the registered model's latent terms | 5, 9 |
| `diagnostics.py` | The numbers now attributed to an unscripted "diagnostic query"; Holm-adjusted registered *P* values | 11, 14 |
| `esrd_sensitivity.py` | Only if the spike in Task 9 succeeds | 10 |
| `tests/conftest.py`, `tests/test_<script>.py` | One test file per script | |

Each script follows `posthoc/pull_savings.py`: a docstring that begins "NOT REGISTERED", says when and why it was
written and gives the run command; `main()` writes `<script>.json` with `registered: false`, `note`, `generated`,
`git_commit`, `seed`. Each task also adds its row to the study folder's `posthoc/README.md` table. **Record shape:** `check_numbers.py` matches an "estimate (lower to upper)" only when the
estimate and a 2-element interval list sit in the same dict, in the unit the prose uses. So every estimate is stored as
`{"estimate": x, "ci95": [lo, hi], ...}` in reporting units (percent or percentage points), never split across dicts.

This repository: `data/posthoc/*.json`, `posthoc/*.py`, `data/README.md`, `posthoc/README.md`, `data/number-allowlist.tsv`,
`scripts/make_tables.py`, `tables/`, `paper.md`, `supplement.md`, `strobe.md`, `metadata.yaml`, `CITATION.cff`,
`.zenodo.json`, `references/other.bib`, `references/AUDIT.md`, `reviews/2026-11-10-response.md`.

---

## Stage 1: verify and compute (study repository)

### Task 1: Branches, guard, and claims checked by reading

**Files:** Create `reviews/2026-11-10-response.md` here (untracked), from the dispositions table, one section per concern.

- [ ] **Step 1:** Create both branches (constraint 10). In the study repository run
  `uv run --group analysis pytest analysis/mssp-benchmark-ratchet/tests -q` and record the pass count.
- [ ] **Step 2:** Define the guard, run after every Stage 1 task; it must print nothing:
  `git diff --stat src_develop -- analysis/mssp-benchmark-ratchet ':!analysis/mssp-benchmark-ratchet/posthoc'`
  and `git diff --stat src_develop -- analysis/mssp-benchmark-ratchet/posthoc/pull_savings.* analysis/mssp-benchmark-ratchet/posthoc/validation_change.*`.
- [ ] **Step 3:** Check by reading, and record "confirmed", "not confirmed" or "differs: ..." with the file and line in
  the response. Already confirmed while planning: the abstract's "29 ... 277 ... on the regional pull" (the pull
  comparison's own counts are in `confirm.json`); `did.json` holds `conventional.twfe_risk_adjusted`, which
  `make_tables.py` never reads; `paper.md` line 603 says "eTables 1-13" while the supplement has eTable 14. Still to check:
  - plan section 7's wording for rules 1, 2 and 8 (`PREREGISTRATION.md`);
  - the Milliman 2024 report (concern 4): the 29 and 26, the stated motives, the net-savings remark, and the
    2019-2020 wave with its counts and savings rates, from `references/audit/milliman2024/`;
  - search and results timestamps (`research/README.md` in both repositories, the `generated` fields);
  - 42 CFR 425.600(d) on 2022-01-01 by the eCFR API: could a low-revenue ACO experienced with risk renew into BASIC Level E;
  - the CY2027 Physician Fee Schedule proposed rule (CMS, July 2026) and whether a final rule exists, with URLs and access dates;
  - whether `confirm.json` or `robustness.json` holds H3 median interval widths and SD-unit coefficients;
  - whether the enrollment files identify ACOs that had renewed early into their 2019 or 2020 agreement
    (`dbt/models/enrollment/`); record the column or "not identifiable";
  - the exact `status` values in `dbt/models/descriptive/did_panel.sql` that mark renewal into 2023 and 2024.
- [ ] **Step 4:** No commit (the response is untracked). Run the guard.

### Task 2: `h4_year_aligned.py` (concern 2)

**Files:** Create `posthoc/h4_year_aligned.py`, `posthoc/tests/conftest.py` (puts the study folder and `posthoc/` on
`sys.path`), `posthoc/tests/test_h4_year_aligned.py`.

**Interfaces:**
- Consumes: `ratchet.did.deltas`, `ratchet.did.estimate`, `ratchet.resample.difference`; the panel loaded exactly as
  `ratchet/run.py` loads it for the `did` stage (`build.connect(stage="full", descriptive=True)`).
- Produces: `year_aligned(panel: pd.DataFrame, outcome: str = "y") -> pd.DataFrame` (columns `aco_id, grp, cohort, py, d`;
  one row per ACO and post year; `d` = outcome that year minus the ACO's mean over PY2020 and PY2021; ACOs kept as in
  `did.deltas`); `estimate_year_aligned(d: pd.DataFrame, n: int, seed: int) -> dict` with keys `by_year` (`"2022"`,
  `"2023"`, `"2024"`) and `average`.

**Estimand (goes in the docstring).** For each post year *t*, Δ*t* is the cohort-weighted early-minus-comparison
difference in `d` among ACOs present in *t* (`resample.difference`). The average is Σ *n*(early, *t*) Δ*t* / Σ *n*(early, *t*).
Interval: Bayesian bootstrap over ACOs within cohort-by-group cells, one weight per ACO applied to all its years.
*P* value: permutation of group labels among ACOs within cohort. Both outcomes: `y` and `y_risk`.

- [ ] **Step 1: Write the failing tests**

```python
def _panel(effect=0.0, g=0.06):
    rows = []
    for i in range(40):
        grp = "early" if i < 10 else "stayer"
        last = 2024 if (grp == "early" or i % 2 == 0) else 2022  # half the stayers have no years after PY2022
        for py in range(2020, last + 1):
            y = 0.1 * i + g * (py - 2020) + (effect if grp == "early" and py >= 2022 else 0.0)
            rows.append({"aco_id": f"A{i}", "grp": grp, "cohort": "2020-01", "py": py, "y": y, "y_risk": y, "status": "included", "post": py >= 2022})
    return pd.DataFrame(rows)


def test_no_effect_is_zero_when_groups_keep_different_years():
    panel = _panel()
    out = h4.estimate_year_aligned(h4.year_aligned(panel), n=200, seed=1)
    assert abs(out["average"]["observed"]) < 1e-12
    assert did.estimate(did.deltas(panel), "delta", 200, 1)["observed"] > 0.01  # the registered estimator on the same panel


def test_constant_effect_is_recovered():
    out = h4.estimate_year_aligned(h4.year_aligned(_panel(effect=-0.02)), n=200, seed=1)
    assert abs(out["average"]["observed"] + 0.02) < 1e-12
    assert set(out["by_year"]) == {"2022", "2023", "2024"}
```

- [ ] **Step 2:** Run `uv run --group analysis pytest analysis/mssp-benchmark-ratchet/posthoc/tests/test_h4_year_aligned.py -v`. Expected: FAIL (module missing).
- [ ] **Step 3:** Implement the two functions and `main()`. JSON: `composition` (`c_mean_early`, `c_mean_comparison`,
  `c_difference` from `did.deltas(panel).c`; `n_by_year`), then for `y` and `y_risk` the keys `by_year` and `average`,
  each record `{"n_early", "n_comparison", "observed", "p_value", "percent": {"estimate", "ci95"}}`, where
  `percent.estimate` is the bootstrap posterior mean, as `did.estimate` reports it.
- [ ] **Step 4:** Run the tests. Expected: PASS. Run ruff.
- [ ] **Step 5:** Commit script and tests. Run `uv run --group analysis python analysis/mssp-benchmark-ratchet/posthoc/h4_year_aligned.py`
  once. `main()` asserts that `did.estimate(did.deltas(panel), "delta", ...)["observed"]` equals `results/did.json`
  `H4.observed` to 1e-12, so the panel is the registered one. Commit the JSON. Run the guard.

### Task 3: `validation_baseline.py` (concern 3)

**Files:** Create `posthoc/validation_baseline.py`, `posthoc/tests/test_validation_baseline.py`.

**Interfaces:** Produces `agreement_levels(pred: np.ndarray, actual: np.ndarray) -> dict` with `n`, `spearman`,
`median_abs_pct_error`, `slope_actual_on_pred`, the statistics of the registered rule (reuse `ratchet.validate`'s
function if it exposes one; do not edit it).

- [ ] **Step 1: Failing tests.** `agreement_levels(a, a)` gives `spearman == 1`, `median_abs_pct_error == 0`,
  `slope_actual_on_pred == 1`; `agreement_levels(1.1 * a, a)["median_abs_pct_error"]` equals `10.0` to 1e-9, for
  `a = np.array([100.0, 200.0, 400.0, 800.0])`.
- [ ] **Step 2:** Run; expected FAIL.
- [ ] **Step 3:** Implement. JSON: `rule` (the registered thresholds, read from `ratchet.config` or `validation.json`);
  `no_change_all` (every regular renewer with a published 2022 benchmark; predictor = current PY2021 benchmark);
  `same_sample` with `no_change` and `rebuilt` on the registered validation ACOs (the `rebuilt` record must equal
  `results/validation.json` to 1e-9, asserted at run time); `by_step` (the same two predictors per phase-in step);
  `change_scale` (`rmse_no_change`, `rmse_rebuilt` of the actual change against 0 and against the rebuilt change);
  `passes_rule` booleans for each predictor; `study_steps` (counts of `analysis.step` for early renewers and stayers).
- [ ] **Step 4:** Tests pass; ruff.
- [ ] **Step 5:** Commit, run once, commit the JSON, guard.

### Task 4: `realized_reset.py` (concern 1)

**Files:** Create `posthoc/realized_reset.py`, `posthoc/tests/test_realized_reset.py`.

**Interfaces:** Produces `mean_interval(x: np.ndarray) -> dict` with `n`, `estimate` (mean), `sd`, `ci95` (Student *t*),
`share_positive`, `min`, `max`.

- [ ] **Step 1: Failing test.** `mean_interval(np.array([1.0, 2.0, 3.0]))`: `estimate == 2`, `sd == 1`, and `ci95`
  equals `2 ∓ scipy.stats.t.ppf(0.975, 2) / 3 ** 0.5` to 1e-12; `share_positive == 1`.
- [ ] **Step 2:** Run; expected FAIL.
- [ ] **Step 3:** Implement. The actual change is defined exactly as in `validation_change.py` part 2. JSON: `early`
  and `regular_renewers` (each a `mean_interval` record); `savings_rate_change` (PY2022 minus PY2021 savings rate, early
  vs stayers, by `resample.compare`, stored as `{"estimate", "ci95", "p_value", "n_early", "n_stayer"}` plus each
  group's mean change). Run-time assertion: `early.estimate` equals `validation_change.json`
  `early_renewers_realized.all_with_hist_2022.mean` to 1e-9.
- [ ] **Step 4:** Tests pass; ruff.
- [ ] **Step 5:** Commit, run once, commit the JSON, guard.

### Task 5: `group_characteristics.py` (concerns 1, 5, 13)

**Files:** Create `posthoc/group_characteristics.py`, `posthoc/tests/test_group_characteristics.py`.

**Interfaces:** Produces `tabulate(d: pd.DataFrame, by: str, column: str) -> dict[str, dict[str, dict]]`, mapping group
to level to `{"n": int, "share": float}`, with missing values under the level `"missing"`.

- [ ] **Step 1: Failing test.** A 5-row frame (`grp` early, early, stayer, stayer, stayer; `x` 1, 2, 1, 1, None):
  `tabulate(d, "grp", "x")["early"]["1"] == {"n": 1, "share": 0.5}` and `["stayer"]["missing"]["n"] == 1`.
- [ ] **Step 2:** Run; expected FAIL.
- [ ] **Step 3:** Implement. JSON: `by_group` for `agreement_number` (`groups.period_2021` as 1, 2, 3 or more),
  `high_revenue`, `prospective`, `step`, and the median and quartiles of assigned beneficiaries (PY2020), for early
  renewers, stayers and leavers; `basic_early_by_revenue` (PY2021 revenue flag by `enhanced_2022`, as counts; the same
  with the PY2022 flag if the enrollment table has one, else `null`); `later_renewers` (stayers who renewed into 2023
  and into 2024, by the `status` values recorded in Task 1: counts, the same characteristics, and mean `pull`, `own` and
  PY2020 savings rate, descriptive only); `prior_early_renewal` (count by group if Task 1 found a column, else `null`).
- [ ] **Step 4:** Tests pass; ruff.
- [ ] **Step 5:** Commit, run once, commit the JSON, guard. Group totals must equal `confirm.json`'s; assert at run time.

### Task 6: `h2b_adjusted.py` (concern 5)

**Files:** Create `posthoc/h2b_adjusted.py`, `posthoc/tests/test_h2b_adjusted.py`.

**Interfaces:**
- Consumes: `ratchet.regression.build_model(y, x)`; `decision.fit(model, decision.FULL, seed, cores=4)`;
  `decision.convergence(idata, [f"b_{n}" for n in x])`; one retry with `decision.RETRY` and `seed + 1` if not converged,
  as `regression.adjusted_difference` does.
- Produces: `MODELS = {"cohort_only": (), "savings": ("sav_rate_2020",), "history": ("agreement_number", "step"), "all": ("sav_rate_2020", "agreement_number", "step")}`
  and `design(frame: pd.DataFrame, adjusters: tuple[str, ...]) -> tuple[np.ndarray, dict[str, np.ndarray], float, float, int]`,
  the return convention of `regression._design` (standardized outcome, design columns, outcome mean, outcome SD, rows
  dropped). `x` always has `early` and `cohort_2020`; continuous adjusters are centered and divided by their SD;
  `agreement_number` and `step` enter as indicators with the lowest level as reference.

- [ ] **Step 1: Failing tests.** On a 12-row synthetic frame with one missing `sav_rate_2020`:
  `design(f, ())` returns `x.keys() == {"early", "cohort_2020"}` and 0 dropped; `design(f, MODELS["savings"])` adds
  `"sav_rate_2020"` with mean 0 and SD 1 to 1e-12 and reports 1 dropped; `design(f, MODELS["history"])` has no column
  for the reference levels.
- [ ] **Step 2:** Run; expected FAIL.
- [ ] **Step 3:** Implement. For each model: fit, then store the `early` coefficient in percentage points as
  `{"estimate", "ci95", "p_positive", "n", "dropped", "convergence"}` (posterior of `b_early` times the outcome SD;
  `convergence` as `decision.convergence` returns it). Run-time assertion: `cohort_only` reproduces the registered
  `adjusted_difference(frame, "pull", seed, adjusted=False)` value in the results files within 0.05 points (Monte Carlo error).
- [ ] **Step 4:** Tests pass; ruff.
- [ ] **Step 5:** Commit, run once (PyMC; minutes), commit the JSON, guard.

### Task 7: `h3_savings.py` (concerns 5, 9)

**Files:** Create `posthoc/h3_savings.py`, `posthoc/tests/test_h3_savings.py`.

**Interfaces:** Consumes `decision.make_design(frame, sigma_v, include_own, exclude, extra)`;
`decision.fit_checked(design, seed) -> (idata, checks)`, which builds the model itself and checks coefficients and
intercept only; `decision.coefficient_summary`, `decision.coefficient_names`. The latent own-spending variables in the
registered model are `own_mu`, `own_tau` and `own_z`. Produces `savings_design(frame: pd.DataFrame) -> decision.Design`,
equal to `make_design(frame, None, include_own=False, extra=("sav_rate_2020",))`, and
`latent_convergence(idata) -> dict` with `max_rhat`, `min_ess_bulk`, `min_ess_tail` over those 3 variables (`az.summary`).

- [ ] **Step 1: Failing test.** With a frame from `ratchet.synthetic` (as `tests/test_decision.py` builds one):
  `decision.coefficient_names(savings_design(frame))` contains `"b_sav_rate_2020"` and `"b_pull"` and does not contain `"b_own"`.
- [ ] **Step 2:** Run; expected FAIL.
- [ ] **Step 3:** Implement. JSON: `registered_refit` (the registered design, `make_design(frame, sigma_v)` with
  `sigma_v` and the seed taken as `ratchet/run.py` takes them for the confirm stage, through `fit_checked`: the
  coefficient summary, `matches_confirm` true if the pull coefficient is within 0.05 of `confirm.json`'s, and
  `latent_convergence`); `savings_model` (`fit_checked(savings_design(frame), seed)`: pull and savings-rate
  coefficients, each `{"estimate", "ci95", "p_positive"}`, with `n`, `events` and `convergence`). No direct-simulation
  test: this is exploratory and decides nothing.
- [ ] **Step 4:** Tests pass; ruff.
- [ ] **Step 5:** Commit, run once, commit the JSON, guard. If `matches_confirm` is false, stop and report.

### Task 8: `diagnostics.py` (concerns 11, 14)

**Files:** Create `posthoc/diagnostics.py`, `posthoc/tests/test_diagnostics.py`.

**Interfaces:** Produces `holm(p: dict[str, float]) -> dict[str, float]` (Holm-adjusted *P* values, keyed like the input).

- [ ] **Step 1: Failing test.** `holm({"a": 0.01, "b": 0.04, "c": 0.03})` equals `{"a": 0.03, "b": 0.06, "c": 0.06}` to 1e-12.
- [ ] **Step 2:** Run; expected FAIL.
- [ ] **Step 3:** Implement. JSON: `n_ab_median` by included or excluded and early or stayer; `excluded_with_aged_dual_hidden`;
  `cohorts_in_py2020_file` and `absent_from_py2021_file`; `median_updated_benchmark_2021` with `n_with_value`;
  `assignment_changed_2022`; `esrd_share_of_person_years` (median, quartiles, PY2021, study ACOs); `multiplicity`
  (the registered *P* values for H2b, H2a, the 3 H3 tests and H4 from the results files, and `holm(...)` of them).
  These reproduce numbers the paper already reports through `data/number-allowlist.tsv`. The check that they match
  is Task 10 Step 2: the allowlist rows are removed and the number check must still pass.
- [ ] **Step 4:** Tests pass; ruff.
- [ ] **Step 5:** Commit, run once, commit the JSON, guard.

### Task 9: ESRD spike (concern 10), 2 hours at most

- [ ] **Step 1:** Read `dbt/models/full/gain_inputs.sql`, `county.sql`, `shares.sql`, `region.sql`. Question: can the
  regional pull be built for the excluded ACOs inside a post hoc script, by SQL over the built tables, with the ESRD
  regional term weighted by total person-years?
- [ ] **Step 2 (yes):** write `esrd_sensitivity.py` on the pattern of Tasks 2-8, with a synthetic test that the
  variant equals the registered pull when no count is hidden; report H2b on the enlarged sample by `resample.compare`
  as `{"estimate", "ci95", "p_value", "n_early", "n_stayer"}`, labelled a sensitivity analysis.
- [ ] **Step 2 (no, or it needs a change under `dbt/`):** stop. The fallback is a Limitations sentence using
  `diagnostics.json` `esrd_share_of_person_years`. Record which in the response.

### Gate

- [ ] Fill the response's per-concern sections with each result and its field, and the difference from the
  assessment's figure where there is one. Samuel reads the results and the author decisions. Stage 2 starts on
  Samuel's yes.

---

## Stage 2: the manuscript (this repository; provisional until the journal's reviews arrive)

### Task 10: Copy results and extend the generated tables

**Files:** Create `data/posthoc/<script>.json`, `posthoc/<script>.py`, `tables/etable15-revision-checks.md`. Modify
`data/README.md`, `posthoc/README.md`, `data/number-allowlist.tsv`, `scripts/make_tables.py`, `supplement.md`,
`paper.md:283-291` (Methods "Post Hoc Checks (Not Registered)") and `paper.md:603`.

- [ ] **Step 1:** Copy each JSON and script unchanged; add a row per JSON to `data/README.md` (source commit, "post
  hoc, not registered", sha256) and per script to `posthoc/README.md`. Run `uv run pytest tests/test_manuscript.py::test_data_matches_recorded_hashes`. Expected: PASS.
- [ ] **Step 2:** Remove from the allowlist the rows `diagnostics.json` now covers; `uv run python scripts/check_numbers.py` must still pass.
- [ ] **Step 3:** In `make_tables.py`:
  - `table1()`: add rows for agreement number, revenue category, assignment method and size from `group_characteristics.json`.
  - `table3()`: keep the own-spending row's registered values; add a note that its posterior equals its prior, so the
    data did not inform it; add the pull and own-spending rows of `robustness.json` `7_no_measurement_error`, labelled
    as the registered robustness model without the measurement-error layer.
  - `table4()` (eTable 8): add rows for the year-aligned estimate (each year and the average; both outcomes) and the
    risk-adjusted two-way fixed effects (pooled, and the event study in the existing event-study table), each labelled registered or post hoc.
  - `etable_posthoc()` (eTable 13): add the pull-savings correlations as rows, so the caption is true.
  - `etable_h3_checks()` (eTable 5): if Task 1 found the H3 median interval widths and SD-unit coefficients in the
    results files, add them; if not, nothing here (see the author decision on `DEVIATIONS.md`).
  - New `etable_revision_checks()` registered in `TABLES` as `"etable15-revision-checks"`: the realized reset
    intervals, the no-change forecast against the registered rule (with the per-step rows), H2b by adjustment set, H3
    with the savings rate and the latent convergence, revenue by destination, later renewers, and the Holm-adjusted *P* values.
- [ ] **Step 4:** `uv run python scripts/make_tables.py`; add eTable 15 to the supplement's list and includes; change
  "eTables 1-13" to the true range. Rewrite Methods "Post Hoc Checks (Not Registered)": the count and list of checks
  come from the scripts that actually ran, each with what prompted it (the earlier reviews or this assessment) and its
  table. Run `uv run pytest -q`. Expected: all pass.
- [ ] **Step 5:** Commit on `revision-1`.

### Task 11: Body text for the headline, and the title (concern 1)

**Files:** Modify `paper.md` (Results "Who Renewed Early"; Discussion "Principal Findings"; Conclusions; not the
Abstract), and, if the title decision is yes, `metadata.yaml`, `supplement.md`, `strobe.md`, `CITATION.cff`,
`.zenodo.json` (title only).

Rules:
- Conclusions states both registered verdicts with the plan's wording: the primary (H2b) "supported", which the plan
  reads as evidence for the reset motive; the secondary (H2a) "contradicted". It then says the weighing is the author's.
- Each support for the sharing-rate reading carries its status where it is used: known before registration (the 26 of
  27), registered descriptive (total expected gain), post hoc (realized reset, benchmark update).
- The realized reset is written as its estimate with `realized_reset.json` `early.ci95`. If the interval contains
  zero, the wording is "no detectable change"; "did not raise", "bear this out", "agree", "does not hold on average"
  and "reset benchmarks that fell" all go. If it excludes zero, the direction is stated with the interval.
- Results adds one sentence from `group_characteristics.json` `basic_early_by_revenue`, stating how many could have
  chosen BASIC Level E (only if Task 1 confirmed the rule), and one from `realized_reset.json` `savings_rate_change`.

- [ ] **Step 1:** Edit by the rules. **Step 2:** `uv run python scripts/check_numbers.py` (expected: "every number
  and interval matches"). **Step 3:** `uv run pytest -q`. **Step 4:** Commit.

### Task 12: Spending comparison, body text (concern 2)

**Files:** Modify `paper.md` (Methods "Spending After Renewal (H4)"; Results "Spending After Renewal"; Discussion;
Limitations; not the Abstract), `supplement.md` if it describes the estimator.

Rules:
- The registered estimate and interval stay, named as registered. Beside them: the year-aligned average
  (`h4_year_aligned.json` `y.average.percent`) and the two-way fixed-effects estimates already in `did.json`, including the risk-adjusted one.
- Limitations names the composition difference with `composition.c_mean_early` and `c_mean_comparison`, and gives its
  direction (STROBE item 19).
- Both "rules out a drop of more than about 4%" sentences go. If a bound is stated, it is the widest lower bound among
  the reported intervals, named as such.
- "following the not-yet-treated design of Callaway and Sant'Anna" becomes a comparison with not-yet-treated ACOs
  that collapses to one change per ACO; the 90-word sentence at lines 238-243 is split.
- Mean reversion is discussed in the direction the data show (early renewers were high savers).
- The H4 minimum detectable effect is described as computed from the pre-period change, beside the width of the
  realized interval.

- [ ] Steps as in Task 11.

### Task 13: Validation, body text (concern 3)

**Files:** Modify `paper.md` (Methods "Validation Before Use"; Results "Validation and Sample"; Limitations; not the Abstract).

Rules:
- Results reports the no-change forecast against the registered rule (`validation_baseline.json` `same_sample`), on the
  same ACOs, and says the rule was lenient if `passes_rule.no_change` is true. If it is false, it says the rule
  discriminated, and the response records that the assessment's point did not hold on the same sample.
- The step cited for the study's ACOs is the one `study_steps` shows, from `by_step`.
- Limitations keeps the statement that the regional pull has no published counterpart.

- [ ] Steps as in Task 11.

### Task 14: Prior work, motives and generalisability (concerns 4, 6, 13)

**Files:** Modify `paper.md` (Background; Discussion "Comparison With Prior Work", "Implications"; Limitations;
"Use of Large Language Models"; not the Abstract), `references/other.bib`, `data/number-allowlist.tsv`, `references/AUDIT.md`.

Rules (each only as far as Task 1 confirmed it at the source):
- The Milliman report is described in full: what it already showed for this cohort, its stated motives, and the
  2019-2020 wave. The contributions paragraph claims the regional measure, the decomposition, the realized benchmarks
  and the spending comparison, and credits the rest. "No peer-reviewed study" stays.
- Methods says when the literature was searched relative to registration and results.
- The 2026 rule is cited (proposed, and final if one exists), in `other.bib` with URL and access date; every figure
  quoted from it or from the report goes in the allowlist with its source.
- "Two motives" becomes "at least two"; the Discussion lists the others the data cannot address.
- Generalisability gets its own paragraph: one cycle and 29 ACOs; the contrast with the 2019-2020 wave; which findings
  the 2024 rules could reverse; the later renewers from `group_characteristics.json`. "give a baseline for the rules in
  force since 2024" goes unless that table supports it.

- [ ] **Step 1:** Edit. **Step 2:** `python3 scripts/audit_references.py` for the new and changed citing sentences;
  update `references/AUDIT.md`. **Step 3:** number check and tests. **Step 4:** Commit.

### Task 15: Registration wording, H3, inference, disclosure, minor items (concerns 5, 7, 8, 9, 12, 14, 15)

**Files:** Modify `paper.md` (not the Abstract), `supplement.md`, `strobe.md`, `metadata.yaml` (keywords, if yes).

Rules:
- **Registration (7):** "could not be opened" and "No savings rate ... was seen" are worded as the author's attestation
  plus what the code enforces (a local file's existence); the dates of design, registration, results and first
  submission are stated in one sentence.
- **Pull (5):** the Background sentence at lines 92-93 is corrected for the January 2020 cohort; Results reports the
  adjusted H2b and the savings-rate H3 from Task 10's table, labelled post hoc.
- **H3 (9):** the text says the own-spending coefficient was not identified, adds the power result for it (eTable 2)
  to the sentence at lines 381-383, reports the latent convergence, and describes the BASIC-level result as an
  association with a level that also sets the renewal options.
- **Inference (8):** the intervals are called bootstrap-type; the HC2 interval from `conventional.json` sits beside the primary result.
- **MDE (12):** "above" and "below the MDE" go; the MDE is reported as design information.
- **Multiplicity (14):** one sentence from `diagnostics.json` `multiplicity`, worded by whether every registered verdict keeps its side of .05 after Holm.
- **Disclosure (15):** which references were read in full (from `references/AUDIT.md`); the search timing; a
  cross-reference between the CRediT line and the Methods statement; one sentence on what the author checked by hand.
- **Minor:** eTable 7's weight in Strengths; STROBE item 19 (a direction for each bias); keywords. "Trial
  registration" stays: it is the journal's heading.

- [ ] Steps as in Task 11.

### Task 16: The abstract (one owner; runs after Tasks 11-15)

**Files:** Modify `paper.md` (Abstract only). `scripts/bmc_fields.py` regenerates `submission/bmc-hsr/abstract-plaintext.txt`.

Rules, each restating what the body now says:
- Both registered verdicts with the plan's wording, then that the weighing is the author's (Task 11).
- The realized reset by Task 11's interval rule ("no detectable change" if the interval contains zero).
- If `h2b_adjusted.json` `all.ci95` contains zero, the abstract says the pull difference did not survive adjustment
  for savings and agreement history; if it excludes zero, the abstract is silent and the body carries it.
- Counts for the pull comparison come from `confirm.json` (not 29 and 277). "ρ" is named as Spearman.
- The year-aligned spending estimate beside the registered one (Task 12). "a preregistered pre-trend condition failed"
  becomes a statement that the registered condition for reading the estimate as an effect could not be met at this
  sample size.
- The change-scale Spearman correlation (`validation_change.json` `regular_renewers_change.spearman`) with or in place
  of the level one, and that the regional pull itself has no published counterpart (Task 13).
- "registered before outcome data were read" is kept only with the attestation wording of Task 15.
- **Budget.** Leaves, in this order until it fits: "by Bayesian bootstrap, permutation tests and logistic
  regression"; "without leaving the program or waiting out its agreement"; "the rules changed in 2024"; "using public
  Medicare files (2016-2024)". Enters, in rank order, and the lowest-ranked items are dropped if 350 cannot hold them
  all: both verdicts; the reset interval wording; the corrected counts; the year-aligned estimate; the validation
  caveat; the reworded pre-trend clause.
- The text "95% CrI, 1.7 to 5.4" stays (constraint 8).

- [ ] **Step 1:** Edit. **Step 2:** `uv run python scripts/validate_bmc_compliance.py`. Expected: "abstract N/350
  words" with N at most 350, and "checks passed". **Step 3:** `uv run python scripts/check_numbers.py` and
  `uv run pytest -q`. **Step 4:** `uv run python scripts/bmc_fields.py`. **Step 5:** Commit.

### Task 17: Build, read-back and response

- [ ] **Step 1:** `scripts/build.sh`; then every command under "Checks before submitting" in
  `submission/bmc-hsr/README.md`. Expected: all pass. Check `paper.docx` by the Pages export (tables, section order).
- [ ] **Step 2:** `git diff main -- paper.md | grep '^+'` and read every added number against its JSON field (Review focus 5).
- [ ] **Step 3:** Grep `paper.md`, `supplement.md` and `strobe.md` for "eTable", "Additional file" and the old title; fix stale cross-references.
- [ ] **Step 4:** Finish `reviews/2026-11-10-response.md` on the pattern of `reviews/2026-10-27-response.md`: per
  concern, what was applied, what was declined and why, and where a rerun differed from the assessment's figure.
- [ ] **Step 5:** Commit on `revision-1`.

### Task 18: Publish together, on Samuel's go-ahead only

- [ ] **Step 1:** Ask Samuel. Nothing below runs without a yes given for that step.
- [ ] **Step 2:** Study repository: merge the post hoc branch into `src_develop` (`--no-ff`); add a build-notes section; push.
- [ ] **Step 3:** This repository: commit the response with the revision (the assessment and this plan are already
  committed); merge `revision-1` into `main` (`--no-ff`); push. A release (`v1.4.0`) is cut only for what is actually
  sent to a journal.
- [ ] **Step 4:** Tell the coordinating session that claims changed, so the site post is brought into line.

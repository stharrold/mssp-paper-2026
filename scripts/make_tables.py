"""Write every manuscript and supplement table, as Markdown, from the committed results.

Each table goes to tables/<name>.md with its caption and notes; paper.md and supplement.md include them with the
include filter (scripts/include.lua). Nothing is typed by hand: rerun this after any change to data/.

Usage: python3 scripts/make_tables.py
"""

import json
import math
from collections import Counter

from results import ROOT, dashboard, interval, load, num, pval

OUT = ROOT / "tables"
D = dashboard()
POSTHOC = json.loads((ROOT / "data" / "posthoc" / "validation_change.json").read_text())
PULL = json.loads((ROOT / "data" / "posthoc" / "pull_savings.json").read_text())
VALIDATION, POWER, CONFIRM, ROBUST, DID, CONV, EXPL = (load(n) for n in ("validation", "power", "confirm", "robustness", "did", "conventional", "exploratory"))
GROUPS = ("early", "stayer", "leaver")
HEAD = ("Early renewers", "Stayers", "Left after PY2021")


def table(header: list[str], rows: list[list[str]], caption: str, notes: str = "", align: str | None = None, widths: list[int] | None = None) -> str:
    """A pipe table. widths are relative column widths; pandoc reads them from the length of each rule's dashes."""
    align = align or "l" + "r" * (len(header) - 1)
    widths = widths or [3] * len(header)

    def rule(a: str, w: int) -> str:
        dashes = "-" * (4 * w)
        return {"l": ":" + dashes, "r": dashes + ":", "c": ":" + dashes + ":"}[a]

    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(rule(a, w) for a, w in zip(align, widths, strict=True)) + "|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    text = "\n".join(lines) + f"\n\n: {caption}\n"
    if notes:
        text += f"\n::: {{.table-notes}}\n{notes}\n:::\n"
    return text


def prob(p: float) -> str:
    """A posterior probability to 3 decimals, never shown as exactly 0 or 1 (10,000 draws cannot establish that)."""
    return ">0.999" if p > 0.9995 else "<0.001" if p < 0.0005 else num(p, 3)


def mean_sd(stat: dict, scale: float = 1.0, digits: int = 1) -> str:
    return f"{num(stat['mean'] * scale, digits)} ({num(stat['sd'] * scale, digits)})"


def table1() -> str:
    tracks = Counter()
    cohorts = Counter()
    for r in EXPL["who_renewed"]:
        level = r["track_2021"]
        band = "ENHANCED" if level == "ENHANCED" else "BASIC A-B" if level in ("BASIC A", "BASIC B") else "BASIC C-E"
        tracks[(r["grp"], band)] += r["n"]
        cohorts[(r["grp"], r["cohort"])] += r["n"]
    n = {g: cohorts[(g, "2019-07")] + cohorts[(g, "2020-01")] for g in GROUPS}

    def count(key: Counter, g: str, k: str) -> str:
        return f"{key[(g, k)]} ({100 * key[(g, k)] / n[g]:.0f})"

    bal = EXPL["balance"]
    lv = EXPL["leavers"]
    rows = [
        ["ACOs, No."] + [str(n[g]) for g in GROUPS],
        ["**Agreement start, No. (%)**", "", "", ""],
        ["\u00a0\u00a0\u00a0\u00a0July 1, 2019"] + [count(cohorts, g, "2019-07") for g in GROUPS],
        ["\u00a0\u00a0\u00a0\u00a0January 1, 2020"] + [count(cohorts, g, "2020-01") for g in GROUPS],
        ["**Track in PY2021, No. (%)**", "", "", ""],
        ["\u00a0\u00a0\u00a0\u00a0BASIC levels A-B (one-sided)"] + [count(tracks, g, "BASIC A-B") for g in GROUPS],
        ["\u00a0\u00a0\u00a0\u00a0BASIC levels C-E (two-sided)"] + [count(tracks, g, "BASIC C-E") for g in GROUPS],
        ["\u00a0\u00a0\u00a0\u00a0ENHANCED"] + [count(tracks, g, "ENHANCED") for g in GROUPS],
        ["**Assigned beneficiaries, PY2020, mean (SD), %**", "", "", ""],
        ["\u00a0\u00a0\u00a0\u00a0Aged 85 y or older"] + [mean_sd(bal[g]["share_85plus_2020"], 100) for g in GROUPS],
        ["\u00a0\u00a0\u00a0\u00a0Female"] + [mean_sd(bal[g]["share_female_2020"], 100) for g in GROUPS],
        ["**Savings rate, PY2020, pp**", "", "", ""],
        ["\u00a0\u00a0\u00a0\u00a0Mean (SD)"] + [mean_sd(lv[g]["sav_rate_2020"], 100) for g in GROUPS],
        ["\u00a0\u00a0\u00a0\u00a0Median"] + [num(lv[g]["sav_rate_2020"]["median"] * 100) for g in GROUPS],
    ]
    for key, label in (("pull", "Regional pull"), ("own", "Own-spending component"), ("regional_comp", "Regional component")):
        rows += [
            [f"**{label}, pp of benchmark**", "", "", ""],
            ["\u00a0\u00a0\u00a0\u00a0ACOs with the variable, No."] + [str(lv[g][key]["n"]) for g in GROUPS],
            ["\u00a0\u00a0\u00a0\u00a0Mean (SD)"] + [mean_sd(lv[g][key]) for g in GROUPS],
            ["\u00a0\u00a0\u00a0\u00a0Median"] + [num(lv[g][key]["median"]) for g in GROUPS],
        ]
    notes = (
        "Abbreviations: ACO, accountable care organization; pp, percentage points; PY, performance year. "
        "Early renewers ended their agreements and began new ones on January 1, 2022; stayers remained in their "
        "agreements; leavers left the program after PY2021. The savings rate is CMS's reported savings as a share of "
        "the benchmark (positive when spending was below the benchmark). The expected-gain variables could not be "
        "built for every ACO; a diagnostic query run after the results, outside the registered pipeline, traced each "
        "exclusion to county counts of assigned beneficiaries with end-stage renal disease that were all suppressed "
        "(Results). Leavers were not compared in any registered test."
    )
    return table(
        ["Characteristic", *HEAD],
        rows,
        f"Table 1. Characteristics of the {sum(n.values())} ACOs in the 2019 and 2020 agreement cohorts, by group",
        notes,
        widths=[10, 4, 4, 4],
    )


def table2() -> str:
    rows = []
    roles = {"primary": "Primary", "secondary": "Secondary", "descriptive": "Descriptive"}
    verdicts = {"supported": "Supported", "contradicted": "Contradicted", None: ""}
    for r in D["comparisons"]["rows"]:
        bold = r["role"] == "primary"
        cells = [
            r["label"].replace("H1 ", "H1, ").replace("H2b ", "H2b, ").replace("H2a ", "H2a, ") + f" ({roles[r['role']].lower()})",
            f"{r['n_early']} / {r['n_stayer']}",
            f"{num(r['mean'], 1, sign=True)} ({interval(r['lo'], r['hi'])})",
            prob(r["p_positive"]),
            pval(r["p"]),
            num(r["mde"]) if r["mde"] else "",
            verdicts[r["verdict"]],
        ]
        rows.append([f"**{c}**" if bold and c else c for c in cells])
    g = CONFIRM["groups"]["H2b_pull"]
    analyzed = {k: 2.80 * POWER["h2"][k]["sd_stayers"] * math.sqrt(1 / g["n_early"] + 1 / g["n_stayer"]) for k in ("pull", "own")}
    notes = (
        "Abbreviations: CrI, credible interval; MDE, minimum detectable effect at 80% power, two-sided $\\alpha$ = .05, "
        f"computed before the tests for 29 vs 277 ACOs (for the {g['n_early']} vs {g['n_stayer']} compared on the expected-gain variables "
        f"it is {num(analyzed['pull'])} for H2b and {num(analyzed['own'])} for H2a); Pr(>0), posterior probability that the "
        "difference is positive; pp, percentage points; PY, performance year. Differences are early renewers "
        "minus stayers within agreement cohort, averaged with weights proportional to early renewers per cohort. "
        "Posterior means and 95% equal-tailed CrIs are from a Bayesian bootstrap (10,000 draws); P values are from "
        "stratified permutation (10,000 shuffles within cohort). Expected-gain variables are in percentage points of "
        "the current benchmark; savings rates in percentage points. Verdicts follow the registered decision rules; H1 "
        "and the two descriptive rows carry none."
    )
    return table(
        ["Measure (role)", "Early / stayers, No.", "Difference (95% CrI)", "Pr(>0)", "*P*", "MDE", "Verdict"],
        rows,
        "Table 2. Early renewers compared with stayers: regional pull (H2b), own-spending component (H2a), savings rates (H1) and the expected gain",
        notes,
        align="lrrrrrl",
        widths=[10, 4, 6, 2, 2, 2, 4],
    )


def table3() -> str:
    normal = {r["name"]: r for r in D["h3"]["posterior"]["normal"]}
    tdist = {r["name"]: r for r in D["h3"]["posterior"]["student_t"]}
    logit = CONV["H3_logit"]["coefficients"]
    rows = []
    for name, r in normal.items():
        t = tdist[name]
        lg = logit[name.removeprefix("b_")]
        test = r.get("test") or {}
        rows.append(
            [
                ("**" + r["label"] + "**") if r["core"] else r["label"],
                f"{num(r['mean'], 2)} ({interval(r['lo'], r['hi'], 2)})",
                prob(r["p_positive"]),
                pval(test.get("p")),
                (test.get("decision") or "adjustment").capitalize(),
                f"{num(t['mean'], 2)} ({interval(t['lo'], t['hi'], 2)})",
                f"{num(lg['odds_ratio'], 2)} ({interval(*lg['or_ci95'], 2)})",
            ]
        )
    s = D["h3"]["sample"]
    notes = (
        "Abbreviations: CrI, credible interval; OR, odds ratio; Pr(>0), posterior probability that the coefficient is "
        f"positive. Bayesian logistic regression of early renewal among "
        f"{s['n']} BASIC-track ACOs ({s['early']} early renewers; {s['excluded']['early']} early renewers and "
        f"{s['excluded']['stayer']} stayers excluded for a missing predictor). Continuous predictors are centered and divided by "
        "2 SD, so their coefficients are log-odds differences per 2 SD; binary predictors are centered, so theirs are "
        "per category (the BASIC level compares levels C-E with A-B). Core "
        "predictors (bold) are tested by direct simulation under the reduced model (10,000 simulated datasets); "
        "adjustment factors are estimates only. The own-spending component enters with a measurement-error model "
        f"($\\sigma_v$ = {num(VALIDATION['sigma_v_model'], 2)} pp). The Student-t column is the registered prior "
        "sensitivity analysis; the maximum-likelihood ORs are the conventional counterpart, reported only."
    )
    return table(
        ["Predictor", "Posterior mean (95% CrI)", "Pr(>0)", "*P*", "Verdict", "Student-t prior (95% CrI)", "Conventional OR (95% CI)"],
        rows,
        "Table 3. Decision model of early renewal among BASIC-track ACOs (H3)",
        notes,
        align="lrrrlrr",
        widths=[7, 6, 2, 2, 4, 6, 6],
    )


def table4() -> str:
    h4 = DID["H4"]
    pre = DID["pre_trend_check"]
    rob = DID["robustness"]
    twfe = DID["conventional"]["twfe"]["pooled"]
    pct_ci = [100 * (math.exp(x) - 1) for x in twfe["ci95"]]

    def row(label, n_e, n_c, est, lo, hi, p, bold=False):
        cells = [label, f"{n_e} / {n_c}", num(est, 1, sign=True), interval(lo, hi), pval(p)]
        return [f"**{c}**" for c in cells] if bold else cells

    rows = [
        row("H4, difference-in-differences", h4["n_early"], h4["n_stayer"], h4["percent"]["posterior_mean"], *h4["percent"]["eti95"], h4["p_value"], True),
        row("Pre-trend, PY2020 to PY2021", pre["n_early"], pre["n_stayer"], pre["percent"]["posterior_mean"], *pre["percent"]["eti95"], pre["p_value"]),
        row(
            "Trend-adjusted",
            rob["5_trend_adjusted"]["n_early"],
            rob["5_trend_adjusted"]["n_stayer"],
            rob["5_trend_adjusted"]["percent"]["posterior_mean"],
            *rob["5_trend_adjusted"]["percent"]["eti95"],
            rob["5_trend_adjusted"]["p_value"],
        ),
        row(
            "Risk-adjusted outcome",
            rob["1_risk_adjusted"]["n_early"],
            rob["1_risk_adjusted"]["n_stayer"],
            rob["1_risk_adjusted"]["percent"]["posterior_mean"],
            *rob["1_risk_adjusted"]["percent"]["eti95"],
            rob["1_risk_adjusted"]["p_value"],
        ),
        row(
            "Balanced panel (all 5 years)",
            rob["2_balanced"]["n_early"],
            rob["2_balanced"]["n_stayer"],
            rob["2_balanced"]["percent"]["posterior_mean"],
            *rob["2_balanced"]["percent"]["eti95"],
            rob["2_balanced"]["p_value"],
        ),
        [
            "Propensity-weighted",
            f"{rob['3_propensity_weighted']['n']} total",
            num(rob["3_propensity_weighted"]["percent"], 1, sign=True),
            "NA",
            pval(rob["3_propensity_weighted"]["p_value"]),
        ],
        row(
            "2020-01-01 cohort only",
            rob["4_cohort_2020"]["n_early"],
            rob["4_cohort_2020"]["n_stayer"],
            rob["4_cohort_2020"]["percent"]["posterior_mean"],
            *rob["4_cohort_2020"]["percent"]["eti95"],
            rob["4_cohort_2020"]["p_value"],
        ),
        [
            "Two-way fixed effects (conventional; 95% CI)",
            f"{DID['conventional']['twfe']['n_acos']} ACOs",
            num(100 * (math.exp(twfe["estimate"]) - 1), 1, sign=True),
            interval(*pct_ci),
            pval(twfe["p_value"]),
        ],
    ]
    eq = pre["equivalence"]
    notes = (
        "Abbreviations: CrI, credible interval; NA, not available (the propensity-weighted estimate has a permutation "
        f"P value but no interval; its largest weight is {num(rob['3_propensity_weighted']['max_weight'], 2)}); PY, "
        "performance year. The outcome is the change in log per-capita spending from "
        "PY2020-PY2021 to PY2022-PY2024, shown as a percent difference in spending growth, early renewers minus ACOs "
        "not yet renewed. A stayer's years after it renewed into a 2023 or 2024 agreement are excluded. Equivalence "
        f"condition: the pre-trend bound scaled to the distance between period midpoints ({num(eq['c_bar'], 2)} years) "
        f"is {num(100 * eq['scaled_bound'], 1)} log points, above the absolute H4 estimate of {num(100 * eq['abs_h4'], 1)} log "
        "points (1 log point = 0.01 in log spending, about 1%), so the condition does not hold and H4 is not read as an effect. "
        "The two-way fixed-effects model has one more ACO: the stayer with no post-period spending value keeps its "
        "pre-period years."
    )
    return table(
        ["Estimate", "Early / comparison, No.", "Difference, %", "95% CrI", "*P*"],
        rows,
        "Table 4. Spending growth after early renewal (H4), with the pre-trend and robustness estimates",
        notes,
        align="lrrrr",
        widths=[10, 4, 3, 4, 2],
    )


def etable_validation() -> str:
    o, s = VALIDATION["overall"], VALIDATION["step1"]
    rows = [["Rebuilt 2022 benchmark, all", str(o["n"]), num(o["spearman"], 2), num(o["median_abs_pct_error"], 1), num(o["slope"], 3), num(o["intercept"], 0)]]
    for step, label in (("1", "first phase-in step"), ("2", "second phase-in step")):
        b = VALIDATION["by_step"][step]
        rows.append(
            [
                f"\u00a0\u00a0\u00a0\u00a0ACOs at the {label}",
                str(b["n"]),
                num(b["spearman"], 2),
                num(b["median_abs_pct_error"], 1),
                num(b["slope"], 3),
                num(b["intercept"], 0),
            ]
        )
    rows.append(
        [
            "Own-spending part (step 1) vs CMS benchmark-year spending",
            str(s["n"]),
            num(s["spearman"], 2),
            num(s["median_abs_pct_error"], 1),
            num(s["slope"], 3),
            num(s["intercept"], 0),
        ]
    )
    notes = (
        f"Validation sample: regular renewers whose 2022 benchmarks CMS publishes ({o['n']} of {o['n'] + VALIDATION['excluded']} "
        "eligible; the rest lack either the rebuilt or the published benchmark). Early renewers were excluded from the "
        "sample, and the 2022 results file was filtered as it was loaded. Registered pass rule: Spearman correlation "
        "at least 0.80 and median absolute percentage error at most 5%; calibration only if the slope of actual on "
        "rebuilt fell outside 0.9 to 1.1. Result: passed, no calibration. The error SD of the step-1 check sets the "
        f"measurement-error SD of the own-spending component, $\\sigma_v$ = {num(VALIDATION['sigma_v_model'], 2)} pp."
    )
    return table(
        ["Check", "ACOs, No.", "Spearman $\\rho$", "Median absolute error, %", "Slope", "Intercept, $"],
        rows,
        "eTable 1. Validation of the rebuilt benchmark against benchmarks CMS published for regular renewers",
        notes,
        align="lrrrrr",
        widths=[10, 3, 3, 4, 2, 3],
    )


def etable_power() -> str:
    p = POWER
    rows = [
        [
            "H1, savings rate",
            f"SD {num(100 * p['h1']['sd'], 1)} pp (PY2016-PY2018)",
            f"{num(100 * p['h1']['mde'], 1)} pp",
            f"simulated power {num(100 * p['h1']['simulated_power_at_mde'], 1)}%",
        ],
        [
            "H2b, regional pull",
            f"SD {num(p['h2']['pull']['sd_stayers'], 1)} pp (stayers)",
            f"{num(p['h2']['pull']['mde'], 1)} pp",
            f"{num(p['h2']['pull']['mde_sd_units'], 2)} SD",
        ],
        [
            "H2a, own-spending component",
            f"SD {num(p['h2']['own']['sd_stayers'], 1)} pp (stayers)",
            f"{num(p['h2']['own']['mde'], 1)} pp",
            f"{num(p['h2']['own']['mde_sd_units'], 2)} SD",
        ],
        [
            "H4, spending change",
            f"SD {num(100 * p['h4']['sd_delta_pre'], 1)} log points (pre-period change)",
            f"{num(100 * p['h4']['mde_log'], 1)} log points",
            f"{num(100 * (math.exp(p['h4']['mde_log']) - 1), 1, sign=True)}% or {num(100 * (math.exp(-p['h4']['mde_log']) - 1), 1)}%",
        ],
    ]
    for key, label in (("pull", "regional pull"), ("own", "own-spending component"), ("basic_high", "higher BASIC level")):
        h = p["h3"][key]
        rows.append(
            [
                f"H3, {label}",
                f"true log-odds difference {num(h['coefficient'], 1)} per 2 SD",
                f"detected in {num(100 * h['detection_share'], 0)}%",
                f"of {h['n_datasets']} simulated datasets",
            ]
        )
    notes = (
        "Minimum detectable effects at 80% power, two-sided $\\alpha$ = .05, for 29 early renewers vs 277 stayers, computed after "
        "registration and committed before any confirmatory estimate; 1 log point = 0.01 in log spending. For H3, power was simulated only at a log-odds "
        "difference of 0.5; a predictor counts as detected when its 95% credible interval excludes zero."
    )
    return table(["Test", "Spread used", "Minimum detectable effect", "Note"], rows, "eTable 2. Power analysis", notes, align="llrl", widths=[5, 7, 4, 5])


def disagrees(r: dict) -> bool:
    """A row whose P value (< .05 or not) and 95% interval (excluding zero or not) disagree, which the plan says to note."""
    if r.get("p") is None or r.get("lo") is None:
        return False
    return (r["p"] < 0.05) != (r["lo"] > 0 or r["hi"] < 0)


def etable_robust_groups() -> str:
    rows = []
    for g in D["robustness"]["groups"]:
        rows.append([f"**{g['label']}**", "", "", ""])
        for r in g["rows"]:
            flag = disagrees(r)
            rows.append([f"\u00a0\u00a0\u00a0\u00a0{r['label']}" + ("^a^" if flag else ""), num(r["mean"], 1, sign=True), interval(r["lo"], r["hi"]), pval(r["p"])])
    notes = (
        "Early renewers minus stayers, in the units of Table 2. Item numbers refer to the registered plan's robustness "
        "list (section 5.5); '5.3' is the registered covariate-adjusted estimate with cohort only. Regression rows are "
        "robust Bayesian linear regressions (Student-t errors on the standardized variable, Normal(0, 1) priors) of the "
        "variable on early renewal and cohort (5.3) or cohort, track, level and size (item 1), with 95% credible "
        "intervals and no P value; the robust likelihood downweights a few large values. Median rows give the "
        "bootstrap posterior mean of the difference in medians; their P value tests the observed difference. "
        "^a^The P value and the 95% interval disagree about zero; the plan requires reporting both and noting the "
        "disagreement."
    )
    return table(["Analysis", "Difference", "95% interval", "*P*"], rows, "eTable 3. Robustness of the group comparisons", notes, align="lrrr")


def etable_robust_h3() -> str:
    rows = []
    for g in D["robustness"]["h3"]:
        rows.append([f"**{g['label']}**", "", "", ""])
        for r in g["rows"]:
            label = f"\u00a0\u00a0\u00a0\u00a0{r['label']}" + ("^a^" if disagrees(r) else "")
            rows.append([label, num(r["mean"], 2), interval(r["lo"], r["hi"], 2), pval(r["p"])])
    notes = (
        "Log-odds differences per 2 SD (BASIC level: C-E vs A-B). The Firth regression includes the core predictors and "
        "cohort, with profile-likelihood intervals and a direct-simulation P value; it would have decided H3 only if the "
        "Bayesian model had failed its convergence checks."
    )
    return table(["Analysis", "Coefficient", "95% interval", "*P*"], rows, "eTable 4. Robustness of the decision model (H3)", notes, align="lrrr")


def etable_h3_checks() -> str:
    c = CONFIRM["h3"]
    conv, tconv = c["convergence"], c["t_prior"]["convergence"]
    pc = c["predictive_checks"]
    tests = c["tests"]
    top = pc["deciles"][-1]
    rows = [
        ["Largest R-hat (Normal / Student-t prior)", f"{num(conv['max_rhat'], 3)} / {num(tconv['max_rhat'], 3)}"],
        ["Smallest bulk effective sample size", f"{conv['min_ess_bulk']:,.0f} / {tconv['min_ess_bulk']:,.0f}"],
        ["Divergent transitions", f"{conv['divergent']} / {tconv['divergent']}"],
        ["Fits needed (registered maximum: 2)", f"{conv['attempts']} / {tconv['attempts']}"],
        [
            "Prior predictive share renewing early, median (95% range)",
            "{}% ({}% to {}%)".format(*(num(100 * pc["prior_share_quantiles"][q], 0) for q in ("0.5", "0.025", "0.975"))),
        ],
        [
            "Observed early renewers (posterior predictive 95% range)",
            f"{pc['observed_count']} ({num(pc['replicated_count_eti95'][0], 0)} to {num(pc['replicated_count_eti95'][1], 0)})",
        ],
        ["Top predicted decile: observed vs predicted share", f"{num(100 * top['observed'], 0)}% vs {num(100 * top['predicted'], 0)}%"],
        [
            "Direct-simulation refits not converged (pull / own / BASIC level)",
            " / ".join(f"{num(100 * tests[k]['share_refits_not_converged'], 2)}%" for k in ("pull", "own", "basic_high")),
        ],
        [
            "Overall test: largest absolute core coefficient (reduced sampler settings)",
            f"{num(c['overall_test']['observed'], 2)}, *P* = {pval(c['overall_test']['p_value'])}",
        ],
    ]
    return table(["Check", "Result"], rows, "eTable 5. Convergence and predictive checks of the decision model (H3)", align="lr")


def etable_conventional() -> str:
    rows = []
    for key, label, scale in (("H2b", "H2b, regional pull", 1), ("H2a", "H2a, own-spending component", 1), ("H1", "H1, savings rate PY2020", 100)):
        for m, mlabel in (("welch", "Welch t test"), ("ols_hc2", "OLS, HC2 errors, cohort"), ("ols_hc2_adjusted", "OLS, HC2 errors, adjusted")):
            r = CONV[key][m]
            rows.append(
                [
                    label if m == "welch" else "",
                    mlabel,
                    num(r["difference"] * scale, 1, sign=True),
                    interval(r["ci95"][0] * scale, r["ci95"][1] * scale),
                    pval(r["p_value"]),
                ]
            )
    es = DID["conventional"]["twfe"]["event_study"]
    for i, year in enumerate(("2020", "2022", "2023", "2024")):
        e = es[year]
        rows.append(
            [
                "H4, event study (TWFE)" if i == 0 else "",
                f"PY{year} vs PY2021",
                num(100 * e["estimate"], 1, sign=True),
                interval(100 * e["ci95"][0], 100 * e["ci95"][1]),
                pval(e["p_value"]),
            ]
        )
    notes = (
        "Reported only; not used for any decision. Differences are early renewers minus stayers (pp; H1 in pp of "
        "savings rate). Adjusted OLS adds track, level and size to cohort. Event-study coefficients are log points "
        "(0.01 in log spending) relative to PY2021, from two-way fixed effects with errors clustered by ACO. TWFE, two-way fixed effects."
    )
    return table(["Hypothesis", "Method", "Estimate", "95% CI", "*P*"], rows, "eTable 6. Conventional (frequentist) counterparts", notes, align="llrrr")


def etable_agreement() -> str:
    names = {"supported": "Supported", "contradicted": "Contradicted", "undetermined": "Undetermined"}
    rows = [[a["claim"], names[a["confirmatory"]], names[a["conventional"]], "Yes" if a["agree"] else "No"] for a in D["agreement"]]
    notes = (
        "For H2a and H2b the registered conventional counterpart is OLS with HC2 errors; for H3, maximum-likelihood "
        "logistic regression; for H4, two-way fixed effects. 'Undetermined' for H4 is the registered label for 'no "
        "detectable difference'."
    )
    return table(["Claim", "Registered method", "Conventional method", "Agree"], rows, "eTable 7. Agreement of registered and conventional verdicts", notes, align="lllc")


def etable_attrition() -> str:
    counts = {(r["grp"], r["py"], r["status"]): r["n"] for r in DID["attrition"]}
    years = (2022, 2023, 2024)
    rows = []
    for grp, label in (("early", "Early renewers (29)"), ("stayer", "Stayers (277)")):
        for status, slabel in (
            ("included", "included"),
            ("absent", "left the program"),
            ("later renewal", "renewed (no longer 'not yet renewed')"),
            ("no spending value", "no spending value"),
        ):
            if grp == "early" and status == "no spending value":
                continue
            rows.append([f"{label}: {slabel}", *(str(counts.get((grp, y, status), 0)) for y in years)])
    post = {g: sum(counts.get((g, y, "included"), 0) for y in years) for g in ("early", "stayer")}
    n_h4 = {"early": DID["sample"]["early"], "stayer": DID["sample"]["comparison"]}
    notes = (
        f"Required by the registered plan (section 4.5). PY2020 and PY2021 include all {counts[('early', 2021, 'included')]} "
        f"early renewers and {counts[('stayer', 2021, 'included')]} stayers. Follow-up: a mean of "
        f"{num(post['early'] / n_h4['early'], 2)} included post-period years per early renewer and "
        f"{num(post['stayer'] / n_h4['stayer'], 2)} per comparison ACO (of 3)."
    )
    return table(["Group and status", "PY2022", "PY2023", "PY2024"], rows, "eTable 8. Attrition from the H4 spending panel, by group and year", notes, align="lrrr")


def etable_exploratory() -> str:
    rows = []
    for g in D["exploratory"]["alternative_exposures"]:
        rows.append([f"**{g['label']}** ({g['unit']})", "", ""])
        for r in g["rows"]:
            rows.append(
                [
                    f"\u00a0\u00a0\u00a0\u00a0{r['label']}",
                    num(r["mean"], 2 if g["unit"] == "log-odds" else 1, sign=True),
                    interval(r["lo"], r["hi"], 2 if g["unit"] == "log-odds" else 1),
                ]
            )
    rows.append(["**Census region in H3** (log-odds vs Northeast)", "", ""])
    for r in D["exploratory"]["region"]["rows"]:
        rows.append([f"\u00a0\u00a0\u00a0\u00a0{r['label']}", num(r["mean"], 2, sign=True), interval(r["lo"], r["hi"], 2)])
    region = EXPL["census_region_in_h3"]
    notes = (
        "Labeled exploratory in the registered plan (section 5.6): no predictions and no verdicts. "
        f"{region['excluded_no_region']} of the 334 ACOs have no census region; the region model's sample is "
        f"{region['sample']['n']} ACOs ({region['sample']['early']} early renewers), as in H3."
    )
    return table(["Analysis", "Estimate", "95% CrI"], rows, "eTable 9. Exploratory analyses", notes, align="lrr")


def etable_enhanced() -> str:
    labels = (
        ("sav_rate_2020", "Savings rate, PY2020, pp", 100),
        ("pull", "Regional pull, pp", 1),
        ("own", "Own-spending component, pp", 1),
        ("regional_comp", "Regional component, pp", 1),
    )
    acos = EXPL["enhanced_early_renewers"]
    rows = [
        [label] + [f"{num(a[key]['value'] * scale, 1, sign=key != 'sav_rate_2020')} ({num(a[key]['stayer_percentile'], 0)})" for a in acos]
        for key, label, scale in labels
    ]
    notes = (
        "The 2 early renewers already in ENHANCED in PY2021, for whom renewal could not raise the sharing rate, reported "
        "individually against the stayer distribution as the plan requires (section 5.6). Values with the stayers' "
        "percentile in parentheses. Exploratory; no test."
    )
    header = ["Variable"] + [f"ACO {i + 1} ({a['cohort']} cohort)" for i, a in enumerate(acos)]
    return table(header, rows, "eTable 10. The 2 early renewers already in ENHANCED", notes, align="lrr")


def etable_spending() -> str:
    rows = [
        [
            str(r["start_year"]),
            str(r["agreement_year"]),
            "Yes" if r["scheduled_benchmark_year"] else "No",
            "Early renewers" if r["early_renewer_from_2020"] else "Other ACOs",
            str(r["n_acos"]),
            f"{r['mean_pc']:,.0f}",
        ]
        for r in EXPL["spending_by_agreement_year"]
    ]
    notes = (
        "Mean per-capita spending (US dollars) of assigned beneficiaries by agreement start year and agreement year "
        "(performance year - start year + 1), PY2020-PY2024 (plan section 5.6). Agreement years 3-5 are the scheduled "
        "benchmark years of the next agreement; early renewers out of a 2020 agreement are shown separately. Benchmark-year "
        "status cannot be separated from tenure here, so this is description only."
    )
    return table(
        ["Agreement start", "Agreement year", "Scheduled benchmark year", "Group", "ACOs, No.", "Mean spending, $"],
        rows,
        "eTable 11. Per-capita spending by agreement year",
        notes,
        align="rrllrr",
    )


def etable_posthoc() -> str:
    reg, er = POSTHOC["regular_renewers_change"], POSTHOC["early_renewers_realized"]
    rv, upd = er["rebuilt_vs_realized"], POSTHOC["benchmark_update_2021_2022"]

    def check(label: str, a: dict) -> list[str]:
        return [
            label,
            str(a["n"]),
            num(a["spearman"], 2),
            num(a["median_abs_error"], 1),
            num(a["mean_error"], 1, sign=True),
            f"{num(100 * a['same_sign_share'], 0)}%",
            f"{num(a['rebuilt']['mean'], 1, sign=True)} / {num(a['actual']['mean'], 1, sign=True)}",
        ]

    rows = [
        check("Regular renewers: rebuilt vs actual change", reg),
        check("Early renewers: rebuilt gain vs realized reset", rv),
    ]
    a = er["all_with_hist_2022"]
    pooled, stayers = PULL["pooled"]["correlations"], PULL["stayers"]["correlations"]
    notes = (
        "Post hoc and exploratory; not registered (stharrold.github.io, analysis/mssp-benchmark-ratchet/posthoc/). "
        "Changes are 100 x (2022 historical benchmark - PY2021 updated benchmark) / PY2021 updated benchmark, in "
        "percentage points of the PY2021 benchmark, both in 2021 dollars: rebuilt from public files, or actual as CMS "
        "published it in the PY2022 results file. Error = rebuilt - actual. Realized reset, all "
        f"{er['n_with_hist_2022']} early renewers: mean {num(a['mean'], 1, sign=True)}, median {num(a['median'], 1, sign=True)}, "
        f"{num(100 * a['share_negative'], 0)}% below the PY2021 benchmark. Updated benchmark PY2021 to PY2022 (includes the "
        f"annual update for both groups): early renewers {num(upd['group_means']['early'], 1, sign=True)}% and stayers "
        f"{num(upd['group_means']['stayer'], 1, sign=True)}% on average; within-cohort difference "
        f"{num(upd['posterior_mean'], 1, sign=True)} points (95% CrI, {interval(*upd['eti95'])}; *P* = {pval(upd['p_value'])}). "
        f"Regional pull and past savings ({pooled['sav_rate_2020']['n']} early renewers and stayers with the variable): "
        f"Spearman $\\rho$ {num(pooled['sav_rate_2020']['spearman'], 2)} with the PY2020 savings rate, "
        f"{num(pooled['sav_rate_2021']['spearman'], 2)} with the PY2021 savings rate and "
        f"{num(pooled['own']['spearman'], 2, sign=True)} with the own-spending component "
        f"(stayers alone: {num(stayers['sav_rate_2020']['spearman'], 2)}, {num(stayers['sav_rate_2021']['spearman'], 2)} and "
        f"{num(stayers['own']['spearman'], 2, sign=True)})."
    )
    return table(
        ["Check", "ACOs, No.", "Spearman $\\rho$", "Median absolute error", "Mean error", "Same sign", "Mean rebuilt / actual"],
        rows,
        "eTable 12. Post hoc checks of the expected gain against CMS's published 2022 benchmarks, and of the regional pull against past savings",
        notes,
        align="lrrrrrr",
        widths=[10, 3, 3, 3, 3, 3, 4],
    )


TABLES = {
    "table1": table1,
    "table2": table2,
    "table3": table3,
    "table4": table4,
    "etable1-validation": etable_validation,
    "etable2-power": etable_power,
    "etable3-robustness-groups": etable_robust_groups,
    "etable4-robustness-h3": etable_robust_h3,
    "etable5-h3-checks": etable_h3_checks,
    "etable6-conventional": etable_conventional,
    "etable7-agreement": etable_agreement,
    "etable8-attrition": etable_attrition,
    "etable9-exploratory": etable_exploratory,
    "etable10-enhanced": etable_enhanced,
    "etable11-spending": etable_spending,
    "etable12-posthoc": etable_posthoc,
}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, build in TABLES.items():
        (OUT / f"{name}.md").write_text(build())
    print(f"wrote {len(TABLES)} tables to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()

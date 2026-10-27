"""Draw the manuscript's four figures from the committed results: 300 dpi PNGs on an opaque white background.

Figure 1 is the flow of ACOs into each analysis; Figures 2-4 are interval plots of the group comparisons, the
decision model and the spending estimates. One mark color throughout, so identity never rests on color.

Usage: uv run python scripts/make_figures.py
"""

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from results import ROOT, dashboard, load, num  # noqa: E402

OUT = ROOT / "figures"
INK, MUTED, GRID, MARK, BAND, BOX = "#111111", "#55534e", "#d9d8d3", "#2a62b8", "#e8eef8", "#f4f4f2"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID, "savefig.facecolor": "white"})

D = dashboard()
CONFIRM, DID, EXPL = load("confirm"), load("did"), load("exploratory")


def save(fig, name: str) -> None:
    fig.savefig(OUT / f"{name}.png", dpi=300, facecolor="white", bbox_inches="tight", pad_inches=0.08, metadata={"Software": None})
    plt.close(fig)


def forest(ax, rows, xlabel, zero=0.0, band=None, digits=1):
    """rows: (label, mean, lo, hi, bold). One interval per row; the value printed at the right edge."""
    ys = list(range(len(rows)))[::-1]
    if band:
        ax.axvspan(-band, band, color=BAND, zorder=0, lw=0)
    ax.axvline(zero, color=MUTED, lw=0.8, zorder=1)
    for y, (_label, mean, lo, hi, _bold) in zip(ys, rows, strict=True):
        if lo is not None:
            ax.plot([lo, hi], [y, y], color=MARK, lw=2, solid_capstyle="round", zorder=2)
        ax.plot(mean, y, "o", color=MARK, ms=5.5, mec="white", mew=1.2, zorder=3)
        text = f"{num(mean, digits, sign=True)}" + (f" ({num(lo, digits)} to {num(hi, digits)})" if lo is not None else "")
        ax.text(1.02, y, text, transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=8.5, color=INK)
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.5, color=INK)
    for tick, r in zip(ax.get_yticklabels(), rows, strict=True):
        tick.set_fontweight("bold" if r[4] else "normal")
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xlabel(xlabel, fontsize=8.5, color=MUTED)
    ax.tick_params(axis="x", colors=MUTED, labelsize=8, length=0)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)


def panel_label(ax, letter, title):
    ax.set_title(f"{letter}  {title}", loc="left", fontsize=9.5, fontweight="bold", color=INK, pad=8)


def figure1() -> None:
    """Flow of ACOs into each analysis, from the counts in the results files."""
    cohorts = {}
    for r in EXPL["who_renewed"]:
        cohorts[(r["grp"], r["cohort"])] = cohorts.get((r["grp"], r["cohort"]), 0) + r["n"]
    n = {g: cohorts[(g, "2019-07")] + cohorts[(g, "2020-01")] for g in ("early", "stayer", "leaver")}
    c19 = sum(v for (g, c), v in cohorts.items() if c == "2019-07")
    c20 = sum(v for (g, c), v in cohorts.items() if c == "2020-01")
    gain = CONFIRM["groups"]["H2b_pull"]
    h3 = CONFIRM["h3"]["sample"]
    basic = {"early": h3["early"] + h3["excluded"]["early"], "stayer": h3["n"] - h3["early"] + h3["excluded"]["stayer"]}
    h4 = DID["sample"]

    fig = plt.figure(figsize=(7.2, 5.6))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def box(x, y, w, h, lines, bold_first=True):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=BOX, ec=MUTED, lw=0.7))
        for i, line in enumerate(lines):
            ax.text(x + w / 2, y + h - 2.6 - i * 3.6, line, ha="center", va="top", fontsize=7.8, color=INK, fontweight="bold" if (i == 0 and bold_first) else "normal")

    def arrow(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops={"arrowstyle": "-|>", "color": MUTED, "lw": 0.7, "shrinkA": 0, "shrinkB": 0})

    box(
        25,
        85,
        50,
        13,
        [
            f"{sum(n.values())} ACOs in the 2019 and 2020 agreement cohorts",
            f"July 1, 2019: {c19}; January 1, 2020: {c20}",
            "(MSSP enrollment files, PY2021 record required)",
        ],
    )
    arrow(50, 84.6, 50, 80)
    ax.plot([16, 84], [80, 80], color=MUTED, lw=0.7)
    for x in (16, 50, 84):
        arrow(x, 80, x, 75.5)
    box(3, 59.5, 26, 16, ["Early renewers", f"{n['early']} ACOs", "new agreement", "January 1, 2022"])
    box(37, 59.5, 26, 16, ["Stayers", f"{n['stayer']} ACOs", "remained in their", "agreements"])
    box(71, 59.5, 26, 16, ["Left after PY2021", f"{n['leaver']} ACOs", "described only;", "in no registered test"])

    rows = [
        ("H1: savings rates", [f"{CONFIRM['groups']['H1_sav_rate_2020']['n_early']} vs {CONFIRM['groups']['H1_sav_rate_2020']['n_stayer']}", "all ACOs"]),
        (
            "H2a, H2b: expected gain",
            [
                f"{gain['n_early']} vs {gain['n_stayer']}",
                f"excluded {gain['excluded']['early']} and {gain['excluded']['stayer']}:",
                "ESRD county counts all",
                "suppressed (post hoc query)",
            ],
        ),
        (
            "H3: decision model",
            [
                f"{h3['early']} vs {h3['n'] - h3['early']}",
                f"BASIC track: {basic['early']} and {basic['stayer']};",
                f"excluded {h3['excluded']['early']} and {h3['excluded']['stayer']}",
                "for a missing predictor",
            ],
        ),
        ("H4: spending", [f"{h4['early']} vs {h4['comparison']}", "comparison: not yet", "renewed; 1 stayer has", "no spending value"]),
    ]
    xs = (2, 26.5, 51, 75.5)
    ax.plot([xs[0] + 11.25, xs[-1] + 11.25], [54, 54], color=MUTED, lw=0.7)
    ax.plot([16, 16], [59.1, 54], color=MUTED, lw=0.7)
    ax.plot([50, 50], [59.1, 54], color=MUTED, lw=0.7)
    for x, (title, lines) in zip(xs, rows, strict=True):
        arrow(x + 11.25, 54, x + 11.25, 50.5)
        box(x, 29, 22.5, 21.5, [title, *lines])
    ax.text(
        50,
        25,
        "Early renewers vs stayers in each analysis (No.). The benchmark approximation was validated first on a separate sample:",
        ha="center",
        fontsize=7.6,
        color=MUTED,
    )
    val = load("validation")
    box(
        25,
        9,
        50,
        12,
        [
            "Validation sample",
            f"{val['overall']['n']} regular renewers with a published 2022 benchmark",
            f"(of {val['overall']['n'] + val['excluded']} eligible); early renewers excluded",
        ],
    )
    save(fig, "figure1-flow")


def figure2() -> None:
    c = {r["key"]: r for r in D["comparisons"]["rows"]}
    fig, (a, b) = plt.subplots(2, 1, figsize=(7.2, 3.9), gridspec_kw={"height_ratios": [4, 2], "hspace": 0.75})
    forest(
        a,
        [
            ("H2b  Regional pull (primary)", c["H2b_pull"]["mean"], c["H2b_pull"]["lo"], c["H2b_pull"]["hi"], True),
            ("Regional component", c["regional_comp"]["mean"], c["regional_comp"]["lo"], c["regional_comp"]["hi"], False),
            ("H2a  Own-spending component", c["H2a_own"]["mean"], c["H2a_own"]["lo"], c["H2a_own"]["hi"], False),
            ("Total expected gain", c["gain"]["mean"], c["gain"]["lo"], c["gain"]["hi"], False),
        ],
        "Early renewers minus stayers, percentage points of the current benchmark",
    )
    a.set_xlim(-5, 7)
    panel_label(a, "A", f"Expected gain from a reset ({c['gain']['n_early']} vs {c['gain']['n_stayer']} ACOs)")
    forest(
        b,
        [
            ("H1  Savings rate, PY2020", c["H1_sav_rate_2020"]["mean"], c["H1_sav_rate_2020"]["lo"], c["H1_sav_rate_2020"]["hi"], False),
            ("H1  Savings rate, PY2021", c["H1_sav_rate_2021"]["mean"], c["H1_sav_rate_2021"]["lo"], c["H1_sav_rate_2021"]["hi"], False),
        ],
        "Early renewers minus stayers, percentage points",
    )
    b.set_xlim(-5, 7)
    panel_label(b, "B", f"Savings rates ({c['H1_sav_rate_2020']['n_early']} vs {c['H1_sav_rate_2020']['n_stayer']} ACOs)")
    save(fig, "figure2-comparisons")


def figure3() -> None:
    rows = [(r["label"], r["mean"], r["lo"], r["hi"], r["core"]) for r in D["h3"]["posterior"]["normal"]]
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    forest(ax, rows, "Log-odds difference per 2 SD (BASIC level: C-E vs A-B); shaded: the prior's central 95%", band=D["h3"]["prior_band"]["normal"], digits=2)
    ax.set_xlim(-2.6, 2.6)
    s = D["h3"]["sample"]
    panel_label(ax, "", f"Early renewal among {s['n']} BASIC-track ACOs ({s['early']} early renewers); bold: core predictors")
    save(fig, "figure3-decision-model")


def figure4() -> None:
    es = DID["conventional"]["twfe"]["event_study"]
    years = [2020, 2021, 2022, 2023, 2024]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.2), gridspec_kw={"width_ratios": [1.15, 1.25], "wspace": 0.95})
    means = [0.0 if y == 2021 else 100 * es[str(y)]["estimate"] for y in years]
    a.axhline(0, color=MUTED, lw=0.8)
    a.axvspan(2021.5, 2024.5, color=BAND, lw=0, zorder=0)
    for y, m in zip(years, means, strict=True):
        if y != 2021:
            lo, hi = (100 * v for v in es[str(y)]["ci95"])
            a.plot([y, y], [lo, hi], color=MARK, lw=2, solid_capstyle="round", zorder=2)
        a.plot(y, m, "o", color=MARK if y != 2021 else "white", mec=MARK, ms=5.5, mew=1.2, zorder=3)
    a.set_xticks(years)
    a.set_xticklabels([str(y) if y != 2021 else "2021\n(ref.)" for y in years], fontsize=7.5)
    a.set_xlabel("Performance year", fontsize=8, color=MUTED)
    a.set_ylabel("Early renewers minus comparison,\nlog points", fontsize=8, color=MUTED)
    a.tick_params(colors=MUTED, labelsize=7.5, length=0)
    a.grid(axis="y", color=GRID, lw=0.6)
    a.set_axisbelow(True)
    lo_y, hi_y = a.get_ylim()
    a.set_ylim(lo_y, hi_y + 1.6)
    a.text(2023, hi_y + 1.3, "after renewal", ha="center", va="top", fontsize=7.5, color=MUTED)
    for side in ("top", "right"):
        a.spines[side].set_visible(False)
    panel_label(a, "A", "Event study (conventional, TWFE)")

    labels = {
        "H4 difference-in-differences": ("H4 (registered)", True),
        "Trend-adjusted": ("Trend-adjusted", False),
        "Propensity-weighted": ("Propensity-weighted", False),
        "Risk-adjusted outcome": ("Risk-adjusted outcome", False),
        "Balanced panel": ("Balanced panel", False),
        "2020-01-01 cohort only": ("2020-01-01 cohort only", False),
        "Two-way fixed effects": ("Two-way fixed effects", False),
    }
    rows = [(labels[e["label"]][0], e["mean"], e["lo"], e["hi"], labels[e["label"]][1]) for e in D["h4"]["estimates"]]
    forest(b, rows, "Difference in spending growth, %")
    b.set_xlim(-13, 6)
    panel_label(b, "B", "Registered, robustness and conventional estimates")
    save(fig, "figure4-spending")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for build in (figure1, figure2, figure3, figure4):
        build()
    assert math.isclose(D["h4"]["estimates"][0]["mean"], DID["H4"]["percent"]["posterior_mean"])
    print(f"wrote 4 figures to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()

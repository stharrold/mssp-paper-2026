"""Load the study's committed results and format numbers for the manuscript.

Two inputs, both copied unchanged from stharrold/stharrold.github.io (see data/README.md for commits and hashes):

- data/results/*.json, the seven results files the registered pipeline wrote;
- data/dashboard-data.json, the post's dashboard data, built from those files by report/dashboard_data.py. It already
  puts the group comparisons, robustness checks and H4 estimates in reporting units (percentage points, percent).

Every number in the manuscript's tables comes through this module, and scripts/check_numbers.py checks the prose
against the same values. Standard library only.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(name: str) -> dict:
    return json.loads((DATA / "results" / f"{name}.json").read_text())


def dashboard() -> dict:
    return json.loads((DATA / "dashboard-data.json").read_text())


def num(x: float | None, digits: int = 1, sign: bool = False) -> str:
    """A number for a table: fixed decimals, a true minus sign, an optional explicit plus."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "NA"
    text = f"{x:+.{digits}f}" if sign else f"{x:.{digits}f}"
    if text in ("-0." + "0" * digits, "+0." + "0" * digits) or (digits == 0 and text in ("-0", "+0")):
        text = text[1:]
    return text.replace("-", "−")


def interval(lo: float | None, hi: float | None, digits: int = 1) -> str:
    if lo is None or hi is None:
        return "NA"
    return f"{num(lo, digits)} to {num(hi, digits)}"


def pval(p: float | None) -> str:
    """AMA style: no leading zero, 2 digits, 3 below .01, '<.001' below .001."""
    if p is None:
        return ""
    if p < 0.001:
        return "<.001"
    digits = 3 if p < 0.01 else 2
    text = f"{p:.{digits}f}"
    if text == "1.00":
        return ">.99"
    return text[1:] if text.startswith("0") else text


def pct(x: float, digits: int = 0) -> str:
    return f"{100 * x:.{digits}f}%"

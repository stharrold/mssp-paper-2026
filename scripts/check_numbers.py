"""Check every number in the manuscript's prose against the committed results.

The tables are generated from the results files, but the prose of paper.md, supplement.md and strobe.md is typed. This script
extracts each number from the prose and accepts it if it matches, at the precision written, some value in the
results files (data/results/*.json and data/dashboard-data.json) under one of the reporting transforms: as is,
x100 (fractions to percent or log points), or 100 x (exp(x) - 1) (log differences to percent), with either sign.
Numbers that do not come from the results (years, regulation section numbers, figures quoted from cited papers,
values from the post-hoc diagnostic query) must be listed with a reason in data/number-allowlist.tsv.

That single-number test is weak: with about 2,700 candidate values, a random 1-decimal number matches by chance
about 90% of the time (2 decimals: about 40%). The stronger test is on intervals: every "estimate (lower to upper)"
or "estimate; 95% CrI, lower to upper" in the prose must match the mean and both bounds of one results record, under
one transform, with signs. The review pass still checks that each number belongs to its sentence.

Exit status 1 if any number or interval is unexplained. Standard library only.

Usage: python3 scripts/check_numbers.py [paper.md supplement.md strobe.md]
"""

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NUMBER = re.compile(r"(?<![\w.])[−-]?(?:\d{1,3}(?:,\d{3})+|\d+)?(?:\.\d+)?%?")
SKIP = [
    re.compile(r"\[@[^\]]*\]"),  # citations
    re.compile(r"\]\([^)]*\)"),  # link targets
    re.compile(r"https?://\S+"),
    re.compile(r"doi:\S+", re.I),
    re.compile(r"\{\{include [^}]*\}\}"),
    re.compile(r"\bPY\d{4}\b"),  # performance years
    re.compile(r"\b(?:19|20)\d{2}\b"),  # calendar years
    re.compile(r"\b4[25] CFR\b|\b\d{2,3}\.\d{3}\b"),  # regulation citations
    re.compile(r"\bH[1-4][ab]?\b"),  # hypothesis labels
    re.compile(r"\b(?:e?Table|Figure|Supplement|Multimedia Appendix|Additional file|Appendix|STROBE item|section|item|step|Level)s? [\d.]+(?:-\d+)?", re.I),
    re.compile(r"\b[0-9a-f]{7,64}\b"),  # commit and file hashes
    re.compile(r"\{[^}]*\}"),  # attributes and LaTeX groups
]


def leaves(x):
    if isinstance(x, dict):
        for v in x.values():
            yield from leaves(v)
    elif isinstance(x, list):
        for v in x:
            yield from leaves(v)
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        yield float(x)


def candidates() -> list[float]:
    values = set()
    sources = [*sorted((DATA / "results").glob("*.json")), *sorted((DATA / "posthoc").glob("*.json")), DATA / "dashboard-data.json"]
    for path in sources:
        for v in leaves(json.loads(path.read_text())):
            values.update({v, 100 * v})
            if abs(v) < 5:
                values.add(100 * math.expm1(v))
    return sorted(abs(v) for v in values if math.isfinite(v))


TRIPLE = re.compile(
    r"(?P<a>[\u2212-]?\d[\d.,]*)%?(?: percentage)?(?: points?)?(?: \(|; )(?:95% Cr?I, )?"
    r"(?P<lo>[\u2212-]?\d[\d.]*)%? to (?P<hi>[\u2212-]?\d[\d.]*)%?"
)


PAIR = re.compile(r"(?<![\w.])(?P<lo>[\u2212-]?\d[\d.]*)%? to (?P<hi>[\u2212-]?\d[\d.]*)%?")


def records() -> list[list[float]]:
    """Every dict in the results, as the numbers directly in it or in its short lists (intervals), per transform."""
    out = []

    def walk(x):
        if isinstance(x, dict):
            nums = []
            for v in x.values():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    nums.append(float(v))
                elif isinstance(v, list) and len(v) == 2 and all(isinstance(e, (int, float)) for e in v):
                    nums.extend(float(e) for e in v)
                elif isinstance(v, dict):
                    nums.extend(float(e) for e in v.values() if isinstance(e, (int, float)) and not isinstance(e, bool))
            for transform in (lambda z: z, lambda z: 100 * z, lambda z: 100 * math.expm1(z) if abs(z) < 5 else math.nan):
                out.append([transform(n) for n in nums])
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    for path in [*sorted((DATA / "results").glob("*.json")), *sorted((DATA / "posthoc").glob("*.json")), DATA / "dashboard-data.json"]:
        walk(json.loads(path.read_text()))
    return out


def close(token: str, value: float) -> bool:
    text = token.replace("\u2212", "-").replace(",", "")
    digits = len(text.split(".")[1]) if "." in text else 0
    return math.isfinite(value) and abs(value - float(text)) <= 0.5 * 10**-digits + 1e-9


def pair_ok(lo: str, hi: str, recs: list[list[float]]) -> bool:
    return any(any(close(lo, v) for v in r) and any(close(hi, v) for v in r) for r in recs)


def triple_ok(a: str, lo: str, hi: str, recs: list[list[float]]) -> bool:
    return any(any(close(a, v) for v in r) and any(close(lo, v) for v in r) and any(close(hi, v) for v in r) for r in recs)


def allowlist() -> dict[str, str]:
    path = DATA / "number-allowlist.tsv"
    out = {}
    for line in path.read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            value, reason = line.split("\t", 1)
            out[value] = reason
    return out


def matches(token: str, values: list[float]) -> bool:
    text = token.replace("−", "").replace("-", "").replace("%", "").replace(",", "")
    if not text or text == ".":
        return True
    written = float(text)
    digits = len(text.split(".")[1]) if "." in text else 0
    tol = 0.5 * 10**-digits + 1e-9
    return any(abs(v - written) <= tol for v in values)


def prose(path: Path) -> list[tuple[int, str]]:
    out = []
    in_math = False
    for i, line in enumerate(path.read_text().splitlines(), 1):
        if line.strip().startswith("$$"):
            in_math = not in_math if line.strip() == "$$" else in_math
            continue
        if in_math or line.startswith("|") or line.startswith(":"):
            continue
        out.append((i, line))
    return out


def main() -> None:
    files = [Path(a) for a in sys.argv[1:]] or [ROOT / "paper.md", ROOT / "supplement.md", ROOT / "strobe.md"]
    values = candidates()
    recs = records()
    allowed = allowlist()
    unexplained = []
    n_triples = n_pairs = 0
    for path in files:
        lines = prose(path)
        paragraphs, current = [], []
        for lineno, line in lines + [(0, "")]:
            if line.strip():
                current.append((lineno, line))
            elif current:
                paragraphs.append((current[0][0], " ".join(text for _, text in current)))
                current = []
        for lineno, para in paragraphs:
            for t in TRIPLE.finditer(para):
                n_triples += 1
                key = f"{t['a']} ({t['lo']} to {t['hi']})"
                if key not in allowed and not triple_ok(t["a"].rstrip(".,"), t["lo"], t["hi"].rstrip(".,"), recs):
                    unexplained.append(f"{path.name}:{lineno}: interval {key}")
            for t in PAIR.finditer(para):
                lo, hi = t["lo"], t["hi"].rstrip(".,")
                if "." not in lo + hi:
                    continue  # integer ranges ("14 to 37" counts, "1 to 10" suppression) are covered by the single test
                n_pairs += 1
                if f"{lo} to {hi}" not in allowed and not pair_ok(lo, hi, recs):
                    unexplained.append(f"{path.name}:{lineno}: interval {lo} to {hi}")
        for lineno, line in lines:
            text = re.sub(r"\$[^$]+\$", " ", line)  # inline math
            for pattern in SKIP:
                text = pattern.sub(" ", text)
            for m in NUMBER.finditer(text):
                token = m.group().rstrip(".,")
                bare = token.replace("−", "-").lstrip("-").rstrip("%")
                if not re.search(r"\d", token) or bare in allowed or token in allowed:
                    continue
                if bare.replace(",", "").isdigit() and int(bare.replace(",", "")) <= 10:
                    continue  # small counts (3 steps, 4 types) are checked by reading, not here
                if not matches(token, values):
                    unexplained.append(f"{path.name}:{lineno}: {token}")
    for u in unexplained:
        print(u)
    print(f"{n_triples} estimate-interval triples and {n_pairs} interval pairs checked")
    print(f"{len(unexplained)} unexplained" if unexplained else "every number and interval matches the results or the allowlist")
    sys.exit(1 if unexplained else 0)


if __name__ == "__main__":
    main()

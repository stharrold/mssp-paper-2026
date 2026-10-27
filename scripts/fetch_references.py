"""Fetch the metadata of every DOI-cited reference from Crossref, as CSL-JSON, into references/doi.json.

Each entry's id is the citation key used in paper.md, so a reference's title, authors, journal and pages come from
the DOI registration rather than from hand typing. References without a DOI (regulations, CMS datasets, software
without a paper) are written by hand in references/other.bib. Standard library only.

Usage: python3 scripts/fetch_references.py
"""

import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "references" / "doi.json"

DOIS = {
    # MSSP literature
    "mcwilliams2016": "10.1056/NEJMsa1600142",
    "mcwilliams2018": "10.1056/NEJMsa1803388",
    "mcwilliams2020": "10.1111/1468-0009.12468",
    "markovitz2019exit": "10.7326/M18-2539",
    "markovitz2019risk": "10.1377/hlthaff.2018.05407",
    "bond2025": "10.1001/jama.2025.3870",
    "douven2015": "10.1377/hlthaff.2014.0444",
    "rose2016": "10.1377/hlthaff.2015.1026",
    "lyu2023": "10.1377/hlthaff.2022.01061",
    "chen2025": "10.1086/726748",
    "srivastava2026": "10.1001/jamanetworkopen.2026.0166",
    "bleser2019": "10.1377/hlthaff.2018.05097",
    "zhu2023": "10.1111/jrh.12672",
    "trombley2022": "10.1377/hlthaff.2020.01819",
    "ying2023": "10.1007/s11606-022-07947-x",
    "ying2024": "10.1093/haschl/qxad093",
    "moloci2021": "10.1007/s11606-020-06424-7",
    # Methods
    "simmons2011": "10.1177/0956797611417632",
    "nosek2018": "10.1073/pnas.1708274114",
    "vonelm2007": "10.1371/journal.pmed.0040296",
    "rubin1981": "10.1214/aos/1176345338",
    "phipson2010": "10.2202/1544-6115.1585",
    "gelman2008": "10.1002/sim.3107",
    "gelmanprior2008": "10.1214/08-AOAS191",
    "firth1993": "10.1093/biomet/80.1.27",
    "vehtari2021": "10.1214/20-BA1221",
    "gelmancarlin2014": "10.1177/1745691614551642",
    "callaway2021": "10.1016/j.jeconom.2020.12.001",
    "roth2022": "10.1257/aeri.20210236",
    "lakens2017": "10.1177/1948550617697177",
    "rambachan2023": "10.1093/restud/rdad018",
    "rosenbaum1983": "10.1093/biomet/70.1.41",
    "welch1947": "10.1093/biomet/34.1-2.28",
    "mackinnon1985": "10.1016/0304-4076(85)90158-7",
    # Software with a citable paper
    "pymc2023": "10.7717/peerj-cs.1516",
    "numpy2020": "10.1038/s41586-020-2649-2",
    "duckdb2019": "10.1145/3299869.3320212",
    "arviz2019": "10.21105/joss.01143",
    "statsmodels2010": "10.25080/Majora-92bf1922-011",
}

# Typography only (capitalization, symbols the PDF fonts lack); the words are the registered title's.
TITLE_OVERRIDES = {
    "welch1947": "The generalization of 'Student's' problem when several different population variances are involved",
    "lakens2017": "Equivalence tests: a practical primer for t tests, correlations, and meta-analyses",
    "vehtari2021": "Rank-normalization, folding, and localization: an improved R-hat for assessing convergence of MCMC",
}


# The CSL fields the AMA style uses; Crossref's other fields (some arrays pandoc cannot read) are dropped.
KEEP = {"type", "title", "subtitle", "author", "editor", "container-title", "volume", "issue", "page", "issued", "published-print", "DOI", "URL", "publisher"}

# Health Affairs registers its online teaser as a subtitle; it is not part of the title.
TEASERS = {"lyu2023", "trombley2022"}

# Fields Crossref lacks, from the article itself (Bond: the PubMed record; the others: the article's e-locator).
FIELD_OVERRIDES = {
    "bond2025": {"page": "1897-1905"},
    "ying2024": {"page": "qxad093"},
    "phipson2010": {"page": "39"},
}


def fix_name(name: str) -> str:
    """Crossref keeps some names in capitals (FIRTH, McWILLIAMS); restore ordinary case."""
    if name.isupper():
        return name.title()
    if name.startswith("Mc") and name[2:].isupper():
        return "Mc" + name[2:].title()
    return name


def fetch(doi: str) -> dict:
    req = urllib.request.Request(
        "https://doi.org/" + doi,
        headers={"Accept": "application/vnd.citationstyles.csl+json", "User-Agent": "mssp-paper-2026 (mailto:samuel.harrold@gmail.com)"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main() -> None:
    entries = []
    for key, doi in DOIS.items():
        item = fetch(doi)
        item = {k: v for k, v in item.items() if k in KEEP}
        for k, v in item.items():
            if isinstance(v, list) and k not in ("author", "editor") and v and isinstance(v[0], str):
                item[k] = v[0]
        item["id"] = key
        if item.get("subtitle") and ":" not in item.get("title", "") and key not in TEASERS:
            item["title"] = f"{item['title']}: {item['subtitle']}"
        for a in item.get("author", []):
            for part in ("family", "given"):
                if part in a:
                    a[part] = fix_name(a[part])
        # AMA cites the issue's year; Crossref's "issued" is sometimes the online-first date.
        if "published-print" in item:
            item["issued"] = item["published-print"]
        item.pop("subtitle", None)
        item.pop("published-print", None)
        if key in TITLE_OVERRIDES:
            item["title"] = TITLE_OVERRIDES[key]
        item.update(FIELD_OVERRIDES.get(key, {}))
        entries.append(item)
        print(f"{key:20} {doi:36} {(item.get('title') or '')[:70]}")
        time.sleep(0.3)
    OUT.write_text(json.dumps(entries, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {len(entries)} entries to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

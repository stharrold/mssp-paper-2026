"""PubMed E-utilities literature pass for the preprint's introduction and discussion (no quota, no sign-in).

Writes pubmed_<n>.json (the query, the count and esummary records) for each query below. Standard library only.
Usage: python3 research/pubmed_search.py
"""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
QUERIES = [
    '"Shared Savings Program"[tiab] AND (benchmark*[tiab] OR rebas*[tiab] OR "regional adjustment"[tiab])',
    '"Shared Savings Program"[tiab] AND (exit*[tiab] OR participation[tiab] OR "two-sided"[tiab] OR "downside risk"[tiab] OR selection[tiab])',
    '"Shared Savings Program"[tiab] AND (spending[tiab] OR savings[tiab]) AND (difference-in-differences[tiab] OR "Medicare spending"[tiab])',
    '"accountable care organization*"[tiab] AND "Pathways to Success"[tiab]',
]


def get(endpoint: str, **params) -> dict:
    url = BASE + endpoint + "?" + urllib.parse.urlencode({**params, "retmode": "json", "tool": "mssp-paper"})
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def main() -> None:
    for n, q in enumerate(QUERIES, 1):
        ids = get("esearch.fcgi", db="pubmed", term=q, retmax=200, sort="relevance")["esearchresult"]
        time.sleep(0.4)
        summ = get("esummary.fcgi", db="pubmed", id=",".join(ids["idlist"])) if ids["idlist"] else {"result": {"uids": []}}
        time.sleep(0.4)
        recs = []
        for uid in summ["result"]["uids"]:
            s = summ["result"][uid]
            doi = next((a["value"] for a in s.get("articleids", []) if a["idtype"] == "doi"), None)
            recs.append(
                {
                    "pmid": uid,
                    "year": s.get("pubdate", "")[:4],
                    "first_author": (s.get("authors") or [{}])[0].get("name"),
                    "title": s.get("title"),
                    "journal": s.get("source"),
                    "doi": doi,
                    "pubtype": s.get("pubtype"),
                }
            )
        out = {"query": q, "searched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "count": int(ids["count"]), "records": recs}
        (HERE / f"pubmed_{n}.json").write_text(json.dumps(out, indent=1) + "\n")
        print(f"query {n}: {out['count']} hits, {len(recs)} saved")


if __name__ == "__main__":
    main()

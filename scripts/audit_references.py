"""Collect per-reference audit evidence into references/audit/<key>/ (git-ignored: it holds publishers' text).

For every reference in references/doi.json and references/other.bib:

    0-entry.txt             the entry as stored
    1-citing-sentences.txt  each sentence citing the key in paper.md, supplement.md and strobe.md, with line numbers
    2-resolution.json       the doi.org handle record, for references with a DOI
    3-metadata.json         Crossref's record for the DOI, including any retraction or correction, or the catalog match
    4-source.*              the page or PDF behind a URL, or 4-source.FAILED.txt with the reason
    5-abstract.txt          the abstract from Europe PMC, for references with a DOI
    5-fulltext.*            an open-access full text from Europe PMC, OpenAlex, PMC or an open copy, if any
    6-text.txt              the best available copy as text, with a first line naming which

and writes references/audit/summary.json. Existing 4-source files and 7-verification.txt files are kept, so
copies fetched by hand survive a rerun; --force refetches. A 200 is not treated as proof: eCFR URLs are checked through
the versioner API, Federal Register URLs through its document API, and data.cms.gov (which answers 200 for any path)
through its data catalog. Whether a source supports the sentence is judged by reading it, and recorded in
7-verification.txt; references/AUDIT.md gives the outcome. Standard library and curl only.

Usage: python3 scripts/audit_references.py [--force] [--only key]
"""

import argparse
import difflib
import html
import json
import re
import subprocess
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "references" / "audit"
MANUSCRIPTS = ["paper.md", "supplement.md", "strobe.md"]
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
BIB_ENTRY = re.compile(r"^@(\w+)\{(\w+),\n(.*?)^\}", re.M | re.S)
BIB_FIELD = re.compile(r"^\s*(\w+) = \{(.*)\},?\s*$", re.M)


# Articles in PMC whose full text is not delivered by Europe PMC, and open copies elsewhere
PMC_COPIES = {
    "mcwilliams2016": "4963149",
    "mcwilliams2018": "6269647",
    "mcwilliams2020": "7482384",
    "markovitz2019exit": "8757576",
    "markovitz2019risk": "6394223",
    "bond2025": "12038717",
    "rose2016": "5436972",
    "lyu2023": "10228701",
    "chen2025": "12393041",
    "ying2023": "10212830",
    "moloci2021": "8342743",
    "einav2022": "8884469",
}
OPEN_COPIES = {
    "gelmanprior2008": "https://arxiv.org/pdf/0901.4011",
    "vehtari2021": "https://arxiv.org/pdf/1903.08008",
    "rambachan2023": "https://www.jonathandroth.com/assets/files/HonestParallelTrends_Main.pdf",
    "gelmancarlin2014": "http://www.stat.columbia.edu/~gelman/research/published/retropower_final.pdf",
    "gelman2008": "http://www.stat.columbia.edu/~gelman/research/published/standardizing7.pdf",
}


def curl(url: str, dest: Path | None = None, timeout: int = 45) -> tuple[int, str, str, bytes]:
    """Return (status, final URL, content type, body); a failed connection is status 0."""
    target = dest or OUT / ".last-fetch"
    target.parent.mkdir(parents=True, exist_ok=True)
    fmt = "%{http_code}\n%{url_effective}\n%{content_type}"
    # URLs can come from third-party APIs: web schemes only, also on redirects, and never read as a curl option
    protocols = ["--proto", "=http,https", "--proto-redir", "=http,https"]
    command = ["curl", "-s", "-L", "--compressed", *protocols, "-A", USER_AGENT, "--max-time", str(timeout), "-o", str(target), "-w", fmt, "--url", url]
    out = subprocess.run(command, capture_output=True, text=True)
    parts = out.stdout.split("\n")
    status = int(parts[0]) if parts and parts[0].isdigit() else 0
    body = target.read_bytes() if target.exists() else b""
    return status, parts[1] if len(parts) > 1 else url, parts[2] if len(parts) > 2 else "", body


def get_json(url: str) -> dict | None:
    status, _, _, body = curl(url)
    if status != 200:
        return None
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None


def plain(text: str) -> str:
    """Lowercase letters and digits only, for comparing titles across markup."""
    text = html.unescape(re.sub(r"<[^>]+>", " ", text)).replace("{", "").replace("}", "")
    return " ".join(re.sub(r"[^a-z0-9 ]+", " ", text.lower()).split())


def match(a: str, b: str) -> float:
    return round(difflib.SequenceMatcher(None, plain(a), plain(b)).ratio(), 3)


def load_references() -> dict[str, dict]:
    refs = {}
    for item in json.loads((ROOT / "references" / "doi.json").read_text()):
        refs[item["id"]] = {"source": "doi.json", "title": item.get("title", ""), "doi": item.get("DOI", ""), "url": "", "entry": json.dumps(item, indent=1)}
    bib = (ROOT / "references" / "other.bib").read_text()
    for kind, key, body in BIB_ENTRY.findall(bib):
        fields = dict(BIB_FIELD.findall(body))
        refs[key] = {
            "source": "other.bib",
            "kind": kind,
            "title": fields.get("title", ""),
            "doi": fields.get("doi", ""),
            "url": fields.get("url", ""),
            "entry": f"@{kind}{{{key},\n{body}}}",
        }
    return refs


def sentences(text: str) -> list[tuple[int, str]]:
    """Split a Markdown file into (first line number, sentence), keeping a citation with the sentence it closes."""
    out = []
    start = 1
    for block in re.split(r"(\n\s*\n)", text):
        if block.strip():
            parts = re.split(r"(?<=[.?!\]\d])(?<!et al\.)(?<!cf\.)\s+(?=[A-Z(])", block)
            for part in parts:
                offset = block.find(part)
                out.append((start + block[:offset].count("\n"), " ".join(part.split())))
        start += block.count("\n")
    return out


def citing(key: str, corpus: dict[str, list[tuple[int, str]]]) -> list[str]:
    pattern = re.compile(rf"@{re.escape(key)}(?![\w])")
    return [f"{name}:{line}: {sentence}" for name, items in corpus.items() for line, sentence in items if pattern.search(sentence)]


def check_doi(doi: str) -> tuple[dict, dict | None]:
    quoted = urllib.parse.quote(doi, safe="/")
    handle = get_json(f"https://doi.org/api/handles/{quoted}") or {"responseCode": None}
    crossref = get_json(f"https://api.crossref.org/works/{quoted}")
    return handle, (crossref or {}).get("message")


def ecfr_api(url: str) -> str | None:
    found = re.search(r"ecfr\.gov/on/(\d{4}-\d{2}-\d{2})/title-(\d+)/", url)
    if not found:
        return None
    date, title = found.groups()
    query = {}
    section = re.search(r"/section-(\d+)\.(\w+)", url)
    part = re.search(r"/part-(\d+)", url)
    if section:
        query = {"part": section.group(1), "section": f"{section.group(1)}.{section.group(2)}"}
    elif part:
        query = {"part": part.group(1)}
    return f"https://www.ecfr.gov/api/versioner/v1/full/{date}/title-{title}.xml?{urllib.parse.urlencode(query)}"


def federal_register_api(url: str) -> str | None:
    found = re.search(r"federalregister\.gov/documents/\d{4}/\d{2}/\d{2}/([\w-]+)/", url)
    return f"https://www.federalregister.gov/api/v1/documents/{found.group(1)}.json" if found else None


def page_title(body: bytes, content_type: str) -> str:
    if "pdf" in content_type or body[:4] == b"%PDF":
        return ""
    text = body.decode("utf-8", "replace")
    found = re.search(r'property="og:title"\s+content="([^"]+)"', text) or re.search(r"<title[^>]*>(.*?)</title>", text, re.S)
    return " ".join(html.unescape(found.group(1)).split()) if found else ""


def fetch_source(key: str, ref: dict, directory: Path, force: bool, catalog: dict) -> dict:
    url = ref["url"]
    result: dict = {"url": url}
    existing = [p for p in directory.glob("4-source.*") if p.suffix != ".txt" or "FAILED" not in p.name]
    if existing and not force:
        result.update({"status": "kept", "file": existing[0].name})
        return result
    if "data.cms.gov" in url:
        hit = catalog.get(url.rstrip("/"))
        result.update({"check": "data.cms.gov catalog", "status": 200 if hit else 404, "catalog_title": hit or "", "title_match": match(ref["title"], hit or "")})
        (directory / "4-source.json").write_text(json.dumps({"landingPage": url, "title": hit}, indent=1))
        return result
    api = ecfr_api(url)
    fr = federal_register_api(url)
    fetch_url = api or fr or url
    result["check"] = "eCFR versioner API" if api else "Federal Register API" if fr else "direct"
    temp = directory / "4-source.tmp"
    status, final, content_type, body = curl(fetch_url, temp, timeout=120 if api else 60)
    result.update({"status": status, "final_url": final, "content_type": content_type, "bytes": len(body)})
    if status == 200 and body:
        kind = "pdf" if body[:4] == b"%PDF" else "xml" if api else "json" if fr else "html"
        temp.rename(directory / f"4-source.{kind}")
        (directory / "4-source.FAILED.txt").unlink(missing_ok=True)
        title = json.loads(body).get("title", "") if fr else page_title(body, content_type)
        result.update({"file": f"4-source.{kind}", "page_title": title})
        if title:
            result["title_match"] = match(ref["title"], title)
    else:
        temp.unlink(missing_ok=True)
        (directory / "4-source.FAILED.txt").write_text(f"{fetch_url}\nHTTP {status}\n{final}\n")
    return result


def catalog_url(dataset: dict) -> str:
    """The dataset's landing page in data.cms.gov's catalog: a string, or a record holding it as accessURL."""
    page = dataset.get("landingPage", "")
    return (page.get("accessURL", "") if isinstance(page, dict) else page).rstrip("/")


def fetch_open_copy(key: str, directory: Path) -> str:
    """Fetch an open copy named in PMC_COPIES or OPEN_COPIES, for articles the two services above do not deliver."""
    if key in PMC_COPIES:
        pmc = PMC_COPIES[key]
        status, _, _, body = curl(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={pmc}&retmode=xml", directory / "5-fulltext.xml")
        if status == 200 and b"<body" in body and len(body) > 20000:
            return f"PMC{pmc} (E-utilities)"
        (directory / "5-fulltext.xml").unlink(missing_ok=True)
        status, _, _, body = curl(f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{pmc}/", directory / "5-fulltext.html")
        if status == 200 and b"<article" in body:
            return f"PMC{pmc} (page)"
        (directory / "5-fulltext.html").unlink(missing_ok=True)
    if key in OPEN_COPIES:
        status, _, _, body = curl(OPEN_COPIES[key], directory / "5-fulltext.tmp")
        if status == 200 and body[:4] == b"%PDF":
            (directory / "5-fulltext.tmp").rename(directory / "5-fulltext.pdf")
            return OPEN_COPIES[key]
        (directory / "5-fulltext.tmp").unlink(missing_ok=True)
    return ""


def extract_text(directory: Path) -> str:
    """Write the best available copy of the source to 6-text.txt, for reading and searching."""
    for name in ["5-fulltext.xml", "5-fulltext.html", "5-fulltext.pdf", "4-source.pdf", "4-source.xml", "4-source.html", "5-abstract.txt"]:
        path = directory / name
        if not path.exists():
            continue
        if path.suffix == ".pdf":
            text = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True).stdout
        elif path.suffix == ".txt":
            text = path.read_text()
        else:
            raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", path.read_text(errors="replace"))
            text = re.sub(r"[ \t]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
            text = re.sub(r"\n\s*\n+", "\n", text)
        (directory / "6-text.txt").write_text(f"[from {name}]\n{text}")
        return name
    return ""


def fetch_fulltext(doi: str, directory: Path) -> dict:
    """Save the abstract and any open-access full text for a DOI; returns where they came from."""
    found: dict = {"abstract": False, "fulltext": ""}
    quoted = urllib.parse.quote(f'DOI:"{doi}"')
    search = get_json(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={quoted}&format=json&resultType=core") or {}
    hits = search.get("resultList", {}).get("result", [])
    if hits and hits[0].get("abstractText"):
        (directory / "5-abstract.txt").write_text(html.unescape(re.sub(r"<[^>]+>", " ", hits[0]["abstractText"])) + "\n")
        found["abstract"] = True
    pmcid = hits[0].get("pmcid") if hits else None
    if pmcid:
        status, _, _, body = curl(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML", directory / "5-fulltext.xml")
        if status == 200 and b"<body" in body:
            found["fulltext"] = f"Europe PMC {pmcid}"
            return found
        (directory / "5-fulltext.xml").unlink(missing_ok=True)
    work = get_json(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi, safe='/')}") or {}
    location = work.get("best_oa_location") or {}
    for url in filter(None, [location.get("pdf_url"), location.get("landing_page_url")]):
        status, _, _, body = curl(url, directory / "5-fulltext.tmp")
        if status == 200 and body[:4] == b"%PDF":
            (directory / "5-fulltext.tmp").rename(directory / "5-fulltext.pdf")
            found["fulltext"] = f"OpenAlex {url}"
            return found
    (directory / "5-fulltext.tmp").unlink(missing_ok=True)
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--only")
    args = parser.parse_args()
    refs = load_references()
    corpus = {name: sentences((ROOT / name).read_text()) for name in MANUSCRIPTS}
    catalog_raw = get_json("https://data.cms.gov/data.json") or {}
    catalog = {catalog_url(d): d.get("title", "").split(" : ")[0] for d in catalog_raw.get("dataset", [])}
    summary = {}
    for key, ref in refs.items():
        if args.only and key != args.only:
            continue
        directory = OUT / key
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "0-entry.txt").write_text(ref["entry"] + "\n")
        cites = citing(key, corpus)
        (directory / "1-citing-sentences.txt").write_text("\n\n".join(cites) + "\n")
        row: dict = {"source": ref["source"], "title": ref["title"], "citations": len(cites)}
        if ref["doi"]:
            handle, crossref = check_doi(ref["doi"])
            (directory / "2-resolution.json").write_text(json.dumps(handle, indent=1))
            row["doi"] = ref["doi"]
            row["doi_registered"] = handle.get("responseCode") == 1
            target = [v["data"]["value"] for v in handle.get("values", []) if v.get("type") == "URL"]
            row["doi_target"] = target[0] if target else ""
            if crossref:
                (directory / "3-metadata.json").write_text(json.dumps(crossref, indent=1))
                registered = " ".join((crossref.get("title") or [""])[:1] + (crossref.get("subtitle") or [])[:1])
                row["crossref_title_match"] = match(ref["title"], registered)
                row["updated_by"] = [{"type": u.get("type"), "doi": u.get("DOI")} for u in crossref.get("updated-by", [])]
                row["is_update_notice"] = [{"type": u.get("type"), "doi": u.get("DOI")} for u in crossref.get("update-to", [])]
            row["open_access"] = fetch_fulltext(ref["doi"], directory)
            if not row["open_access"]["fulltext"]:
                row["open_access"]["fulltext"] = fetch_open_copy(key, directory)
            time.sleep(0.2)
        if ref["url"]:
            row["source_check"] = fetch_source(key, ref, directory, args.force, catalog)
        row["text_from"] = extract_text(directory)
        summary[key] = row
        print(key, "cited", len(cites), "doi" if ref["doi"] else "", (row.get("source_check") or {}).get("status", ""))
    (OUT / ".last-fetch").unlink(missing_ok=True)
    if not args.only:
        (OUT / "summary.json").write_text(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()

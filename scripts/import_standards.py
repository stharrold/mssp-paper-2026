"""Convert journal pages saved from the browser into local Markdown copies in standards/<venue>/.

Springer's pages refuse scripted downloads, so the pages are fetched inside a signed-out Chrome tab on the publisher's
site and saved as one JSON bundle: {"retrieved": ISO time, "pages": {url: {"status", "final", "title", "html"}}}, where
"html" is the page's <main> with scripts, styles, images and buttons removed. The in-page snippet:

    const out = {};
    for (const u of URLS) {
      const r = await fetch(u), d = new DOMParser().parseFromString(await r.text(), 'text/html');
      const el = d.querySelector('main') || d.body;
      el.querySelectorAll('script,style,svg,img,noscript,button').forEach(x => x.remove());
      out[u] = {status: r.status, final: r.url, title: d.title, html: el.innerHTML};
    }
    // then save JSON.stringify({retrieved: new Date().toISOString(), pages: out}) as a download

Each page becomes <prefix>_<last path segment>.md with its title, source URL and retrieval date, converted by pandoc
(GitHub Markdown; complex tables stay as HTML). The copies are the publishers' text, so they stay out of git (.gitignore); the
venue's SOURCES.md lists them.

Usage: uv run python scripts/import_standards.py <bundle.json> <standards/venue> <prefix> [<url-prefix>=<file-prefix> ...]
  e.g. ... ~/Downloads/bmc-hsr_springer-pages.json standards/bmc-hsr bmc /collections/=bmc-hsr_collection
"""

import json
import subprocess
import sys
from pathlib import Path

UNWRAP = Path(__file__).resolve().parent / "unwrap.lua"


def to_markdown(html: str) -> str:
    command = ["pandoc", "-f", "html", "-t", "gfm", "--wrap=none", "--lua-filter", str(UNWRAP)]
    out = subprocess.run(command, input=html, capture_output=True, text=True, check=True)
    return out.stdout.strip() + "\n"


def main() -> None:
    bundle, dest, prefix, *rules = sys.argv[1:]
    data = json.loads(Path(bundle).read_text())
    retrieved = data["retrieved"][:10]
    overrides = dict(rule.split("=", 1) for rule in rules)
    dest_dir = Path(dest)
    dest_dir.mkdir(parents=True, exist_ok=True)
    for url, page in data["pages"].items():
        if page["status"] != 200:
            print(f"skipped {url} (HTTP {page['status']})")
            continue
        name = f"{prefix}_{url.rstrip('/').rsplit('/', 1)[-1]}"
        for match, other in overrides.items():
            if match in url:
                name = f"{other}_{url.rstrip('/').rsplit('/', 1)[-1]}"
        title = page["title"].split(" | ")[0].strip()
        header = f"# {title}\n\n**Source:** {url}\n\n**Retrieved:** {retrieved}, in a browser (scripts/import_standards.py)\n\n---\n\n"
        path = dest_dir / f"{name}.md"
        path.write_text(header + to_markdown(page["html"]))
        print(f"wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

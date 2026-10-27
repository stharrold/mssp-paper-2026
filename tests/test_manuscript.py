"""Checks that keep the manuscript consistent with the committed results. Run: uv run pytest"""

import hashlib
import re
import subprocess
import sys
from pathlib import Path

import check_numbers
import make_tables

ROOT = Path(__file__).resolve().parent.parent


def test_data_matches_recorded_hashes():
    table = (ROOT / "data" / "README.md").read_text()
    for name, digest in re.findall(r"\| `([^`]+\.json)` \|[^|]*\| `([0-9a-f]{64})` \|", table):
        assert hashlib.sha256((ROOT / "data" / name).read_bytes()).hexdigest() == digest, name


def test_tables_are_current():
    for name, build in make_tables.TABLES.items():
        assert (ROOT / "tables" / f"{name}.md").read_text() == build(), f"rerun scripts/make_tables.py ({name})"


def test_every_included_table_exists():
    for doc in ("paper.md", "supplement.md"):
        for path in re.findall(r"\{\{include (\S+)\}\}", (ROOT / doc).read_text()):
            assert (ROOT / path).is_file(), path


def test_every_citation_is_defined():
    import json

    keys = {e["id"] for e in json.loads((ROOT / "references" / "doi.json").read_text())}
    keys |= set(re.findall(r"@\w+\{(\w+),", (ROOT / "references" / "other.bib").read_text()))
    for doc in ("paper.md", "supplement.md"):
        cited = set(re.findall(r"@([A-Za-z][\w]*)", " ".join(re.findall(r"\[@[^\]]*\]", (ROOT / doc).read_text()))))
        assert cited <= keys, cited - keys


def test_prose_numbers_match_results():
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_numbers.py")], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout


def test_number_check_catches_a_changed_interval(tmp_path):
    text = (ROOT / "paper.md").read_text().replace("95% CrI, 1.7 to 5.4", "95% CrI, 1.8 to 5.4", 1)
    mutated = tmp_path / "paper.md"
    mutated.write_text(text)
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_numbers.py"), str(mutated)], capture_output=True, text=True)
    assert result.returncode == 1 and "1.8 to 5.4" in result.stdout
    assert check_numbers  # imported for its module docstring and helpers

"""Write the plain-text fields for a JMIR submission form from paper.md and metadata.yaml.

JMIR's metadata form takes the title, abstract and keywords as plain text, and figure captions without their
"Figure N." prefix, with figure files as PNGs of at most 1200 x 1200 pixels and no transparency. medRxiv's form
turned non-ASCII characters into HTML entities, so every field is written as ASCII (rho, hyphen-minus, straight
quotes) and the script fails if anything else remains.

Usage: uv run python scripts/form_fields.py
  writes submission/ijmr/*-plaintext.txt (including the cover letter for the comments-to-editor field),
  figures/*.figure.png (upload copies of figures/*.png) and figures/*.caption.txt
"""

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "submission" / "ijmr"
ASCII = {"−": "-", "–": "-", "—": "-", "’": "'", "‘": "'", "“": '"', "”": '"', " ": " ", "≈": "~", "×": "x"}


def plain(text: str) -> str:
    text = text.replace("$\\rho$", "rho").replace("$\\hat{R}$", "R-hat")
    text = re.sub(r"\[@[^\]]*\]", "", text)
    text = re.sub(r"\*\*?([^*]+?)\*\*?", r"\1", text)
    text = text.replace("\\[", "[").replace("\\]", "]").replace("\\$", "$")
    for k, v in ASCII.items():
        text = text.replace(k, v)
    text = "\n\n".join(" ".join(para.split()) for para in re.split(r"\n\s*\n", text.strip()))  # unwrap, keep paragraphs
    bad = sorted({c for c in text if ord(c) > 127})
    assert not bad, f"non-ASCII left: {bad}"
    return text.strip() + "\n"


def main() -> None:
    paper = (ROOT / "paper.md").read_text()
    title = re.search(r'^title: "(.*)"$', (ROOT / "metadata.yaml").read_text(), re.M).group(1)
    abstract = re.search(r"^# Abstract\n(.*?)^# ", paper, re.S | re.M).group(1)
    keywords = re.search(r"^\*\*Keywords:\*\* (.*?)\\?$", paper, re.M).group(1)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "title-plaintext.txt").write_text(plain(title))
    (OUT / "abstract-plaintext.txt").write_text(plain(abstract))
    (OUT / "keywords-plaintext.txt").write_text(plain(keywords))
    letter = (OUT / "cover-letter.md").read_text()
    (OUT / "cover-letter-plaintext.txt").write_text(plain(letter[letter.index("Dear Editor") :]))
    (OUT / "figures").mkdir(exist_ok=True)
    for caption, name in re.findall(r"!\[Figure \d\. (.*?)\]\(figures/([^)]+)\.png\)", paper):
        (OUT / "figures" / f"{name}.caption.txt").write_text(plain(caption))
        image = Image.open(ROOT / "figures" / f"{name}.png").convert("RGBA")
        flat = Image.new("RGB", image.size, "white")
        flat.paste(image, mask=image.getchannel("A"))
        scale = 1200 / max(flat.size)
        flat.resize((round(flat.width * scale), round(flat.height * scale)), Image.LANCZOS).save(OUT / "figures" / f"{name}.figure.png", optimize=True)
    print("wrote", ", ".join(p.name for p in sorted(OUT.glob("*-plaintext.txt"))), "and figure uploads with captions")


if __name__ == "__main__":
    main()

"""Write the plain-text fields and figure uploads for the BMC Health Services Research submission.

The submission form takes the title, abstract and keywords as text, the figures as separate files (numbered in order
of first mention, PNG accepted, at most 10 MB each) and their titles and legends in the manuscript. Fields are ASCII,
as for the earlier forms (scripts/form_fields.py, which writes the frozen i-JMR package and is not run for this one).

Usage: uv run python scripts/bmc_fields.py
  writes submission/bmc-hsr/*-plaintext.txt (including the cover letter), and submission/bmc-hsr/figures/FigureN.png
  (figures/*.png flattened onto white and closely cropped, as BMC asks) with FigureN.caption.txt
"""

import re
from pathlib import Path

from form_fields import plain
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "submission" / "bmc-hsr"
MAX_BYTES = 10 * 1024 * 1024
CROP_MARGIN = 12  # pixels of white kept around each figure


def main() -> None:
    paper = (ROOT / "paper.md").read_text()
    title = re.search(r'^title: "(.*)"$', (ROOT / "metadata.yaml").read_text(), re.M).group(1)
    abstract = re.search(r"^# Abstract\n(.*?)\*\*Keywords:\*\*", paper, re.S | re.M).group(1)
    keywords = re.search(r"^\*\*Keywords:\*\* (.*?)\n\n", paper, re.S | re.M).group(1)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "title-plaintext.txt").write_text(plain(title))
    # BMC's abstract includes its Trial registration section; the form may also ask for the registration on its own.
    (OUT / "abstract-plaintext.txt").write_text(plain(abstract))
    (OUT / "trial-registration-plaintext.txt").write_text(plain(abstract.split("**Trial registration:**")[1]))
    (OUT / "keywords-plaintext.txt").write_text(plain(keywords))
    letter = (OUT / "cover-letter.md").read_text()
    (OUT / "cover-letter-plaintext.txt").write_text(plain(letter[letter.index("Dear Editor") :]))
    (OUT / "figures").mkdir(exist_ok=True)
    for n, caption, name in re.findall(r"!\[Figure (\d+)\. (.*?)\]\(figures/([^)]+)\.png\)", paper):
        (OUT / "figures" / f"Figure{n}.caption.txt").write_text(plain(caption))
        image = Image.open(ROOT / "figures" / f"{name}.png").convert("RGBA")
        flat = Image.new("RGB", image.size, "white")
        flat.paste(image, mask=image.getchannel("A"))
        left, top, right, bottom = ImageChops.difference(flat, Image.new("RGB", flat.size, "white")).getbbox()
        flat = flat.crop((max(left - CROP_MARGIN, 0), max(top - CROP_MARGIN, 0), min(right + CROP_MARGIN, flat.width), min(bottom + CROP_MARGIN, flat.height)))
        path = OUT / "figures" / f"Figure{n}.png"
        flat.save(path, optimize=True)
        assert path.stat().st_size <= MAX_BYTES, f"{path.name} is over 10 MB"
    print("wrote", ", ".join(p.name for p in sorted(OUT.glob("*-plaintext.txt"))), "and", len(list((OUT / "figures").glob("Figure*.png"))), "figures")


if __name__ == "__main__":
    main()

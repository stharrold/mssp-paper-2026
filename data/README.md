# Data

Copied unchanged from [stharrold/stharrold.github.io](https://github.com/stharrold/stharrold.github.io); nothing here
is recomputed. Every table and figure in the manuscript is generated from these files.

| File | Source | SHA-256 |
|---|---|---|
| `results/validation.json` | `analysis/mssp-benchmark-ratchet/results/` at commit [`3da8cd2`](https://github.com/stharrold/stharrold.github.io/tree/3da8cd28c6601c45bc7a4da9abf91af62af20722/analysis/mssp-benchmark-ratchet/results) | `046d82a1cc40548ec41b75b5877c7e49c89c0cee76aabde1666724adce24b365` |
| `results/power.json` | same | `9d48835d8b87aac180cf29ce119d35134cfffeb8df27bd725798ba11b6c1a41e` |
| `results/confirm.json` | same | `35bba7e38d3dd6e17156ba4f4763b8b9fe38672fc24a3e3ac2d3f5b932ecbc94` |
| `results/robustness.json` | same | `66f00ad1a01e2f1c3cb5ceb69d744afd076ccc39f646b48ba90fda15c671af07` |
| `results/did.json` | same | `8f3a6842df52d1eb7e0b3d1412b2a610d9c5a95d8301db1b6b94dbf89a8705b6` |
| `results/conventional.json` | same | `3508370b700d1d005b228d943bd25d79b10578acc8aa9781e47b6570be347e1d` |
| `results/exploratory.json` | same | `280bbe10b738a284a3eefb47e6e69fe2a035a8ecc26f5eddf005de535f51efb5` |
| `dashboard-data.json` | `content/static/20261027-preregistered-mssp-early-renewal/data.json` at commit [`a226a7f`](https://github.com/stharrold/stharrold.github.io/blob/a226a7f71cf96bee8f3479111dd96a89744e6fc3/content/static/20261027-preregistered-mssp-early-renewal/data.json) | `894953791e3396125530892ac222aae02e92135fa1758ac838b00733ebd6583e` |

Each results file records the commit of the registered code it ran at (`git_commit`). `dashboard-data.json` is built
from the results files by `analysis/mssp-benchmark-ratchet/report/dashboard_data.py`; it puts the comparisons,
robustness checks and H4 estimates in reporting units. One quirk: its exploratory group summaries scale the PY2020
savings-rate mean and median to percentage points but not the SD, so Table 1 reads those from `exploratory.json`
directly.

`number-allowlist.tsv` lists the numbers in the prose that are not in these files, each with its source
(`scripts/check_numbers.py`).

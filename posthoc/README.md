# Post hoc analyses (not registered)

Copies, byte for byte, of the study's post hoc scripts, so this repository's archive holds every script behind the
manuscript that the OSF registration does not. The originals, and the environment they run in, are in
`stharrold/stharrold.github.io` under `analysis/mssp-benchmark-ratchet/posthoc/`; they import the registered pipeline
(`ratchet/`) and run from that repository's root, not from here.

| Script | Source commit | sha256 | Output (copied to `data/posthoc/`) |
|---|---|---|---|
| `validation_change.py` | [`bf91e5c`](https://github.com/stharrold/stharrold.github.io/blob/bf91e5c/analysis/mssp-benchmark-ratchet/posthoc/validation_change.py) | `a301cab211e6a70c...` | `validation_change.json` |
| `pull_savings.py` | [`7fa20c0`](https://github.com/stharrold/stharrold.github.io/blob/7fa20c0/analysis/mssp-benchmark-ratchet/posthoc/pull_savings.py) | `802e900c268c6fad...` | `pull_savings.json` |

Both were written after every registered result had been read, change no registered file and decide no registered
hypothesis (see each script's docstring).

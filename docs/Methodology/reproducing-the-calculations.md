---
title: "Reproducing the Calculations"
excerpt: "How to run the calculations project and verify its inputs."
hidden: true
---

*Source of truth: [`calculations/README.md`](https://github.com/icanbwell/cms-hte-patient-matching/blob/main/calculations/README.md) and [`calculations/docs/PROCESS.md`](https://github.com/icanbwell/cms-hte-patient-matching/blob/main/calculations/docs/PROCESS.md). If these steps differ from the repository, the repository is correct.*

The tool is a self-contained Python 3.12 project. It does not import from the matching library and needs no patient data.

## Setup

```bash
cd calculations
python3.12 -m venv .venv        # or: uv venv .venv --python 3.12
source .venv/bin/activate
pip install -r requirements.txt  # or: uv pip install -r requirements.txt
```

Optional credentials go in a gitignored `calculations/.env` file:

| Variable | Effect |
|---|---|
| `CENSUS_API_KEY` | Avoids Census API rate limiting on the ZCTA-level ACS calls. Without it, the queries still work but may be throttled. |
| `HUD_TOKEN` | Enables the optional HUD USPS ZIP crosswalk step. Without it, that step is skipped and city u-probabilities use Census places and CDPs only. The tool prints this clearly at runtime. |

## Running

```bash
make venv       # create .venv and install requirements.txt
make download   # download all raw sources into data/raw/ (idempotent)
make calculate  # compute from data/raw/, print the headline table, write outputs/
make all        # download, then calculate
make test       # pytest tests/
```

Equivalent direct commands are `python run_all.py`, `python run_all.py --download-only`, and `python run_all.py --compute-only`.

`make calculate` reads only what is already in `data/raw/` and never touches the network. The raw files are committed, so it works on a fresh clone offline. A run writes `outputs/u_probabilities.csv` and `outputs/u_probabilities.md`.

The fuzzy-match computations for last and first names are the slowest step. They are checkpointed to `data/processed/*_ball_mass.npy`, which is gitignored; delete the relevant file to force a recompute.

## Verifying the inputs

```bash
cd calculations/data/raw && shasum -a 256 -c SHA256SUMS
```

## Refreshing a raw file

1. Delete the file (`make download` skips files that already exist).
2. Run `make download`.
3. Regenerate the checksums: `cd data/raw && shasum -a 256 <files> > SHA256SUMS`.
4. Commit the changed files.

Keep raw files byte-identical to what the source serves, because the checksums and the "upstream changed" signal depend on it. `make clean` leaves `data/raw/` alone because it is tracked. Do not edit `data/raw/` or `data/processed/` by hand.

## Tests

`pytest tests/` runs unit tests that exercise the math against small synthetic fixtures, without real data.

## Project layout

| File | Role |
|---|---|
| `config.py` | Source URLs with provenance comments, the specification's conservative values used for comparison, and sanity ranges |
| `download.py` | Idempotent downloaders for every source |
| `compute.py` | One pure, unit-tested function per field, with no I/O |
| `run_all.py` | Orchestrates download, compute, and output writing, with checkpointing |

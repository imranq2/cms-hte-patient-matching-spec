---
title: "Data Sources"
excerpt: "The public data behind the calculations project, with attribution and download dates."
hidden: true
---

*Source of truth: the "Sources and download dates" section of [`calculations/outputs/u_probabilities.md`](https://github.com/icanbwell/cms-hte-patient-matching/blob/main/calculations/outputs/u_probabilities.md), and [`calculations/config.py`](https://github.com/icanbwell/cms-hte-patient-matching/blob/main/calculations/config.py), which records how each URL was resolved.*

The calculations project uses **only public aggregate data**. It uses no patient data. As recorded in the generated output, all data was downloaded or re-verified on 2026-10-06.

## Sources used for the computed values

| Used for | Source | Publisher |
|---|---|---|
| First names (2020) | `Names2020_FirstNames_Sex.xlsx` | U.S. Census Bureau |
| Last names (2020) | `Names2020_LastNames_RaceHispanic.xlsx`. This file publishes race and Hispanic-origin cross-tabs; the tool sums the race columns, which it verified equal the total frequency column. | U.S. Census Bureau |
| Last names (2010), comparison only | `names_2010census.zip` | U.S. Census Bureau |
| Year of birth and full date of birth | `nc-est2025-agesex-res.csv` (national single-year-of-age estimates) | U.S. Census Bureau |
| State | `NST-EST2025-POP.xlsx` (July 1, 2025 estimate) | U.S. Census Bureau |
| City | `sub-est2025.csv` (incorporated places and Census Designated Places, July 1, 2025 estimate) | U.S. Census Bureau |
| ZIP (via ZCTA), street line | American Community Survey 2024 5-year estimates at ZCTA level: population (B01003), household size (B11016, B25010), housing units (B25001) | U.S. Census Bureau |
| MBI | "Medicare Total Enrollment" (2024), Program Statistics | Centers for Medicare & Medicaid Services |
| Phone (share of households with a landline) | NCHS Wireless Substitution survey, July to December 2024, Table 1: [doi.org/10.15620/cdc/174608](https://doi.org/10.15620/cdc/174608) | CDC National Center for Health Statistics |
| SSN / ITIN last 4 | SSA SSN Randomization policy (closed form, no data file): [ssa.gov/employer/randomization.html](https://www.ssa.gov/employer/randomization.html) | Social Security Administration |

## Cited but not used in a computed value

- **FCC 18-31, CG Docket No. 17-59, para. 3 (2018-03-22):** cited in the phone notes as a named, deliberately unquantified gap (mobile number reassignment, about 35 million U.S. numbers per year). No data file is used.

## Not used

- **HUD USPS ZIP crosswalk:** skipped because no `HUD_TOKEN` was configured, so the alternate USPS-city-via-ZIP calculation for city is not part of the published numbers.

## Reproducibility of the data

- The raw files are committed in the repository under `calculations/data/raw/` (about 41 MB), with SHA-256 checksums in `SHA256SUMS`. `make calculate` therefore runs offline, and an upstream change to a source file shows up as a diff.
- ACS 2024 5-year estimates are used because the 2025 5-year estimates were not yet published as of the project's last documented run.
- Census name files list only names occurring 100 or more times. See [Known Limitations](/docs/known-limitations).

## Test data is separate

The labeled test cases come from a different public dataset, the ONC 2017 Patient Matching Algorithm Challenge dataset. See [Test Set Methodology](/docs/test-set-methodology) and [Test Set Overview](/docs/test-set) for its provenance and attribution.

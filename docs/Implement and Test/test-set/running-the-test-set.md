---
title: "Running the Test Set"
excerpt: "File formats, scoring, and reporting rules for the two test tiers."
hidden: true
---

*Source of truth: the "How to test a patient-matching algorithm against this dataset" document at [`evaluation/cases/README.md`](https://github.com/icanbwell/cms-hte-patient-matching-test-set/blob/main/evaluation/cases/README.md), which includes runnable Python scoring examples. This page summarizes the contract and the reporting rules; use the repository for the code.*

Your algorithm needs to satisfy one contract: given two FHIR `Patient` documents, decide match or no-match. Any language works.

## Get the data

Clone or download the [test set repository](https://github.com/icanbwell/cms-hte-patient-matching-test-set). The committed files are in `evaluation/cases/`.

## Tier 1: per-provision pairs

**File:** `sample_labeled_pairs.jsonl`, one JSON object per line.

| Field | Meaning |
|---|---|
| `case_id` | Stable identifier for the case |
| `source` | The "Outside Record" or query FHIR `Patient` |
| `target` | The "Internal Record" or candidate FHIR `Patient` |
| `expected_match` | The gold label: `true` if both records are the same person |
| `rationale` | The category and subtype the case traces to, such as `fuzzy_variant/dob_day` or `special_population/shelter` |
| `frequency` | A relative prevalence weight; currently `1.0` for every case, meaning no real-world weighting has been applied |

**To score:** stream the file, give each `source` and `target` to your algorithm, compare its answer with `expected_match`, and tally true positives, false positives, false negatives, and true negatives. Compute metrics from the tallies, never per case and never by averaging per-case percentages.

## Tier 2: population queries

**Files:** `population_queries.jsonl` and `population_candidates.jsonl`.

| File | Fields |
|---|---|
| `population_candidates.jsonl` | `id`, `patient`: one row per unique candidate |
| `population_queries.jsonl` | `query_id`, `query`, `candidate_ids` (the pool, resolved against the candidates file), `expected_match_ids` (the subset that is the same person as the query, which may be empty), `rationale` |

**To score:** load the candidates once. For each query, evaluate the query against every candidate in its pool, and mark a candidate as an actual match if its id is in `expected_match_ids`. Tally the four buckets across all queries.

## Reporting rules

- **Use the right metrics for each tier.** On tier 1, trust only recall and false-positive rate. Compute precision, FDR, F1, and accuracy on tier 2.
- **Break results out by `rationale`,** using the prefix before the `/`, such as `fuzzy_variant` or `hard_negative`. A single blended number hides categories your algorithm handles poorly.
- **Report skipped cases separately.** If your algorithm cannot evaluate a case, count it. Do not exclude it silently.
- **Do not infer real-world prevalence** from category counts.

## Before relying on a result

- Every record is a real ONC record or a mutation of one. Institutional-category cases carry a deliberately fabricated, marked address ("SYNTHETIC TEST ADDRESS" and a reserved ZIP block).
- The committed files are curated snapshots and change between releases. Pin the release you test against and record it with your results. Row counts and case ids can change; the repository's dataset changelog lists changes.
- Section VI.A of the specification asks for precision, recall, and false-positive rate at the configured operating point. See [Test Set Overview](/docs/test-set) for how this test set relates to that requirement.

---
title: "Test Set Methodology"
excerpt: "How the labeled test cases are generated from the ONC 2017 challenge dataset."
hidden: false
---

*Source of truth: [`evaluation/cases/README.md`](https://github.com/icanbwell/cms-hte-patient-matching-test-set/blob/main/evaluation/cases/README.md) in the cms-hte-patient-matching-test-set repository, in particular its "How this test data was generated" section, and [`docs/METHODOLOGY.md`](https://github.com/icanbwell/cms-hte-patient-matching-test-set/blob/main/docs/METHODOLOGY.md). The repository changes as the test set evolves; this page summarizes it and does not repeat counts that change between releases.*

## Source population

Every record derives from the public ONC 2017 Patient Matching Algorithm Challenge dataset: nine alphabetically sharded CSV files of about one million records in total. It is public and already synthetic. The test set's generator maps ONC's columns to FHIR `Patient` resources. No real member-organization or client data, and no de-identification step, is involved anywhere in the pipeline.

The repository documents that every `EnterpriseID` across all nine shards is unique in the vendored copy, so it has no native duplicate-person clusters. Every true-match cluster is therefore built by the test set's own generators, not looked up from ONC.

## How cases are labeled

Each case has a stable `case_id` built from the ONC identifiers involved and a `rationale` that records its category and subtype, so every case traces to a specific reason. The generators run from a fixed random seed (default `0`) and reproduce the same output given the same input records. The committed files are curated snapshots and are not guaranteed to regenerate byte for byte; the repository explains why.

## True-match cases

| Category | What it does |
|---|---|
| Fuzzy-tolerance variants | One variation of a real record per case. Most are single-character edits matching the specification's fuzzy tolerance (insertion, deletion, substitution, transposition); some are broader, such as small date-of-birth shifts, dropping about 20% of a family name's letters, nickname substitution, and reducing a given name to an initial. Ten mutation types are registered. |
| Normalization edge cases | Diacritic and punctuation variants that the specification's normalization requirements say must fold into an identical match. |
| Compound variants and scenario mutators | Several edits in one pair, a dropped SSN, a marriage-driven surname and address change, and a second phone number. The marriage and second-phone categories have intentionally small yields, because the underlying ONC fields are sparsely populated. |
| Drift scenarios | Registry scenarios named `surname_change`, `address_move`, `phone_churn`, `email_churn`, `placeholder`, and `gender_drift`. |

## True-non-match cases

Non-matches are never produced by mutating a record, since that would test only a matcher's own fuzzy tolerance, not reality. They are always two genuinely distinct ONC identities:

- **General hard negatives:** distinct people who share a postal code and date of birth but have different family names.
- **Multi-generational households:** same address and family name with birth years at least 15 years apart. In the committed sample every such pair is constructed, by giving a real younger same-surname record the elder's real address, because ONC addresses are near-unique. The generator can also mine same-street pairs from inputs that have co-resident records.
- **Institutional negatives:** eight categories (shelter, nursing facility, correctional institution, hotel or short-term housing, halfway house, dormitory, group home, migrant camp). Three already-distinct real identities have only their address overwritten with a fixed synthetic address. Each carries an unambiguous "SYNTHETIC TEST ADDRESS" line and a reserved ZIP block.
- **Sibling negatives:** distinct people sharing postal code and family name, with different first names and birth years no more than 3 years apart.
- **Name-collision negatives:** near-identical full names (edit distance of 1 or less) with no shared postal code or date of birth.
- **Placeholder-collision negatives:** two distinct people sharing a placeholder SSN, phone, or date of birth.

Literal twins are deliberately never constructed, because, according to the test set's README, that case cannot be resolved through field matching alone. Every non-match pair is checked so that none shares a real SSN or an identical first name, family name, and date of birth.

## Two tiers

The same generation logic is assembled into two test tiers. The per-provision pairs support recall and false-positive rate; the population-query tier supports precision, recall, false-positive rate, FDR, F1, and accuracy. See [Running the Test Set](/docs/running-the-test-set).

## What this dataset does not claim

Case counts per category are an artifact of how the file was generated and are not real-world prevalence. The repository warns against computing an aggregate expected accuracy by weighting categories by their counts. See that section of the test set README before reporting results.

## Provenance and attribution

The ONC dataset is published by the Office of the National Coordinator for Health IT and is also mirrored at [onc-healthit/patient-matching](https://github.com/onc-healthit/patient-matching). The test set vendors it for reproducibility. The test set's own README advises independently confirming the terms ONC published it under before redistributing it further.

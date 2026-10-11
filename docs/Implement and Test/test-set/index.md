---
title: "Test Set Overview"
excerpt: "A public, algorithm-agnostic dataset for validating a matching algorithm against the specification."
hidden: true
---

*Source of truth: the [cms-hte-patient-matching-test-set repository](https://github.com/icanbwell/cms-hte-patient-matching-test-set) and its [README for test data](https://github.com/icanbwell/cms-hte-patient-matching-test-set/blob/main/evaluation/cases/README.md). Where this page differs from the repository, the repository is correct.*

## What it is

A set of labeled patient-matching cases for checking an algorithm against the CMS HTE Patient Matching Specification. It is portable and algorithm-agnostic: it has no runtime dependency on any matching engine, and any language can use it. The repository is Apache-2.0 licensed and tagged in releases (the latest tag as of 2026-10-07 is `0.0.5`).

Every record derives from the public ONC 2017 Patient Matching Algorithm Challenge dataset, which is already synthetic and contains no PHI. Its generation code adds variants, mined non-matches, and constructed scenarios. See [Test Set Methodology](/docs/test-set-methodology) for how, and for the data's provenance and attribution.

## Two tiers

| Tier | Shape | Use it for |
|---|---|---|
| **Per-provision pairs** | One `(source, target)` pair per case, deliberately over-sampling rare and high-risk categories | Recall and false-positive rate. **Not** precision, FDR, F1, or accuracy. |
| **Population query** | One query patient against a candidate pool (default 40 candidates), with an expected-match set that may be empty or contain several candidates | Precision, recall, FPR, FDR, F1, and accuracy |

See [Running the Test Set](/docs/running-the-test-set).

## How it relates to the specification's validation requirements

Section VI.A requires an implementation to demonstrate documented performance on the ONC patient matching test dataset, on a successor dataset, or through an approved third-party assessment approved through the governance process, and to report observed precision, recall, and false-positive rate at the configured operating point. See [Validation Requirements](/docs/validation-requirements).

This test set is built from the ONC dataset. Whether it counts as an approved successor dataset is a governance decision that this site does not make. Accepted proposal v3.3.5 (Test Dataset & Accuracy Methodology, [issue #5](https://github.com/imranq2/cms-hte-patient-matching-spec/issues/5)) concerns the test dataset and accuracy methodology.

## What it does not tell you

- **It does not certify a P(collision) of 2e-12.** Section VI.B asks for validation of P(collision) values using population-scale datasets totaling at least 1 million records. The test set's pools, even in the population tier, are far smaller. The test set README states this limitation.
- **Category counts are not real-world prevalence.** Do not weight categories by their counts to estimate real-world accuracy.

## Contributing test data

Test data contributions follow the test set's own rules: only synthetic records derived from a disclosed method, or cited aggregate statistics; no raw real records. See [Contribute](/docs/contribute).

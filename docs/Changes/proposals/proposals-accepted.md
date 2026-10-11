---
title: "Accepted Proposals"
excerpt: "Proposals that were accepted and are part of specification v3.4.0."
hidden: true
---

All five accepted proposals are incorporated in [v3.4.0](/docs/v3-4-0), according to that version's Executive Summary.

| Proposal | Summary | Affected specification sections | Submitted | Shipped in | Discussion |
|---|---|---|---|---|---|
| **v3.3.1**: Household-Then-Individual Matching | Splits matching for 8 rules into two steps: first prove the household, then prove the individual inside it, and multiply the two probabilities. The other rules are unchanged. | Section III.C, Tables 2, 3 and 4, as numbered in the proposal | 2026-07-03 | [v3.4.0](/docs/v3-4-0) | [Issue #1](https://github.com/imranq2/cms-hte-patient-matching-spec/issues/1) |
| **v3.3.2**: Compliance, Testing & Audit Clarifications | Splits compliance into Path A (rules-based, assumed compliance) and Path B (performance-based, empirical compliance), with separate audit tracks. Adds a sentence clarifying that SHALL language describes future obligations, and a definition of "conservative floor". | Purpose and Executive Summary, IV.A, VI.A, VII, as numbered in the proposal | 2026-07-15 | [v3.4.0](/docs/v3-4-0) | [Issue #2](https://github.com/imranq2/cms-hte-patient-matching-spec/issues/2) |
| **v3.3.3**: Relationship-Based Matching for Minors and Newborns | Uses relationship data defensively, to flag same-household false positives, and offensively, with new rules 39 (guardian-verified minor) and 40 (newborn via maternal linkage). | IV.D, Table 2, Table 3, as numbered in the proposal | 2026-07-15 | [v3.4.0](/docs/v3-4-0) | [Issue #3](https://github.com/imranq2/cms-hte-patient-matching-spec/issues/3) |
| **v3.3.4**: Placeholder Value Exclusion in Patient Matching | Treats known placeholder values as if the field were blank, for every field Table 2 relies on, using a reference table of patterns that is maintained through governance. | V.D, VIII, as numbered in the proposal | 2026-07-15 | [v3.4.0](/docs/v3-4-0) | [Issue #4](https://github.com/imranq2/cms-hte-patient-matching-spec/issues/4) |
| **v3.3.5**: Test Dataset & Accuracy Methodology | States the commitment to an accuracy floor up front in the core principles and charters a follow-on effort to define the number and build the test dataset. It does not set the number. | II, VI, as numbered in the proposal | 2026-07-15 | [v3.4.0](/docs/v3-4-0) | [Issue #5](https://github.com/imranq2/cms-hte-patient-matching-spec/issues/5) |

"Submitted" is the date printed on each proposal.

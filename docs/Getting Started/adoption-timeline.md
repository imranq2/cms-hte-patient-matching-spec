---
title: "Adoption Timeline"
excerpt: "What the specification says about dates, transition periods, and phased adoption."
hidden: true
---

The specification is a draft. This page collects what it says about timing, and what has not been decided. It adds no requirements.

## Current status

| Item | Value | Source |
|---|---|---|
| Version | 3.4.0 | Document Control |
| Status | Final Consolidated Draft | Document Control |
| Release date | 9/10/2026, as printed (the date format is ambiguous) | Document Control |
| Comment period ends | `[Date + 60 days]`, a placeholder | Document Control |
| Effective date | `[TBD after finalization]` | Document Control |

The specification says its SHALL language describes requirements that would apply once the framework is adopted. It does not create a present obligation during any comment period (Purpose).

## What the specification says about timing

| Topic | What it says | Section |
|---|---|---|
| Public comment on changes | Changes that materially affect Table 2, the threshold, approved fields, normalization rules, fuzzy constraints, or required testing are published for public comment for not less than 30 calendar days, unless an emergency update is needed to address a material patient-safety, privacy, security, or compliance risk. | [Governance and Versioning](/docs/governance-and-versioning) |
| Transition period | Substantive changes include a transition period of not less than 90 days unless a shorter period is necessary to mitigate immediate risk. | [Governance and Versioning](/docs/governance-and-versioning) |
| Accuracy floor | The numeric floor for precision, recall, and false-positive rate is to be established through a follow-on effort before the framework's effective date, with interim reporting-only in the meantime. | [Validation Requirements](/docs/validation-requirements) |
| Collision-value validation | The P(collision) values used to approve Table 2 combinations are to be empirically validated at the framework level within 12 months of proposal adoption, using datasets totaling at least 1 million records. | [Validation Requirements](/docs/validation-requirements) |
| Phased adoption and safe harbor | The specification proposes a phased adoption period and a documented safe harbor for organizations whose current matching performance is demonstrably at or above its collision and recall benchmarks, regardless of method. | [Implementation and Testing](/docs/implementation-and-testing) |
| New test dataset versions | As the ONC dataset is revised, or an approved successor becomes available, implementations validate against the current approved version within the implementation period established through governance. | [Validation Requirements](/docs/validation-requirements) |

## Not yet set

- The effective date.
- The end of the comment period (a placeholder in the specification).
- The accuracy floor number.
- The length of the phased adoption period, which the specification does not specify.

## Open changes

Two proposals are under review and could change the specification before it takes effect. See [Under Review](/docs/proposals-under-review).

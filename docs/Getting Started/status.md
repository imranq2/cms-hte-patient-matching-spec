---
title: "Status"
excerpt: "The current version, what is open, and notes on the specification text."
hidden: true
---

## Current version

| Item | Value |
|---|---|
| Specification | v3.4.0, Final Consolidated Draft |
| Release date | 9/10/2026, as printed in the specification's Document Control table |
| Comment period | Open. The end date is the placeholder `[Date + 60 days]` in the specification. |
| Effective date | Not set (`[TBD after finalization]`) |

See the [Changelog](/docs/changelog) and the [Compatibility Matrix](/docs/compatibility-matrix).

## Open proposals

Two proposals are under review: v3.3.6 (Institutional Address Identification Methodology) and v3.4.1 (Remove Rule 29). See [Under Review](/docs/proposals-under-review).

## Rule counts

The specification's Executive Summary counts 30 Category 1 rules and 8 Category 2 rules, and also describes two new rules, 39 and 40, which appear in the section III.C.4 table. That is 40 rules in total. The reference library implements 39, because it omits rule 29 ahead of proposal v3.4.1. Always state which specification version a rule count refers to.

## Notes on the specification text

These are observations about the text of v3.4.0 that readers may trip over. They are not changes; the specification's wording is reproduced here without modification. If you think one is an error in the specification, send a comment (see [Report an Issue](/docs/report-an-issue)).

- **Section references from earlier proposals.** Several passages in section III.C use section numbers such as §3.3, §3.4, §3.7, §3.9, §4.3, §4.4 and §4.5, which come from the proposal that introduced them and do not match the numbering of v3.4.0.
- **Rule numbers in prose.** Section III.C.8 refers to "Rules 13, 14, 15, 16, 34, 35, 37, and 38" for the household-then-individual pairings, but Table 2 numbers its Category 1 rules 01 to 30, so 13 to 16 there are different rules. Section III.C.7 refers to "Rule 26" for a persistent identifier with ≈0 collision, whereas Table 2 lists namespace-bound unique identifiers as rule 22 and rule 26 is Email Address + Member ID.
- **Which fields may be fuzzy.** Section IV.C says fuzzy comparison may be used only for first name, last name, and street line. Table 2 also marks date of birth with an asterisk, and its notes allow a ±1-day tolerance for it.
- **Combination counts.** Section IV.D describes an analysis of 2554 combinations reduced to 1150, and about 68 additional combinations that could be added. The chart in the same section reports 692 canonical combinations, 556 threshold-qualified, 224 that are not a superset of a threshold-qualified combination, and 20 reference-list rows. The specification does not explain how these counts relate.
- **Validation population.** Section VI.B says individual participants "are required to assemble a dataset of that size on its own in order to comply", which reads as inconsistent with the preceding sentence listing who may perform the validation.
- **Interrupted text.** Section VI.A contains a sentence about the ONC dataset that is interrupted by two unrelated paragraphs, and section VI.B has a sentence that ends mid-clause ("SHOULD perform ecosystem-specific validation or").
- **Two tables about administrative restrictions.** The table in section III.C.6 (Administrative Restrictions) and the table captioned Table 4 in section IV.D are separate tables. Only the latter is labeled Table 4.

## Formatting repairs on this site

The specification pages reproduce the specification's wording without change. Two formatting repairs were made in [References](/docs/references): reference 1's page range, which the source splits across two paragraphs, was joined, and reference 7's URL, which the source splits with only the first half linked, was joined and linked in full.

---
title: "Compatibility Matrix"
excerpt: "Which versions of the specification, library, test set, and service go together."
hidden: true
---

*Last updated 2026-10-10 from the public package indexes and repository tags. Update this page at every specification release and every library, test set, or service release.*

## Current versions

| Component | Latest release | Released | Specification version it targets |
|---|---|---|---|
| Specification | v3.4.0, Final Consolidated Draft | 9/10/2026, as printed in the specification's Document Control table | n/a |
| Patient matching library (`cms-hte-patient-matching`) | 0.0.12 on PyPI | 2026-10-07 | v3.4.0, per its README |
| Test set (`cms-hte-patient-matching-test-set`) | tag `0.0.5` | 2026-10-07 | Not stated in its top-level README. Its test-data README says it excludes true-match pairs that only rule 29 could link. |
| Patient matching service | tag `0.0.11` | 2026-10-07 | Wraps the library. It depends on `cms-hte-ial2-reader` 0.0.4 or later, and on `cms-hte-patient-matching` 0.0.11 or later only through its optional `matching` extra. The default public build leaves the library out and returns 503 from `$match`. |
| IAL2 reader (`cms-hte-ial2-reader`) | 0.0.5 on PyPI | 2026-10-07 | Implements token handling for section III.D. Source repository is not public. |
| Hosted testing UI | Not recorded | | Which library version it runs is not published |

## Known differences

- **Rule 29.** Specification v3.4.0 lists rule 29. The library does not implement it, and the test set excludes pairs only rule 29 could link, ahead of proposal v3.4.1 (remove rule 29), which is under review ([issue #7](https://github.com/imranq2/cms-hte-patient-matching-spec/issues/7)). Until v3.4.1 is accepted, an implementation built strictly to v3.4.0 includes rule 29, so its results will differ from the library's and from the test set's expectations on those pairs.
- **Rule counts.** The specification's Category 1 count is 30, and the library implements 29. The library's README therefore says 29 Category 1 rules plus 10 Category 2 rules.

See the [Spec-to-Code Map](/docs/spec-to-code-map) for rule-level detail.

## How to use this page

Pin the specification version, library version, and test set release together when you report validation results, and record them with your results. If you need a combination not listed here, check the repositories' release notes.

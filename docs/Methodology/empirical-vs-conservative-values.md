---
title: "Empirical vs. Conservative Values"
excerpt: "The specification's conservative u-values compared with empirical estimates from public data."
hidden: true
---

*Source of truth: [`calculations/docs/conservative_u_comparison.md`](https://github.com/icanbwell/cms-hte-patient-matching/blob/main/calculations/docs/conservative_u_comparison.md) and the generated [`outputs/u_probabilities.md`](https://github.com/icanbwell/cms-hte-patient-matching/blob/main/calculations/outputs/u_probabilities.md). The values below are copied from those files as of repository commit `0b50516`. They change if the tool is re-run, so check the repository for current values.*

<Callout icon="⚠️" theme="warn">
  The ratio in the last column is the specification's conservative value divided by the tool's estimate. It is **not** a measure of how over-cautious a value is for every row. Rows marked as a floor, proxy, or closed form do not measure what the specification's value is meant to cover. Read the notes under the table before drawing any conclusion.
</Callout>

## Two kinds of numbers

- **Conservative u (input, from the specification).** The hand-picked assumptions in the specification's Table 3. The tool does not produce them. They are the values being checked against.
- **Empirical u (calculated by the tool).** Derived from public data, or from a closed form for SSN and ITIN. See [u-Probability Calculations](/docs/u-probability-calculations).

## Fields the tool computes

| Field | Variant | Conservative u (spec) | Empirical u (tool) | Ratio |
|---|---|---|---|---|
| Last name | exact | 0.005 | 0.0006779 | 7.38x |
| Last name | fuzzy | 0.01 | 0.0008325 | 12.01x |
| First name | exact | 0.02 | 0.001793 | 11.16x |
| First name | fuzzy | 0.03 | 0.002257 | 13.29x |
| Middle name | exact | 0.01 | 0.001793 (proxy) | 5.58x |
| Year of birth | exact | 0.015 | 0.01178 | 1.27x |
| Date of birth (full) | exact | 0.0001 | 3.226e-05 | 3.10x |
| ZIP code (5-digit) | exact | 0.0003 | 9.698e-05 | 3.09x |
| State | exact | 0.06 | 0.04455 | 1.35x |
| City | exact | 0.01 | 0.003121 (bound a) | 3.20x |
| Street line | exact / fuzzy | 0.00003 / 0.00006 | see note | see note |
| Phone number | exact | 0.000001 | 1.31e-09 (co-resident landline floor) | see note |
| SSN last 4 | exact | 0.0001 | 0.0001 (1/9999, closed form) | 1.00x |
| ITIN last 4 | exact | 0.0001 | 0.0001 (1/9999, assumed by analogy) | 1.00x |
| MBI | exact | 0.000001 | 1.471e-08 (1/N, N = 2024 Medicare enrollment) | 67.99x |

## Notes on specific rows

- **Year of birth (1.27x).** The tightest margin of any computed field. The tool's documentation says it is worth revisiting whether 0.015 is the right conservative value.
- **City (3.20x).** The headline is bound (a), which covers only the 63.1% of the population living in a Census place or Census Designated Place. Bound (b), which treats everyone else as unique, gives 1.243e-03, so the coverage-adjusted ratio against 0.01 is closer to 8x.
- **Street line.** The specification's value is conditional on the ZIP already matching. The tool's closest quantity is `street_line_given_zip` (6.527e-05), which is *higher* than the specification's 0.00003. The tool's other quantity, `street_line_with_zip` (6.33e-09), is the joint probability of street line and ZIP and answers a different question, so its ratio (4739x) should not be read as over-conservatism. Both are co-resident floors that ignore unrelated households on the same street name.
- **Phone.** The 763x ratio against 0.000001 is not evidence that the specification's value is overly cautious. The tool's number covers only landline sharing among co-resident household members. It excludes shared "family contact" numbers and mobile number reassignment, which the tool names but does not quantify.
- **SSN and ITIN last 4 (1.00x).** This is not an independent check: the specification's value and the tool's closed form are the same calculation. The closed form holds only for SSNs issued on or after 2011-06-25. Earlier SSNs were assigned sequentially, so the population-wide value is likely higher. The tool does not estimate that cohort. For ITIN, the IRS has not published a randomization policy, so the closed form is an unverified assumption.
- **Middle name (5.58x).** Based on a proxy (the first-name distribution), not a direct measurement. Indicative only.
- **MBI (67.99x).** A namespace-size floor assuming every MBI is issued to exactly one person. The specification's value is set well above it deliberately, to cover duplicate issuance, reissuance, and transcription errors.
- **Fuzzy name values** were revised after two bug fixes recorded in the tool's documentation. The values in the table are the corrected ones.

## Fields the tool does not compute

For these, only the specification's value exists. They are not discrepancies.

| Field | Conservative u (spec) | Why the tool cannot compute it |
|---|---|---|
| Suffix | 0.2 | Dismissed in the specification; no public suffix frequency table |
| Year of birth (dismissed variant) | 0.015 | Dismissed in the specification separately from the exact variant computed above |
| Email address | 0.000001 | Same shape as phone; no public sharing-rate survey is used |
| Legal ID | 0.000001 | Namespace-specific per issuing authority; no single public count |
| Namespace-bound unique identifiers (EMPI, FHIR Patient Identifier, CSP UUID) | ≈0 | Namespace size is an organization's own patient count, which is internal data |
| Insurance Member ID | 0.000001 | Payer-specific enrollment; no single public figure |
| Insurance Subscriber ID | 0.0001 | Same as Member ID; the roughly 40% dependent-sharing assumption is not validated against public data |
| Relationship Linkage, clinical source | 0.01 | An error-rate question that needs an internal accuracy study |
| Relationship Linkage, self-reported or intake | 0.05 | Same as above |

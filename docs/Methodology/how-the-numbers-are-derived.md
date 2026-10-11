---
title: "How the Numbers Are Derived"
excerpt: "From field frequencies to u-probabilities to P(collision) to the Table 2 threshold, and how the calculations project checks them."
hidden: false
---

This page explains where the probabilities in the specification come from, and what the [calculations project](https://github.com/icanbwell/cms-hte-patient-matching/tree/main/calculations) does and does not do. It is written for data scientists and reviewers. The specification text governs; see the [Probability Model](/docs/probability-model) pages for the normative wording.

## The chain from data to Table 2

1. **Per-field u-probability.** For a single field, the u-probability is the probability that two distinct people share the same value. Specification section IV.C gives the exact form, with counts n<sub>i</sub> across N distinct individuals: `u_field = Σ[n_i(n_i − 1)] / [N(N − 1)]`. For large populations it is approximated as `Σ(f_i²)`, where f<sub>i</sub> is the relative frequency of value i. For an approximately uniform field it is approximated as `1 / N_distinct`.
2. **Conservative single-point values.** The specification does not use measured frequencies directly. Its Table 3 assigns each field a *conservative* u-value, described as a single-point assumption based on expected cardinality, skew, missingness, and data quality, "for threshold setting, comparative scoring, and rule classification, not for precise actuarial measurement" (section IV.C). See [Per-Field Collision Probabilities](/docs/per-field-collision-probabilities).
3. **Joint probability for a combination.** For a combination of fields, the specification approximates P(collision) as the product of the fields' u-values. It calls this a first-order heuristic and states that it should not be read as a claim that fields are independent (section IV.D). See [Joint Collision Probability](/docs/joint-collision-probability).
4. **The threshold.** A combination whose P(collision) is at or below 2e-12 is *eligible* for Table 2. Meeting the threshold is necessary, not sufficient; administrative risks such as data independence, shared contact channels, reassignment, multiple births, and generational names are evaluated as well (Core Principle 6 and section IV.D).
5. **Category 2 rules.** For the household-then-individual rules, the combined probability is the product of a household-tier value (Table 2-H) and an individual-tier value (Table 2-I). See [Category 2: Household and Individual Rules](/docs/category-2-household-and-individual-rules).

## What the specification says these numbers are

Section IV.A states that exact national collision probabilities cannot be known with precision for every field and combination. The values are described as order-of-magnitude estimates for threshold setting, relative comparison, and risk ranking, and as provisional and subject to recalibration as better population-specific data become available. Section IV.F and section VI.B describe ecosystem-specific and framework-level validation of the values.

## What the calculations project is

The calculations project (`calculations/` in the [cms-hte-patient-matching repository](https://github.com/icanbwell/cms-hte-patient-matching)) is a standalone tool. It downloads public U.S. Census, ACS, and CMS data and computes *empirical* u-probabilities for the fields it can measure. Its purpose is to check the specification's conservative values against real numbers, so that those values can be justified or revisited.

Points that are easy to get wrong:

- **The specification's u-values are chosen independently.** They are not outputs of the calculations project. The project's own documentation describes them as the "hand-picked" values "being checked against".
- **The project does not change the specification or the model.** Its documentation says it produces evidence, not a conclusion; a change to the model's u-values would be a separate, reviewed change.
- **The project is not part of the reference matching library.** It does not import from the library and uses no patient data, only public aggregate data.
- **It covers some fields, not all.** Several fields cannot be estimated from public data. See [Empirical vs. Conservative Values](/docs/empirical-vs-conservative-values).

## Where to go next

- [u-Probability Calculations](/docs/u-probability-calculations): the formulas and the per-field method.
- [Data Sources](/docs/data-sources): what data is used, with attribution.
- [Empirical vs. Conservative Values](/docs/empirical-vs-conservative-values): the comparison table and its caveats.
- [Known Limitations](/docs/known-limitations)
- [Reproducing the Calculations](/docs/reproducing-the-calculations)
- [Test Set Methodology](/docs/test-set-methodology): how the labeled test cases were generated.

---
title: "FAQ"
excerpt: "Short answers to common questions, with the sections they come from."
hidden: true
---

Each answer summarizes the specification and links to the governing text. The specification governs.

## What does the specification require?

If a query's identity attributes correspond to a combination in Table 2, and the query produces a unique candidate, the responding entity SHALL return matching records for that patient within the permitted scope. See [For Decision Makers](/docs/for-decision-makers).

## What is P(collision)?

The probability that two distinct individuals in the population share identical values for a given combination of fields. It measures the discriminating power of the combination itself, independent of any algorithm or vendor. See [Summary and Purpose](/docs/summary-and-purpose) and [How the Numbers Are Derived](/docs/how-the-numbers-are-derived).

## Why 2e-12?

Core Principle 1 says thresholds SHALL NOT be arbitrary and states the threshold as 2e-12, or 1 in 500 billion. Section IV.D says the threshold was chosen from the clustering of combinations commonly used in national matching products, compared against a distribution of field combinations and their supersets. See [Joint Collision Probability](/docs/joint-collision-probability).

## Is meeting the threshold enough for a combination to be approved?

No. The specification calls passing the threshold a necessary condition, not a sufficient one. Administrative risks such as data independence, shared contact channels, reassignment, multiple births, and generational names are evaluated too. See [Joint Collision Probability](/docs/joint-collision-probability) and [Administrative Restrictions](/docs/administrative-restrictions).

## Do we have to collect SSN or ITIN?

No. An organization's decision not to collect them does not constitute non-compliance. Full SSN and full ITIN SHALL NOT be transmitted in matching queries; only the last four digits are used, as optional attributes. See [SSN and ITIN](/docs/ssn-and-itin).

## Is fuzzy matching allowed?

Yes, within limits. It applies only where Table 2 marks a field, it is not applied to strings shorter than 5 characters, and Soundex and other phonetic matching are prohibited, except that phonetic comparison on first and last name is permitted where the implementer can validate the technique against the approved test datasets at or below the framework's false-positive threshold. See [Fuzzy Matching](/docs/fuzzy-matching).

## What if more than one record matches?

A match requires a unique candidate. The specification describes escalation when two candidates are found and a stricter threshold, with a possible decline, when three or more are found. See the [Implementation Guide](/docs/implementation-guide).

## Do we have to implement Table 2 exactly?

The specification describes two compliance paths: Path A (Assumed Compliance, rules-based) and Path B (Empirical Compliance, performance-based). It states that the framework is a baseline against which existing methods can be tested, not a mandated replacement for methods that already meet or exceed its performance. See [Implementation and Testing](/docs/implementation-and-testing).

## How do we check our implementation?

The specification asks for documented performance on the ONC patient matching test dataset, on a successor dataset, or through an approved third-party assessment, reporting precision, recall, and false-positive rate. The public [test set](/docs/test-set) is built from the ONC dataset. See [Validation Requirements](/docs/validation-requirements).

## Is the reference implementation required?

No. The [reference implementations](/docs/reference-implementations) are provided to help. If one differs from the specification text, the specification governs.

## Does the specification say what data to return, or how?

No. It defines when a responding entity returns matching records, and does not set governance or protocol recommendations beyond matching, such as the data returned, exchange purposes, or enforcement. See [Summary and Purpose](/docs/summary-and-purpose).

## When does it take effect?

The effective date has not been set. See [Adoption Timeline](/docs/adoption-timeline).

## How do I comment, or propose a change?

See [Report an Issue](/docs/report-an-issue) and [Contribute](/docs/contribute).

---
title: "Patient Matching Service UI"
excerpt: "A hosted page for trying the matching service with synthetic data."
hidden: false
---

b.well hosts an instance of the patient matching service at [patient-matching-service.bwell.com](https://patient-matching-service.bwell.com). The service README places its manual-testing page at the path `/testing-ui`.

<Callout icon="⚠️" theme="warn">
  **Use synthetic data only.** The page accepts synthetic test data. Never enter real patient data. The [test set](/docs/test-set) contains records you can use.
</Callout>

## What the testing page does

According to the service's README, the testing page lets you do two things:

- Paste an IAL2 token and see the FHIR `Patient` it decodes to.
- Paste two FHIR `Patient` resources, run real matching, and see which rule matched, or why they did not match.

The matching it runs is the [patient matching library](/docs/patient-matching-library), so the rule that matched is one of the rules in the [Spec-to-Code Map](/docs/spec-to-code-map). According to the service's source, the explanation of why two records did not match is built from the Category 1 and household-then-individual rules (`C2-13` to `C2-38`) and does not include the relationship rules `C2-39` and `C2-40`.

## Limits

- It is a testing aid, not a production endpoint. For an HTTP endpoint you can deploy, see [Service and IAL2 Reader](/docs/service-and-ial2-reader).
- A result is only as current as the library and specification version the hosted instance runs. See the [Compatibility Matrix](/docs/compatibility-matrix).
- Matching behavior can differ from the specification text. If it does, the specification governs. Report differences using [Report an Issue](/docs/report-an-issue).

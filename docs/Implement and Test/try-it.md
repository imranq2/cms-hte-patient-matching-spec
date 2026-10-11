---
title: "Patient Matching Service UI"
excerpt: "A hosted page for trying the matching service with synthetic data."
hidden: true
---

b.well hosts an instance of the patient matching service with a manual-testing page at [patient-matching-service.bwell.com](https://patient-matching-service.bwell.com).

<Callout icon="⚠️" theme="warn">
  **Use synthetic data only.** The page accepts synthetic test data. Never enter real patient data. The [test set](/docs/test-set) contains records you can use.
</Callout>

## What the testing page does

According to the service's README, the testing page lets you do two things:

- Paste an IAL2 token and see the FHIR `Patient` it decodes to.
- Paste two FHIR `Patient` resources, run real matching, and see which rule matched, or why they did not match.

The matching it runs is the [patient matching library](/docs/patient-matching-library), so the rule that matched is one of the rules in the [Spec-to-Code Map](/docs/spec-to-code-map).

## Limits

- It is a testing aid, not a production endpoint. For an HTTP endpoint you can deploy, see [Service and IAL2 Reader](/docs/service-and-ial2-reader).
- A result is only as current as the library and specification version the hosted instance runs. See the [Compatibility Matrix](/docs/compatibility-matrix).
- Matching behavior can differ from the specification text. If it does, the specification governs. Report differences using [Report an Issue](/docs/report-an-issue).

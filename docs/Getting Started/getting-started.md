---
title: Welcome to Patient Matching
excerpt: The CMS HealthTech Ecosystem Patient Matching Specification, with the tools to implement and test it.
hidden: false
---
<Callout icon="📘" theme="info">
  **Status:** specification v3.4.0, Final Consolidated Draft. Its effective date has not been set, and the end of its comment period is a placeholder in the specification. Two proposals are [under review](/docs/proposals-under-review). See [Status](/docs/status).
</Callout>

The specification defines when a responding entity SHALL return matching patient records. If the identity attributes in a query correspond to a combination listed in Table 2, and the query produces a unique candidate, the responding entity returns the records for that patient within the permitted scope for that query, subject to the administrative controls in section IV.D and Table 4. Table 2 lists combinations whose conservative probability of collision is 2e-12 (1 in 500 billion) or lower and that satisfy additional administrative controls. Two relationship-based rows carry caveats that the specification itself flags as unresolved.

This site hosts the specification, explains how its numbers are derived, and gives you the software and test data to check your implementation. The code, data, and documentation behind it are public.

## Start with your role

<Cards>
  <Card title="Decision makers" href="/docs/for-decision-makers" icon="fa-duotone fa-briefcase">What the specification requires of an organization, and why</Card>

  <Card title="Engineers" href="/docs/implementation-guide" icon="fa-duotone fa-code">How to evaluate a query, and how to show your implementation conforms</Card>

  <Card title="Data scientists" href="/docs/how-the-numbers-are-derived" icon="fa-duotone fa-chart-line">How the collision probabilities were calculated, from what data</Card>

  <Card title="Reviewers and commenters" href="/docs/summary-and-purpose" icon="fa-duotone fa-comments">Read the specification, review proposals, and send comments</Card>
</Cards>

<br />

## What's here

<Cards>
  <Card kind="tile" title="Specification" href="/docs/summary-and-purpose" icon="fa-duotone fa-book">The full text of v3.4.0, one topic per page</Card>

  <Card kind="tile" title="Test set" href="/docs/test-set" icon="fa-duotone fa-vial">Labeled cases for validating an algorithm</Card>

  <Card kind="tile" title="Reference implementations" href="/docs/reference-implementations" icon="fa-duotone fa-terminal">A Python library and a matching service</Card>

  <Card kind="tile" title="Try it" href="/docs/try-it" icon="fa-duotone fa-flask">A hosted page for trying the matching service with synthetic data</Card>

  <Card kind="tile" title="Changelog" href="/docs/changelog" icon="fa-duotone fa-clock-rotate-left">What changed in each version</Card>

  <Card kind="tile" title="Proposals" href="/docs/proposals" icon="fa-duotone fa-file-pen">Proposals under review and accepted</Card>
</Cards>

<br />

## Get involved

- [Report an issue](/docs/report-an-issue) or comment on the draft.
- [Contribute](/docs/contribute) a proposal, test data, code, or documentation.
- See who has [contributed](/docs/contributors).

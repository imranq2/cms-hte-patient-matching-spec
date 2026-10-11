---
title: "Proposals"
excerpt: "How changes to the specification are proposed, reviewed, and accepted."
hidden: false
---

Changes to the specification go through the governance process in [Governance and Versioning](/docs/governance-and-versioning). Proposals are GitHub issues in the [docs repository](https://github.com/imranq2/cms-hte-patient-matching-spec/issues), so their discussion and status are public.

## What a proposal contains

The specification requires a proposed change to include a description of the change, the rationale for the change, the anticipated implementation impact, and, where applicable, a validation plan or supporting evidence.

## Review and adoption

- Changes that materially affect Table 2, the framework threshold, approved fields, normalization rules, fuzzy constraints, or required testing are published for public comment for not less than 30 calendar days, unless an emergency update is needed to address a material patient-safety, privacy, security, or compliance risk.
- After review of comments and supporting evidence, adopted changes are published with a version increment and an effective date. Substantive changes include a transition period of not less than 90 days unless a shorter period is necessary to mitigate immediate risk.
- Proposals are decided by the workgroup. This is a convention of this project; the specification's governance text does not name who decides.

## Statuses

Each proposal issue carries a `proposal` label and one status label:

| Status | Label | Page |
|---|---|---|
| Under review | `status: under-review` | [Under Review](/docs/proposals-under-review) |
| Accepted | `status: accepted` | [Accepted](/docs/proposals-accepted) |
| Rejected | `status: rejected` | [Rejected and Withdrawn](/docs/proposals-rejected-and-withdrawn) |
| Withdrawn | `status: withdrawn` | [Rejected and Withdrawn](/docs/proposals-rejected-and-withdrawn) |

The specification's governance text describes how changes are adopted. It does not define rejected or withdrawn outcomes, so those two statuses are a convention of this site's proposal tracking.

## Submitting a proposal

See [Contribute](/docs/contribute).

## Numbering

Existing proposals are named by the version number they were drafted for, for example "Proposal v3.3.1". Proposals v3.3.1 to v3.3.6 each modify v3.3.0, and proposal v3.4.1 modifies v3.4.0. Section references inside a proposal use the section numbering of the version it modifies, which can differ from the current specification's numbering.

---
title: "Governance and Versioning"
excerpt: "Specification v3.4.0, section VIII"
hidden: false
---

*Specification v3.4.0, section VIII*

This framework SHALL be maintained through a documented governance process that supports transparency, reproducibility, public review, and orderly implementation. A proposed change SHALL include a description of the change, the rationale for the change, the anticipated implementation impact, and, where applicable, a validation plan or supporting evidence. Changes that materially affect Table 2,  
the framework threshold, approved fields, normalization rules, fuzzy constraints, or required testing SHALL be published for public comment for not less than calendar 30 days, unless an emergency update is needed to address a material patient-safety, privacy, security, or compliance risk.

After review of comments and supporting evidence, adopted changes SHALL be published with a version increment and an effective date. Substantive changes SHALL include a transition period of not less than 90 days unless a shorter period is necessary to mitigate immediate risk. Supporting validation results for substantive changes SHOULD be made available in a form that allows participants to understand the operational impact of the change.

Semantic versioning, in the form Major.Minor.Patch, SHALL be used. A Major version change indicates a change to the framework threshold, core methodology, or other foundational requirement. A Minor version change indicates a substantive implementation change, including additions to or removals from Table 2, support for new fields or identifier classes, or changes to validation or normalization requirements that materially affect matching behavior. A Patch version change indicates clarifications, corrections, citation updates, or other non-substantive revisions that do not materially change participant obligations.

An approved combination SHALL be reviewed for restriction, suspension, or removal when framework-level validation, ecosystem-specific validation, or sustained operational monitoring shows that the combination may no longer perform within the framework threshold or risk assumptions. Grounds for such action include observed P(collision) above the framework threshold, systematic issues in collision detection or implementation performance, or sustained false-positive behavior attributable to the combination. Where immediate risk mitigation is needed, a combination MAY be temporarily suspended pending full review. All such actions SHALL be documented and communicated through the governance process.

---
title: "Core Principles"
excerpt: "Specification v3.4.0, section II"
hidden: true
---

*Specification v3.4.0, section II*

1. Matching thresholds SHALL NOT be arbitrary. Under this framework, the threshold is 2e-12 probability of collision, 0.0000000002% or 1 in 500 billion.

2. Confidence is measured by aggregate Probability of Collision, not field count.

3. If a query matches a Table 2-listed combination and produces a unique candidate, the responding entity shall respond with a match appropriate to the protocol subject to the administrative controls in §IV.D and Table 4\.

4. A match is satisfied only when it produces a unique candidate subject at the source system. Network queries could have unique candidates found at more than one source systems and SHALL return the match from each source system. Compliance for matching is assessed at the source-system level for each Participant; the network’s compliance role is to faithfully convey the query, including the IAL2 Claims Token where present, and to aggregate Participant responses without distortion.

5. Fuzzy techniques are permitted but constrained and testable.

6. Meeting the threshold is the baseline metric for inclusion in the approved list of matching criteria, however, administrative evaluation for known risks such as data independence, shared contract risk, multiple birth risk, and others are also critical to evaluating a criteria.

7. Ongoing validation and transparency are mandatory.

8. False positives (wrong-patient releases) are critical errors and must be minimized — but they are auditable and correctable and we propose operational containment (audit logging, downstream notice under 45 CFR 164.404–410, revocation where technically feasible).  The patient’s rights to notice, accounting (§164.528), and OCR complaint are not extinguished by remediation.

9. False negatives (failure to return data to the correct patient) cause invisible, cumulative harm and must be minimized.

10. Each identity attribute represents a set of values, current and historical. Matching shall evaluate against all known values for a field (e.g., all known last names, all known addresses, all known phone numbers). Historical values are weighed by collision contribution within the combination, not by recency in isolation ; a match on any known value satisfies the field.

11. IAL2 Claims Tokens that can be cryptographically verified with an authorized Credential Service Provider (“CSP”) provide a high level of assurance the identity of the individual and app requesting data has been verified.

12. Covered entities may request PHI from other covered entities without a signed CSP token being required. Patient facing apps not covered by HIPAA may only request records by transmitting a CSP-issued IAL2 Claims Token

13. Implementations SHALL be held to an empirically validated accuracy floor (precision, recall, and false-positive rate), in addition to the 2e-12 collision threshold in Principle 1\. The specific numeric floor and the methodology for measuring it are defined later in this document; this principle states the commitment in advance of that number being set.

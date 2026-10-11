---
title: "Audit and Monitoring"
excerpt: "Specification v3.4.0, section VII"
hidden: false
---

*Specification v3.4.0, section VII*

Each participant SHALL maintain audit and monitoring practices sufficient to explain match decisions, investigate incidents, and identify performance degradation over time.

For each query evaluated under Table 2, the participant SHALL retain information sufficient to reconstruct the decision, including the Table 2 combination evaluated, whether the comparison was exact or fuzzy, the uniqueness-check result, the attribute-level comparison outcomes needed to explain the determination including at a minimum:

* The query initiator

* Table 2 combination evaluated

* Match type (exact or fuzzy)

* Identifiers of records matched

* Uniqueness-check result

* Final match determination

* Timestamp

Where feasible, the participant SHOULD also retain the applicable rules or software version so that the decision can be reproduced during audit or incident review. Audit records SHALL be protected in accordance with applicable privacy and security requirements.

Participants SHALL have an established process to monitor ambiguous match rates, suspected wrong-patient incidents, fuzzy-constraint violations, and material changes in non-return, manual-review, or exception rates.

If monitoring indicates that an approved combination may be degrading, that a rule is being applied incorrectly, or that false-positive behavior may be emerging, the participant SHALL document the issue, take proportionate interim mitigation steps, and escalate the matter through the governance process when the issue could affect Table 2 or the framework threshold.

We are committing to publishing validated population-level collision-rate benchmarks at the framework level, enabling participants to calibrate against their own populations without requiring disclosure of proprietary matching methodologies. 

**Path A Audit: Integrity of Implementation**  
Audit efforts for Path A must focus on verifying the correct application and integrity of the defined rules in Table 2\. "SHALL" obligations here pertain to the fidelity of the rules-based engine.

**Path B Audit: Outcomes & Performance**  
Audit efforts for Path B must focus on macro-level metrics, statistical thresholds, and continuous improvement. "SHALL" obligations here pertain to the accuracy of outcomes and reporting transparency:

- Match / no-candidate / ambiguous rate, as a % of queries evaluated

- Correction rate — matches later revoked or confirmed wrong-patient (the false-positive signal)

- Appeal rate — no-candidate results later found to be an actual match (the false-negative signal)

- Trend over time, so degradation is visible without waiting for an incident

- A thin per-query record for incident investigation only: initiator, records involved, determination, timestamp — methodology-agnostic, no "which rule fired."

- An explicit definition of "every query": every query where a match was attempted, excluding malformed or pre-validation-failed requests.

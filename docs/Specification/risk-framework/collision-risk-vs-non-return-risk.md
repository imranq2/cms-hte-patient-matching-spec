---
title: "Collision Risk vs. Non-Return Risk"
excerpt: "Specification v3.4.0, section III.B"
hidden: false
---

*Specification v3.4.0, section III.B*

The framework approval threshold is P(collision) less than or equal to 2e-12 or 1 in 500 billion. The question, however, is not "is 0.0000000002% probability of collision acceptable?" The question is "compared to what?"

For a typical single-physician practice (\~2,000 patients), the expected number of wrong-patient releases per year from the defined threshold probability of collision is effectively zero.

Meanwhile, the same practice under a 40% match rate silently fails to return data on roughly 3,000 queries per year, each one a missed opportunity to prevent harm.

*Table 1 Threshold comparison: framework standard versus status quo*

|  | 0.0000000002% Collision Threshold | Status Quo (40% match rate) |
| --- | --- | --- |
| Wrong-patient releases/year | ~0 | Unknown (no one measures) |
| Correct data NOT returned/year | Near zero | ~3,000 |
| Detectable? | Yes — auditable | No — invisible |
| Correctable? | Yes — discrete events | No — systemic |

For every query that clears the threshold, there is at most a 1 in 500 billion theoretical probability that the matching field combination could also belong to a different individual. But "could theoretically belong to" is not "will be released to the wrong person." Additional safeguards reduce the actual wrong-release rate to near zero and provide a path to remediation in the event it does.

---
title: "Risk of False Positives"
excerpt: "Specification v3.4.0, section III.B.1"
hidden: true
---

*Specification v3.4.0, section III.B.1*

The harm of non-return is invisible and cumulative. The harm of false positives is discrete and detectable. Both are real, and the framework does not minimize either. The framework’s operational response to false-positive risk has three components.

**First**, the framework operates a tiered match logic. When a query yields a single Table 2-qualifying unique candidate, the responder returns. When a query yields two candidates, the protocol layer MAY escalate to multi-factor authentication or supplementary disambiguation. When a query yields three or more candidates, the responder applies the more stringent 1-in-a-million collision threshold and may decline to return absent further evidence. This is the framework’s primary operational mechanism for managing false-positive risk — not a single absolute threshold.

**Second**, the verified-attribute foundation is materially stronger than the alternatives in routine use today. A patient may request records from a covered entity by fax, by web-portal login, or by paper form. Each of those channels offers substantially less identity assurance than IAL2 identity proofing performed by a Kantara-certified, independently-audited Credential Service Provider with biometric binding and document authentication under NIST SP 800-63A §§5.2 and 5.3. The proposed framework reduces — not increases — the residual false-positive exposure relative to status-quo patient-submission channels.

**Third**, HIPAA at 45 CFR 164.514(h) requires reasonable verification, not perfect verification. The community is proposing through this framework that IAL2 reliance plus the §II matching rules plus the §IV.D administrative controls plus the §VII audit infrastructure constitutes a reasonable verification posture. The relevant liability question is: when an organization uses best-practice identity proofing, a federally-grounded collision threshold, the tiered match-disambiguation logic, and the audit infrastructure described in §VII — and a single-patient error nonetheless occurs at a 1-in-500-billion collision probability — what is the residual liability that does not also attach to fax, portal, or paper channels operating with materially weaker assurance? We believe the answer is: less.

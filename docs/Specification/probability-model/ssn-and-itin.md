---
title: "SSN and ITIN"
excerpt: "Specification v3.4.0, section IV.E"
hidden: true
---

*Specification v3.4.0, section IV.E*

Social Security Numbers (SSN) and Individual Taxpayer Identification Numbers (ITIN) are highly sensitive federal identifiers with well-documented value in improving patient matching accuracy. Full SSN, in particular, functions as a near-deterministic identifier and can materially improve match precision and reduce both false positives and false negatives. These benefits may be especially pronounced for populations with fragmented or unstable demographic data, where SSN may serve as a more persistent identifier than name or address.

This proposal, however, does not permit the use or transmission of full SSN or full ITIN in matching queries. This reflects a deliberate risk tradeoff in the context of a national-scale, multi-party interoperability network. Unlike local or single-organization environments, network-based exchange introduces materially higher risks related to data exposure, including query logging, aggregation across participants, and the potential for unauthorized harvesting of sensitive identifiers. Even when optional, the presence of full SSN in queries would result in its propagation across a broad set of entities, increasing the severity and impact of breach scenarios.

In addition, there is a clear and ongoing trend among covered entities to minimize or eliminate the collection and storage of full SSN due to security, regulatory, and liability considerations. Consumer expectations have similarly evolved, with strong resistance to sharing SSN in digital health workflows and demonstrated impacts on engagement when requested. While some identity proofing workflows may collect SSN at the point of credential issuance, this proposal intentionally avoids extending its use into routine data exchange.

Accordingly, this framework limits use to the last four digits of SSN or ITIN as optional matching attributes. This approach preserves some incremental matching value while materially reducing sensitivity and exposure risk. ITIN is treated with the same sensitivity and handling requirements as SSN throughout this proposal. Full SSN and full ITIN SHALL NOT be transmitted as part of matching queries.

An organization’s decision not to collect SSN or ITIN does not constitute non-compliance with the framework. The framework treats SSN/ITIN as optional throughout, and alternative demographic combinations in Table 2 are independently sufficient. Policy should not incentivize — directly or indirectly — reliance on SSN or ITIN where alternatives perform equivalently. 

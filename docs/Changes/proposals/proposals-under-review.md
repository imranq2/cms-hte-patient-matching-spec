---
title: "Proposals Under Review"
excerpt: "Proposals currently open for review."
hidden: false
---

| Proposal | Summary | Affected specification sections | Submitted | Discussion |
|---|---|---|---|---|
| **v3.3.6**: Institutional Address Identification Methodology | Specifies how a responding entity determines whether an address is institutional. Step 1 matches the address against named public facility registries (CMS, federal and state corrections, IPEDS, HIFLD). Step 2, as a fallback, uses a postal multi-unit signal that routes the address to manual review rather than excluding it. Adds a reference table of data sources. | Section IV.G (Patient Matching for Vulnerable Populations) and section VIII (Governance), as numbered in the proposal | 2026-07-30 | [Issue #6](https://github.com/imranq2/cms-hte-patient-matching-spec/issues/6) |
| **v3.4.1**: Remove Rule 29 (First Name + Last Name + Phone Number + ZIP) | Removes rule 29 from Table 2, retiring its ID without renumbering, because the rule has no date of birth and matched a parent and child sharing a name, phone number, and ZIP code in testing. Updates the Category 1 count from 30 to 29. Notes that rule 29 is currently the only approved rule that can evaluate provider data of the NPPES shape, so provider matching needs a separate follow-up, and says the removal should not be adopted without a decision on provider matching. It also notes that patient queries with name, phone, and ZIP but no date of birth would no longer match. | Section III.C (Table 2), Executive Summary, validation datasets | 2026-10-05 | [Issue #7](https://github.com/imranq2/cms-hte-patient-matching-spec/issues/7) |

"Submitted" is the date printed on each proposal. Section references are as numbered in each proposal.

To comment on a proposal, add a comment to its issue. See [Contribute](/docs/contribute).

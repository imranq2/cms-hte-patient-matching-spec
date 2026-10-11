---
title: "Conformance Checklist"
excerpt: "The specification's SHALL requirements, quoted and linked. Informational, not normative."
hidden: false
---

<Callout icon="📘" theme="info">
  **This checklist is informational and non-normative.** The specification text governs. Each item below is a verbatim quotation from the specification v3.4.0, with a link to the page where it appears. If a quotation here ever differs from the specification, the specification is correct.
</Callout>

## What it covers and what it leaves out

- It lists statements that use SHALL or SHALL NOT, plus the three lowercase "shall" statements in the specification. Where a quotation is shortened to the part that states the requirement, it begins or ends with an ellipsis (…).
- It does **not** list statements phrased as "must" or "required", which the specification also uses in places. Read the linked pages for those, including the rules in Table 2 itself.
- It does not replace the Table 2 rules, the household-then-individual process, or the validation and audit sections. Use the [Implementation Guide](/docs/implementation-guide) for how they fit together.
- The specification says its SHALL language describes requirements that would apply once the framework is adopted, and creates no present obligation during a comment period (Purpose).

Use the boxes to track your own progress. They are not saved.

## Returning a match (Executive Summary, I, II)

- [ ] … If the identity attributes in a query correspond to a field combination listed in Table 2 of this document, and the query produces a unique candidate subject, the responding entity SHALL return matching records for that patient within the permitted scope for that query context. ([source](/docs/summary-and-purpose))

## Core Principles (II)

- [ ] Matching thresholds SHALL NOT be arbitrary. ([source](/docs/core-principles))
- [ ] … the responding entity shall respond with a match appropriate to the protocol subject to the administrative controls in §IV.D and Table 4. ([source](/docs/core-principles))
- [ ] Network queries could have unique candidates found at more than one source systems and SHALL return the match from each source system. ([source](/docs/core-principles))
- [ ] Matching shall evaluate against all known values for a field (e.g., all known last names, all known addresses, all known phone numbers). ([source](/docs/core-principles))
- [ ] Implementations SHALL be held to an empirically validated accuracy floor (precision, recall, and false-positive rate), in addition to the 2e-12 collision threshold in Principle 1. ([source](/docs/core-principles))

## Table 2 notes (III.C)

- [ ] Member ID means the full individual-level identifier inclusive of any dependent suffix; the bare subscriber base value without a dependent suffix SHALL NOT be used under Member ID rules. ([source](/docs/table-2-category-1-rules))
- [ ] For all rules in this group, the Payer ID establishes the namespace and matching SHALL be performed only within that namespace. ([source](/docs/table-2-category-1-rules))

## Category 2: household and individual rules (III.C.2 to III.C.5)

- [ ] A responder MAY log or flag a Last Name mismatch for data-quality review, but SHALL NOT withhold an otherwise-qualifying match because Last Name differs … ([source](/docs/category-2-household-and-individual-rules))
- [ ] A responding entity SHALL return a match when a query's Household-tier fields resolve to exactly one household per Table 2-H (§3.3), its Individual-tier fields resolve to exactly one member of that household per Table 2-I (§3.4), and the product of the two listed probabilities does not exceed 2e-12. ([source](/docs/category-2-household-and-individual-rules))

## Multiple births (III.C.7)

- [ ] Whenever Household-tier matching resolves to more than one candidate sharing an identical DOB, First Name comparison SHALL be exact, not fuzzy … ([source](/docs/multiple-births))
- [ ] … if removal leaves no discriminating value, or the first names are genuinely identical, the query SHALL produce more than one candidate and SHALL NOT resolve to a unique match … ([source](/docs/multiple-births))

## Applying the tables (III.C.8)

- [ ] A step that does not resolve to exactly one candidate SHALL NOT be treated as satisfied for purposes of combining probabilities in step 2 above. ([source](/docs/applying-the-tables))

## IAL2 claims tokens (III.D and III.E)

- [ ] A patient-facing app SHALL include a CSP-issued IAL2 Claims Token in a query to match a patient. ([source](/docs/ial2-claims-tokens))
- [ ] If an IAL2 Claims Token is included in a query, the Responder SHALL validate the token prior to responding. ([source](/docs/ial2-claims-tokens))
- [ ] Validation SHALL include: ([source](/docs/ial2-claims-tokens))
  - [ ] The token's digital signature using the CSP's published JWKS or other applicable key distribution mechanism
  - [ ] The iss claim identifies a trusted CSP. A trusted CSP must use distinct issuer URLs for production and non-production id_tokens.
  - [ ] The aud claim identifies the intended relying party, IAS Provider, or other expected audience for the transaction
  - [ ] The token is unexpired based on the exp claim, or otherwise within the Responder's maximum acceptable age based on iat; and reasonable checks of token integrity and freshness.
  - [ ] Anti-replay controls using the jti claim in combination with issuer context.
- [ ] At a minimum, the Responder SHALL record previously accepted iss + jti values, or maintain equivalent controls, for the applicable token-validity window and SHALL reject subsequent reuse of the same token identifier. ([source](/docs/ial2-claims-tokens))
- [ ] If token validation fails or replay is detected, the Responder SHALL NOT rely on the token or any claim extracted from it for matching or response. ([source](/docs/ial2-claims-tokens))
- [ ] When an IAL2 Claims Token is successfully validated, demographic claims extracted from the token SHALL be used as query demographics for matching. ([source](/docs/ial2-claims-tokens))
- [ ] Such demographics SHALL be subject to the same normalization, placeholder suppression, historical-value handling, exact and fuzzy comparison constraints, approved Table 2 combinations, and uniqueness requirements that apply when the same demographics are transmitted directly in the query. ([source](/docs/ial2-claims-tokens))
- [ ] aud \| Identifies the intended audience of the token \| Required - OIDC SHALL be the App’s Client ID (be it an NPD ID, Medicare App Library client id, etc). ([source](/docs/ial2-claims-tokens))
- [ ] exp \| Expiration time for the token \| Required - OIDC SHALL NOT be &gt; iat+300 ([source](/docs/ial2-claims-tokens))
- [ ] email_verified \| True if the End-User's e-mail address has been verified; otherwise false \| SHALL NOT be populated ([source](/docs/ial2-claims-tokens))
- [ ] phone_number_verified \| True if the End-User's phone number has been verified; otherwise false \| SHALL NOT be populated ([source](/docs/ial2-claims-tokens))

## Probability model (IV)

- [ ] Until such a method is adopted through governance, combinations whose approval depends on a geographic dependency discount SHALL NOT be added to Table 2. ([source](/docs/joint-collision-probability))

## SSN and ITIN (IV.E)

- [ ] Full SSN and full ITIN SHALL NOT be transmitted as part of matching queries. ([source](/docs/ssn-and-itin))

## Ecosystem-specific validation (IV.F)

- [ ] While published population-scale collision probabilities shall be used for initial Table 2 classification, responding entities are encouraged to validate collision probabilities against their own patient populations and report major deviations and observations to CMS. ([source](/docs/ecosystem-specific-collision-validation))

## Insurance identifiers (IV.H)

- [ ] Implementations SHALL NOT substitute the bare subscriber base value for an individual member ID when applying Member ID combinations from Table 2. ([source](/docs/insurance-identifiers))
- [ ] If the implementation cannot confirm that a submitted identifier includes the individual-level suffix, it SHALL treat the identifier as a Subscriber ID and apply the corresponding, more conservative, u-probability. ([source](/docs/insurance-identifiers))
- [ ] Matching SHALL be performed only within the payer namespace established by the co-submitted Payer ID. ([source](/docs/insurance-identifiers))
- [ ] A query that provides an insurance identifier without a Payer ID SHALL NOT be evaluated under any insurance identifier combination in Table 2. ([source](/docs/insurance-identifiers))
- [ ] Implementations SHALL enforce the namespace binding at the Coverage.identifier.system or equivalent level. ([source](/docs/insurance-identifiers))
- [ ] An insurance identifier SHALL NOT be combined solely with other insurance-derived or plan-administrative fields (such as group number, plan type, or enrollment date) in a Table 2 combination … ([source](/docs/insurance-identifiers))

## Required normalization, names, and demographic fields (V.A to V.C)

- [ ] All string matching SHALL be case insensitive ([source](/docs/required-normalization-names-and-demographics))
- [ ] All whitespace SHALL be removed or ignored during matching except as required in normalized address fields ([source](/docs/required-normalization-names-and-demographics))
- [ ] All punctuation (e.g. hyphens, periods, apostrophes, etc) SHALL be removed or ignored during matching except as required in normalized address fields ([source](/docs/required-normalization-names-and-demographics))
- [ ] All string fields shall implement Diacritic folding as part of the matching process ([source](/docs/required-normalization-names-and-demographics))
- [ ] Date of birth SHALL be represented in YYYY-MM-DD format when the full date is known. ([source](/docs/required-normalization-names-and-demographics))
- [ ] If only year or year-month is known, the value SHALL be transmitted as partial and SHALL NOT be imputed, padded, or converted to a full date for matching. ([source](/docs/required-normalization-names-and-demographics))
- [ ] Each implementation SHALL maintain a versioned reference table of nickname values first name field used in matching. ([source](/docs/required-normalization-names-and-demographics))
- [ ] All name fields including First, Middle, Last, Prefix, Suffix, Title and any others SHALL be separated into discrete components used for matching ([source](/docs/required-normalization-names-and-demographics))
- [ ] Matching algorithms SHALL match against ALL known names (maiden, previous, AKA) ([source](/docs/required-normalization-names-and-demographics))
- [ ] For the avoidance of doubt, matching SHALL ignore or remove all punctuation and whitespace in name fields ([source](/docs/required-normalization-names-and-demographics))
- [ ] If a generational suffix can be identified on both the query and the response and they do not match then the responder SHALL NOT return the match. ([source](/docs/required-normalization-names-and-demographics))
- [ ] For the avoidance of doubt, this rule SHALL negate a match that was made by matching a combination in table 2. ([source](/docs/required-normalization-names-and-demographics))
- [ ] Suffix expansion tables SHALL be maintained and integrated to support abbreviations and shorthand. ([source](/docs/required-normalization-names-and-demographics))
- [ ] All addresses SHALL be normalized to Project US@ standard formats by the Requestor and Responder ([source](/docs/required-normalization-names-and-demographics))
- [ ] Address SHALL match regardless of designated type (home, legal, office, physical, postal, etc) ([source](/docs/required-normalization-names-and-demographics))
- [ ] All phone numbers SHALL be normalized to E.164 specifications for matching purposes … ([source](/docs/required-normalization-names-and-demographics))
- [ ] Phone numbers SHALL match regardless of designated type (home, cell, work, etc) ([source](/docs/required-normalization-names-and-demographics))
- [ ] Responders SHALL match against ALL known values, current or historical. ([source](/docs/required-normalization-names-and-demographics))
- [ ] Demographic matching SHALL be performed in a case insensitive manner ([source](/docs/required-normalization-names-and-demographics))

## Placeholder values (V.D)

- [ ] Each implementation SHALL maintain versioned reference tables of non-comparable values (e.g. placeholder values) and patterns for each demographic field used in matching. ([source](/docs/placeholder-values))
- [ ] When a field value is identified as placeholder, temporary, unknown, test, or otherwise non-comparable, that field SHALL be treated as unavailable for use in matching. ([source](/docs/placeholder-values))
- [ ] It SHALL NOT count as an exact match, fuzzy match, nickname match, phonetic match, or conflict. ([source](/docs/placeholder-values))
- [ ] Placeholder-name categories SHALL include, at minimum, newborn temporary names, unidentified-patient names, unknown-value placeholders, and local test or training values. ([source](/docs/placeholder-values))
- [ ] Placeholder suppression SHALL apply to both requestor-side query preparation and responder-side record evaluation. ([source](/docs/placeholder-values))
- [ ] Unknown dates of birth, including all dates of birth prior to the current year – 120 years or after the current date + 2 days SHALL be treated as unavailable for use in matching. ([source](/docs/placeholder-values))
- [ ] Requesters and responders SHALL maintain a reference list of known placeholder values per field and SHALL exclude any field value on that list from matching entirely … ([source](/docs/placeholder-values))

## Fuzzy matching (V.E)

- [ ] Fuzzy matching SHALL NOT be applied to query strings that are less than 5 characters long. ([source](/docs/fuzzy-matching))

## Validation (VI)

- [ ] Before initial production use, and after any material change to matching logic, normalization rules, placeholder handling, fuzzy-comparison settings, or decision thresholds, an implementation SHALL demonstrate documented performance on the ONC patient matching test dataset. ([source](/docs/validation-requirements))
- [ ] The accuracy floor SHALL be established through a follow-on effort before the framework's effective date, with interim reporting-only in the meantime. ([source](/docs/validation-requirements))
- [ ] At a minimum, validation results SHALL report observed precision, recall, and false-positive rate at the configured operating point. ([source](/docs/validation-requirements))
- [ ] Validation SHALL confirm that the implementation correctly handles matches, non-matches, placeholder values, normalization requirements, uniqueness checks, approved fuzzy comparisons, and other material edge cases. ([source](/docs/validation-requirements))
- [ ] Local acceptance testing need not replicate population-scale benchmarking, but it SHALL confirm that required fields, comparison rules, and response behavior operate as configured in production. ([source](/docs/validation-requirements))
- [ ] As the ONC dataset is revised, or as an approved successor dataset becomes available, implementations SHALL validate against the current approved version within the implementation period established through governance. ([source](/docs/validation-requirements))
- [ ] The P(collision) values used to approve combinations in Table 2 are conservative estimates intended for threshold design and rule classification. Those values SHALL be empirically validated at the framework level within 12 months of proposal adoption … ([source](/docs/validation-requirements))
- [ ] … the validation record SHALL report the observed collision rate for the combination's field set, the 95 percent confidence interval, and a description of the validation population … ([source](/docs/validation-requirements))

## Audit and monitoring (VII)

- [ ] Each participant SHALL maintain audit and monitoring practices sufficient to explain match decisions, investigate incidents, and identify performance degradation over time. ([source](/docs/audit-and-monitoring))
- [ ] For each query evaluated under Table 2, the participant SHALL retain information sufficient to reconstruct the decision … ([source](/docs/audit-and-monitoring))
- [ ] Audit records SHALL be protected in accordance with applicable privacy and security requirements. ([source](/docs/audit-and-monitoring))
- [ ] Participants SHALL have an established process to monitor ambiguous match rates, suspected wrong-patient incidents, fuzzy-constraint violations, and material changes in non-return, manual-review, or exception rates. ([source](/docs/audit-and-monitoring))
- [ ] If monitoring indicates that an approved combination may be degrading, that a rule is being applied incorrectly, or that false-positive behavior may be emerging, the participant SHALL document the issue, take proportionate interim mitigation steps, and escalate the matter through the governance process … ([source](/docs/audit-and-monitoring))

## Governance and versioning (VIII), which apply to maintainers of the framework

- [ ] This framework SHALL be maintained through a documented governance process that supports transparency, reproducibility, public review, and orderly implementation. ([source](/docs/governance-and-versioning))
- [ ] A proposed change SHALL include a description of the change, the rationale for the change, the anticipated implementation impact, and, where applicable, a validation plan or supporting evidence. ([source](/docs/governance-and-versioning))
- [ ] Changes that materially affect Table 2, the framework threshold, approved fields, normalization rules, fuzzy constraints, or required testing SHALL be published for public comment for not less than calendar 30 days, unless an emergency update is needed to address a material patient-safety, privacy, security, or compliance risk. ([source](/docs/governance-and-versioning))
- [ ] After review of comments and supporting evidence, adopted changes SHALL be published with a version increment and an effective date. ([source](/docs/governance-and-versioning))
- [ ] Substantive changes SHALL include a transition period of not less than 90 days unless a shorter period is necessary to mitigate immediate risk. ([source](/docs/governance-and-versioning))
- [ ] Semantic versioning, in the form Major.Minor.Patch, SHALL be used. ([source](/docs/governance-and-versioning))
- [ ] An approved combination SHALL be reviewed for restriction, suspension, or removal when framework-level validation, ecosystem-specific validation, or sustained operational monitoring shows that the combination may no longer perform within the framework threshold or risk assumptions. ([source](/docs/governance-and-versioning))
- [ ] All such actions SHALL be documented and communicated through the governance process. ([source](/docs/governance-and-versioning))

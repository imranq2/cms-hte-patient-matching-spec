---
title: "Glossary"
excerpt: "Terms used in the specification and on this site."
hidden: true
---

Definitions follow the specification's wording where it defines a term, and give the section. Where the specification does not define a term, the entry says how this site uses it.

**Category 1 rules.** The rules in Table 2 that already carry an individuating field and are evaluated in one step. See [Table 2: Category 1 Rules](/docs/table-2-category-1-rules).

**Category 2 rules.** The rules evaluated in two disjoint steps: a Household Match, then an Individual Match within that household. See [Category 2: Household and Individual Rules](/docs/category-2-household-and-individual-rules).

**Conservative floor.** The lowest plausible value assigned in the absence of precise empirical measurement, an engineering lower bound chosen so the field's true discriminating power is assumed to be at least as strong as the stated value (section VI.A).

**CSP (Credential Service Provider).** The entity that identity-proofs a person and issues an IAL2 Claims Token. The specification requires the issuer to be a trusted CSP. See [IAL2 Claims Tokens](/docs/ial2-claims-tokens).

**Damerau-Levenshtein distance.** An edit distance that counts one insertion, deletion, substitution, or adjacent transposition as 1. The specification describes fuzzy matching as tolerating a distance of 1 (section V.E). See [Fuzzy Matching](/docs/fuzzy-matching).

**Fellegi-Sunter model.** A probabilistic record linkage model in which the u-probability for a field is the probability of coincidental agreement among records that do not belong to the same person (section IV.B).

**Fuzzy matching.** Matching that tolerates a limited data-entry variation after normalization. Fields allowed to be fuzzy are marked with an asterisk in Table 2.

**Household Match, Individual Match.** The two steps of a Category 2 rule. The household step uses fields commonly shared within a household (Table 2-H); the individual step identifies one person within it (Table 2-I).

**IAL2 Claims Token.** A signed OpenID Connect ID token issued by a CSP after identity proofing to at least NIST IAL2 (section III.D).

**Legal ID.** A government-issued legal identity document identifier, such as a driver's license or passport number, matched exactly within its issuing-authority namespace.

**MBI (Medicare Beneficiary Identifier).** The CMS-issued Medicare Beneficiary Identifier. Table 2 rules that reference MBI apply only to CMS-issued MBI values (section IV.H.4).

**Member ID, Subscriber ID.** The Insurance Member ID is the individual-level identifier, including any dependent suffix. The Insurance Subscriber ID is the policyholder-level base value shared by family members on a policy. See [Insurance Identifiers](/docs/insurance-identifiers).

**Namespace-bound identifier.** An identifier compared only within the namespace of the entity that issued it, such as a payer's member ID within that payer, or an EMPI.

**ONC dataset.** The ONC 2017 Patient Matching Algorithm Challenge dataset, which the specification names as a validation dataset (section VI.A). See [Test Set Overview](/docs/test-set).

**P(collision).** The probability that two distinct individuals in the population share identical values for a given combination of fields. It measures the discriminating power of the combination itself, independent of any algorithm (Executive Summary).

**Path A, Path B.** The specification's two compliance paths: Path A, Assumed Compliance (rules-based), and Path B, Empirical Compliance (performance-based).

**Payer namespace.** The namespace established by the Payer ID, within which an insurance identifier is matched (section IV.H.2).

**Placeholder value.** A value that is a placeholder, temporary, unknown, test, or otherwise non-comparable. It is treated as unavailable for matching (section V.D).

**Responding entity, Responder.** The participant that receives a query and decides whether to return matching records. The specification does not give a formal definition.

**RFC 2119.** The convention that gives SHALL, SHALL NOT, SHOULD, and MAY their requirement meanings, which the specification applies (section I).

**Table 2.** The specification's list of approved field combinations whose conservative P(collision) is at or below 2e-12 and that satisfy additional administrative controls.

**u-probability.** For a field, the probability that two distinct individuals share the same value. See [How the Numbers Are Derived](/docs/how-the-numbers-are-derived).

**Unique candidate.** A match is satisfied only when it produces a unique candidate subject at the source system (Core Principle 4).

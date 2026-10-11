#!/usr/bin/env python3
"""Build the informational Conformance Checklist from the specification pages.

Every checklist item is a verbatim quotation from a converted specification page. The script
asserts that each quoted text still exists in its page, so a specification change that alters a
quoted requirement fails the build instead of leaving a stale quotation on the site.

Usage (from the repository root):
  python3 tools/build_conformance_checklist.py
"""
import re
import sys
from pathlib import Path

SPEC = Path("docs/Specification")
OUT = Path("docs/Implement and Test/conformance-checklist.md")

# (section heading, spec page slug, [verbatim texts]). A text starting with "  " is rendered as a sub-item.
GROUPS = [
    ("Returning a match (Executive Summary, I, II)", "summary-and-purpose", [
        "If the identity attributes in a query correspond to a field combination listed in Table 2 of this document, and the query produces a unique candidate subject, the responding entity SHALL return matching records for that patient within the permitted scope for that query context.",
    ]),
    ("Core Principles (II)", "core-principles", [
        "Matching thresholds SHALL NOT be arbitrary.",
        "the responding entity shall respond with a match appropriate to the protocol subject to the administrative controls in §IV.D and Table 4.",
        "Network queries could have unique candidates found at more than one source systems and SHALL return the match from each source system.",
        "Matching shall evaluate against all known values for a field (e.g., all known last names, all known addresses, all known phone numbers).",
        "Implementations SHALL be held to an empirically validated accuracy floor (precision, recall, and false-positive rate), in addition to the 2e-12 collision threshold in Principle 1.",
    ]),
    ("Table 2 notes (III.C)", "table-2-category-1-rules", [
        "Member ID means the full individual-level identifier inclusive of any dependent suffix; the bare subscriber base value without a dependent suffix SHALL NOT be used under Member ID rules.",
        "For all rules in this group, the Payer ID establishes the namespace and matching SHALL be performed only within that namespace.",
    ]),
    ("Category 2: household and individual rules (III.C.2 to III.C.5)", "category-2-household-and-individual-rules", [
        "A responder MAY log or flag a Last Name mismatch for data-quality review, but SHALL NOT withhold an otherwise-qualifying match because Last Name differs",
        "A responding entity SHALL return a match when a query's Household-tier fields resolve to exactly one household per Table 2-H (§3.3), its Individual-tier fields resolve to exactly one member of that household per Table 2-I (§3.4), and the product of the two listed probabilities does not exceed 2e-12.",
    ]),
    ("Multiple births (III.C.7)", "multiple-births", [
        "Whenever Household-tier matching resolves to more than one candidate sharing an identical DOB, First Name comparison SHALL be exact, not fuzzy",
        "if removal leaves no discriminating value, or the first names are genuinely identical, the query SHALL produce more than one candidate and SHALL NOT resolve to a unique match",
    ]),
    ("Applying the tables (III.C.8)", "applying-the-tables", [
        "A step that does not resolve to exactly one candidate SHALL NOT be treated as satisfied for purposes of combining probabilities in step 2 above.",
    ]),
    ("IAL2 claims tokens (III.D and III.E)", "ial2-claims-tokens", [
        "A patient-facing app SHALL include a CSP-issued IAL2 Claims Token in a query to match a patient.",
        "If an IAL2 Claims Token is included in a query, the Responder SHALL validate the token prior to responding.",
        "Validation SHALL include:",
        "  The token's digital signature using the CSP's published JWKS or other applicable key distribution mechanism",
        "  The iss claim identifies a trusted CSP. A trusted CSP must use distinct issuer URLs for production and non-production id_tokens.",
        "  The aud claim identifies the intended relying party, IAS Provider, or other expected audience for the transaction",
        "  The token is unexpired based on the exp claim, or otherwise within the Responder's maximum acceptable age based on iat; and reasonable checks of token integrity and freshness.",
        "  Anti-replay controls using the jti claim in combination with issuer context.",
        "At a minimum, the Responder SHALL record previously accepted iss + jti values, or maintain equivalent controls, for the applicable token-validity window and SHALL reject subsequent reuse of the same token identifier.",
        "If token validation fails or replay is detected, the Responder SHALL NOT rely on the token or any claim extracted from it for matching or response.",
        "When an IAL2 Claims Token is successfully validated, demographic claims extracted from the token SHALL be used as query demographics for matching.",
        "Such demographics SHALL be subject to the same normalization, placeholder suppression, historical-value handling, exact and fuzzy comparison constraints, approved Table 2 combinations, and uniqueness requirements that apply when the same demographics are transmitted directly in the query.",
        "aud | Identifies the intended audience of the token | Required - OIDC SHALL be the App’s Client ID (be it an NPD ID, Medicare App Library client id, etc).",
        "exp | Expiration time for the token | Required - OIDC SHALL NOT be > iat+300",
        "email_verified | True if the End-User's e-mail address has been verified; otherwise false | SHALL NOT be populated",
        "phone_number_verified | True if the End-User's phone number has been verified; otherwise false | SHALL NOT be populated",
    ]),
    ("Probability model (IV)", "joint-collision-probability", [
        "Until such a method is adopted through governance, combinations whose approval depends on a geographic dependency discount SHALL NOT be added to Table 2.",
    ]),
    ("SSN and ITIN (IV.E)", "ssn-and-itin", [
        "Full SSN and full ITIN SHALL NOT be transmitted as part of matching queries.",
    ]),
    ("Ecosystem-specific validation (IV.F)", "ecosystem-specific-collision-validation", [
        "While published population-scale collision probabilities shall be used for initial Table 2 classification, responding entities are encouraged to validate collision probabilities against their own patient populations and report major deviations and observations to CMS.",
    ]),
    ("Insurance identifiers (IV.H)", "insurance-identifiers", [
        "Implementations SHALL NOT substitute the bare subscriber base value for an individual member ID when applying Member ID combinations from Table 2.",
        "If the implementation cannot confirm that a submitted identifier includes the individual-level suffix, it SHALL treat the identifier as a Subscriber ID and apply the corresponding, more conservative, u-probability.",
        "Matching SHALL be performed only within the payer namespace established by the co-submitted Payer ID.",
        "A query that provides an insurance identifier without a Payer ID SHALL NOT be evaluated under any insurance identifier combination in Table 2.",
        "Implementations SHALL enforce the namespace binding at the Coverage.identifier.system or equivalent level.",
        "An insurance identifier SHALL NOT be combined solely with other insurance-derived or plan-administrative fields (such as group number, plan type, or enrollment date) in a Table 2 combination",
    ]),
    ("Required normalization, names, and demographic fields (V.A to V.C)", "required-normalization-names-and-demographics", [
        "All string matching SHALL be case insensitive",
        "All whitespace SHALL be removed or ignored during matching except as required in normalized address fields",
        "All punctuation (e.g. hyphens, periods, apostrophes, etc) SHALL be removed or ignored during matching except as required in normalized address fields",
        "All string fields shall implement Diacritic folding as part of the matching process",
        "Date of birth SHALL be represented in YYYY-MM-DD format when the full date is known.",
        "If only year or year-month is known, the value SHALL be transmitted as partial and SHALL NOT be imputed, padded, or converted to a full date for matching.",
        "Each implementation SHALL maintain a versioned reference table of nickname values first name field used in matching.",
        "All name fields including First, Middle, Last, Prefix, Suffix, Title and any others SHALL be separated into discrete components used for matching",
        "Matching algorithms SHALL match against ALL known names (maiden, previous, AKA)",
        "For the avoidance of doubt, matching SHALL ignore or remove all punctuation and whitespace in name fields",
        "If a generational suffix can be identified on both the query and the response and they do not match then the responder SHALL NOT return the match.",
        "For the avoidance of doubt, this rule SHALL negate a match that was made by matching a combination in table 2.",
        "Suffix expansion tables SHALL be maintained and integrated to support abbreviations and shorthand.",
        "All addresses SHALL be normalized to Project US@ standard formats by the Requestor and Responder",
        "Address SHALL match regardless of designated type (home, legal, office, physical, postal, etc)",
        "All phone numbers SHALL be normalized to E.164 specifications for matching purposes",
        "Phone numbers SHALL match regardless of designated type (home, cell, work, etc)",
        "Responders SHALL match against ALL known values, current or historical.",
        "Demographic matching SHALL be performed in a case insensitive manner",
    ]),
    ("Placeholder values (V.D)", "placeholder-values", [
        "Each implementation SHALL maintain versioned reference tables of non-comparable values (e.g. placeholder values) and patterns for each demographic field used in matching.",
        "When a field value is identified as placeholder, temporary, unknown, test, or otherwise non-comparable, that field SHALL be treated as unavailable for use in matching.",
        "It SHALL NOT count as an exact match, fuzzy match, nickname match, phonetic match, or conflict.",
        "Placeholder-name categories SHALL include, at minimum, newborn temporary names, unidentified-patient names, unknown-value placeholders, and local test or training values.",
        "Placeholder suppression SHALL apply to both requestor-side query preparation and responder-side record evaluation.",
        "Unknown dates of birth, including all dates of birth prior to the current year – 120 years or after the current date + 2 days SHALL be treated as unavailable for use in matching.",
        "Requesters and responders SHALL maintain a reference list of known placeholder values per field and SHALL exclude any field value on that list from matching entirely",
    ]),
    ("Fuzzy matching (V.E)", "fuzzy-matching", [
        "Fuzzy matching SHALL NOT be applied to query strings that are less than 5 characters long.",
    ]),
    ("Validation (VI)", "validation-requirements", [
        "Before initial production use, and after any material change to matching logic, normalization rules, placeholder handling, fuzzy-comparison settings, or decision thresholds, an implementation SHALL demonstrate documented performance on the ONC patient matching test dataset.",
        "The accuracy floor SHALL be established through a follow-on effort before the framework's effective date, with interim reporting-only in the meantime.",
        "At a minimum, validation results SHALL report observed precision, recall, and false-positive rate at the configured operating point.",
        "Validation SHALL confirm that the implementation correctly handles matches, non-matches, placeholder values, normalization requirements, uniqueness checks, approved fuzzy comparisons, and other material edge cases.",
        "Local acceptance testing need not replicate population-scale benchmarking, but it SHALL confirm that required fields, comparison rules, and response behavior operate as configured in production.",
        "As the ONC dataset is revised, or as an approved successor dataset becomes available, implementations SHALL validate against the current approved version within the implementation period established through governance.",
        "The P(collision) values used to approve combinations in Table 2 are conservative estimates intended for threshold design and rule classification. Those values SHALL be empirically validated at the framework level within 12 months of proposal adoption",
        "the validation record SHALL report the observed collision rate for the combination's field set, the 95 percent confidence interval, and a description of the validation population",
    ]),
    ("Audit and monitoring (VII)", "audit-and-monitoring", [
        "Each participant SHALL maintain audit and monitoring practices sufficient to explain match decisions, investigate incidents, and identify performance degradation over time.",
        "For each query evaluated under Table 2, the participant SHALL retain information sufficient to reconstruct the decision",
        "Audit records SHALL be protected in accordance with applicable privacy and security requirements.",
        "Participants SHALL have an established process to monitor ambiguous match rates, suspected wrong-patient incidents, fuzzy-constraint violations, and material changes in non-return, manual-review, or exception rates.",
        "If monitoring indicates that an approved combination may be degrading, that a rule is being applied incorrectly, or that false-positive behavior may be emerging, the participant SHALL document the issue, take proportionate interim mitigation steps, and escalate the matter through the governance process",
    ]),
    ("Governance and versioning (VIII), which apply to maintainers of the framework", "governance-and-versioning", [
        "This framework SHALL be maintained through a documented governance process that supports transparency, reproducibility, public review, and orderly implementation.",
        "A proposed change SHALL include a description of the change, the rationale for the change, the anticipated implementation impact, and, where applicable, a validation plan or supporting evidence.",
        "Changes that materially affect Table 2, the framework threshold, approved fields, normalization rules, fuzzy constraints, or required testing SHALL be published for public comment for not less than calendar 30 days, unless an emergency update is needed to address a material patient-safety, privacy, security, or compliance risk.",
        "After review of comments and supporting evidence, adopted changes SHALL be published with a version increment and an effective date.",
        "Substantive changes SHALL include a transition period of not less than 90 days unless a shorter period is necessary to mitigate immediate risk.",
        "Semantic versioning, in the form Major.Minor.Patch, SHALL be used.",
        "An approved combination SHALL be reviewed for restriction, suspension, or removal when framework-level validation, ecosystem-specific validation, or sustained operational monitoring shows that the combination may no longer perform within the framework threshold or risk assumptions.",
        "All such actions SHALL be documented and communicated through the governance process.",
    ]),
]

PAGE_FILES = {}
for p in SPEC.rglob("*.md"):
    if p.name != "index.md":
        PAGE_FILES[p.stem] = p


def norm(s: str) -> str:
    s = s.replace("&gt;", ">").replace("&lt;", "<").replace("<br />", " ")
    s = re.sub(r"\\(.)", r"\1", s)
    s = s.replace("**", "").replace("*", "")
    return re.sub(r"\s+", " ", s).strip()


def main() -> int:
    lines = [
        "---",
        'title: "Conformance Checklist"',
        'excerpt: "The specification\'s SHALL requirements, quoted and linked. Informational, not normative."',
        "hidden: true",
        "---",
        "",
        '<Callout icon="📘" theme="info">',
        "  **This checklist is informational and non-normative.** The specification text governs. Each item below is a verbatim quotation from the specification v3.4.0, with a link to the page where it appears. If a quotation here ever differs from the specification, the specification is correct.",
        "</Callout>",
        "",
        "## What it covers and what it leaves out",
        "",
        "- It lists statements that use SHALL or SHALL NOT, plus the three lowercase \"shall\" statements in the specification. Where a quotation is shortened to the part that states the requirement, it begins or ends with an ellipsis (…).",
        "- It does **not** list statements phrased as \"must\" or \"required\", which the specification also uses in places. Read the linked pages for those, including the rules in Table 2 itself.",
        "- It does not replace the Table 2 rules, the household-then-individual process, or the validation and audit sections. Use the [Implementation Guide](/docs/implementation-guide) for how they fit together.",
        "- The specification says its SHALL language describes requirements that would apply once the framework is adopted, and creates no present obligation during a comment period (Purpose).",
        "",
        "Use the boxes to track your own progress. They are not saved.",
    ]
    total = 0
    for heading, slug, texts in GROUPS:
        page = PAGE_FILES[slug]
        raw = page.read_text(encoding="utf-8")
        # One unit per paragraph or list item; table rows are separate units.
        units = []
        for blk in re.split(r"\n\s*\n", raw):
            if blk.lstrip().startswith("|"):
                units += blk.split("\n")
            else:
                units.append(blk)
        page_lines = [norm(re.sub(r"^\s*([-*]|\d+\\?\.)\s+", "", u)).strip("| ").strip() for u in units]
        lines += ["", f"## {heading}", ""]
        for t in texts:
            sub = t.startswith("  ")
            body = t.strip()
            q = norm(body)
            hit = next(((l, l.index(q)) for l in page_lines if q in l), None)
            if hit is None:
                sys.exit(f"quotation not found in {page}: {body[:100]}")
            line, pos = hit
            rest = line[pos + len(q):].strip()
            starts_mid = pos > 0 and line[max(0, pos - 2):pos] not in (". ", "? ", "! ", ": ")
            ends_mid = bool(rest) and (not q.endswith((".", ":", "?")) or rest[0].islower() or rest.startswith("—"))
            display = body.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")
            if starts_mid:
                display = "… " + display
            if ends_mid:
                display = display.rstrip(".") + " …" if False else display + " …"
            marker = "  - [ ]" if sub else "- [ ]"
            suffix = f" ([source](/docs/{slug}))" if not sub else ""
            lines.append(f"{marker} {display}{suffix}")
            total += 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT} with {total} items")
    return 0


if __name__ == "__main__":
    sys.exit(main())

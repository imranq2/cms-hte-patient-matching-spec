# Design: Populating the Patient Matching Docs Site

Status: Draft for review
Author: Imran Qureshi
Date: 2026-10-10

## Goal

Publish the CMS HealthTech Ecosystem Patient Matching Specification (v3.4.0) on this ReadMe site so implementers, validators, and reviewers can find what they need without reading an 85K-character document end to end. Give them direct access to the [test set](https://github.com/icanbwell/cms-hte-patient-matching-test-set) and the [reference implementations](https://github.com/icanbwell/cms-hte-patient-matching).

## Inputs

**Spec source:** [Google Doc](https://docs.google.com/document/d/1NytpfZ05aokS-gD7uDIQE7gEyms9zMgoiaIah_w4VTE/edit), "CMS Patient Matching Specification", v3.4.0, Final Consolidated Draft, released 9/10/2026, in a public comment period. One tab, ~85K characters, 11 tables.

| Spec section (H1) | ~Size | Notes |
|---|---|---|
| Executive Summary, Purpose, Core Principles | 7.6K | Normative language is RFC 2119 (SHALL/SHOULD) |
| Risk Framework | 29.5K | Contains Table 2 (Category 1), 2-H, 2-I, Category 2 combined, Table 4 admin restrictions, twins, IAL2 token fields |
| Model & Assumptions | 26K | Per-field u-probabilities, joint P(collision), SSN/ITIN, insurance identifiers, reference script |
| Normalization Requirements | 7K | Name handling, placeholders table, fuzzy matching |
| Validation Requirements | 4K | References the ONC test dataset |
| Audit & Monitoring, Governance & Versioning, IX Implementation and Testing, References, Document Control | 10K | Document Control holds comment-period info |

**Test set** (`cms-hte-patient-matching-test-set`, public, Apache-2.0): algorithm-agnostic labeled cases derived from the ONC 2017 challenge dataset. Two tiers: per-provision pairs and population queries. Entry point is `evaluation/cases/README.md` (formats, scoring examples, generation methodology).

**Reference implementation** (`cms-hte-patient-matching`, public, Python library): implements the Table 2 rules over FHIR R4 Patient resources. Related repos it names: `cms-hte-patient-matching-service` (HTTP wrapper) and `cms-hte-ial2-reader` (IAL2 token → FHIR Patient).

## Problems with the source to solve

1. **Single long document, mixed audiences.** Normative rules, statistical derivation, and governance are interleaved.
2. **Inconsistent section lettering.** Headings run B.1, "Matching Criteria" (no letter), C.2–C.9, E, G, H.1–H.5, I; there is no A, D, or F heading. Cross-references such as "§IV.D" don't map to visible headings.
3. **Still in comment period.** Content will change after publication.
4. **Possible rule-count mismatch.** The spec's Executive Summary says 30 Category 1 and 8 Category 2 rules. The reference implementation README says 29 Category 1 and 10 Category 2 (39 total, though its diagram says 38). To be confirmed with the spec authors before we publish rule counts anywhere on the site.

## Information architecture

Organize by what the reader is trying to do, not by the document's original order. Spec content is split into pages of roughly 1–5K characters, one topic each, with stable slugs.

```
Getting Started
  Welcome to Patient Matching          landing page, audience paths, status banner (draft / comment period)
  Quick Start                          3 paths: implement / validate / review (links only)
  Glossary                             P(collision), u-probability, Category 1/2, household tier, IAL2, ...

Specification  (v3.4.0)
  Overview                             Executive Summary + Purpose + conformance language (SHALL/SHOULD)
  Core Principles
  Risk Framework
    Harm of Non-Return
    Collision Risk vs. Non-Return Risk
    Risk of False Positives
  Matching Rules
    Table 2: Category 1 Rules
    Category 2: Household and Individual Rules      Table 2-H, Table 2-I, combined probabilities, decision rule
    Administrative Restrictions                     Table 4
    Multiple Births
    Applying the Tables                             how to apply + defensive use
  IAL2 Claims Tokens
  Probability Model
    Assumptions and Intended Use
    Per-Field Collision Probabilities
    Joint Collision Probability
    SSN and ITIN
    Insurance Identifiers                           H.1–H.5
    Twins and Fragile Identities
    Reference Script
  Normalization
    Required Normalization, Names, Demographic Fields
    Placeholder Values
    Fuzzy Matching
  Validation and Testing                            links into Test Set section
  Audit and Monitoring
  Governance and Versioning
  References
  Document Control and Comments                     comment instructions, focus areas

Changelog
  Overview                             how versions are numbered (Major.Minor.Patch per Governance), how to read an entry
  v3.4.0                               one page per released spec version, newest first
  v3.3.0, ...                          backfilled from prior versions if available

Proposals
  Overview                             how proposals work (links to Governance and Versioning), lifecycle and statuses
  Under Review                         index table: ID, title, summary, affected spec sections, comment deadline, link
  Accepted                             index table: ID, title, summary, spec version it shipped in, effective date, link
  Proposals/<ID>-<slug>                one page per proposal (see below)

Community
  Contributors                         people and organizations that have contributed to the spec and tooling
  Report an Issue                      where to send what: spec feedback, test-set bugs, library bugs, site errors
  Contribute                           how to contribute: spec proposals, test data, code, docs

Try It
  Patient Matching Service UI          what the hosted UI does, who can use it, link to patient-matching-service.bwell.com
  Walkthrough                          run a sample query end to end, how results map to Table 2 rule IDs

Test Set
  Overview                             what it is, what it isn't, ONC provenance and attribution
  Running the Test Set                 tiers, file formats, scoring example (summary, links to repo README)
  Methodology                          how cases were generated (summary, link)

Reference Implementations
  Overview                             what exists, which to use when
  Patient Matching Library             cms-hte-patient-matching: install, quick start, rule coverage
  Service and IAL2 Reader              short pointers to the other two repos
  Spec-to-Code Map                     table: spec rule ID → implementation location
```

Approximate page count: 40 for the spec, test set, and implementations, plus one page per released version and per proposal.

### Changelog and Proposals

**Requirements:** show a changelog each time a new spec version is created, and list proposals currently under review and proposals previously accepted.

**Lifecycle, grounded in the spec's Governance and Versioning section:** a proposal states the change, rationale, anticipated implementation impact, and a validation plan or evidence where applicable. Changes affecting Table 2, the threshold, approved fields, normalization, fuzzy constraints, or required testing get at least 30 days of public comment. Adopted changes ship with a version increment, an effective date, and (for substantive changes) a transition period of at least 90 days. Statuses on the site: **Under Review** → **Accepted** (shipped in vX.Y.Z). The Governance text does not define a rejected or withdrawn outcome; see Open questions.

**Changelog entries** (`docs/Changelog/v3-4-0.md` etc.), one page per version, newest first, each with:
- Version, release date, effective date, semver class (Major / Minor / Patch) and a one-line reason
- Change list grouped as Added / Changed / Removed, each item linking to the affected spec page and rule ID anchor (e.g. Table 2 rows added or removed)
- Links to the Accepted proposals that produced the change
- Transition period end date for substantive changes

**Proposal pages** (`docs/Proposals/<ID>-<slug>.md`) use a fixed template: status, submitted date, comment deadline, affected spec sections (links), description, rationale, implementation impact, validation plan/evidence, outcome (version shipped, effective date) once accepted. Frontmatter carries `status`, `comment_deadline`, `shipped_in` so the index tables can be built or checked from it.

**Index pages** (Under Review / Accepted) are hand-maintained Markdown tables at first. A small script that regenerates them from proposal frontmatter is optional and only worth adding once there are more than ~10 proposals. Moving a proposal Under Review → Accepted is a PR that edits its page and moves its table row.

**Link between the two:** a proposal's `shipped_in` points to a changelog entry, and the changelog entry lists its proposals, so a reader can go in either direction.

**Spec status banner:** the landing page and Spec Overview show the current released version and link to Under Review proposals, since the spec is in a comment period.

### Navigation aids

- **Landing page with audience paths.** Implementer (Matching Rules → Normalization → Reference Implementations), Validator (Validation and Testing → Test Set), Reviewer/Commenter (Overview → Document Control and Comments).
- **Rule IDs as anchors.** Each Table 2 / 2-H / 2-I row gets a stable anchor by rule ID so other pages, the code map, and external references can deep-link to a single rule.
- **Real Markdown tables**, not images, so ReadMe search indexes cell contents.
- **Cross-links at the point of need.** Matching Rules → the probability rows backing a rule; Validation → the test set; Normalization → the library functions.
- **Replace the spec's lettering with descriptive page titles** and keep the original section label in each page's frontmatter excerpt or a first-line "Spec section: C.7" note, so people citing the PDF/Doc can still find the page.
- **Prev/next and "Related pages" footer** on spec pages to preserve linear reading for people who want it.

## Community: contributors, issues, contributing

Three pages under a **Community** nav entry, linked from the landing page and the site footer-level "Related" links on spec pages.

**Report an Issue.** One page that routes by what the reader found, so reports land in the right place:

| What | Where it goes |
|---|---|
| Spec content: unclear, incorrect, or a change request | The spec's public comment process (Document Control and Comments page) during a comment period; afterwards, submit a proposal (see Contribute) |
| Test set: wrong label, bad case, format problem | GitHub Issues on `cms-hte-patient-matching-test-set` |
| Reference library: bug or rule-coverage gap | GitHub Issues on `cms-hte-patient-matching` |
| Hosted UI | Contact route TBD (see Open questions) |
| This site: typo, broken link, stale content | GitHub Issues on this docs repo, or a "Suggest edits" link, depending on whether the repo is made public |

The page lists what to include in a report (spec version or library/test-set version, rule ID, minimal example using synthetic data only, expected vs. actual) and carries a prominent "never include real patient data" warning. Per-repo issue templates are optional follow-up work in those repos, not part of this plan.

**Contribute.** One page with a section per contribution type, each linking to the authoritative instructions rather than restating them:

- **Spec changes:** submit a proposal containing the elements the Governance section requires (description, rationale, implementation impact, validation plan or evidence). Describes the path Under Review → Accepted, the 30-day comment period, and the 90-day transition for substantive changes. Links to the Proposals pages and the proposal template.
- **Test data:** link to the test set's `CONTRIBUTING.md`. Summarize its key rules in a few lines (only synthetic records derived from a disclosed method, or cited aggregate statistics; no raw real records; fabricated values marked as synthetic).
- **Code (library, test set):** link to each repo's `CONTRIBUTING.md` (dev setup, tests, pre-commit) and their license (Apache-2.0).
- **Docs (this site):** how to edit and submit a change. Local edit, `npx @readme/cli lint`, PR into `v1.0`, with the note that merged changes publish. The ReadMe web editor path, if contributors are allowed to use it.
- **Licensing:** contributions are accepted under the target repo's license; state that on the page.

**Contributors.** A page listing contributors, grouped as Spec authors and workgroup, Test set and library contributors, and Organizations. Built from a curated list, not a raw `git log` dump, because:
- the repos' contributor lists include bots (`claude[bot]`, `bwell-dev`) and GitHub handles rather than names;
- listing a person by name publicly should be their choice.

Each entry: name or handle, organization, role, optional link. Source is a `contributors` data block in the page, edited by PR. Seed it from the spec's workgroup/author information and the GitHub contributor lists, then confirm names with each person before publishing.

## Hosted testing UI

b.well also runs a service with a UI for testing patient matching: https://patient-matching-service.bwell.com. The site gets a **Try It** section for it.

- **Placement:** a top-level nav entry and a card on the landing page ("Try matching in your browser"), plus links from Matching Rules (try a rule combination), Reference Implementations (the hosted service wraps the library), and the Test Set (run cases through the UI).
- **Content:** a page describing what the UI does and its limits, and a walkthrough with a sample query and how the result maps to a Table 2 rule ID. The walkthrough needs screenshots, which go in the repo and must use synthetic data only.
- **Scope boundary:** the site links to the UI; it does not document an HTTP API unless the service exposes one for ecosystem participants (see Open questions on the API Reference).
- **Not verified:** I could not reach the URL from this environment (no response), so access requirements and behavior are unconfirmed.

## Test set and reference implementation access

Site pages summarize and link; they do not copy repo content.

- **Why link rather than mirror:** the test set README and library README change with the code (the test set repo is actively iterating, with sessions logs and pending work). Copied content would drift.
- **What the site adds:** orientation (what/why/when), the spec-to-test mapping, and a stable entry URL. Each page opens with a "Source of truth: `<repo path>`" link.
- **Cross-links from the spec:** the Validation Requirements page links to the test set; the Matching Rules and Normalization pages link to the library's rule/normalizer modules.
- **Spec-to-Code Map** is the one page that is new content. It is built from the library's rule definitions and must be regenerated or re-verified when the library changes (see Maintenance).

## Conversion approach

1. **Extract mechanically, not by copy-paste.** Pull the Doc as JSON via the Google Docs API (already retrievable in this environment) and convert to Markdown with a script, so table cells and numeric values (P(collision) etc.) are not retyped. Script lives in the scratch area or a `tools/` directory and is not published.
2. **Split by heading** into the pages above, applying the slug and `_order.yaml` plan.
3. **Hand-edit for MDX/ReadMe:** frontmatter, `<Callout>` for normative notes and draft status, `<Cards>` for audience paths, link rewriting.
4. **Verify against source:**
   - Diff the extracted plain text of the site pages against the Doc's plain text; every sentence in the Doc appears exactly once.
   - Row/column counts of all 11 tables match (31×4, 31×3, 22×4, 15×3, 11×3, 8×3, 7×4, 6×2, 5×3, 4×4, 3×4).
   - Every numeric cell in Table 2 / 2-H / 2-I / Model tables is compared programmatically.
   - Check the Doc for inline images/drawings (none seen in the text extract; confirm) and for the embedded Gist link in the Executive Summary.
5. `npx @readme/cli lint` plus a link check on the final tree.

## Delivery plan

Because `v1.0` publishes on push, work goes through PRs into `v1.0`. Each PR is independent (base `v1.0`; no stacking) and states what it covers and defers.

| PR | Scope | Defers |
|---|---|---|
| 1. Skeleton | `_order.yaml` files, empty-but-titled pages hidden (`hidden: true`), landing page, glossary stub, remove template callouts | All spec content |
| 2. Spec: framing | Overview, Core Principles, Risk Framework | Rules, model |
| 3. Spec: Matching Rules | Table 2, 2-H, 2-I, Category 2, Table 4, twins, how-to-apply, IAL2 tokens | Probability model |
| 4. Spec: Probability Model | Model & Assumptions pages incl. insurance identifiers, reference script | Normalization onward |
| 5. Spec: Normalization, Validation, Audit, Governance, References, Document Control | Remainder of the spec | Test set / implementations |
| 6. Test Set section | 3 pages | Spec-to-code map |
| 7a. Community | Contributors, Report an Issue, Contribute | Contributor list contents beyond what is confirmed |
| 7. Reference Implementations and Try It | 4 implementation pages including Spec-to-Code Map, 2 Try It pages for the hosted UI | — |
| 8. Changelog and Proposals | Overview pages, proposal template, changelog entry for v3.4.0, any existing proposals (Under Review / Accepted) | Backfill of versions before v3.4.0 unless source material exists |
| 9. Unhide + landing page finalization | Flip `hidden`, fill Quick Start and cross-links | — |

Pages stay `hidden: true` until PR 9 so partial content is never public.

## Maintenance

- **Spec changes during comment period.** Record the Doc `revisionId` used for each conversion in the PR description. Re-run the extract and diff script to produce a change list instead of re-reading the Doc.
- **Source of truth.** Until the spec is finalized, the Google Doc is canonical and the site follows it. Decision needed on whether the repo becomes canonical afterward (see Open questions).
- **Spec-to-Code Map** is re-verified whenever the library's rule set changes; add a note on the page naming the library version it was built against.

## Open questions

1. **Source of truth after finalization:** does the Markdown in this repo replace the Google Doc, or does the Doc stay canonical and the site stay derived? Recommendation: the repo becomes canonical once the comment period closes.
2. **Rule-count mismatch** (30+8 in the spec vs 29+10 in the library README): which is correct, and is it a spec edit, a library edit, or a version skew?
3. **ReadMe versioning:** should spec v3.4.0 be pinned to ReadMe version `v1.0`, or will future spec versions get their own ReadMe versions/branches? This affects slug design (e.g. whether the spec version appears in URLs).
4. **Other branches:** does ReadMe sync non-`v1.0` branches to preview versions? If not, PR review is by Markdown only and there is no rendered preview before publish. Check the sync configuration in the ReadMe dashboard.
5. **API Reference:** `reference/` has only the config stubs. If `cms-hte-patient-matching-service` exposes an API intended for ecosystem participants, should its OpenAPI spec be published here? Out of scope for this plan.
6. **Comment submission:** the Doc's "Submit Comments To" section looks empty in the extract. Needs content before the Document Control page is published.
7. **Spec-to-Code Map ownership:** who maintains it as the library evolves?
8. **Proposal source and statuses:** where do proposals originate today (Google Docs, GitHub issues, email)? Do we need Rejected / Withdrawn / Superseded statuses, or only Under Review and Accepted?
9. **Existing proposals and history:** is there a current list of proposals under review and accepted proposals to import, and do prior spec versions (before v3.4.0, e.g. v3.3.0 mentioned in the spec) have change notes to backfill?
10. **Changelog granularity:** per-version pages (proposed) vs. a single running page. Per-version pages scale better and give each release a stable URL.
11. **Hosted UI access and audience:** is `patient-matching-service.bwell.com` public, login-gated, or internal? Which spec version and library version does it run? If it is not open to site readers, the Try It pages need an access-request path instead of a plain link.
12. **Hosted UI data handling:** does it accept real patient data? If it can, the page needs an explicit "use synthetic data only" warning, and the walkthrough and screenshots must use test-set records.
13. **Delivery slot for Try It:** proposed as part of PR 7 (Reference Implementations) since the service wraps the library; say if it should ship separately.
14. **Who are the contributors, and do they consent to being listed?** Who are the spec authors and workgroup members and organizations to credit, and in what form (name, handle, organization)?
15. **Where do issue reports go for the spec and the hosted UI?** The docs repo `icanbwell/cms-hte-patient-matching-spec` is private, so readers cannot file issues there. Options: make it public, point the site at a public repo or intake form, or use an email/form alias. Which one?
16. **Who triages reports and who approves proposals?** The Report an Issue and Contribute pages need a named owner or alias and an expected response, or readers get no answer.
17. **Can external contributors edit the docs?** Today only people with access to this private repo can open PRs. If not, the Contribute page's docs section becomes "suggest an edit" via the issue route.

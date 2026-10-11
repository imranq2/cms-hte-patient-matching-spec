# Design: Populating the Patient Matching Docs Site

Status: Draft for review
Author: Imran Qureshi
Date: 2026-10-10

## Goal

Publish the CMS HealthTech Ecosystem Patient Matching Specification (v3.4.0) on this ReadMe site so each audience can find what they need without reading an 85K-character document end to end:

- **Business readers:** what the spec requires, why, who it applies to, and when.
- **Engineers:** how to implement and show conformance.
- **Data scientists:** how the collision probabilities were calculated, from what data, and how to reproduce them.
- **Reviewers and commenters:** the current draft, proposals under review, and how to respond.

Give them direct access to the [test set](https://github.com/icanbwell/cms-hte-patient-matching-test-set), the [reference implementations](https://github.com/icanbwell/cms-hte-patient-matching), and the [probability calculations](https://github.com/icanbwell/cms-hte-patient-matching/tree/main/calculations). The site, the reference implementations, the calculations, and the test set are all open source.

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

**Probability calculations** (`cms-hte-patient-matching/calculations/`, public): a standalone Python project that downloads public Census, ACS, and CMS aggregate data and computes empirical u-probabilities (the chance two distinct people agree on a field) per field. It does not import from the library and uses no patient data. Per its README it is a sanity check on the model's hand-picked conservative u-values. It computes `u_simple = Σ(n_v/N)²` and the headline `u_unbiased = Σ n_v(n_v−1)/(N(N−1))`, for last/first name (exact and fuzzy), middle name (proxy), year of birth, date of birth, ZIP, state, city, street line, phone, SSN/ITIN last 4, and MBI. `data/raw/` is committed with SHA-256 checksums, so `make calculate` runs offline. Docs to link: `docs/conservative_u_comparison.md` (results), `outputs/u_probabilities.md` (auto-generated methodology and sources), `docs/PROCESS.md` (how it was built).

## Problems with the source to solve

1. **Single long document, mixed audiences.** Normative rules, statistical derivation, and governance are interleaved.
2. **Inconsistent section lettering.** Headings run B.1, "Matching Criteria" (no letter), C.2–C.9, E, G, H.1–H.5, I; there is no A, D, or F heading. Cross-references such as "§IV.D" don't map to visible headings.
3. **Still in comment period.** Content will change after publication.
4. **Possible rule-count mismatch.** The spec's Executive Summary says 30 Category 1 and 8 Category 2 rules. The reference implementation README says 29 Category 1 and 10 Category 2 (39 total, though its diagram says 38). To be confirmed with the spec authors before we publish rule counts anywhere on the site.
5. **Docs repo is private; the project is open source.** `icanbwell/cms-hte-patient-matching-spec` is private and has no LICENSE file, so readers cannot file issues or send PRs against the site, and the site content has no stated license. The spec's own license is also unstated.
6. **Stale reference script.** The spec's "Reference Script to calculate P(collision)" section points to a personal Gist. The repo's `calculations/` project supersedes it. Fixing the spec link is for the spec authors; the site links to the repo.
7. **Spec values vs. computed values.** The calculations README calls its output a check on "hand-picked conservative u-values". Not confirmed: whether the spec's published values (Per-Field Collision Probabilities, Table 2) come from this tool or are independently chosen. The Methodology pages must not claim otherwise until confirmed.

## Information architecture

Organize by what the reader is trying to do. The Specification section stays one-to-one with the Google Doc (normative text only, so people citing the Doc can find each page); audience-specific material sits in the sections around it and links back in. Six top-level sections:

```
Start Here
  Welcome to Patient Matching          landing page: four audience cards, status banner (draft / comment period)
  For Decision Makers                  what the spec requires of an organization, in plain language (see Audience layer)
  Adoption Timeline                    effective date, transition period, phased adoption and safe harbor
  FAQ
  Glossary                             P(collision), u-probability, Category 1/2, household tier, IAL2, ...
  Status                               current version, comment period, known issues

Specification  (v3.4.0)
  Summary and Purpose                  Executive Summary + Purpose + conformance language (SHALL/SHOULD)
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
  Probability Model                    the spec's own text, faithful; links to Methodology for derivation
    Assumptions and Intended Use
    Per-Field Collision Probabilities
    Joint Collision Probability
    SSN and ITIN
    Insurance Identifiers                           H.1–H.5
    Twins and Fragile Identities
    Reference Script                                short page: points to Methodology → Calculations
  Normalization
    Required Normalization, Names, Demographic Fields
    Placeholder Values
    Fuzzy Matching
  Validation Requirements
  Audit and Monitoring
  Governance and Versioning
  References
  Document Control and Comments        comment instructions, focus areas

Methodology  (data scientists)
  How the Numbers Are Derived          overview: from field frequencies to u to P(collision) to Table 2 threshold
  u-Probability Calculations           formulas (u_simple, u_unbiased), per-field approach, what each field uses
  Data Sources                         Census names, ACS ZCTA, CMS enrollment, population estimates; dates, checksums, attribution
  Empirical vs. Conservative Values    per-field comparison, margin, caveats
  Known Limitations                    middle-name proxy, SSN post-2011 cohort only, phone/street co-resident floors, city needs HUD token
  Reproducing the Calculations         setup, make targets, offline run, refreshing raw files
  Test Set Methodology                 how test cases were generated (summary, link)

Implement and Test  (engineers)
  Implementation Guide                 decision flow: normalize → query → Table 2 → uniqueness → Table 4 → respond; worked examples
  Conformance Checklist                what "compliant" means and how to demonstrate it
  Table 2 Downloads                    CSV/JSON of Table 2, 2-H, 2-I, Table 4, generated from the spec conversion
  Reference Implementations
    Overview                           what exists, which to use when
    Patient Matching Library           cms-hte-patient-matching: install, quick start, rule coverage
    Service and IAL2 Reader            short pointers to the other two repos
    Spec-to-Code Map                   table: spec rule ID → implementation location
  Test Set
    Overview                           what it is, what it isn't, ONC provenance and attribution
    Running the Test Set               tiers, file formats, scoring example (summary, links to repo README)
  Try It
    Patient Matching Service UI        what the hosted UI does, who can use it, link to patient-matching-service.bwell.com
    Walkthrough                        run a sample query end to end, how results map to Table 2 rule IDs
  Compatibility Matrix                 spec version ↔ library ↔ test set ↔ hosted service versions

Changes
  Changelog
    Overview                           how versions are numbered (Major.Minor.Patch per Governance), how to read an entry
    v3.4.0                             one page per released spec version, newest first
    v3.3.0, ...                        backfilled from prior versions if available
  Proposals
    Overview                           how proposals work (links to Governance and Versioning), lifecycle and statuses
    Under Review                       index table: ID, title, summary, affected spec sections, comment deadline, link
    Accepted                           index table: ID, title, summary, spec version it shipped in, effective date, link
    <ID>-<slug>                        one page per proposal (see below)

Community
  Contributors                         people and organizations that have contributed to the spec and tooling
  Report an Issue                      where to send what: spec feedback, test-set bugs, library bugs, site errors
  Contribute                           how to contribute: spec proposals, test data, code, docs
  License and Open Source              licenses per repo and for the site and spec text
  How to Cite                          citing a specific spec version
```

Approximate page count: 65 for the fixed pages, plus one page per released version and per proposal. Nesting is at most two levels below a top-level section.

### Audience layer

New content (not in the Google Doc) that sits above the faithful spec pages. Each page is short and links into the spec for detail rather than restating it.

- **For Decision Makers:** what the spec requires (return matching records when a query matches a Table 2 combination and yields a unique candidate; failing to is non-compliant), who it applies to, why (the cost of mismatches and non-return), and what an organization needs to do. Wording must be reviewed by the spec authors.
- **Adoption Timeline:** effective date (currently TBD in the Doc), the 90-day transition for substantive changes, and the phased adoption and safe harbor the spec describes.
- **Implementation Guide:** a decision-flow diagram and step list, plus worked examples for a Category 1 match, a Category 2 household/individual two-step, and a twin case. Examples use test-set records.
- **Conformance Checklist:** the SHALL requirements gathered in one checklist with links to the pages that define them, and the validation evidence the spec requires (observed precision, recall, and false-positive rate on the ONC dataset or a successor).
- **FAQ:** seeded from comment-period questions as they arrive.
- **Status:** current version, comment-period dates, known issues (such as the rule-count mismatch) until resolved.

### Methodology and Data

The calculations are a separate project, not a reference implementation, so they get their own section rather than a place under Reference Implementations. Pages summarize and link to `calculations/` (see "Test set, reference implementation, and calculations access"). Content rules:

- Report what the README and generated `outputs/u_probabilities.md` say, with the data download dates and checksum note, not a paraphrase that could drift.
- State plainly which fields are point estimates and which are floors or proxies.
- Do not state that spec values were computed by this tool until open question 18 is answered.
- Data Sources carries attribution for each public source and the redistribution caveat from the test-set README for the ONC dataset.

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

- **Landing page with four audience cards:** Decision Maker (For Decision Makers → Adoption Timeline), Engineer (Implementation Guide → Matching Rules → Reference Implementations), Data Scientist (Methodology → Probability Model), Reviewer/Commenter (Summary → Proposals → Document Control and Comments). Each audience also gets a short "Start here" pointer at the top of its section's first page.
- **Find a rule by fields.** Table 2 is split across category pages, and a "Find a rule" index page maps field combinations to rule IDs, because a 31×4 table is hard to scan on small screens.
- **Rule IDs as anchors**, so the code map, changelog, and other pages can deep-link to a rule. ReadMe auto-anchors headings; whether it supports `id` attributes inside table cells is not verified. Test it in PR 1. If it doesn't work, fall back to one heading per rule or a rule-ID list above each table.
- **Real Markdown tables**, not images, so ReadMe search indexes cell contents.
- **Cross-links at the point of need.** Matching Rules → the probability rows backing a rule → Methodology; Validation Requirements → Test Set; Normalization → library functions.
- **Replace the spec's lettering with descriptive page titles** and keep the original section label in a first-line "Spec section: C.7" note, so people citing the Doc can find the page.
- **Unique page titles.** No page is simply "Overview"; the section name is part of the title (for example "Test Set Overview").
- **Prev/next and "Related pages" footer** on spec pages to preserve linear reading.
- **Machine-readable downloads** (Table 2 CSV/JSON) from the same conversion script, so engineers don't retype rules.

## Community: contributors, issues, contributing

Pages under a **Community** nav entry (Contributors, Report an Issue, Contribute, License and Open Source, How to Cite), linked from the landing page and the "Related pages" footers on spec pages.

**Report an Issue.** One page that routes by what the reader found, so reports land in the right place:

| What | Where it goes |
|---|---|
| Spec content: unclear, incorrect, or a change request | The spec's public comment process (Document Control and Comments page) during a comment period; afterwards, submit a proposal (see Contribute) |
| Test set: wrong label, bad case, format problem | GitHub Issues on `cms-hte-patient-matching-test-set` |
| Reference library: bug or rule-coverage gap | GitHub Issues on `cms-hte-patient-matching` |
| Hosted UI | Contact route TBD (see Open questions) |
| This site: typo, broken link, stale content | GitHub Issues on this docs repo (requires the repo to be public; see Open questions) |

The page lists what to include in a report (spec version or library/test-set version, rule ID, minimal example using synthetic data only, expected vs. actual) and carries a prominent "never include real patient data" warning. Per-repo issue templates are optional follow-up work in those repos, not part of this plan.

**Contribute.** One page with a section per contribution type, each linking to the authoritative instructions rather than restating them:

- **Spec changes:** submit a proposal containing the elements the Governance section requires (description, rationale, implementation impact, validation plan or evidence). Describes the path Under Review → Accepted, the 30-day comment period, and the 90-day transition for substantive changes. Links to the Proposals pages and the proposal template.
- **Test data:** link to the test set's `CONTRIBUTING.md`. Summarize its key rules in a few lines (only synthetic records derived from a disclosed method, or cited aggregate statistics; no raw real records; fabricated values marked as synthetic).
- **Code (library, test set):** link to each repo's `CONTRIBUTING.md` (dev setup, tests, pre-commit) and their license (Apache-2.0).
- **Docs (this site):** how to edit and submit a change. Local edit, `npx @readme/cli lint`, PR into `v1.0`, with the note that merged changes publish. The ReadMe web editor path, if contributors are allowed to use it.
- **Licensing:** contributions are accepted under the target repo's license; state that on the page.

**License and Open Source.** Lists the license of each repo (site, spec text, library, calculations, test set) and the data-source terms (Census, ACS, CMS, ONC). Requires adding a LICENSE file to the docs repo and a decision on the license for the spec text.

**How to Cite.** Gives the citation form for a spec version, including version number and release date.

**Contributors.** A page listing contributors, grouped as Spec authors and workgroup, Test set and library contributors, and Organizations. Built from a curated list, not a raw `git log` dump, because:
- the repos' contributor lists include bots (`claude[bot]`, `bwell-dev`) and GitHub handles rather than names;
- listing a person by name publicly should be their choice.

Each entry: name or handle, organization, role, optional link. Source is a `contributors` data block in the page, edited by PR. Seed it from the spec's workgroup/author information and the GitHub contributor lists, then confirm names with each person before publishing.

## Hosted testing UI

b.well also runs a service with a UI for testing patient matching: https://patient-matching-service.bwell.com. The site gets a **Try It** page group for it.

- **Placement:** pages under Implement and Test → Try It, and a card on the landing page ("Try matching in your browser"), plus links from Matching Rules (try a rule combination), Reference Implementations (the hosted service wraps the library), and the Test Set (run cases through the UI).
- **Content:** a page describing what the UI does and its limits, and a walkthrough with a sample query and how the result maps to a Table 2 rule ID. The walkthrough needs screenshots, which go in the repo and must use synthetic data only.
- **Scope boundary:** the site links to the UI; it does not document an HTTP API unless the service exposes one for ecosystem participants (see Open questions on the API Reference).
- **Not verified:** I could not reach the URL from this environment (no response), so access requirements and behavior are unconfirmed.

## Test set, reference implementation, and calculations access

Site pages summarize and link; they do not copy repo content.

- **Why link rather than mirror:** the test set README and library README change with the code (the test set repo is actively iterating, with sessions logs and pending work). Copied content would drift.
- **What the site adds:** orientation (what/why/when), the spec-to-test mapping, and a stable entry URL. Each page opens with a "Source of truth: `<repo path>`" link.
- **Cross-links from the spec:** the Validation Requirements page links to the test set; the Matching Rules and Normalization pages link to the library's rule/normalizer modules.
- **Calculations follow the same rule.** Methodology pages link to `calculations/docs/` and the generated `outputs/u_probabilities.md` as the source of truth. Numbers shown on the site (e.g. the empirical-vs-conservative comparison) are quoted with the calculations commit they came from.
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

Because `v1.0` publishes on push, work goes through PRs into `v1.0`. Each PR is independent (base `v1.0`; no stacking) and states what it covers and defers. Pages stay `hidden: true` until the last PR so partial content is never public.

| PR | Scope | Defers |
|---|---|---|
| 0. Repo readiness | LICENSE file, decision on repo visibility, branch/preview check (open questions 4, 15, 17, 19) | All content |
| 1. Skeleton | `_order.yaml` files for the six sections, titled hidden pages, remove template callouts, rule-ID anchor test | All content |
| 2. Spec: framing | Summary and Purpose, Core Principles, Risk Framework | Rules, model |
| 3. Spec: Matching Rules | Table 2, 2-H, 2-I, Category 2, Table 4, twins, how-to-apply, IAL2 tokens, Find a Rule index | Probability model |
| 4. Spec: Probability Model | Model & Assumptions pages incl. insurance identifiers, Reference Script pointer | Normalization onward |
| 5. Spec: remainder | Normalization, Validation, Audit, Governance, References, Document Control | Methodology and tools |
| 6. Methodology | 7 pages sourced from `calculations/` and the test-set methodology | Spec-to-Code Map |
| 7. Implement and Test | Reference Implementations (incl. Spec-to-Code Map), Test Set, Try It, Table 2 downloads, Compatibility Matrix | Implementation Guide, Conformance Checklist |
| 8. Audience layer | For Decision Makers, Adoption Timeline, Implementation Guide, Conformance Checklist, FAQ, Status, Glossary | Spec-author review is a gate before merge |
| 9. Changes | Changelog and Proposals overview pages, proposal template, v3.4.0 entry, existing proposals | Pre-3.4.0 backfill unless source material exists |
| 10. Community | Contributors, Report an Issue, Contribute, License and Open Source, How to Cite | Contributor names not yet confirmed |
| 11. Launch | Landing page with audience cards, flip `hidden`, cross-link pass, lint and link check | — |

## Maintenance

- **Spec changes during comment period.** Record the Doc `revisionId` used for each conversion in the PR description. Re-run the extract and diff script to produce a change list instead of re-reading the Doc.
- **Source of truth.** Until the spec is finalized, the Google Doc is canonical and the site follows it. Decision needed on whether the repo becomes canonical afterward (see Open questions).
- **Methodology pages** record the `calculations/` commit they were written against and are re-checked when `outputs/u_probabilities.md` changes.
- **Compatibility Matrix** is updated at every spec release and every library, test-set, or service release.
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
15. **Where do issue reports go for the spec and the hosted UI?** The docs repo `icanbwell/cms-hte-patient-matching-spec` is private, so readers cannot file issues there. Since the project is open source, recommendation: make it public. Alternatives: a public repo or intake form, or an email alias.
16. **Who triages reports and who approves proposals?** The Report an Issue and Contribute pages need a named owner or alias and an expected response, or readers get no answer.
17. **Can external contributors edit the docs?** Yes if the repo becomes public (question 15). Otherwise the Contribute page's docs section becomes "suggest an edit" via the issue route.
18. **Origin of the spec's probability values:** are the spec's per-field conservative u-values and Table 2 P(collision) values derived from the `calculations/` tool, chosen independently and checked against it, or something else? This decides how Methodology describes the relationship.
19. **Licenses:** which license covers the site content and the spec text (the code repos are Apache-2.0)? The docs repo has no LICENSE file.
20. **Audience-layer authorship and review:** who writes For Decision Makers, the Implementation Guide, and the Conformance Checklist, and do the spec authors review them before publication? These pages interpret the spec and carry more risk of misstatement than the converted pages.
21. **Conformance Checklist scope:** is it informational, or does the workgroup consider it an official companion to the spec? This changes its wording and who approves it.

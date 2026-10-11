# Design: Populating the Patient Matching Docs Site

Status: Draft for review. Open questions from the first review were resolved on 2026-10-10; see Decisions.
Author: Imran Qureshi
Date: 2026-10-10
Docs repo: https://github.com/imranq2/cms-hte-patient-matching-spec (public)

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
2. **Mixed section numbering and stale cross-references.** Sections are numbered I to IX with letters A to I. Most numbers are automatic list numbering in the Doc, while others are typed by hand (B.1, C.2 to C.9, G, H.1 to H.5, I), and there is no C.1 heading. Several passages in section III.C cite section numbers from the proposals that introduced them (for example §3.3 and §4.5) that do not exist in v3.4.0. The site pages keep the Doc's wording and show the Doc's section label on each page; the Status page lists the cross-reference issues.
3. **Still in comment period.** Content will change after publication.
4. **Rule counts differ between spec and library.** The spec's Executive Summary counts 30 Category 1 and 8 Category 2 rules and also describes two new rules, 39 and 40 (40 in total). The library README counts 29 Category 1 and 10 Category 2 (39 in total), because the library omits rule 29 ahead of proposal v3.4.1 (under review); its architecture diagram still says 38. Rule counts on the site always carry a spec version.
5. **No license on the docs repo.** `imranq2/cms-hte-patient-matching-spec` is public with issues enabled, but has no LICENSE file, so the site content and the spec text have no stated license. The repo is under a personal account, not an `icanbwell` org repo (see Remaining open items).
6. **Stale reference script.** The spec's "Reference Script to calculate P(collision)" section points to a personal Gist. The repo's `calculations/` project supersedes it. Fixing the spec link is for the spec authors; the site links to the repo.
7. **Spec values vs. computed values.** Confirmed: the spec's per-field conservative u-values and Table 2 P(collision) values were chosen independently, and the `calculations/` tool is a check against them (matching its README, which calls them "hand-picked conservative u-values"). The Methodology pages must say this and must not describe the spec values as computed by the tool.

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
    v3.3.x entries                     backfilled from proposals v3.3.1 to v3.3.6 (see Changelog and Proposals)
  Proposals
    Overview                           how proposals work (links to Governance and Versioning), lifecycle and statuses
    Under Review                       index table: ID, title, summary, affected spec sections, link to GitHub issue
    Accepted                           index table: ID, title, summary, link to GitHub issue, changelog entry
    Rejected and Withdrawn             same table form; empty at launch

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

- **For Decision Makers:** what the spec requires (return matching records when a query matches a Table 2 combination and yields a unique candidate; failing to is non-compliant), who it applies to, why (the cost of mismatches and non-return), and what an organization needs to do. Drafted by Claude and reviewed by Imran before publication (no separate workgroup sign-off; the spec authors can still correct pages after publication).
- **Adoption Timeline:** effective date (currently TBD in the Doc), the 90-day transition for substantive changes, and the phased adoption and safe harbor the spec describes.
- **Implementation Guide:** a decision-flow diagram and step list, plus worked examples for a Category 1 match, a Category 2 household/individual two-step, and a twin case. Examples use test-set records.
- **Conformance Checklist (informational, non-normative; the spec text governs):** the SHALL requirements gathered in one checklist with links to the pages that define them, and the validation evidence the spec requires (observed precision, recall, and false-positive rate on the ONC dataset or a successor).
- **FAQ:** seeded from comment-period questions as they arrive.
- **Status:** current version, comment-period dates, known issues (such as the rule-count mismatch) until resolved.

### Methodology and Data

The calculations are a separate project, not a reference implementation, so they get their own section rather than a place under Reference Implementations. Pages summarize and link to `calculations/` (see "Test set, reference implementation, and calculations access"). Content rules:

- Report what the README and generated `outputs/u_probabilities.md` say, with the data download dates and checksum note, not a paraphrase that could drift.
- State plainly which fields are point estimates and which are floors or proxies.
- Say that the spec's values were chosen independently and checked against this tool. Do not describe them as computed by it.
- Data Sources carries attribution for each public source and the redistribution caveat from the test-set README for the ONC dataset.

### Changelog and Proposals

**Requirements:** show a changelog each time a new spec version is created, and list proposals currently under review and proposals previously accepted.

**Where proposals live.** Proposals are GitHub Issues in this repo, and that is where discussion and status are recorded. The 7 existing proposals (previously Google Docs in a Drive folder) were migrated on 2026-10-10 as issues #1 to #7 with the original Doc linked from each. New proposals are filed as GitHub Issues or PRs.

| Issue | Proposal | State | Labels |
|---|---|---|---|
| #1 | v3.3.1 Household-Then-Individual Matching | Closed | `proposal`, `status: accepted` |
| #2 | v3.3.2 Compliance, Testing & Audit Clarifications | Closed | `proposal`, `status: accepted` |
| #3 | v3.3.3 Relationship-Based Matching for Minors and Newborns | Closed | `proposal`, `status: accepted` |
| #4 | v3.3.4 Placeholder Value Exclusion in Patient Matching | Closed | `proposal`, `status: accepted` |
| #5 | v3.3.5 Test Dataset & Accuracy Methodology | Closed | `proposal`, `status: accepted` |
| #6 | v3.3.6 Institutional Address Identification Methodology | Open | `proposal`, `status: under-review` |
| #7 | v3.4.1 Remove Rule 29 | Open | `proposal`, `status: under-review` |

**Lifecycle, grounded in the spec's Governance and Versioning section.** A proposal states the change, rationale, anticipated implementation impact, and a validation plan or evidence where applicable. Changes affecting Table 2, the threshold, approved fields, normalization, fuzzy constraints, or required testing get at least 30 days of public comment. Adopted changes ship with a version increment, an effective date, and (for substantive changes) a transition period of at least 90 days. The workgroup decides proposals. Status is a label on the issue: `status: under-review`, `status: accepted`, `status: rejected`, `status: withdrawn` (all four created). The Governance text itself defines only adoption, so the Rejected and Withdrawn statuses are additions to be reflected in a Governance proposal if the workgroup wants them in the spec.

**Site pages.** The Proposals section has an overview and index tables by status (Under Review, Accepted, Rejected and Withdrawn). Each row has the ID, title, one-line summary, affected spec sections, and a link to the issue. The site does not mirror full proposal text, so it cannot drift from the issue. A small script can generate the tables from `gh issue list --label proposal`; until there are more than ~10 proposals they are maintained by hand.

**Changelog entries** (`docs/Changelog/v3-4-0.md` etc.), one page per version, newest first, each with:
- Version, release date, effective date, semver class (Major / Minor / Patch) and a one-line reason
- Change list grouped as Added / Changed / Removed, each item linking to the affected spec page and rule ID anchor (e.g. Table 2 rows added or removed)
- Links to the issues for the proposals that produced the change
- Transition period end date for substantive changes

**Backfill.** The Changelog starts at v3.4.0 and backfills v3.3.1 to v3.3.6 from the proposals, since no other change notes were identified. Which of those versions were actually released needs confirming (see Remaining open items).

**Spec status banner:** the landing page and Spec Summary show the current released version and link to the Under Review table, since the spec is in a comment period.

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
| Spec content: unclear, incorrect, or a comment on the draft | GitHub Issues on this docs repo (titled with a "Spec comment:" prefix; maintainers apply labels), during the comment period; a substantive change is filed as a proposal (see Contribute) |
| Test set: wrong label, bad case, format problem | GitHub Issues on `cms-hte-patient-matching-test-set` |
| Reference library: bug or rule-coverage gap | GitHub Issues on `cms-hte-patient-matching` |
| Hosted UI | Contact route not decided (see Remaining open items) |
| This site: typo, broken link, stale content | GitHub Issues on this docs repo |

The page lists what to include in a report (spec version or library/test-set version, rule ID, minimal example using synthetic data only, expected vs. actual) and carries a prominent "never include real patient data" warning. b.well maintainers triage issues. Per-repo issue templates are optional follow-up work in those repos, not part of this plan. The spec's Document Control "Submit Comments To" field is empty today; it should point to this route (a spec-author edit).

**Contribute.** One page with a section per contribution type, each linking to the authoritative instructions rather than restating them:

- **Spec changes:** file a proposal as a GitHub Issue (or PR) containing the elements the Governance section requires (description, rationale, implementation impact, validation plan or evidence). Describes the path Under Review → Accepted, the 30-day comment period, the 90-day transition for substantive changes, and that the workgroup decides. Links to the Proposals index and to an issue template (to be added to this repo) based on the migrated proposals' structure.
- **Test data:** link to the test set's `CONTRIBUTING.md`. Summarize its key rules in a few lines (only synthetic records derived from a disclosed method, or cited aggregate statistics; no raw real records; fabricated values marked as synthetic).
- **Code (library, test set):** link to each repo's `CONTRIBUTING.md` (dev setup, tests, pre-commit) and their license (Apache-2.0).
- **Docs (this site):** the repo is public, so outside contributors open PRs. Steps: local edit, `npx @readme/cli lint`, preview locally with `@readme/cli`, PR into `v1.0`. State that there are no hosted PR previews and that merged changes publish.
- **Licensing:** contributions are accepted under the target repo's license (Apache-2.0 for the code repos and for this site and the spec text); state that on the page.

**License and Open Source.** Lists the license of each repo (site, spec text, library, calculations, test set) and the data-source terms (Census, ACS, CMS, ONC). The site content and the spec text are Apache-2.0; this requires adding a LICENSE file to the docs repo.

**How to Cite.** Gives the citation form for a spec version, including version number and release date.

**Contributors.** A page listing contributors, from the list Imran provided, grouped as Spec authors and workgroup, Test set and library contributors, and Organizations. Built from a curated list, not a raw `git log` dump, because:
- the repos' contributor lists include bots (`claude[bot]`, `bwell-dev`) and GitHub handles rather than names;
- listing a person by name publicly should be their choice.

**Initial list** (provided 2026-10-10; names and organizations only, never email addresses). Some names were derived from the email addresses supplied; the last column lists what still needs confirmation:

| Name | Organization | Needs confirmation |
|---|---|---|
| Aaron Madsen | Portobello Health | |
| Sean Hegarty | b.well Connected Health | Spelling |
| Adam Culbertson | b.well Connected Health | Spelling |
| Cody Ebberson | Medplum | Surname inferred from the v3.4.1 proposal text; confirm it's the same person |
| Andre Quina | Arcadia | Spelling |
| Nicholas Orser | Verato | Supplied twice (as Nicholas and as Nick); listed once |
| Lance Laforge | Verato | Capitalization of surname |
| Harry Freedman | Epic | |
| Luke Breyer | Epic | |

Each entry: name or handle, organization, role, optional link. Source is a `contributors` data block in the page, edited by PR. Nothing is published until Imran has confirmed each entry. Proposal text in issues #6 and #7 and the migrated proposals also name individual commenters; those names are public in the issues.

## Hosted testing UI

b.well also runs a service with a UI for testing patient matching: https://patient-matching-service.bwell.com. The site gets a **Try It** page group for it.

- **Access (confirmed by Imran):** public, no login. The UI accepts synthetic data only.
- **Placement:** pages under Implement and Test → Try It, and a card on the landing page ("Try matching in your browser"), plus links from Matching Rules (try a rule combination), Reference Implementations (the hosted service wraps the library), and the Test Set (run cases through the UI). Ships in PR 7.
- **Content:** a page describing what the UI does and its limits, with a prominent "synthetic data only" warning, and a walkthrough with a sample query and how the result maps to a Table 2 rule ID. Screenshots go in the repo and use test-set records.
- **Scope boundary:** the site links to the UI. It does not publish an API Reference. The Service page links to the `cms-hte-patient-matching-service` repo and to the running service's own `/docs`.
- **Unresolved conflict (launch blocker for linking to the UI):** the service README says the testing UI (`ENABLE_TESTING_UI`) "has no auth of its own" and must never be enabled in a production or externally reachable deployment. A public, no-login UI contradicts this. Resolve before the site links to it: confirm what is deployed at that URL, or update the README if the exposure is intended.
- **Not verified:** I could not reach the URL from this environment (no response), so behavior is unconfirmed.

## Test set, reference implementation, and calculations access

Site pages summarize and link; they do not copy repo content.

- **Why link rather than mirror:** the test set README and library README change with the code (the test set repo is actively iterating, with sessions logs and pending work). Copied content would drift.
- **What the site adds:** orientation (what/why/when), the spec-to-test mapping, and a stable entry URL. Each page opens with a "Source of truth: `<repo path>`" link.
- **Cross-links from the spec:** the Validation Requirements page links to the test set; the Matching Rules and Normalization pages link to the library's rule/normalizer modules.
- **Calculations follow the same rule.** Methodology pages link to `calculations/docs/` and the generated `outputs/u_probabilities.md` as the source of truth. Numbers shown on the site (e.g. the empirical-vs-conservative comparison) are quoted with the calculations commit they came from.
- **Spec-to-Code Map** is the one page that is new content. It is built from the library's rule definitions and is maintained by the library maintainers, as part of the library's release process; the site page is refreshed from it (see Maintenance).

## Conversion approach

1. **Extract mechanically, not by copy-paste.** Pull the Doc as JSON via the Google Docs API (already retrievable in this environment) and convert to Markdown with a script, so table cells and numeric values (P(collision) etc.) are not retyped. Script lives in the scratch area or a `tools/` directory and is not published.
2. **Split by heading** into the pages above, applying the slug and `_order.yaml` plan.
3. **Hand-edit for MDX/ReadMe:** frontmatter, `<Callout>` for normative notes and draft status, `<Cards>` for audience paths, link rewriting.
4. **Verify against source:**
   - Diff the extracted plain text of the site pages against the Doc's plain text; every sentence in the Doc appears exactly once.
   - Row/column counts of all 11 tables match (31×4, 31×3, 22×4, 15×3, 11×3, 8×3, 7×4, 6×2, 5×3, 4×4, 3×4).
   - Every numeric cell in Table 2 / 2-H / 2-I / Model tables is compared programmatically.
   - Check the Doc for inline images/drawings (none seen in the text extract; confirm) and for the embedded Gist link in the Executive Summary.
5. `npx @readme/cli lint` plus a link check on the final tree, and a local rendered preview with `@readme/cli`, because ReadMe does not sync non-`v1.0` branches to previews.

## Delivery plan

Because `v1.0` publishes on push, work goes through PRs into `v1.0`. Each PR is independent (base `v1.0`; no stacking) and states what it covers and defers. Pages stay `hidden: true` until the last PR so partial content is never public.

| PR | Scope | Defers |
|---|---|---|
| 0. Repo readiness | Apache-2.0 LICENSE file, proposal issue template, local-preview instructions, resolve ReadMe version naming | All content |
| 1. Skeleton | `_order.yaml` files for the six sections, titled hidden pages, remove template callouts, rule-ID anchor test | All content |
| 2. Spec: framing | Summary and Purpose, Core Principles, Risk Framework | Rules, model |
| 3. Spec: Matching Rules | Table 2, 2-H, 2-I, Category 2, Table 4, twins, how-to-apply, IAL2 tokens, Find a Rule index | Probability model |
| 4. Spec: Probability Model | Model & Assumptions pages incl. insurance identifiers, Reference Script pointer | Normalization onward |
| 5. Spec: remainder | Normalization, Validation, Audit, Governance, References, Document Control | Methodology and tools |
| 6. Methodology | 7 pages sourced from `calculations/` and the test-set methodology | Spec-to-Code Map |
| 7. Implement and Test | Reference Implementations (incl. Spec-to-Code Map), Test Set, Try It, Table 2 downloads, Compatibility Matrix | Implementation Guide, Conformance Checklist |
| 8. Audience layer | For Decision Makers, Adoption Timeline, Implementation Guide, Conformance Checklist (informational), FAQ, Status, Glossary | Imran reviews before merge |
| 9. Changes | Changelog overview and v3.4.0 entry, v3.3.1 to v3.3.6 backfill from proposals, Proposals overview and index tables from issues #1 to #7 | Anything before v3.3.1 |
| 10. Community | Contributors, Report an Issue, Contribute, License and Open Source, How to Cite | Contributor entries Imran has not confirmed |
| 11. Launch | Landing page with audience cards, flip `hidden`, cross-link pass, lint and link check | — |

## Maintenance

- **Spec changes during comment period.** Record the Doc `revisionId` used for each conversion in the PR description. Re-run the extract and diff script to produce a change list instead of re-reading the Doc.
- **Source of truth.** Until the spec is finalized, the Google Doc is canonical and the site follows it. Once the comment period closes and the spec is final, the Markdown in this repo becomes canonical and the Google Doc is archived or read-only. After that, spec changes are PRs.
- **ReadMe versions.** Each spec version gets its own ReadMe version (branch), so older spec text stays browsable; the Changelog links across them.
- **Methodology pages** record the `calculations/` commit they were written against and are re-checked when `outputs/u_probabilities.md` changes.
- **Compatibility Matrix** is updated at every spec release and every library, test-set, or service release.
- **Spec-to-Code Map** is re-verified whenever the library's rule set changes; add a note on the page naming the library version it was built against.

## Decisions

Resolved with Imran on 2026-10-10.

| # | Topic | Decision |
|---|---|---|
| 1 | Source of truth after finalization | This repo; Google Doc archived or read-only |
| 2 | Spec vs. library rule counts | Spec is correct (30 Category 1 + 8 Category 2 in v3.4.0); library README needs correcting |
| 3 | ReadMe versioning | One ReadMe version per spec version |
| 4 | Branch previews | None exist; use local preview and Markdown review; merging publishes |
| 5 | API Reference for the service | Link only; no OpenAPI under `reference/` |
| 6 | Comment route | GitHub Issues on this repo |
| 7 | Spec-to-Code Map owner | Library maintainers |
| 8 | Proposal source and statuses | GitHub Issues/PRs going forward; four statuses (Under Review, Accepted, Rejected, Withdrawn) |
| 9 | Existing proposals and history | 7 proposals migrated to issues #1 to #7; Changelog backfilled from them |
| 10 | Changelog granularity | One page per version |
| 11 | Hosted UI access | Public, no login (conflicts with service README; see Hosted testing UI) |
| 12 | Hosted UI data | Synthetic data only |
| 13 | Try It delivery | PR 7 |
| 14 | Contributors | Imran provided the list; confirmations pending |
| 15 | Docs repo visibility | Public (it already is: `imranq2/cms-hte-patient-matching-spec`) |
| 16 | Triage | Workgroup decides proposals; b.well maintainers triage issues |
| 17 | External docs edits | Yes, via PRs to the public repo |
| 18 | Origin of spec probability values | Chosen independently; `calculations/` is a check |
| 19 | Content license | Apache-2.0 |
| 20 | Audience pages | Claude drafts, Imran reviews; no workgroup sign-off |
| 21 | Conformance Checklist | Informational (non-normative) |

## Remaining open items

1. **Hosted UI exposure vs. README warning.** Confirm what is deployed at `patient-matching-service.bwell.com` and reconcile with the service README before the site links to it.
2. **Docs repo home.** It is under the personal account `imranq2`, not an `icanbwell` org repo. Moving it later changes URLs; issues transfer with the repo. Decide whether to transfer before launch. Note that `icanbwell/cms-hte-patient-matching-spec` redirects to an unrelated private repo, so links using that name are wrong.
3. **ReadMe version naming.** The current branch and ReadMe version are `v1.0`. Decide how spec version 3.4.0 maps to it and what future branches are called (for example `v3.5`), including slug conventions.
4. **Changelog backfill (resolved by the implementation).** Proposals v3.3.1 to v3.3.6 and v3.4.1 are named for the version they were drafted for, and each modifies v3.3.0 (or v3.4.0 for v3.4.1). The spec's Executive Summary says v3.4.0 incorporates v3.3.1 to v3.3.5. They are not separate releases, so the Changelog has one page, v3.4.0, listing the changes by proposal. Still open: whether change notes exist for v3.3.0 and earlier.
5. **Proposal text on the site.** The plan links to issues and does not mirror proposal text. Confirm that is acceptable, or add per-proposal site pages.
6. **Library README correction.** Someone needs to correct the rule counts in `cms-hte-patient-matching`'s README (29+10, diagram 38).
7. **Named individuals.** Issues #6 and #7 and the migrated proposals name commenters (Cody Ebberson, David Pyke, Alex Dzeda, and "We Malone", likely a typo). They are now public; confirm those people are comfortable. Four contributor-table entries also still need confirmation (see Contributors).
8. **Hosted UI contact route** for the Report an Issue page.
9. **Spec's "Submit Comments To" field** is empty and should point to GitHub Issues (spec-author edit).

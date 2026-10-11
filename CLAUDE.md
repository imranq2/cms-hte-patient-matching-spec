# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The source for the Patient Matching documentation site, which is git-synced with [ReadMe](https://readme.com) (readme.io). It contains only Markdown/MDX content and YAML ordering files — no application code, build system, or tests.

The default branch is `v1.0`, which corresponds to ReadMe docs version 1.0 (not `main`). Because of the sync, this repo is the published site's source of truth:

- Content merged/pushed to `v1.0` is what ReadMe publishes, so treat commits there as publishing changes. Prefer a branch and PR for non-trivial edits.
- Edits made in the ReadMe web editor are committed back to this repo automatically (the `Created "<Page>" in docs|reference` commits). Pull before editing locally to avoid conflicts.
- Page slugs, frontmatter, and `_order.yaml` entries drive the live site's URLs and navigation, so renaming or deleting a page changes or breaks published links.

## Commands

Uses `@readme/cli` via `npx` (no local install):

- `npx @readme/cli lint` — lint docs
- `npx @readme/cli --help` — preview locally, validate OAS specs, etc.
- `npx @readme/cli setup:github` — add lint GitHub Action (not yet configured; there is no `.github/`)

## Structure

- `docs/` — guides, in six categories (each a subdirectory): `Getting Started` (landing page and audience pages), `Specification` (spec v3.4.0), `Methodology` (probability calculations, test-set methodology), `Implement and Test`, `Changes` (changelog and proposals), `Community`. Pages with children are a folder with an `index.md` plus an `_order.yaml` (the folder name is the slug).
- `reference/` — API reference section. `reference/ReadMeConfig/` holds the stub pages that configure ReadMe's API Explorer via `api_config`; they are `hidden: true`. No OpenAPI spec is published; the service page links to the service repo instead.
- `tools/` — scripts that generate or check content (not published). `assets/` — images and data files linked from pages by `raw.githubusercontent.com` URLs on the `main` branch. `design/` — the site design document (not published).
- Proposals are GitHub Issues in this repo (labels `proposal` and `status: under-review|accepted|rejected|withdrawn`); the site's Proposals pages index them.

## Specification pages are generated

`docs/Specification/**` is produced from the source Google Doc (document id `1NytpfZ05aokS-gD7uDIQE7gEyms9zMgoiaIah_w4VTE`). **Do not hand-edit these pages**; re-run the converter so the text stays identical to the Doc.

- Inputs: the Doc's Markdown export (`https://docs.google.com/document/d/<id>/export?format=md`) and its Google Docs API JSON (`documents.get`).
- `python3 tools/convert_spec.py --markdown spec.md --json spec.json --out docs/Specification` writes the pages and prints a word-by-word comparison against the Doc. Expected differences are list numbers, headings moved into page titles, and the cover lines. Anything else is a bug.
- `python3 tools/build_conformance_checklist.py` rebuilds `docs/Implement and Test/conformance-checklist.md`. Every item is a verbatim quotation and the script fails if the spec no longer contains it.
- `python3 tools/export_tables.py --json spec.json --out assets/data` regenerates the CSV/JSON downloads.
- Re-run all three for every new spec version, and update the Changelog, Compatibility Matrix, and Spec-to-Code Map.
- Do not copy facts about the other repos (library, service, test set, calculations) from memory. Read their READMEs and source; the site pages link to them as the source of truth.

## Conventions specific to ReadMe

- Navigation order is controlled by `_order.yaml` files, not filenames. Each directory has one listing page slugs (without `.md`) in display order; `docs/_order.yaml` and `reference/_order.yaml` list category directory names. A folder's `_order.yaml` must not list `index`. When adding, renaming, or removing a page or category, update the matching `_order.yaml`.
- Slugs are the file names (or folder names for pages with children) and must be unique across `docs/`. Internal links are `/docs/<slug>`.
- Pages begin with YAML frontmatter (`title`, `hidden`, optionally `excerpt`, `icon`, `api_config`). Pages are `hidden: false` (visible) except the `reference/ReadMeConfig` stubs. Hidden is a visibility setting, not access control; set `hidden: true` on a page you do not want shown.
- Pages are MDX. Escape `<`, `>`, `{` and `}` in prose and tables, write `<br />` (not `<br>`), and use `[text](url)` links, not `<https://...>` autolinks. Use `<Callout>` and `<Cards>`/`<Card>` where the template does.
- `@readme/cli` could not be installed in one environment (npm 403 on a dependency). To check MDX syntax without it, compile each page with `@mdx-js/mdx` and `remark-gfm`.

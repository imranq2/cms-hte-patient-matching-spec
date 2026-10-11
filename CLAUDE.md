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

- `docs/` — guides. Each subdirectory is a category (e.g. `docs/Getting Started/`) containing pages.
- `reference/` — API reference section. `reference/ReadMeConfig/` holds the stub pages (`getting-started`, `authentication`, `my-requests`) that configure ReadMe's API Explorer via the `api_config` frontmatter key; they are `hidden: true`.
- No OpenAPI spec has been added yet; endpoint pages will need one under `reference/`.

## Conventions specific to ReadMe

- Navigation order is controlled by `_order.yaml` files, not filenames. Each directory has one listing page slugs (without `.md`) in display order; the top-level `docs/_order.yaml` and `reference/_order.yaml` list category directory names. When adding, renaming, or removing a page or category, update the matching `_order.yaml`.
- Pages begin with YAML frontmatter (`title`, `hidden`, optionally `excerpt`, `icon`, `api_config`).
- Pages use ReadMe MDX components (`<Callout>`, `<Cards>`/`<Card>`), not plain Markdown equivalents.
- `docs/Getting Started/getting-started.md` is still the unedited ReadMe template (contains a "Template: Delete this callout" notice and placeholder `href="#"` links).

# Changelog

## 0.4.0 - 2026-06-01

- Reframed the project around local knowledge organization, AI governance, recall, and maintenance.
- Added `00-Agent-Governance/` with startup contract, write-back rules, review gates, and maintenance loop.
- Added `02-Knowledge-Pipeline/` for local material intake and source-to-knowledge workflow.
- Added `03-Recall-System/` for task-to-context maps and recall fields.
- Added `scripts/kb.py intake-source` to create source analysis cards from local paths or URLs.
- Added `examples/source-to-knowledge/` as an end-to-end source organization example.

## 0.3.0 - 2026-06-01

- Removed the thin extra startup layer. Startup rules now live in `START-HERE.md` and `AGENTS.md`.
- Removed the thin map-of-content layer from the starter kit. Navigation now starts from `index.md` and project bridge cards.
- Added `MIGRATION.md` for existing Obsidian vaults.
- Added a filled project example under `examples/filled-example/`.
- Added repository-level versioning with `VERSION` and this changelog.
- Generalized role fields in templates.
- Marked the multi-agent coordination guide as an optional advanced module.

## 0.2.0 - 2026-06-01

- Flattened Inbox paths.
- Added `scripts/kb.py health-check`.
- Added `scripts/kb.py new-project`.
- Rewrote health checks to use only public starter-kit concepts.

## 0.1.0 - 2026-06-01

- Initial private release of Obsidian AI Memory Kit.
- Added startup entry, project bridge card, templates, source triage, shared assets, and bilingual README files.

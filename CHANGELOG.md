# Changelog

## 0.5.6 - 2026-06-01

- Added Python unit tests under `tests/` and made CI run them.
- Added a Before / After case showing how a messy folder becomes AI-readable project knowledge.
- Clarified that the kit is a workflow convention, not a full automation platform, and that it depends on continued write-back discipline.
- Clarified the local-clone install path for security-sensitive users.
- Added an English README note explaining non-English source filenames.

## 0.5.5 - 2026-06-01

- Added `TPL-问题事故经验卡.md` for failure, rework, wrong-assumption, user-correction, and tool-incident lessons.
- Updated startup, recall, governance, and write-back rules so agents check whether incidents should be promoted before ending a task.
- Added the incident template to health-check required paths and README template lists.
- Aligned README version text with the `0.5.5` release.

## 0.5.4 - 2026-06-01

- Replaced the README Mermaid architecture diagram with a generated PNG image.
- Added `docs/images/architecture-flow.png` as the project architecture visual.
- Updated the `docs/` layout description to include diagrams.

## 0.5.3 - 2026-06-01

- Replaced the mixed `LICENSE.md` file with a standard root `LICENSE` for MIT-licensed code and scripts.
- Added `CONTENT-LICENSE.md` for CC BY 4.0 licensing of written content, templates, examples, and documentation.
- Removed private-repository install warnings from README files before public beta.
- Updated release checklist wording for public beta readiness.

## 0.5.2 - 2026-06-01

- Added CI status badges to the English and Chinese README files.
- Documented the `docs/` directory in the repository layout.
- Aligned the repository version with the latest release tag after documentation updates.

## 0.5.1 - 2026-06-01

- Renamed the project to Obsidian AI Workflow Kit.
- Updated repository slug references, installer URLs, script wording, and documentation wording.
- Kept the workflow focused on Obsidian-based AI handoff, local knowledge organization, governance, and recall.

## 0.5.0 - 2026-06-01

- Added GitHub Actions CI for health checks, installer tests, and tool tests.
- Added `RELEASE_CHECKLIST.md` for private beta and public release readiness.
- Added 10-minute first-run guides in English and Chinese.
- Clarified target users, non-goals, maturity, and private repository install limits in README files.

## 0.4.5 - 2026-06-01

- Added `scripts/kb.py intake-folder` to create controlled folder inventory cards without moving original files.
- Added `scripts/kb.py audit-vault` to check entry points, Inbox files, project bridge coverage, stale concepts, and links.
- Added script tests for folder intake and vault audit behavior.
- Documented the new tools in both README files and script documentation.

## 0.4.4 - 2026-06-01

- Added `install.sh` for one-line remote installation.
- Added installer tests covering dry-run, install, skip-existing, and overwrite behavior.
- Added one-line install instructions to both README files and script documentation.

## 0.4.3 - 2026-06-01

- Added `scripts/kb.py install-core` for installing the kit into an existing Obsidian vault.
- Documented the safe dry-run install path in both README files.
- Clarified that installation skips existing files by default and only overwrites with `--overwrite`.

## 0.4.2 - 2026-06-01

- Rewrote the README opening around the repeated AI session handoff problem.
- Added comparison tables explaining why this is different from tool-specific memory, rules files, vector memory, plain notes, and RAG plugins.
- Added a Mermaid architecture diagram for the pipeline, governance, recall, and maintenance loop.
- Synced the same positioning to the Chinese README.

## 0.4.1 - 2026-06-01

- Removed the stale project-area metadata field from public metadata standards and templates.
- Added English agent-facing instructions to `AGENTS.md` and `00-Agent-Governance/README.md`.
- Clarified that filled examples are read-only and real projects live under `10-Projects/`.
- Replaced Inbox child placeholder README files with `.gitkeep` files and clarified Inbox routing.
- Clarified the `intake-source` promotion path from source card to project state, shared asset, or recall map.
- Added an English quick index for Shared Assets files with Chinese filenames.

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

- Initial private release of Obsidian AI Workflow Kit.
- Added startup entry, project bridge card, templates, source triage, shared assets, and bilingual README files.

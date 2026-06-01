# Changelog

## 0.6.5 - 2026-06-02

- Added local adapter protection via `.obsidian-ai-workflow-kit/adoption-policy.json`.
- `install-core` and `upgrade-core` now refuse to write into protected adapter vaults unless explicitly overridden.
- Documented how a working vault can consume the public kit as architecture authority without becoming a managed kit install.

## 0.6.4 - 2026-06-02

- Clarified the three-place responsibility model: public kit as architecture authority, working vault as live work record, and private backup remote as backup only.
- Updated the maintainer source sync policy to forbid treating private backups as public-kit upstream sources.

## 0.6.3 - 2026-06-02

- Added a managed install manifest at `.obsidian-ai-workflow-kit/manifest.json`.
- Added `scripts/kb.py upgrade-core` for safer updates after installation.
- Added `install.sh --update` so users can pull newer GitHub versions with the same one-line installer.
- Documented the update flow and the private-vault/public-kit sync policy.

## 0.6.2 - 2026-06-02

- Added `03-Recall-System/example-recall-chain.md` to show how a reusable lesson is recalled by a future task.
- Added agent rules for warning users when project bridge cards are missing `updated` dates or have gone stale.
- Made `stale-check` recommendations more actionable by naming the bridge-card fields and project files to update.
- Clarified in README that recall is based on task routing and recall fields, not whole-vault scanning.

## 0.6.1 - 2026-06-02

- Moved maintainer-facing files out of the repository root:
  - `MIGRATION.md` -> `docs/migration.md`
  - `CONTENT-LICENSE.md` -> `docs/legal/content-license.md`
  - `NOTICE.md` -> `docs/legal/notice.md`
  - `OPEN-SOURCE-CHECKLIST.md` -> `docs/release/open-source-checklist.md`
  - `RELEASE_CHECKLIST.md` -> `docs/release/release-checklist.md`
- Added a 30-second demo guide in English and Chinese.
- Updated README demo instructions so new users can understand what “Open folder as vault” means.
- Collapsed same-day beta iteration notes into one historical section to keep this changelog readable.

## 0.6.0 - 2026-06-01

- Replaced Codex-specific default bridge naming with agent-neutral `BRIDGE-*.md` and `project-bridge`.
- Renamed core templates and shared modules to English filenames while preserving Chinese titles and aliases.
- Kept legacy `CODEX-BRIDGE-*.md` compatibility in stale checks and project bridge coverage checks.
- Added `scripts/kb.py migrate-codex-names` to rename old Codex-specific files and update Markdown references.
- Added migration guidance and alias tables for users upgrading older vaults.

## 0.1.0 to 0.5.8 - 2026-06-01

These were rapid beta iterations during the first public-release preparation window. They are grouped here so the changelog reflects the project history without implying separate release days.

- Created the initial Obsidian AI Workflow Kit with startup entry, project bridge cards, templates, source triage, shared assets, and bilingual README files.
- Flattened the early structure, removed thin placeholder layers, added `index.md`, `MIGRATION.md`, repository versioning, and a filled project example.
- Added the agent governance layer, knowledge pipeline, recall system, maintenance loop, and source-to-knowledge example.
- Added `scripts/kb.py` commands for `health-check`, `new-project`, `install-core`, `intake-source`, `intake-folder`, `audit-vault`, and `stale-check`.
- Added `install.sh` for one-line installation, plus full and barebone install modes.
- Added CI, Python tests, install/tool test scripts, release checklist, 10-minute guides, before/after case, concept docs, template docs, and automation docs.
- Renamed the project to Obsidian AI Workflow Kit and updated repository URLs, description, topics, README copy, and installer links.
- Split code licensing and content licensing, keeping root `LICENSE` as MIT and written content under CC BY 4.0.
- Replaced the README architecture diagram with `docs/images/architecture-flow.png`.
- Added incident-experience handling and Claude Code Stop hook examples.
- Simplified README into a GitHub homepage and moved deeper explanation into `docs/`.

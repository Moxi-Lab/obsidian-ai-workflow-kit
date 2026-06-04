# Language and Preset Install Design

## Conclusion

The next useful install feature is language plus recommended configuration selection.

The kit should keep GitHub as the source of truth for files, templates, and rules. A future Obsidian plugin should only provide a friendlier install wizard that passes the chosen language and preset to the existing installer.

## Completion Standard

- Installer supports exactly two languages: `zh-CN` and `en`.
- Installer supports a small fixed preset list.
- Presets do not replace install modes and do not introduce `barebone` or `full` decisions in the UI.
- Dry-run shows the language, preset, and files that would be written.
- Existing files are skipped unless the existing overwrite flag is used.
- Managed manifest records the selected language and preset.
- Tests cover valid options, invalid options, dry-run output, and manifest fields.

## Scope

In scope:

- Add `--language zh-CN|en` to `install.sh`, `install-core`, and `upgrade-core`.
- Add `--preset personal|agent-projects|research|content` to `install.sh`, `install-core`, and `upgrade-core`.
- Add language-specific starter files where user-facing body text differs.
- Add preset-specific starter defaults for prompts, example project text, and recommended folder guidance.
- Keep the existing safe update behavior.
- Prepare the command shape that a future Obsidian plugin can call.

Out of scope:

- Bilingual installs.
- New install modes.
- Cloud sync.
- RAG or search backend.
- Automatic rewriting of an existing vault.
- A full plugin implementation in this change.

## Options Considered

### Recommended: Installer First, Plugin Later

Add language and preset choices to the current installer first. The plugin becomes a thin UI later.

Pros:

- Smallest change.
- Easy to test from the command line.
- Keeps content in one source of truth.
- Avoids maintaining separate plugin-bundled copies.

Cons:

- First release still uses command line unless a plugin is added later.

### Plugin First

Build an Obsidian plugin that contains the selection UI and writes files directly.

Pros:

- Better first-use experience.
- Easier for non-technical Obsidian users.

Cons:

- Higher maintenance cost.
- Easy to create two competing install paths.
- Harder to test safely across vaults.

### Documentation Only

Keep the installer unchanged and document which files users should copy for each language or preset.

Pros:

- Very low implementation cost.

Cons:

- Does not solve the installation friction.
- Easy for users to copy inconsistent file sets.

## Recommended Design

### Language

Supported values:

- `zh-CN`
- `en`

No bilingual output is supported.

Language affects user-facing installed content:

- startup instruction text
- governance rule body text
- template body text
- example project text
- README or local index text when installed

Stable paths should stay English where possible so AI agents can locate files consistently across languages.

### Presets

Supported values:

- `personal`
- `agent-projects`
- `research`
- `content`

Presets affect starter defaults, not install size.

Preset behavior:

- `personal`: general notes, long-term memory, daily reference, light project tracking.
- `agent-projects`: project bridge cards, current state, decisions, handoff, reusable lessons.
- `research`: external sources, reading notes, source analysis, topic maps.
- `content`: ideas, materials, drafts, publishing review, reusable content lessons.

### Installer Contract

Command examples:

```bash
bash install.sh --language zh-CN --preset agent-projects --dry-run "/path/to/vault"
bash install.sh --language en --preset research "/path/to/vault"
```

The Python commands should accept the same options:

```bash
python3 00-AI/scripts/kb.py install-core "/path/to/vault" --language zh-CN --preset agent-projects --dry-run
python3 00-AI/scripts/kb.py upgrade-core "/path/to/vault" --language en --preset research --dry-run
```

Default values:

- `language`: `en`
- `preset`: `agent-projects`

### File Organization

Use one canonical path for installed files. Source variants can live in kit-only directories, but installed target paths should remain stable.

Proposed source layout:

```text
00-AI/i18n/zh-CN/
00-AI/i18n/en/
00-AI/presets/personal/
00-AI/presets/agent-projects/
00-AI/presets/research/
00-AI/presets/content/
```

The installer resolves the selected language and preset into the normal installed paths.

### Manifest

The managed manifest should include:

```json
{
  "language": "zh-CN",
  "preset": "agent-projects"
}
```

On upgrade, the installer should default to the manifest values when the user does not pass new values.

### Obsidian Plugin Boundary

A later plugin should only provide:

- language selector
- preset selector
- target vault confirmation
- dry-run preview
- install button
- health-check button

The plugin should not maintain a separate copy of the kit content. It should download or call the same release source used by the command-line installer.

## Error Handling

- Unknown language exits with a clear message listing valid values.
- Unknown preset exits with a clear message listing valid values.
- Missing language files fail before writing.
- Missing preset files fail before writing.
- Existing files continue to be skipped unless overwrite is explicit.
- Protected local adapters still refuse writes unless the existing override flag is used.

## Testing

Required checks:

- `install.sh --language zh-CN --preset agent-projects --dry-run`
- `install.sh --language en --preset research --dry-run`
- invalid language fails
- invalid preset fails
- `install-core` writes manifest language and preset
- `upgrade-core` reuses manifest language and preset when omitted
- health check passes after installing each language with at least one preset

## Open Decisions

- The first version uses exactly four presets: `personal`, `agent-projects`, `research`, and `content`.
- The default language is `en` because the public GitHub landing page is English-first. Chinese users can explicitly choose `zh-CN`.

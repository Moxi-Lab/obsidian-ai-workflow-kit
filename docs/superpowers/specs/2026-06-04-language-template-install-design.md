# Language Template Install Design

## Conclusion

The next install feature should stay minimal: choose a vault path, choose one language, then create the default kit directory structure.

There are no recommended configuration presets in this version.

## Completion Standard

- Installer accepts a target vault path.
- Installer supports exactly two languages: `zh-CN` and `en`.
- Installer creates one default template structure for the selected language.
- Dry-run shows the selected vault path, selected language, and files that would be created.
- Existing files are skipped unless the existing overwrite flag is used.
- Managed manifest records the selected language.
- Tests cover valid language choices, invalid language choices, dry-run output, existing-file skip behavior, and manifest language.

## Scope

In scope:

- Add `--language zh-CN|en` to `install.sh`, `install-core`, and `upgrade-core`.
- Keep one default directory/template set.
- Add language-specific source files only where user-facing body text differs.
- Keep stable installed paths so AI agents can locate the same files in either language.
- Keep the existing safe update behavior.
- Prepare the command shape that a future Obsidian plugin can call.

Out of scope:

- Recommended configuration presets.
- Bilingual installs.
- New install modes.
- Cloud sync.
- RAG or search backend.
- Automatic rewriting of an existing vault.
- A full plugin implementation in this change.

## Options Considered

### Recommended: Installer First, Plugin Later

Add language selection to the current installer first. A future Obsidian plugin becomes a thin UI for choosing the vault path and language.

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

Keep the installer unchanged and document which language files users should copy.

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
- example text
- README or local index text when installed

Stable paths should stay English where possible so AI agents can locate files consistently across languages.

### Default Template

The first version installs one default kit template.

The template should create the normal AI workflow structure:

```text
00-AI/START-HERE.md
00-AI/AGENTS.md
00-AI/governance/
00-AI/pipeline/
00-AI/recall/
00-AI/templates/
10-Projects/
20-SharedAssets/
40-ExternalSources/
```

The directory structure does not change by language. Only user-facing file content changes.

### Installer Contract

Command examples:

```bash
bash install.sh --language zh-CN --dry-run "/path/to/vault"
bash install.sh --language en "/path/to/vault"
```

The Python commands should accept the same option:

```bash
python3 00-AI/scripts/kb.py install-core "/path/to/vault" --language zh-CN --dry-run
python3 00-AI/scripts/kb.py upgrade-core "/path/to/vault" --language en --dry-run
```

Default value:

- `language`: `en`

### File Organization

Use one canonical path for installed files. Source variants can live in kit-only directories, but installed target paths should remain stable.

Proposed source layout:

```text
00-AI/i18n/zh-CN/
00-AI/i18n/en/
```

The installer resolves the selected language into the normal installed paths.

### Manifest

The managed manifest should include:

```json
{
  "language": "zh-CN"
}
```

On upgrade, the installer should default to the manifest language when the user does not pass a new language.

### Obsidian Plugin Boundary

A later plugin should only provide:

- vault path selector
- language selector
- dry-run preview
- install button
- health-check button

The plugin should not maintain a separate copy of the kit content. It should download or call the same release source used by the command-line installer.

## Error Handling

- Unknown language exits with a clear message listing valid values.
- Missing language files fail before writing.
- Existing files continue to be skipped unless overwrite is explicit.
- Protected local adapters still refuse writes unless the existing override flag is used.

## Testing

Required checks:

- `install.sh --language zh-CN --dry-run`
- `install.sh --language en --dry-run`
- invalid language fails
- `install-core` writes manifest language
- `upgrade-core` reuses manifest language when omitted
- health check passes after installing each language

## Decisions

- The first version has no recommended configuration presets.
- The first version has no bilingual install.
- The default language is `en` because the public GitHub landing page is English-first. Chinese users can explicitly choose `zh-CN`.

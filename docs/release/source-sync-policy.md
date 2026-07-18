# Source Sync Policy

This file is for maintainers. It prevents the public kit, a working vault, and a private backup remote from drifting into mixed responsibilities.

Core rule: **the public kit is the reusable-core authority, the working vault is the live work record plus local extensions, and a private backup remote is only a backup.**

## Source Roles

| Source | Owns | Does not own |
|---|---|---|
| Public kit | Reusable architecture, generic templates, shared rules, scripts, public examples, release docs | Private project state, raw handoffs, personal context, backup duties |
| Working vault | Real project memory, private project state, user preferences, incidents, next actions, explicitly local extensions | Public distribution, duplicate maintenance of shared-core files, installer UX |
| Private backup remote | Backup and restore point for a working vault | Architecture authority, public upstream, manual rule maintenance |

A private backup remote must not be treated as an upstream source for this kit. If a reusable pattern is found in a backup, inspect it in the working vault, remove private context, and write the public version here.

## Allowed From A Working Vault To This Kit

- Stable startup rules.
- Generic project bridge structure.
- Generic write-back rules.
- Recall fields and tagging guidance.
- Lesson promotion patterns.
- Incident lesson patterns.
- Vault health checks.
- Sanitized examples.
- Scripts that do not depend on private paths or private projects.

## Never Copy Into This Kit

- Real project state or next actions.
- User preferences, identities, contacts, or personal notes.
- Private paths, private repositories, private task boards.
- Raw handoffs, full chat logs, raw web clips, or third-party source text.
- Trading, financial, customer, credential, or operational details from a private project.
- Secrets, tokens, cookies, API keys, passwords, verification codes, or private keys.
- Unverified working notes.

## Managed Shared Core

An established working vault may opt into the `shared-core` profile. Its adoption policy must use `mode: managed-core`, set `allow_public_kit_writes: true`, and list only `shared-core` in `allowed_install_modes`.

The shared-core profile owns reusable system files only. It must never own or overwrite the working vault's startup entry, Inbox, projects, archives, private context, or root documents. Working-vault customizations belong in clearly named local-extension paths rather than edits to managed files.

Preview every update first:

```bash
python3 00-AI/scripts/kb.py upgrade-core "/path/to/working-vault" --mode shared-core --language zh-CN --dry-run
```

After review, run the same command without `--dry-run`. Re-running an unchanged version must produce zero updated files and zero conflicts.

In `shared-core` mode, the public health check validates only required shared paths, the managed manifest and file hashes, and shared Base structure. The working vault must keep its own independent health check for private projects, Inbox, archives, and local extensions.

## Allowed From This Kit Back To A Working Vault

- Clearer generic naming.
- Better template fields.
- Safer check scripts.
- Install, health-check, audit, and stale-check improvements.
- External feedback that has been verified.
- Recall-chain improvements that help AI agents take over complex work.

## Do Not Push Back Blindly

- Simplified public folder structures.
- Public demo content.
- English-first wording that weakens a private vault's existing local conventions.
- Agent-neutral naming changes that would break older private links.
- Documentation cuts made only for public onboarding.

## Maintainer Checklist

Before promoting a change between a working vault and this kit:

- [ ] The change is a reusable pattern, not private content.
- [ ] Public files contain no private paths, project states, handoff history, or secrets.
- [ ] Working-vault private state and local extensions are outside the managed shared-core boundary.
- [ ] Shared-core files are changed only in the public kit, then imported through the managed manifest.
- [ ] This kit passes the relevant release checks.
- [ ] The working vault records the public version or imported rule in its own project bridge card.

## Release Note Rule

When a release is based on a pattern from a working vault, describe the public behavior only. Do not mention the private project, private path, or private incident that produced the pattern.

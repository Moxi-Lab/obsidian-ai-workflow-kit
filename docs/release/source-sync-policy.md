# Source Sync Policy

This file is for maintainers. It prevents a working vault and the public kit from drifting into two unrelated systems.

Core rule: **do not mirror vaults. Promote reusable patterns.**

## Source Roles

| Source | Owns | Does not own |
|---|---|---|
| Working vault | Real project memory, private project state, user preferences, incidents, next actions | Public distribution, generic examples, installer UX |
| Public kit | Reusable structure, generic templates, public examples, scripts, release docs | Private project state, raw handoffs, personal context |

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
- [ ] Working-vault rules are not overwritten by simplified public docs.
- [ ] Both sides use their own naming and reader context when both need updates.
- [ ] This kit passes the relevant release checks.
- [ ] The working vault records the public version or imported rule in its own project bridge card.

## Release Note Rule

When a release is based on a pattern from a working vault, describe the public behavior only. Do not mention the private project, private path, or private incident that produced the pattern.

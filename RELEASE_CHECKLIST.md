# Release Checklist

Use this checklist before switching the repository public or announcing a release.

## Required Checks

- [ ] Repository visibility decision is intentional.
- [ ] `README.md` explains who this is for, who it is not for, and current maturity.
- [ ] One-line installer has been tested from a clean environment.
- [ ] `python3 scripts/kb.py health-check` passes.
- [ ] `bash scripts/test_install.sh` passes.
- [ ] `bash scripts/test_tools.sh` passes.
- [ ] GitHub Actions CI passes on `main`.
- [ ] `VERSION` matches the intended release tag.
- [ ] `CHANGELOG.md` has an entry for the release.
- [ ] Root `LICENSE` is standard MIT and `CONTENT-LICENSE.md` explains CC BY 4.0 content licensing.

## Beta Trial Checks

- [ ] Install into at least one empty test vault.
- [ ] Install into at least one existing Obsidian vault with `--dry-run` first.
- [ ] Create one project bridge card using `new-project`.
- [ ] Create one folder intake using `intake-folder`.
- [ ] Run `audit-vault --write-report`.
- [ ] Ask an AI agent to read `START-HERE.md` and confirm it returns the expected startup receipt.

## Public Release Checks

- [ ] Repository is public.
- [ ] Raw GitHub installer URL works without authentication.
- [ ] Release is tagged and marked as prerelease if still in beta.
- [ ] README install command has been tested after the visibility change.
- [ ] No private paths, secrets, personal notes, source clips, or private handoff history are included.

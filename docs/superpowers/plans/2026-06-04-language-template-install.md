# Language Template Install Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add language selection to the existing installer so users can choose a vault path and either `zh-CN` or `en`, then install the same default directory structure with language-specific starter content.

**Architecture:** Keep the existing install and upgrade flow. Add a small language resolution layer in `00-AI/scripts/kb/config.py` and use it from `00-AI/scripts/kb/install.py` when selecting source files. `install.sh` only parses and forwards `--language`.

**Tech Stack:** Python standard library, Bash, `unittest`, existing shell verification scripts.

---

### Task 1: Add Failing Language Install Tests

**Files:**
- Modify: `tests/test_kb.py`

- [ ] **Step 1: Write failing tests**

Add tests that install `zh-CN` and `en`, verify different `00-AI/START-HERE.md` content, verify manifest `language`, verify invalid language fails, and verify upgrade reuses manifest language when omitted.

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
python3 -m unittest tests.test_kb.InstallLanguageTests -v
```

Expected: fail because language helpers and language args do not exist yet.

### Task 2: Add Language Resolution and Overlay Sources

**Files:**
- Modify: `00-AI/scripts/kb/config.py`
- Modify: `00-AI/scripts/kb/install.py`
- Create: `00-AI/i18n/en/00-AI/START-HERE.md`
- Create: `00-AI/i18n/zh-CN/00-AI/START-HERE.md`
- Create: `00-AI/i18n/en/index.md`
- Create: `00-AI/i18n/zh-CN/index.md`

- [ ] **Step 1: Implement language constants and validation**

Add valid languages `en` and `zh-CN`, default `en`, and helper functions for validation and manifest fallback.

- [ ] **Step 2: Implement language-aware file selection**

When copying a file, prefer `00-AI/i18n/<language>/<relative-path>` if it exists; otherwise use the base source file.

- [ ] **Step 3: Add starter language variants**

Add language-specific `00-AI/START-HERE.md` and `index.md` files. Keep installed target paths stable.

- [ ] **Step 4: Run tests to verify GREEN**

Run:

```bash
python3 -m unittest tests.test_kb.InstallLanguageTests -v
```

Expected: pass.

### Task 3: Wire CLI and Bash Installer

**Files:**
- Modify: `00-AI/scripts/kb/cli.py`
- Modify: `install.sh`
- Modify: `00-AI/scripts/test_install.sh`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

- [ ] **Step 1: Add CLI options**

Add `--language en|zh-CN` to `install-core` and `upgrade-core`.

- [ ] **Step 2: Add Bash option parsing**

Add `--language en|zh-CN` to `install.sh`, validate it, and forward it to Python.

- [ ] **Step 3: Update docs and shell checks**

Show language examples in README files and add shell checks for both languages.

- [ ] **Step 4: Run targeted checks**

Run:

```bash
python3 -m unittest tests.test_kb.InstallLanguageTests -v
bash 00-AI/scripts/test_install.sh
```

Expected: both pass.

### Task 4: Full Verification

**Files:**
- No new files expected.

- [ ] **Step 1: Run unit tests**

```bash
python3 -m unittest tests/test_kb.py
```

Expected: all tests pass.

- [ ] **Step 2: Run shell tests**

```bash
bash 00-AI/scripts/test_install.sh
bash 00-AI/scripts/test_tools.sh
```

Expected: both scripts exit 0.

- [ ] **Step 3: Run repository checks**

```bash
python3 00-AI/scripts/kb.py health-check
python3 00-AI/scripts/kb.py stale-check --vault . --fail-on-findings
python3 -m py_compile 00-AI/scripts/kb.py 00-AI/scripts/kb/*.py
git diff --check
```

Expected: all commands exit 0.

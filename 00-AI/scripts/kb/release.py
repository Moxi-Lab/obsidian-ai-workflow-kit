from __future__ import annotations

import argparse
import io
import json
import tempfile
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

from .config import VALID_LANGUAGES, language_target_path
from .health import check_private_user_paths, health_check
from .install import install_core, read_kit_version
from .utils import repo_root


CORE_PLUGINS = [
    "file-explorer",
    "global-search",
    "switcher",
    "graph",
    "backlink",
    "canvas",
    "outgoing-link",
    "tag-pane",
    "page-preview",
    "daily-notes",
    "templates",
    "note-composer",
    "command-palette",
    "editor-status",
    "bookmarks",
    "outline",
    "word-count",
    "file-recovery",
    "bases",
]


def write_safe_obsidian_config(vault: Path, language: str) -> None:
    config = vault / ".obsidian"
    config.mkdir(parents=True, exist_ok=True)
    (config / "core-plugins.json").write_text(
        json.dumps(CORE_PLUGINS, indent=2) + "\n",
        encoding="utf-8",
    )
    (config / "community-plugins.json").write_text("[]\n", encoding="utf-8")
    template_folder = language_target_path(language, "00-AI/templates").as_posix()
    (config / "templates.json").write_text(
        json.dumps(
            {"folder": template_folder, "dateFormat": "YYYY-MM-DD", "timeFormat": "HH:mm"},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def write_download_start(vault: Path, language: str, mode: str) -> None:
    if language == "zh-CN":
        start_path = language_target_path(language, "00-AI/START-HERE.md").as_posix()
        home_path = language_target_path(language, "index.md").as_posix()
        text = f"""# 下载后从这里开始

1. 在 Obsidian 中选择“打开文件夹作为仓库”，并选择当前文件夹。
2. 人类入口：`{home_path}`。
3. 把下面这句话发给 Codex 或其他可读取本地文件的 AI Agent：

```text
请读取当前 vault 的 {start_path}，并接手这个任务：<你的任务>
```

安装模式：`{mode}`。当前对话能完成的任务直接执行；只有排队、跨会话或阻塞时才创建本地任务卡。
"""
    else:
        text = f"""# Start After Download

1. In Obsidian, choose **Open folder as vault** and select this folder.
2. Human entry: `index.md`.
3. Send this instruction to Codex or another local-file AI agent:

```text
Read 00-AI/START-HERE.md in this vault and take over this task: <your task>
```

Install mode: `{mode}`. Execute directly when the current conversation can finish the task; create a local task card only for queued, cross-session, or blocked work.
"""
    (vault / "START.md").write_text(text, encoding="utf-8")


def zip_vault(vault: Path, archive: Path) -> None:
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(item for item in vault.rglob("*") if item.is_file()):
            arcname = Path(vault.name) / path.relative_to(vault)
            bundle.write(path, arcname.as_posix())


def build_release(args: argparse.Namespace) -> int:
    source_root = repo_root()
    version = read_kit_version(source_root)
    if version == "unknown":
        raise SystemExit("cannot build release without VERSION")
    output = Path(args.output).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    languages = VALID_LANGUAGES if args.language == "all" else (args.language,)
    modes = ("barebone", "full") if args.mode == "all" else (args.mode,)

    built = []
    for language in languages:
        for mode in modes:
            package_name = f"obsidian-ai-workflow-kit-v{version}-{language}-{mode}"
            archive = output / f"{package_name}.zip"
            with tempfile.TemporaryDirectory() as tmp:
                vault = Path(tmp) / package_name
                install_args = argparse.Namespace(
                    target=str(vault),
                    mode=mode,
                    language=language,
                    overwrite=False,
                    dry_run=False,
                    allow_protected_adapter_write=False,
                )
                with redirect_stdout(io.StringIO()):
                    install_core(install_args)
                write_download_start(vault, language, mode)
                if mode == "full":
                    write_safe_obsidian_config(vault, language)
                health_args = argparse.Namespace(vault=str(vault), mode=mode)
                health_output = io.StringIO()
                with redirect_stdout(health_output):
                    result = health_check(health_args)
                if result:
                    raise SystemExit(
                        f"release candidate failed health-check: {language}/{mode}\n"
                        f"{health_output.getvalue()}"
                    )
                privacy_errors = check_private_user_paths(vault)
                if privacy_errors:
                    raise SystemExit(
                        f"release candidate contains private-looking paths: {language}/{mode}\n"
                        + "\n".join(privacy_errors)
                    )
                zip_vault(vault, archive)
            built.append(archive)
            print(f"built {archive}")

    print(f"summary: {len(built)} release archives built for v{version}")
    return 0

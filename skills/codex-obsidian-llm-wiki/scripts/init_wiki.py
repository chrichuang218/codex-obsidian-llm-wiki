#!/usr/bin/env python3
"""Initialize an Obsidian-compatible Markdown LLM Wiki."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path


DIRS = [
    "raw/articles",
    "raw/notes",
    "raw/pdfs",
    "raw/assets",
    "wiki/sources",
    "wiki/topics",
    "wiki/entities",
    "wiki/comparisons",
    "wiki/synthesis",
    "wiki/queries",
    "wiki/review",
]


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def init_wiki(root: Path, topic: str) -> None:
    today = date.today().isoformat()
    root.mkdir(parents=True, exist_ok=True)
    for item in DIRS:
        (root / item).mkdir(parents=True, exist_ok=True)

    write_if_missing(root / ".gitignore", ".wiki-tmp/\n")
    write_if_missing(root / ".wiki-cache.json", json.dumps({"version": 1, "entries": {}}, ensure_ascii=False, indent=2) + "\n")
    write_if_missing(
        root / "purpose.md",
        f"""# 研究目的与方向

## 核心目标

围绕「{topic}」构建一个中文优先、Obsidian 兼容、可持续维护的 Markdown LLM Wiki。

## 关键问题

1. 这个知识库最需要回答什么问题？
2. 哪些素材应该进入长期知识？
3. 哪些问题需要进入 review 队列？

## 研究范围

**涵盖：** {topic}

**不涵盖：** 与主题无关、未脱敏或无法追溯来源的内容。
""",
    )
    write_if_missing(
        root / ".wiki-schema.md",
        f"""# Wiki Schema

- 主题：{topic}
- 创建日期：{today}
- 语言：简体中文为主，关键术语保留英文

## 目录

- `raw/`：原始素材，只读
- `wiki/sources/`：素材摘要
- `wiki/topics/`：主题页
- `wiki/entities/`：实体页
- `wiki/comparisons/`：对比分析
- `wiki/synthesis/`：综合分析
- `wiki/queries/`：查询结果
- `wiki/review/`：人工复核队列

## 规则

- 先分析，再写入。
- 每个重要结论必须能追到 `wiki/sources/` 或 `raw/`。
- 不确定内容进入 `wiki/review/`。
- 每次操作更新 `index.md` 和 `log.md`。
""",
    )
    write_if_missing(
        root / "index.md",
        f"""# 知识库索引

> 最后更新：{today}

## 概览

- 主题：{topic}
- 素材总数：0
- Wiki 页面总数：0

## 素材摘要

（暂无）

## 主题页

（暂无）

## 实体页

（暂无）

## Review

（暂无）
""",
    )
    write_if_missing(
        root / "log.md",
        f"""# 操作日志

## {today} init

- 初始化知识库：{topic}
""",
    )
    write_if_missing(
        root / "wiki/overview.md",
        f"""# {topic} — 总览

> 这个页面记录知识库全貌。

## 知识地图

（随着素材积累更新）
""",
    )
    print(f"Initialized wiki at {root}")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: init_wiki.py <wiki-root> [topic]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).expanduser().resolve()
    topic = sys.argv[2] if len(sys.argv) > 2 else "我的知识库"
    init_wiki(root, topic)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


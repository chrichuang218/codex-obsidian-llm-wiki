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
        root / "AGENTS.md",
        """# AGENTS.md

## 项目定位

本仓库是一个中文优先、兼容 Obsidian 的 Markdown LLM Wiki，由 Codex 通过 `codex-obsidian-llm-wiki` 工作流维护。

## 必读上下文

执行任何 `init`、`ingest`、`batch`、`query`、`lint`、`graph` 或 `review` 操作前，先读取：

- `.wiki-schema.md`：schema、语言、目录规则和别名词表
- `purpose.md`：研究目标和范围
- `index.md`：当前目录索引

## 语言

默认用简体中文输出和写入 wiki；关键名称、工具名、协议名、配置字段和核心概念保留英文。

## 工作风格

- 先读真实上下文，再修改。
- 能合理假设就继续，高风险或不可逆操作再询问。
- 优先做最小可验证改动，不做无关扩展。
- 先给结论或结果，再补必要上下文。

## Agent 工作边界

- 回答必须基于当前 wiki 内容和可追溯来源，不用通用记忆替代检索。
- 重要结论必须能追到 `wiki/sources/` 或 `raw/`。
- 不确定内容进入 `wiki/review/`，不要强行写成事实。
- 不创建重复页面；遇到重名、歧义或冲突时先查现有页面。
- 不把短期任务细节写进长期规则或主题页。

## 执行规则

- 修改前先读相关文件。
- 改动保持最小闭环。
- 不修改无关文件。
- 不覆盖用户已有未提交改动，不重写 `raw/` 原始素材。
- 禁止使用 `git reset --hard`，除非用户明确要求。

## Wiki 规则

- Wiki 操作使用已安装的 `codex-obsidian-llm-wiki` skill。
- `raw/` 作为原始素材目录，保持不可变。
- 生成的知识写入 `wiki/`。
- 素材摘要写入 `wiki/sources/`。
- 主题页写入 `wiki/topics/`。
- 实体、工具、协议、组件和独立概念写入 `wiki/entities/`。
- 可长期保留的查询答案写入 `wiki/queries/`。
- 不确定结论、冲突信息、歧义命名或隐私风险写入 `wiki/review/`。
- 完成有意义的 ingest 或 compile 操作后，更新 `index.md`、`.wiki-cache.json` 和 `log.md`。

## 验证

- Wiki 改动优先运行或参考 `cow lint` / `lint_wiki.py` 的检查规则。
- 检查新增或修改页面是否已被 `index.md` 收录。
- 检查重要结论是否能追溯到 `wiki/sources/` 或 `raw/`。
- 能跑就跑；不能跑要说明原因。
- 不把静态阅读包装成运行时验证。

## 安全

- 不 ingest 或写入 secret、token、API key、cookie、手机号或其他敏感个人信息。
- 发现疑似敏感信息时，停止写入并提醒用户。
""",
    )
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

# Codex Obsidian LLM Wiki

一个中文优先的 Codex skill，用来构建 Obsidian 兼容的 Markdown LLM Wiki。

不需要桌面客户端，不绑定数据库。核心组合是：

```text
Codex + Skill + Obsidian + Markdown
```

## 适合谁

适合想要下面这种工作流的人：

- 用 Codex 消化文章、PDF、debug 笔记和项目文档。
- 用 Obsidian 浏览、搜索、改错和看双链图谱。
- 所有知识都保存成普通 Markdown。
- 不想额外使用独立知识库客户端。

## 安装

直接让 Codex 安装：

```text
安装这个 skill：
https://github.com/chrichuang218/codex-obsidian-llm-wiki/tree/main/skills/codex-obsidian-llm-wiki
```

或使用 Codex 通用 skill 安装器：

```powershell
python $env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py --repo chrichuang218/codex-obsidian-llm-wiki --path skills/codex-obsidian-llm-wiki
```

安装后重启 Codex。

## 快速开始

初始化知识库：

```text
用 codex-obsidian-llm-wiki 初始化一个知识库到 D:\Wiki\my-wiki
```

整理资料：

```text
把 D:\Notes\debug-crash.md 整理进 D:\Wiki\my-wiki 知识库
```

查询知识库：

```text
基于 D:\Wiki\my-wiki 知识库回答：AIDL hidden API crash 是什么？
```

健康检查：

```text
检查 D:\Wiki\my-wiki 知识库健康状态，并修复确定的问题
```

## 指令速查

自然语言可以用，但明确指令更好记：

```text
/cow:init D:\Wiki\my-wiki "我的知识库"
/cow:ingest D:\Notes\debug-crash.md D:\Wiki\my-wiki
/cow:batch D:\Wiki\my-wiki
/cow:query D:\Wiki\my-wiki "AIDL hidden API crash 是什么？"
/cow:lint D:\Wiki\my-wiki
/cow:graph D:\Wiki\my-wiki
/cow:review D:\Wiki\my-wiki
/cow:help
```

`cow` 是 **Codex Obsidian Wiki** 的缩写。

## 目录结构

```text
my-wiki/
├── raw/                 原始素材，只读
├── wiki/
│   ├── sources/         素材摘要
│   ├── topics/          主题页
│   ├── entities/        实体页
│   ├── comparisons/     对比分析
│   ├── synthesis/       综合分析
│   ├── queries/         查询结果
│   └── review/          人工复核队列
├── index.md             总索引
├── purpose.md           研究目标
├── .wiki-schema.md      维护规则
├── .wiki-cache.json     去重缓存
└── log.md               操作日志
```

## 设计原则

- 中文优先，关键术语保留英文。
- 先分析，再写入，避免边读边乱建页面。
- 每个重要结论都要能追到 `wiki/sources/` 或 `raw/`。
- 不确定内容进入 `wiki/review/`，不强行写死。
- Obsidian 只做前端，Markdown 才是数据。

## License

MIT

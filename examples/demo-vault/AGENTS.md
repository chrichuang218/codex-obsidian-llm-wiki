# AGENTS.md

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

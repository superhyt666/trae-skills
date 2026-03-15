# 更新日志

本文档记录 hy-skill 的所有重要更改。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增
- 优化 SKILL.md 元数据结构，添加 version、author、license、allowed-tools、files 字段
- 新增工作流文档阅读与修改模块
- 新增 references/workflow-document-guide.md - 工作流文档阅读与修改指南
- 添加 CHANGELOG.md 版本历史记录
- 添加自动提升规则说明

### 变更
- **重要**：重构 `references/workflow-nodes-knowledge.md`，详细区分文档知识检索与知识检索节点
  - 新增文档知识检索 (DOCUMENT_KNOWLEDGE_SEARCH) 详细配置说明
  - 新增知识检索 (KNOWLEDGE_SEARCH) 详细配置说明
  - 新增组合使用模式和 JSON 配置示例
- 优化工作流文档节点配置说明，提供完整的 JSON 格式示例

### 修复
- 修正工作流文档中节点命名不准确的问题（知识片段检索 → 知识检索）
- 修正并行处理滥用问题，移除无意义的并行分支

## [1.1.0] - 2026-03-14

### 新增
- 新增工作流文档阅读与修改模块
- 新增 references/workflow-document-guide.md 参考文档

## [1.0.0] - 2026-03-12

### 新增
- 初始版本发布
- Python 代码生成模块
- 工作流搭建模块
- Agent 提示词设计模块
- 工作流识别模块

---

## 参考文档

- references/python-standards.md - Python 代码生成详细规范
- references/workflow-setup.md - 工作流搭建指南
- references/workflow-node-variable-mapping.md - 节点变量类型映射表
- references/agent-prompts.md - Agent 提示词设计指南
- references/agent-examples.md - Agent 配置示例库
- references/workflow-recognition.md - 工作流识别参考文档
- references/workflow-document-guide.md - 工作流文档阅读与修改指南
- references/design-philosophy.md - 设计哲学（任务拆解原则）
- references/retrieval-augmented-pattern.md - 检索增强模式
- references/template-lookup-pattern.md - 模板化+查表法
- references/keywords.md - 关键字映射表
- references/workflow-nodes-calling.md - 调用类节点
- references/workflow-nodes-control.md - 流程控制节点
- references/workflow-nodes-ai.md - AI 能力节点
- references/workflow-nodes-knowledge.md - 知识管理节点
- references/workflow-nodes-table.md - 智能表格节点
- references/workflow-nodes-text.md - 文本处理节点

---

*最后更新：2026-03-14*

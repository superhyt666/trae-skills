# 💡 功能请求 (FEATURE_REQUESTS.md)

记录用户请求的新功能或能力。

---

## [FEAT-20260315-001] user_feedback
**Logged**: 2026-03-15T02:00:00Z
**Priority**: high
**Status**: resolved
**Complexity**: medium

### Capability
flow-to-markdown 技能解析工作流时必须包含详细的输入输出配置

### Description
用户反馈工作流解析文档缺少节点间变量传递的详细信息：
- 无法看到输入参数来自哪个变量
- 无法看到输出参数传递到哪个变量
- 子工作流节点的输出参数没有正确解析

需要：
1. 变量 ID 映射表（含 ID、名称、类型）
2. 节点输入参数表（含来源变量）
3. 节点输出参数表（含输出目标）
4. 子工作流特殊处理（outputParametersByNode 字段解析）

### User Scenario
用户分析工作流文档时，能够清晰看到每个节点的数据流向，便于：
- 理解变量传递关系
- 定位配置问题
- 优化工作流结构

### Implementation
已更新：
1. flow-to-markdown/SKILL.md - 添加详细的解析规范
2. convert_flow.py - 重写解析逻辑，支持：
   - 变量引用解析（`{{变量ID}}` → `变量名称(变量ID)`）
   - 子工作流 outputParametersByNode 解析
   - 条件分支表生成

### Metadata
- Source: user_feedback
- Related Files: .trae/skills/flow-to-markdown/SKILL.md, .trae/skills/flow-to-markdown/scripts/convert_flow.py

## [FEAT-20260312-001] user_feedback
**Logged**: 2026-03-12T10:50:00Z
**Priority**: high
**Status**: resolved
**Complexity**: low

### Capability
自动提升规则执行时，给予用户明显的更新提示

### Description
当学习内容重复出现 (Recurrence-Count ≥ 3) 触发自动提升时，需要：
1. 明确告知用户"正在更新 hy-skill"
2. 说明更新了哪个文件
3. 说明更新了什么内容
4. 提供更新前后的对比或摘要

### User Scenario
用户使用 hy-skill 过程中，Agent 发现重复模式并自动优化 skill 时，用户能清晰感知到 skill 的演进。

### Implementation
已在 hy-skill SKILL.md 中添加：
- 学习记录机制章节
- dependencies 字段声明 self-learning 依赖
- learning 配置字段定义记录时机

### Metadata
- Source: user_feedback
- Related Files: hy-skill/SKILL.md, .learnings/LEARNINGS.md

---

## [FEAT-20260314-001] user_feedback
**Logged**: 2026-03-14T08:00:00Z
**Priority**: high
**Status**: resolved
**Complexity**: medium

### Capability
工作流文档节点配置需要更详细的 JSON 格式示例

### Description
当前工作流文档中的节点配置说明不够详细，用户难以理解具体的 JSON 配置格式。

需要：
1. 提供完整的 JSON 配置示例
2. 解释每个参数的含义
3. 区分不同节点类型的配置方式

### User Scenario
用户阅读工作流文档时，能够直接复制 JSON 配置，快速完成节点配置。

### Implementation
已更新 `references/workflow-nodes-knowledge.md`：
- 新增文档知识检索和知识检索的详细配置说明
- 提供 JSON 格式的完整配置示例
- 区分两种节点类型的配置差异

### Metadata
- Source: user_feedback
- Related Files: references/workflow-nodes-knowledge.md, hy-custom-workflow/【Ver.】更新基础数据文档数据版本.md

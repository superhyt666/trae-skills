# 🧠 学习记录 (LEARNINGS.md)

记录纠正、知识缺口、最佳实践。

## 条目格式

```markdown
## [LRN-YYYYMMDD-XXX] category
**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | in_progress | resolved | promoted | wont_fix
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description

### Details
Full context

### Suggested Action
Specific fix

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- See Also: LRN-XXXX-XXX
- Pattern-Key: stable.key (optional)

## [LRN-20260315-001] best_practice
**Logged**: 2026-03-15T01:00:00Z
**Priority**: high
**Status**: resolved
**Area**: docs

### Summary
flow-to-markdown 技能解析工作流时必须包含每一步输入输出的详细配置

### Details
**问题**：原始 flow-to-markdown 技能解析的 Markdown 文档缺少节点间变量传递的详细信息，用户无法清晰看到：
- 输入参数来自哪个变量
- 输出参数传递到哪个变量

**改进要求**：
1. **变量 ID 映射表**：每个变量的 ID、名称、类型、必填性
2. **节点输入参数详情**：参数名、参数值（显示来源变量名称）
3. **节点输出参数详情**：参数名、变量ID、输出到哪个变量
4. **变量传递关系**：完整的数据流向图
5. **子工作流调用信息**：输入参数、版本ID、输出参数

**子工作流输出参数特殊处理**：
子工作流节点的输出参数存储在 `outputParametersByNode` 字段中，格式如下：
```json
{
  "output-92c57b1ed5": {
    "fill": "37dee9afb4",
    "input_prompt": "642ca9fc04",
    "output_prompt": "a7d036b446",
    "knowledge_result": "5f90c85875"
  }
}
```
需要解析为：
| 参数名 | 变量ID | 说明 | 输出到变量 |
|--------|--------|------|-----------|
| fill | 37dee9afb4 | 待填写字段 | 待填写字段 |
| knowledge_result | 5f90c85875 | 模板正文内容 | 模板正文内容 |

**变量引用解析规则**：
当参数值包含 `{{变量ID}}` 时，必须：
1. 提取变量 ID
2. 查找变量名称
3. 显示为：`变量名称(变量ID)`

例如：`{{3506a7cac2}}` → `知识名称(3506a7cac2)`

### Suggested Action
已更新 flow-to-markdown 技能的 SKILL.md 和 convert_flow.py

### Metadata
- Source: user_feedback
- Related Files: .trae/skills/flow-to-markdown/SKILL.md, .trae/skills/flow-to-markdown/scripts/convert_flow.py
- Pattern-Key: flowtodoc.detailed_io_config

---

## [LRN-20260315-002] knowledge_gap
**Logged**: 2026-03-15T01:30:00Z
**Priority**: medium
**Status**: resolved
**Area**: workflow

### Summary
子工作流 versionId 为 null 表示"随版本启用"，不是未设置

### Details
**纠正**：之前理解有误。

**澄清**：
- `versionId: null` 表示"随版本启用"，即使用当前激活的最新版本
- 这是平台的一种正常配置方式，不是问题

**可能卡顿的真正原因**：
1. 子工作流本身未激活/未发布
2. 子工作流内部逻辑执行缓慢
3. 网络或资源问题

**判断方法**：
| versionId 值 | 含义 | 是否正常 |
|-------------|------|---------|
| null | 随版本启用（使用最新激活版本） | ✅ 正常 |
| 具体数字 | 指定特定版本 | ✅ 正常 |
| 空或未填 | 可能导致问题 | ⚠️ 检查 |

### Suggested Action
已更正文档中的描述，避免误导

### Metadata
- Source: user_feedback
- Related Files: hy-skill/hy-custom-workflow/*.md
- Pattern-Key: workflow.subprocess.version_null

---
```

---

## [LRN-20260312-001] best_practice
**Logged**: 2026-03-12T10:30:00Z
**Priority**: high
**Status**: resolved
**Area**: docs | config

### Summary
从 self-learning skill 学习到 Skill 元数据结构最佳实践

### Details
通过对比 self-learning skill 的 SKILL.md，发现 hy-skill 的元数据结构可以优化：

1. **description 字段格式化**：使用 YAML 多行字符串 `|` 使描述更清晰
2. **添加 Use this skill when 部分**：明确列出触发条件，便于 Agent 判断
3. **添加 Triggers 标签**：提供关键词快速匹配
4. **添加版本元数据**：version、author、license、repository
5. **添加 allowed-tools**：声明 Skill 需要使用的工具
6. **添加 files 列表**：列出核心文件及其用途

### Suggested Action
已应用到 hy-skill SKILL.md 的优化中

### Metadata
- Source: conversation
- Related Files: hy-skill/SKILL.md, .trae/skills/self-learning/SKILL.md
- Pattern-Key: skill.metadata.structure

---

## [LRN-20260312-002] best_practice
**Logged**: 2026-03-12T10:35:00Z
**Priority**: medium
**Status**: resolved
**Area**: docs

### Summary
Skill 项目应包含 CHANGELOG.md 记录版本历史

### Details
self-learning skill 包含 CHANGELOG.md 文件，记录：
- 版本号遵循语义化版本规范
- 使用 [Keep a Changelog](https://keepachangelog.org/) 格式
- 区分 Added、Changed、Deprecated、Removed、Fixed、Security 类型
- 便于用户了解 Skill 演进历史

### Suggested Action
已为 hy-skill 添加 CHANGELOG.md

### Metadata
- Source: conversation
- Related Files: hy-skill/CHANGELOG.md
- Pattern-Key: skill.project.changelog

---

## [LRN-20260312-003] best_practice
**Logged**: 2026-03-12T10:40:00Z
**Priority**: medium
**Status**: resolved
**Area**: config

### Summary
Skill 项目应包含 config.yaml 配置文件

### Details
self-learning skill 使用 config.yaml 管理：
- 模块配置（enabled、priority、triggers）
- 节点类型配置
- 设计模式配置
- 日志配置

配置文件使 Skill 更易于维护和扩展。

### Suggested Action
已为 hy-skill 添加 config.yaml，包含四大模块和节点类型配置

### Metadata
- Source: conversation
- Related Files: hy-skill/config.yaml
---

## [LRN-20260312-004] user_preference
**Logged**: 2026-03-12T10:52:00Z
**Priority**: high
**Status**: resolved
**Area**: docs

### Summary
用户偏好：自动提升时需要明显的更新提示

### Details
用户明确要求在执行自动提升规则时，需要给予明显提示：
1. 明确告知"正在更新 hy-skill"
2. 说明更新了哪个文件
3. 说明更新了什么内容
4. 提供更新前后的对比或摘要

### Suggested Action
在每次自动提升时，使用以下格式通知用户：

```
🔄 **自动提升触发** (Recurrence-Count: X)

📝 **更新文件**: [文件路径]

📌 **更新内容**:
- 新增/修改: xxx

📋 **变更摘要**:
[具体变更说明]
```

### Metadata
- Source: user_feedback
- Related Files: hy-skill/SKILL.md, .learnings/LEARNINGS.md
- Pattern-Key: skill.update.notification

---

## [LRN-20260312-005] best_practice
**Logged**: 2026-03-12T11:00:00Z
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
Skill 间依赖声明：通过 dependencies 字段建立技能协作关系

### Details
为了让 hy-skill 能够主动记录学习内容到 self-learning，需要在 SKILL.md 中声明依赖关系：

```yaml
dependencies:
  - self-learning: 学习记录系统，用于记录使用过程中的学习内容
learning:
  enabled: true
  workspace: ./
  record_on:
    - user_correction
    - new_discovery
    - error_occurred
    - feature_request
```

### Suggested Action
已为 hy-skill 添加 dependencies 和 learning 配置字段

### Metadata
- Source: user_feedback
- Related Files: hy-skill/SKILL.md
- Pattern-Key: skill.dependencies.declaration

---

## [LRN-20260312-006] best_practice
**Logged**: 2026-03-12T11:10:00Z
**Priority**: medium
**Status**: resolved
**Area**: config

### Summary
学习记录同步策略：选择性上传到 GitHub

### Details
学习记录的同步需要平衡隐私和便利性：

**推荐策略**：
```
.learnings/
├── LEARNINGS.md          ✅ 上传（最佳实践、知识沉淀）
├── FEATURE_REQUESTS.md   ✅ 上传（功能规划）
└── ERRORS.md             ❌ 不上传（可能含敏感信息）
```

**配置方式**：在 .gitignore 中添加注释说明，默认上传，用户可自行选择排除。

### Suggested Action
已在项目根目录和 hy-skill 目录的 .gitignore 中添加学习记录同步配置说明

### Metadata
- Source: user_feedback
- Related Files: .gitignore, hy-skill/.gitignore
- Pattern-Key: skill.learning.sync

---

## [LRN-20260312-007] best_practice
**Logged**: 2026-03-12T11:20:00Z
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
学习记录目录应放在 Skill 目录内，便于 GitHub 同步

### Details
将 `.learnings/` 目录移入 `hy-skill/` 内的好处：
1. 与 Skill 一起同步到 GitHub
2. 远程加载 self-learning 后可直接使用
3. 学习记录与 Skill 绑定，更清晰

**目录结构**：
```
hy-skill/
├── .learnings/
│   ├── LEARNINGS.md
│   ├── ERRORS.md
│   └── FEATURE_REQUESTS.md
├── SKILL.md
├── CHANGELOG.md
├── config.yaml
└── references/
```

### Suggested Action
已将 .learnings 移入 hy-skill 目录，并更新 SKILL.md 配置

### Metadata
- Source: user_feedback
- Related Files: hy-skill/SKILL.md, hy-skill/.learnings/
- Pattern-Key: skill.learnings.location

---

## [LRN-20260314-001] knowledge_gap
**Logged**: 2026-03-14T08:00:00Z
**Priority**: critical
**Status**: resolved
**Area**: docs

### Summary
文档知识检索节点与知识检索节点是不同的节点类型，配置方式有显著差异

### Details
**关键区别**：

| 节点类型 | 组件类型 | 功能 | 输出类型 |
|---------|---------|------|---------|
| 文档知识检索 | DOCUMENT_KNOWLEDGE_SEARCH | 检索整个文档 | KNOWLEDGE |
| 知识检索 | KNOWLEDGE_SEARCH | 检索知识片段 | JSON |

**文档知识检索配置**：
```json
{
  "type": "rule",
  "conditions": [
    {
      "field": "documentName",
      "operator": "contains",
      "value": "关键词"
    }
  ],
  "knowledgeInventorySn": "知识库SN"
}
```

**知识检索配置**：
```json
{
  "searchModel": "all",
  "searchKnowledge": "all_knowledge || {{文档变量}}"
}
```

**标准组合模式**：
```
文档知识检索（规则检索定位文档）
    ↓
知识检索（searchModel: "all" 返回全部片段）
    ↓
JSON解析（提取关键字段）
```

### Suggested Action
已更新 `references/workflow-nodes-knowledge.md`，详细区分两种节点类型及其配置方式

### Metadata
- Source: user_feedback
- Related Files: references/workflow-nodes-knowledge.md
- Pattern-Key: workflow.knowledge.nodes.distinction

---

## [LRN-20260314-002] best_practice
**Logged**: 2026-03-14T08:30:00Z
**Priority**: high
**Status**: resolved
**Area**: workflow

### Summary
工作流中公共操作应提前到条件判断之前，避免重复配置

### Details
**优化原则**：如果一个操作在所有分支中都需要执行，应该提前到条件判断之前。

**优化前**：
```
条件判断 → 路径A: 获取配置 → ...
        → 路径B: 并行(获取配置 + 调用子工作流) → ...
```
问题：获取配置需要配置两次，且并行处理增加了复杂度

**优化后**：
```
获取配置 → 条件判断 → 路径A: 直接后续处理
                  → 路径B: 调用子工作流 → 后续处理
```
优点：
1. 获取配置只需配置一次
2. 移除不必要的并行处理
3. 降低用户操作复杂度

### Suggested Action
已更新工作流文档，采用优化后的流程结构

### Metadata
- Source: user_feedback
- Related Files: hy-custom-workflow/【Ver.】更新基础数据文档数据版本.md
- Pattern-Key: workflow.optimization.common_operation

---

## [LRN-20260314-003] gotcha
**Logged**: 2026-03-14T09:00:00Z
**Priority**: high
**Status**: resolved
**Area**: workflow

### Summary
并行处理的一个分支是空操作时，并行处理没有意义

### Details
**错误设计**：
```
并行处理
├─ 分支A: 获取配置（有实际工作）
└─ 分支B: 空操作（无实际工作）
```

如果一个分支是空操作，并行处理完全没有意义，反而增加了不必要的节点复杂度。

**正确做法**：
- 只有一个分支有实际工作时，直接串行执行
- 两个分支都有实际工作时，才使用并行处理

### Suggested Action
已修正工作流文档，移除无意义的并行处理

### Metadata
- Source: user_feedback
- Related Files: hy-custom-workflow/【Ver.】更新基础数据文档数据版本.md
- Pattern-Key: workflow.parallel.meaningful

---

## [LRN-20260314-004] best_practice
**Logged**: 2026-03-14T10:00:00Z
**Priority**: high
**Status**: resolved
**Area**: docs

### Summary
工作流文档的配置参数应优先使用表格形式呈现，JSON 作为"供复制"的补充

### Details
**问题**：直接展示完整 JSON 配置对用户不友好，难以快速理解每个参数的含义。

**最佳实践**：
1. **表格优先**：用表格清晰展示参数、值、说明
2. **JSON 补充**：JSON 放在"完整配置（供复制）"部分，方便用户复制

**示例**：

```markdown
**配置参数**：

| 参数 | 值 | 说明 |
|------|-----|------|
| 检索类型 | `rule`（规则检索） | 按文档属性精确匹配 |
| 知识库 | `53604b1a-...` | 配置模版所在知识库 |

**检索条件**：

| 条件字段 | 操作符 | 匹配值 | 说明 |
|---------|--------|--------|------|
| documentName | contains | `配置模版` | 文档名称包含"配置模版" |

**完整配置（供复制）**：
```json
{
  "type": "rule",
  "conditions": [...]
}
```

**优点**：
- 用户可以快速理解每个参数的作用
- 需要复制时可以直接复制 JSON
- 文档更加易读

### Suggested Action
已更新工作流文档，采用"表格优先 + JSON 补充"的格式

### Metadata
- Source: user_feedback
- Related Files: hy-custom-workflow/【Ver.】更新基础数据文档数据版本.md
- Pattern-Key: docs.config.format

---

## [LRN-20260314-005] knowledge_gap
**Logged**: 2026-03-14T11:00:00Z
**Priority**: critical
**Status**: resolved
**Area**: workflow

### Summary
知识检索输出的 JSON 可能包含多个版本数据，需要自定义组件处理才能提取最新版本

### Details
**问题**：知识检索输出虽然是 JSON 格式，但结果可能是多个版本的数组：

```json
[
  {"Version": "0.0.1", "Data": {"步骤A": 10}},
  {"Version": "0.0.2", "Data": {"步骤A": 10, "步骤B": 15}},
  {"Version": "0.0.3", "Data": {"步骤A": 10, "步骤B": 15, "步骤C": 20}}
]
```

**解决方案**：使用自定义组件处理：

| 场景 | 处理方式 | 说明 |
|------|---------|------|
| 多版本数据 | 自定义组件 | 提取最新版本、比较变化、准备后续输入 |
| 单版本数据 | JSON解析 | 直接提取字段 |

**标准模式**：
```
文档知识检索 → 知识检索 → 自定义组件
                              ↓
                    输出: current_version, has_changes, llm_input
```

**自定义组件功能**：
1. 提取最新版本（按 Version 排序）
2. 与新数据比较，判断是否有变化
3. 准备后续节点需要的输入

### Suggested Action
已更新 `references/workflow-nodes-knowledge.md`，补充自定义组件处理模式

### Metadata
- Source: user_feedback
- Related Files: references/workflow-nodes-knowledge.md, hy-custom-workflow/【H.】文档知识更新与版本同步.md
- Pattern-Key: workflow.knowledge.multi_version

---

## [LRN-20260314-006] best_practice
**Logged**: 2026-03-14T11:30:00Z
**Priority**: critical
**Status**: resolved
**Area**: workflow

### Summary
选择节点不能仅凭输出格式与预期格式一致，还需考虑数据内容和业务逻辑

### Details
**错误思维**：
```
知识检索输出是 JSON 格式
    ↓
预期需要 JSON 格式
    ↓
直接用 JSON 解析节点 ❌
```

**正确思维**：
```
知识检索输出是 JSON 格式
    ↓
分析数据内容：
  - 是单版本还是多版本？
  - 需要提取最新版本吗？
  - 需要比较变化吗？
  - 需要准备后续输入吗？
    ↓
选择合适的节点：
  - 单版本 + 简单提取 → JSON解析
  - 多版本 + 复杂逻辑 → 自定义组件
```

**节点选择原则**：

| 考虑因素 | 说明 |
|---------|------|
| 输出格式 | 只是基础条件，不是唯一标准 |
| 数据内容 | 分析实际数据结构（单值/数组/嵌套） |
| 业务逻辑 | 需要排序、比较、转换等处理吗？ |
| 后续需求 | 输出需要供哪些节点使用？ |

**示例对比**：

| 场景 | 输出格式 | 数据内容 | 正确选择 |
|------|---------|---------|---------|
| 获取单版本配置 | JSON | `{"Version": "0.0.1", "Data": {...}}` | JSON解析 |
| 获取最新版本 | JSON | `[{"Version": "0.0.1"}, {"Version": "0.0.2"}]` | 自定义组件 |
| 比较新旧数据 | JSON | 需要对比逻辑 | 自定义组件 |

### Suggested Action
已更新 `references/workflow-nodes-knowledge.md`，强调节点选择需考虑数据内容和业务逻辑

### Metadata
- Source: user_feedback
- Related Files: references/workflow-nodes-knowledge.md
- Pattern-Key: workflow.node_selection.principle

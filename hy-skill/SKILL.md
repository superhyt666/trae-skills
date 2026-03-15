---
name: hy-skill
description: |
  工作流平台智能助手，提供 Python 代码生成、工作流搭建、Agent 提示词设计、工作流识别和工作流文档阅读修改五大核心能力。
  Invoke when: Python 代码生成、工作流搭建、Agent 设计、工作流识别、代码生成、提示词设计、工作流文档阅读
version: 1.1.0
author: hyt
license: MIT
repository: https://github.com/superhyt666/trae-skills
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebSearch
  - WebFetch
dependencies:
  - self-learning: 学习记录系统，用于记录使用过程中的学习内容
files:
  - references/python-standards.md: Python 代码生成详细规范
  - references/workflow-setup.md: 工作流搭建指南
  - references/workflow-node-variable-mapping.md: 节点变量类型映射表
  - references/agent-prompts.md: Agent 提示词设计指南
  - references/agent-examples.md: Agent 配置示例库
  - references/workflow-recognition.md: 工作流识别参考文档
  - references/workflow-document-guide.md: 工作流文档阅读与修改指南
  - references/design-philosophy.md: 设计哲学
  - references/keywords.md: 关键字映射表
learning:
  enabled: true
  learnings_dir: .learnings
  record_on:
    - user_correction
    - new_discovery
    - error_occurred
    - feature_request
---

## 功能概述

将 .flow 格式的工作流文件转换为结构清晰的 Markdown 文档，输出保存到 `hy-custom-workflow/` 目录。

hy-skill 是专为线上工作流平台设计的智能助手，提供五大核心能力：

| 模块 | 功能 | 触发关键字 |
|------|------|-----------|
| Python 代码生成 | 生成符合平台规范的 Python 函数代码 | `python 代码`、`代码生成`、`写脚本` |
| 工作流搭建 | 指导工作流配置和节点连接 | `工作流`、`搭建流程`、`配置流程` |
| Agent 提示词 | 设计 Agent 配置和提示词 | `提示词`、`agent 设置`、`角色配置` |
| 工作流识别 | 识别工作流截图或 .flow 文件 | `工作流识别`、`识别工作流截图`、`截图识别` |
| 工作流文档阅读 | 阅读并修改工作流文档 | `阅读工作流文档`、`分析工作流文档`、`修改工作流文档` |

**模块间关联**：
- 工作流中的 **Agent 节点** 使用 Agent 提示词模块设计的 Agent
- 工作流中的 **Python 代码执行节点** 使用 Python 代码生成模块生成的代码
- **工作流识别模块** 为工作流搭建提供参考和复现依据
- **工作流文档阅读模块** 支持对已识别的工作流文档进行修改和扩展

---

## 触发机制

| 触发关键字 | 功能模块 | 优先级 | 参考文档 |
|-----------|---------|--------|---------|
| `利用 hy-skill 技能编写 python 技能代码` | Python 代码生成 | P0 | [python-standards.md](references/python-standards.md) |
| `使用 hy-skill 进行工作流搭建` | 工作流搭建 | P0 | [workflow-setup.md](references/workflow-setup.md) |
| `使用 hy-skill 设计 agent 实现` | Agent 提示词 | P0 | [agent-prompts.md](references/agent-prompts.md) |
| `工作流识别`、`识别工作流截图` | 工作流识别 | P0 | [workflow-recognition.md](references/workflow-recognition.md) |
| `阅读工作流文档`、`分析工作流文档` | 工作流文档阅读 | P0 | [workflow-document-guide.md](references/workflow-document-guide.md) |
| `python 代码`、`代码生成`、`写脚本` | Python 代码生成 | P1 | [python-standards.md](references/python-standards.md) |
| `工作流`、`搭建流程`、`配置流程` | 工作流搭建 | P1 | [workflow-setup.md](references/workflow-setup.md) |
| `提示词`、`agent 设置`、`角色配置` | Agent 提示词 | P1 | [agent-prompts.md](references/agent-prompts.md) |
| `分析工作流截图`、`截图识别` | 工作流识别 | P1/P2 | [workflow-recognition.md](references/workflow-recognition.md) |
| `修改工作流文档`、`扩展工作流文档` | 工作流文档阅读 | P1 | [workflow-document-guide.md](references/workflow-document-guide.md) |

---

## Python 代码生成模块

### 触发条件

- `利用 hy-skill 技能编写 python 技能代码`（P0）
- `python 代码`、`代码生成`、`写脚本`（P1）

### 核心规范

**两段式交付流程**：

| 阶段 | 目标 | 特征 |
|------|------|------|
| 阶段 1：开发测试版 | 功能验证 | 包含 `if __name__ == "__main__":`、测试用例、`print()` 调试 |
| 阶段 2：交付展示版 | 平台部署 | 移除测试代码、保留调用示例、使用占位符 |

**关键规则**：
- 函数必须返回 **Python 对象**（dict/list），**禁止** `json.dumps()` 序列化
- 所有 `import` 语句放在文件顶部
- 禁止 `print()` 输出结果
- 禁止在代码中初始化输入

### 代码示例

```python
import json
from typing import Any, Dict

def process_request(input_data: Any) -> Dict[str, Any]:
    """处理请求的主函数"""
    try:
        data = parse_input(input_data)
        result = business_logic(data)
        return result  # 返回 Python 对象，不是 JSON 字符串
    except Exception as e:
        return {"error": True, "message": str(e)}

def parse_input(input_data: Any) -> Any:
    if isinstance(input_data, (dict, list)):
        return input_data
    if isinstance(input_data, str):
        try:
            return json.loads(input_data)
        except json.JSONDecodeError:
            return {"text": input_data}
    return {"text": str(input_data)}

def business_logic(data: Any) -> Dict[str, Any]:
    return {"status": "success", "data": data}

# 调用示例：result = process_request(user_input)
```

## 使用方法

### 与 hy-skill 集成使用
```
当使用 hy-skill 进行工作流识别时：
1. 用户发出"识别这个工作流"指令
2. 选择".flow文件识别"方式
3. 上传或选择本地 .flow 文件
4. 系统自动调用此技能进行处理
5. 输出 Markdown 格式的完整工作流文档到 hy-custom-workflow/ 目录
```

## 依赖

- Python 3.x
- 无需额外依赖（使用标准库）

## 核心脚本

### convert_flow.py

主转换脚本，实现以下功能：
1. Base64 + URL 解码 .flow 文件
2. 解析嵌套 JSON 结构
3. 提取变量 ID 到名称的映射
4. 翻译组件类型为中文
5. 生成包含 Mermaid 流程图的 Markdown 文档

## 参考文档

### Agent 类型选择

| 类型 | 适用场景 | 核心配置 |
|------|---------|---------|
| 智能会话 Agent | 客服对话、文本生成、代码生成 | 模型 + 创造性级别 + 提示词 |
| 知识检索 Agent | 知识库问答、文档查询、技术支持 | 模型 + 知识库 + 答复模式 |

### 快速配置模板

**智能会话 Agent**：
```markdown
【基础配置】
模型：Qwen32B
创造性：5 级

【提示词】
你是一个 [角色]，负责 [职责]。
工作要求: 1. [要求1] 2. [要求2]
输出格式：[格式说明]
```

**知识检索 Agent**：
```markdown
【基础配置】
模型：Qwen32B
创造性：3 级
知识库：[知识库名称]

【答复模式】
上下文记忆：开启（5 轮）
问题分析：开启
问题聚焦：开启
答复质量模式：答复质量优先
```

### 详细文档

完整指南见：[references/agent-prompts.md](references/agent-prompts.md)

---

## 工作流识别模块

### 触发条件

- `工作流识别`、`识别工作流截图`（P0）
- `识别这个工作流`（P0）
- `分析工作流截图`、`截图识别`（P1/P2）

### 核心能力

- **截图识别**：识别截图中的所有节点类型、变量、连接关系和流程分析
- **.flow文件识别**：直接解析 .flow 格式文件，生成结构化 Markdown 文档

### 识别方式选择

当用户发出"识别这个工作流"指令时，提供两种识别方式：

| 方式 | 输入类型 | 输出格式 | 适用场景 |
|------|---------|---------|---------|
| 截图识别 | 工作流截图/图片 | 纯文本描述（节点、连接、流程） | 已有工作流截图，需要分析结构 |
| .flow文件识别 | .flow文件 | Markdown文档（含Mermaid流程图） | 有.flow源文件，需要完整文档 |

### 识别方式1：截图识别

```
输入：工作流截图
 ↓
AI分析截图中的节点、连接线、变量标注
 ↓
输出结构化描述（按 workflow-recognition.md 规范）
```

**输出示例**：
```
【工作流名称】：xxx
【流程类型】：线性/分支/循环/并行

【执行路径】：
输入节点 → 节点A → 节点B → 输出节点

【详细配置】：
1. 输入节点
   - 输入变量：文本：user_input
2. 节点A（节点类型）
   - 输出：文本：result
```

### 识别方式2：.flow文件识别

```
输入：.flow文件（Base64 + URL 编码）
 ↓
调用 flow-to-markdown 技能处理，输出 Markdown 文档到 hy-skill/hy-custom-workflow/ 目录
 ↓
输出 Markdown 文档（包含 Mermaid 流程图）
```

**输出内容**：
- 基本信息（流程ID、状态、创建时间等）
- 输入输出变量表
- 流程节点详情（每个节点的配置参数）
- Mermaid 流程图

**调用方式**：
```
选择"通过.flow文件识别"后：
1. 用户上传或选择本地 .flow 文件
2. 系统自动调用 flow-to-markdown 技能，生成 Markdown 文件到 hy-skill/hy-custom-workflow/ 目录
3. 技能执行 convert_flow.py 脚本
4. 生成对应的 Markdown 格式输出
```

### 详细文档

完整指南见：[references/workflow-recognition.md](references/workflow-recognition.md)

---

## 工作流文档阅读与修改模块

### 触发条件

- `阅读工作流文档`、`分析工作流文档`（P0）
- `读取工作流文档`、`查看工作流文档`（P0）
- `修改工作流文档`、`扩展工作流文档`（P1）

### 核心能力

- **文档阅读**：读取并解析工作流 Markdown 文档，理解技术规范、流程说明和版本信息
- **需求响应**：根据用户需求对文档内容进行修改或功能扩展
- **工作流搭建联动**：修改涉及工作流结构时，调用工作流搭建模块的能力

### 工作流程

```
步骤 1：读取文档
 ↓
完整阅读指定的工作流文档内容
 ↓
步骤 2：理解文档
 ↓
解析文档结构，提取关键信息：
- 基本信息（流程ID、状态、创建时间等）
- 输入输出变量
- 节点配置详情
- 流程走向
- 子工作流依赖
 ↓
步骤 3：主动询问
 ↓
向用户询问具体诉求：
- 需要修改哪些内容？
- 需要添加什么功能？
- 需要优化哪些流程？
 ↓
步骤 4：执行修改
 ↓
根据用户需求执行操作：
- 修改文档内容 → 直接更新 Markdown 文件
- 扩展工作流功能 → 调用工作流搭建模块
- 优化节点配置 → 更新节点配置说明
```

### 支持的文档格式

工作流文档存放路径：`hy-skill/hy-custom-workflow/`

**标准文档结构**：

```markdown
# 【前缀】工作流名称

## 基本信息
| 属性 | 值 |
|------|-----|
| **流程名称** | xxx |
| **流程ID** | process:xxxx |
| **状态** | 已发布/草稿 |
| **创建时间** | YYYY-MM-DD HH:mm:ss |
| **创建者** | xxx |
| **版本** | vx |

## 流程类型
**xxx流程**：xxx

## 输入变量
| 变量名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| xxx | TEXT/JSON/... | ✅/❌ | xxx |

## 输出变量
| 变量名 | 类型 | 说明 |
|--------|------|------|
| xxx | TEXT/JSON/... | xxx |

## 执行路径
```
流程图描述
```

## 详细节点配置
### 1. 节点名称 (节点类型) - ID: xxx
- 配置详情...

## Mermaid 流程图
```mermaid
flowchart TD
    ...
```

## 核心功能说明
xxx

## 变量传递关系
xxx

## 子工作流依赖
| 子工作流名称 | 流程ID | 用途 |
|-------------|--------|------|
| xxx | process:xxxx | xxx |

## 注意事项
xxx
```

### 修改类型与处理方式

| 修改类型 | 处理方式 | 说明 |
|---------|---------|------|
| 文档内容修正 | 直接修改 Markdown | 修正错别字、补充说明、更新信息 |
| 节点配置调整 | 更新节点配置章节 | 修改节点参数、输入输出变量 |
| 流程优化 | 调用工作流搭建模块 | 添加/删除节点、调整流程走向 |
| 功能扩展 | 调用工作流搭建模块 | 添加新功能节点、扩展工作流能力 |
| 版本更新 | 更新基本信息和变更记录 | 记录版本变更历史 |

### 使用示例

**示例 1：阅读工作流文档**

```
用户：阅读工作流文档 c:\...\hy-custom-workflow\【Ver.】解码指定项目的进度.md

Agent：
1. 读取文档内容
2. 解析文档结构
3. 输出文档摘要：
   - 流程名称：【Ver.】解码指定项目的进度
   - 流程ID：process:4640
   - 流程类型：复合流程（线性流程 + 并行处理 + 条件判断）
   - 核心功能：解码指定项目的进度状态
   - 主要节点：并行处理、工作流调用、数据类型转换
4. 询问用户：您需要对这个工作流进行什么操作？
```

**示例 2：修改工作流文档**

```
用户：在这个工作流中添加一个错误处理节点

Agent：
1. 确认修改需求
2. 分析当前流程结构
3. 调用工作流搭建模块，设计错误处理节点
4. 更新文档内容：
   - 添加节点配置说明
   - 更新执行路径
   - 更新 Mermaid 流程图
   - 更新变量传递关系
5. 保存修改后的文档
```

### 与其他模块的联动

| 联动模块 | 联动场景 | 说明 |
|---------|---------|------|
| 工作流识别 | 文档不存在时 | 先识别工作流生成文档，再进行阅读修改 |
| 工作流搭建 | 流程结构修改时 | 调用搭建模块设计新的节点和流程 |
| Python 代码生成 | 代码节点修改时 | 生成新的 Python 代码并更新文档 |
| Agent 提示词 | Agent 节点修改时 | 设计新的 Agent 配置并更新文档 |

### 详细文档

完整指南见：[references/workflow-document-guide.md](references/workflow-document-guide.md)

---

## 学习记录机制

hy-skill 集成了 self-learning skill 的学习记录系统，在使用过程中会主动记录学习内容。

### 记录时机

| 场景 | 记录到 | 示例 |
|------|--------|------|
| 用户纠正工作流配置 | LEARNINGS.md | 节点变量类型纠正 |
| 发现新的节点用法 | LEARNINGS.md | 新节点配置技巧 |
| 执行命令失败 | ERRORS.md | 命令错误信息 |
| 用户提出新需求 | FEATURE_REQUESTS.md | 新功能请求 |

### 记录方式

Agent 在使用 hy-skill 时，会自动调用 self-learning 的记录机制：

```markdown
# 记录学习内容
- 分类：correction / knowledge_gap / best_practice / gotcha / workflow
- 优先级：low / medium / high / critical
- Pattern-Key：用于追踪重复模式
```

### 学习记录文件位置

```
hy-skill/.learnings/
├── LEARNINGS.md          # 学习记录
├── ERRORS.md             # 错误记录
└── FEATURE_REQUESTS.md   # 功能请求
```

---

## 自动提升规则

当学习内容重复出现 (Recurrence-Count ≥ 3) 时，会自动提升到 hy-skill：

| 学习类型 | 提升到 | 示例 |
|---------|--------|------|
| 行为模式 | SKILL.md | 新增触发条件 |
| 新节点用法 | references/workflow-nodes-*.md | 节点配置技巧 |
| 代码规范 | references/python-standards.md | 新的代码约定 |
| Agent 配置技巧 | references/agent-examples.md | Agent 配置模板 |

### 更新通知格式

每次自动提升时，会使用以下格式通知用户：

```
🔄 **自动提升触发** (Recurrence-Count: X)

📝 **更新文件**: [文件路径]

📌 **更新内容**:
- 新增/修改: xxx

📋 **变更摘要**:
[具体变更说明]
```

---

## 资源目录

### references/

| 文档 | 说明 |
|------|------|
| [python-standards.md](references/python-standards.md) | Python 代码生成详细规范 |
| [workflow-setup.md](references/workflow-setup.md) | 工作流搭建指南 |
| [workflow-node-variable-mapping.md](references/workflow-node-variable-mapping.md) | 节点变量类型映射表（核心参考） |
| [agent-prompts.md](references/agent-prompts.md) | Agent 提示词设计指南 |
| [agent-examples.md](references/agent-examples.md) | Agent 配置示例库 |
| [workflow-recognition.md](references/workflow-recognition.md) | 工作流识别参考文档 |
| [workflow-document-guide.md](references/workflow-document-guide.md) | 工作流文档阅读与修改指南 |
| [design-philosophy.md](references/design-philosophy.md) | 设计哲学（任务拆解原则） |
| [retrieval-augmented-pattern.md](references/retrieval-augmented-pattern.md) | 检索增强模式 |
| [template-lookup-pattern.md](references/template-lookup-pattern.md) | 模板化+查表法 |
| [keywords.md](references/keywords.md) | 关键字映射表 |
| [workflow-nodes-calling.md](references/workflow-nodes-calling.md) | 调用类节点详细文档 |
| [workflow-nodes-control.md](references/workflow-nodes-control.md) | 流程控制节点详细文档 |
| [workflow-nodes-ai.md](references/workflow-nodes-ai.md) | AI 能力节点详细文档 |
| [workflow-nodes-knowledge.md](references/workflow-nodes-knowledge.md) | 知识管理节点详细文档 |
| [workflow-nodes-table.md](references/workflow-nodes-table.md) | 智能表格节点详细文档 |
| [workflow-nodes-text.md](references/workflow-nodes-text.md) | 文本处理节点详细文档 |

### hy-custom-workflow/

存放工作流识别生成的 Markdown 文档，每个文档对应一个已识别的工作流。

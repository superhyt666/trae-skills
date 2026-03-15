# 工作流节点变量类型映射表

> **⚠️ 重要：此文件是 hy-skill 工作流搭建的核心参考文档，agent 必须严格按照此文件的规定进行节点配置。**

> **⚠️ 关键规则：任何节点的输入输出变量类型必须严格匹配此表，不得随意猜测或省略。**

***

## 📋 目录

1. [变量类型总览](#变量类型总览)
2. [节点类型与文档映射](#节点类型与文档映射)
3. [节点连接兼容性速查表](#节点连接兼容性速查表)
4. [关键禁令](#关键禁令必须严格遵守)
5. [检查清单](#必须遵循的检查清单)

***

## 🔑 变量类型总览

平台支持的完整变量类型列表（按优先级排序）：

| 类别     | 类型         | 说明            |
| ------ | ---------- | ------------- |
| 基础类型   | `文本`       | 字符串类型，最常用     |
| <br /> | `json`     | JSON 对象，结构化数据 |
| <br /> | `markdown` | Markdown 格式文本 |
| <br /> | `引用`       | 引用其他变量或资源     |
| <br /> | `超链接`      | URL 链接地址      |
| 文档类型   | `文档`       | 单个文档文件        |
| <br /> | `文档/数组`    | 文档文件列表        |
| <br /> | `文档知识库`    | 文档知识库对象       |
| <br /> | `文档知识库/数组` | 知识库列表         |
| 图片类型   | `图片`       | 单个图片文件        |
| <br /> | `图片/数组`    | 图片文件列表        |
| 音频类型   | `音频`       | 单个音频文件        |
| <br /> | `音频/数组`    | 音频文件列表        |
| 知识类型   | `知识`       | 单个知识片段        |
| <br /> | `知识/数组`    | 知识片段列表        |
| 图表类型   | `图表`       | 图表对象          |
| <br /> | `图表/数组`    | 图表对象列表        |
| 复合类型   | `文本/数组`    | 字符串列表         |
| <br /> | `json/数组`  | JSON 对象列表     |
| <br /> | `超链接/数组`   | URL 链接列表      |

### 数组类型命名规则

- 格式：`基础类型/数组`
- 例如：`文本/数组`、`json/数组`、`文档/数组`

***

## 📚 节点类型与文档映射

各节点的详细变量类型说明请查阅对应文档：

### 调用类节点

| 节点类型 | 详细文档 | 核心要点 |
|---------|---------|---------|
| Agent 节点 | [workflow-nodes-calling.md](workflow-nodes-calling.md#agent-节点) | 输出**始终**为文本类型 |
| 工作流节点 | [workflow-nodes-calling.md](workflow-nodes-calling.md#工作流节点) | 类型完全继承自子工作流 |
| Python 代码执行节点 | [workflow-nodes-calling.md](workflow-nodes-calling.md#python-代码执行节点) | 支持多种类型，需明确指定 |
| HTTP 技能节点 | [workflow-nodes-calling.md](workflow-nodes-calling.md#http-技能节点) | 输出通常为 json |
| LLM 节点 | [workflow-nodes-calling.md](workflow-nodes-calling.md#llm-节点) | 输出**始终**为文本类型 |

### 流程控制节点

| 节点类型 | 详细文档 | 核心要点 |
|---------|---------|---------|
| 条件判断节点 | [workflow-nodes-control.md](workflow-nodes-control.md#条件判断节点) | 无直接输出，通过分支传递变量 |
| 循环处理节点 | [workflow-nodes-control.md](workflow-nodes-control.md#循环处理节点) | 输入**必须**是数组类型 |
| 并行处理节点 | [workflow-nodes-control.md](workflow-nodes-control.md#并行处理节点) | 分支间变量隔离 |
| 路径合并节点 | [workflow-nodes-control.md](workflow-nodes-control.md#路径合并节点) | 可访问所有分支输出变量 |

### AI 能力节点

| 节点类型 | 详细文档 | 核心要点 |
|---------|---------|---------|
| 图像生成节点 | [workflow-nodes-ai.md](workflow-nodes-ai.md#图像生成节点) | 输入仅支持文本 |
| 语音识别节点 | [workflow-nodes-ai.md](workflow-nodes-ai.md#语音识别节点) | 输入为音频，输出为文本 |
| 语音合成节点 | [workflow-nodes-ai.md](workflow-nodes-ai.md#语音合成节点) | 输入为文本，输出为音频 |

### 知识管理节点

| 节点类型 | 详细文档 | 核心要点 |
|---------|---------|---------|
| 添加知识节点 | [workflow-nodes-knowledge.md](workflow-nodes-knowledge.md#添加知识节点) | 输出**始终**为知识/数组 |
| 知识问答节点 | [workflow-nodes-knowledge.md](workflow-nodes-knowledge.md#知识问答节点) | 问题内容**必须**是文本 |
| 文档知识检索节点 | [workflow-nodes-knowledge.md](workflow-nodes-knowledge.md#文档知识检索节点) | 输出为知识/数组 |
| 知识检索节点 | [workflow-nodes-knowledge.md](workflow-nodes-knowledge.md#知识检索节点) | 输出为 json（非 json/数组） |
| 知识片段排序节点 | [workflow-nodes-knowledge.md](workflow-nodes-knowledge.md#知识片段排序节点) | 输入输出类型一致 |

### 智能表格节点

| 节点类型 | 详细文档 | 核心要点 |
|---------|---------|---------|
| 智能表格检索节点 | [workflow-nodes-table.md](workflow-nodes-table.md#智能表格检索节点) | 输出**始终**为 json/数组，必须限制行数 |
| 写入智能表格节点 | [workflow-nodes-table.md](workflow-nodes-table.md#写入智能表格节点) | 支持逐一或批量写入 |

### 文本处理节点

| 节点类型 | 详细文档 | 核心要点 |
|---------|---------|---------|
| 关键词识别节点 | [workflow-nodes-text.md](workflow-nodes-text.md#关键词识别节点) | 输出**始终**为文本/数组 |
| 文本替换节点 | [workflow-nodes-text.md](workflow-nodes-text.md#文本替换节点) | 输入输出均为文本 |
| 文本拼接节点 | [workflow-nodes-text.md](workflow-nodes-text.md#文本拼接节点) | 输出**始终**为文本 |
| 数据类型转换器节点 | [workflow-nodes-text.md](workflow-nodes-text.md#数据类型转换器节点) | 输出与转换目标类型一致 |
| Json 拼接节点 | [workflow-nodes-text.md](workflow-nodes-text.md#json-拼接节点) | 输出为 json（非 json/数组），字段名不支持嵌套 |
| Json 解析节点 | [workflow-nodes-text.md](workflow-nodes-text.md#json-解析节点) | 输入输出数组属性**必须**一致 |

### 文档处理节点

| 节点类型 | 详细文档 | 核心要点 |
|---------|---------|---------|
| 文档解析节点 | [workflow-setup.md](workflow-setup.md#文档处理节点) | 输入为文档，输出为文本 |
| Word/Excel/自定义文档生成节点 | [workflow-setup.md](workflow-setup.md#文档处理节点) | 输出为文档 |
| Excel 读取节点 | [workflow-setup.md](workflow-setup.md#文档处理节点) | 输出为 json 或 json/数组 |

### 搜索与数据节点

| 节点类型 | 详细文档 | 核心要点 |
|---------|---------|---------|
| 联网搜索节点 | [workflow-setup.md](workflow-setup.md#搜索与数据节点) | 输出为 json 或文本 |
| 网页信息获取节点 | [workflow-setup.md](workflow-setup.md#搜索与数据节点) | 输入为超链接或文本 |
| SQL 生成节点 | [workflow-setup.md](workflow-setup.md#搜索与数据节点) | 输出为文本（SQL 语句） |
| 数据库 SQL 查询节点 | [workflow-setup.md](workflow-setup.md#搜索与数据节点) | 输出为 json 或 json/数组 |

### 可视化节点

| 节点类型 | 详细文档 | 核心要点 |
|---------|---------|---------|
| 图表生成节点 | [workflow-setup.md](workflow-setup.md#可视化节点) | 输入为 json 或 json/数组，输出为图表 |

### 输入输出节点

| 节点类型 | 详细文档 | 核心要点 |
|---------|---------|---------|
| 输入节点 | [workflow-setup.md](workflow-setup.md#输入输出节点) | 支持所有 18 种变量类型 |
| 输出节点 | [workflow-setup.md](workflow-setup.md#输入输出节点) | 支持所有 18 种变量类型 |

***

## 📋 节点连接兼容性速查表

### 快速查询：这个节点的输出可以连接到哪个节点的输入？

| 源节点                 | 输出类型              | 可连接的目标节点                            |
| ------------------- | ----------------- | ----------------------------------- |
| Agent 节点            | `文本`              | LLM、文本处理、数据类型转换、知识问答、条件判断、Python 代码 |
| LLM 节点              | `文本`              | 同上                                  |
| 知识问答节点              | `文本`              | 同上                                  |
| 智能表格检索              | `json/数组`         | 循环处理、Json 解析、Python 代码、Json 拼接      |
| 添加知识                | `知识/数组`           | 知识问答、知识检索、知识片段排序                    |
| 关键词识别               | `文本/数组`           | 循环处理、文本拼接、Python 代码                 |
| Json 解析（输入 json）    | `文本`/`json`       | 取决于输出类型                             |
| Json 解析（输入 json/数组） | `文本/数组`/`json/数组` | 取决于输出类型                             |
| Python 代码           | 取决于配置             | 取决于输出类型                             |

### 常见连接模式

```
模式 1：知识检索增强
输入文档 → 添加知识（输出：知识/数组） → 知识问答（输入：文本，输出：文本） → 输出

模式 2：数据检索处理
智能表格检索（输出：json/数组） → 循环处理 → Json 解析 → 文本拼接 → 输出

模式 3：格式转换
LLM（输出：文本） → 数据类型转换（文本→json） → Json 解析 → 输出

模式 4：数组处理
文本/数组 → 循环处理（输入必须是数组） → [循环体内节点] → 输出（文本/数组）
```

***

## ⚠️ 关键禁令（必须严格遵守）

### ❌ 绝对禁止的操作

1. **禁止猜测变量类型**：必须查阅此表确定类型
2. **禁止数组与非数组混用**：输入是数组时输出必须是数组，反之亦然
3. **禁止改变固定输出类型**：某些节点输出类型是固定的（如 Agent→文本），不得修改
4. **禁止循环节点输入非数组**：循环处理节点的输入 *必须* 是数组类型
5. **禁止 Json 拼接使用嵌套字段**：字段名只能是单层，如 `name`，不能是 `user.name`
6. **禁止智能表格检索不限制行数**：必须指定正整数（1、10、100 等）

***

## ✅ 必须遵循的检查清单

在完成工作流设计后，必须逐项检查：

- [ ] 所有节点的输入类型与前一个节点的输出类型匹配
- [ ] 数组类型输入连接到数组类型输出
- [ ] 非数组类型输入连接到非数组类型输出
- [ ] 固定输出类型的节点（如 Agent、LLM）正确使用
- [ ] 循环处理节点的输入是数组类型
- [ ] Json 解析节点的输出数组属性与输入一致
- [ ] 智能表格检索指定了最大输出行数
- [ ] 变量命名使用 `类型：变量名` 格式
- [ ] 所有引用的变量在工作流中已定义

***

**版本**: v2.0 | **更新**: 2026-03-12 | **状态**: 🔴 强制执行

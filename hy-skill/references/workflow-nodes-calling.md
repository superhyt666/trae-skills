# 调用类节点详细文档

## 📋 概述

调用类节点用于调用外部服务、代码或已有的 Agent/工作流，实现工作流与外部系统或复杂逻辑的交互。

---

## 🤖 Agent 节点

### 功能说明
调用已配置的 Agent，复用已有的 Agent 能力。

### 输入输出

**输入变量**:
- `问题内容`: 文本/文本数组/JSON/Markdown 类型，Agent 的输入问题
- `Agent`: 从已配置的 Agent 列表中选择

**输出变量**:
- `文本：variable_name` - Agent 的执行结果（始终为文本类型）

### 配置步骤

1. **前置准备**: 使用 Agent 提示词模块设计并配置 Agent
2. **选择 Agent**: 从下拉列表选择已配置的 Agent
3. **设置输入**: 配置问题内容（支持变量引用）
4. **设置输出**: 指定输出变量名

### 典型示例

**示例 1: 智能客服**
```
节点名称：智能客服回答
输入变量:
  - 问题内容：user_question (文本类型)
  - Agent: 电商客服 Agent
输出变量：文本：customer_reply
```

**示例 2: 数据分析**
```
节点 1: 智能表格检索 → 输出 json/数组：search_result
节点 2: 文本拼接 → 输出 文本：data_summary
节点 3: Agent 分析
  - 问题内容：data_summary
  - Agent: 数据分析助手 Agent
输出变量：文本：analysis_conclusion
```

### 应用场景
- 智能客服工作流
- 数据分析工作流
- 文档问答工作流
- 内容创作工作流

### 注意事项
1. Agent 节点输出始终为文本类型
2. 需先在平台中配置好 Agent
3. 支持文本、JSON、Markdown 三种输入类型

---

## 🔗 工作流节点

### 功能说明
调用子工作流，实现复杂工作流的模块化设计。

### 输入输出

**输入变量**:
- 取决于被调用的子工作流定义
- 类型和数量与子工作流一致

**输出变量**:
- 取决于被调用的子工作流定义
- 类型和数量与子工作流一致

### 配置步骤

1. **创建子工作流**: 预先创建并保存子工作流
2. **选择子工作流**: 从列表选择要调用的工作流
3. **配置输入映射**: 映射主工作流变量到子工作流输入
4. **配置输出**: 指定输出变量名（与子工作流输出一致）

### 典型示例

**示例 1: 文本翻译子工作流**
```
子工作流定义:
  - 输入：文本：source_text
  - 输出：文本：translated_text

主工作流中的工作流节点:
  - 调用子工作流：文本翻译工作流
  - 输入变量：文本：input_content
  - 输出变量：文本：translation_result
```

**示例 2: 数据分析子工作流**
```
子工作流定义:
  - 输入：json/数组：data_list, 文本：analysis_type
  - 输出：json: statistics, 文本：conclusion

主工作流中的工作流节点:
  - 调用子工作流：数据分析工作流
  - 输入变量：json/数组：order_data, 文本：type
  - 输出变量：json: stats_result, 文本：analysis_conclusion
```

### 应用场景
- 模块化设计通用功能
- 多个工作流复用同一功能
- 构建大型工作流系统
- 团队协作开发

### 注意事项
1. 输入输出类型必须与子工作流定义完全一致
2. 避免循环依赖
3. 子工作流执行失败会影响主工作流

---

## 🐍 Python 代码执行节点

### 功能说明
运行自定义 Python 代码，实现复杂的数据处理逻辑。

### 输入输出

**输入变量**:
- 支持任意类型的变量，由用户根据代码需求定义
- 例如：`文本：input_text`、`json/数组：data_list`

**输出变量**:
- 支持任意类型的变量，由用户根据代码返回值定义
- 例如：`文本：result`、`json: processed_data`

### 代码规范

- 直接使用变量名访问输入和输出
- 无需函数定义，直接编写处理逻辑
- 支持 Python 标准库
- 建议添加异常处理

### 典型示例

**示例 1: 文本处理**
```
节点名称：文本格式化
输入变量:
  - 文本：raw_text
输出变量:
  - 文本：formatted_text

代码:
formatted_text = raw_text.strip().title()
```

**示例 2: 数据筛选**
```
节点名称：数据筛选
输入变量:
  - json/数组：data_list
  - 文本：filter_key
输出变量:
  - json/数组：filtered_data

代码:
filtered_data = [item for item in data_list if filter_key in item]
```

**示例 3: 复杂数据转换**
```
节点名称：订单数据转换
输入变量:
  - json/数组：orders
输出变量:
  - 文本：summary_text
  - json: statistics

代码:
try:
    total_amount = sum(order.get('amount', 0) for order in orders)
    order_count = len(orders)
    avg_amount = total_amount / order_count if order_count > 0 else 0
    
    summary_text = f"共{order_count}个订单，总金额{total_amount:.2f}元，平均{avg_amount:.2f}元"
    
    statistics = {
        "total": total_amount,
        "count": order_count,
        "average": avg_amount
    }
except Exception as e:
    summary_text = f"处理失败：{str(e)}"
    statistics = {"error": str(e)}
```

### 应用场景
- 数据清洗和格式转换
- 统计分析和聚合计算
- 自定义业务逻辑
- 批量数据处理

### 注意事项
1. 变量命名使用英文，避免中文变量名
2. 添加异常处理保证稳定性
3. 避免耗时操作影响执行效率
4. 不要执行危险操作（文件系统、网络请求等）

---

## 🌐 HTTP 技能节点

### 功能说明
调用 HTTP 请求，对接外部 API 服务。

### 输入输出

**输入变量**:
- HTTP 请求相关参数（URL、方法、headers、body 等）

**输出变量**:
- `json：variable_name` - HTTP 响应结果（始终为 json 类型）

### 配置要点

1. **请求方法**: GET/POST/PUT/DELETE 等
2. **请求 URL**: 完整的 API 地址
3. **请求头**: Content-Type、Authorization 等
4. **请求体**: JSON、表单等格式

### 应用场景
- 调用第三方 API
-  webhook 通知
- 数据同步
- 外部系统集成

---

## 🧠 LLM 节点

### 功能说明
调用大语言模型（支持 8B 和 32B 模型），实现内容生成、文本分析等功能。

### 输入输出

**输入变量**:
- `prompt`: 文本类型，模型的输入提示词

**输出变量**:
- `文本：variable_name` - LLM 生成的文本内容

### 配置要点

1. **选择模型**: 8B 或 32B 模型
2. **设置创造性级别**: 控制输出的随机性
3. **配置 prompt**: 支持变量引用
4. **设置输出变量**: 指定变量名保存结果

### 典型示例

**示例 1: 内容生成**
```
节点名称：文章标题生成
输入变量:
  - prompt: "为以下主题生成 5 个吸引人的标题：@topic"
输出变量：文本：titles
```

**示例 2: 文本分析**
```
节点名称：情感分析
输入变量:
  - prompt: "分析以下文本的情感倾向（正面/负面/中性）：@comment_text"
输出变量：文本：sentiment
```

### 应用场景
- 内容创作和文案生成
- 文本摘要和总结
- 情感分析和分类
- 问答和对话

---

## 🔗 与其他节点配合

### 典型工作流模式

1. **数据检索 → 处理 → 生成**
   ```
   智能表格检索 → Python 处理 → LLM 生成报告
   ```

2. **条件判断 → 分支处理**
   ```
   条件判断 → [分支 1: Agent 处理] / [分支 2: LLM 处理]
   ```

3. **循环处理 → 批量调用**
   ```
   循环处理 → 逐个调用 HTTP 技能
   ```

4. **模块化调用**
   ```
   主工作流 → 工作流节点（子工作流） → 输出
   ```

---

## 💡 最佳实践

1. **Agent 复用**: 将通用能力封装为 Agent，多个工作流复用
2. **子工作流模块化**: 复杂功能拆分为子工作流
3. **Python 代码简洁**: 保持代码简洁，避免复杂嵌套
4. **错误处理**: 添加 try-except 处理异常
5. **API 限流**: 注意外部 API 的调用频率限制

---

## 📚 相关文档

- [主文档](./workflow-setup.md) - 工作流搭建指南
- [流程控制节点](./workflow-nodes-control.md) - 条件判断、循环处理等
- [文本处理节点](./workflow-nodes-text.md) - 文本拼接、Json 解析等

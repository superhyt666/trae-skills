# Python 代码生成规范

本文档定义了 hy-skill 生成的 Python 代码必须遵循的技术规范和最佳实践。

## 目录

0. [代码交付流程](#0-代码交付流程)
1. [函数结构规范](#1-函数结构规范)
2. [代码质量要求](#2-代码质量要求)
3. [异常处理机制](#3-异常处理机制)
4. [输入输出处理](#4-输入输出处理)
5. [代码模板](#5-代码模板)
6. [常见错误示例](#6-常见错误示例)

---

## 0. 代码交付流程

### 0.1 两段式交付模式

hy-skill 采用**两段式交付流程**，确保代码质量和规范性：

#### 阶段 1：开发测试版（内部使用）

**目标：** 全面功能验证，确保代码逻辑正确

**代码特征：**
- ✅ 包含 `if __name__ == "__main__":` 入口
- ✅ 包含完整的测试用例和测试数据
- ✅ 可以使用 `print()` 输出调试信息
- ✅ 可以包含输入初始化和测试逻辑
- ✅ 验证所有功能路径和异常处理

**适用场景：**
- 开发阶段的功能验证
- 交付前的全面测试
- 调试和问题排查

**示例代码：**
```python
"""数据处理模块 - 开发测试版"""

import json


def process_request(input_data):
    """处理请求的主函数"""
    try:
        data = parse_input(input_data)
        result = business_logic(data)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def parse_input(input_data):
    """解析输入数据"""
    if isinstance(input_data, str):
        return json.loads(input_data)
    return input_data


def business_logic(data):
    """业务逻辑实现"""
    return {"status": "success", "data": data}


def test_process_request():
    """测试函数 - 仅在开发阶段使用"""
    # 测试用例 1：正常输入
    test_input = {"key": "value"}
    result = process_request(test_input)
    print(f"测试 1 - 正常输入：{result}")
    assert "success" in result
    
    # 测试用例 2：边界条件
    test_input = {}
    result = process_request(test_input)
    print(f"测试 2 - 空对象：{result}")
    
    # 测试用例 3：异常处理
    try:
        result = process_request(None)
        print(f"测试 3 - 异常处理：{result}")
    except Exception as e:
        print(f"测试 3 - 捕获异常：{e}")
    
    print("✅ 所有测试通过！")


if __name__ == "__main__":
    # 执行测试
    test_process_request()
```

---

#### 阶段 2：交付展示版（交付用户）

**目标：** 符合平台规范，清晰展示调用方式

**代码特征：**
- ❌ 移除 `if __name__ == "__main__":` 结构
- ❌ 移除所有测试函数和测试数据
- ❌ 移除所有 `print()` 语句
- ❌ 移除输入初始化逻辑
- ✅ 保留详细注释标注的调用示例
- ✅ 保留核心功能实现
- ✅ 使用占位符（如 `user_input`）展示调用方式

**适用场景：**
- 交付给最终用户
- 部署到生产环境
- 集成到工作流平台

**示例代码：**
```python
"""数据处理模块 - 交付展示版

功能：解析输入数据并执行业务逻辑处理
输入：JSON 字符串或 dict 对象
输出：JSON 格式的处理结果
"""

import json
from typing import Any, Dict


def process_request(input_data: Any) -> str:
    """处理请求的主函数。
    
    Args:
        input_data: 输入数据（字符串或 dict/list）
        
    Returns:
        JSON 格式的处理结果
        
    Raises:
        ValueError: 当输入格式不正确时
        Exception: 处理过程中的其他异常
    """
    try:
        # 1. 解析输入
        data = parse_input(input_data)
        
        # 2. 业务处理
        result = business_logic(data)
        
        # 3. 序列化输出
        return json.dumps(result, ensure_ascii=False)
    
    except Exception as e:
        # 异常处理并返回错误响应
        return json.dumps({
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "context": "process_request 执行失败"
            }
        }, ensure_ascii=False)


def parse_input(input_data: Any) -> Any:
    """解析输入数据。
    
    支持以下输入格式：
    - JSON 字符串：自动解析为 dict/list
    - Python dict/list: 直接返回
    
    Args:
        input_data: 输入数据
        
    Returns:
        解析后的 Python 对象
        
    Raises:
        json.JSONDecodeError: 当 JSON 解析失败时
    """
    if isinstance(input_data, (dict, list)):
        return input_data
    
    if isinstance(input_data, str):
        return json.loads(input_data)
    
    raise TypeError(f"不支持的输入类型：{type(input_data)}")


def business_logic(data: Any) -> Dict[str, Any]:
    """业务逻辑实现。
    
    Args:
        data: 已解析的输入数据
        
    Returns:
        包含处理结果的字典
    """
    # 实现具体的业务处理逻辑
    return {
        "status": "success",
        "data": data,
        "message": "处理完成"
    }


# ============================================================================
# 调用示例（可在平台上取消注释使用）
# ============================================================================
# 平台调用方式：
# result = process_request(user_input)
#
# 参数说明：
# - user_input: 平台传入的输入数据
#   - 该变量名需要与平台配置的输入变量名一致
#   - 平台会自动将实际输入值映射到该变量
#   - 支持格式：
#     * JSON 字符串：'{"key": "value"}'
#     * Python 对象：{"key": "value"}
#
# 返回值说明：
# - result: JSON 格式的处理结果字符串
#   - 成功示例：{"status": "success", "data": {...}}
#   - 失败示例：{"error": {"type": "ErrorType", "message": "错误信息"}}
#
# 使用说明：
# 1. 在平台代码编辑器中，可以取消注释此行来使用
# 2. 确保平台配置的输入变量名为 "user_input"
# 3. 如果平台输入变量名不同，请相应修改调用示例
# 4. 输出通过返回值提供，不要使用 print 语句
# ============================================================================
```

---

### 0.2 代码转换规则

**从开发测试版转换为交付展示版的操作步骤：**

#### 步骤 1：移除测试代码

```python
# ❌ 删除以下部分：

def test_xxx():
    """测试函数"""
    # 所有测试代码

if __name__ == "__main__":
    # 所有测试执行代码
    test_xxx()
```

#### 步骤 2：移除 print 语句

```python
# ❌ 删除所有 print 语句：
print(f"调试信息：{value}")
print("测试通过")

# ✅ 如果需要日志，使用 logging 模块（如果平台支持）
# import logging
# logging.info("信息")
```

#### 步骤 3：移除输入初始化

```python
# ❌ 删除：
test_data = "具体值"
user_input = test_data
result = process_function(user_input)

# ✅ 保留调用示例（注释形式）：
# result = process_function(user_input)
```

#### 步骤 4：添加详细注释

```python
# ✅ 在代码末尾添加：

# ============================================================================
# 调用示例（仅供参考，请勿取消注释）
# ============================================================================
# result = main_function(user_input)
#
# 参数说明：
# - user_input: 平台传入的输入数据
#
# 返回值说明：
# - result: JSON 格式的处理结果
# ============================================================================
```

#### 步骤 5：验证核心功能

```python
# ✅ 确保保留以下内容：
# - 主处理函数（入口函数）
# - 所有辅助函数
# - 异常处理逻辑
# - 输入输出处理逻辑
# - 函数文档字符串（docstring）
```

---

### 0.3 质量检查清单

#### 开发测试阶段检查

在交付前，必须完成以下测试：

- [ ] **正常输入场景**：使用有效输入数据验证功能
- [ ] **边界条件**：测试空值、极限值等边界情况
- [ ] **异常处理**：验证错误输入能否正确捕获
- [ ] **输出格式**：确认输出符合平台要求（JSON/文本）
- [ ] **代码覆盖率**：确保所有代码路径都被测试
- [ ] **性能测试**：验证大数据量下的性能表现

#### 交付转换阶段检查

在交付给用户前，必须完成以下检查：

- [ ] **测试代码移除**：已删除所有测试函数
- [ ] **main 入口移除**：已删除 `if __name__ == "__main__":`
- [ ] **print 语句移除**：已删除所有调试输出
- [ ] **输入初始化移除**：已删除测试数据赋值
- [ ] **调用示例添加**：已添加详细的注释说明
- [ ] **占位符使用**：使用 `user_input` 等占位符
- [ ] **注释正确性**：调用示例已正确注释
- [ ] **核心功能完整**：所有业务逻辑代码保留
- [ ] **文档字符串完整**：所有函数都有 docstring
- [ ] **PEP 8 规范**：代码格式符合规范
- [ ] **导入语句检查**：所有必要的导入都已添加

---

### 0.4 最佳实践建议

#### 开发阶段建议

1. **编写全面的测试用例**
   - 覆盖正常场景、边界场景、异常场景
   - 使用断言验证结果正确性
   - 记录测试数据和预期结果

2. **使用 print 进行调试**
   - 输出关键变量的值
   - 跟踪代码执行流程
   - 验证异常处理逻辑

3. **逐步验证功能**
   - 先测试核心功能
   - 再测试辅助功能
   - 最后测试集成流程

#### 交付阶段建议

1. **代码清理**
   - 删除所有调试代码
   - 删除注释掉的无用代码
   - 优化代码格式

2. **文档完善**
   - 添加模块级文档字符串
   - 完善函数 docstring
   - 提供清晰的调用示例

3. **代码审查**
   - 检查是否有遗漏的测试代码
   - 验证异常处理是否完整
   - 确认输入输出格式正确

---

## 1. 函数结构规范

### 1.1 单一职责原则

每个函数应只负责一项具体任务，避免函数承担过多职责。

**✅ 正确示例:**
```python
import json


def parse_input(input_data):
    """解析输入数据"""
    if isinstance(input_data, str):
        return json.loads(input_data)
    return input_data


def transform_data(data):
    """转换数据"""
    # 实现具体的转换逻辑
    return {"processed": True, "data": data}


def serialize_output(result):
    """序列化输出结果"""
    return json.dumps(result, ensure_ascii=False)
```

**❌ 错误示例:**
```python
# 错误：import 语句在函数内部
def process_everything(input_data):
    """一个函数做所有事情"""
    # 解析输入
    if isinstance(input_data, str):
        import json  # ❌ import 应该在文件顶部
        data = json.loads(input_data)
    else:
        data = input_data
    
    # 处理数据
    result = {"processed": True, "data": data}
    
    # 序列化输出
    import json  # ❌ import 应该在文件顶部
    output = json.dumps(result, ensure_ascii=False)
    
    return output
```

### 1.2 显式函数调用

必须采用显式函数调用方式，清晰地展示函数执行流程。

**✅ 正确示例:**
```python
def main_workflow(input_data):
    """主工作流程"""
    try:
        # 步骤 1: 解析输入
        data = parse_input(input_data)
        
        # 步骤 2: 验证数据
        validation_result = validate_data(data)
        if not validation_result["valid"]:
            return create_error_response("数据验证失败", validation_result["message"])
        
        # 步骤 3: 处理数据
        processed_data = transform_data(data)
        
        # 步骤 4: 序列化输出
        output = serialize_output(processed_data)
        
        return output
    
    except Exception as e:
        return handle_exception(e, "main_workflow")


# 函数调用示例 (仅展示调用方式，不执行):
# result = main_workflow(user_input)
```

**❌ 错误示例:**
```python
# 错误 1: 包含具体的输入值
# result = process_data("hello world")  # ❌ 不应包含具体值

# 错误 2: 使用 print 语句
# print(result)  # ❌ 禁止使用 print

# 错误 3: 包含输入初始化逻辑
input_data = "test"  # ❌ 不允许在代码中初始化输入
result = process_data(input_data)
print(result)  # ❌ 禁止使用 print 输出
```

**重要说明:**
- 函数调用示例只能使用 `user_input` 作为参数占位符
- 禁止使用具体的输入值 (如 `"hello world"`)
- 函数调用示例必须注释掉，仅作为说明
- 绝对禁止出现 `print()` 语句

### 1.3 禁止 main 函数结构

**❌ 错误示例:**
```python
def main():
    """主函数 - 不允许这样写"""
    input_data = get_input()  # 不允许在代码中初始化输入
    result = process(input_data)
    # 禁止使用 print 输出结果

# 禁止出现 if __name__ == "__main__": 结构
```

**✅ 正确示例:**
```python
def process_request(input_data):
    """处理请求 - 输入由平台外部传入"""
    try:
        result = business_logic(input_data)
        return serialize(result)
    except Exception as e:
        return create_error_response(str(e), "process_request")


def business_logic(data):
    """业务逻辑实现"""
    # 实现具体的业务处理
    return {"status": "success", "data": data}


# 函数调用示例 (仅展示调用方式):
# result = process_request(user_input)
```

### 1.4 输入输出规范

#### 输入规范

- **输入来源**: 由平台外部传入函数参数
- **变量命名**: 函数参数名必须与平台配置的输入变量名一致
- **禁止行为**: 代码中不得包含输入初始赋值逻辑

**示例：**
```python
# ✅ 正确：参数名与平台输入变量名一致
def process_request(input_text):
    # input_text 由平台自动提供
    pass

# ❌ 错误：参数名不匹配
def process_request(data):  # 平台配置的是 input_text
    pass

# ❌ 错误：在代码中初始化输入
def process_request(input_text):
    input_text = "默认值"  # 不允许
    pass
```

#### 输出规范（关键）

⚠️ **重要：平台期望返回 Python 对象，不是 JSON 字符串**

- **返回类型**: 必须返回 Python 对象（dict、list、str、int、float、bool 或 None）
- **禁止行为**: 禁止使用 `json.dumps()` 序列化返回值
- **平台处理**: 平台会根据输出格式设置自动处理序列化

**输出格式说明：**

| 输出格式 | 平台期望的返回类型 | 平台处理方式 |
|---------|------------------|-------------|
| 文本 | 任意 Python 对象 | 转换为文本显示 |
| JSON | dict 或 list | 序列化为 JSON 字符串 |
| JSON 数组 | list | 验证并序列化为 JSON 数组 |

**示例：**
```python
# ✅ 正确：返回 Python 对象
def process_request(input_text):
    result = {"status": "success", "data": [1, 2, 3]}
    return result  # 直接返回 dict 对象

# ❌ 错误：返回 JSON 字符串
def process_request(input_text):
    import json
    result = {"status": "success", "data": [1, 2, 3]}
    return json.dumps(result)  # 不要序列化！

# ✅ 正确：返回 list 对象
def convert_to_array(input_text):
    return [1, 2, 3]  # 直接返回 list

# ❌ 错误：返回字符串形式的数组
def convert_to_array(input_text):
    return "[1, 2, 3]"  # 不要返回字符串
```

#### 输入输出处理最佳实践

```python
import json


def process_request(input_text):
    """处理请求的主函数。
    
    Args:
        input_text: 平台传入的输入数据（字符串类型）
        
    Returns:
        Python 对象（dict、list 或其他平台支持的类型）
    """
    try:
        # 1. 解析输入（如果需要）
        data = json.loads(input_text) if isinstance(input_text, str) else input_text
        
        # 2. 业务处理
        result = business_logic(data)
        
        # 3. 返回 Python 对象（不是 JSON 字符串）
        return result  # ✅ 直接返回对象
    
    except Exception as e:
        # 错误处理也返回 dict 对象
        return {
            "error": True,
            "message": str(e),
            "context": "处理失败"
        }
```

### 1.5 函数调用示例规范

**重要规则:**

1. **使用占位符**: 函数调用示例必须使用 `user_input` 作为参数占位符
   ```python
   # ✅ 正确：使用 user_input
   # result = myfunction(user_input)
   ```

2. **禁止具体值**: 不得使用具体的输入值
   ```python
   # ❌ 错误：使用具体值
   # result = myfunction("hello world")  # 不允许
   ```

3. **必须注释**: 函数调用示例必须注释掉，仅作为说明
   ```python
   # ✅ 正确：注释掉的调用示例
   # result = process_data(user_input)
   ```

4. **禁止 print**: 绝对禁止出现 print() 语句
   ```python
   # ❌ 错误：使用 print
   print(result)  # 绝对禁止
   ```

5. **简洁说明**: 如有需要，可以添加简短说明
   ```python
   # 函数调用示例 (仅展示调用方式):
   # result = process_data(user_input)
   ```

---

## 2. 代码质量要求

### 2.1 PEP 8 编码规范

#### 2.1 PEP 8 编码规范

#### 命名规范
- 函数名：小写字母 + 下划线，如 `process_data()`
- 变量名：小写字母 + 下划线，如 `user_input`
- 常量名：大写字母 + 下划线，如 `MAX_RETRIES`
- 类名：大驼峰命名，如 `DataProcessor`

#### 代码格式
- 缩进：4 个空格 (不使用 Tab)
- 行宽：不超过 79 个字符
- 空行：函数之间空 2 行，逻辑块之间空 1 行

#### 导入语句规范（重要）
- ✅ **必须位置**: 所有 `import` 语句必须放在文件顶部（在模块文档字符串之后）
- ❌ **禁止行为**: 禁止在函数内部使用 `import` 语句
- 格式：每个导入单独一行，标准库在前，第三方库在后
- 顺序：Python 标准库 → 第三方库 → 本地模块

**✅ 正确示例:**
```python
"""模块说明文档"""

import json
from typing import Any, Dict

# 第三方库
import requests


def process_data(input_data):
    """函数实现 - 不需要在内部 import"""
    # 直接使用 json，不需要 import
    pass
```

**❌ 错误示例:**
```python
"""模块说明文档"""


def process_data(input_data):
    """函数实现"""
    import json  # ❌ 错误：import 在函数内部
    return json.loads(input_data)
```

**✅ 正确示例:**
```python
import json
from typing import Any, Dict, Optional


def process_user_data(
    user_input: str,
    config: Optional[Dict[str, Any]] = None
) -> str:
    """处理用户数据。
    
    Args:
        user_input: 用户输入的字符串
        config: 可选的配置字典
        
    Returns:
        JSON 格式的处理结果
    """
    # 实现逻辑
    pass
```

### 2.2 代码简洁性

避免冗余操作，保持代码简洁高效。

**✅ 正确示例:**
```python
def get_user_name(user_id: str) -> str:
    """获取用户名称"""
    if not user_id:
        raise ValueError("用户 ID 不能为空")
    
    user_data = fetch_user(user_id)
    return user_data.get("name", "未知用户")
```

**❌ 错误示例:**
```python
def get_user_name(user_id: str) -> str:
    """获取用户名称"""
    # 冗余的空值检查
    if user_id is None:
        raise ValueError("用户 ID 不能为空")
    if user_id == "":
        raise ValueError("用户 ID 不能为空")
    if len(user_id) == 0:
        raise ValueError("用户 ID 不能为空")
    
    # 冗余的变量赋值
    temp_user_data = fetch_user(user_id)
    result_data = temp_user_data
    name_value = result_data.get("name")
    final_name = name_value if name_value is not None else "未知用户"
    
    return final_name
```

### 2.3 代码审查清单

每次代码修改后，必须检查:

- [ ] 函数是否符合单一职责原则
- [ ] 是否采用显式函数调用
- [ ] 是否没有 main 函数或 print 输出
- [ ] 异常处理是否完整
- [ ] 输入输出格式是否正确
- [ ] 代码是否符合 PEP 8 规范
- [ ] 是否有冗余或重复的代码
- [ ] 变量和函数命名是否清晰
- [ ] 是否添加了必要的文档字符串
- [ ] 错误信息是否包含足够的上下文
- [ ] 函数调用示例是否使用 `user_input` 占位符
- [ ] 函数调用示例是否已注释掉
- [ ] 是否没有使用具体的输入值 (如 "hello world")

---

## 3. 异常处理机制

### 3.1 异常处理策略

必须实现全面的异常处理，包括但不限于:

1. **参数类型验证**: 检查输入参数的类型是否符合预期
2. **边界条件处理**: 处理空值、空字符串、超出范围等边界情况
3. **资源访问异常**: 处理文件、网络、数据库等资源访问失败
4. **业务逻辑异常**: 处理业务规则违反、状态不一致等情况

### 3.2 try-except-finally 结构

使用 try-except-finally 结构确保代码健壮性。

**✅ 正确示例:**
```python
def process_file(file_path: str, encoding: str = "utf-8") -> str:
    """处理文件内容"""
    file_handle = None
    try:
        # 参数验证
        if not file_path or not isinstance(file_path, str):
            raise ValueError("文件路径必须是非空字符串")
        
        # 资源访问
        file_handle = open(file_path, "r", encoding=encoding)
        content = file_handle.read()
        
        # 业务处理
        result = analyze_content(content)
        
        # 序列化输出
        return json.dumps(result, ensure_ascii=False)
    
    except FileNotFoundError as e:
        error_msg = f"文件未找到：{file_path}"
        return create_error_response(error_msg, "FileNotFoundError", str(e))
    
    except UnicodeDecodeError as e:
        error_msg = f"文件编码错误，请使用正确的编码格式 (当前：{encoding})"
        return create_error_response(error_msg, "UnicodeDecodeError", str(e))
    
    except Exception as e:
        error_msg = f"处理文件时发生未知错误：{file_path}"
        return create_error_response(error_msg, "UnknownError", str(e))
    
    finally:
        # 资源清理
        if file_handle is not None:
            file_handle.close()
```

### 3.3 异常信息规范

异常信息应包含足够的上下文，便于问题定位。

**✅ 正确示例:**
```python
import json


def create_error_response(
    error_message: str,
    error_type: str,
    original_error: str = "",
    context: Optional[Dict[str, Any]] = None
) -> str:
    """创建错误响应"""
    error_response = {
        "success": False,
        "error": {
            "type": error_type,
            "message": error_message,
            "original_error": original_error,
            "timestamp": get_current_timestamp(),
            "context": context or {}
        }
    }
    
    return json.dumps(error_response, ensure_ascii=False)


def get_current_timestamp() -> str:
    """获取当前时间戳"""
    from datetime import datetime
    return datetime.now().isoformat()
```

**错误响应示例:**
```json
{
  "success": false,
  "error": {
    "type": "FileNotFoundError",
    "message": "文件未找到：/path/to/file.txt",
    "original_error": "[Errno 2] No such file or directory: '/path/to/file.txt'",
    "timestamp": "2026-03-04T20:30:00.123456",
    "context": {
      "file_path": "/path/to/file.txt",
      "encoding": "utf-8",
      "function": "process_file"
    }
  }
}
```

### 3.4 常见异常类型处理

```python
def robust_processor(input_data: Any) -> str:
    """健壮的处理器"""
    try:
        # 1. 参数类型验证
        if input_data is None:
            raise TypeError("输入数据不能为 None")
        
        # 2. 边界条件处理
        if isinstance(input_data, str) and len(input_data.strip()) == 0:
            raise ValueError("输入字符串不能为空")
        
        if isinstance(input_data, (list, dict)) and len(input_data) == 0:
            raise ValueError("输入集合不能为空")
        
        # 3. 数据解析
        try:
            data = parse_input(input_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失败：{str(e)}")
        
        # 4. 业务处理
        result = business_logic(data)
        
        # 5. 结果验证
        if result is None:
            raise RuntimeError("业务逻辑返回空结果")
        
        # 6. 序列化输出
        return serialize_output(result)
    
    except (TypeError, ValueError) as e:
        # 参数错误
        return create_error_response(
            str(e),
            "ParameterError",
            context={"input_type": type(input_data).__name__}
        )
    
    except json.JSONDecodeError as e:
        # JSON 解析错误
        return create_error_response(
            f"输入格式错误：{str(e)}",
            "JSONDecodeError",
            context={"input_sample": str(input_data)[:100]}
        )
    
    except Exception as e:
        # 未知错误
        return create_error_response(
            f"处理过程中发生错误：{str(e)}",
            "ProcessingError",
            str(e),
            context={"function": "robust_processor"}
        )
```

---

## 4. 输入输出处理

### 4.1 平台限制说明

工作流平台对用户输入和输出有以下限制:

- **输入格式**: 仅支持文本 (string) 或 JSON 格式
- **输出格式**: 仅支持文本 (string) 或 JSON 格式
- **数据转换**: 需要实现文本/JSON 与 Python 数据结构 (dict/list) 的双向转换

### 4.2 输入解析函数

```python
import json
from typing import Any, Dict


def parse_input(input_data: Any) -> Dict[str, Any]:
    """解析输入数据。
    
    支持以下输入格式:
    - JSON 字符串：自动解析为 dict/list
    - Python dict/list: 直接返回
    - 普通字符串：包装为 {"text": input_data}
    
    Args:
        input_data: 输入数据，可以是字符串、dict 或 list
        
    Returns:
        解析后的 Python 对象 (dict 或 list)
        
    Raises:
        ValueError: 当输入格式不正确时
        json.JSONDecodeError: 当 JSON 解析失败时
    """
    if input_data is None:
        raise ValueError("输入数据不能为 None")
    
    # 如果已经是 Python 对象，直接返回
    if isinstance(input_data, (dict, list)):
        return input_data
    
    # 如果是字符串，尝试解析为 JSON
    if isinstance(input_data, str):
        # 空字符串处理
        if not input_data or len(input_data.strip()) == 0:
            raise ValueError("输入字符串不能为空")
        
        # 尝试 JSON 解析
        try:
            return json.loads(input_data)
        except json.JSONDecodeError:
            # 如果不是 JSON，作为普通文本处理
            return {"text": input_data}
    
    # 其他类型，转换为字符串
    return {"text": str(input_data)}
```

### 4.3 输出序列化函数

```python
import json
from datetime import datetime, date
from decimal import Decimal
from typing import Any


def serialize_output(result: Any, pretty: bool = False) -> str:
    """序列化输出结果。
    
    将 Python 对象转换为 JSON 字符串，确保:
    - 中文字符正确显示 (ensure_ascii=False)
    - 支持美观格式化 (pretty 参数)
    - 处理特殊数据类型
    
    Args:
        result: 要序列化的 Python 对象
        pretty: 是否美化输出 (默认 False)
        
    Returns:
        JSON 格式的输出字符串
        
    Raises:
        TypeError: 当对象无法序列化时
    """
    
    def default_serializer(obj: Any) -> Any:
        """自定义序列化处理器"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, bytes):
            return obj.decode("utf-8", errors="replace")
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        raise TypeError(f"对象类型 {type(obj)} 无法序列化")
    
    try:
        if pretty:
            return json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                default=default_serializer
            )
        else:
            return json.dumps(
                result,
                ensure_ascii=False,
                default=default_serializer
            )
    
    except (TypeError, ValueError) as e:
        # 序列化失败，返回错误信息
        error_response = {
            "success": False,
            "error": {
                "type": "SerializationError",
                "message": f"结果序列化失败：{str(e)}",
                "result_type": type(result).__name__
            }
        }
        return json.dumps(error_response, ensure_ascii=False)
```

### 4.4 格式转换错误处理

```python
def safe_parse_input(input_data: Any) -> Dict[str, Any]:
    """安全的输入解析，包含完整的错误处理。
    
    Args:
        input_data: 输入数据
        
    Returns:
        解析后的数据或错误响应
    """
    try:
        return parse_input(input_data)
    
    except json.JSONDecodeError as e:
        error_msg = (
            f"JSON 格式解析失败。请检查输入格式是否正确。\n"
            f"错误详情：{str(e)}\n"
            f"输入样本：{str(input_data)[:200]}..."
        )
        raise ValueError(error_msg) from e
    
    except ValueError as e:
        error_msg = (
            f"输入值验证失败：{str(e)}\n"
            f"支持的输入格式：\n"
            f"  - JSON 字符串：'{\"key\": \"value\"}'\n"
            f"  - Python 对象：{{\"key\": \"value\"}}\n"
            f"  - 普通文本字符串"
        )
        raise ValueError(error_msg) from e
    
    except Exception as e:
        error_msg = (
            f"输入解析过程中发生未知错误：{str(e)}\n"
            f"输入类型：{type(input_data).__name__}\n"
            f"输入值：{str(input_data)[:100]}"
        )
        raise RuntimeError(error_msg) from e
```

---

## 5. 代码模板

### 5.1 基础模板

```python
"""
模块说明：[模块功能描述]
作者：[作者]
创建日期：[日期]

注意：本代码用于工作流平台，返回值必须是 Python 对象，不是 JSON 字符串
"""

import json
from typing import Any, Dict, List, Optional


def process_request(input_data: Any) -> Dict[str, Any]:
    """处理请求的主函数。
    
    Args:
        input_data: 输入数据（字符串或 dict/list）
        
    Returns:
        Python dict 对象（平台会自动处理序列化）
    """
    try:
        # 1. 解析输入
        data = parse_input(input_data)
        
        # 2. 验证数据
        validate_input(data)
        
        # 3. 业务处理
        result = business_logic(data)
        
        # 4. 返回 Python 对象（不是 JSON 字符串）
        return result
    
    except Exception as e:
        return handle_exception(e, "process_request")


def parse_input(input_data: Any) -> Any:
    """解析输入数据"""
    if isinstance(input_data, (dict, list)):
        return input_data
    
    if isinstance(input_data, str):
        if not input_data.strip():
            raise ValueError("输入字符串不能为空")
        try:
            return json.loads(input_data)
        except json.JSONDecodeError:
            return {"text": input_data}
    
    return {"text": str(input_data)}


def validate_input(data: Any) -> None:
    """验证输入数据"""
    if data is None:
        raise ValueError("输入数据不能为空")
    
    if isinstance(data, dict):
        # 添加具体的验证逻辑
        pass


def business_logic(data: Any) -> Any:
    """业务逻辑实现"""
    # TODO: 实现具体的业务处理
    return {"status": "success", "data": data}


def handle_exception(exception: Exception, function_name: str) -> Dict[str, Any]:
    """处理异常并返回错误响应。
    
    Returns:
        dict 对象（不是 JSON 字符串）
    """
    return {
        "success": False,
        "error": {
            "type": type(exception).__name__,
            "message": str(exception),
            "function": function_name
        }
    }


# ============================================================================
# 调用示例（可在平台上取消注释使用）
# ============================================================================
# result = process_request(user_input)
#
# 参数说明：
# - user_input: 平台传入的输入数据（变量名必须与平台配置一致）
#
# 返回值说明：
# - result: Python 对象（dict 或 list）
#   - 平台会根据输出格式设置自动处理序列化
#   - 不要使用 json.dumps() 序列化返回值
# ============================================================================
```

### 5.2 数据处理模板

```python
"""数据处理模块

注意：返回值必须是 Python 对象，不是 JSON 字符串
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime


def transform_data_pipeline(input_data: Any) -> Dict[str, Any]:
    """数据处理管道。
    
    执行完整的数据处理流程:
    1. 输入解析
    2. 数据清洗
    3. 数据转换
    4. 结果验证
    5. 返回 Python 对象
    
    Args:
        input_data: 输入数据
        
    Returns:
        Python dict 对象（平台会自动处理序列化）
    """
    try:
        # 解析输入
        raw_data = parse_input(input_data)
        
        # 数据清洗
        cleaned_data = clean_data(raw_data)
        
        # 数据转换
        transformed_data = transform_data(cleaned_data)
        
        # 结果验证
        validation_result = validate_result(transformed_data)
        if not validation_result["valid"]:
            return create_error_response(
                "数据验证失败",
                "ValidationError",
                validation_result["errors"]
            )
        
        # 添加元数据
        final_result = {
            "success": True,
            "data": transformed_data,
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "record_count": len(transformed_data) if isinstance(transformed_data, list) else 1
            }
        }
        
        # 返回 Python 对象（不是 JSON 字符串）
        return final_result
    
    except Exception as e:
        return handle_exception(e, "transform_data_pipeline")


def clean_data(data: Any) -> Any:
    """清洗数据"""
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [item for item in data if item is not None]
    return data


def transform_data(data: Any) -> Any:
    """转换数据"""
    # 实现具体的转换逻辑
    return data


def validate_result(result: Any) -> Dict[str, Any]:
    """验证结果"""
    errors = []
    
    if result is None:
        errors.append("结果为空")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


# 函数调用示例 (仅展示调用方式):
# result = transform_data_pipeline(user_input)
```

---

## 6. 常见错误示例

### 6.1 错误：使用 print 输出

**❌ 错误:**
```python
def process(data):
    result = data * 2
    print(result)  # 错误：使用 print 输出
```

**✅ 正确:**
```python
def process(data):
    result = data * 2
    return json.dumps({"result": result})  # 正确：通过返回值输出


# 函数调用示例 (仅展示调用方式):
# result = process(user_input)
```

### 6.2 错误：包含输入初始化

**❌ 错误:**
```python
def process():
    data = "initial value"  # 错误：在代码中初始化输入
    result = data.upper()
    return result
```

**✅ 正确:**
```python
def process(data):  # 正确：通过参数接收输入
    result = data.upper()
    return json.dumps({"result": result})


# 函数调用示例 (仅展示调用方式):
# result = process(user_input)
```

### 6.3 错误：缺少异常处理

**❌ 错误:**
```python
def parse_json(text):
    return json.loads(text)  # 没有异常处理
```

**✅ 正确:**
```python
def parse_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败：{str(e)}") from e
```

### 6.4 错误：异常信息不完整

**❌ 错误:**
```python
try:
    process_data(data)
except Exception as e:
    return json.dumps({"error": "出错了"})  # 错误信息不完整
```

**✅ 正确:**
```python
try:
    process_data(data)
except Exception as e:
    return json.dumps({
        "error": {
            "type": type(e).__name__,
            "message": str(e),
            "context": "process_data 执行失败"
        }
    })
```

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|-----|------|---------|
| 1.0 | 2026-03-04 | 初始版本，包含完整的 Python 代码生成规范 |

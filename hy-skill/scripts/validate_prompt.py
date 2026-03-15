import re
import sys
import json
from typing import Dict, List, Any, Optional
from pathlib import Path


REQUIRED_FIELDS = {
    "智能会话 Agent": ["模型", "创造性", "提示词"],
    "知识检索 Agent": ["模型", "知识库", "答复模式"],
}


OPTIONAL_FIELDS = {
    "智能会话 Agent": ["温度", "最大令牌", "系统提示词"],
    "知识检索 Agent": ["上下文记忆", "问题分析", "问题聚焦", "答复质量模式"],
}


class PromptValidator:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, prompt_data: str, agent_type: str = "") -> Dict[str, Any]:
        self.errors = []
        self.warnings = []
        
        if isinstance(prompt_data, str):
            try:
                prompt_data = json.loads(prompt_data)
            except json.JSONDecodeError:
                pass
        
        if isinstance(prompt_data, dict):
            self._validate_json_format(prompt_data, agent_type)
        else:
            self._validate_markdown_format(str(prompt_data), agent_type)
        
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }
    
    def _validate_json_format(self, data: Dict, agent_type: str):
        if not agent_type:
            agent_type = data.get("type", "")
        
        required = REQUIRED_FIELDS.get(agent_type, [])
        for field in required:
            if field not in data:
                self.errors.append(f"❌ 缺少必要字段: {field}")
        
        if agent_type == "智能会话 Agent":
            if "模型" in data:
                self._check_model(data["模型"])
            if "创造性" in data:
                self._check_creativity(data["创造性"])
            if "提示词" in data:
                self._check_prompt_content(data["提示词"])
        
        elif agent_type == "知识检索 Agent":
            if "知识库" in data:
                self._check_knowledge_base(data["知识库"])
    
    def _validate_markdown_format(self, text: str, agent_type: str):
        required = REQUIRED_FIELDS.get(agent_type, [])
        
        for field in required:
            if field not in text:
                self.errors.append(f"❌ 缺少必要字段: {field}")
        
        if "提示词" in text or "【提示词】" in text:
            prompt_match = re.search(r'【提示词】\s*(.+?)(?=\n【|\n\n|$)', text, re.DOTALL)
            if prompt_match:
                self._check_prompt_content(prompt_match.group(1))
        
        if "模型：" in text or "【模型】" in text:
            model_match = re.search(r'【模型】\s*(.+?)(?:\n|【|$)', text)
            if model_match:
                self._check_model(model_match.group(1))
    
    def _check_model(self, model: str):
        valid_models = [
            "Qwen32B", "Qwen72B", "GPT-4", "GPT-3.5", 
            "Claude", "Claude3", "Gemini", "Llama"
        ]
        model_lower = model.lower()
        if not any(m.lower() in model_lower for m in valid_models):
            self.warnings.append(f"⚠️ 未知的模型: {model}")
    
    def _check_creativity(self, creativity: str):
        if not re.match(r'^\d+\s*级|^\d+$', creativity):
            self.warnings.append(f"⚠️ 创造性格式不正确，应为 X 级: {creativity}")
    
    def _check_prompt_content(self, prompt: str):
        if len(prompt) < 10:
            self.errors.append("❌ 提示词内容过短")
        
        if "你是一个" not in prompt and "你是" not in prompt:
            self.warnings.append("⚠️ 提示词缺少角色定义")
        
        if "。" not in prompt and "！" not in prompt and "？" not in prompt:
            self.warnings.append("⚠️ 提示词缺少标点符号")
    
    def _check_knowledge_base(self, kb: str):
        if not kb or kb == "[]":
            self.errors.append("❌ 知识库不能为空")


def validate_file(filepath: str, agent_type: str = "") -> Dict[str, Any]:
    path = Path(filepath)
    if not path.exists():
        return {"valid": False, "errors": [f"文件不存在: {filepath}"], "warnings": []}
    
    content = path.read_text(encoding="utf-8")
    validator = PromptValidator()
    return validator.validate(content, agent_type)


def validate_json(json_str: str, agent_type: str = "") -> Dict[str, Any]:
    validator = PromptValidator()
    return validator.validate(json_str, agent_type)


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_prompt.py <prompt.md|json> [agent_type]")
        print("   agent_type: 智能会话 Agent | 知识检索 Agent")
        sys.exit(1)
    
    filepath = sys.argv[1]
    agent_type = sys.argv[2] if len(sys.argv) > 2 else ""
    
    result = validate_file(filepath, agent_type)
    
    print("\n📋 Agent 提示词验证结果")
    print("=" * 50)
    
    if result["warnings"]:
        print("\n🔔 警告:")
        for w in result["warnings"]:
            print(f"  {w}")
    
    if result["errors"]:
        print("\n❌ 错误:")
        for e in result["errors"]:
            print(f"  {e}")
        print(f"\n❌ 验证失败 ({len(result['errors'])} 个错误)")
        sys.exit(1)
    else:
        print("\n✅ 验证通过!")
        sys.exit(0)


if __name__ == "__main__":
    main()

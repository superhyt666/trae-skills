import json
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path


NODE_INPUT_TYPES = {
    "文本": ["文本", "json", "markdown", "引用", "超链接"],
    "json": ["json", "文本"],
    "markdown": ["markdown", "文本"],
    "引用": ["引用", "文本"],
    "超链接": ["超链接", "文本"],
    "文本/数组": ["文本/数组", "文本"],
    "json/数组": ["json/数组", "json"],
    "文档/数组": ["文档/数组", "文档"],
    "知识/数组": ["知识/数组", "知识"],
}

NODE_OUTPUT_TYPES = {
    "文本": "文本",
    "json": "json",
    "markdown": "markdown",
    "引用": "引用",
    "超链接": "超链接",
    "文档": "文档",
    "知识": "知识",
    "文本/数组": "文本/数组",
    "json/数组": "json/数组",
    "文档/数组": "文档/数组",
    "知识/数组": "知识/数组",
}

CALLING_NODES = ["Agent", "Python代码执行", "LLM", "HTTP技能"]
CONTROL_NODES = ["条件判断", "循环处理", "并行处理"]
AI_NODES = ["图像生成", "语音识别", "语音合成"]
KNOWLEDGE_NODES = ["添加知识", "知识问答", "知识检索"]
TABLE_NODES = ["智能表格检索", "写入智能表格"]
TEXT_NODES = ["关键词识别", "Json解析", "数据类型转换"]


class WorkflowValidator:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        self.errors = []
        self.warnings = []
        
        if isinstance(workflow_data, str):
            try:
                workflow_data = json.loads(workflow_data)
            except json.JSONDecodeError as e:
                return {
                    "valid": False,
                    "errors": [f"❌ JSON 解析失败: {e}"],
                    "warnings": []
                }
        
        self._check_structure(workflow_data)
        self._check_nodes(workflow_data.get("nodes", []))
        self._check_connections(workflow_data.get("nodes", []), workflow_data.get("edges", []))
        
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }
    
    def _check_structure(self, workflow: Dict[str, Any]):
        required_fields = ["nodes", "edges"]
        for field in required_fields:
            if field not in workflow:
                self.errors.append(f"❌ 缺少必要字段: {field}")
        
        if "nodes" in workflow and not isinstance(workflow["nodes"], list):
            self.errors.append("❌ nodes 必须是数组类型")
    
    def _check_nodes(self, nodes: List[Dict]):
        node_ids = set()
        
        for i, node in enumerate(nodes):
            if "id" not in node:
                self.errors.append(f"❌ 节点 {i} 缺少 id 字段")
                continue
            
            node_id = node["id"]
            if node_id in node_ids:
                self.errors.append(f"❌ 节点 ID 重复: {node_id}")
            node_ids.add(node_id)
            
            if "type" not in node:
                self.errors.append(f"❌ 节点 {node_id} 缺少 type 字段")
            
            self._check_node_input(node)
            self._check_node_output(node)
    
    def _check_node_input(self, node: Dict):
        node_type = node.get("type", "")
        
        if node_type in CALLING_NODES:
            if "inputs" not in node:
                self.warnings.append(f"⚠️ 节点 {node['id']} 缺少 inputs 字段")
        
        if node_type == "循环处理":
            if "arrayInput" not in node.get("inputs", {}):
                self.errors.append(f"❌ 节点 {node['id']} 是循环处理节点，必须有 arrayInput 输入")
    
    def _check_node_output(self, node: Dict):
        node_type = node.get("type", "")
        
        if node_type == "条件判断":
            if "branches" not in node:
                self.errors.append(f"❌ 节点 {node['id']} 是条件判断节点，必须有 branches 字段")
    
    def _check_connections(self, nodes: List[Dict], edges: List[Dict]):
        node_ids = {node["id"] for node in nodes if "id" in node}
        
        for edge in edges:
            if "source" not in edge or "target" not in edge:
                self.errors.append(f"❌ 边缺少 source 或 target 字段: {edge}")
                continue
            
            if edge["source"] not in node_ids:
                self.warnings.append(f"⚠️ 边的 source 节点不存在: {edge['source']}")
            if edge["target"] not in node_ids:
                self.warnings.append(f"⚠️ 边的 target 节点不存在: {edge['target']}")


def validate_file(filepath: str) -> Dict[str, Any]:
    path = Path(filepath)
    if not path.exists():
        return {"valid": False, "errors": [f"文件不存在: {filepath}"], "warnings": []}
    
    try:
        content = path.read_text(encoding="utf-8")
        workflow = json.loads(content)
    except json.JSONDecodeError as e:
        return {"valid": False, "errors": [f"❌ JSON 解析失败: {e}"], "warnings": []}
    
    validator = WorkflowValidator()
    return validator.validate(workflow)


def validate_json(json_str: str) -> Dict[str, Any]:
    validator = WorkflowValidator()
    return validator.validate(json_str)


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_workflow.py <workflow.json>")
        print("   或: python validate_workflow.py -j '<json>'")
        sys.exit(1)
    
    if sys.argv[1] == "-j":
        result = validate_json(sys.argv[2] if len(sys.argv) > 2 else "{}")
    else:
        result = validate_file(sys.argv[1])
    
    print("\n📋 工作流验证结果")
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

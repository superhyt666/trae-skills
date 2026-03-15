import json
import sys
from typing import Dict, List, Any, Optional, Set
from pathlib import Path


VARIABLE_TYPES = {
    "base": ["文本", "json", "markdown", "引用", "超链接", "文档", "知识"],
    "array": ["文本/数组", "json/数组", "文档/数组", "知识/数组"],
    "all": ["文本", "json", "markdown", "引用", "超链接", "文档", "知识", 
            "文本/数组", "json/数组", "文档/数组", "知识/数组"]
}

NODE_OUTPUT_TYPES = {
    "输入": "文本",
    "LLM": "文本",
    "Agent": "文本",
    "HTTP技能": "json",
    "Python代码执行": "json",
    "条件判断": "分支",
    "循环处理": "迭代结果",
    "并行处理": "数组",
    "图像生成": "超链接",
    "语音识别": "文本",
    "语音合成": "超链接",
    "添加知识": "知识",
    "知识问答": "文本",
    "知识检索": "知识/数组",
    "智能表格检索": "json/数组",
    "写入智能表格": "json",
    "关键词识别": "json",
    "Json解析": "json",
    "数据类型转换": "任意",
}


COMPATIBLE_INPUTS = {
    "文本": ["文本", "引用"],
    "json": ["json", "文本"],
    "markdown": ["markdown", "文本"],
    "引用": ["引用", "文本"],
    "超链接": ["超链接", "文本"],
    "文档": ["文档", "引用"],
    "知识": ["知识", "引用"],
    "文本/数组": ["文本/数组", "文本", "引用"],
    "json/数组": ["json/数组", "json", "文本"],
    "文档/数组": ["文档/数组", "文档", "引用"],
    "知识/数组": ["知识/数组", "知识", "引用"],
    "分支": ["文本"],
    "迭代结果": ["文本/数组", "json/数组"],
    "数组": ["文本/数组", "json/数组", "文档/数组", "知识/数组"],
    "任意": VARIABLE_TYPES["all"],
}


class NodeTypeChecker:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def check(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
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
        
        nodes = workflow_data.get("nodes", [])
        edges = workflow_data.get("edges", [])
        
        self._check_node_types(nodes)
        self._check_type_compatibility(nodes, edges)
        
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }
    
    def _check_node_types(self, nodes: List[Dict]):
        for node in nodes:
            node_type = node.get("type", "")
            if node_type not in NODE_OUTPUT_TYPES:
                self.warnings.append(f"⚠️ 未知节点类型: {node_type} (节点: {node.get('id', 'unknown')})")
    
    def _check_type_compatibility(self, nodes: List[Dict], edges: List[Dict]):
        node_map = {node["id"]: node for node in nodes if "id" in node}
        
        for edge in edges:
            source_id = edge.get("source")
            target_id = edge.get("target")
            source_var = edge.get("sourceVar", "")
            target_var = edge.get("targetVar", "")
            
            if source_id not in node_map:
                continue
            if target_id not in node_map:
                continue
            
            source_node = node_map[source_id]
            target_node = node_map[target_id]
            
            source_type = source_node.get("type", "")
            target_type = target_node.get("type", "")
            
            output_type = NODE_OUTPUT_TYPES.get(source_type, "任意")
            
            compatible = COMPATIBLE_INPUTS.get(output_type, VARIABLE_TYPES["all"])
            
            target_inputs = target_node.get("inputs", {}).get(target_var, {})
            expected_type = target_inputs.get("type", "")
            
            if expected_type and expected_type not in compatible:
                self.warnings.append(
                    f"⚠️ 类型不匹配: {source_id}.{source_var} ({output_type}) -> "
                    f"{target_id}.{target_var} (期望: {expected_type})"
                )


def check_file(filepath: str) -> Dict[str, Any]:
    path = Path(filepath)
    if not path.exists():
        return {"valid": False, "errors": [f"文件不存在: {filepath}"], "warnings": []}
    
    try:
        content = path.read_text(encoding="utf-8")
        workflow = json.loads(content)
    except json.JSONDecodeError as e:
        return {"valid": False, "errors": [f"❌ JSON 解析失败: {e}"], "warnings": []}
    
    checker = NodeTypeChecker()
    return checker.check(workflow)


def check_json(json_str: str) -> Dict[str, Any]:
    checker = NodeTypeChecker()
    return checker.check(json_str)


def main():
    if len(sys.argv) < 2:
        print("用法: python check_node_types.py <workflow.json>")
        print("   或: python check_node_types.py -j '<json>'")
        sys.exit(1)
    
    if sys.argv[1] == "-j":
        result = check_json(sys.argv[2] if len(sys.argv) > 2 else "{}")
    else:
        result = check_file(sys.argv[1])
    
    print("\n📋 节点类型检查结果")
    print("=" * 50)
    
    if result["warnings"]:
        print("\n🔔 警告:")
        for w in result["warnings"]:
            print(f"  {w}")
    
    if result["errors"]:
        print("\n❌ 错误:")
        for e in result["errors"]:
            print(f"  {e}")
        print(f"\n❌ 检查失败 ({len(result['errors'])} 个错误)")
        sys.exit(1)
    else:
        print("\n✅ 类型检查通过!")
        sys.exit(0)


if __name__ == "__main__":
    main()

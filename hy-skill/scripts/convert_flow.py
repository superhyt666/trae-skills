import base64
import urllib.parse
import json
import re
import sys
from pathlib import Path

COMPONENT_TYPE_MAP = {
    "DOCUMENT_KNOWLEDGE_SEARCH": "文档知识检索",
    "KNOWLEDGE_SEARCH": "知识检索",
    "PYTHON_CODE_EXEC": "Python代码执行",
    "CUSTOM": "自定义组件",
    "LLM": "大语言模型",
    "IF_ELSE": "条件判断",
    "PATH_MERGER": "路径合并",
    "DATA_CONVERTOR": "数据类型转换",
    "KNOWLEDGE_ADD": "添加知识",
    "START": "开始节点",
    "END": "结束节点",
}

ELEMENT_TYPE_MAP = {
    "startEvent": "开始节点",
    "endEvent": "结束节点",
    "serviceAction": "服务节点",
    "exclusiveGateway": "条件判断",
    "parallelGateway": "并行网关",
    "inclusiveGateway": "包容网关",
}

def decode_flow_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    decoded = base64.b64decode(content).decode('utf-8')
    decoded = urllib.parse.unquote(decoded)
    
    parts = decoded.split('}{')
    if len(parts) > 1:
        password_json = parts[0] + '}'
        workflow_json = '{' + parts[1]
    else:
        workflow_json = decoded
    
    workflow_data = json.loads(workflow_json)
    content_str = workflow_data.get('content', '')
    inner_json = json.loads(content_str)
    
    return inner_json

def build_variable_mapping(variables):
    mapping = {}
    for var in variables:
        var_id = var.get('id', '')
        var_name = var.get('name', '')
        if var_id and var_name:
            mapping[var_id] = var_name
    return mapping

def translate_component_type(comp_type):
    return COMPONENT_TYPE_MAP.get(comp_type, comp_type)

def translate_element_type(element_type):
    return ELEMENT_TYPE_MAP.get(element_type, element_type)

def replace_variable_refs_simple(text, var_mapping):
    for var_id, var_name in var_mapping.items():
        text = text.replace("{{" + var_id + "}}", f"{var_name} || {{{{{var_id}}}}}")
    return text

def extract_nodes(process_list, var_mapping):
    nodes = []
    edges = []
    node_id_to_name = {}
    
    for idx, proc in enumerate(process_list):
        node_id = proc.get('id', f'node_{idx}')
        node_name = proc.get('name', f'节点{idx+1}')
        
        element_type = proc.get('element', '')
        node_type_zh = translate_element_type(element_type)
        
        component_type = proc.get('type', '')
        translated_component = translate_component_type(component_type)
        
        input_params = proc.get('inputParameters', {})
        output_params = proc.get('outputParameters', {})
        
        input_params_str = json.dumps(input_params, ensure_ascii=False, indent=2)
        input_params_str = replace_variable_refs_simple(input_params_str, var_mapping)
        
        output_params_str = json.dumps(output_params, ensure_ascii=False, indent=2)
        
        next_nodes = []
        next_conditions = {}
        
        if 'target' in proc and proc['target']:
            next_nodes.append(proc['target'])
        
        if 'conditions' in proc:
            for cond in proc['conditions']:
                if 'target' in cond and cond['target']:
                    next_nodes.append(cond['target'])
                    expr = cond.get('expression', '')
                    if expr:
                        next_conditions[cond['target']] = expr
        
        if 'conditions' in input_params:
            for cond in input_params['conditions']:
                if 'target' in cond and cond['target']:
                    next_nodes.append(cond['target'])
        
        nodes.append({
            'id': node_id,
            'name': node_name,
            'element': element_type,
            'type_zh': node_type_zh,
            'component_type': component_type,
            'component_type_zh': translated_component,
            'input_params': input_params_str,
            'output_params': output_params_str,
            'next_nodes': next_nodes,
            'next_conditions': next_conditions
        })
        
        node_id_to_name[node_id] = node_name
    
    for node in nodes:
        for next_id in node['next_nodes']:
            if next_id in node_id_to_name:
                edges.append((node['id'], next_id))
    
    return nodes, edges, node_id_to_name

def generate_mermaid_graph(nodes, edges, node_id_to_name):
    lines = ["```mermaid", "graph TD"]
    
    for node in nodes:
        node_id = node['id']
        name = node['name']
        
        name = name.replace('[', '【').replace(']', '】')
        
        element = node['element']
        if element == 'startEvent':
            lines.append(f'    {node_id}["{name}"]')
        elif element == 'endEvent':
            lines.append(f'    {node_id}(("{name}"))')
        elif element == 'exclusiveGateway':
            lines.append(f'    {node_id}{{{name}}}')
        elif element == 'inclusiveGateway':
            lines.append(f'    {node_id}{{{name}}}')
        elif element == 'parallelGateway':
            lines.append(f'    {node_id}{{{name}}}')
        else:
            lines.append(f'    {node_id}["{name}"]')
    
    for src_node in nodes:
        src = src_node['id']
        next_conditions = src_node.get('next_conditions', {})
        for dst in src_node['next_nodes']:
            if dst in next_conditions and next_conditions[dst]:
                lines.append(f'    {src} -->|{next_conditions[dst]}| {dst}')
            else:
                lines.append(f'    {src} --> {dst}')
    
    lines.append("```")
    return '\n'.join(lines)

def convert_flow_to_markdown(flow_file_path, output_path=None):
    flow_data = decode_flow_file(flow_file_path)
    
    variables = flow_data.get('variables', [])
    var_mapping = build_variable_mapping(variables)
    
    process_list = flow_data.get('process', [])
    nodes, edges, node_id_to_name = extract_nodes(process_list, var_mapping)
    
    tenant_id = flow_data.get('tenantSn', '')
    process_id = flow_data.get('processId', '')
    workflow_name = flow_data.get('name', '')
    status = flow_data.get('status', 1)
    released = flow_data.get('released', False)
    enabled = flow_data.get('enable', False)
    deleted = flow_data.get('deleted', False)
    create_time = flow_data.get('createTime', '')
    update_time = flow_data.get('updateTime', '')
    created_by = flow_data.get('createdByName', '')
    
    status_name = {1: "设计中", 2: "已发布"}.get(status, "未知")
    released_str = "是" if released else "否"
    enabled_str = "是" if enabled else "否"
    
    if status == 1 and released:
        status_name = "已发布"
    
    lines = []
    lines.append(f"# {workflow_name}")
    lines.append("")
    lines.append("## 基本信息")
    lines.append("")
    lines.append(f"- **租户ID**: {tenant_id}")
    lines.append(f"- **流程ID**: {process_id}")
    lines.append(f"- **状态**: {status_name}")
    lines.append(f"- **是否发布**: {released_str}")
    lines.append(f"- **是否启用**: {enabled_str}")
    lines.append(f"- **创建时间**: {create_time}")
    lines.append(f"- **更新时间**: {update_time}")
    lines.append(f"- **创建者**: {created_by}")
    lines.append("")
    lines.append("## 输入输出变量")
    lines.append("")
    lines.append("| 变量名称 | 类型 | 必填 | 说明 |")
    lines.append("| --------- | ---- | ---- | ---- |")
    
    for var in variables:
        var_name = var.get('name', '')
        var_type = var.get('type', 'TEXT')
        required = "是" if var.get('required', False) else "否"
        lines.append(f"| {var_name} | {var_type} | {required} | |")
    
    lines.append("")
    lines.append("## 流程节点")
    lines.append("")
    
    for idx, node in enumerate(nodes, 1):
        lines.append(f"### 节点 {idx}: {node['name']}")
        lines.append("")
        lines.append(f"- **节点ID**: {node['id']}")
        lines.append(f"- **节点类型**: {node['type_zh']}")
        
        if node['component_type']:
            lines.append(f"- **组件类型**: {node['component_type_zh']}")
        
        if node['next_nodes']:
            lines.append(f"- **下一节点**: {', '.join(node['next_nodes'])}")
        
        lines.append("")
        
        if node['input_params'] and node['input_params'] != '{}':
            lines.append("**输入参数**:")
            lines.append("")
            lines.append("```json")
            lines.append(node['input_params'])
            lines.append("```")
            lines.append("")
        
        if node['output_params'] and node['output_params'] != '{}':
            lines.append("**输出参数**:")
            lines.append("")
            lines.append("```json")
            lines.append(node['output_params'])
            lines.append("```")
            lines.append("")
    
    mermaid_graph = generate_mermaid_graph(nodes, edges, node_id_to_name)
    
    lines.append("## 节点连接关系")
    lines.append("")
    lines.append(mermaid_graph)
    
    markdown_content = '\n'.join(lines)
    
    if output_path is None:
        output_path = Path("hy-skill") / "hy-custom-workflow" / (Path(flow_file_path).stem + '.md')
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"转换完成！输出文件: {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python convert_flow.py <flow文件路径>")
        sys.exit(1)
    
    flow_file = sys.argv[1]
    convert_flow_to_markdown(flow_file)

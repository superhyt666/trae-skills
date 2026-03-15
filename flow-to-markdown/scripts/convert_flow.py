# -*- coding: utf-8 -*-
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
    "TEXT_MERGE": "文本合并",
    "JSON_PARSER": "JSON解析",
    "JSON_SPLICING": "JSON拼接",
    "SUB_PROCESS": "子工作流",
    "PARALLEL": "并行处理",
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
    "parallelProcess": "并行处理",
}


def decode_flow_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    decoded = base64.b64decode(content).decode('utf-8')
    decoded = urllib.parse.unquote(decoded)

    start_idx = decoded.find('{"version')
    if start_idx < 0:
        raise ValueError("Cannot find workflow JSON")

    count = 0
    end_idx = start_idx
    in_string = False
    escape_next = False

    for i in range(start_idx, len(decoded)):
        ch = decoded[i]
        if escape_next:
            escape_next = False
            continue
        if ch == '\\':
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
        if not in_string:
            if ch == '{':
                count += 1
            elif ch == '}':
                count -= 1
                if count == 0:
                    end_idx = i + 1
                    break

    wj_str = decoded[start_idx:end_idx]
    wj = json.loads(wj_str)
    inner_json = json.loads(wj['content'])

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


def extract_variable_refs(text, var_mapping):
    refs = []
    if isinstance(text, str):
        matches = re.findall(r'\{\{(\w+)\}\}', text)
        for match in matches:
            var_name = var_mapping.get(match, match)
            refs.append(f"{var_name}({match})")
    return refs


def format_input_param_value(value, var_mapping):
    if isinstance(value, str):
        refs = extract_variable_refs(value, var_mapping)
        if refs:
            return ", ".join(refs)
        if len(value) > 50:
            return value[:50] + "..."
        return value
    elif isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)[:100]
    elif isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)[:100]
    else:
        return str(value)


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
        output_params_by_node = proc.get('outputParametersByNode', {})

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

        nodes.append({
            'id': node_id,
            'name': node_name,
            'element': element_type,
            'type_zh': node_type_zh,
            'component_type': component_type,
            'component_type_zh': translated_component,
            'input_params': input_params,
            'output_params': output_params,
            'output_params_by_node': output_params_by_node,
            'next_nodes': next_nodes,
            'next_conditions': next_conditions,
            'conditions': proc.get('conditions', [])
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
        elif element == 'parallelProcess':
            lines.append(f'    {node_id}{{{name}}}')
        else:
            lines.append(f'    {node_id}["{name}"]')

    for src_node in nodes:
        src = src_node['id']
        next_conditions = src_node.get('next_conditions', {})
        for dst in src_node['next_nodes']:
            if dst in next_conditions and next_conditions[dst]:
                lines.append(f'    {src} -->|{next_conditions[dst][:30]}| {dst}')
            else:
                lines.append(f'    {src} --> {dst}')

    lines.append("```")
    return '\n'.join(lines)


def format_node_input_table(input_params, var_mapping):
    lines = []
    for param_name, param_value in input_params.items():
        value_str = format_input_param_value(param_value, var_mapping)
        lines.append(f"| {param_name} | {value_str} |")
    return '\n'.join(lines) if lines else "| 无 | 无 |"


def format_node_output_table(output_params, output_params_by_node, var_mapping):
    lines = []

    if output_params_by_node:
        for sub_node_id, outputs in output_params_by_node.items():
            for param_name, var_id in outputs.items():
                var_name = var_mapping.get(var_id, f"未知({var_id})")
                lines.append(f"| {param_name} | {var_id} | {var_name} | {var_name} |")
    elif output_params:
        for param_name in output_params.keys():
            lines.append(f"| {param_name} | - | 输出到变量 |")
    else:
        return "| 无 | 无 | 无 |"

    return '\n'.join(lines)


def format_conditions_table(conditions, var_mapping):
    lines = []
    for cond in conditions:
        target = cond.get('target', '')
        expr = cond.get('expression', '')
        lines.append(f"| {target} | {expr[:50]}... |")
    return '\n'.join(lines) if lines else ""


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
    lines.append(f"| 属性 | 值 |")
    lines.append(f"|------|-----|")
    lines.append(f"| **流程名称** | {workflow_name} |")
    lines.append(f"| **流程ID** | {process_id} |")
    lines.append(f"| **状态** | {status_name} |")
    lines.append(f"| **是否发布** | {released_str} |")
    lines.append(f"| **是否启用** | {enabled_str} |")
    lines.append(f"| **创建时间** | {create_time} |")
    lines.append(f"| **更新时间** | {update_time} |")
    lines.append(f"| **创建者** | {created_by} |")
    lines.append(f"| **租户ID** | {tenant_id} |")
    lines.append("")

    lines.append("## 输入变量")
    lines.append("")
    lines.append("| 变量名称 | 变量ID | 类型 | 必填 | 说明 |")
    lines.append("|----------|--------|------|------|------|")

    for var in variables:
        var_name = var.get('name', '')
        var_id = var.get('id', '')
        var_type = var.get('type', 'TEXT')
        required = "✅" if var.get('required', False) else "❌"
        lines.append(f"| {var_name} | {var_id} | {var_type} | {required} | |")

    lines.append("")

    lines.append("## 执行路径")
    lines.append("")
    lines.append("```")
    lines.append("输入 → 条件判断 → [分支] → 数据处理 → LLM处理 → 子工作流 → 输出")
    lines.append("```")
    lines.append("")

    lines.append("## 详细节点配置（含输入输出变量）")
    lines.append("")
    lines.append("---")
    lines.append("")

    for idx, node in enumerate(nodes, 1):
        lines.append(f"### {idx}. {node['name']} - ID: {node['id']}")
        lines.append("")
        lines.append(f"- **节点类型**: {node['type_zh']} ({node['element']})")
        if node['component_type']:
            lines.append(f"- **组件类型**: {node['component_type_zh']}")

        if node['next_nodes']:
            next_names = [node_id_to_name.get(nid, nid) for nid in node['next_nodes']]
            lines.append(f"- **下一节点**: {', '.join(next_names)}")

        lines.append("")

        if node['input_params']:
            lines.append("**输入参数**:")
            lines.append("")
            lines.append("| 参数名 | 值 |")
            lines.append("|--------|-----|")
            lines.append(format_node_input_table(node['input_params'], var_mapping))
            lines.append("")

        if node['conditions']:
            lines.append("**条件分支**:")
            lines.append("")
            lines.append("| 目标节点 | 条件 |")
            lines.append("|----------|------|")
            lines.append(format_conditions_table(node['conditions'], var_mapping))
            lines.append("")

        output_by_node = node.get('output_params_by_node', {})
        output_params = node.get('output_params', {})

        if output_by_node or output_params:
            if node['component_type'] == 'SUB_PROCESS':
                lines.append("**输出参数**:")
                lines.append("")
                lines.append("| 参数名 | 变量ID | 说明 | 输出到变量 |")
                lines.append("|--------|--------|------|-----------|")
                lines.append(format_node_output_table(output_params, output_by_node, var_mapping))
            else:
                lines.append("**输出参数**:")
                lines.append("")
                lines.append("| 参数名 | 说明 |")
                lines.append("|--------|------|")
                for param_name in output_params.keys():
                    lines.append(f"| {param_name} | 输出到变量 |")
                if not output_params and output_by_node:
                    for sub_node_id, outputs in output_by_node.items():
                        for param_name, var_id in outputs.items():
                            var_name = var_mapping.get(var_id, var_id)
                            lines.append(f"| {param_name} | {var_name} |")
            lines.append("")

        lines.append("---")
        lines.append("")

    mermaid_graph = generate_mermaid_graph(nodes, edges, node_id_to_name)

    lines.append("## Mermaid 流程图")
    lines.append("")
    lines.append(mermaid_graph)
    lines.append("")

    lines.append("## 子工作流依赖")
    lines.append("")
    lines.append("| 子工作流名称 | 流程ID | 版本ID | 状态 |")
    lines.append("|-------------|--------|--------|------|")

    subprocess_list = []
    for node in nodes:
        if node['component_type'] == 'SUB_PROCESS':
            input_params = node.get('input_params', {})
            sub_id = input_params.get('subProcessId', '')
            version_id = input_params.get('versionId', '')
            version_str = str(version_id) if version_id else "随版本启用"
            status_str = "✅ 正常" if version_id else "✅ 正常"
            if sub_id and sub_id not in [s[0] for s in subprocess_list]:
                subprocess_list.append((node['name'], sub_id, version_str, status_str))

    for name, sub_id, version, status in subprocess_list:
        lines.append(f"| {name} | {sub_id} | {version} | {status} |")

    lines.append("")

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

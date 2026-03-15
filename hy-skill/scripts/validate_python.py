import ast
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


class PythonCodeValidator:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
        self.forbidden_patterns = [
            (r'print\s*\(', '禁止使用 print() 输出结果'),
            (r'json\.dumps\s*\(', '禁止使用 json.dumps() 序列化返回值'),
            (r'console\.log', '禁止使用 console.log'),
            (r'logger\.info\(', '禁止使用 logger.info 输出结果'),
        ]
        
        self.required_imports = []
        
    def validate(self, code: str, filename: str = "input.py") -> Dict[str, Any]:
        self.errors = []
        self.warnings = []
        
        self._check_forbidden_patterns(code)
        self._check_return_statement(code)
        self._check_imports(code)
        self._check_function_structure(code)
        
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "filename": filename
        }
    
    def _check_forbidden_patterns(self, code: str):
        for pattern, message in self.forbidden_patterns:
            if re.search(pattern, code):
                self.errors.append(f"❌ {message}")
    
    def _check_return_statement(self, code: str):
        if "return" not in code and "def " in code:
            self.warnings.append("⚠️ 函数没有 return 语句")
    
    def _check_imports(self, code: str):
        try:
            tree = ast.parse(code)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(node.module)
            
            for imp in imports:
                if imp and imp.startswith("_"):
                    self.warnings.append(f"⚠️ 导入私有模块: {imp}")
        except SyntaxError as e:
            self.errors.append(f"❌ 语法错误: {e}")
    
    def _check_function_structure(self, code: str):
        if "if __name__" in code:
            self.warnings.append("⚠️ 包含测试代码 (if __name__ == '__main__')，交付前请移除")
        
        if "TODO" in code or "FIXME" in code:
            self.warnings.append("⚠️ 代码中包含未完成的 TODO/FIXME")


def validate_file(filepath: str) -> Dict[str, Any]:
    path = Path(filepath)
    if not path.exists():
        return {"valid": False, "errors": [f"文件不存在: {filepath}"], "warnings": []}
    
    code = path.read_text(encoding="utf-8")
    validator = PythonCodeValidator()
    return validator.validate(code, path.name)


def validate_code(code: str) -> Dict[str, Any]:
    validator = PythonCodeValidator()
    return validator.validate(code, "input.py")


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_python.py <file.py>")
        print("   或: python validate_python.py -c '<code>'")
        sys.exit(1)
    
    if sys.argv[1] == "-c":
        code = sys.argv[2] if len(sys.argv) > 2 else ""
        result = validate_code(code)
    else:
        result = validate_file(sys.argv[1])
    
    print(f"\n📋 验证结果: {result['filename']}")
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

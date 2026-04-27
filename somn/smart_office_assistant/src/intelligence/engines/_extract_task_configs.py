"""
V2: 更智能的配置提取器 - 追踪变量赋值链
解决:
1. result.output_data = variable_name (非字面量)
2. findings = variable["key_findings"] (间接引用)
3. quality_score从变量追踪
"""
import ast
import json
from pathlib import Path

SOURCE_FILE = Path(__file__).parent / 'research_phase_manager.py'
OUTPUT_FILE = Path(__file__).parent / 'data' / 'task_executor_configs.json'

def extract_value(node, var_map=None):
    """递归提取AST节点的值，支持变量引用解析"""
    if var_map is None:
        var_map = {}
    
    # 字面量
    if isinstance(node, ast.Constant):
        return node.value
    
    # 变量引用 -> 查var_map
    if isinstance(node, ast.Name) and node.id in var_map:
        return var_map[node.id]
    
    # 字典
    if isinstance(node, ast.Dict):
        d = {}
        for k, v in zip(node.keys, node.values):
            key = extract_value(k, var_map)
            val = extract_value(v, var_map)
            if key is not None and not (isinstance(key, str) and key == '<unextractable>'):
                d[key] = val
        return d
    
    # 列表
    if isinstance(node, ast.List):
        return [extract_value(e, var_map) for e in node.elts]
    
    # 元组
    if isinstance(node, ast.Tuple):
        return tuple(extract_value(e, var_map) for e in node.elts)
    
    # 下标访问: variable["key"] 或 variable[key]
    if isinstance(node, ast.Subscript):
        obj_val = extract_value(node.value, var_map)
        slice_val = extract_value(node.slice, var_map)
        if isinstance(obj_val, dict) and slice_val is not None:
            return obj_val.get(slice_val, f"<subscript:{slice_val}>")
        return f"<subscript>"
    
    # 属性访问: obj.attr (如 datetime.now())
    if isinstance(node, ast.Attribute):
        return f"<attr:{node.attr}>"
    
    # 函数调用: 返回标记
    if isinstance(node, ast.Call):
        return f"<call>"
    
    # 二元运算
    if isinstance(node, ast.BinOp):
        try:
            left = extract_value(node.left, var_map)
            right = extract_value(node.right, var_map)
            if isinstance(node.op, ast.Add): return left + right
            if isinstance(node.op, ast.Mult): return left * right
            if isinstance(node.op, ast.Sub): return left - right
            if isinstance(node.op, ast.Div): return left / right
        except Exception:
            pass  # if isinstance(node.op, ast.Div): return left / right失败时静默忽略
        return "<binop>"
    
    # 比较运算
    if isinstance(node, ast.Compare):
        return "<compare>"
    
    # 格式化字符串
    if isinstance(node, ast.JoinedStr):
        parts = [extract_value(v, var_map) for v in node.values]
        return ''.join(str(p) if not p.startswith('<') else '' for p in parts)
    
    return f"<{type(node).__name__}>"


class ExecutorConfigExtractor(ast.NodeVisitor):
    """提取执行器配置"""
    
    def __init__(self):
        self.configs = {}
        self.current_class = None
        self.current_config = None
    
    def visit_ClassDef(self, node):
        class_name = node.name
        
        # 只处理执行器类
        if not (class_name.startswith('Phase') and 'T' in class_name or class_name == 'Phase4SystemBuilder'):
            return
        if class_name == 'BaseTaskExecutor':
            return
        
        self.current_class = class_name
        self.current_config = {
            'class_name': class_name,
            'task_id': '',
            'task_name': '',
            'phase': 1,
            'required_intersections': [],
            'output_data': {},
            'quality_score': 0.0,
            'key_findings': [],
            'extra_method_data': {},  # 额外方法的返回数据
        }
        
        # 访问类体
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self._visit_function(item)
        
        if self.current_config['task_id']:
            self.configs[self.current_config['task_id']] = self.current_config
        
        self.current_class = None
        self.current_config = None
    
    def _visit_function(self, func_node):
        """处理函数定义"""
        func_name = func_node.name
        
        if func_name == '__init__':
            self._process_init(func_node)
        elif func_name == 'execute':
            self._process_execute(func_node)
        elif func_name.startswith('_'):
            self._process_helper_method(func_node)
    
    def _process_init(self, node):
        """处理__init__方法"""
        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                tgt = self._get_target(stmt)
                val = extract_value(stmt.value)
                
                if tgt == 'task_id' and isinstance(val, str):
                    self.current_config['task_id'] = val
                elif tgt == 'task_name' and isinstance(val, str):
                    self.current_config['task_name'] = val
                elif tgt == 'phase' and isinstance(val, int):
                    self.current_config['phase'] = val
                elif tgt == 'required_intersections' and isinstance(val, list):
                    self.current_config['required_intersections'] = val
    
    def _process_execute(self, node):
        """处理execute方法 - 核心数据提取"""
        var_map = {}  # 局部变量映射表
        output_var_name = None  # 赋给output_data的变量名
        
        for stmt in node.body:
            # 跳过非赋值和非表达式语句
            if isinstance(stmt, ast.Assign):
                tgt = self._get_target(stmt)
                val = extract_value(stmt.value, var_map)
                
                # 记录局部变量到映射表（用于后续变量引用解析）
                if tgt and isinstance(tgt, str) and not tgt.startswith('.'):
                    if isinstance(val, (dict, list, str, int, float)):
                        var_map[tgt] = val
                
                # 检查是否是关键赋值
                if tgt == 'output_data':
                    # result.output_data = xxx
                    if isinstance(val, dict):
                        self.current_config['output_data'] = val
                    elif isinstance(val, str) and val in var_map:
                        ref_val = var_map.get(val, {})
                        if isinstance(ref_val, dict):
                            self.current_config['output_data'] = ref_val
                
                elif tgt == 'quality_score':
                    if isinstance(val, (int, float)):
                        self.current_config['quality_score'] = float(val)
                
                elif tgt == 'findings':
                    if isinstance(val, list):
                        self.current_config['key_findings'] = val
                    elif isinstance(val, str) and '<subscript:' in str(val):
                        # findings = variable["key_findings"]
                        # 尝试直接从var_map中的对应字典找
                        pass
            
            elif isinstance(stmt, ast.Try):
                # 处理try块内的所有语句
                self._process_stmts_in_try(stmt.body, var_map)
            
            elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                # 独立函数调用语句，忽略
                pass
    
    def _process_stmts_in_try(self, stmts, var_map):
        """处理try块内的语句列表"""
        for stmt in stmts:
            if isinstance(stmt, ast.Assign):
                tgt = self._get_target(stmt)
                val = extract_value(stmt.value, var_map)
                
                # 记录局部变量
                if tgt and isinstance(tgt, str) and not tgt.startswith('.'):
                    if isinstance(val, (dict, list, str, int, float, bool)) and not str(val).startswith('<'):
                        var_map[tgt] = val
                
                # 关键赋值检测
                if tgt == 'output_data':
                    if isinstance(val, dict):
                        self.current_config['output_data'] = val
                    elif isinstance(val, str) and val in var_map:
                        ref = var_map.get(val)
                        if isinstance(ref, dict):
                            self.current_config['output_data'] = ref
                
                elif tgt == 'quality_score':
                    if isinstance(val, (int, float)):
                        self.current_config['quality_score'] = float(val)
                
                elif tgt == 'findings':
                    if isinstance(val, list):
                        self.current_config['key_findings'] = val
            
            # 处理内嵌的if/for等块
            elif hasattr(stmt, 'body'):
                self._process_stmts_in_try(getattr(stmt, 'body', []), var_map)
                for handler in getattr(stmt, 'orelse', []):
                    if isinstance(handler, list):
                        self._process_stmts_in_try(handler, var_map)
    
    def _process_helper_method(self, node):
        """处理辅助方法（如_get_neural_mechanism等）"""
        method_data = {}
        
        # 查找return语句中的字典或.get()调用
        for stmt in reversed(node.body):
            if isinstance(stmt, ast.Return) and stmt.value:
                val = extract_value(stmt.value, {})
                if isinstance(val, dict) and val:
                    method_data = val
                    break
                # 处理 .get(x, default) 模式
                if isinstance(stmt.value, ast.Call):
                    func = stmt.value.func
                    if isinstance(func, ast.Attribute) and func.attr == 'get':
                        # 这是一个 .get() 调用，说明方法内部有条件逻辑
                        # 尝试查找前面的变量赋值
                        pass
        
        if method_data:
            self.current_config['extra_method_data'][node.name] = method_data
    
    def _get_target(self, assign_node):
        """获取赋值目标名称（支持简单属性访问如result.output_data）"""
        target = assign_node.targets[0]
        
        # 简单变量名
        if isinstance(target, ast.Name):
            return target.id
        
        # 属性访问: result.output_data
        if isinstance(target, ast.Attribute):
            return target.attr
        
        return None


def main():
    source_text = SOURCE_FILE.read_text(encoding='utf-8')
    tree = ast.parse(source_text)
    
    extractor = ExecutorConfigExtractor()
    extractor.visit(tree)
    
    # 后处理：对每个config，尝试从output_data中提取findings
    for tid, cfg in extractor.configs.items():
        output = cfg.get('output_data', {})
        # 如果output_data中有key_findings但cfg中没有
        if not cfg.get('key_findings') and 'key_findings' in output:
            kf = output['key_findings']
            if isinstance(kf, list):
                cfg['key_findings'] = kf
        # 清理output_data中的key_findings（避免冗余存储，它已经在顶层了）
        if 'key_findings' in output and cfg.get('key_findings'):
            # 保留在output_data中也OK，保持原始结构
            pass
    
    final_output = {
        "version": "v1.0",
        "source": "research_phase_manager.py v1.0.0",
        "generated": "2026-04-23",
        "total_tasks": len(extractor.configs),
        "tasks": extractor.configs
    }
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"Extracted {len(extractor.configs)} task configurations")
    print(f"Output: {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size / 1024:.1f} KB)")
    
    for tid, cfg in sorted(extractor.configs.items()):
        data_keys = list(cfg.get('output_data', {}).keys())[:5]
        findings_count = len(cfg.get('key_findings', []))
        extra_methods = list(cfg.get('extra_method_data', {}).keys())
        print(f"  {tid}: {cfg['task_name']} | phase={cfg['phase']} | "
              f"findings={findings_count} | data_keys={[data_keys]} | extra={extra_methods}")


if __name__ == '__main__':
    main()

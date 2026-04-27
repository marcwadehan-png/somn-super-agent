import sys
from pathlib import Path

# 动态添加项目路径
_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_project_root))
sys.path.insert(0, str(_project_root / "smart_office_assistant"))
sys.path.insert(0, str(_project_root / "smart_office_assistant" / "src"))

import json
import re
from pathlib import Path
from src.core.paths import DATA_DIR
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Read the file
_engine_file = Path(__file__).resolve().parent / "smart_office_assistant" / "src" / "intelligence" / "reasoning" / "deep_reasoning_engine.py"
with open(_engine_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Check what type SOLUTION_CONSTRAINT_DIMENSIONS is defined as
import ast
tree = ast.parse(content)

class ClassVisitor(ast.NodeVisitor):
    def visit_ClassDef(self, node):
        if node.name == 'DeepReasoningEngine':
            for item in ast.iter_child_nodes(node):
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and 'SOLUTION_CONSTRAINT' in target.id:
                            print(f"Found: {target.id} = {type(item.value).__name__}")
                            if isinstance(item.value, ast.Dict):
                                print("  It's a dict with keys:", [k.value if isinstance(k, ast.Constant) else str(k) for k in item.value.keys][:3])
        self.generic_visit(node)

visitor = ClassVisitor()
visitor.visit(tree)

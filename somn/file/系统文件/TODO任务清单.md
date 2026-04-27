# TODO/FIXME 任务清单

生成时间: handle_todo_comments.py

## docs\source\conf.py

- **L23**: `'sphinx.ext.todo',`
- **L93**: `# Todo extension`

## scripts\code_optimization_analyzer.py

- **L61**: `# 检查 TODO 注释`
- **L62**: `todo_count = content.count('TODO') + content.count('FIXME')`
- **L96**: `f.write(f"- **TODO/FIXME 文件**: {len(results['todo_files'])} 个\n\n")`
- **L124**: `f.write("## 三、TODO/FIXME 注释分析\n\n")`
- **L126**: `f.write(f"共 {len(results['todo_files'])} 个文件包含 TODO/FIXME 注释，建议逐步处理这些待办事项。\n\n")`
- **L134**: `f.write("无 TODO/FIXME 注释。\n")`
- **L139**: `f.write("2. **处理 TODO/FIXME**: 逐步处理代码中的待办事项，提高代码质量\n")`
- **L147**: `f.write("2. 处理 TODO/FIXME 注释，提高代码质量\n")`
- **L179**: `print(f"TODO/FIXME: {len(results['todo_files'])} 个")`

## scripts\handle_todo_comments.py

- **L3**: `处理项目中的 TODO/FIXME 注释`
- **L23**: `"""查找包含 TODO/FIXME 的 Python 文件"""`
- **L38**: `if re.search(r"\b(TODO|FIXME|HACK|XXX)\b", line, re.IGNORECASE):`
- **L48**: `print("TODO/FIXME 注释处理工具")`
- **L52**: `print(f"\n找到 {len(results)} 个文件包含 TODO/FIXME：\n")`
- **L68**: `f.write("# TODO/FIXME 任务清单\n\n")`
- **L78**: `print(f"\n建议：逐项审查这些 TODO/FIXME，决定是删除、实现还是保留。")`

## scripts\project_continue_optimization.py

- **L144**: `# 检查 TODO 注释`
- **L145**: `if 'TODO' in content or 'FIXME' in content:`
- **L148**: `'count': content.count('TODO') + content.count('FIXME'),`
- **L161**: `print(f"发现 TODO/FIXME 注释: {len(opportunities['todo_comments'])} 个")`
- **L183**: `f.write(f"- **TODO/FIXME 注释**: {len(opportunities['todo_comments'])} 个\n\n")`
- **L234**: `f.write("### 3. TODO/FIXME 注释\n\n")`
- **L235**: `f.write(f"共 {len(opportunities['todo_comments'])} 个文件包含 TODO/FIXME 注释\n\n")`
- **L247**: `f.write("3. **处理 TODO/FIXME**: 逐步处理代码中的待办事项\n")`
- **L285**: `print(f"TODO/FIXME: {len(opportunities['todo_comments'])} 个")`

## smart_office_assistant\main_chain_verification.py

- **L58**: `# 处理 src.core.xxx 或 src.intelligence.xxx`

## smart_office_assistant\scripts\fix_code_violations.py

- **L71**: `将 xxx = SomeEngine() 改为惰性加载函数`

## smart_office_assistant\scripts\fix\thorough_fix.py

- **L103**: `# 需要把 "xxx" 改为 "xxx"（保持不变）`

## smart_office_assistant\scripts\tools\rebuild_persona.py

- **L11**: `# 问题是：所有的 "xxx" 变成了 xxx"`
- **L12**: `# 需要把 xxx" 改为 "xxx"`
- **L16**: `# 如果行中有 xxx" 这样的模式，且前面是 = 或 : 或 , 或 ( 或 [ 或 {`
- **L20**: `# 修复模式1: self.xxx = value" -> self.xxx = "value"`
- **L21**: `# 匹配 = xxx" 或 : xxx" 等`
- **L24**: `# 修复模式2: "xxx"y y" -> "xxx'yyy" (嵌套中文引号)`
- **L49**: `# 行开头有 xxx" 模式`
- **L56**: `# 修复 = xxx" 模式`

## smart_office_assistant\src\core\timeout_guard.py

- **L11**: `guard = create_timeout_guard(request_id="xxx")`

## smart_office_assistant\src\intelligence\claws\_claw_architect.py

- **L1617**: `TODO: 未来接入向量检索（NeuralMemorySystem语义搜索）[延期: 等待NeuralMemorySystem v1.0]`

## smart_office_assistant\src\intelligence\claws\_extract_court_data.py

- **L28**: `# 格式: id="XXX", name="岗位名", department="部门"`

## smart_office_assistant\src\intelligence\claws\_onboarding_claws_v2.py

- **L115**: `# 格式: id="XXX", name="岗位名", department="部门", ...`

## smart_office_assistant\src\intelligence\dispatcher\wisdom_dispatch\_dispatch_mapping.py

- **L386**: `# 统一从 src.intelligence 加载: reg[0] 格式为 "engines.xxx" 或 "reasoning.xxx"`

## smart_office_assistant\src\intelligence\engines\sticker_saver.py

- **L28**: `xxx.png / xxx.jpg ...`

## smart_office_assistant\src\intelligence\engines\_extract_task_configs.py

- **L173**: `# result.output_data = xxx`

## smart_office_assistant\src\intelligence\engines\cloning\_sage_proxy_factory.py

- **L127**: `# 格式1: **法则一：xxx——yyy**`
- **L128**: `# 格式2: **法则一：xxx**  (无破折号)`
- **L129**: `# 格式3: 1. xxx (编号列表)`

## smart_office_assistant\src\learning\engine\local_data_learner.py

- **L471**: `key_lines = re.findall(r'.*(TODO|FIXME|NOTE|HACK|XXX).*', content, re.IGNORECASE)`
- **L582**: `insights.append(f"包含 {len(knowledge['key_lines'])} 个标记行(TODO/FIXME等)")`

## smart_office_assistant\src\ppt\ppt_memory_integration.py

- **L337**: `# TODO: 实现模式发现逻辑 [延期: 需要先建立模式库]`

## smart_office_assistant\src\tool_layer\dual_model_service.py

- **L681**: `messages=[{"role": "user", "content": "描述这张图片", "image_urls": ["xxx.jpg"]}]`


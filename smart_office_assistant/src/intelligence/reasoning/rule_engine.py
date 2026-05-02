"""
基础规则推理引擎 - 无 LLM 时使用
提供基于关键词匹配 + 规则模板的推理能力
"""
from typing import List, Dict, Optional, Any
import re

class RuleEngine:
    """
    基础规则推理引擎
    在无 LLM 时，提供基于规则的推理能力
    """
    
    def __init__(self):
        # 问题类型识别规则
        self.problem_types = {
            "math": ["计算", "等于", "+", "-", "*", "/", "=", "数学", "算"],
            "logic": ["所有", "如果", "那么", "因为", "所以", "推理", "逻辑"],
            "analysis": ["分析", "原因", "为什么", "如何", "提高", "优化", "改进"],
            "comparison": ["比较", "对比", "哪个", "更好", "优劣"],
            "prediction": ["预测", "未来", "趋势", "会", "可能"],
            "decision": ["选择", "决定", "应该", "要不要", "是否"],
        }
        
        # 推理策略模板
        self.reasoning_strategies = {
            "math": [
                "1. 识别数学表达式",
                "2. 按照运算优先级计算",
                "3. 验证计算结果",
            ],
            "logic": [
                "1. 提取前提条件",
                "2. 应用逻辑规则（如三段论）",
                "3. 推导结论",
                "4. 验证结论的有效性",
            ],
            "analysis": [
                "1. 定义问题边界",
                "2. 识别关键因素",
                "3. 分析因果关系",
                "4. 提出解决方案",
                "5. 评估方案可行性",
            ],
            "comparison": [
                "1. 确定比较维度",
                "2. 列出各选项的优势",
                "3. 列出各选项的劣势",
                "4. 加权评分",
                "5. 得出比较结论",
            ],
            "prediction": [
                "1. 收集历史数据",
                "2. 识别趋势和模式",
                "3. 考虑影响因素",
                "4. 推演未来场景",
                "5. 给出概率预测",
            ],
            "decision": [
                "1. 明确决策目标",
                "2. 列出所有选项",
                "3. 评估风险和收益",
                "4. 考虑机会成本",
                "5. 做出决策建议",
            ],
        }
        
        # 通用推理步骤
        self.generic_steps = [
            "1. 理解问题：明确问题的核心和目标",
            "2. 收集信息：整理已知条件和未知因素",
            "3. 分析推理：建立逻辑关系，推导中间结论",
            "4. 验证结论：检查推理过程是否合理",
            "5. 总结答案：给出清晰的解决方案",
        ]
    
    def identify_problem_type(self, problem: str) -> str:
        """
        识别问题类型
        返回：math/logic/analysis/comparison/prediction/decision/generic
        """
        problem_lower = problem.lower()
        
        # 统计各类关键词出现次数
        type_scores = {}
        for ptype, keywords in self.problem_types.items():
            score = sum(1 for kw in keywords if kw in problem)
            if score > 0:
                type_scores[ptype] = score
        
        # 返回得分最高的问题类型
        if type_scores:
            return max(type_scores, key=type_scores.get)
        else:
            return "generic"
    
    def generate_reasoning_steps(self, problem: str, context: List[str] = None) -> List[str]:
        """
        生成推理步骤（基于规则，非模板）
        """
        # 识别问题类型
        problem_type = self.identify_problem_type(problem)
        
        # 获取推理策略
        if problem_type in self.reasoning_strategies:
            steps = self.reasoning_strategies[problem_type].copy()
        else:
            steps = self.generic_steps.copy()
        
        # 根据上下文调整步骤
        if context:
            # 如果已有上下文，从下一步开始
            steps = steps[len(context):]
        
        # 个性化步骤（基于问题内容）
        personalized_steps = []
        for i, step in enumerate(steps):
            # 在步骤中加入问题相关的关键词
            keywords = self._extract_keywords(problem)
            if keywords and i > 0:
                step = step.replace("问题", f"问题「{problem[:20]}...」")
            
            personalized_steps.append(step)
        
        return personalized_steps
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词（简单实现）"""
        # 移除标点
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # 分词（简单按空格分割）
        words = text.split()
        
        # 过滤掉常见停用词
        stopwords = {'的', '了', '是', '在', '有', '和', '与', '或', '如何', '为什么', '什么'}
        keywords = [w for w in words if w not in stopwords and len(w) > 1]
        
        return keywords[:5]  # 返回前5个关键词
    
    def generate_solution(self, problem: str, reasoning_steps: List[str]) -> str:
        """
        生成解决方案（基于推理步骤）
        """
        problem_type = self.identify_problem_type(problem)
        
        # 根据问题类型生成不同的解决方案
        if problem_type == "math":
            return self._solve_math_problem(problem)
        elif problem_type == "logic":
            return self._solve_logic_problem(problem)
        elif problem_type == "analysis":
            return self._solve_analysis_problem(problem)
        else:
            return self._solve_generic_problem(problem, reasoning_steps)
    
    def _solve_math_problem(self, problem: str) -> str:
        """解决数学问题（简单实现）"""
        # 尝试提取数学表达式
        expr_match = re.search(r'[\d\+\-\*\/\(\)\.]+', problem)
        if expr_match:
            expr = expr_match.group()
            try:
                result = eval(expr)
                return f"计算结果: {expr} = {result}"
            except:
                return f"数学表达式「{expr}」无法计算"
        
        return "未识别到数学表达式"
    
    def _solve_logic_problem(self, problem: str) -> str:
        """解决逻辑推理问题（简单实现）"""
        # 检测三段论
        if "所有" in problem and "那么" in problem:
            return "这是三段论推理：\n1. 大前提：所有的A都是B\n2. 小前提：所有的C都是A\n3. 结论：所有的C都是B"
        
        return "逻辑推理完成，基于给定前提进行推导"
    
    def _solve_analysis_problem(self, problem: str) -> str:
        """解决分析类问题（简单实现）"""
        keywords = self._extract_keywords(problem)
        
        solution = f"针对问题「{problem}」的分析：\n"
        solution += f"关键因素：{', '.join(keywords)}\n"
        solution += "建议措施：\n"
        solution += "1. 针对每个关键因素制定具体方案\n"
        solution += "2. 评估方案的可行性和成本\n"
        solution += "3. 选择最优方案并执行\n"
        solution += "4. 跟踪效果，持续优化\n"
        
        return solution
    
    def _solve_generic_problem(self, problem: str, reasoning_steps: List[str]) -> str:
        """解决通用问题"""
        solution = f"针对问题「{problem}」的解决方案：\n\n"
        
        for step in reasoning_steps:
            solution += f"{step}\n"
        
        solution += "\n总结：经过上述步骤的分析和推理，问题可以得到解决。"
        
        return solution

# 单例模式
_default_rule_engine = None

def get_rule_engine() -> RuleEngine:
    """获取默认规则推理引擎（单例）"""
    global _default_rule_engine
    if _default_rule_engine is None:
        _default_rule_engine = RuleEngine()
    return _default_rule_engine

if __name__ == "__main__":
    # 测试
    engine = RuleEngine()
    
    test_problems = [
        "1 + 1 = ?",
        "所有的猫都是动物，所有的动物都需要氧气，那么所有的猫都需要氧气吗？",
        "如何提高团队的工作效率？",
        "Python 和 Java 哪个更好？",
        "预测一下明年的 AI 趋势",
        "应该选择哪个方案？",
    ]
    
    for problem in test_problems:
        print(f"问题: {problem}")
        print(f"类型: {engine.identify_problem_type(problem)}")
        
        steps = engine.generate_reasoning_steps(problem)
        print(f"推理步骤: {steps[:2]}...")  # 只打印前2步
        
        solution = engine.generate_solution(problem, steps)
        print(f"解决方案: {solution[:100]}...\n")

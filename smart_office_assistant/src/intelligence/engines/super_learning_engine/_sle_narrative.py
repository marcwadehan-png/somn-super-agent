"""
__all__ = [
    'analyze_narrative_structure',
    'analyze_temporal_dynamics',
    'evaluate_perspective_diversity',
    'extract_emotional_patterns',
]

叙事学习方法模块 [v4.1.0 文学智能增强]
"""

from typing import Dict

def analyze_narrative_structure(content: str, narrative_type: str) -> Dict:
    """
    分析叙事结构 - recognize起承转合模式
    """
    if not content:
        return {"patterns": ["默认线性叙事"], "coherence": 0.7, "complexity": "medium"}
    
    # 分析内容characteristics
    has_dialogue = "说" in content or "道" in content or '"' in content
    has_time_markers = any(kw in content for kw in ["后来", "当时", "那年", "从此", "终于"])
    has_multiple_pov = any(kw in content for kw in ["我觉得", "他认为", "有人说", "旁人"])
    
    # recognize叙事模式
    patterns = []
    if has_multiple_pov:
        patterns.append("多声部叙事")
    if has_time_markers:
        patterns.append("时间轴叙事")
    if has_dialogue:
        patterns.append("对话叙事")
    if len(content) > 500:
        patterns.append("深度叙事")
    
    if not patterns:
        patterns.append("基础叙事")
    
    # 评估连贯性
    coherence = min(0.95, 0.6 + len(patterns) * 0.1)
    
    return {
        "patterns": patterns,
        "coherence": round(coherence, 2),
        "complexity": "high" if len(patterns) >= 3 else ("medium" if len(patterns) >= 2 else "simple")
    }

def extract_emotional_patterns(content: str) -> Dict:
    """
    提取情感模式 - recognize叙事中的情感共鸣点
    """
    if not content:
        return {"key_emotions": [], "resonance_potential": 0.7}
    
    # 情感关键词词典
    emotion_keywords = {
        "坚韧": ["坚持", "不放弃", "忍耐", "咬牙", "挺住"],
        "温暖": ["家", "亲情", "温暖", "回忆", "守候"],
        "希望": ["未来", "梦想", "相信", "希望", "明天"],
        "挣扎": ["困境", "挣扎", "艰难", "痛苦", "折磨"],
        "突破": ["突破", "成功", "终于", "逆袭", "改变"],
        "归属": ["家乡", "故土", "根", "传统", "传承"]
    }
    
    key_emotions = []
    for emotion, keywords in emotion_keywords.items():
        count = sum(1 for kw in keywords if kw in content)
        if count > 0:
            key_emotions.append({"emotion": emotion, "intensity": count, "keywords_matched": count})
    
    # 情感共鸣潜力
    resonance = min(0.95, 0.5 + len(key_emotions) * 0.1)
    
    return {
        "key_emotions": key_emotions,
        "resonance_potential": round(resonance, 2)
    }

def evaluate_perspective_diversity(content: str) -> Dict:
    """
    评估视角多样性 - 检测多声部叙事覆盖度
    """
    if not content:
        return {"perspectives": ["默认视角"], "coverage": 0.6}
    
    perspective_markers = {
        "第一人称": ["我", "我们", "我的"],
        "第二人称": ["你", "你们", "你的"],
        "第三人称": ["他", "她", "他们", "其"],
        "集体视角": ["大家", "人们", "社会", "时代"],
        "客观视角": ["数据显示", "研究表明", "根据"]
    }
    
    perspectives = []
    for perspective, markers in perspective_markers.items():
        if any(m in content for m in markers):
            perspectives.append(perspective)
    
    coverage = min(1.0, len(perspectives) / len(perspective_markers))
    
    return {
        "perspectives": perspectives if perspectives else ["单一视角"],
        "coverage": round(coverage, 2),
        "diversity_score": round(coverage * 1.2, 2)  # 多样性加分
    }

def analyze_temporal_dynamics(content: str) -> Dict:
    """
    分析时间动力学 - recognize叙事中的时间演变模式
    
    基于: 路遥"线性时间叙事中的苦难积累与蜕变"
    """
    if not content:
        return {"phases": ["均衡态"], "trajectory": "stable"}
    
    # 时间阶段检测
    phase_keywords = {
        "困境期": ["困难", "挫折", "失败", "困境", "低谷"],
        "积累期": ["努力", "坚持", "积累", "学习", "磨练"],
        "转折期": ["转机", "突破", "机遇", "改变", "变化"],
        "上升期": ["成长", "发展", "成功", "提升", "壮大"],
        "成熟期": ["稳定", "成熟", "巩固", "传承", "持续"]
    }
    
    phases = []
    for phase, keywords in phase_keywords.items():
        if any(kw in content for kw in keywords):
            phases.append(phase)
    
    # judge时间轨迹
    if not phases:
        trajectory = "stable"
    elif "转折期" in phases and "上升期" in phases:
        trajectory = "breakthrough"
    elif "困境期" in phases and "积累期" in phases:
        trajectory = "accumulation"
    else:
        trajectory = "evolving"
    
    return {
        "phases": phases if phases else ["均衡态"],
        "trajectory": trajectory,
        "phase_count": len(phases)
    }

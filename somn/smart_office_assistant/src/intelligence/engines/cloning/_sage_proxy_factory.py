# -*- coding: utf-8 -*-
"""
贤者智能代理类工厂 v1.0.0 - 个性化P1+P2数据驱动

升级要点:
  - 从P2编码注册表(WisdomEncodingRegistry)读取个性化core_methods/cognitive_dimensions/triggers/wisdom_functions
  - 从P1蒸馏文档解析6条个性化智慧法则
  - 个性化Cloning类使用真实P1+P2数据，而非通用学派模板
  - 通用学派模板作为兜底（无P1/P2数据的贤者）
  - 修复硬编码路径为动态相对路径

数据流: P0(深度学习文档) → P1(蒸馏) → P2(编码SageCode) → P3(克隆Cloning)
"""

from typing import Dict, List, Optional, Any, Type
from ._cloning_base import SageCloning
from ._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier
from ._sage_proxy_generator import (
    get_wisdom_laws, get_school_theme, get_capability_default
)

import logging
import os
import re
import glob
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
#  名称别名映射（P0文档名 → P2编码名）
# ═══════════════════════════════════════════════════════════════

_NAME_ALIASES: Dict[str, str] = {
    "康德": "康德（Immanuel Kant）",
    "尼采": "尼采（Friedrich Nietzsche）",
    "马克思": "马克思（Karl Marx）",
    "马克斯韦伯": "马克斯·韦伯",
    "培根(哲学)": "培根",
    "杨衒之洛阳伽蓝记": "杨衒之",
    "范晔后汉书": "范晔",
    "康德（Immanuel-Kant）": "康德（Immanuel Kant）",
    "尼采（Friedrich-Nietzsche）": "尼采（Friedrich Nietzsche）",
    "马克思（Karl-Marx）": "马克思（Karl Marx）",
}

# 非人物文档（不纳入克隆系统）
_NON_PERSON_NAMES = {
    "天才向左疯子向右", "宇宙另一种真相", "神经科学的数学基础_",
    "玉台新咏", "莫言代表作品", "路遥代表作品",
}

# P2维度 → SageProfile capability 维度映射
_DIM_TO_CAPABILITY = {
    "cog_depth": "strategic_vision",
    "decision_quality": "execution",
    "value_judge": "ethical_judgment",
    "gov_decision": "governance",
    "strategy": "innovation",
    "self_mgmt": "leadership",
}


def _resolve_alias(name: str) -> str:
    """解析名称别名，返回P2编码中的标准名"""
    return _NAME_ALIASES.get(name, name)


def _build_sage_code_index() -> Dict[str, Any]:
    """
    构建P2 SageCode按名称索引
    
    Returns:
        {name: SageCode} 字典
    """
    try:
        from ...wisdom_encoding.wisdom_encoding_registry import (
            WisdomEncodingRegistry, ALL_SAGE_CODES
        )
    except ImportError:
        try:
            from src.intelligence.wisdom_encoding.wisdom_encoding_registry import (
                WisdomEncodingRegistry, ALL_SAGE_CODES
            )
        except ImportError:
            logger.warning("无法导入P2编码注册表，将使用通用模板")
            return {}
    
    index = {}
    for sage_code in ALL_SAGE_CODES:
        index[sage_code.name] = sage_code
    return index


def _parse_distillation_doc(doc_path: str) -> Dict[str, Any]:
    """
    解析P1蒸馏文档，提取个性化数据
    
    提取内容:
    - 6条智慧法则（法则一至法则六）
    - 认知维度评分
    - 身份概要（头衔、作品、专长、部门）
    - 触发关键词
    
    Returns:
        {wisdom_laws, cognitive_dims, title, works, expertise, department, triggers}
    """
    result = {
        "wisdom_laws": [],
        "cognitive_dims": {},
        "title": "",
        "works": [],
        "expertise": [],
        "department": "",
        "triggers": [],
    }
    
    if not os.path.exists(doc_path):
        return result
    
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.warning(f"读取蒸馏文档失败 {doc_path}: {e}")
        return result
    
    # 解析智慧法则：支持多种格式
    # 格式1: **法则一：xxx——yyy**
    # 格式2: **法则一：xxx**  (无破折号)
    # 格式3: 1. xxx (编号列表)
    law_patterns = [
        # 标准格式：**法则X：名称——解读**
        re.compile(r'\*\*法则[一二三四五六]：(.+?)(?:——(.+?))?\*\*'),
        # bold序号格式：**1. 名称——解读**
        re.compile(r'\*\*\d+\.\s*(.+?)(?:——(.+?))?\*\*'),
        # ###子标题格式：### 法则一：名称
        re.compile(r'###\s*法则[一二三四五六]：(.+)'),
    ]
    
    laws_found = []
    for pattern in law_patterns:
        matches = pattern.findall(content)
        if matches:
            for m in matches:
                if isinstance(m, tuple):
                    name = m[0].strip()
                    desc = m[1].strip() if len(m) > 1 and m[1] else ""
                    law_text = f"{name}——{desc}" if desc else name
                else:
                    law_text = m.strip()
                if law_text:
                    laws_found.append(law_text)
            break  # 第一个匹配到的格式即可
    
    if laws_found:
        result["wisdom_laws"] = laws_found[:6]
    
    # 解析认知维度评分
    dim_pattern = re.compile(
        r'\|\s*(认知深度|决策质量|价值判断|治理决策|战略眼光|自我管理)'
        r'\((\w+)\)\s*\|\s*(\d+\.?\d*)\s*\|'
    )
    for match in dim_pattern.finditer(content):
        dim_key = match.group(2)
        dim_val = float(match.group(3))
        result["cognitive_dims"][dim_key] = dim_val
    
    # 解析身份概要
    title_match = re.search(r'\*\*头衔\*\*:\s*(.+)', content)
    if title_match:
        result["title"] = title_match.group(1).strip()
    
    works_match = re.search(r'\*\*代表作品\*\*:\s*(.+)', content)
    if works_match:
        result["works"] = [w.strip() for w in works_match.group(1).split('、') if w.strip()]
    
    expertise_match = re.search(r'\*\*专长领域\*\*:\s*(.+)', content)
    if expertise_match:
        result["expertise"] = [e.strip() for e in expertise_match.group(1).split('、') if e.strip()]
    
    dept_match = re.search(r'\*\*所属部门\*\*:\s*(.+)', content)
    if dept_match:
        result["department"] = dept_match.group(1).strip()
    
    # 解析触发关键词
    triggers_match = re.search(r'\*\*触发关键词\*\*:\s*(.+)', content)
    if triggers_match:
        result["triggers"] = [t.strip() for t in triggers_match.group(1).split('、') if t.strip()]
    
    return result


def _find_distillation_doc(name: str, school: str) -> Optional[str]:
    """
    查找P1蒸馏文档路径
    
    搜索策略:
    1. 精确匹配: docs/蒸馏卷/{school}/{name}智慧蒸馏.md
    2. 全局搜索: docs/蒸馏卷/*/{name}智慧蒸馏.md
    """
    # 项目根目录
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
    )
    distill_base = os.path.join(project_root, 'docs', '蒸馏卷')
    
    if not os.path.exists(distill_base):
        # 尝试绝对路径（已废弃，仅作为最终回退）
        logger.warning("蒸馏卷目录未在项目根找到，请检查路径")
        return None
    
    # 策略1: 精确学派匹配
    school_map = {
        "儒家": "儒家", "道家": "道家", "佛家": "佛学", "佛学": "佛学",
        "法家": "法家", "兵家": "兵家", "墨家": "墨家", "纵横家": "纵横家",
        "医家": "医学", "史家": "史学", "文学家": "文学", "文学": "文学",
        "科学家": "科学", "经济学家": "经济", "经济": "经济",
        "投资家": "投资", "心理学家": "心理", "心理": "心理",
        "社会学家": "社会", "社会": "社会",
        "营销学家": "营销", "管理学家": "管理", "管理学": "管理",
        "企业家": "创业", "政治治理": "政治", "政治": "政治",
        "禅宗": "佛学", "心学": "心学", "理学": "理学",
        "西方哲学": "西方哲学", "外交": "外交",
    }
    
    school_dir = school_map.get(school, school)
    exact_path = os.path.join(distill_base, school_dir, f"{name}智慧蒸馏.md")
    if os.path.exists(exact_path):
        return exact_path
    
    # 策略2: 全局搜索
    for subdir in os.listdir(distill_base):
        subdir_path = os.path.join(distill_base, subdir)
        if not os.path.isdir(subdir_path):
            continue
        candidate = os.path.join(subdir_path, f"{name}智慧蒸馏.md")
        if os.path.exists(candidate):
            return candidate
    
    return None


def get_sages_from_literature_dir() -> List[Dict[str, Any]]:
    """
    从文学研究目录读取所有贤者信息，并融合P1+P2个性化数据
    
    Returns:
        [{name, school, era, lifespan, tier, titles, works, expertise,
          department, description, wisdom_laws_p1, cognitive_dims,
          triggers, core_methods, wisdom_functions, capability}, ...]
    """
    lit_dir = os.path.join(project_root, '文学研究')
    
    if not os.path.exists(lit_dir):
        logger.warning(f"文学研究目录不存在: {lit_dir}")
        return _get_default_sages()
    
    # 构建P2编码索引
    sage_code_index = _build_sage_code_index()
    logger.info(f"P2编码索引构建完成: {len(sage_code_index)}人")
    
    # 查找所有md文件
    md_files = glob.glob(os.path.join(lit_dir, "*深度学习文档.md"))
    
    sages = []
    p1_hit = 0
    p2_hit = 0
    
    for fpath in md_files:
        fname = os.path.basename(fpath)
        name = fname.replace("深度学习文档.md", "").strip()
        
        if not name or name in _NON_PERSON_NAMES:
            continue
        
        # 解析别名
        resolved_name = _resolve_alias(name)
        
        # 基础推断（兜底）
        school = _infer_school(name, fpath)
        era = _infer_era(name)
        
        sage_data = {
            "name": name,
            "school": school,
            "era": era,
            "lifespan": "",
            "tier": "SCHOLAR",
            "titles": [],
            "works": _extract_works(name),
            "expertise": _infer_expertise(name, school),
            "department": "礼部",
            "description": f"{era}{school}学者",
            # P1+P2个性化数据（初始为空，后续填充）
            "wisdom_laws_p1": [],
            "cognitive_dims": {},
            "triggers": [],
            "core_methods": [],
            "wisdom_functions": [],
            "capability": {},
        }
        
        # ── 从P1蒸馏文档提取 ──
        p1_doc = _find_distillation_doc(name, school)
        if p1_doc:
            p1_data = _parse_distillation_doc(p1_doc)
            sage_data["wisdom_laws_p1"] = p1_data["wisdom_laws"]
            sage_data["cognitive_dims"] = p1_data["cognitive_dims"]
            sage_data["triggers"] = p1_data["triggers"]
            if p1_data["title"]:
                sage_data["titles"] = [p1_data["title"]]
            if p1_data["works"]:
                sage_data["works"] = p1_data["works"]
            if p1_data["expertise"]:
                sage_data["expertise"] = p1_data["expertise"]
            if p1_data["department"]:
                sage_data["department"] = p1_data["department"]
            p1_hit += 1
        
        # ── 从P2 SageCode提取 ──
        sage_code = sage_code_index.get(resolved_name)
        if sage_code:
            sage_data["core_methods"] = sage_code.core_methods
            sage_data["wisdom_functions"] = sage_code.wisdom_functions
            sage_data["triggers"] = sage_data["triggers"] or sage_code.triggers
            sage_data["school"] = sage_code.school  # P2的学派分类更准确
            sage_data["era"] = sage_code.era  # P2的时代也更新
            # P2认知维度覆盖P1（更精细）
            if sage_code.cognitive_dimensions:
                sage_data["cognitive_dims"] = sage_code.cognitive_dimensions
            # P2系统映射
            if sage_code.system_mapping:
                dept = sage_code.system_mapping.get("department", "")
                if dept and dept != "—":
                    sage_data["department"] = dept
            p2_hit += 1
        elif resolved_name != name:
            # 尝试用别名再查找
            sage_code = sage_code_index.get(name)
            if sage_code:
                sage_data["core_methods"] = sage_code.core_methods
                sage_data["wisdom_functions"] = sage_code.wisdom_functions
                sage_data["triggers"] = sage_data["triggers"] or sage_code.triggers
                sage_data["school"] = sage_code.school
                sage_data["era"] = sage_code.era
                if sage_code.cognitive_dimensions:
                    sage_data["cognitive_dims"] = sage_code.cognitive_dimensions
                if sage_code.system_mapping:
                    dept = sage_code.system_mapping.get("department", "")
                    if dept and dept != "—":
                        sage_data["department"] = dept
                p2_hit += 1
        
        # ── 映射认知维度到capability ──
        sage_data["capability"] = _map_cognitive_dims_to_capability(
            sage_data["cognitive_dims"], school
        )
        
        sages.append(sage_data)
    
    logger.info(
        f"从文学研究目录读取了 {len(sages)} 个贤者 | "
        f"P1蒸馏命中: {p1_hit} | P2编码命中: {p2_hit}"
    )
    return sages if sages else _get_default_sages()


def _map_cognitive_dims_to_capability(
    cognitive_dims: Dict[str, float],
    school: str
) -> Dict[str, float]:
    """
    将P2认知维度(cog_depth等6维)映射到SageProfile的capability字典
    
    映射规则:
    - cog_depth → strategic_vision (认知深度→战略视野)
    - decision_quality → execution (决策质量→执行力)
    - value_judge → ethical_judgment (价值判断→伦理判断)
    - gov_decision → governance (治理决策→治理能力)
    - strategy → innovation (战略眼光→创新能力)
    - self_mgmt → leadership (自我管理→领导力)
    
    无P2数据时使用通用学派默认值
    """
    if cognitive_dims:
        capability = {}
        for dim_key, cap_key in _DIM_TO_CAPABILITY.items():
            val = cognitive_dims.get(dim_key)
            if val is not None:
                capability[cap_key] = int(val)  # SageProfile用int
        # 补充剩余维度
        for extra_key in ["dialectical_reasoning", "practical_wisdom",
                          "long_term_vision", "crisis_response",
                          "system_thinking", "pattern_recognition",
                          "communication", "conflict_resolution"]:
            if extra_key not in capability:
                capability[extra_key] = 7  # 默认中等
        return capability
    else:
        # 兜底：使用通用学派默认
        return get_capability_default(school)


def _infer_school(name: str, fpath: str) -> str:
    """根据文件名推断学派"""
    name_lower = name.lower()
    
    if "儒" in name or "论语" in name or "孟子" in name:
        return "儒家"
    if "道" in name or "道德经" in name or "庄子" in name or "老子" in name:
        return "道家"
    if "佛" in name or "禅" in name or "金刚经" in name:
        return "佛家"
    if "法" in name or "韩非" in name:
        return "法家"
    if "兵" in name or "孙武" in name or "孙子" in name:
        return "兵家"
    if "墨" in name or "墨子" in name:
        return "墨家"
    if "纵横" in name or "苏秦" in name or "张仪" in name:
        return "纵横家"
    if "医" in name or "本草" in name:
        return "医家"
    if "史" in name or "史记" in name or "汉书" in name:
        return "史家"
    if "诗" in name or "词" in name or "杜甫" in name or "李白" in name or "苏轼" in name:
        return "文学"
    if "科学家" in name or "数学" in name or "物理" in name:
        return "科学家"
    if "投资" in name or "巴菲" in name or "索罗" in name:
        return "投资家"
    if "管理" in name or "德鲁" in name:
        return "管理学家"
    if "营销" in name or "科特" in name:
        return "营销学家"
    if "心理" in name:
        return "心理学家"
    if "素书" in name:
        return "法家"
    if "鸿铭" in name:
        return "儒家"
    
    return "儒家"


def _infer_era(name: str) -> str:
    """根据名字推断时代"""
    if any(k in name for k in ["孔子", "孟子", "老子", "庄子", "墨子"]):
        return "先秦"
    if any(k in name for k in ["韩非", "荀子", "商鞅", "孙子", "鬼谷"]):
        return "先秦"
    if any(k in name for k in ["秦始皇", "李斯", "刘邦", "项羽"]):
        return "秦汉"
    if any(k in name for k in ["汉武帝", "司马迁", "董仲舒"]):
        return "西汉"
    if any(k in name for k in ["王莽", "刘秀"]):
        return "东汉"
    if any(k in name for k in ["曹操", "刘备", "诸葛亮", "曹丕"]):
        return "三国"
    if any(k in name for k in ["李白", "杜甫", "王维", "白居易"]):
        return "唐代"
    if any(k in name for k in ["苏轼", "王安石", "欧阳修", "司马光"]):
        return "北宋"
    if any(k in name for k in ["朱熹", "陆九渊", "辛弃疾", "岳飞"]):
        return "南宋"
    if any(k in name for k in ["王阳明", "唐伯虎", "张居正"]):
        return "明代"
    if any(k in name for k in ["康熙", "雍正", "乾隆", "曾国藩"]):
        return "清代"
    if any(k in name for k in ["孙中山", "鲁迅", "胡适", "辜鸿铭"]):
        return "近现代"
    if any(k in name for k in ["巴菲特", "索罗斯", "彼得林奇"]):
        return "当代"
    if any(k in name for k in ["德鲁克", "科特勒"]):
        return "当代"
    
    return "历代"


def _extract_works(name: str) -> List[str]:
    """从名字提取作品"""
    works = []
    known_works = {
        "论语": ["论语"],
        "孟子": ["孟子"],
        "道德经": ["道德经"],
        "庄子": ["庄子"],
        "荀子": ["荀子"],
        "韩非子": ["韩非子"],
        "孙子兵法": ["孙子兵法"],
        "鬼谷子": ["鬼谷子"],
        "大学": ["大学"],
        "中庸": ["中庸"],
        "素书": ["素书"],
        "贞观政要": ["贞观政要"],
        "资治通鉴": ["资治通鉴"],
        "史记": ["史记"],
        "汉书": ["汉书"],
        "后汉书": ["后汉书"],
        "三国演义": ["三国演义"],
        "传习录": ["传习录"],
        "四书章句集注": ["四书章句集注"],
        "春秋繁露": ["春秋繁露"],
        "日知录": ["日知录"],
    }
    for work, names in known_works.items():
        for n in names:
            if n in name:
                works.append(work)
    return works


def _infer_expertise(name: str, school: str) -> List[str]:
    """推断专长领域"""
    school_expertise = {
        "儒家": ["仁学", "礼治", "教育", "德治"],
        "道家": ["道法自然", "无为而治", "逍遥", "太极"],
        "佛家": ["慈悲", "解脱", "禅定", "因缘"],
        "佛学": ["慈悲", "解脱", "禅定", "因缘"],
        "法家": ["法治", "刑名", "权术", "耕战"],
        "兵家": ["战略", "战术", "军令", "地形"],
        "墨家": ["兼爱", "非攻", "尚贤", "节用"],
        "纵横家": ["合纵", "连横", "游说", "外交"],
        "医家": ["阴阳", "五行", "经络", "本草"],
        "医学": ["阴阳", "五行", "经络", "本草"],
        "史家": ["史学", "考据", "纪传", "编年"],
        "史学": ["史学", "考据", "纪传", "编年"],
        "文学": ["诗词", "散文", "辞赋", "小说"],
        "科学家": ["格物", "致知", "创新", "实验"],
        "科学": ["格物", "致知", "创新", "实验"],
        "经济学家": ["富国", "裕民", "市场", "制度"],
        "经济": ["富国", "裕民", "市场", "制度"],
        "投资家": ["价值", "长期", "复利", "护城河"],
        "投资": ["价值", "长期", "复利", "护城河"],
        "心理学家": ["认知", "行为", "情感", "发展"],
        "心理": ["认知", "行为", "情感", "发展"],
        "社会学家": ["社会", "结构", "文化", "制度"],
        "社会": ["社会", "结构", "文化", "制度"],
        "营销学家": ["市场", "定位", "品牌", "客户"],
        "营销": ["市场", "定位", "品牌", "客户"],
        "管理学家": ["组织", "决策", "领导", "效率"],
        "管理": ["组织", "决策", "领导", "效率"],
        "企业家": ["创新", "创造", "执行", "整合"],
        "创业": ["创新", "创造", "执行", "整合"],
        "政治治理": ["治国", "安邦", "选贤", "法治"],
        "政治": ["治国", "安邦", "选贤", "法治"],
        "心学": ["心即理", "知行合一", "致良知", "事上磨练"],
        "理学": ["格物", "穷理", "存诚", "居敬"],
        "西方哲学": ["理性", "逻辑", "批判", "思辨"],
        "外交": ["合纵", "连横", "游说", "谈判"],
    }
    return school_expertise.get(school, ["智慧", "处世"])


def _get_default_sages() -> List[Dict[str, Any]]:
    """默认贤者列表（备用）"""
    return [
        {"name": "孔子", "school": "儒家", "era": "先秦", "tier": "FOUNDER", "expertise": ["仁学", "礼治", "教育"]},
        {"name": "孟子", "school": "儒家", "era": "先秦", "tier": "FOUNDER", "expertise": ["性善论", "仁政"]},
        {"name": "老子", "school": "道家", "era": "先秦", "tier": "FOUNDER", "expertise": ["道法自然", "无为"]},
        {"name": "庄子", "school": "道家", "era": "先秦", "tier": "MASTER", "expertise": ["逍遥", "齐物"]},
        {"name": "韩非", "school": "法家", "era": "先秦", "tier": "FOUNDER", "expertise": ["法治", "刑名"]},
        {"name": "孙子", "school": "兵家", "era": "先秦", "tier": "FOUNDER", "expertise": ["战略", "战术"]},
        {"name": "王阳明", "school": "心学", "era": "明代", "tier": "MASTER", "expertise": ["心学", "知行合一"]},
        {"name": "朱熹", "school": "理学", "era": "南宋", "tier": "MASTER", "expertise": ["理学", "格物致知"]},
    ]


class SageProxyFactory:
    """贤者智能代理工厂 v1.0 — P1+P2个性化数据驱动"""

    @staticmethod
    def create_cloning_class(
        name: str,
        school: str,
        era: str,
        lifespan: str = "",
        tier: str = "SCHOLAR",
        titles: List[str] = None,
        works: List[str] = None,
        expertise: List[str] = None,
        department: str = "",
        description: str = "",
        # v2.0新增：P1+P2个性化数据
        wisdom_laws_p1: List[str] = None,
        cognitive_dims: Dict[str, float] = None,
        triggers: List[str] = None,
        core_methods: List[str] = None,
        wisdom_functions: List[str] = None,
        capability: Dict[str, float] = None,
    ) -> Type[SageCloning]:
        """
        动态创建一个贤者代理Cloning类 — 个性化P1+P2数据驱动
        
        数据优先级:
        1. P1个性化智慧法则 > 通用学派模板
        2. P2 core_methods > P1 wisdom_laws > 通用学派laws
        3. P2 cognitive_dimensions > P1 cognitive_dims > 通用学派defaults
        """
        titles = titles or []
        works = works or []
        expertise = expertise or []
        wisdom_laws_p1 = wisdom_laws_p1 or []
        cognitive_dims = cognitive_dims or {}
        triggers = triggers or []
        core_methods = core_methods or []
        wisdom_functions = wisdom_functions or []

        # 映射tier
        tier_map = {
            "FOUNDER": CloningTier.TIER1_CORE,
            "MASTER": CloningTier.TIER1_CORE,
            "SCHOLAR": CloningTier.TIER2_CLUSTER,
            "PRACTITIONER": CloningTier.TIER2_CLUSTER,
        }
        cloning_tier = tier_map.get(tier, CloningTier.TIER2_CLUSTER)

        # ── 智慧法则优先级: P1个性化 > P2 core_methods > 通用学派 ──
        if wisdom_laws_p1:
            wisdom_laws = wisdom_laws_p1[:6]
        elif core_methods:
            wisdom_laws = core_methods[:6]
        else:
            wisdom_laws = get_wisdom_laws(school, 6)

        # 学派主题
        school_theme = get_school_theme(school)

        # 能力向量（P2个性化 > 通用学派默认）
        if capability:
            final_capability = capability
        else:
            final_capability = get_capability_default(school)

        # 创建类名
        safe_name = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]', '_', name)
        class_name = f"_Proxy{safe_name}Cloning"

        # ── 个性化分析/决策/建议方法 ──
        
        def make_analyze_method(w_name, w_school, w_theme, w_laws, w_triggers, w_core_methods):
            def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
                context = context or {}
                user_prefs = context.get("user_preferences", {})
                industry = context.get("industry", "")
                
                # 根据触发词匹配提升置信度
                confidence_boost = 0.0
                if w_triggers:
                    trigger_hits = sum(1 for t in w_triggers[:8] if t in problem)
                    confidence_boost = min(0.08, trigger_hits * 0.02)
                
                if industry and any(kw in problem for kw in [industry, industry.replace("_", "")]):
                    confidence_boost += 0.05
                
                # 核心洞察：优先使用P1/P2个性化法则
                if w_core_methods:
                    core_insight = w_core_methods[0]
                elif w_laws and "——" in w_laws[0]:
                    core_insight = w_laws[0].split("——")[1]
                elif w_laws:
                    core_insight = w_laws[0]
                else:
                    core_insight = f"从{w_name}的{w_school}智慧出发"
                
                # 推荐列表：来自P1/P2法则
                recommendations = []
                for law in w_laws:
                    if "——" in law:
                        recommendations.append(law.split("——")[1])
                    else:
                        recommendations.append(law)
                
                return AnalysisResult(
                    sage_name=w_name,
                    school=w_school,
                    problem=problem,
                    perspective=f"从{w_name}的{w_school}智慧出发",
                    core_insight=core_insight,
                    recommendations=recommendations,
                    wisdom_laws_applied=w_laws,
                    confidence=min(0.95, 0.82 + confidence_boost),
                )
            return analyze

        def make_decide_method(w_name, w_expertise, w_triggers):
            def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
                context = context or {}
                
                # 个性化评分：结合专长和触发词
                def score_fn(o):
                    base = 7.0
                    # 专长匹配
                    base += sum(1.5 for kw in w_expertise[:3] if kw in o)
                    # 触发词匹配（P2个性化触发词）
                    if w_triggers:
                        base += sum(0.8 for t in w_triggers[:5] if t in o)
                    # 通用决策关键词
                    base += sum(1.0 for kw in ["战略", "决策", "选择", "规划"] if kw in o)
                    return base
                
                chosen = max(options, key=score_fn)
                return DecisionResult(
                    sage_name=w_name,
                    problem=context.get("problem", ""),
                    chosen_option=chosen,
                    confidence=0.80
                )
            return decide

        def make_advise_method(w_name, w_theme, w_laws, w_core_methods, w_triggers):
            def advise(self, context: Dict[str, Any]) -> str:
                context = context or {}
                objective = context.get("objective", "")
                industry = context.get("industry", "")
                
                # 个性化建议：使用P1/P2数据
                base_advice = f"{w_name}的智慧：以{w_theme}为核心"
                
                # 展示个性化法则
                if w_core_methods and len(w_core_methods) >= 2:
                    base_advice += f"\n核心方法论：{w_core_methods[0]}、{w_core_methods[1]}"
                elif w_laws:
                    first_law = w_laws[0].split("——")[1] if "——" in w_laws[0] else w_laws[0]
                    base_advice += f"\n核心法则：{first_law}"
                
                if industry:
                    base_advice += f"\n针对{industry}行业："
                    if w_core_methods and len(w_core_methods) >= 2:
                        base_advice += f" {w_core_methods[1]}"
                    elif len(w_laws) >= 2:
                        base_advice += f" {w_laws[1].split('——')[1] if '——' in w_laws[1] else w_laws[1]}"
                
                if objective:
                    base_advice += f"\n实现目标'{objective}'："
                    if w_core_methods and len(w_core_methods) >= 3:
                        base_advice += f" {w_core_methods[2]}"
                    elif len(w_laws) >= 3:
                        base_advice += f" {w_laws[2].split('——')[1] if '——' in w_laws[2] else w_laws[2]}"
                
                return base_advice
            return advise

        def make_init_method(w_name, w_school, w_era, w_lifespan, w_titles, w_works,
                              w_expertise, w_department, w_description, w_tier, w_capability,
                              w_triggers, w_core_methods, w_wisdom_functions):
            def __init__(self):
                title_str = "/".join(w_titles) if w_titles else "贤者"
                works_str = "/".join(w_works) if w_works else ""
                desc = w_description or f"{w_era}{w_school}学者"
                super(self.__class__, self).__init__(SageProfile(
                    name=w_name,
                    name_en=w_name,
                    era=w_era,
                    years=w_lifespan,
                    school=w_school,
                    tier=w_tier,
                    position=title_str,
                    department=w_department or "礼部",
                    title=title_str,
                    biography=desc,
                    core_works=[works_str] if works_str else [],
                    capability=w_capability,
                ))
                # 存储P2个性化数据到实例（供高级查询使用）
                self._triggers = w_triggers
                self._core_methods = w_core_methods
                self._wisdom_functions = w_wisdom_functions
            return __init__

        # 构建类属性字典
        namespace = {
            '__init__': make_init_method(
                name, school, era, lifespan, titles, works, expertise, department,
                description, cloning_tier, final_capability,
                triggers, core_methods, wisdom_functions,
            ),
            'analyze': make_analyze_method(name, school, school_theme, wisdom_laws, triggers, core_methods),
            'decide': make_decide_method(name, expertise, triggers),
            'advise': make_advise_method(name, school_theme, wisdom_laws, core_methods, triggers),
        }

        return type(class_name, (SageCloning,), namespace)

    @staticmethod
    def create_cluster_proxy(
        sage_list: List[Dict[str, Any]]
    ) -> Dict[str, SageCloning]:
        """为一组贤者创建代理Cloning实例 — v2.0个性化"""
        result = {}
        for sage in sage_list:
            try:
                cls = SageProxyFactory.create_cloning_class(
                    name=sage.get("name", "未知"),
                    school=sage.get("school", "儒家"),
                    era=sage.get("era", "未知"),
                    lifespan=sage.get("lifespan", ""),
                    tier=sage.get("tier", "SCHOLAR"),
                    titles=sage.get("titles", []),
                    works=sage.get("works", []),
                    expertise=sage.get("expertise", []),
                    department=sage.get("department", ""),
                    description=sage.get("description", ""),
                    # v2.0个性化参数
                    wisdom_laws_p1=sage.get("wisdom_laws_p1", []),
                    cognitive_dims=sage.get("cognitive_dims", {}),
                    triggers=sage.get("triggers", []),
                    core_methods=sage.get("core_methods", []),
                    wisdom_functions=sage.get("wisdom_functions", []),
                    capability=sage.get("capability", {}),
                )
                instance = cls()
                result[sage.get("name", "未知")] = instance
            except Exception as e:
                logger.warning(f"创建贤者代理失败 {sage.get('name', '未知')}: {e}")
        return result


def build_sage_proxies_from_literature() -> Dict[str, SageCloning]:
    """
    从文学研究目录读取所有贤者，生成个性化代理Cloning
    
    v2.0升级: 融合P1蒸馏文档+P2编码注册表数据
    
    Returns:
        {name: SageCloning实例} 字典
    """
    sages = get_sages_from_literature_dir()
    proxies = SageProxyFactory.create_cluster_proxy(sages)
    
    # 统计个性化覆盖率
    p1_count = sum(1 for s in sages if s.get("wisdom_laws_p1"))
    p2_count = sum(1 for s in sages if s.get("core_methods"))
    
    logger.info(
        f"从文学研究目录生成 {len(proxies)} 个贤者代理Cloning | "
        f"P1个性化: {p1_count}/{len(sages)} | P2个性化: {p2_count}/{len(sages)}"
    )
    return proxies

# -*- coding: utf-8 -*-
"""
Global Code Optimizer v1.0
Converts Chinese code identifiers to pinyin/English while preserving functionality.
"""

import os
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Chinese to pinyin/English mapping for common terms
PYTHON_MAPPING = {
    # Initialization patterns
    '初始化': 'init',
    '初始化代表作品': 'init_representative_works',
    '初始化名篇': 'init_famous_poems',
    '初始化心诀': 'init_spiritual_insight',
    '初始化特征': 'init_characteristics',
    '初始化启示': 'init_revelations',
    '初始化词学贡献': 'init_poetry_contributions',
    '初始化词作特色': 'init_poetry_style',
    '初始化辋川': 'init_wangchuan',
    '初始化风格特征': 'init_style_features',
    '初始化词人信息': 'init_poet_info',
    '初始化词牌库': 'init_ci_patterns',
    '初始化意象库': 'init_imagery',
    '初始化映射': 'init_mapping',
    '初始化所有引擎': 'init_all_engines',
    '初始化流派映射': 'init_school_mapping',
    '初始化融合指标': 'init_fusion_metrics',
    '初始化意象': 'recognize_imagery',
    '初始化所有': 'init_all',
    
    # Analysis patterns
    '分析情感': 'analyze_emotion',
    '分析风格': 'analyze_style',
    '识别意象': 'recognize_imagery',
    '判断风格': 'judge_style',
    
    # Fusion patterns
    '融合策略': 'fusion_strategy',
    '融合点': 'fusion_point',
    '生成心学依据': 'generate_xinxue_basis',
    '生成纠正行动': 'generate_corrective_action',
    '综合决策': 'synthesize_decision',
    '获取融合策略': 'get_fusion_strategy',
    '获取融合点': 'get_fusion_point',
    
    # Common patterns
    '代表作品': 'representative_works',
    '心诀': 'spiritual_insight',
    '启示': 'revelations',
    '特征': 'characteristics',
    '风格': 'style',
    '意象': 'imagery',
    '融合': 'fusion',
    '策略': 'strategy',
    '决策': 'decision',
    '综合': 'synthesize',
    '生成': 'generate',
    '获取': 'get',
    '判断': 'judge',
    '识别': 'recognize',
    
    # System names (keep some)
    'P2级融合系统实例': 'P2FusionSystemInstance',
    'P2级统一融合系统': 'P2UnifiedFusionSystem',
    '统一融合系统': 'UnifiedFusionSystem',
    
    # Domain patterns
    '心学': 'xinxue',
    '词学': 'ci_study',
    '词牌': 'ci_pattern',
    '词人': 'poet',
    '诗人': 'poet',
    '名篇': 'famous_poems',
    '意象库': 'imagery_database',
    '风格特征': 'style_features',
    '词人信息': 'poet_info',
    '流派映射': 'school_mapping',
    '融合指标': 'fusion_metrics',
    '词学贡献': 'poetry_contributions',
    '词作特色': 'poetry_style',
    
    # Other common terms
    '统一': 'unified',
    '映射': 'mapping',
    '指标': 'metrics',
    '系统实例': 'system_instance',
    '依据': 'basis',
    '行动': 'action',
    '纠正': 'corrective',
    '辋川': 'wangchuan',
}

# Simple pinyin mapping for single characters
PINYIN_MAP = {
    '初': 'chu', '始': 'shi', '化': 'hua', '名': 'ming', '篇': 'pian',
    '心': 'xin', '诀': 'jue', '特': 'te', '征': 'zheng', '风': 'feng',
    '格': 'ge', '启': 'qi', '示': 'shi', '词': 'ci', '学': 'xue',
    '贡': 'gong', '献': 'xian', '作': 'zuo', '色': 'se', '风': 'feng',
    '格': 'ge', '者': 'zhe', '人': 'ren', '诗': 'shi', '象': 'xiang',
    '库': 'ku', '融': 'rong', '合': 'he', '策': 'ce', '略': 'lue',
    '点': 'dian', '判': 'pan', '断': 'duan', '识': 'shi', '别': 'bie',
    '获': 'huo', '取': 'qu', '生': 'sheng', '成': 'cheng', '综': 'zong',
    '合': 'he', '统': 'tong', '一': 'yi', '映': 'ying', '射': 'she',
    '据': 'ju', '基': 'ji', '础': 'chu', '行': 'xing', '动': 'dong',
    '纠': 'jiu', '正': 'zheng', '修': 'xiu', '正': 'zheng', '补': 'bu',
    '充': 'chong', '替': 'ti', '代': 'dai', '删': 'shan', '除': 'chu',
    '查': 'cha', '询': 'xun', '找': 'zhao', '定': 'ding', '位': 'wei',
    '设': 'she', '置': 'zhi', '改': 'gai', '变': 'bian', '调': 'tiao',
    '整': 'zheng', '管': 'guan', '理': 'li', '控': 'kong', '输': 'shu',
    '入': 'ru', '出': 'chu', '数': 'shu', '据': 'ju', '内': 'nei',
    '容': 'rong', '文': 'wen', '本': 'ben', '句': 'ju', '段': 'duan',
    '书': 'shu', '页': 'ye', '标': 'biao', '题': 'ti', '签': 'qian',
    '列': 'lie', '表': 'biao', '记': 'ji', '录': 'lu', '志': 'zhi',
    '志': 'zhi', '志': 'zhi', '日': 'ri', '志': 'zhi', '志': 'zhi',
}


def to_pinyin(chinese_str):
    """Convert Chinese string to pinyin."""
    if not chinese_str:
        return chinese_str
    
    # Check if it's a known mapping
    if chinese_str in PYTHON_MAPPING:
        return PYTHON_MAPPING[chinese_str]
    
    # Try to convert character by character
    result = []
    for char in chinese_str:
        if '\u4e00' <= char <= '\u9fff':  # Chinese character
            result.append(PINYIN_MAP.get(char, char))
        else:
            result.append(char)
    
    return ''.join(result)


def convert_file(filepath):
    """Convert Chinese identifiers in a file to pinyin/English."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Replace known mappings first
        for cn, en in sorted(PYTHON_MAPPING.items(), key=lambda x: -len(x[0])):
            content = content.replace(cn, en)
        
        # Also handle patterns like _初始化名篇 -> _init_famous_poems
        # Look for Chinese after underscore
        def replace_chinese_after_underscore(match):
            prefix = match.group(1)
            chinese = match.group(2)
            pinyin = to_pinyin(chinese)
            return prefix + pinyin
        
        # Pattern: underscore followed by Chinese
        content = re.sub(r'(_)([\u4e00-\u9fff]+)', replace_chinese_after_underscore, content)
        
        # Pattern: def/function Chinese names
        content = re.sub(r'(def\s+)([\u4e00-\u9fff]+)', 
                        lambda m: m.group(1) + to_pinyin(m.group(2)), content)
        
        # Pattern: class Chinese names
        content = re.sub(r'(class\s+)([\u4e00-\u9fff]+)',
                        lambda m: m.group(1) + to_pinyin(m.group(2)), content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, filepath
        return False, None
    except Exception as e:
        logger.error(f"Error processing {filepath}: {e}")
        return False, None


def process_directory(src_dir):
    """Process all Python files in a directory."""
    count = 0
    files = []
    
    for root, dirs, filenames in os.walk(src_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.trash', '.pytest_cache', '.git', 'node_modules']]
        
        for f in filenames:
            if f.endswith('.py'):
                filepath = os.path.join(root, f)
                changed, result = convert_file(filepath)
                if changed:
                    count += 1
                    files.append(result)
    
    return count, files


if __name__ == '__main__':
    import sys
    
    # Default directory
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    
    if len(sys.argv) > 1:
        src_dir = sys.argv[1]
    
    logger.info(f"Processing directory: {src_dir}")
    count, files = process_directory(src_dir)
    
    logger.info(f"\n=== Conversion Complete ===")
    logger.info(f"Total files modified: {count}")
    
    if files:
        logger.info("\nModified files:")
        for f in files[:20]:
            logger.info(f"  - {f}")
        if len(files) > 20:
            logger.info(f"  ... and {len(files) - 20} more")

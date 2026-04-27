"""神经元智慧网络 - 智慧学派定义(精简版)"""

# 核心智慧学派定义
WISDOM_SCHOOLS = {
    "CONFUCIAN": {
        "name": "儒家", "tag": "以儒治世",
        "keywords": ["仁义", "道德", "伦理", "秩序", "忠恕", "修身", "齐家", "治国", "平天下"],
        "problems": ["ETHICAL", "GOVERNANCE", "TALENT", "CULTURE"],
        "activation_pattern": "gradual",
        "mutual_enhance": ["SUFU", "HONGMING"], "mutual_inhibit": []
    },
    "DAOIST": {
        "name": "道家", "tag": "以道治身",
        "keywords": ["道法自然", "无为", "柔弱", "玄德", "阴阳", "太极", "逍遥", "返璞", "归真"],
        "problems": ["STRATEGY", "CRISIS", "CHANGE", "BALANCE", "TIMING"],
        "activation_pattern": "resonant",
        "mutual_enhance": ["BUDDHIST", "METAPHYSICS"], "mutual_inhibit": ["MILITARY"]
    },
    "BUDDHIST": {
        "name": "佛家", "tag": "以佛治心",
        "keywords": ["空", "缘起", "无常", "四谛", "八正道", "般若", "禅定", "慈悲", "放下"],
        "problems": ["MINDSET", "HARMONY", "INTEREST", "LONGTERM"],
        "activation_pattern": "resonant",
        "mutual_enhance": ["DAOIST", "CONFUCIAN"], "mutual_inhibit": []
    },
    "SUFU": {
        "name": "素书", "tag": "五德决策",
        "keywords": ["道", "德", "仁", "义", "礼", "人才", "修身", "福祸"],
        "problems": ["LEADERSHIP", "RISK", "FORTUNE", "PERSONNEL"],
        "activation_pattern": "sharp",
        "mutual_enhance": ["MILITARY", "CONFUCIAN"], "mutual_inhibit": []
    },
    "MILITARY": {
        "name": "兵法", "tag": "三十六计",
        "keywords": ["知己知彼", "兵不厌诈", "出奇制胜", "因势利导", "以逸待劳", "瞒天过海"],
        "problems": ["COMPETITION", "ATTACK", "DEFENSE", "NEGOTIATION"],
        "activation_pattern": "sharp",
        "mutual_enhance": ["SUFU", "CIVILIZATION"], "mutual_inhibit": ["DAOIST"]
    },
    "YANGMING": {
        "name": "王阳明心学", "tag": "知行合一",
        "keywords": ["致良知", "知行合一", "事上磨练", "心即理", "格物致知", "万物一体"],
        "problems": ["MINDSET", "GROWTH", "ETHICAL", "CLOSED_LOOP"],
        "activation_pattern": "resonant",
        "mutual_enhance": ["CONFUCIAN", "BUDDHIST"], "mutual_inhibit": []
    },
    "GROWTH": {
        "name": "成长思维", "tag": "持续迭代",
        "keywords": ["成长", "迭代", "突破", "极限", "思维模式", "努力", "坚持", "学习"],
        "problems": ["GROWTH_MINDSET", "CLOSED_LOOP"],
        "activation_pattern": "sharp",
        "mutual_enhance": ["SCI_FI", "BEHAVIOR"], "mutual_inhibit": []
    },
    "SCIENCE": {
        "name": "科学思维", "tag": "证据为先",
        "keywords": ["科学", "证据", "假设", "验证", "系统", "模型", "数据", "分析"],
        "problems": ["SCIENTIFIC_METHOD", "SYSTEM_THINKING", "EVIDENCE"],
        "activation_pattern": "sharp",
        "mutual_enhance": ["BEHAVIOR", "NATURAL_SCIENCE"], "mutual_inhibit": []
    },
    "MATH": {
        "name": "数学智慧", "tag": "数列之美",
        "keywords": ["数列", "斐波那契", "黄金分割", "概率", "统计", "博弈", "最优化"],
        "problems": ["PROBABILITY", "GAME_THEORY", "OPTIMIZATION"],
        "activation_pattern": "sharp",
        "mutual_enhance": ["SCIENCE", "LOGIC"], "mutual_inhibit": []
    },
    "SOCIAL_SCIENCE": {
        "name": "社会科学", "tag": "经营经济",
        "keywords": ["营销", "市场", "经济", "增长", "STP", "4P", "蓝海", "波特", "品牌"],
        "problems": ["MARKET_ANALYSIS", "COMPETITIVE_STRATEGY", "GROWTH_STRATEGY"],
        "activation_pattern": "sharp",
        "mutual_enhance": ["MILITARY", "GROWTH", "BEHAVIOR"], "mutual_inhibit": []
    },
}

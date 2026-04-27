__all__ = [
    'generate_honglou_actions',
    'get_honglou_wisdom',
    'get_recommend_honglou_case',
    'summarize_honglou_wisdom',
]

# -*- coding: utf-8 -*-
"""四大名著智慧 - 红楼梦模块"""

from typing import Dict, List, Any

def get_honglou_wisdom() -> Dict[str, Any]:
    """获取红楼梦智慧库"""
    return {
        # 家族兴衰周期
        "family_cycle": {
            "鼎盛期": {
                "标志": "元春省亲--烈火烹油,鲜花着锦",
                "特征": "经济繁荣,人丁兴旺,社会地位高",
                "启示": "繁华时的危机意识"
            },
            "转折期": {
                "标志": "抄检大观园--矛盾开始爆发",
                "特征": "内部争斗,资源浪费,方向迷失",
                "启示": "问题往往从内部开始"
            },
            "衰落期": {
                "标志": "贾母去世,凤姐病逝",
                "特征": "领导力真空,人心涣散",
                "启示": "核心人物的重要性"
            },
            "败落期": {
                "标志": "贾府被抄--大厦倾覆",
                "特征": "树倒猢狲散",
                "启示": "没有永远的靠山"
            }
        },

        # 人物关系分析
        "relationships": {
            "核心三角": {
                "贾宝玉": {
                    "定位": "核心人物,家族希望",
                    "性格": "叛逆,多情,善良,不喜功名",
                    "命运": "出家--看破红尘"
                },
                "林黛玉": {
                    "定位": "精神伴侣,情感寄托",
                    "性格": "才情绝世,多愁多病,清高孤傲",
                    "命运": "泪尽而亡--还完前世眼泪"
                },
                "薛宝钗": {
                    "定位": "现实选择,世俗成功",
                    "性格": "温柔敦厚,端庄贤淑,城府深沉",
                    "命运": "独守空房--金玉良缘的悲剧"
                }
            },
            "木石前盟 vs 金玉良缘": {
                "木石前盟": "理想主义--追求真挚爱情",
                "金玉良缘": "现实主义--追求世俗成功",
                "悲剧": "理想与现实无法调和"
            }
        },

        # 组织政治智慧
        "organizational_politics": {
            "王熙凤协理宁国府": {
                "优点": "精明能干,雷厉风行",
                "缺点": "心狠手辣,过度揽权",
                "结局": "机关算尽,反误了卿卿性命",
                "启示": "能力与道德需要平衡"
            },
            "探春改革": {
                "背景": "大观园经济困境",
                "举措": "承包责任制,节流开源",
                "阻力": "既得利益者反对",
                "结局": "改革半途而废",
                "启示": "改革需要一把手的支持"
            },
            "晴雯之死": {
                "原因": "王夫人诬陷--能力太强遭人嫉妒",
                "背景": "木秀于林,风必摧之",
                "启示": "职场中锋芒太露的危险"
            }
        },

        # 人物性格与命运
        "character_destiny": {
            "贾宝玉": {
                "性格": "不愿走仕途经济的叛逆者",
                "能力": "诗词歌赋,审美情趣",
                "命运": "出家--与世俗彻底决裂"
            },
            "林黛玉": {
                "性格": "清高孤傲,不屑世俗",
                "能力": "诗才冠绝,情感细腻",
                "命运": "为爱而死--诗意的悲剧"
            },
            "薛宝钗": {
                "性格": "温柔敦厚,成熟稳重",
                "能力": "情商极高,人际圆融",
                "命运": "独守空房--世俗成功的空洞"
            },
            "王熙凤": {
                "性格": "精明强干,心狠手辣",
                "能力": "管理才能,权谋手段",
                "命运": "病逝--成也权力,败也权力"
            },
            "刘姥姥": {
                "性格": "朴实善良,知恩图报",
                "能力": "人情练达,智慧通达",
                "命运": "救出巧姐--善有善报"
            }
        },

        # 家族企业警示
        "enterprise_warnings": [
            "经济管理混乱--贾府入不敷出",
            "人才青黄不接--贾敬出家,贾珍荒淫",
            "接班人问题--宝玉不愿走仕途",
            "内斗消耗--王夫人与邢夫人争权",
            "过于依赖外部资源--元春的庇护不可持续",
            "创新不足--守着祖业不思进取"
        ],

        # 人生哲理
        "life_philosophy": {
            "繁华与虚无": "赤条条来去无牵挂--一切皆空",
            "真与假": "假作真时真亦假--世事如梦",
            "情与理": "情之所钟,正在我辈--为情而生",
            "得与失": "机关算尽太聪明--算来算去一场空",
            "生与死": "纵有千年铁门槛,终须一个土馒头--生死无常"
        },

        # 情感洞察
        "emotional_insights": {
            "宝黛爱情": "青梅竹马,两情相悦却无法在一起",
            "晴雯之死": "美好事物的毁灭最令人心痛",
            "探春远嫁": "有才能的人往往被迫离开",
            "惜春出家": "看透红尘的觉醒",
            "凤姐之死": "权势褪去后的凄凉"
        },

        # 管理智慧
        "management_wisdom": [
            "王熙凤的管理才能--雷厉风行,责任到人",
            "探春的改革尝试--开源节流,承包到户",
            "贾母的权威维护--平衡各方势力",
            "平儿的善良周全--在夹缝中生存的智慧",
            "鸳鸯的刚烈不屈--宁折不弯的骨气"
        ]
    }

def get_recommend_honglou_case(matched_themes: List[str]) -> Dict[str, Any]:
    """根据匹配主题推荐红楼案例"""
    wisdom = get_honglou_wisdom()
    case_map = {
        "组织": "王熙凤协理宁国府",
        "人物": "探春改革",
        "兴衰": "家族兴衰周期",
        "人际关系": "核心三角",
        "组织管理": "王熙凤协理宁国府"
    }

    case_name = case_map.get(matched_themes[0] if matched_themes else "组织", "王熙凤协理宁国府")

    # 尝试从不同来源获取案例
    if case_name in wisdom["organizational_politics"]:
        detail = wisdom["organizational_politics"][case_name]
    elif case_name in wisdom["relationships"]:
        detail = wisdom["relationships"][case_name]
    elif case_name in wisdom["family_cycle"]:
        detail = wisdom["family_cycle"][case_name]
    else:
        detail = wisdom["organizational_politics"]["王熙凤协理宁国府"]

    return {"case_name": case_name, "case_detail": detail}

def summarize_honglou_wisdom(matched_themes: List[str]) -> str:
    """总结红楼智慧"""
    wisdom = get_honglou_wisdom()
    return (
        f"红楼智慧揭示组织兴衰规律：{', '.join(wisdom['enterprise_warnings'][:3])}。"
        f"人生哲理：{wisdom['life_philosophy']['得与失']}，"
        f"管理警示：{wisdom['management_wisdom'][0]}。"
    )

def generate_honglou_actions(matched_themes: List[str]) -> List[str]:
    """生成红楼视角的行动建议"""
    actions = [
        "建立危机意识，防患于未然",
        "重视人才培养和梯队建设",
        "平衡效率与公平，避免过度内斗",
        "培养健康的组织文化",
        "核心领导要德才兼备"
    ]

    if "组织" in matched_themes:
        actions.insert(0, "完善内部管理制度，明确权责")
    if "兴衰" in matched_themes:
        actions.insert(0, "关注关键成功因素和潜在风险")

    return actions[:5]

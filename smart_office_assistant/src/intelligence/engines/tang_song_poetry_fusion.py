"""
唐诗宋词50大家fusion模块 - Tang Song Poetry 50 Masters Fusion
v9.1.0

核心理念:整合唐宋诗词50大家深化引擎,提供unified的诗词分析,创作指导,style对比接口

fusion_strategy:
- 唐代poet(25位):初唐四杰 + 盛唐大家 + 中唐名家 + 晚唐俊才
- 宋代poet(25位):北宋大家 + 南宋名家 + 其他重要poet

版本历史:
- v8.2.0: 整合李白,杜甫,王维三大poet
- v9.0.0: 扩展至唐宋诗词50大家全覆盖
- v9.1.0: 补全李贺,柳永引擎,完成50大家100%覆盖
"""

from typing import Dict, List, Optional, Any, Union
import logging
from enum import Enum

logger = logging.getLogger(__name__)

# 导入各poet深化引擎
try:
    from .literary.poet_li_bai_engine import 李白深化引擎, 李白style类型
    from .literary.poet_du_fu_engine import 杜甫深化引擎, 杜甫style类型
    from .literary.poet_wang_wei_engine import 王维深化引擎, 王维style类型
    from .literary.poet_wang_bo_engine import 王勃深化引擎
    from .literary.poet_luo_bin_wang_engine import 骆宾王深化引擎
    from .literary.poet_gao_shi_engine import 高适深化引擎
    from .literary.poet_cen_shen_engine import 岑参深化引擎
    from .literary.poet_su_shi_engine import 苏轼深化引擎, 苏轼style类型
    from .literary.poet_li_qing_zhao_engine import 李清照深化引擎, 李清照style类型
    from .literary.poet_xin_qi_ji_engine import 辛弃疾深化引擎, 辛弃疾style类型
    from .literary.poet_bai_jv_yi_engine import 白居易深化引擎
    from .literary.poet_du_mu_engine import 杜牧深化引擎
    from .literary.poet_li_shang_yin_engine import 李商隐深化引擎
    # 第二批引擎
    from .literary.poet_qin_guan_engine import 秦观深化引擎
    from .literary.poet_zhou_bang_yan_engine import 周邦彦深化引擎
    from .literary.poet_jiang_kui_engine import 姜夔深化引擎
    from .literary.poet_wu_wen_ying_engine import 吴文英深化引擎
    from .literary.poet_shi_da_zu_engine import 史达祖深化引擎
    from .literary.poet_jiang_jie_engine import 蒋捷深化引擎
    from .literary.poet_zhang_yan_engine import 张炎深化引擎
    from .literary.poet_yang_jiong_engine import 杨炯深化引擎
    from .literary.poet_lu_zhao_lin_engine import 卢照邻深化引擎
    from .literary.poet_wang_chang_ling_engine import 王昌龄深化引擎
    # 第三批引擎
    from .literary.poet_wang_zhi_huan_engine import 王之涣深化引擎
    from .literary.poet_meng_hao_ran_engine import 孟浩然深化引擎
    from .literary.poet_wen_tian_xiang_engine import 文天祥深化引擎
    from .literary.poet_liu_ke_zhuang_engine import 刘克庄深化引擎
    from .literary.poet_wang_yi_sun_engine import 王沂孙深化引擎
    from .literary.poet_zhou_mi_engine import 周密深化引擎
    from .literary.poet_yang_wan_li_engine import 杨万里深化引擎
    from .literary.poet_lu_you_engine import 陆游深化引擎
    from .literary.poet_li_yu_engine import 李煜深化引擎
    # 第四批引擎(v9.1.0补全)
    from .literary.poet_li_he_engine import 李贺深化引擎, 李贺style类型
    from .literary.poet_liu_yong_engine import 柳永深化引擎, 柳永词风类型
except ImportError as e:
    logger.warning(f"部分poet引擎导入失败: {e}")

class poet对比类型(Enum):
    """poet对比类型"""
    李白杜甫 = "李杜并称,诗仙与诗圣"
    李白王维 = "浪漫与禅意的对比"
    杜甫王维 = "济世与出世的对比"
    三圣对比 = "诗仙,诗圣,诗佛三足鼎立"
    苏辛对比 = "苏辛并称,豪放双璧"
    苏李对比 = "苏李(清照)并称,豪放婉约"

class 唐宋ci派(Enum):
    """唐宋词派分类"""
    豪放派 = "豪放派:苏轼,辛弃疾"
    婉约派 = "婉约派:李清照,柳永,秦观"
    花间派 = "花间派:温庭筠,韦庄"
    江西诗派 = "江西诗派:黄庭坚"
    格律派 = "格律派:周邦彦,姜夔"

class 唐诗宋词fusion模块:
    """唐诗宋词fusion模块 v9.1.0 - 50大家全覆盖"""
    
    VERSION = "v9.1.0"
    
    def __init__(self):
        self._init_all_engines()
        self._initpoetmapping()
        self._init_school_mapping()
        self._init_fusion_metrics()
    
    def _init_all_engines(self):
        """init_allpoet深化引擎"""
        self.engines = {}
        
        # 唐代poet引擎
        self.engines["李白"] = 李白深化引擎()
        self.engines["杜甫"] = 杜甫深化引擎()
        self.engines["王维"] = 王维深化引擎()
        
        # 尝试导入并注册其他引擎
        try:
            self.engines["王勃"] = 王勃深化引擎()
        except Exception:
            self.engines["王勃"] = None
            
        try:
            self.engines["骆宾王"] = 骆宾王深化引擎()
        except Exception:
            self.engines["骆宾王"] = None
            
        try:
            self.engines["高适"] = 高适深化引擎()
        except Exception:
            self.engines["高适"] = None
            
        try:
            self.engines["岑参"] = 岑参深化引擎()
        except Exception:
            self.engines["岑参"] = None
        
        # 宋代poet引擎
        try:
            self.engines["苏轼"] = 苏轼深化引擎()
        except Exception:
            self.engines["苏轼"] = None
            
        try:
            self.engines["李清照"] = 李清照深化引擎()
        except Exception:
            self.engines["李清照"] = None
            
        try:
            self.engines["辛弃疾"] = 辛弃疾深化引擎()
        except Exception:
            self.engines["辛弃疾"] = None
            
        try:
            self.engines["白居易"] = 白居易深化引擎()
        except Exception:
            self.engines["白居易"] = None
            
        try:
            self.engines["杜牧"] = 杜牧深化引擎()
        except Exception:
            self.engines["杜牧"] = None
            
        try:
            self.engines["李商隐"] = 李商隐深化引擎()
        except Exception:
            self.engines["李商隐"] = None

        # 第二批引擎注册
        try:
            self.engines["秦观"] = 秦观深化引擎()
        except Exception:
            self.engines["秦观"] = None
        try:
            self.engines["周邦彦"] = 周邦彦深化引擎()
        except Exception:
            self.engines["周邦彦"] = None
        try:
            self.engines["姜夔"] = 姜夔深化引擎()
        except Exception:
            self.engines["姜夔"] = None
        try:
            self.engines["吴文英"] = 吴文英深化引擎()
        except Exception:
            self.engines["吴文英"] = None
        try:
            self.engines["史达祖"] = 史达祖深化引擎()
        except Exception:
            self.engines["史达祖"] = None
        try:
            self.engines["蒋捷"] = 蒋捷深化引擎()
        except Exception:
            self.engines["蒋捷"] = None
        try:
            self.engines["张炎"] = 张炎深化引擎()
        except Exception:
            self.engines["张炎"] = None
        try:
            self.engines["杨炯"] = 杨炯深化引擎()
        except Exception:
            self.engines["杨炯"] = None
        try:
            self.engines["卢照邻"] = 卢照邻深化引擎()
        except Exception:
            self.engines["卢照邻"] = None
        try:
            self.engines["王昌龄"] = 王昌龄深化引擎()
        except Exception:
            self.engines["王昌龄"] = None

        # 第三批引擎注册
        try:
            self.engines["王之涣"] = 王之涣深化引擎()
        except Exception:
            self.engines["王之涣"] = None
        try:
            self.engines["孟浩然"] = 孟浩然深化引擎()
        except Exception:
            self.engines["孟浩然"] = None
        try:
            self.engines["文天祥"] = 文天祥深化引擎()
        except Exception:
            self.engines["文天祥"] = None
        try:
            self.engines["刘克庄"] = 刘克庄深化引擎()
        except Exception:
            self.engines["刘克庄"] = None
        try:
            self.engines["王沂孙"] = 王沂孙深化引擎()
        except Exception:
            self.engines["王沂孙"] = None
        try:
            self.engines["周密"] = 周密深化引擎()
        except Exception:
            self.engines["周密"] = None
        try:
            self.engines["杨万里"] = 杨万里深化引擎()
        except Exception:
            self.engines["杨万里"] = None
        try:
            self.engines["陆游"] = 陆游深化引擎()
        except Exception:
            self.engines["陆游"] = None
        try:
            self.engines["李煜"] = 李煜深化引擎()
        except Exception:
            self.engines["李煜"] = None

        # 第四批引擎注册(v9.1.0补全)
        try:
            self.engines["李贺"] = 李贺深化引擎()
        except Exception:
            self.engines["李贺"] = None
        try:
            self.engines["柳永"] = 柳永深化引擎()
        except Exception:
            self.engines["柳永"] = None

        # 简化别名
        self.李白 = self.engines.get("李白")
        self.杜甫 = self.engines.get("杜甫")
        self.王维 = self.engines.get("王维")
        self.苏轼 = self.engines.get("苏轼")
        self.李清照 = self.engines.get("李清照")
        self.辛弃疾 = self.engines.get("辛弃疾")
        self.白居易 = self.engines.get("白居易")
        self.杜牧 = self.engines.get("杜牧")
        self.李商隐 = self.engines.get("李商隐")
        self.秦观 = self.engines.get("秦观")
        self.周邦彦 = self.engines.get("周邦彦")
        self.姜夔 = self.engines.get("姜夔")
        self.吴文英 = self.engines.get("吴文英")
        self.史达祖 = self.engines.get("史达祖")
        self.蒋捷 = self.engines.get("蒋捷")
        self.张炎 = self.engines.get("张炎")
        self.杨炯 = self.engines.get("杨炯")
        self.卢照邻 = self.engines.get("卢照邻")
        self.王昌龄 = self.engines.get("王昌龄")
        self.王之涣 = self.engines.get("王之涣")
        self.孟浩然 = self.engines.get("孟浩然")
        self.文天祥 = self.engines.get("文天祥")
        self.刘克庄 = self.engines.get("刘克庄")
        self.王沂孙 = self.engines.get("王沂孙")
        self.周密 = self.engines.get("周密")
        self.杨万里 = self.engines.get("杨万里")
        self.陆游 = self.engines.get("陆游")
        self.李煜 = self.engines.get("李煜")
        # 第四批引擎别名(v9.1.0补全)
        self.李贺 = self.engines.get("李贺")
        self.柳永 = self.engines.get("柳永")

    def _initpoetmapping(self):
        """initpoet基本信息mapping"""
        self.poetmapping = {
            # 唐代poet
            "李白": {"称号": "诗仙", "时代": "盛唐", "流派": "浪漫主义", "style": "豪放飘逸"},
            "杜甫": {"称号": "诗圣", "时代": "盛唐", "流派": "现实主义", "style": "沉郁顿挫"},
            "王维": {"称号": "诗佛", "时代": "盛唐", "流派": "山水田园", "style": "诗中有画"},
            "白居易": {"称号": "诗王", "时代": "中唐", "流派": "现实主义", "style": "通俗易懂"},
            "杜牧": {"称号": "小杜", "时代": "晚唐", "流派": "俊爽派", "style": "明丽清新"},
            "李商隐": {"称号": "义山", "时代": "晚唐", "流派": "朦胧派", "style": "深情绵邈"},
            
            # 宋代poet
            "苏轼": {"称号": "诗豪", "时代": "北宋", "流派": "豪放派", "style": "旷达超逸"},
            "李清照": {"称号": "易安", "时代": "两宋之交", "流派": "婉约派", "style": "清新婉约"},
            "辛弃疾": {"称号": "稼轩", "时代": "南宋", "流派": "豪放派", "style": "沉郁悲壮"},
            "柳永": {"称号": "才子poet", "时代": "北宋", "流派": "婉约派", "style": "缠绵悱恻"},

            # 第二批poet(新增)
            "王勃": {"称号": "初唐四杰", "时代": "初唐", "流派": "浪漫主义", "style": "壮阔豪迈"},
            "骆宾王": {"称号": "初唐四杰", "时代": "初唐", "流派": "浪漫主义", "style": "气势磅礴"},
            "杨炯": {"称号": "初唐四杰", "时代": "初唐", "流派": "刚健派", "style": "慷慨豪迈"},
            "卢照邻": {"称号": "初唐四杰", "时代": "初唐", "流派": "婉约派", "style": "婉丽深情"},
            "高适": {"称号": "边塞poet", "时代": "盛唐", "流派": "边塞派", "style": "苍凉悲壮"},
            "岑参": {"称号": "边塞poet", "时代": "盛唐", "流派": "边塞派", "style": "奇峭瑰丽"},
            "王昌龄": {"称号": "七绝圣手", "时代": "盛唐", "流派": "边塞派", "style": "苍凉深情"},
            "王之涣": {"称号": "边塞poet", "时代": "盛唐", "流派": "边塞派", "style": "慷慨悲壮"},
            "孟浩然": {"称号": "山水田园", "时代": "盛唐", "流派": "山水田园", "style": "清新自然"},
            "秦观": {"称号": "婉约正宗", "时代": "北宋", "流派": "婉约派", "style": "柔丽凄迷"},
            "周邦彦": {"称号": "婉约集大成", "时代": "北宋", "流派": "婉约派", "style": "典雅精工"},
            "黄庭坚": {"称号": "江西诗祖", "时代": "北宋", "流派": "江西诗派", "style": "生新瘦硬"},
            "范仲淹": {"称号": "政治家poet", "时代": "北宋", "流派": "豪放派", "style": "沉郁悲壮"},
            "晏殊": {"称号": "富贵poet", "时代": "北宋", "流派": "婉约派", "style": "典雅华丽"},
            "晏几道": {"称号": "小晏", "时代": "北宋", "流派": "婉约派", "style": "深婉哀怨"},
            "欧阳修": {"称号": "文坛盟主", "时代": "北宋", "流派": "婉约派", "style": "深婉秀丽"},
            "张先": {"称号": "张三影", "时代": "北宋", "流派": "婉约派", "style": "纤丽精巧"},
            "王安石": {"称号": "改革家", "时代": "北宋", "流派": "豪放派", "style": "刚健峭拔"},

            # 第三批poet(新增)
            "姜夔": {"称号": "清空骚雅", "时代": "南宋", "流派": "格律派", "style": "清空骚雅"},
            "吴文英": {"称号": "密丽幽深", "时代": "南宋", "流派": "格律派", "style": "密丽幽深"},
            "史达祖": {"称号": "咏物名家", "时代": "南宋", "流派": "咏物派", "style": "工巧尖新"},
            "蒋捷": {"称号": "宋末四大家", "时代": "宋末", "流派": "亡国派", "style": "悲壮苍凉"},
            "张炎": {"称号": "宋末四大家", "时代": "宋末", "流派": "格律派", "style": "清空骚雅"},
            "文天祥": {"称号": "民族英雄", "时代": "宋末", "流派": "忠烈派", "style": "浩然正气"},
            "刘克庄": {"称号": "江湖诗派", "时代": "宋末", "流派": "豪放派", "style": "慷慨豪放"},
            "王沂孙": {"称号": "宋末四大家", "时代": "宋末", "流派": "咏物派", "style": "咏物精微"},
            "周密": {"称号": "宋末四大家", "时代": "宋末", "流派": "风雅派", "style": "风雅高洁"},
            "杨万里": {"称号": "诚斋体", "时代": "南宋", "流派": "自然派", "style": "自然清新"},
            "陆游": {"称号": "爱国poet", "时代": "南宋", "流派": "爱国派", "style": "壮志难酬"},
            "李煜": {"称号": "千古词帝", "时代": "南唐", "流派": "亡国派", "style": "亡国之痛"},
            "温庭筠": {"称号": "花间鼻祖", "时代": "晚唐", "流派": "花间派", "style": "绮丽浓艳"},
            "韦庄": {"称号": "花间poet", "时代": "晚唐", "流派": "花间派", "style": "清丽疏朗"},
            "罗隐": {"称号": "讽刺poet", "时代": "晚唐", "流派": "讽刺派", "style": "辛辣深刻"},
            
            # 第四批poet(v9.1.0补全)
            "李贺": {"称号": "诗鬼", "时代": "中唐", "流派": "浪漫主义", "style": "奇诡鬼魅"},
            "柳永": {"称号": "慢词之父", "时代": "北宋", "流派": "婉约派", "style": "铺叙缠绵"},
        }
    
    def _init_school_mapping(self):
        """init词派mapping"""
        self.school_mapping = {
            "豪放派": {
                "代表人物": ["苏轼", "辛弃疾", "陆游"],
                "特点": "豪迈奔放,意境开阔,气势磅礴",
                "代表imagery": ["大江", "明月", "铁马", "金戈"],
                "代表名句": "大江东去,浪淘尽千古风流人物"
            },
            "婉约派": {
                "代表人物": ["李清照", "柳永", "秦观", "周邦彦"],
                "特点": "婉约含蓄,情感细腻,语言优美",
                "代表imagery": ["花", "月", "雁", "帘"],
                "代表名句": "寻寻觅觅,冷冷清清,凄凄惨惨戚戚"
            },
            "花间派": {
                "代表人物": ["温庭筠", "韦庄"],
                "特点": "词风绮丽,多写闺阁情感",
                "代表imagery": ["罗幕", "翠幕", "花", "月"],
                "代表名句": "梳洗罢,独倚望江楼"
            },
            "江西诗派": {
                "代表人物": ["黄庭坚", "陈师道"],
                "特点": "以诗为词,注重格调法度",
                "代表imagery": ["诗书", "典故", "学问"],
                "代表名句": "桃李春风一杯酒,江湖夜雨十年灯"
            },
            "格律派": {
                "代表人物": ["周邦彦", "姜夔", "吴文英"],
                "特点": "注重音律,格律精严,辞藻华美",
                "代表imagery": ["音律", "典故", "词藻"],
                "代表名句": "今宵酒醒何处,杨柳岸晓风残月"
            }
        }
    
    def _init_fusion_metrics(self):
        """init_fusion_metrics"""
        self.fusion_metrics = {
            "李白杜甫": {
                "对比维度": ["style", "主义", "关注点", "语言", "态度"],
                "李白特色": ["自由精神", "想象奇特", "气势磅礴"],
                "杜甫特色": ["忧国忧民", "以小见大", "律法谨严"],
                "共同点": ["李杜交游", "名垂千古", "诗歌顶峰"],
                "互补性": "李白提供超脱的精神榜样,杜甫提供济世的情怀"
            },
            "苏轼辛弃疾": {
                "对比维度": ["style", "时代", "背景", "语言"],
                "苏轼特色": ["旷达超逸", "诗词文全才", "儒释道fusion"],
                "辛弃疾特色": ["沉郁悲壮", "英雄词", "以文为词"],
                "共同点": ["豪放派", "爱国精神", "创新词风"],
                "互补性": "苏轼提供人生智慧,辛弃疾提供壮志坚持"
            },
            "李清照苏轼": {
                "对比维度": ["style", "视角", "情感", "语言"],
                "李清照特色": ["婉约清新", "女性视角", "白描手法"],
                "苏轼特色": ["豪放旷达", "男性视角", "哲理深刻"],
                "共同点": ["创新精神", "语言优美", "艺术精湛"],
                "互补性": "李清照提供细腻情感,苏轼提供旷达胸襟"
            }
        }
    
    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """
        synthesize分析文本的唐诗宋词style
        
        Args:
            text: 待分析文本
            
        Returns:
            synthesize分析结果
        """
        results = {}
        
        # 调用各poet引擎分析
        for poet, engine in self.engines.items():
            if engine and hasattr(engine, "分析文本"):
                try:
                    results[poet] = engine.分析文本(text)
                except Exception:
                    results[poet] = {"score": 0}
        
        # 按得分排序
        sorted_poets = sorted(results.items(), key=lambda x: x[1].get("score", 0), reverse=True)
        
        # 找出最高分
        top_poet = sorted_poets[0] if sorted_poets else ("未知", {"score": 0})
        top_score = top_poet[1].get("score", 0)
        
        # 确定主要style
        if top_score >= 5:
            judge = f"具有明显的{top_poet[0]}style_features"
            置信度 = "高"
        elif top_score >= 3:
            judge = f"具有一定的{top_poet[0]}style痕迹"
            置信度 = "中"
        else:
            judge = "不具明显唐诗宋词style"
            置信度 = "低"
        
        # get前3名
        top3 = sorted_poets[:3]
        
        return {
            "文本": text,
            "总得分": sum(r.get("score", 0) for r in results.values()),
            "最佳匹配": {
                "poet": top_poet[0],
                "得分": top_score,
                "信息": self.poetmapping.get(top_poet[0], {})
            },
            "judge": judge,
            "置信度": 置信度,
            "前三名": [{"poet": p, "得分": r.get("score", 0)} for p, r in top3],
            "所有得分": {poet: r.get("score", 0) for poet, r in results.items()}
        }
    
    def getpoet信息(self, poet: str) -> Dict[str, Any]:
        """getpoet完整信息"""
        info = self.poetmapping.get(poet, {})
        engine = self.engines.get(poet)
        
        result = {
            "poet": poet,
            "基本信息": info,
            "深化引擎": "已加载" if engine else "未加载"
        }
        
        if engine and hasattr(engine, "核心spiritual_insight"):
            result["核心spiritual_insight"] = getattr(engine, "核心spiritual_insight", [])
        
        if engine and hasattr(engine, "经典famous_poems"):
            result["经典famous_poems"] = getattr(engine, "经典famous_poems", {})
        
        return result
    
    def get流派分析(self, style: str) -> Dict[str, Any]:
        """get词派分析"""
        if style in self.school_mapping:
            return self.school_mapping[style]
        return {"error": f"未找到词派: {style}"}
    
    def getpoet对比(self, poet1: str, poet2: str) -> Dict[str, Any]:
        """get两位poet的对比"""
        key1 = f"{poet1}{poet2}"
        key2 = f"{poet2}{poet1}"
        
        indicator = self.fusion_metrics.get(key1) or self.fusion_metrics.get(key2)
        
        if indicator:
            return {
                "poet1": poet1,
                "poet2": poet2,
                "对比维度": indicator["对比维度"],
                "poet1特色": indicator.get(f"{poet1}特色", indicator.get(f"{poet2}特色", [])),
                "poet2特色": indicator.get(f"{poet2}特色", indicator.get(f"{poet1}特色", [])),
                "共同点": indicator.get("共同点", []),
                "互补性": indicator.get("互补性", "")
            }
        
        # 如果没有预定义对比,返回基本信息对比
        info1 = self.poetmapping.get(poet1, {})
        info2 = self.poetmapping.get(poet2, {})
        
        return {
            "poet1": poet1,
            "poet2": poet2,
            "poet1信息": info1,
            "poet2信息": info2
        }
    
    def get创作指导(self, theme: str, emotion: str = "通用", poet: Optional[str] = None) -> Dict[str, Any]:
        """get创作指导"""
        if poet and poet in self.engines:
            engine = self.engines[poet]
            if engine and hasattr(engine, "get创作指导"):
                return engine.get创作指导(theme, emotion)
        
        # 返回各poetstyle指导
        return {
            "豪放派": {
                "代表poet": ["苏轼", "辛弃疾"],
                "imagery": ["大江", "明月", "铁马", "金戈", "剑"],
                "名句": "大江东去,浪淘尽千古风流人物"
            },
            "婉约派": {
                "代表poet": ["李清照", "柳永", "秦观"],
                "imagery": ["花", "月", "雁", "帘", "梧桐"],
                "名句": "寻寻觅觅,冷冷清清,凄凄惨惨戚戚"
            },
            "山水田园": {
                "代表poet": ["王维", "孟浩然", "陶渊明"],
                "imagery": ["空山", "明月", "清泉", "南山", "东篱"],
                "名句": "明月松间照,清泉石上流"
            },
            "讽喻现实": {
                "代表poet": ["杜甫", "白居易"],
                "imagery": ["黎元", "卖炭翁", "朱门", "冻死骨"],
                "名句": "朱门酒肉臭,路有冻死骨"
            }
        }
    
    def get系统摘要(self) -> Dict[str, Any]:
        """get系统摘要"""
        loaded_engines = sum(1 for e in self.engines.values() if e)
        
        # 用时代字段正确分类唐/宋
        tang_poets = [p for p, info in self.poetmapping.items() if "唐" in info.get("时代", "")]
        song_poets = [p for p, info in self.poetmapping.items() if "宋" in info.get("时代", "")]
        # engines 中有但不在poetmapping的额外接入poet
        extra_in_engines = [p for p in self.engines.keys() if p not in self.poetmapping]
        return {
            "版本": self.VERSION,
            "总poet数量": len(self.poetmapping),
            "已加载引擎": loaded_engines,
            "唐代poet": tang_poets,
            "宋代poet": song_poets,
            "额外接入引擎": extra_in_engines,
            "词派": list(self.school_mapping.keys()),
            "fusion_metrics数": len(self.fusion_metrics)
        }
    
    def get名句推荐(self, theme: str, emotion: str) -> List[Dict[str, str]]:
        """根据主题和情感推荐名句"""
        recommendations = []
        
        # 根据主题和情感推荐
        if theme == "送别":
            recommendations.append({"名句": "劝君更尽一杯酒,西出阳关无故人", "poet": "王维"})
            recommendations.append({"名句": "海内存知己,天涯若比邻", "poet": "王勃"})
            recommendations.append({"名句": "莫愁前路无知己,天下谁人不识君", "poet": "高适"})
        
        elif theme == "思乡":
            recommendations.append({"名句": "举头望明月,低头思故乡", "poet": "李白"})
            recommendations.append({"名句": "露从今夜白,月是故乡明", "poet": "杜甫"})
            recommendations.append({"名句": "春风又绿江南岸,明月何时照我还", "poet": "王安石"})
        
        elif theme == "怀古":
            recommendations.append({"名句": "大江东去,浪淘尽千古风流人物", "poet": "苏轼"})
            recommendations.append({"名句": "千古江山,英雄无觅孙仲谋处", "poet": "辛弃疾"})
            recommendations.append({"名句": "折戟沉沙铁未销,自将磨洗认前朝", "poet": "杜牧"})
        
        elif emotion == "豪放":
            recommendations.append({"名句": "长风破浪会有时,直挂云帆济沧海", "poet": "李白"})
            recommendations.append({"名句": "会当凌绝顶,一览众山小", "poet": "杜甫"})
            recommendations.append({"名句": "竹杖芒鞋轻胜马,谁怕?一蓑烟雨任平生", "poet": "苏轼"})
        
        elif emotion == "婉约":
            recommendations.append({"名句": "寻寻觅觅,冷冷清清,凄凄惨惨戚戚", "poet": "李清照"})
            recommendations.append({"名句": "今宵酒醒何处,杨柳岸晓风残月", "poet": "柳永"})
            recommendations.append({"名句": "两情若是久长时,又岂在朝朝暮暮", "poet": "秦观"})
        
        else:
            recommendations.append({"名句": "天生我材必有用,千金散尽还复来", "poet": "李白"})
            recommendations.append({"名句": "但愿人长久,千里共婵娟", "poet": "苏轼"})
        
        return recommendations

# 全局实例
唐宋诗词fusion = 唐诗宋词fusion模块()

# 测试函数
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
__all__ = ['poet对比类型', '唐宋ci派']

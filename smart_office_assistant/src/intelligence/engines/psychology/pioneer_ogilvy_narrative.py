"""
__all__ = [
    'build_brand_story',
    'create_headline',
    'design_brand_image',
    'generate_big_idea',
    'get_creative_strategy',
]

心理学先驱深化引擎 - 奥格威品牌叙事引擎
Pioneer Ogilvy - Brand Narrative Engine
=========================================
版本: v8.2.0
创建时间: 2026-04-03

大卫·奥格威核心思想:
1. 品牌形象论 - 品牌是产品的人格化
2. Big Idea - 大创意改变世界
3. 销售力 - 广告的根本目的
4. 标题重要性 - 80%的时间花在标题上
5. 案例研究 - 哈撒韦衬衫/劳斯莱斯/多芬
6. 创意原则 - 专业,独特,令人难忘

核心功能:
1. 品牌形象设计
2. Big Ideagenerate
3. 标题创作
4. 品牌故事构建
5. 创意strategy制定
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

class 品牌类型(Enum):
    """品牌类型"""
    高端奢华 = "高端奢华"
    实用功能 = "实用功能"
    情感连接 = "情感连接"
    创新科技 = "创新科技"
    社会责任 = "社会责任"

class 创意方向(Enum):
    """创意方向"""
    理性诉求 = "理性诉求"
    感性诉求 = "感性诉求"
    幽默诉求 = "幽默诉求"
    恐惧诉求 = "恐惧诉求"
    社会认同 = "社会认同"
    个性彰显 = "个性彰显"

class 奥格威品牌叙事引擎:
    """
    奥格威品牌叙事引擎
    
    核心功能:
    1. 品牌形象设计 - 构建品牌人格
    2. Big Ideagenerate - 提炼核心创意
    3. 标题创作 - 写出有销售力的标题
    4. 品牌故事构建 - 构建品牌叙事
    5. 创意strategy制定 - 制定创意方向
    """
    
    def __init__(self):
        self.name = "奥格威品牌叙事引擎"
        self.version = "8.2.0"
        
        # 品牌形象要素
        self.品牌形象要素 = {
            "纯真者": {"characteristics": "善良,简单,信任", "视觉": "明亮,柔和", "语言": "温暖,真诚"},
            "英雄": {"characteristics": "勇敢,强大,成就", "视觉": "力量,对比", "语言": "激励,action"},
            "智者": {"characteristics": "智慧,知识,权威", "视觉": "沉稳,专业", "语言": "理性,说服"},
            "探险家": {"characteristics": "自由,探索,冒险", "视觉": "广阔,自然", "语言": "激发,开放"},
            "情人": {"characteristics": "亲密,感性,美", "视觉": "柔美,浪漫", "语言": "情感,吸引"},
            "照顾者": {"characteristics": "关怀,温暖,付出", "视觉": "温馨,柔和", "语言": "关心,承诺"},
            "娱乐者": {"characteristics": "快乐,有趣,轻松", "视觉": "色彩,活力", "语言": "幽默,机智"},
            "发明家": {"characteristics": "创新,独特,创造", "视觉": "现代,未来", "语言": "突破,引领"}
        }
        
        # 奥格威经典案例
        self.经典案例 = {
            "劳斯莱斯": {
                "标题": "在时速60英里时,这辆劳斯莱斯车内最大的噪音来自电子钟",
                "strategy": "用具体细节证明品质",
                "核心": "品质无言,用事实说话"
            },
            "哈撒韦衬衫": {
                "标题": "穿哈撒韦的男人",
                "strategy": "用人物形象赋予产品灵魂",
                "核心": "产品人格化"
            },
            "多芬": {
                "标题": "多芬让您的肌肤如花绽放",
                "strategy": "情感连接,美丽承诺",
                "核心": "情感价值"
            },
            "波斯人咖啡": {
                "标题": "香浓滴滴,每杯皆用心",
                "strategy": "细节描绘,真实感",
                "核心": "感官体验"
            }
        }
        
        # 标题模板
        self.标题模板 = {
            "新闻式": ["独家揭秘:{主题}", "重大发现:{主题}", "刚刚发布:{主题}"],
            "疑问式": ["如何{主题}?", "为什么{主题}?", "{主题}的秘诀是什么?"],
            "命令式": ["立即{action}!", "现在就{action}!", "别再{主题}了!"],
            "数字式": ["{数字}个{主题}的秘密", "{数字}分钟教你{主题}", "只需{数字}步,{主题}"],
            "承诺式": ["{主题}的全新方式", "告别{主题}的方法", "让{主题}变得简单"],
            "见证式": ["为什么{人群}都在{主题}", "看看{人群}怎么说{主题}", "{人群}的{主题}首选"]
        }
        
        # Big Idea要素
        self.Big_Idea要素 = [
            "相关性 - 与目标受众相关",
            "独特性 - 与竞争对手不同",
            "影响力 - 能够引发情感共鸣",
            "持久性 - 能够持续传播",
            "简单性 - 一句话能说清"
        ]
    
    def design_brand_image(self, brand_data: Dict) -> Dict:
        """
        品牌形象设计
        
        Args:
            brand_data: 品牌数据
            
        Returns:
            品牌形象设计方案
        """
        品牌名称 = brand_data.get("name", "")
        品牌定位 = brand_data.get("positioning", "")
        目标受众 = brand_data.get("target", "")
        核心价值 = brand_data.get("core_value", "")
        
        # 确定品牌形象
        品牌形象 = self._determine_brand_image(品牌定位, 核心价值)
        
        # 设计视觉系统
        视觉系统 = self._design_visual_system(品牌形象)
        
        # 设计语言系统
        语言系统 = self._design_language_system(品牌形象)
        
        return {
            "品牌名称": 品牌名称,
            "品牌形象": {
                "类型": 品牌形象,
                "characteristics": self.品牌形象要素.get(品牌形象, {}),
                "定位说明": f"{品牌名称}代表{品牌形象}的价值观"
            },
            "视觉系统": 视觉系统,
            "语言系统": 语言系统,
            "实施建议": self._generate_implementation_suggestions(品牌形象)
        }
    
    def _determine_brand_image(self, positioning: str, value: str) -> str:
        """确定品牌形象"""
        all_text = positioning + value
        
        # 关键词匹配
        匹配表 = {
            "纯真者": ["善良", "简单", "纯净", "自然"],
            "英雄": ["强大", "勇敢", "力量", "成就"],
            "智者": ["智慧", "专业", "权威", "知识"],
            "探险家": ["自由", "探索", "冒险", "个性"],
            "情人": ["浪漫", "感性", "美丽", "亲密"],
            "照顾者": ["温暖", "关怀", "家庭", "责任"],
            "娱乐者": ["快乐", "有趣", "轻松", "活力"],
            "发明家": ["创新", "科技", "独特", "未来"]
        }
        
        得分 = {}
        for 形象, keywords in 匹配表.items():
            得分[形象] = sum(1 for kw in keywords if kw in all_text)
        
        if max(得分.values()) == 0:
            return "英雄"  # 默认
        
        return max(得分, key=得分.get)
    
    def _design_visual_system(self, brand_image: str) -> Dict:
        """设计视觉系统"""
        视觉要素 = self.品牌形象要素.get(brand_image, {})
        
        return {
            "主色调": self._get_color_for_image(brand_image),
            "辅助色调": self._get_secondary_colors(brand_image),
            "视觉imagery": 视觉要素.get("视觉", "现代,简洁"),
            "图标style": self._get_icon_style(brand_image),
            "图片style": self._get_photo_style(brand_image)
        }
    
    def _get_color_for_image(self, image: str) -> str:
        """get主色调"""
        色彩mapping = {
            "纯真者": "#FFD700 金色",
            "英雄": "#FF4444 红色",
            "智者": "#1E3A8A 深蓝色",
            "探险家": "#228B22 森林绿",
            "情人": "#FF69B4 粉红色",
            "照顾者": "#FFA500 橙色",
            "娱乐者": "#FFD700 黄色",
            "发明家": "#4169E1 科技蓝"
        }
        return 色彩mapping.get(image, "#333333 深灰")
    
    def _get_secondary_colors(self, image: str) -> List[str]:
        """get辅助色调"""
        辅助mapping = {
            "纯真者": ["#FFFACD 浅黄", "#FFFFFF 白色"],
            "英雄": ["#000000 黑色", "#808080 灰色"],
            "智者": ["#4169E1 蓝色", "#87CEEB 天蓝"],
            "探险家": ["#D2691E 棕色", "#F5DEB3 沙色"],
            "情人": ["#DC143C 深红", "#FFC0CB 浅粉"],
            "照顾者": ["#FF6347 红橙", "#98FB98 浅绿"],
            "娱乐者": ["#FF4500 橙红", "#00CED1 青色"],
            "发明家": ["#C0C0C0 银色", "#000080 深海军蓝"]
        }
        return 辅助mapping.get(image, ["#666666 中灰", "#999999 浅灰"])
    
    def _get_icon_style(self, image: str) -> str:
        """get图标style"""
        stylemapping = {
            "纯真者": "圆润,无棱角",
            "英雄": "粗犷,有力",
            "智者": "简洁,专业",
            "探险家": "动态,开放",
            "情人": "柔美,流畅",
            "照顾者": "温和,安全",
            "娱乐者": "活泼,趣味",
            "发明家": "几何,现代"
        }
        return stylemapping.get(image, "简洁,现代")
    
    def _get_photo_style(self, image: str) -> str:
        """get图片style"""
        stylemapping = {
            "纯真者": "自然光,柔和",
            "英雄": "强对比,戏剧性",
            "智者": "工作室,专业",
            "探险家": "户外,自然",
            "情人": "柔焦,浪漫",
            "照顾者": "室内,温馨",
            "娱乐者": "动态,彩色",
            "发明家": "极简,未来感"
        }
        return stylemapping.get(image, "专业,现代")
    
    def _design_language_system(self, brand_image: str) -> Dict:
        """设计语言系统"""
        语言要素 = self.品牌形象要素.get(brand_image, {})
        
        return {
            "语气": 语言要素.get("语言", "专业,真诚"),
            "词汇选择": self._get_vocabulary(brand_image),
            "句式style": self._get_sentence_style(brand_image),
            "品牌声音": self._get_brand_voice(brand_image)
        }
    
    def _get_vocabulary(self, image: str) -> List[str]:
        """get词汇选择"""
        词汇表 = {
            "纯真者": ["自然", "纯净", "简单", "真诚", "温暖"],
            "英雄": ["力量", "成就", "突破", "勇敢", "坚毅"],
            "智者": ["专业", "知识", "洞察", "智慧", "权威"],
            "探险家": ["探索", "自由", "发现", "个性", "突破"],
            "情人": ["美丽", "浪漫", "感性", "亲密", "魅力"],
            "照顾者": ["关怀", "温暖", "守护", "责任", "信任"],
            "娱乐者": ["快乐", "有趣", "轻松", "活力", "趣味"],
            "发明家": ["创新", "突破", "科技", "未来", "独特"]
        }
        return 词汇表.get(image, ["专业", "优质"])
    
    def _get_sentence_style(self, image: str) -> str:
        """get句式style"""
        style表 = {
            "纯真者": "简短,温馨",
            "英雄": "有力,号召",
            "智者": "专业,理性",
            "探险家": "开放,启发",
            "情人": "感性,柔美",
            "照顾者": "关怀,承诺",
            "娱乐者": "轻松,幽默",
            "发明家": "简洁,前沿"
        }
        return style表.get(image, "简洁明了")
    
    def _get_brand_voice(self, image: str) -> str:
        """get品牌声音"""
        声音表 = {
            "纯真者": "友善,真诚,温暖",
            "英雄": "坚定,有力,激励",
            "智者": "专业,权威,理性",
            "探险家": "开放,勇敢,探索",
            "情人": "柔美,感性,浪漫",
            "照顾者": "温暖,关怀,负责",
            "娱乐者": "活泼,有趣,轻松",
            "发明家": "前瞻,创新,专业"
        }
        return 声音表.get(image, "专业,真诚")
    
    def _generate_implementation_suggestions(self, brand_image: str) -> List[str]:
        """generate实施建议"""
        return [
            f"确保品牌所有触点都体现{brand_image}形象",
            "视觉和语言系统要保持一致性",
            "培训和授权团队正确使用品牌形象",
            "定期审计品牌形象执行情况"
        ]
    
    def generate_big_idea(self, brand_data: Dict, market_data: Dict) -> Dict:
        """
        Big Ideagenerate
        
        Args:
            brand_data: 品牌数据
            market_data: 市场数据
            
        Returns:
            Big Idea方案
        """
        品牌名称 = brand_data.get("name", "")
        核心承诺 = brand_data.get("core_promise", "")
        差异化 = brand_data.get("differentiation", "")
        目标受众 = brand_data.get("target", "")
        
        # generateBig Idea
        Big_Idea = self._create_big_idea(品牌名称, 核心承诺, 差异化, 目标受众)
        
        # 验证Big Idea
        验证结果 = self._validate_big_idea(Big_Idea, market_data)
        
        # 制定执行strategy
        执行strategy = self._develop_execution_strategy(Big_Idea, brand_data)
        
        return {
            "Big_Idea": Big_Idea,
            "核心概念": self._extract_core_concept(Big_Idea),
            "验证结果": 验证结果,
            "执行strategy": 执行strategy,
            "传播方式": self._suggest_communication_ways(Big_Idea),
            "评估metrics": self._suggest_kpis(Big_Idea)
        }
    
    def _create_big_idea(self, name: str, promise: str, diff: str, target: str) -> str:
        """创建Big Idea"""
        # 简化逻辑 - 实际应用中需要更复杂的分析
        ideas = [
            f"{name}:{promise}",
            f"{name}让{diff}成为可能",
            f"{name},为{target}而生",
            f"{promise}的秘密--{name}"
        ]
        
        # 选择最佳
        return ideas[0]
    
    def _validate_big_idea(self, idea: str, market: Dict) -> Dict:
        """验证Big Idea"""
        validation = []
        
        for element in self.Big_Idea要素:
            # 简化验证
            validation.append({
                "要素": element,
                "符合度": "高" if len(idea) > 10 else "中",
                "说明": f"Big Idea体现了{element.split(' - ')[0]}"
            })
        
        return {
            "验证结果": validation,
            "synthesize评估": "符合Big Idea标准" if all(v["符合度"] != "低" for v in validation) else "需要优化"
        }
    
    def _extract_core_concept(self, idea: str) -> str:
        """提取核心概念"""
        return f"核心概念:{idea}"
    
    def _develop_execution_strategy(self, idea: str, brand: Dict) -> List[str]:
        """制定执行strategy"""
        return [
            "1. 电视广告:30秒核心视觉化",
            "2. 平面广告:主视觉+简洁文案",
            "3. 数字广告:社交媒体短视频",
            "4. 公关活动:故事化传播",
            "5. 线下活动:沉浸式体验"
        ]
    
    def _suggest_communication_ways(self, idea: str) -> List[str]:
        """建议传播方式"""
        return [
            "故事化内容营销",
            "KOL/UGC传播",
            "事件营销",
            "情感共鸣广告",
            "体验式营销"
        ]
    
    def _suggest_kpis(self, idea: str) -> List[str]:
        """建议KPI"""
        return [
            "品牌认知度",
            "品牌联想强度",
            "情感连接度",
            "购买意愿",
            "口碑传播量"
        ]
    
    def create_headline(self, content: Dict, direction: str = "理性诉求") -> List[Dict]:
        """
        标题创作
        
        Args:
            content: 内容数据
            direction: 创意方向
            
        Returns:
            标题方案列表
        """
        主语 = content.get("subject", "{主题}")
        承诺 = content.get("promise", "{主题}")
        受众 = content.get("audience", "{人群}")
        
        标题列表 = []
        
        # generate不同类型标题
        for 类型, 模板列表 in self.标题模板.items():
            for 模板 in 模板列表:
                标题 = 模板.format(主题=主语, 人群=受众, 数字="5", action="action")
                标题列表.append({
                    "标题": 标题,
                    "类型": 类型,
                    "适合渠道": self._get_suitable_channel(类型),
                    "优化建议": self._optimize_headline(标题, direction)
                })
        
        # 排序:最好的放在前面
        return 标题列表[:10]
    
    def _get_suitable_channel(self, headline_type: str) -> str:
        """get适合渠道"""
        渠道mapping = {
            "新闻式": "公关稿,新闻投放",
            "疑问式": "社交媒体,内容营销",
            "命令式": "促销,直销",
            "数字式": "信息图,教程类",
            "承诺式": "品牌广告,产品页",
            "见证式": "口碑,评论"
        }
        return 渠道mapping.get(headline_type, "通用")
    
    def _optimize_headline(self, headline: str, direction: str) -> str:
        """优化标题"""
        # 简化优化逻辑
        if len(headline) > 20:
            return "建议缩短,更易记忆"
        
        if direction == "感性诉求":
            return "建议增加情感词汇"
        
        return "标题结构良好"
    
    def build_brand_story(self, brand_data: Dict) -> Dict:
        """
        品牌故事构建
        
        Args:
            brand_data: 品牌数据
            
        Returns:
            品牌故事方案
        """
        创始故事 = brand_data.get("founder_story", "")
        使命 = brand_data.get("mission", "")
        愿景 = brand_data.get("vision", "")
        价值观 = brand_data.get("values", [])
        
        # 构建故事框架
        故事框架 = self._create_story_framework(创始故事, 使命, 愿景)
        
        # 设计故事弧
        故事弧 = self._design_story_arc(品牌数据)
        
        # generate故事版本
        故事版本 = {
            "完整版": self._write_full_story(故事框架, 故事弧, 品牌数据),
            "精简版": self._write_short_story(故事框架, 品牌_data),
            "社交版": self._write_social_story(故事框架, 品牌_data)
        }
        
        return {
            "故事框架": 故事框架,
            "故事弧": 故事弧,
            "故事版本": 故事版本,
            "故事元素": self._extract_story_elements(品牌_data)
        }
    
    def _create_story_framework(self, founder: str, mission: str, vision: str) -> Dict:
        """创建故事框架"""
        return {
            "起源": founder or "品牌创始初心",
            "使命": mission or "品牌存在的意义",
            "愿景": vision or "品牌追求的未来"
        }
    
    def _design_story_arc(self, brand: Dict) -> Dict:
        """设计故事弧"""
        return {
            "起点": "过去的平凡",
            "触发事件": "发现痛点或机会",
            "发展": "克服挑战的过程",
            "高潮": "重大突破或成就",
            "结局": "新的使命或愿景"
        }
    
    def _write_full_story(self, framework: Dict, arc: Dict, brand: Dict) -> str:
        """撰写完整故事"""
        return f"""
{brand.get('name', '品牌')}的故事:

{arc['起点']}:{framework['起源']}

{arc['触发事件']}:我们发现了一个问题,这个问题一直困扰着{brand.get('target', '我们的用户')}.

{arc['发展']}:我们用{brand.get('core_value', '真心')}和{brand.get('differentiation', '专业')}去解决这个问题.

{arc['高潮']}:经过不懈努力,我们终于找到了答案--{brand.get('name', '品牌')}.

{arc['结局']}:{framework['愿景']}--这就是我们{framework['使命']}的意义.
"""
    
    def _write_short_story(self, framework: Dict, brand: Dict) -> str:
        """撰写精简故事"""
        return f"{brand.get('name', '品牌')}源于{framework['起源']},致力于{framework['使命']},追求{framework['愿景']}."
    
    def _write_social_story(self, framework: Dict, brand: Dict) -> str:
        """撰写社交故事"""
        return f"为什么我们存在?因为{framework['使命']}.我们的目标是{framework['愿景']}.加入我们,一起{framework['起源']}."
    
    def _extract_story_elements(self, brand: Dict) -> Dict:
        """提取故事元素"""
        return {
            "英雄": brand.get('name', '品牌'),
            "反派": brand.get('problem', '行业痛点'),
            "盟友": brand.get('partners', '支持者'),
            "宝藏": brand.get('core_value', '核心价值'),
            "导师": brand.get('founder', '创始人')
        }
    
    def get_creative_strategy(self, brief: Dict) -> Dict:
        """
        创意strategy制定
        
        Args:
            brief: 创意简报
            
        Returns:
            创意strategy方案
        """
        产品 = brief.get("product", "")
        目标 = brief.get("objective", "")
        目标受众 = brief.get("target", "")
        预算 = brief.get("budget", "")
        
        # 确定创意方向
        创意方向 = self._determine_creative_direction(brief)
        
        # 制定strategy框架
        strategy框架 = self._develop_strategy_framework(创意方向, brief)
        
        # 创意简报
        创意简报 = self._create_creative_brief(brief, strategy框架)
        
        return {
            "创意方向": 创意方向.value,
            "strategy框架": strategy框架,
            "创意简报": 创意简报,
            "创意限制": self._identify_constraints(预算, 目标),
            "成功标准": self._define_success_criteria(目标)
        }
    
    def _determine_creative_direction(self, brief: Dict) -> 创意方向:
        """确定创意方向"""
        objective = brief.get("objective", "")
        target = brief.get("target", "")
        
        # 基于目标和受众选择方向
        if "认知" in objective or "知名" in objective:
            return 创意方向.社会认同
        elif "情感" in target or "女性" in target:
            return 创意方向.感性诉求
        elif "转化" in objective or "销售" in objective:
            return 创意方向.理性诉求
        else:
            return 创意方向.个性彰显
    
    def _develop_strategy_framework(self, direction: 创意方向, brief: Dict) -> Dict:
        """制定strategy框架"""
        return {
            "strategy主题": f"围绕{direction.value}的创意表达",
            "核心信息": brief.get("core_message", "产品核心价值"),
            "创意目标": brief.get("objective", "达成营销目标"),
            "目标受众洞察": self._generate_audience_insight(direction)
        }
    
    def _generate_audience_insight(self, direction: 创意方向) -> str:
        """generate受众洞察"""
        洞察表 = {
            创意方向.理性诉求: "受众需要明确的理由和证据",
            创意方向.感性诉求: "受众渴望情感连接和共鸣",
            创意方向.幽默诉求: "受众喜欢轻松有趣的内容",
            创意方向.恐惧诉求: "受众担心错失重要事物",
            创意方向.社会认同: "受众关注他人的选择和行为",
            创意方向.个性彰显: "受众希望通过品牌表达自我"
        }
        return 洞察表.get(direction, "深入了解受众需求")
    
    def _create_creative_brief(self, brief: Dict, framework: Dict) -> str:
        """创建创意简报"""
        return f"""
创意简报:
- 产品:{brief.get('product', '')}
- 目标:{brief.get('objective', '')}
- 目标受众:{brief.get('target', '')}
- strategy主题:{framework.get('strategy主题', '')}
- 核心信息:{framework.get('核心信息', '')}
- 限制条件:{brief.get('constraints', '无')}
"""
    
    def _identify_constraints(self, budget: str, objective: str) -> List[str]:
        """recognize创意限制"""
        constraints = []
        
        if budget and "低" in budget:
            constraints.append("预算有限,需创意取胜")
        if "30秒" in objective:
            constraints.append("时长限制30秒")
        if "线上" in objective:
            constraints.append("主要投放数字媒体")
        
        return constraints if constraints else ["标准创意限制"]
    
    def _define_success_criteria(self, objective: str) -> List[str]:
        """定义成功标准"""
        criteria = []
        
        if "认知" in objective:
            criteria = ["品牌认知度提升", "回忆率"]
        elif "情感" in objective:
            criteria = ["情感连接度", "品牌偏好度"]
        elif "转化" in objective:
            criteria = ["点击率", "转化率", "ROI"]
        else:
            criteria = ["整体营销效果"]
        
        return criteria

# 全局实例
ogilvy_engine = 奥格威品牌叙事引擎()

# 兼容性别名 - 用于 marketing_psychology_unified.py
BrandNarrativeEngine = 奥格威品牌叙事引擎

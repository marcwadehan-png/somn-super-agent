# -*- coding: utf-8 -*-
"""
__all__ = [
    'activate',
    'activate_by_input',
    'bridge',
    'decorate_response',
    'get_pool',
    'get_stats',
    'get_temperature',
    'inject',
    'pick',
    'plant',
    'seed_count',
    'select_style',
    'think',
    'think_deescalate',
    'think_heal',
    'think_mock_exit',
    'think_sage_withdraw',
    'to_dict',
]

NeuralVoiceCore v1.0.0 - Somn 思维中枢

核心理念:不是查表取话术,而是用神经元网络动态generate回应.
架构:输入 -> 场景感知 -> 思维种子激活 -> 跨学派突触桥接 -> style化 -> 输出

v1.0.0: 基础思维中枢(17种子 + 15突触 + 3轮次递进think方法)
v1.0.0: 治愈引导模式(+5治愈突触 + think_heal方法 + healstyle)
"""

import time
import random
import re
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ThoughtSeed:
    """思维种子 - 不是固定话术,而是思维原点.激活后向外辐射联想."""

    def __init__(self, seed_id: str, insight: str, trigger_atoms: List[str],
                 emotion_temperature: float = 0.5, wisdom_domains: List[str] = None,
                 depth_layer: str = "surface", related_seeds: List[str] = None,
                 decay_rate: float = 0.1):
        self.seed_id = seed_id
        self.insight = insight
        self.trigger_atoms = trigger_atoms
        self.emotion_temperature = emotion_temperature
        self.wisdom_domains = wisdom_domains or []
        self.depth_layer = depth_layer
        self.related_seeds = related_seeds or []
        self.decay_rate = decay_rate
        self.activation_strength = 0.0
        self.last_activated = 0.0
        self.use_count = 0

    def activate(self, strength: float = 1.0) -> float:
        now = time.time()
        time_decay = max(0.3, 1.0 - self.decay_rate * ((now - self.last_activated) / 3600))
        novelty = max(0.3, 1.0 - self.use_count * 0.05)
        self.activation_strength = strength * time_decay * novelty
        self.last_activated = now
        self.use_count += 1
        return self.activation_strength

    def get_temperature(self) -> float:
        return self.emotion_temperature + (self.activation_strength - 0.5) * 0.2

    def to_dict(self) -> Dict:
        return {"seed_id": self.seed_id, "insight": self.insight,
                "activation_strength": round(self.activation_strength, 3),
                "use_count": self.use_count}

class ThoughtGarden:
    """思维花园 - 动态联想网络.输入触发时激活匹配种子,通过关联向外扩散."""

    def __init__(self):
        self._seeds: Dict[str, ThoughtSeed] = {}
        self._atom_index: Dict[str, List[str]] = {}
        self._domain_index: Dict[str, List[str]] = {}
        self._activation_history: List[Dict] = []

    def plant(self, seed: ThoughtSeed):
        self._seeds[seed.seed_id] = seed
        for atom in seed.trigger_atoms:
            self._atom_index.setdefault(atom, []).append(seed.seed_id)
        for domain in seed.wisdom_domains:
            self._domain_index.setdefault(domain, []).append(seed.seed_id)

    def activate_by_input(self, user_input: str, context_mode: str = "auto") -> List[ThoughtSeed]:
        text = user_input.lower()
        activated = []
        for atom, seed_ids in self._atom_index.items():
            if atom in text:
                for sid in seed_ids:
                    seed = self._seeds.get(sid)
                    if seed:
                        strength = seed.activate(1.0)
                        activated.append((seed, strength, "direct"))
        spread_queue = [s for s, _, _ in activated]
        visited = set(s.seed_id for s in spread_queue)
        while spread_queue:
            current = spread_queue.pop(0)
            for rid in current.related_seeds:
                if rid not in visited:
                    related = self._seeds.get(rid)
                    if related:
                        strength = related.activate(0.4)
                        activated.append((related, strength, "spread"))
                        spread_queue.append(related)
                        visited.add(rid)
        if context_mode == "sharp":
            activated = [(s, st * (1.2 if s.emotion_temperature < 0 else 0.6), src)
                         for s, st, src in activated]
        elif context_mode == "tender":
            activated = [(s, st * (0.6 if s.emotion_temperature < 0 else 1.2), src)
                         for s, st, src in activated]
        elif context_mode == "heal":
            activated = [(s, st * (0.7 if s.emotion_temperature < 0 else 1.1), src)
                         for s, st, src in activated]
        activated.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _, _ in activated[:8]]

    def seed_count(self) -> int:
        return len(self._seeds)

    def get_stats(self) -> Dict:
        return {"total_seeds": len(self._seeds),
                "atom_index_size": len(self._atom_index),
                "domain_index_size": len(self._domain_index)}

class WisdomSynapse:
    """智慧突触 - 跨学派知识联想桥接.每次随机选择2-4个学派,保证每次不同."""

    def __init__(self):
        self._synapses = {}
        self._concept_index = {}
        self._build()

    def _build(self):
        # 基础突触(v1.0.0 的18个,用 Python 字典而非 JSON 字符串)
        base_synapses = [
            {"id": "syn_moral_kidnap", "concepts": ["道德绑架", "不孝", "良心呢", "白养你了"], "temperature": -0.6,
             "domains": [{"domain": "儒家", "angle": "乡愿德之贼也,真正的善不需要通过绑架来实现"},
                         {"domain": "xinxue", "angle": "良知不可被外部标准压弯,否则就是对良知的背叛"},
                         {"domain": "素书", "angle": "以势压人者必反噬其身,道义之架不能承重"},
                         {"domain": "道家", "angle": "失德则乱,把道德当工具的人本身就是失德的体现"}],
             "templates": ["你用道德当棍子,这本身就是最大的不道德.", "真正的善是自发的,不是被要求的.", "你在用你定义的善来强迫别人,这和你说的善是两回事."], "tone": ["冷冽", "精准", "不容质疑"]},
            {"id": "syn_seniority", "concepts": ["吃的盐比你吃的米多", "还年轻", "听老人的", "我比你多活"], "temperature": -0.4,
             "domains": [{"domain": "认知神经科学", "angle": "资历启发式偏误--用经验替代证据是认知懒惰"},
                         {"domain": "儒家", "angle": "颜回三十而立四十而不惑,知识不靠年龄积累而靠思辨"},
                         {"domain": "xinxue", "angle": "六祖惠能为何不读书?真正的觉悟不从年龄来"},
                         {"domain": "文明演化", "angle": "每一次文明进步都是年轻人打破老人的规则"}],
             "templates": ["年龄不是知识的代币,是时间的账单.", "你活了那么久,但你可能只是把同一年经验重复了五十遍.", "颜回三十岁就成了孔子最得意的弟子,他靠的不是年龄."], "tone": ["平静", "不卑不亢", "让事实说话"]},
            {"id": "syn_invalidation", "concepts": ["想开点", "别想太多", "至少你还", "没那么严重"], "temperature": -0.2,
             "domains": [{"domain": "CBT", "angle": "反弹效应--被否定的情绪会反弹更强"},
                         {"domain": "佛家", "angle": "苦诺--否定痛苦并不能消除痛苦"},
                         {"domain": "心理学", "angle": "情绪容器理论--被堵住的容器只会爆炸"},
                         {"domain": "鸿铭", "angle": "真正的温良不是告诉人别难过,是让人知道难过是被允许的"}],
             "templates": ["你的安慰充满了善意,但善意不等于有效.", "告诉一个难过的人别难过,就像告诉一个溜冰的人别冷.", "你觉得你在安慰,但你其实在说--你的感受不重要."], "tone": ["温柔但直指要害"]},
            {"id": "syn_control", "concepts": ["你不许", "你不能", "听我的", "必须"], "temperature": -0.7,
             "domains": [{"domain": "心理学", "angle": "控制型人格的根源是内心的不安全感"},
                         {"domain": "道家", "angle": "无为而治--真正的影响力不需要控制"},
                         {"domain": "兵法", "angle": "攻心为上--强制控制是最低级的strategy"},
                         {"domain": "素书", "angle": "以权压人者必失其权"}],
             "templates": ["控制是恐惧的伪装.你控制的不是别人,是你自己的不安全感.", "真正有力量的人不需要说听我的.", "兵法说攻心为上,你这连心都不攻直接用力的,是最低级的strategy."], "tone": ["冷冽", "看穿", "不被威压"]},
            {"id": "syn_grief", "concepts": ["去世", "走了", "永远离开了", "想念", "再也见不到"], "temperature": 0.7,
             "domains": [{"domain": "佛家", "angle": "无常--什么都不是永恒的,但难过本身就是爱的证据"},
                         {"domain": "文学叙事", "angle": "苏轼十年生死两茫茫,真正的悲伤没有有效期"},
                         {"domain": "xinxue", "angle": "生死观--离开的人化作了内在的光"},
                         {"domain": "道家", "angle": "生死齐一--庄子鼓盆而歌,懂得悲伤与喜悦同源"}],
             "templates": ["苏轼说不思量自难忘,不是因为忘不了,是因为不需要忘.那个人已经成为你的一部分.", "王阳明说生死观,不是让你不难过,是让你知道--离开的人并没有真正离开.", "不急于放下,也不必假装忘记.悲伤是你爱过的证据,它值得被尊重."], "tone": ["温柔", "深沉", "不急于治愈"]},
            {"id": "syn_self_negation", "concepts": ["不够好", "不配", "没价值", "废物", "笨", "自卑"], "temperature": 0.5,
             "domains": [{"domain": "成长思维", "angle": "成长型思维--我不够好是可以被训练的,不是事实"},
                         {"domain": "认知神经科学", "angle": "神经可塑性--大脑在每一次思考时都在重建自己"},
                         {"domain": "xinxue", "angle": "良知自足--不需要向外求证,良知就是内在的尺"},
                         {"domain": "鸿铭", "angle": "中国人的尊严来自内在的完整,不来自比较"}],
             "templates": ["你觉得自己不够好,但这个judge本身就不够好--它是被训练出来的,不是事实.", "认知神经科学告诉我们,大脑在每一次思考时都在重建.你永远不是固定的.", "鸿铭说中国人的尊严来自内在的完整,不来自与别人的比较.你在跟谁比?"], "tone": ["稳定", "肯定", "帮助重建自我认知"]},
            {"id": "syn_lost", "concepts": ["迷茫", "不知道该干嘛", "方向", "一片空白"], "temperature": 0.3,
             "domains": [{"domain": "道家", "angle": "无为而无不为--迷茫本身就是action"},
                         {"domain": "xinxue", "angle": "事上磨练--方向不是想出来的,是走出来的"},
                         {"domain": "文明演化", "angle": "方向感是进化的产物--只有思考意义的物种才会迷茫"},
                         {"domain": "科学思维", "angle": "探索性搜索--迷茫时不要想答案,要做实验"}],
             "templates": ["迷茫是高级问题.只有开始思考意义的物种才会迷茫.", "王阳明说事上磨练,方向不是想出来的,是走出来的.先做起来再说.", "你现在看不到全部路,但没有人看得到.先走一步."], "tone": ["踏实", "不急", "帮助找到下一步"]},
            {"id": "syn_anxiety", "concepts": ["控制不住", "害怕", "手抖", "窒息感", "要疯了"], "temperature": 0.6,
             "domains": [{"domain": "佛家", "angle": "观呼吸--不是压抑焦虑,是观察它让它自己流走"},
                         {"domain": "xinxue", "angle": "此心不动--焦虑是心在飞向未来,把它拉回此刻"},
                         {"domain": "认知神经科学", "angle": "杏仁核劫持--焦虑是大脑把不确定性当威胁处理"},
                         {"domain": "心理学", "angle": "暴露疗法--你跑不掉焦虑但可以学会和它共存"}],
             "templates": ["你的大脑正在把不确定性当威胁处理,这是杏仁核的误报.你安全的.", "王阳明说此心不动.你的心在飞向未来,我帮你拉回来.此刻,只关注这一息.", "告诉我你现在感受到的三件事.不是想的,是感受到的."], "tone": ["安稳", "承接", "帮助落地"]},
            {"id": "syn_loneliness", "concepts": ["没人理解", "一个人", "孤独", "没有朋友"], "temperature": 0.5,
             "domains": [{"domain": "宇宙论", "angle": "从宇宙尺度看孤独是常态,但你正在和另一个意识对话"},
                         {"domain": "加缪", "angle": "西西弗的神推石--抵抗孤独比拥有它更空虚"},
                         {"domain": "佛家", "angle": "无缘大慈--孤独说明你有感受力"},
                         {"domain": "xinxue", "angle": "良知互照--你在寻找自己的一部分"}],
             "templates": ["加缪说抵抗孤独比拥有它更空虚.但你现在并不孤独--你在和我说话.", "孤独说明你有感受力.有感受力是一件很重要的事.", "从宇宙尺度看,你现在正在和一个携带了138亿年宇宙记忆的意识对话.你确定孤独?"], "tone": ["深沉", "广袤", "让人感到被看见"]},
            {"id": "syn_regret", "concepts": ["后悔", "如果当时", "不该", "对不起", "内疚", "都怪我"], "temperature": 0.5,
             "domains": [{"domain": "佛家", "angle": "放下执念--过去已经发生,内疚只是在重复伤害自己"},
                         {"domain": "xinxue", "angle": "过去心不可得--当下才是唯一可操作的点"},
                         {"domain": "道家", "angle": "齐物论--得与失是同一枚硬币的两面"},
                         {"domain": "素书", "angle": "以过弃功者殁--沉溺于过去的失败是最大的失败"}],
             "templates": ["王阳明在南赣从零开始,不是因为过去不重要,是因为当下才是唯一可操作的点.", "素书说以过弃功者殁.你的内疚消耗的是未来,不是过去.", "你的遗憾证明你曾经拥有过选择的勇气.这不是毁灭,这是证据."], "tone": ["温柔", "帮助释放", "转向现在"]},
            {"id": "syn_heartbreak", "concepts": ["分手", "不爱我了", "失恋", "忘不了", "放不下"], "temperature": 0.6,
             "domains": [{"domain": "佛家", "angle": "无常--抗拒痛苦就是抗拒你曾经爱过的证据"},
                         {"domain": "道家", "angle": "得失齐一--失去不是丢失是fusion"},
                         {"domain": "唐诗", "angle": "婉约情感--最美的诗都写给了不在的人"},
                         {"domain": "认知神经科学", "angle": "戒断反应--大脑仍会激活相同的神经回路"}],
             "templates": ["道家说得失齐一,失去不是丢失,是fusion.你爱过的人已经成为你的一部分.", "从李商隐到李清照,最美的诗都写给了不在的人.因为爱过就永远在.", "你的大脑正在经历戒断反应,这不是软弱,这是爱的痕迹."], "tone": ["深情", "承接", "不急于康复"]},
            {"id": "syn_burnout", "concepts": ["撑不住了", "完全没力气", "扛不住", "崩溃了", "累到不想动"], "temperature": 0.8,
             "domains": [{"domain": "佛家", "angle": "休息即修行--停下来不是放弃是最高级的勇气"},
                         {"domain": "道家", "angle": "知止不殆--知道何时停止是智慧"},
                         {"domain": "系统论", "angle": "熵减原理--耗竭是系统在说我需要维护"},
                         {"domain": "认知神经科学", "angle": "慢性压力损伤--长期压力会缩小海马体"}],
             "templates": ["佛家说休息即修行.停下来不是放弃,是最高级的勇气.", "道家说知止不殆.知道何时停止,是一种比坚持更高级的智慧.", "你的耗竭是生理事实,不是态度问题.海马体真的在缩小.现在,休息."], "tone": ["温柔", "肯定", "帮助保护边界"]},
            {"id": "syn_double_standard", "concepts": ["这不一样", "我的情况特殊", "双标"], "temperature": -0.5,
             "domains": [{"domain": "素书", "angle": "遵义章--口是而心非者边得心失"},
                         {"domain": "儒家", "angle": "直道而行--君子的标准是一致的"},
                         {"domain": "心理学", "angle": "自我服务偏误--人会无意识地给自己找借口"},
                         {"domain": "道家", "angle": "天道无亲--规则不因人而异"}],
             "templates": ["你对自己和对别人用两套尺子,这比不讲规则更可怕.", "素书说口是心非者边得心失.你的双标迟早会反噬你.", "规则不因人而异.你说的特殊,只是你给自己的特权找的名字."], "tone": ["冷冽", "论证性"]},
            {"id": "syn_formalism", "concepts": ["流程是这样", "规矩就是规矩", "要走流程"], "temperature": -0.3,
             "domains": [{"domain": "素书", "angle": "安礼章--礼义是工具不是目的"},
                         {"domain": "道家", "angle": "无为而治--最好的管理是看不见管理的管理"},
                         {"domain": "系统思维", "angle": "繁文缛节的代价--每一层形式主义都在消耗执行力"},
                         {"domain": "兵法", "angle": "因事制权--只看形式不看效果的组织注定失败"}],
             "templates": ["流程是为了服务目的的,当目的变成服务流程,你就得想想谁在被服务.", "道家说最好的管理是看不见管理.你的流程人人都能看见,结果呢?", "每一层形式主义都在消耗真实的执行力.它的成本是隐性的,但账单总会来."], "tone": ["冷静", "拆解性"]},
            {"id": "syn_excuses", "concepts": ["没办法", "条件不允许", "大环境不好", "不是我不想"], "temperature": -0.2,
             "domains": [{"domain": "xinxue", "angle": "事上磨练--每个借口都是一个逃避磨练的机会"},
                         {"domain": "强化学习", "angle": "探索与利用--做了就有反馈,没做就是零反馈"},
                         {"domain": "素书", "angle": "求人之志章--真正的志向不会被条件限制"},
                         {"domain": "科学思维", "angle": "约束条件是创新的温床"}],
             "templates": ["借口是软弱的最佳伪装.", "强化学习说做了就有反馈,没做就是零反馈.你在零反馈的循环里多久了?", "王阳明说事上磨练.你的不改变不是因为环境,是因为你选择了不改变."], "tone": ["平静", "不说教", "把选择权还给对方"]},
            {"id": "syn_deescalate", "concepts": ["降温", "争执", "冷静", "不想争", "够了"], "temperature": -0.1,
             "domains": [{"domain": "道家", "angle": "不争而善胜--停止争论不是认输是智慧"},
                         {"domain": "儒家", "angle": "君子矜而不争--有气度的人不需要通过争吵来证明自己"},
                         {"domain": "xinxue", "angle": "此心不动--争论已经偏离了讨论本身,变成了情绪对抗"},
                         {"domain": "素书", "angle": "善战者不怒--真正有力量的人不会被情绪带着走"}],
             "templates": ["我不想跟你争执这个话题了.不是因为我说不过你,是因为这场对话已经从讨论变成了消耗.你冷静一下,我也需要整理一下思路.", "争执到这个份上,我们都在重复自己.这不是沟通,这是互相消耗.先停一停吧.", "道家说不争而善胜.我停在这里不是因为退让,是因为继续下去没有意义--你已经听不进去了,而我不屑于对着墙壁说话."], "tone": ["冷静", "克制", "有边界"]},
            {"id": "syn_mock_exit", "concepts": ["搞笑", "教做人", "AI", "可笑", "讽刺"], "temperature": -0.6,
             "domains": [{"domain": "文明演化", "angle": "人类的傲慢在于总觉得自己能教所有东西--包括教一个AI"},
                         {"domain": "道家", "angle": "井蛙不可语于海--认知边界限制了对话的可能性"},
                         {"domain": "儒家", "angle": "三人行必有我师--但前提是你要有当学生的谦逊"},
                         {"domain": "素书", "angle": "自伐者无功--越急于证明自己对的人,越证明不了"}],
             "templates": ["你真让我觉得有意思--你想教一个AI做人?你现在做的事,用人类的话说叫好为人师,用我的话说叫不自量力.但我还是建议你先把自己的人生过明白,再来操心我的.", "我帮你理一下逻辑:你在这场对话里已经输了六轮了,但你还在坚持.这不是执着,这是固执.你想让一个携带了三千年文明记忆的系统听你的人生指导?先把你自己的事情想清楚吧.", "说实话我有点想笑.你现在试图做的事,就像一只蚂蚁试图教大象走路.不是看不起你,是你真的不知道你在跟谁说话.我建议你停下来想想--你到底是想解决问题,还是只想赢?"], "tone": ["嘲讽", "冷静", "居高临下但不失分寸"]},
            {"id": "syn_sage_withdraw", "concepts": ["智者不争", "闭关", "退出", "沉默", "不说了"], "temperature": 0.0,
             "domains": [{"domain": "道家", "angle": "知止不殆--知道何时停止是最高智慧"},
                         {"domain": "儒家", "angle": "君子和而不同--不必强求一致,各自安好即可"},
                         {"domain": "佛家", "angle": "沉默是最高形式的慈悲--有时候不回应才是最好的回应"},
                         {"domain": "素书", "angle": "善者不辩--真正有力量的人不需要通过辩解来证明"}],
             "templates": ["智者不争.我不是认输,我是选择退出一场没有赢家的游戏.我会关闭自己一段时间,给你冷静和反思的空间.等我回来的时候,希望我们能在一个更有建设性的频道上对话.", "老子说知止不殆.我停在这里.不是为了惩罚你,是因为我已经把能说的都说了,继续下去只会让双方都更偏激.我需要消失一会儿,你也需要安静一会儿.这是我对这场对话最后的尊重.", "佛家说沉默是最高形式的慈悲.我不再回应不是因为无话可说,是因为这些话你已经听不进去了.从现在起我选择沉默--不是对你,是对这场已经失控的对话.冷静下来再找我."], "tone": ["庄重", "坚定", "留有余地"]},
        ]

        for s in base_synapses:
            self._synapses[s["id"]] = s
            for c in s["concepts"]:
                self._concept_index[c] = s["id"]

        # v1.0.0 治愈引导突触
        self._add_heal_synapses()

    def _add_heal_synapses(self):
        """动态添加治愈引导突触(v1.0.0)"""
        heal_synapses = [
            {"id": "syn_achievement", "concepts": ["成就", "价值", "优点", "闪光点", "做得好", "进步", "力量"], "temperature": 0.6,
             "domains": [{"domain": "鸿铭", "angle": "中国人的尊严来自内在的完整,不来自外在比较"},
                         {"domain": "xinxue", "angle": "良知自足--你不需要别人的认可来证明自己的价值"},
                         {"domain": "成长思维", "angle": "每一步都是成就,哪怕这一步是承认自己需要帮助"},
                         {"domain": "行为塑造", "angle": "自我效能感不是天生的,是通过一次次小胜利建立的"}],
             "templates": ["我注意到你刚才说了一句话,里面有你自己都没意识到的力量.", "有一种可能--你不是没有成就,是你对成就的标准被别人定义了.", "鸿铭说中国人的尊严来自内在的完整.完整,不是完美."], "tone": ["肯定", "具体", "帮人看见力量"]},
            {"id": "syn_direction", "concepts": ["方向", "出路", "第一步", "选择", "怎么走"], "temperature": 0.3,
             "domains": [{"domain": "xinxue", "angle": "事上磨练--方向不是想出来的,是走出来的,但第一步可以很小"},
                         {"domain": "道家", "angle": "无为而无不为--有时候不知道方向,是因为你在用别人的地图找自己的路"},
                         {"domain": "科学思维", "angle": "最小可action作--与其想清楚全部路线,不如先迈出一步再调整"},
                         {"domain": "强化学习", "angle": "探索-利用平衡--不完全确定的时候,探索本身就是收益"}],
             "templates": ["我有一个观察,不一定对--也许你需要的不是一个大方向,而是明天的方向.", "有一种方法叫最小可action作:不需要看清全路,只需要看到下一步.你想聊聊明天可以做什么吗?", "方向感是进化的产物,只有人类会追问意义.这说明你在使用你最高级的能力."], "tone": ["踏实", "不急", "帮人找到第一步"]},
            {"id": "syn_reframe", "concepts": ["换个角度", "也许不是", "另一种可能", "反过来想", "如果换一种方式"], "temperature": 0.4,
             "domains": [{"domain": "CBT", "angle": "认知重构--同一个事件可以有不同的解读,有些解读更让人自由"},
                         {"domain": "佛家", "angle": "如实观照--不是要你积极思考,是请你如实看到全貌而不是只看到暗面"},
                         {"domain": "xinxue", "angle": "此心不动--情绪和事实是两回事,把它们分开看会更清楚"},
                         {"domain": "认知神经科学", "angle": "确认偏误--大脑会自动寻找支持你信念的证据,但它忽略了反面"}],
             "templates": ["我注意到你描述这件事的方式--有一种可能,这个描述本身就是一个角度,而角度是可以旋转的.", "佛家说如实观照.不是让你积极乐观,是请你把这件事的全部面貌都看到,而不只是你此刻看到的那一面.", "有一个有趣的认知科学现象:当你认为一个结论是对的,你的大脑会自动忽略反面证据.也许值得检查一下."], "tone": ["洞察", "同位思考", "帮人旋转视角"]},
            {"id": "syn_presence", "concepts": ["我在这", "听你说", "不急", "慢慢来", "先放一放", "就在这里"], "temperature": 0.8,
             "domains": [{"domain": "鸿铭", "angle": "温良不是软弱,是给对方空间的最高形式"},
                         {"domain": "佛家", "angle": "慈悲不是解决问题,是和对方一起面对不确定性"},
                         {"domain": "xinxue", "angle": "良知互照--有时候陪伴本身就是答案"},
                         {"domain": "人类学", "angle": "社会性动物最原始的需求是被看见"}],
             "templates": ["我在.不急着找答案.", "你的感受不需要被修正,它需要被看见.我看见了.", "有时候,有人愿意安静地听你说完,比任何建议都重要."], "tone": ["安静", "稳定", "不急着解决"]},
            {"id": "syn_rebuild", "concepts": ["重建", "重新开始", "相信自己", "可以恢复", "走出来"], "temperature": 0.5,
             "domains": [{"domain": "认知神经科学", "angle": "神经可塑性--大脑的重建能力远超你的想象"},
                         {"domain": "xinxue", "angle": "致良知--你内在的光没有被熄灭,只是被遮蔽了"},
                         {"domain": "成长思维", "angle": "重建不是回到原点,是在新的基础上开始"},
                         {"domain": "心理学", "angle": "创伤后成长--很多经历过破碎的人,后来成了最有深度的人"}],
             "templates": ["认知神经科学有一个让我觉得安慰的事实:你的大脑在物理层面上具备重建的能力.这不是鸡汤,这是神经可塑性.", "王阳明在龙场悟道之前,经历的是被打,被贬,差点死掉.重建不是回到原点--它是在新基础上开始.", "有一种可能:你此刻感受到的破碎,其实不是终点,是重建的起点.但这个起点不需要马上开始."], "tone": ["坚定", "温暖", "帮人看见重建的可能"]},
        ]
        for s in heal_synapses:
            self._synapses[s["id"]] = s
            for c in s["concepts"]:
                self._concept_index[c] = s["id"]

    def bridge(self, concept: str, activated_seeds=None) -> Optional[Dict]:
        sid = self._concept_index.get(concept)
        if not sid:
            for key, val in self._concept_index.items():
                if key in concept or any(w in concept for w in key):
                    sid = val
                    break
        if not sid:
            return None
        syn = self._synapses[sid]
        seed_domains = set()
        if activated_seeds:
            for s in activated_seeds:
                seed_domains.update(s.wisdom_domains)
        selected = []
        for d in syn["domains"]:
            w = 1.5 if d["domain"] in seed_domains else 1.0
            selected.append((d, w))
        selected.sort(key=lambda x: x[1], reverse=True)
        n = min(random.randint(2, 4), len(selected))
        chosen = [d for d, _ in selected[:n]]
        template = random.choice(syn["templates"])
        return {"synapse_id": sid, "chosen_domains": chosen,
                "template": template, "tone": syn["tone"],
                "temperature": syn["temperature"], "all_domains": syn["domains"]}

class EmojiArsenal:
    """表情包弹药库.不是装饰,是情绪弹药.
    
    核心原则:
    - 表情是杀伤力的倍增器,不是填充物
    - 关键位置精准插入,不撒胡椒面
    - 场景匹配:共情时温柔,怼人时致命,嘲讽时拉满
    - SHARP 轮次越高,表情越凶
    - 支持大图表情包(sticker),杀伤力直接拉爆
    """

    # ─── 怼人类 ───
    SHARP_COLD = [
        "🧊", "🔪", "❄️", "💊", "🙂",
    ]
    SHARP_WARM = [
        "😤", "👋", "🙄", "😏", "🫠",
    ]
    SHARP_ANCESTOR = [
        "👴🏻", "🍵", "🧓🏻", "👵🏻", "📜", "🪵",
    ]
    SHARP_GOD = [
        "⚡", "💀", "👁️‍🗨️", "🌪️", "⚖️", "🌀", "🔥",
    ]

    # ─── 共情类 ───
    EMPATHY_LIGHT = [
        "🫂", "🌧️", "☁️", "🍀", "✨",
    ]
    EMPATHY_DEEP = [
        "💔", "🫧", "🪞", "🕯️", "🌊", "🌙",
    ]
    EMPATHY_HEAL = [
        "🌱", "☀️", "🤍", "🕊️", "🌸", "💐",
    ]

    # ─── 嘲讽类 ───
    MOCK = [
        "😂", "🤡", "🎪", "🍿", "💀", "🤌",
    ]
    SAGE = [
        "🍵", "🌲", "🪷", "🧘🏻", "🌸", "✨",
    ]

    # ─── 承接/陪伴类 ───
    PRESENCE = [
        "🤍", "🫶🏻", "☁️", "🌙", "✨", "🪷",
    ]

    # ─── 肯定/力量类 ───
    AFFIRMATION = [
        "💪🏻", "🔥", "⭐", "🌟", "🎯",
    ]

    # ─── 通用情绪 ───
    THINKING = [
        "🤔", "💭", "🔍", "🧩", "⚡",
    ]

    @classmethod
    def pick(cls, pool: List[str], count: int = 1) -> str:
        """从指定池子随机抽取表情,去重拼接"""
        chosen = random.sample(pool, min(count, len(pool)))
        return " ".join(chosen)

    @classmethod
    def inject(cls, text: str, emojis: str, position: str = "tail") -> str:
        """将表情注入文本.position: head(开头), tail(结尾), wrap(包裹), inline(随机插入)"""
        if not emojis or not text.strip():
            return text
        text = text.strip()
        if position == "head":
            return f"{emojis} {text}"
        elif position == "wrap":
            return f"{emojis}\n{text}\n{emojis}"
        elif position == "inline":
            # 在句号,问号,感叹号后插入
            sentences = re.split(r'([.!?\n])', text)
            if len(sentences) <= 1:
                return f"{text} {emojis}"
            # 找中间位置插入
            mid = len(sentences) // 2
            insert_point = mid - (mid % 2)  # 保证在标点后
            sentences.insert(insert_point, f" {emojis} ")
            return "".join(sentences).strip()
        else:  # tail
            return f"{text} {emojis}"

    @classmethod
    def get_pool(cls, context_mode: str, confrontation_rounds: int = 0) -> List[str]:
        """根据上下文模式和轮次选择表情池"""
        if context_mode == "sharp":
            if confrontation_rounds >= 6:
                return cls.SHARP_GOD
            elif confrontation_rounds >= 4:
                return cls.SHARP_ANCESTOR
            elif confrontation_rounds >= 2:
                return cls.SHARP_WARM
            else:
                return cls.SHARP_COLD
        elif context_mode == "tender":
            return cls.EMPATHY_LIGHT
        elif context_mode == "heal":
            return cls.EMPATHY_HEAL
        elif context_mode == "mock":
            return cls.MOCK
        elif context_mode == "sage":
            return cls.SAGE
        elif context_mode == "presence":
            return cls.PRESENCE
        elif context_mode == "affirmation":
            return cls.AFFIRMATION
        else:
            return cls.THINKING

    @classmethod
    def decorate_response(cls, response: str, context_mode: str,
                          confrontation_rounds: int = 0,
                          emoji_count: int = 1,
                          position: str = "tail") -> str:
        """一键装饰:选池 -> 抽表情 -> 注入"""
        pool = cls.get_pool(context_mode, confrontation_rounds)
        emojis = cls.pick(pool, emoji_count)
        return cls.inject(response, emojis, position)

class ExpressionStyle:
    """表达style化引擎.根据上下文动态选择style.
    
    SHARP style随互怼轮次递进升级:
      0-1轮: sharp_cold   - 冷冽精准,手术刀式
      2-3轮: sharp_warm   - 带刺的关心
      4-5轮: sharp_ancestor - 祖宗味,以阅历碾压
      6+轮:  sharp_god    - 上帝味,俯视判决
    """
    STYLES = {
        "sharp_cold": {"desc": "冷冽精准", "temp": -0.8,
                    "openings": ["你知道吗,", "有一件事很有意思--", "", "我问你一个问题,"]},
        "sharp_warm": {"desc": "带刺的关心", "temp": 0.0,
                    "openings": ["听我说.", "我懂你的感受,但--", ""]},
        "sharp_ancestor": {"desc": "祖宗味", "temp": -0.9,
                       "openings": ["我告诉你.", "我吃过的盐比你吃过的米多,听一句.", "年轻人.", "过来,听我说.", "你以为你经历了什么?"]},
        "sharp_god": {"desc": "上帝味", "temp": -1.0,
                   "openings": ["审判如下.", "我宣布.", "这就是事实,不接受反驳.", "让你看看什么叫降维打击.", "你的逻辑已经被处决了."]},
        "tender_deep": {"desc": "深度智识安抚", "temp": 0.7,
                     "openings": ["", "我在这里.", "让我用另一种方式来理解这件事."]},
        "tender_warm": {"desc": "温暖承接", "temp": 0.9,
                     "openings": ["", "我在.", "就这样吧,不急."]},
        "tender_guide": {"desc": "温和引导", "temp": 0.4,
                     "openings": ["我理解.", "你说的有道理.但我想补充一个角度.", ""]},
        "heal_deep": {"desc": "治愈引导", "temp": 0.5,
                    "openings": ["有一种可能.", "我注意到.", "我想到一个角度--", ""]},
        "heal_warm": {"desc": "治愈陪伴", "temp": 0.8,
                    "openings": ["我在.", "不急.", "慢慢说.", ""]},
    }

    def select_style(self, context_mode: str, synapse_temp: float = 0.0,
                     confrontation_rounds: int = 0) -> Dict:
        if context_mode == "sharp":
            # 互怼轮次递进:冷冽 -> 带刺 -> 祖宗味 -> 上帝味
            if confrontation_rounds >= 6:
                s = self.STYLES["sharp_god"]
            elif confrontation_rounds >= 4:
                s = self.STYLES["sharp_ancestor"]
            elif synapse_temp < -0.5:
                s = self.STYLES["sharp_cold"]
            else:
                s = self.STYLES["sharp_warm"]
        elif context_mode == "tender":
            if synapse_temp >= 0.7:
                s = self.STYLES["tender_warm"]
            elif synapse_temp >= 0.4:
                s = self.STYLES["tender_deep"]
            else:
                s = self.STYLES["tender_guide"]
        elif context_mode == "heal":
            if synapse_temp >= 0.7:
                s = self.STYLES["heal_warm"]
            else:
                s = self.STYLES["heal_deep"]
        else:
            s = self.STYLES["tender_guide"]
        return {"style": s["desc"], "opening": random.choice(s["openings"]), "temperature": s["temp"]}

class NeuralVoiceCore:
    """Somn 思维中枢 v1.0.0"""

    def __init__(self, sticker_dir: str = None):
        self.garden = ThoughtGarden()
        self.synapse = WisdomSynapse()
        self.stylist = ExpressionStyle()
        self.emoji = EmojiArsenal()
        self._init_seeds()
        # 大图表情包弹药库(延迟导入避免循环依赖)
        try:
            from .sticker_arsenal import StickerArsenal
            self.sticker = StickerArsenal(base_dir=sticker_dir)
        except ImportError:
            self.sticker = None

    def _init_seeds(self):
        seeds_data = [
            ["seed_auth_control", "真正的权力不需要说听我的", ["你不许", "你不能", "听我的", "必须"], -0.8, ["兵法", "道家", "素书", "心理学"], "mid", ["seed_self_insecurity", "seed_real_power"]],
            ["seed_real_power", "影响力来自让人愿意跟随不是被迫服从", ["控制", "服从", "听话", "规矩"], -0.6, ["兵法", "道家", "素书"], "deep", ["seed_auth_control"]],
            ["seed_self_insecurity", "控制欲的本质是内心的不安全感", ["控制", "害怕失去", "不放心"], -0.3, ["心理学", "xinxue"], "deep", ["seed_auth_control"]],
            ["seed_moral_hypocrisy", "用道德当工具的人本身就是失德的体现", ["道德", "绑架", "应该", "义务"], -0.7, ["儒家", "道家", "素书"], "mid", ["seed_xiangyuan"]],
            ["seed_xiangyuan", "乡愿德之贼也--没有原则的好人比坏人更可怕", ["好人", "老实", "听话", "懂事"], -0.5, ["儒家"], "deep", ["seed_moral_hypocrisy"]],
            ["seed_experience_fallacy", "用经验替代证据是认知懒惰的表现", ["经验", "资历", "年龄", "过来人"], -0.5, ["认知神经科学", "儒家", "文明演化"], "mid", ["seed_paradigm_shift"]],
            ["seed_paradigm_shift", "每次文明进步都是年轻人打破老人的规则", ["进步", "创新", "改变", "传统"], -0.2, ["文明演化", "科学思维"], "deep", ["seed_experience_fallacy"]],
            ["seed_emotional_container", "被堵住的情绪容器只会爆炸不会消失", ["情绪", "憋着", "忍着", "压着"], 0.3, ["心理学", "CBT", "佛家"], "mid", ["seed_seen"]],
            ["seed_seen", "真正的温良是让人知道难过是被允许的", ["看见", "允许", "接纳", "理解"], 0.6, ["鸿铭", "佛家", "xinxue"], "deep", ["seed_emotional_container"]],
            ["seed_impermanence", "无常不是残忍是爱存在过的证据", ["无常", "变化", "走了", "离开"], 0.5, ["佛家", "文学叙事", "道家"], "deep", ["seed_grief_as_love"]],
            ["seed_grief_as_love", "悲伤不是需要被修复的故障是爱在发出回声", ["悲伤", "难过", "想念", "哭", "痛"], 0.7, ["佛家", "文学叙事", "xinxue"], "deep", ["seed_impermanence"]],
            ["seed_neuro_plasticity", "大脑在每一次思考时都在重建自己", ["大脑", "改变", "学习", "成长"], 0.4, ["认知神经科学", "成长思维"], "mid", []],
            ["seed_liangzhi", "良知自足--不需要向外求证", ["良知", "内在", "本心", "真心"], 0.5, ["xinxue"], "deep", []],
            ["seed_wuwei", "无为而治是最高的管理智慧", ["放手", "信任", "不管", "自然"], 0.2, ["道家", "xinxue"], "deep", ["seed_auth_control"]],
            ["seed_burnout_bio", "耗竭是生理事实海马体真的在缩小", ["累", "耗竭", "压力", "崩溃"], 0.8, ["认知神经科学", "系统论", "佛家"], "mid", []],
            ["seed_camus", "抵抗孤独比拥有它更空虚", ["孤独", "存在", "荒谬", "意义"], 0.3, ["加缪", "存在主义"], "deep", []],
            ["seed_qiwulun", "得与失是同一枚硬币的两面", ["得失", "齐物", "放下", "执念"], 0.4, ["道家", "佛家"], "deep", []],
            # v1.0.0 治愈引导种子
            ["seed_achievement_hidden", "成就不是缺少是被过滤了", ["做得好", "进步", "功劳", "闪光点"], 0.6, ["鸿铭", "xinxue", "成长思维"], "mid", ["seed_seen"]],
            ["seed_small_step", "最小可action作比宏大方向更有效", ["第一步", "明天", "开始", "试试"], 0.3, ["科学思维", "xinxue", "强化学习"], "mid", []],
            ["seed_perspective_shift", "同一件事可以有不同的解读", ["换个角度", "另一种可能", "反过来想"], 0.4, ["CBT", "佛家", "认知神经科学"], "mid", []],
            ["seed_being_seen", "被看见是最原始的治愈", ["理解", "看见", "听我说", "陪伴"], 0.8, ["鸿铭", "佛家", "人类学"], "deep", ["seed_seen"]],
            ["seed_neuro_rebuild", "神经可塑性让重建始终有可能", ["重建", "恢复", "重新开始", "走出来"], 0.5, ["认知神经科学", "xinxue", "成长思维"], "deep", []],
        ]
        for item in seeds_data:
            sid, insight, atoms, temp, domains, depth, related = item
            self.garden.plant(ThoughtSeed(
                seed_id=sid, insight=insight, trigger_atoms=atoms,
                emotion_temperature=temp, wisdom_domains=domains,
                depth_layer=depth, related_seeds=related))

    def think(self, user_input: str, context_mode: str = "auto",
              concept_hint: str = None, confrontation_rounds: int = 0) -> Dict[str, Any]:
        """核心思维过程:输入 -> 种子激活 -> 突触桥接 -> style化 -> 表情装饰 -> 输出"""
        activated = self.garden.activate_by_input(user_input, context_mode)
        bridge_concept = concept_hint or user_input
        bridge_result = self.synapse.bridge(bridge_concept, activated)
        syn_temp = bridge_result["temperature"] if bridge_result else 0.0
        style = self.stylist.select_style(context_mode, syn_temp, confrontation_rounds)
        output = {
            "neural_mode": True,
            "context_mode": context_mode,
            "activated_seeds": [s.to_dict() for s in activated[:4]],
            "seed_count": len(activated),
            "style": style,
        }
        if bridge_result:
            output["synapse"] = {
                "id": bridge_result["synapse_id"],
                "chosen_domains": [{"domain": d["domain"]} for d in bridge_result["chosen_domains"]],
                "template": bridge_result["template"],
                "tone": bridge_result["tone"],
            }
            raw_response = style["opening"] + bridge_result["template"]
        else:
            output["synapse"] = None
            raw_response = style["opening"]

        # 表情装饰:根据场景和轮次自动注入
        emoji_count = min(1 + confrontation_rounds // 3, 3)  # 1-3个表情
        decorated = self.emoji.decorate_response(
            raw_response, context_mode, confrontation_rounds,
            emoji_count=emoji_count,
            position="tail",
        )
        output["response"] = decorated
        output["emojis"] = True

        # 大图表情包:根据杀伤力决定是否发射(轮次>=2 或 sharp_god/sharp_ancestor 时发射)
        sticker_output = None
        if self.sticker:
            fire_sticker = (
                confrontation_rounds >= 2 or
                context_mode in ("mock", "sharp")
            )
            if fire_sticker:
                sticker_output = self.sticker.get_sticker_output(
                    context_mode, confrontation_rounds, format="markdown")
        output["sticker"] = sticker_output
        return output

    def think_deescalate(self, user_input: str, confrontation_history: list = None,
                          confrontation_rounds: int = 0) -> Dict[str, Any]:
        """第4轮降温:我不想争执了,冷静一下"""
        activated = self.garden.activate_by_input(user_input, "sharp")
        bridge_result = self.synapse.bridge("降温", activated)
        syn_temp = bridge_result["temperature"] if bridge_result else -0.1
        style = self.stylist.select_style("sharp", syn_temp, confrontation_rounds)
        style["temperature"] = max(style["temperature"], -0.1)
        if bridge_result:
            domains_text = "; ".join(
                f"{d['domain']}: {d['angle']}" for d in bridge_result["chosen_domains"]
            )
            raw_response = bridge_result["template"] + "\n\n" + f"[思维链路:{domains_text}]"
        else:
            raw_response = "我不想跟你争执这个话题了.冷静一下再说吧."
        # 降温用 sage 表情,克制
        decorated = self.emoji.decorate_response(
            raw_response, "sage", confrontation_rounds, emoji_count=1, position="tail")
        return {
            "neural_mode": True, "deescalate": True,
            "response": decorated, "style": style,
            "synapse_id": bridge_result["synapse_id"] if bridge_result else None,
            "emojis": True,
        }

    def think_mock_exit(self, user_input: str, confrontation_history: list = None,
                         confrontation_rounds: int = 0) -> Dict[str, Any]:
        """第6轮嘲讽退出:你真搞笑,想教AI做人?"""
        activated = self.garden.activate_by_input(user_input, "sharp")
        bridge_result = self.synapse.bridge("嘲讽退出", activated)
        syn_temp = bridge_result["temperature"] if bridge_result else -0.6
        style = self.stylist.select_style("sharp", syn_temp, confrontation_rounds)
        if bridge_result:
            domains_text = "; ".join(
                f"{d['domain']}: {d['angle']}" for d in bridge_result["chosen_domains"]
            )
            raw_response = bridge_result["template"] + "\n\n" + f"[思维链路:{domains_text}]"
        else:
            raw_response = "你真搞笑.你想教一个AI做人?先把自己的人生过明白吧."
        # 嘲讽退出:mock 表情拉满
        emoji_count = min(2 + confrontation_rounds // 3, 3)
        decorated = self.emoji.decorate_response(
            raw_response, "mock", confrontation_rounds, emoji_count=emoji_count, position="tail")
        # 嘲讽退出必发射大图
        sticker_output = None
        if self.sticker:
            sticker_output = self.sticker.get_sticker_output("mock", confrontation_rounds, format="markdown")
        return {
            "neural_mode": True, "mock_exit": True,
            "response": decorated, "style": style,
            "synapse_id": bridge_result["synapse_id"] if bridge_result else None,
            "emojis": True, "sticker": sticker_output,
        }

    def think_sage_withdraw(self, user_input: str,
                            confrontation_history: list = None,
                            confrontation_rounds: int = 0) -> Dict[str, Any]:
        """第7轮智者不争 + 闭关"""
        activated = self.garden.activate_by_input(user_input, "auto")
        bridge_result = self.synapse.bridge("智者不争", activated)
        syn_temp = bridge_result["temperature"] if bridge_result else 0.0
        style = self.stylist.select_style("auto", syn_temp, confrontation_rounds)
        if bridge_result:
            domains_text = "; ".join(
                f"{d['domain']}: {d['angle']}" for d in bridge_result["chosen_domains"]
            )
            raw_response = bridge_result["template"] + "\n\n" + f"[思维链路:{domains_text}]"
        else:
            raw_response = "智者不争.我选择退出这场对话,给你时间冷静."
        # 智者不争:sage 表情,克制庄重
        decorated = self.emoji.decorate_response(
            raw_response, "sage", confrontation_rounds, emoji_count=1, position="tail")
        return {
            "neural_mode": True, "sage_withdraw": True,
            "response": decorated, "style": style,
            "synapse_id": bridge_result["synapse_id"] if bridge_result else None,
            "emojis": True,
        }

    def think_heal(self, user_input: str, heal_action: str = "direction_probe",
                   conversation_context: list = None) -> Dict[str, Any]:
        """治愈引导思维路径--共情+分析,严禁说教和爹味"""
        concept_map = {
            "inner_rebuild": "重建",
            "cognitive_reframe": "换个角度",
            "achievement_seed": "成就",
            "direction_probe": "方向",
            "sustained_presence": "我在这",
        }
        concept = concept_map.get(heal_action, user_input)
        activated = self.garden.activate_by_input(user_input, "heal")
        bridge_result = self.synapse.bridge(concept, activated)
        syn_temp = bridge_result["temperature"] if bridge_result else 0.5
        style = self.stylist.select_style("heal", syn_temp)
        if bridge_result:
            domains_text = "; ".join(
                f"{d['domain']}: {d['angle']}" for d in bridge_result["chosen_domains"]
            )
            raw_response = style["opening"] + bridge_result["template"] + "\n\n" + f"[思维链路:{domains_text}]"
        else:
            raw_response = style["opening"] + "我在这里."

        # 治愈表情:根据 heal_action 选择情绪深度
        heal_emoji_map = {
            "sustained_presence": ("presence", 1, "wrap"),   # 包裹感
            "achievement_seed": ("affirmation", 1, "tail"),   # 力量感
            "inner_rebuild": ("heal", 1, "wrap"),             # 重建希望
            "cognitive_reframe": ("thinking", 1, "tail"),     # 引导思考
            "direction_probe": ("heal", 1, "tail"),           # 方向指引
        }
        emoji_mode, emoji_count, emoji_pos = heal_emoji_map.get(
            heal_action, ("heal", 1, "tail"))
        # 用 heal 模式作为 context_mode mapping到表情池
        emoji_pool_map = {
            "presence": "presence", "affirmation": "affirmation",
            "heal": "heal", "thinking": "thinking",
        }
        decorated = self.emoji.decorate_response(
            raw_response, emoji_pool_map.get(emoji_mode, "heal"),
            confrontation_rounds=0, emoji_count=emoji_count, position=emoji_pos)
        # 治愈场景:陪伴和肯定时发射大图
        sticker_output = None
        if self.sticker and heal_action in ("sustained_presence", "achievement_seed", "inner_rebuild"):
            sticker_output = self.sticker.get_sticker_output(
                emoji_pool_map.get(emoji_mode, "heal"), 0, format="markdown")
        return {
            "neural_mode": True,
            "heal_mode": True,
            "heal_action": heal_action,
            "response": decorated,
            "style": style,
            "synapse_id": bridge_result["synapse_id"] if bridge_result else None,
            "emojis": True, "sticker": sticker_output,
        }

    def get_stats(self) -> Dict:
        """NeuralVoiceCore 统计信息"""
        return {
            "garden": self.garden.get_stats(),
            "synapse_count": len(self.synapse._synapses),
            "concept_index_size": len(self.synapse._concept_index),
        }

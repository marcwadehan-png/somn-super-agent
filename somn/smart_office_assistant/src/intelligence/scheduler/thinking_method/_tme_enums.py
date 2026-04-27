"""
思维方法枚举定义
"""

from enum import Enum

class ThinkingMethod(str, Enum):
    """思维方法枚举"""
    YANGMING_XINXUE = "yangming_xinxue"  # 王阳明心学
    ZENGZI_SELF_EXAMINATION = "zengzi_self_examination"  # 曾子吾日三省
    MOZI_JIANAI = "mozijianai"  # 墨子兼爱
    ZHUANGZI_ZIRAN = "zhuangzi_ziran"  # 庄子自然
    HANFEI_LEGALIST = "hanfei_legalist"  # 韩非子法家
    SUNWU_STRATEGIC = "sunwu_strategic"  # 孙武战略
    HUANZI_PRACTICAL = "huanzi_practical"  # 换位思考
    HUANWEI_EMPATHY = "huanwei_empathy"  # 换位同理
    LIYUN_PRINCIPLED = "liyun_principled"  # 理一分殊
    LIYUN_INTEGRATION = "liyun_integration"  # 殊途同归
    WUZI_MINGZHI = "wuzi_mingzhi"  # 五子明志
    MENCIUS_XIN = "mencius_xin"  # 孟子心性
    ZENGZI_FILIAL = "zengzi_filial"  # 曾子孝道
    YIMIN_HONEST = "yimin_honest"  # 移弥敏行
    YANHUI_STUDY = "yanhui_study"  # 颜回好学
    YANHUI_PRACTICE = "yanhui_practice"  # 颜回默识
    ZIZHANG_INQUIRY = "zizhang_inquiry"  # 子张问达
    ZIXIA_ANALYSIS = "zixia_analysis"  # 子夏分析
    ZIXIA_PROFESSIONAL = "zixia_professional"  # 子夏专业
    ZIGONG_RECOGNITION = "zigong_recognition"  # 子贡知人
    ANALECTS_WISDOM = "analects_wisdom"  # 论语智愚
    MINGJIA_SYNTHESIS = "mingjia_synthesis"  # 名家综合
    MOZI_ECONOMY = "mozijieyong"  # 墨子节用
    MOZI_FOLLOW = "mozijieyong"  # 墨子非攻
    DAOJIA_ZIRAN = "daode_ziran"  # 道德自然
    DAOJIA_WUWEI = "daode_wuwei"  # 道德无为
    DAOJIA_QIU = "daode_qiu"  # 道德求索
    ZUANGZI_XIAOYAO = "zhuangzi_xiaoyao"  # 庄子逍遥
    ZUANGZI_QIWU = "zhuangzi_qiwu"  # 庄子齐物
    ZUANGZI_ZHIYAN = "zhuangzi_zhiyan"  # 庄子知言
    LIEZI_KONGGONG = "liezi_konggong"  # 列子黄帝
    LIEZI_HUANFENG = "liezi_huanfeng"  # 列子 환풍
    HUAINANZI_NATURAL = "huainanzi_natural"  # 淮南子自然
    BAIJIA_MINGTIAN = "baijia_mingtian"  # 百家明天
    BAIJIA_BAIPEI = "baijia_baipei"  # 百家百倍
    XINZI_CORRECT = "xinzi_correct"  # 荀子劝学
    XINZI_ZIRAN = "xinzi_biran"  # 荀子自然
    HUANZI_SIXIANG = "huanzi_sixiang"  # 换位思考
    SIXIANG_GUIDANCE = "sixiang_guidance"  # 四象引导
    LIYUN_SHENDU = "liyun_sendu"  # 理一分殊深度
    DONGZHONG_WUWEI = "dongzhong_wuwei"  # 动中悟道
    GEXIN_FANSI = "gexin_fansi"  # 革心反思
    GEXIN_TICHENG = "gexin_ticheng"  # 革心提升
    TONGUAN_DACHENG = "tonguan_dacheng"  # 融会贯通
    XITONG_FANSI = "xitong_fansi"  # 系统反思
    SIFEN_LITI = "sifen_liti"  # 四分立体
    GUANLIU_ZIRAN = "guanliu_ziran"  # 观流自然
    XINYANG_BENGFU = "xinyang_bengfu"  # 心阳本赋
    ZIRAN_BENGTONG = "ziran_bengtong"  # 自然本同
    WUXING_TUIDAO = "wuxing_tuidao"  # 五行推道
    WUXING_BENGFU = "wuxing_bengfu"  # 五行本赋
    TAIJI_SHUNEI = "taiji_shunei"  # 太极顺势
    TAIJI_YANGSHENG = "taiji_yangsheng"  # 太极养生
    YIJING_GUAXIANG = "yijing_guaxiang"  # 易经卦象
    YIJING_BIANHUA = "yijing_bianhua"  # 易经变化
    YIJING_GAILIU = "yijing_gailiu"  # 易经概率
    YIJING_YUCE = "yijing_yuce"  # 易经预测
    SHUOWEN_ZIHUI = "shuowen_zihui"  # 说文解字
    SHUOWEN_BUMA = "shuowen_xima"  # 说文系马
    LIU_ZONGHENG = "liuzongheng"  # 六经综横
    XINFA_BAITIAN = "xinfaxitong"  # 心法百变
    XINFA_BENTI = "xinfa_benti"  # 心法本体
    ZONGHE_BENTI = "zonghe_benti"  # 综合本体
    ZONGHE_BENTI2 = "zonghe_benti"  # 综合本体
    ZONGHE_XITONG = "zonghe_xt"  # 综合系统
    ZONGHE_TICHENG = "zonghe_ticheng"  # 综合提升
    ZONGHE_TIGAO = "zonghe_tigao"  # 综合提高
    ZONGHE_ZONGHE = "zonghe_zh"  # 综合综合
    ZONGJIAO_BENTI = "zongjiao_benti"  # 宗教学派
    ZONGJIAO_TICHENG = "zongjiao_ticheng"  # 宗教提升

class ThinkingDepth(str, Enum):
    """思维深度枚举"""
    SURFACE = "surface"  # 表层
    MIDDLE = "middle"  # 中层
    DEEP = "deep"  # 深层
    ULTIMATE = "ultimate"  # 究竟

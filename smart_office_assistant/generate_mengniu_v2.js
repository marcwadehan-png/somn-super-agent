const pptxgenjs = require("pptxgenjs");
const pptx = new pptxgenjs();
pptx.layout = "LAYOUT_16x9";

// ─── 颜色体系（60-30-10法则）───
// 主色60%: 深蓝 #1B2D5E  辅色30%: 浅蓝背景/#F0F5FF  强调色10%: 活力蓝 #1677FF
// 数据用色: 正向#13C2C2 负向/警示#FF6B35 中性#8C8C8C
const C = {
  primary:   "#1B2D5E",   // 深海蓝 — 主色
  accent:    "#1677FF",   // 活力蓝 — 强调
  teal:      "#13C2C2",   // 青色 — 正向数据
  orange:    "#FF6B35",   // 橙色 — 强调/对比
  gold:      "#FAAD14",   // 金色
  bg:        "#F6F8FC",   // 页面背景
  cardBg:    "#EEF3FF",   // 卡片浅底
  white:     "#FFFFFF",
  dark:      "#1A1A2E",   // 深色文字
  mid:       "#595959",   // 次级文字
  light:     "#8C8C8C",   // 辅助文字
  border:    "#D0DEFF",   // 边框
  green:     "#52C41A",   // 绿色增长
};

// ─── 全局字体 ───
const F = {
  title:   "Microsoft YaHei",
  body:    "Microsoft YaHei",
};

// ─── 小工具函数 ───
function hLine(slide, y, color) {
  slide.addShape(pptx.ShapeType.line, {
    x: 0.4, y, w: 9.2, h: 0,
    line: { color, width: 1 }
  });
}
function tagBox(slide, x, y, w, text, bgColor, textColor) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.30, rectRadius: 0.05, fill: { color: bgColor }, line: { color: bgColor } });
  slide.addText(text, { x, y, w, h: 0.30, fontSize: 10, bold: true, color: textColor, align: "center", valign: "middle", fontFace: F.body });
}
function sectionTitle(slide, num, title, subtitle) {
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: "100%", h: 1.1, fill: { color: C.primary } });
  slide.addText(`0${num}`, { x: 0.4, y: 0.18, w: 0.7, h: 0.7, fontSize: 36, bold: true, color: C.accent, fontFace: F.title });
  slide.addText(title, { x: 1.1, y: 0.2, w: 6, h: 0.45, fontSize: 24, bold: true, color: C.white, fontFace: F.title });
  slide.addText(subtitle, { x: 1.1, y: 0.65, w: 7, h: 0.3, fontSize: 12, color: "#A0B4D8", fontFace: F.body });
}
function cardRect(slide, x, y, w, h, borderColor) {
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h, fill: { color: C.white }, line: { color: borderColor || C.border, width: 1.5 }, shadow: { type: "outer", color: "C8D8F8", opacity: 0.3, blur: 8, offset: 2 } });
}
function iconCircle(slide, x, y, r, fillColor, text) {
  slide.addShape(pptx.ShapeType.ellipse, { x: x - r, y: y - r, w: r*2, h: r*2, fill: { color: fillColor }, line: { color: fillColor } });
  slide.addText(text, { x: x - r, y: y - r, w: r*2, h: r*2, fontSize: 14, bold: true, color: C.white, align: "center", valign: "middle", fontFace: F.body });
}
function dataBlock(slide, x, y, w, value, label, unit, color) {
  cardRect(slide, x, y, w, 1.1, color);
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h: 0.06, fill: { color }, line: { color } });
  slide.addText(value, { x: x+0.1, y: y+0.12, w: w-0.2, h: 0.55, fontSize: 28, bold: true, color, align: "center", fontFace: F.title });
  if (unit) slide.addText(unit, { x: x+0.1, y: y+0.62, w: w-0.2, h: 0.22, fontSize: 10, color: C.mid, align: "center", fontFace: F.body });
  slide.addText(label, { x: x+0.1, y: y+0.82, w: w-0.2, h: 0.22, fontSize: 11, color: C.mid, align: "center", fontFace: F.body });
}

// ═══════════════════════════════════════════════
// 封面
// ═══════════════════════════════════════════════
const s1 = pptx.addSlide();
s1.background = { color: C.primary };
// 右侧装饰大圆
s1.addShape(pptx.ShapeType.ellipse, { x: 7.0, y: -1.0, w: 4.5, h: 4.5, fill: { color: "223472" }, line: { color: "223472" } });
s1.addShape(pptx.ShapeType.ellipse, { x: 8.2, y: 3.5, w: 2.8, h: 2.8, fill: { color: "162350" }, line: { color: "162350" } });
// 左上标签
tagBox(s1, 0.5, 0.45, 1.6, "私域增长方案", C.accent, C.white);
// 主标题
s1.addText("蒙牛营养生活家", { x: 0.5, y: 1.1, w: 8, h: 0.85, fontSize: 40, bold: true, color: C.white, fontFace: F.title });
s1.addText("私域运营全场景规划", { x: 0.5, y: 1.9, w: 8, h: 0.65, fontSize: 30, bold: false, color: "#A0C4FF", fontFace: F.title });
// 摘要
s1.addShape(pptx.ShapeType.rect, { x: 0.5, y: 2.85, w: 5.8, h: 0.02, fill: { color: C.accent }, line: { color: C.accent } });
s1.addText("基于蒙牛现有「扫码加企微→营养生活家小程序→超级会员」\n体系，构建消费者全生命周期私域运营闭环", {
  x: 0.5, y: 3.0, w: 5.8, h: 0.9,
  fontSize: 13, color: "#A0B4D8", fontFace: F.body, lineSpacing: 22
});
// 核心指标预览
const previewItems = [
  { val: "1000万+", lab: "私域用户目标" },
  { val: "45%↑", lab: "复购率提升" },
  { val: "ROI 1:5", lab: "私域投入产出" },
  { val: "12个月", lab: "落地周期" },
];
previewItems.forEach((item, i) => {
  const x = 0.5 + i * 2.3;
  s1.addShape(pptx.ShapeType.rect, { x, y: 4.2, w: 2.1, h: 1.0, fill: { color: "243672" }, line: { color: "2D4A8A" } });
  s1.addText(item.val, { x, y: 4.3, w: 2.1, h: 0.45, fontSize: 20, bold: true, color: C.accent, align: "center", fontFace: F.title });
  s1.addText(item.lab, { x, y: 4.75, w: 2.1, h: 0.3, fontSize: 11, color: "#7090C0", align: "center", fontFace: F.body });
});
// 日期版本
s1.addText("2026年 · Somn超级智能体", { x: 0.5, y: 5.55, w: 9, h: 0.3, fontSize: 11, color: "#5070A0", align: "center", fontFace: F.body });

// ═══════════════════════════════════════════════
// 目录
// ═══════════════════════════════════════════════
const s2 = pptx.addSlide();
s2.background = { color: C.bg };
s2.addText("目 录", { x: 0.5, y: 0.35, w: 9, h: 0.55, fontSize: 26, bold: true, color: C.primary, fontFace: F.title });
s2.addText("CONTENTS", { x: 0.5, y: 0.9, w: 9, h: 0.3, fontSize: 12, color: C.light, fontFace: F.body });
hLine(s2, 1.2, C.border);

const chapters = [
  { n:"01", t:"现状诊断与战略定位", d:"私域现状·行业基准·战略机会" },
  { n:"02", t:"目标用户深度画像",   d:"四大人群·消费行为·需求洞察" },
  { n:"03", t:"全场景运营体系",      d:"五大场景闭环·触点矩阵·流量路径" },
  { n:"04", t:"私域运营四大引擎",    d:"引流·激活·留存·转化" },
  { n:"05", t:"技术与工具支撑",      d:"企微+小程序+SCRM+数据中台" },
  { n:"06", t:"KPI体系与预期效益",   d:"核心指标·ROI测算·效果预测" },
  { n:"07", t:"12个月实施路线图",    d:"四阶段·里程碑·资源配置" },
];

chapters.forEach((ch, i) => {
  const y = 1.5 + i * 0.6;
  const isEven = i % 2 === 0;
  s2.addShape(pptx.ShapeType.rect, { x: 0.5, y: y - 0.02, w: 9, h: 0.52, fill: { color: isEven ? C.white : C.bg }, line: { color: C.border, width: 0.5 } });
  s2.addShape(pptx.ShapeType.rect, { x: 0.5, y: y - 0.02, w: 0.04, h: 0.52, fill: { color: C.accent }, line: { color: C.accent } });
  s2.addText(ch.n, { x: 0.62, y, w: 0.45, h: 0.35, fontSize: 16, bold: true, color: C.accent, fontFace: F.title });
  s2.addText(ch.t, { x: 1.12, y, w: 4.5, h: 0.35, fontSize: 15, bold: true, color: C.dark, fontFace: F.title });
  s2.addText(ch.d, { x: 1.12, y: y + 0.32, w: 6, h: 0.2, fontSize: 10, color: C.light, fontFace: F.body });
  s2.addText(` ${i + 1} `, { x: 8.9, y, w: 0.6, h: 0.35, fontSize: 12, color: C.light, align: "right", fontFace: F.body });
});

// ═══════════════════════════════════════════════
// 01 现状诊断与战略定位
// ═══════════════════════════════════════════════
const s3 = pptx.addSlide();
s3.background = { color: C.bg };
sectionTitle(s3, 1, "现状诊断与战略定位", "蒙牛营养生活家私域体系已打通，但增长潜力尚未充分释放");

// 左：现有私域成果（真实数据）
cardRect(s3, 0.4, 1.25, 4.4, 3.3, C.teal);
s3.addShape(pptx.ShapeType.rect, { x: 0.4, y: 1.25, w: 4.4, h: 0.06, fill: { color: C.teal }, line: { color: C.teal } });
s3.addText("✅  蒙牛现有私域基础", { x: 0.55, y: 1.38, w: 4.1, h: 0.35, fontSize: 14, bold: true, color: C.teal, fontFace: F.title });
const existingItems = [
  "纯甄私域3个月拉新6万+用户",
  "建立132个企微社群，GMV 37万+",
  "营养生活家小程序累计24万+注册",
  "「扫码加企微→社群→小程序」全链路",
  "超级会员体系：积分/等级/任务/勋章",
  "米多数据引擎：标签同步+精准引流",
];
existingItems.forEach((item, i) => {
  s3.addShape(pptx.ShapeType.ellipse, { x: 0.58, y: 1.9 + i * 0.4, w: 0.16, h: 0.16, fill: { color: C.teal }, line: { color: C.teal } });
  s3.addText(item, { x: 0.82, y: 1.85 + i * 0.4, w: 3.8, h: 0.32, fontSize: 12, color: C.dark, fontFace: F.body });
});

// 右：现存痛点
cardRect(s3, 5.0, 1.25, 4.4, 3.3, C.orange);
s3.addShape(pptx.ShapeType.rect, { x: 5.0, y: 1.25, w: 4.4, h: 0.06, fill: { color: C.orange }, line: { color: C.orange } });
s3.addText("⚠️  核心痛点与增长瓶颈", { x: 5.15, y: 1.38, w: 4.1, h: 0.35, fontSize: 14, bold: true, color: C.orange, fontFace: F.title });
const painItems = [
  { pain: "转化链路断裂", desc: "扫码无即时奖励，转化率低" },
  { pain: "场景覆盖不足", desc: "仅包装引流，线下场景缺失" },
  { pain: "内容运营薄弱", desc: "社群内容以UGC为主，质量参差" },
  { pain: "用户分层不精准", desc: "标签体系不完整，千人千面不足" },
  { pain: "数据孤岛", desc: "线上线下数据未打通，决策滞后" },
];
painItems.forEach((item, i) => {
  s3.addText(`▶  ${item.pain}`, { x: 5.15, y: 1.9 + i * 0.42, w: 4.1, h: 0.2, fontSize: 12, bold: true, color: C.orange, fontFace: F.body });
  s3.addText(item.desc, { x: 5.35, y: 2.08 + i * 0.42, w: 3.9, h: 0.18, fontSize: 10.5, color: C.mid, fontFace: F.body });
});

// 底部：行业基准
s3.addShape(pptx.ShapeType.rect, { x: 0.4, y: 4.68, w: 9, h: 0.02, fill: { color: C.border }, line: { color: C.border } });
s3.addText("行业基准参照 ·", { x: 0.4, y: 4.76, w: 1.5, h: 0.25, fontSize: 10.5, bold: true, color: C.mid, fontFace: F.body });
const benchmarks = [
  "头部FMCG私域ROI可达 1:5～1:8",
  "私域会员复购率比公域高 25%～35%",
  "精细化运营可将LTV提升 2倍",
  "企微生态覆盖用户 8.3亿（2025）",
];
benchmarks.forEach((b, i) => {
  s3.addText(`  ${b}`, { x: 1.9 + i * 2.12, y: 4.76, w: 2.1, h: 0.25, fontSize: 10, color: C.light, fontFace: F.body });
});

// ═══════════════════════════════════════════════
// 02 目标用户深度画像
// ═══════════════════════════════════════════════
const s4 = pptx.addSlide();
s4.background = { color: C.bg };
sectionTitle(s4, 2, "目标用户深度画像", "四类核心人群 · 差异化需求 · 精准运营策略");

const personas = [
  {
    tag:"健康宝妈",       icon:"👩‍👧", pct:"35%",  color: C.accent,
    age:"25~38岁",        city:"一二线城市",
    need:"关注儿童发育营养，重视产品安全认证，愿意为健康溢价",
    pain:"信息繁杂真假难辨，优质内容和专业建议严重稀缺",
    channel:"小红书种草→企微社群→小程序订购",
    ltv:"高，周期购比例高，客单价200～400元/月",
  },
  {
    tag:"都市健康白领",  icon:"💼", pct:"28%",  color: C.teal,
    age:"25~40岁",        city:"一线城市",
    need:"便捷健康补给，乳糖不耐/功能型产品，快速决策",
    pain:"时间碎片化，对繁琐操作容忍度低，会员权益复杂",
    channel:"抖音内容→小程序下单→企微专属服务",
    ltv:"中高，客单价150～300元/月",
  },
  {
    tag:"营养关怀银发族", icon:"👴", pct:"22%",  color: C.gold,
    age:"55岁以上",        city:"全国下沉城市",
    need:"关节/骨密度/血糖管理，需要功能型乳制品+知识陪伴",
    pain:"操作难度高，子女决策代入强，线上购物信任度低",
    channel:"子女推荐→线下扫码→企微1v1服务",
    ltv:"高，长期复购稳定，黏性强",
  },
  {
    tag:"运动健身人群",   icon:"🏋️", pct:"15%",  color: C.orange,
    age:"20~35岁",        city:"一二线城市",
    need:"高蛋白/无糖/运动后恢复，社群归属感和专业背书",
    pain:"对营养成分要求高，传统乳品形象不符，需重建认知",
    channel:"B站/小红书KOL→私域会员→限量新品优先购",
    ltv:"中，但裂变能力强，KOC价值高",
  },
];

personas.forEach((p, i) => {
  const x = 0.4 + (i % 2) * 4.7;
  const y = 1.25 + Math.floor(i / 2) * 2.35;
  cardRect(s4, x, y, 4.5, 2.2, p.color);
  s4.addShape(pptx.ShapeType.rect, { x, y, w: 4.5, h: 0.06, fill: { color: p.color }, line: { color: p.color } });

  // 头部信息行
  s4.addText(`${p.icon}  ${p.tag}`, { x: x+0.15, y: y+0.12, w: 2.5, h: 0.35, fontSize: 14, bold: true, color: C.dark, fontFace: F.title });
  tagBox(s4, x+3.0, y+0.14, 1.3, `占比 ${p.pct}`, p.color, C.white);

  // 基础信息
  s4.addText(`📅 ${p.age}  📍 ${p.city}`, { x: x+0.15, y: y+0.53, w: 4.2, h: 0.22, fontSize: 10.5, color: C.mid, fontFace: F.body });

  // 三行核心信息
  const rows = [
    { icon: "💡", label: "核心需求", val: p.need },
    { icon: "😤", label: "痛点",   val: p.pain },
    { icon: "📱", label: "路径",   val: p.channel },
  ];
  rows.forEach((row, ri) => {
    s4.addText(`${row.icon} ${row.label}`, { x: x+0.15, y: y+0.82 + ri*0.41, w: 1.0, h: 0.2, fontSize: 9.5, bold: true, color: p.color, fontFace: F.body });
    s4.addText(row.val, { x: x+1.15, y: y+0.82 + ri*0.41, w: 3.2, h: 0.22, fontSize: 10, color: C.mid, fontFace: F.body });
  });
  // LTV
  s4.addShape(pptx.ShapeType.rect, { x: x+0.15, y: y+2.03, w: 4.2, h: 0.01, fill: { color: C.border }, line: { color: C.border } });
  s4.addText(`💰 LTV：${p.ltv}`, { x: x+0.15, y: y+2.05, w: 4.2, h: 0.15, fontSize: 9.5, color: p.color, fontFace: F.body });
});

// ═══════════════════════════════════════════════
// 03 全场景运营体系
// ═══════════════════════════════════════════════
const s5 = pptx.addSlide();
s5.background = { color: C.bg };
sectionTitle(s5, 3, "全场景运营体系", "五大场景闭环 · 触点矩阵 · 消费者全旅程");

// 中央流程图（线性）
const scenes = [
  { label: "公域曝光", sub: "抖音/小红书/微信广告", color: C.light, bg: "#E8E8E8" },
  { label: "扫码引流", sub: "包装码/货架码/门店码", color: C.accent, bg: "#DBEAFE" },
  { label: "私域沉淀", sub: "企微好友+营养生活家社群", color: C.teal, bg: "#D1FAF5" },
  { label: "服务激活", sub: "1v1营养顾问+小程序体验", color: C.gold, bg: "#FEF3C7" },
  { label: "复购裂变", sub: "周期购+会员权益+口碑传播", color: C.green, bg: "#D1FAE5" },
];

scenes.forEach((scene, i) => {
  const x = 0.35 + i * 1.88;
  const y = 1.35;
  // 主框
  s5.addShape(pptx.ShapeType.roundRect, { x, y, w: 1.75, h: 0.95, rectRadius: 0.1, fill: { color: scene.bg }, line: { color: scene.color, width: 2 } });
  s5.addText(scene.label, { x, y: y+0.1, w: 1.75, h: 0.38, fontSize: 14, bold: true, color: scene.color === C.light ? C.mid : scene.color, align: "center", fontFace: F.title });
  s5.addText(scene.sub, { x, y: y+0.50, w: 1.75, h: 0.35, fontSize: 9, color: C.mid, align: "center", fontFace: F.body, lineSpacing: 16 });
  // 箭头
  if (i < scenes.length - 1) {
    s5.addShape(pptx.ShapeType.line, { x: x+1.75, y: y+0.47, w: 0.13, h: 0, line: { color: C.border, width: 2, endArrowType: "open" } });
  }
});

// 5大场景详情卡
const sceneDetails = [
  {
    title: "消费场景",  icon:"🛒",  color: C.accent,
    items: ["电商平台大促联动","线下商超扫码入会","会员日专属折扣","周期购免费配送"],
  },
  {
    title: "内容场景",  icon:"📱",  color: "#722ED1",
    items: ["营养知识科普推文","配方师直播答疑","食谱/搭配分享","AI个性化营养方案"],
  },
  {
    title: "服务场景",  icon:"🎯",  color: C.teal,
    items: ["企微1v1营养顾问","产品定制化选购","售后快速响应","孕期/育儿专属服务"],
  },
  {
    title: "社交场景",  icon:"👥",  color: C.gold,
    items: ["家庭社区UGC打卡","KOC口碑裂变","老带新积分奖励","节日社群互动活动"],
  },
  {
    title: "数据场景",  icon:"📊",  color: C.orange,
    items: ["用户行为标签化","复购预测模型","沉睡唤醒自动化","ROI效果实时看板"],
  },
];

sceneDetails.forEach((sc, i) => {
  const x = 0.35 + i * 1.88;
  const y = 2.55;
  cardRect(s5, x, y, 1.75, 3.1, sc.color);
  s5.addShape(pptx.ShapeType.rect, { x, y, w: 1.75, h: 0.06, fill: { color: sc.color }, line: { color: sc.color } });
  s5.addText(`${sc.icon} ${sc.title}`, { x: x+0.06, y: y+0.12, w: 1.65, h: 0.32, fontSize: 13, bold: true, color: sc.color, fontFace: F.title });
  sc.items.forEach((item, j) => {
    s5.addShape(pptx.ShapeType.ellipse, { x: x+0.1, y: y+0.56 + j*0.57, w: 0.1, h: 0.1, fill: { color: sc.color }, line: { color: sc.color } });
    s5.addText(item, { x: x+0.24, y: y+0.52 + j*0.57, w: 1.44, h: 0.3, fontSize: 10.5, color: C.dark, fontFace: F.body });
  });
});

// ═══════════════════════════════════════════════
// 04 私域运营四大引擎
// ═══════════════════════════════════════════════
const s6 = pptx.addSlide();
s6.background = { color: C.bg };
sectionTitle(s6, 4, "私域运营四大引擎", "引流 · 激活 · 留存 · 转化 · 完整AARRR私域飞轮");

const engines = [
  {
    name: "引流引擎", phase:"ACQUIRE", color: C.accent, icon:"🔗",
    target: "年新增私域用户500万",
    tactics: [
      { t:"包装扫码+即时奖励", d:"产品二维码扫码即领红包/积分，降低加企微门槛" },
      { t:"KOL/KOC内容引流",   d:"小红书、抖音达人测评植入企微入口" },
      { t:"线下场景覆盖",       d:"商超导购员二维码、餐饮渠道联动" },
      { t:"老带新裂变",         d:"邀请1位好友入群奖励30元券，上限3人" },
    ]
  },
  {
    name: "激活引擎", phase:"ACTIVATE", color: C.teal, icon:"⚡",
    target: "新用户7日激活率 > 60%",
    tactics: [
      { t:"新人7天陪伴SOP",     d:"D1欢迎礼→D3营养测评→D5新品试用→D7首购优惠" },
      { t:"营养档案建立",       d:"引导填写家庭成员/营养需求，完成即解锁专属推荐" },
      { t:"首单专属福利包",     d:"积分×3倍+赠品+专属客服，消除首购顾虑" },
      { t:"限量体验装领取",     d:"完成企微互动解锁1元购体验装，制造惊喜感" },
    ]
  },
  {
    name: "留存引擎", phase:"RETAIN", color: C.gold, icon:"🔒",
    target: "30日留存率 > 55%",
    tactics: [
      { t:"超级会员积分体系",   d:"购买/分享/打卡均可积分，兑换实物/权益/无门槛券" },
      { t:"内容栏目固定化",     d:"周二营养课堂·周五食谱·月度KOL直播" },
      { t:"生命周期关怀SOP",   d:"生日礼/孕期陪伴/儿童入学等节点定向推送" },
      { t:"沉睡唤醒自动化",     d:"30天未购推专属券→60天电话回访→90天流失预警" },
    ]
  },
  {
    name: "转化引擎", phase:"REVENUE", color: C.orange, icon:"💰",
    target: "私域GMV年增40%+",
    tactics: [
      { t:"周期购订阅引导",     d:"首次下单页弹出周期购优惠，锁定长期消费" },
      { t:"智能组合推荐",       d:"基于家庭画像推荐产品套餐，提升客单价25%+" },
      { t:"社群限时快闪",       d:"每周三社群专属秒杀，制造稀缺感和紧迫性" },
      { t:"复购预测+定向触达",  d:"AI预判复购时间窗，提前3天推送个性化提醒" },
    ]
  },
];

engines.forEach((eng, i) => {
  const x = 0.35 + (i % 2) * 4.7;
  const y = 1.25 + Math.floor(i / 2) * 2.55;
  cardRect(s6, x, y, 4.5, 2.4, eng.color);
  s6.addShape(pptx.ShapeType.rect, { x, y, w: 4.5, h: 0.06, fill: { color: eng.color }, line: { color: eng.color } });

  // 标题行
  s6.addText(`${eng.icon}  ${eng.name}`, { x: x+0.15, y: y+0.12, w: 2.5, h: 0.35, fontSize: 15, bold: true, color: eng.color, fontFace: F.title });
  tagBox(s6, x+3.15, y+0.14, 1.2, eng.target, eng.color, C.white);

  // 分隔
  s6.addShape(pptx.ShapeType.rect, { x: x+0.15, y: y+0.55, w: 4.2, h: 0.01, fill: { color: C.border }, line: { color: C.border } });

  // 战术列表
  eng.tactics.forEach((tac, j) => {
    s6.addText(`${tac.t}`, { x: x+0.2, y: y+0.65 + j*0.41, w: 1.7, h: 0.22, fontSize: 11, bold: true, color: C.dark, fontFace: F.body });
    s6.addText(tac.d, { x: x+1.95, y: y+0.65 + j*0.41, w: 2.45, h: 0.22, fontSize: 10, color: C.mid, fontFace: F.body });
  });
});

// ═══════════════════════════════════════════════
// 05 技术与工具支撑
// ═══════════════════════════════════════════════
const s7 = pptx.addSlide();
s7.background = { color: C.bg };
sectionTitle(s7, 5, "技术与工具支撑", "企业微信 + 营养生活家小程序 + SCRM + 数据中台");

// 架构层级图
const layers = [
  { label:"数据智能层",   desc:"数据中台·BI看板·复购预测·效果归因", color: C.primary, w: 8.8 },
  { label:"运营工具层",   desc:"SCRM系统（艾客/探马）·营销自动化SOP·标签体系·智能群发", color: "#1D4ED8", w: 8.0 },
  { label:"核心触点层",   desc:"企业微信 · 营养生活家小程序商城 · 超级会员中心", color: C.accent, w: 7.2 },
  { label:"流量入口层",   desc:"包装扫码 · 抖音/小红书内容 · 线下门店 · 电商平台", color: C.teal, w: 6.4 },
];

layers.forEach((layer, i) => {
  const y = 1.35 + i * 1.0;
  const x = (9.6 - layer.w) / 2;
  s7.addShape(pptx.ShapeType.roundRect, { x, y, w: layer.w, h: 0.82, rectRadius: 0.08, fill: { color: layer.color }, line: { color: layer.color } });
  s7.addText(layer.label, { x: x+0.2, y: y+0.05, w: 2.0, h: 0.35, fontSize: 13, bold: true, color: C.white, fontFace: F.title });
  s7.addText(layer.desc, { x: x+2.2, y: y+0.1, w: layer.w - 2.4, h: 0.6, fontSize: 11, color: "#C8D8F8", fontFace: F.body, valign: "middle" });
});

// 底部工具选型
s7.addText("推荐工具选型", { x: 0.4, y: 5.45, w: 2.0, h: 0.28, fontSize: 12, bold: true, color: C.mid, fontFace: F.title });
const tools = [
  { cat:"SCRM", name:"艾客SCRM / 探马SCRM" },
  { cat:"数据分析", name:"神策数据 / GrowingIO" },
  { cat:"营销自动化", name:"致趣百川MA / Linkflow" },
  { cat:"社群运营", name:"微盛·企微管家" },
  { cat:"内容分发", name:"腾讯广告 + 巨量引擎" },
];
tools.forEach((tool, i) => {
  s7.addShape(pptx.ShapeType.roundRect, { x: 0.4 + i * 1.88, y: 5.78, w: 1.75, h: 0.55, rectRadius: 0.06, fill: { color: C.white }, line: { color: C.border } });
  s7.addText(tool.cat, { x: 0.4 + i * 1.88, y: 5.82, w: 1.75, h: 0.2, fontSize: 9, bold: true, color: C.accent, align: "center", fontFace: F.body });
  s7.addText(tool.name, { x: 0.4 + i * 1.88, y: 6.02, w: 1.75, h: 0.22, fontSize: 8.5, color: C.mid, align: "center", fontFace: F.body });
});

// ═══════════════════════════════════════════════
// 06 KPI体系与预期效益
// ═══════════════════════════════════════════════
const s8 = pptx.addSlide();
s8.background = { color: C.bg };
sectionTitle(s8, 6, "KPI体系与预期效益", "基于行业基准测算 · 12个月分阶段达成");

// 顶部6个数据块
const kpiData = [
  { val:"1000万", unit:"用户", label:"私域累计用户", color: C.accent },
  { val:"45%",    unit:"↑",   label:"复购率提升",   color: C.teal },
  { val:"ROI 1:5",unit:"",    label:"私域投入产出比",color: C.gold },
  { val:"120元",  unit:"/月", label:"会员客单价",    color: C.orange },
  { val:"5亿+",   unit:"元/年",label:"私域贡献GMV",  color: C.primary },
  { val:"-30%",   unit:"",    label:"获客成本降低",  color: C.green },
];
kpiData.forEach((k, i) => {
  dataBlock(s8, 0.35 + i * 1.55, 1.25, 1.45, k.val, k.label, k.unit, k.color);
});

// 效果对比表
s8.addText("前后效果对比", { x: 0.4, y: 2.58, w: 3.0, h: 0.3, fontSize: 13, bold: true, color: C.dark, fontFace: F.title });
const compRows = [
  { metric:"触达成本",    before:"10元/人",   after:"3元/人",    delta:"-70%",  good: true },
  { metric:"转化率",      before:"2%",         after:"8%",         delta:"+300%", good: true },
  { metric:"复购周期",    before:"90天",       after:"45天",       delta:"-50%",  good: true },
  { metric:"月均客单价",  before:"80元",       after:"120元",      delta:"+50%",  good: true },
  { metric:"用户活跃率",  before:"5%",         after:"25%",        delta:"+400%", good: true },
  { metric:"私域占销售比",before:"<5%",        after:"30%+",       delta:"+600%", good: true },
];
// 表头
["指标", "现状", "目标", "变化"].forEach((h, i) => {
  const xs = [0.4, 2.2, 3.5, 4.8];
  s8.addShape(pptx.ShapeType.rect, { x: xs[i], y: 2.95, w: i === 0 ? 1.7 : 1.2, h: 0.3, fill: { color: C.primary }, line: { color: C.primary } });
  s8.addText(h, { x: xs[i], y: 2.95, w: i === 0 ? 1.7 : 1.2, h: 0.3, fontSize: 11, bold: true, color: C.white, align: "center", fontFace: F.body });
});
compRows.forEach((row, i) => {
  const y = 3.28 + i * 0.35;
  const bg = i % 2 === 0 ? C.white : C.bg;
  s8.addShape(pptx.ShapeType.rect, { x: 0.4, y, w: 5.8, h: 0.32, fill: { color: bg }, line: { color: C.border, width: 0.5 } });
  s8.addText(row.metric, { x: 0.5, y: y+0.04, w: 1.6, h: 0.24, fontSize: 11, color: C.dark, fontFace: F.body });
  s8.addText(row.before, { x: 2.2, y: y+0.04, w: 1.2, h: 0.24, fontSize: 11, color: C.mid, align: "center", fontFace: F.body });
  s8.addText(row.after,  { x: 3.5, y: y+0.04, w: 1.2, h: 0.24, fontSize: 11, bold: true, color: C.accent, align: "center", fontFace: F.body });
  s8.addText(row.delta,  { x: 4.8, y: y+0.04, w: 1.2, h: 0.24, fontSize: 11, bold: true, color: C.green, align: "center", fontFace: F.body });
});

// 右侧ROI测算
cardRect(s8, 6.25, 2.55, 3.15, 4.0, C.accent);
s8.addShape(pptx.ShapeType.rect, { x: 6.25, y: 2.55, w: 3.15, h: 0.06, fill: { color: C.accent }, line: { color: C.accent } });
s8.addText("💰 ROI测算示意", { x: 6.35, y: 2.65, w: 2.9, h: 0.35, fontSize: 13, bold: true, color: C.accent, fontFace: F.title });
const roiRows = [
  { k:"年私域运营投入",  v:"约1亿元" },
  { k:"私域GMV贡献",     v:"5亿+元" },
  { k:"ROI",             v:"1:5+" },
  { k:"每用户年贡献",    v:"50元/人" },
  { k:"会员LTV（2年）",  v:"约1200元" },
];
roiRows.forEach((r, i) => {
  s8.addText(r.k, { x: 6.35, y: 3.1 + i*0.55, w: 1.7, h: 0.25, fontSize: 11, color: C.mid, fontFace: F.body });
  s8.addText(r.v, { x: 8.0, y: 3.1 + i*0.55, w: 1.3, h: 0.25, fontSize: 13, bold: true, color: C.accent, align: "right", fontFace: F.title });
  if (i < roiRows.length - 1)
    s8.addShape(pptx.ShapeType.rect, { x: 6.35, y: 3.38 + i*0.55, w: 2.9, h: 0.01, fill: { color: C.border }, line: { color: C.border } });
});
s8.addText("*基于行业头部FMCG私域基准估算", { x: 6.25, y: 6.08, w: 3.15, h: 0.25, fontSize: 9, color: C.light, align: "center", fontFace: F.body });

// ═══════════════════════════════════════════════
// 07 12个月实施路线图
// ═══════════════════════════════════════════════
const s9 = pptx.addSlide();
s9.background = { color: C.bg };
sectionTitle(s9, 7, "12个月实施路线图", "四阶段分步落地 · 里程碑验收 · 可量化执行");

const phases = [
  {
    phase:"Phase 1",  period:"第1-3月",  title:"基础建设期",
    color: C.accent,
    milestone:"完成技术平台搭建，上线超级会员2.0",
    tasks:[
      "企微体系升级：IP人设+标签体系+SOP流程设计",
      "SCRM系统选型采购（艾客/探马）并完成对接",
      "营养生活家小程序2.0：周期购+会员体系+家庭档案",
      "全渠道扫码引流方案设计和物料制作",
      "团队人员招募：私域运营专员×4，内容创作×2",
    ],
    kpi:"企微日新增用户 ≥ 5000",
  },
  {
    phase:"Phase 2",  period:"第4-6月",  title:"引流激活期",
    color: C.teal,
    milestone:"私域用户突破200万，激活率≥60%",
    tasks:[
      "包装全系产品上线「扫码加企微+即时奖励」",
      "KOL矩阵搭建：50位腰部KOL+300位KOC签约",
      "新人7天陪伴SOP自动化上线",
      "小红书/抖音内容矩阵运营启动（日更3条）",
      "首轮大型私域引流活动「营养家庭季」",
    ],
    kpi:"月新增私域用户 ≥ 50万",
  },
  {
    phase:"Phase 3",  period:"第7-9月",  title:"运营深化期",
    color: C.gold,
    milestone:"会员活跃率≥25%，复购率突破35%",
    tasks:[
      "超级会员等级权益体系完善（4级：普通/成长/尊享/卓越）",
      "AI营养顾问功能上线，个性化推荐准确率≥75%",
      "社群运营精细化：每群配置1名专职运营+机器人辅助",
      "内容栏目固定化：周二营养课·周五食谱·月度直播",
      "数据中台上线：复购预测模型+流失预警自动化",
    ],
    kpi:"月GMV ≥ 3000万，复购率≥35%",
  },
  {
    phase:"Phase 4",  period:"第10-12月",  title:"规模扩张期",
    color: C.orange,
    milestone:"私域用户突破1000万，GMV贡献占线上30%",
    tasks:[
      "大区私域运营体系下沉：赋能全国500+城市导购员",
      "跨品牌联动：特仑苏/纯甄/妙可蓝多私域资产共享",
      "全年战役复盘：数据迭代+方法论沉淀+SOP升级",
      "2027年私域战略升级规划制定",
    ],
    kpi:"私域GMV全年≥5亿，用户NPS≥60",
  },
];

phases.forEach((ph, i) => {
  const y = 1.28 + i * 1.35;
  // 左侧标签
  s9.addShape(pptx.ShapeType.roundRect, { x: 0.35, y: y, w: 1.0, h: 1.15, rectRadius: 0.06, fill: { color: ph.color }, line: { color: ph.color } });
  s9.addText(ph.phase, { x: 0.35, y: y+0.06, w: 1.0, h: 0.25, fontSize: 11, bold: true, color: C.white, align: "center", fontFace: F.body });
  s9.addText(ph.period, { x: 0.35, y: y+0.32, w: 1.0, h: 0.25, fontSize: 11, color: "D0E8FF", align: "center", fontFace: F.body });
  s9.addText(ph.title, { x: 0.35, y: y+0.60, w: 1.0, h: 0.45, fontSize: 10.5, bold: true, color: C.white, align: "center", fontFace: F.body, lineSpacing: 16 });

  // 主卡
  cardRect(s9, 1.45, y, 8.1, 1.15, ph.color);
  // 里程碑行
  s9.addShape(pptx.ShapeType.rect, { x: 1.45, y, w: 8.1, h: 0.32, fill: { color: ph.color }, line: { color: ph.color } });
  s9.addText(`🏁  里程碑：${ph.milestone}`, { x: 1.55, y: y+0.04, w: 7.8, h: 0.24, fontSize: 11, bold: true, color: C.white, fontFace: F.body });

  // 任务列表 (2列)
  ph.tasks.forEach((task, j) => {
    const col = j < 3 ? 0 : 1;
    const row = j < 3 ? j : j - 3;
    const tx = 1.55 + col * 4.0;
    const ty = y + 0.38 + row * 0.24;
    s9.addShape(pptx.ShapeType.ellipse, { x: tx, y: ty+0.06, w: 0.1, h: 0.1, fill: { color: ph.color }, line: { color: ph.color } });
    s9.addText(task, { x: tx+0.14, y: ty+0.02, w: 3.7, h: 0.22, fontSize: 9.5, color: C.mid, fontFace: F.body });
  });

  // KPI标签
  tagBox(s9, 7.75, y + 0.38, 1.7, `▶ ${ph.kpi}`, ph.color, C.white);
});

// ═══════════════════════════════════════════════
// 结尾
// ═══════════════════════════════════════════════
const s10 = pptx.addSlide();
s10.background = { color: C.primary };
s10.addShape(pptx.ShapeType.ellipse, { x: -1, y: -1, w: 5, h: 5, fill: { color: "162350" }, line: { color: "162350" } });
s10.addShape(pptx.ShapeType.ellipse, { x: 7.5, y: 3.5, w: 3.5, h: 3.5, fill: { color: "223472" }, line: { color: "223472" } });

s10.addText("三步启动私域增长飞轮", { x: 0.8, y: 1.0, w: 8.4, h: 0.6, fontSize: 28, bold: true, color: C.white, align: "center", fontFace: F.title });

const actions = [
  { step:"第一步", action:"选定SCRM工具 + 重构企微IP人设", time:"第1个月完成", color: C.accent },
  { step:"第二步", action:"全品包装换新 + 扫码即奖励机制上线",  time:"第2个月完成", color: C.teal },
  { step:"第三步", action:"KOL矩阵签约 + 超级会员2.0发布",  time:"第3个月完成", color: C.gold },
];
actions.forEach((a, i) => {
  s10.addShape(pptx.ShapeType.roundRect, { x: 0.8 + i * 3.0, y: 2.0, w: 2.8, h: 2.0, rectRadius: 0.1, fill: { color: "1E3570" }, line: { color: a.color, width: 2 } });
  s10.addText(a.step, { x: 0.8 + i * 3.0, y: 2.1, w: 2.8, h: 0.35, fontSize: 13, bold: true, color: a.color, align: "center", fontFace: F.title });
  s10.addText(a.action, { x: 0.9 + i * 3.0, y: 2.52, w: 2.6, h: 0.7, fontSize: 12, color: C.white, align: "center", fontFace: F.body, lineSpacing: 22 });
  tagBox(s10, 0.9 + i * 3.0, 3.35, 2.6, a.time, a.color, C.white);
});

s10.addText("私域不是渠道，是品牌与消费者之间最有价值的长期关系资产。", {
  x: 0.8, y: 4.5, w: 8.4, h: 0.5,
  fontSize: 14, italic: true, color: "#7090C0", align: "center", fontFace: F.body
});
s10.addText("THANK YOU · Somn超级智能体 · 2026", {
  x: 0.8, y: 6.0, w: 8.4, h: 0.3,
  fontSize: 11, color: "#3A5080", align: "center", fontFace: F.body
});

// ─── 保存 ───
pptx.writeFile({ fileName: "蒙牛营养生活家私域运营方案v2.pptx" })
  .then(() => console.log("✅ PPT生成成功: 蒙牛营养生活家私域运营方案v2.pptx"))
  .catch(e => console.error("❌ 生成失败:", e));

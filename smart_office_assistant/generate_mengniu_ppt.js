const pptxgenjs = require("pptxgenjs");

const pptx = new pptxgenjs();

// 配色方案：基于蒙牛品牌色 + 营养健康主题
const colors = {
  primary: '#1E90FF',      // 蒙牛蓝
  secondary: '#0066CC',    // 深蓝
  accent: '#FF6B35',       // 活力橙
  light: '#E8F4FD',        // 浅蓝背景
  white: '#FFFFFF',
  dark: '#1A1A2E',         // 深色文字
  green: '#28A745',        // 健康
  gold: '#FFD700'          // 尊贵
};

// 全局设置
pptx.layout = 'LAYOUT_16x9';
pptx.defineSlideMaster({
  title: 'MASTER_SLIDE',
  background: { color: colors.white },
  objects: [
    { rect: { x: 0, y: 0, w: '100%', h: 0.15, fill: { color: colors.primary } } },
    { rect: { x: 0, y: 6.85, w: '100%', h: 0.15, fill: { color: colors.primary } } }
  ]
});

// ========== 封面页 ==========
const slide1 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
slide1.background = { color: colors.primary };
slide1.addText('蒙牛营养生活家', { x: 0.5, y: 1.5, w: '90%', h: 1, fontSize: 48, bold: true, color: colors.white, align: 'center' });
slide1.addText('私域运营全场景规划方案', { x: 0.5, y: 2.5, w: '90%', h: 0.6, fontSize: 32, color: colors.light, align: 'center' });
slide1.addText('2026年', { x: 0.5, y: 5.5, w: '90%', h: 0.5, fontSize: 20, color: colors.light, align: 'center' });

// ========== 目录页 ==========
const slide2 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
slide2.addText('目录', { x: 0.5, y: 0.5, w: '90%', h: 0.6, fontSize: 40, bold: true, color: colors.dark });

const contents = [
  '01 项目背景与目标',
  '02 用户画像分析',
  '03 全场景运营规划',
  '04 运营策略与执行',
  '05 技术支撑与工具',
  '06 预期效果与KPI',
  '07 实施路线图'
];

contents.forEach((item, index) => {
  slide2.addText(item, {
    x: 1.5,
    y: 1.5 + index * 0.6,
    w: '80%',
    h: 0.5,
    fontSize: 22,
    color: colors.dark
  });
});

// ========== 01 项目背景 ==========
const slide3 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
slide3.addText('01 项目背景与目标', { x: 0.5, y: 0.5, w: '90%', h: 0.6, fontSize: 36, bold: true, color: colors.dark });

// 背景卡片
slide3.addShape(pptx.ShapeType.rect, { x: 0.5, y: 1.3, w: 4.3, h: 2.4, fill: { color: colors.light }, line: { color: colors.primary, width: 2 } });
slide3.addText('市场环境', { x: 0.6, y: 1.4, w: 4.1, h: 0.4, fontSize: 20, bold: true, color: colors.primary });
slide3.addText('• 奶制品行业竞争加剧\n• 消费者健康意识提升\n• 数字化转型加速\n• 私域成为标配', { x: 0.6, y: 1.8, w: 4.1, h: 1.6, fontSize: 15, color: colors.dark, lineSpacing: 28 });

// 目标卡片
slide3.addShape(pptx.ShapeType.rect, { x: 5.1, y: 1.3, w: 4.3, h: 2.4, fill: { color: colors.light }, line: { color: colors.accent, width: 2 } });
slide3.addText('核心目标', { x: 5.2, y: 1.4, w: 4.1, h: 0.4, fontSize: 20, bold: true, color: colors.accent });
slide3.addText('• 构建千万级私域流量池\n• 提升用户LTV 30%+\n• 降低CAC 25%+\n• 品牌忠诚度提升', { x: 5.2, y: 1.8, w: 4.1, h: 1.6, fontSize: 15, color: colors.dark, lineSpacing: 28 });

// 关键数据
const keyMetrics = [
  { label: '目标用户数', value: '1000万+', color: colors.primary },
  { label: '年增GMV', value: '5亿+', color: colors.green },
  { label: '复购率提升', value: '40%+', color: colors.accent },
  { label: '私域占比', value: '30%+', color: colors.secondary }
];

keyMetrics.forEach((metric, i) => {
  const x = 0.5 + i * 2.3;
  slide3.addShape(pptx.ShapeType.rect, { x: x, y: 4.2, w: 2.1, h: 1.8, fill: { color: colors.light }, line: { color: metric.color, width: 3 } });
  slide3.addText(metric.value, { x: x + 0.1, y: 4.4, w: 1.9, h: 0.8, fontSize: 32, bold: true, color: metric.color, align: 'center' });
  slide3.addText(metric.label, { x: x + 0.1, y: 5.2, w: 1.9, h: 0.5, fontSize: 14, color: colors.dark, align: 'center' });
});

// ========== 02 用户画像 ==========
const slide4 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
slide4.addText('02 用户画像分析', { x: 0.5, y: 0.5, w: '90%', h: 0.6, fontSize: 36, bold: true, color: colors.dark });

const userSegments = [
  { name: '健康宝妈', age: '25-35', percent: '35%', needs: '儿童营养、安全放心', icon: '👶' },
  { name: '都市白领', age: '28-40', percent: '30%', needs: '便捷营养、健康管理', icon: '💼' },
  { name: '银发健康', age: '55+', percent: '20%', needs: '营养补充、健康关怀', icon: '👴' },
  { name: '运动健身', age: '20-35', percent: '15%', needs: '蛋白补充、运动营养', icon: '💪' }
];

userSegments.forEach((seg, i) => {
  const x = 0.5 + (i % 2) * 4.7;
  const y = 1.5 + Math.floor(i / 2) * 2.3;

  slide4.addShape(pptx.ShapeType.rect, { x: x, y: y, w: 4.5, h: 2.1, fill: { color: colors.light }, line: { color: colors.primary, width: 2 } });
  slide4.addText(`${seg.icon} ${seg.name}`, { x: x + 0.2, y: y + 0.15, w: 4.1, h: 0.4, fontSize: 18, bold: true, color: colors.dark });
  slide4.addText(`年龄: ${seg.age}  占比: ${seg.percent}\n需求: ${seg.needs}`, { x: x + 0.2, y: y + 0.55, w: 4.1, h: 1.3, fontSize: 14, color: colors.dark, lineSpacing: 26 });
});

// ========== 03 全场景规划 ==========
const slide5 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
slide5.addText('03 全场景运营规划', { x: 0.5, y: 0.5, w: '90%', h: 0.6, fontSize: 36, bold: true, color: colors.dark });

// 流程图 - 从左到右
const scenarios = ['消费场景', '服务场景', '社交场景', '内容场景', '数据场景'];
const positions = [
  { x: 0.5, y: 2.5 },
  { x: 2.4, y: 2.5 },
  { x: 4.3, y: 2.5 },
  { x: 6.2, y: 2.5 },
  { x: 8.1, y: 2.5 }
];

scenarios.forEach((scene, i) => {
  // 圆形节点
  slide5.addShape(pptx.ShapeType.ellipse, { x: positions[i].x, y: positions[i].y, w: 1.6, h: 1.6, fill: { color: colors.primary }, line: { color: colors.secondary, width: 3 } });
  slide5.addText(scene, { x: positions[i].x, y: positions[i].y + 0.5, w: 1.6, h: 0.6, fontSize: 16, bold: true, color: colors.white, align: 'center' });

  // 连接线
  if (i < scenarios.length - 1) {
    slide5.addShape(pptx.ShapeType.line, {
      x: positions[i].x + 1.6,
      y: positions[i].y + 0.8,
      w: 0.2,
      h: 0,
      line: { color: colors.secondary, width: 4, endArrowType: 'arrow' }
    });
  }

  // 下方说明
  const descriptions = [
    '电商平台\n线下门店\n扫码引流',
    '营养咨询\n产品定制\n健康服务',
    '社群运营\nKOL合作\n用户裂变',
    '短视频\n直播带货\n知识科普',
    '用户画像\n行为分析\n效果优化'
  ];
  slide5.addShape(pptx.ShapeType.rect, { x: positions[i].x - 0.1, y: 4.5, w: 1.8, h: 1.4, fill: { color: colors.light }, line: { color: colors.primary, width: 1 } });
  slide5.addText(descriptions[i], { x: positions[i].x, y: 4.6, w: 1.6, h: 1.2, fontSize: 11, color: colors.dark, align: 'center', lineSpacing: 20 });
});

// ========== 04 运营策略 ==========
const slide6 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
slide6.addText('04 运营策略与执行', { x: 0.5, y: 0.5, w: '90%', h: 0.6, fontSize: 36, bold: true, color: colors.dark });

const strategies = [
  { title: '引流策略', items: ['产品包装二维码', '会员扫码领券', '社群裂变活动', 'KOL带货引流'], color: colors.primary },
  { title: '激活策略', items: ['新人专属礼包', '首单优惠', '7天陪伴计划', '营养知识推送'], color: colors.green },
  { title: '留存策略', items: ['会员积分体系', '专属福利日', '生日关怀', '定期健康评测'], color: colors.accent },
  { title: '转化策略', items: ['精准产品推荐', '节日促销', '套餐组合', '限时抢购'], color: colors.secondary }
];

strategies.forEach((strat, i) => {
  const x = 0.5 + (i % 2) * 4.7;
  const y = 1.5 + Math.floor(i / 2) * 2.3;

  slide6.addShape(pptx.ShapeType.rect, { x: x, y: y, w: 4.5, h: 2.1, fill: { color: colors.light }, line: { color: strat.color, width: 3 } });
  slide6.addText(strat.title, { x: x + 0.2, y: y + 0.15, w: 4.1, h: 0.4, fontSize: 18, bold: true, color: strat.color });
  strat.items.forEach((item, j) => {
    slide6.addText(`• ${item}`, { x: x + 0.2, y: y + 0.6 + j * 0.35, w: 4.1, h: 0.3, fontSize: 13, color: colors.dark });
  });
});

// ========== 05 技术支撑 ==========
const slide7 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
slide7.addText('05 技术支撑与工具', { x: 0.5, y: 0.5, w: '90%', h: 0.6, fontSize: 36, bold: true, color: colors.dark });

const techStack = [
  { name: '企业微信', desc: '私域运营主阵地', features: ['客户管理', '社群运营', '标签体系', '营销自动化'] },
  { name: 'SCRM系统', desc: '私域运营核心工具', features: ['数据整合', '用户画像', '行为追踪', '智能推荐'] },
  { name: '小程序商城', desc: '转化核心渠道', features: ['商品展示', '在线购买', '会员中心', '积分商城'] },
  { name: '数据中台', desc: '数据驱动决策', features: ['数据采集', '实时分析', '效果追踪', 'BI看板'] }
];

techStack.forEach((tech, i) => {
  const x = 0.5 + (i % 2) * 4.7;
  const y = 1.5 + Math.floor(i / 2) * 2.2;

  slide7.addShape(pptx.ShapeType.rect, { x: x, y: y, w: 4.5, h: 2, fill: { color: colors.light }, line: { color: colors.primary, width: 2 } });
  slide7.addText(tech.name, { x: x + 0.2, y: y + 0.15, w: 4.1, h: 0.35, fontSize: 18, bold: true, color: colors.primary });
  slide7.addText(tech.desc, { x: x + 0.2, y: y + 0.5, w: 4.1, h: 0.3, fontSize: 13, italic: true, color: colors.dark });
  tech.features.forEach((feat, j) => {
    slide7.addText(`✓ ${feat}`, { x: x + 0.2, y: y + 0.85 + j * 0.3, w: 4.1, h: 0.25, fontSize: 13, color: colors.dark });
  });
});

// ========== 06 预期效果 ==========
const slide8 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
slide8.addText('06 预期效果与KPI', { x: 0.5, y: 0.5, w: '90%', h: 0.6, fontSize: 36, bold: true, color: colors.dark });

// 左侧：核心KPI
slide8.addShape(pptx.ShapeType.rect, { x: 0.5, y: 1.3, w: 4.5, h: 4.8, fill: { color: colors.light }, line: { color: colors.primary, width: 2 } });
slide8.addText('核心KPI指标', { x: 0.6, y: 1.4, w: 4.3, h: 0.4, fontSize: 20, bold: true, color: colors.primary });

const kpis = [
  { metric: '私域用户数', target: '1000万+', growth: '+300%' },
  { metric: '月活跃用户', target: '300万+', growth: '+200%' },
  { metric: '私域GMV', target: '5亿+/年', growth: '+400%' },
  { metric: '复购率', target: '45%+', growth: '+40%' },
  { metric: 'CAC', target: '降低25%', growth: '-25%' },
  { metric: 'LTV', target: '提升30%', growth: '+30%' }
];

kpis.forEach((kpi, i) => {
  slide8.addText(kpi.metric, { x: 0.6, y: 1.9 + i * 0.5, w: 1.5, h: 0.35, fontSize: 13, color: colors.dark });
  slide8.addText(kpi.target, { x: 2.2, y: 1.9 + i * 0.5, w: 1.5, h: 0.35, fontSize: 13, bold: true, color: colors.primary });
  slide8.addText(kpi.growth, { x: 3.8, y: 1.9 + i * 0.5, w: 1.0, h: 0.35, fontSize: 13, bold: true, color: colors.green });
});

// 右侧：效果对比
slide8.addShape(pptx.ShapeType.rect, { x: 5.2, y: 1.3, w: 4.2, h: 4.8, fill: { color: colors.light }, line: { color: colors.accent, width: 2 } });
slide8.addText('效果对比', { x: 5.3, y: 1.4, w: 4.0, h: 0.4, fontSize: 20, bold: true, color: colors.accent });

const comparisons = [
  { item: '触达成本', before: '10元', after: '3元' },
  { item: '转化率', before: '2%', after: '8%' },
  { item: '复购周期', before: '90天', after: '45天' },
  { item: '客单价', before: '80元', after: '120元' },
  { item: '用户活跃', before: '5%', after: '25%' },
  { item: '品牌忠诚', before: '60分', after: '85分' }
];

comparisons.forEach((comp, i) => {
  slide8.addText(comp.item, { x: 5.3, y: 1.9 + i * 0.5, w: 1.2, h: 0.35, fontSize: 13, color: colors.dark });
  slide8.addText(comp.before, { x: 6.6, y: 1.9 + i * 0.5, w: 0.8, h: 0.35, fontSize: 13, color: colors.dark });
  slide8.addText('→', { x: 7.5, y: 1.9 + i * 0.5, w: 0.3, h: 0.35, fontSize: 16, bold: true, color: colors.accent, align: 'center' });
  slide8.addText(comp.after, { x: 7.8, y: 1.9 + i * 0.5, w: 1.2, h: 0.35, fontSize: 13, bold: true, color: colors.green });
});

// ========== 07 实施路线图 ==========
const slide9 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
slide9.addText('07 实施路线图', { x: 0.5, y: 0.5, w: '90%', h: 0.6, fontSize: 36, bold: true, color: colors.dark });

const phases = [
  { title: '第一阶段：基础搭建', time: '1-3月', tasks: ['企微体系搭建', 'SCRM系统选型', '标签体系设计', '团队组建培训'] },
  { title: '第二阶段：引流激活', time: '4-6月', tasks: ['全渠道二维码部署', '会员引流活动', '新人礼包上线', '社群运营启动'] },
  { title: '第三阶段：运营深化', time: '7-9月', tasks: ['精细化运营', '会员体系完善', '内容营销升级', 'KOL合作深化'] },
  { title: '第四阶段：数据优化', time: '10-12月', tasks: ['数据中台上线', '效果分析优化', '策略迭代升级', '规模化复制'] }
];

phases.forEach((phase, i) => {
  const y = 1.5 + i * 1.4;

  // 时间标签
  slide9.addShape(pptx.ShapeType.rect, { x: 0.5, y: y, w: 1.5, h: 0.5, fill: { color: colors.primary } });
  slide9.addText(phase.time, { x: 0.5, y: y + 0.05, w: 1.5, h: 0.4, fontSize: 14, bold: true, color: colors.white, align: 'center' });

  // 阶段标题
  slide9.addShape(pptx.ShapeType.rect, { x: 2.1, y: y, w: 2.8, h: 0.5, fill: { color: colors.light }, line: { color: colors.primary, width: 2 } });
  slide9.addText(phase.title, { x: 2.2, y: y + 0.05, w: 2.6, h: 0.4, fontSize: 14, bold: true, color: colors.dark });

  // 任务列表
  phase.tasks.forEach((task, j) => {
    slide9.addText(`• ${task}`, { x: 5.1 + j * 1.6, y: y + 0.05, w: 1.5, h: 0.4, fontSize: 13, color: colors.dark });
  });
});

// ========== 结尾页 ==========
const slide10 = pptx.addSlide({ masterName: 'MASTER_SLIDE' });
slide10.background = { color: colors.primary };
slide10.addText('携手共进', { x: 0.5, y: 2.5, w: '90%', h: 0.6, fontSize: 40, bold: true, color: colors.white, align: 'center' });
slide10.addText('构建蒙牛营养生活家私域生态', { x: 0.5, y: 3.3, w: '90%', h: 0.5, fontSize: 28, color: colors.light, align: 'center' });
slide10.addText('THANK YOU', { x: 0.5, y: 5, w: '90%', h: 0.4, fontSize: 24, color: colors.gold, align: 'center' });

// 保存PPT
pptx.writeFile({ fileName: '蒙牛营养生活家私域运营方案.pptx' });

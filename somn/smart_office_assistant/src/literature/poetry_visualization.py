"""
__all__ = [
    'autolabel',
    'create_comprehensive_dashboard',
    'create_dynasty_comparison_chart',
    'create_geographic_distribution_chart',
    'create_style_comparison_chart',
    'create_theme_distribution_chart',
    'create_timeline_chart',
    'create_word_frequency_chart',
    'demo_visualization',
]

诗词可视化分析模块
基于唐诗宋词50大家深度学习研究项目成果开发
Version: 1.0.0
Created: 2026-04-02
"""

import json
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from collections import defaultdict, Counter

class VisualizationType(Enum):
    """可视化类型"""
    TIMELINE = "timeline"              # 时间轴
    NETWORK = "network"                # 网络图
    DISTRIBUTION = "distribution"      # 分布图
    COMPARISON = "comparison"          # 对比图
    HEATMAP = "heatmap"                # 热力图
    WORDCLOUD = "wordcloud"            # 词云
    GEOGRAPHIC = "geographic"          # 地理分布

class ChartStyle(Enum):
    """图表style"""
    CLASSICAL = "classical"        # 古典style
    MODERN = "modern"              # 现代style
    MINIMALIST = "minimalist"      # 极简style
    COLORFUL = "colorful"          # 多彩style

class PoetryVisualization:
    """诗词可视化分析系统"""
    
    def __init__(self, data_dir: str = None):
        """
        init可视化系统
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir or os.path.join("data", "visualization")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 颜色方案
        self.color_schemes = {
            ChartStyle.CLASSICAL: ["#8B4513", "#D2691E", "#CD853F", "#F4A460", "#DEB887"],
            ChartStyle.MODERN: ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD"],
            ChartStyle.MINIMALIST: ["#333333", "#666666", "#999999", "#CCCCCC", "#F0F0F0"],
            ChartStyle.COLORFUL: ["#FF6B6B", "#4ECDC4", "#FFD166", "#06D6A0", "#118AB2"]
        }
        
        # 基于唐诗宋词研究项目的示例数据
        self._load_sample_data()
    
    def _load_sample_data(self):
        """加载示例数据(基于50大家研究项目)"""
        # 唐代poet时间分布
        self.tang_poets_timeline = [
            {"name": "王勃", "birth": 650, "death": 676, "period": "初唐", "style": "初唐四杰"},
            {"name": "杨炯", "birth": 650, "death": 693, "period": "初唐", "style": "初唐四杰"},
            {"name": "卢照邻", "birth": 634, "death": 686, "period": "初唐", "style": "初唐四杰"},
            {"name": "骆宾王", "birth": 619, "death": 687, "period": "初唐", "style": "初唐四杰"},
            {"name": "陈子昂", "birth": 661, "death": 702, "period": "初唐", "style": "革新派"},
            {"name": "李白", "birth": 701, "death": 762, "period": "盛唐", "style": "浪漫主义"},
            {"name": "杜甫", "birth": 712, "death": 770, "period": "盛唐", "style": "现实主义"},
            {"name": "王维", "birth": 701, "death": 761, "period": "盛唐", "style": "山水田园"},
            {"name": "孟浩然", "birth": 689, "death": 740, "period": "盛唐", "style": "山水田园"},
            {"name": "高适", "birth": 704, "death": 765, "period": "盛唐", "style": "边塞诗派"},
            {"name": "岑参", "birth": 715, "death": 770, "period": "盛唐", "style": "边塞诗派"},
            {"name": "王昌龄", "birth": 698, "death": 756, "period": "盛唐", "style": "边塞诗派"},
            {"name": "白居易", "birth": 772, "death": 846, "period": "中唐", "style": "新乐府运动"},
            {"name": "元稹", "birth": 779, "death": 831, "period": "中唐", "style": "新乐府运动"},
            {"name": "韩愈", "birth": 768, "death": 824, "period": "中唐", "style": "古文运动"},
            {"name": "柳宗元", "birth": 773, "death": 819, "period": "中唐", "style": "古文运动"},
            {"name": "李贺", "birth": 790, "death": 816, "period": "中唐", "style": "诗鬼"},
            {"name": "李商隐", "birth": 813, "death": 858, "period": "晚唐", "style": "婉约派"},
            {"name": "杜牧", "birth": 803, "death": 852, "period": "晚唐", "style": "豪放派"},
            {"name": "温庭筠", "birth": 812, "death": 870, "period": "晚唐", "style": "花间派"}
        ]
        
        # 宋代poet时间分布
        self.song_poets_timeline = [
            {"name": "柳永", "birth": 984, "death": 1053, "period": "北宋前期", "style": "婉约派"},
            {"name": "范仲淹", "birth": 989, "death": 1052, "period": "北宋前期", "style": "豪放派"},
            {"name": "晏殊", "birth": 991, "death": 1055, "period": "北宋前期", "style": "婉约派"},
            {"name": "欧阳修", "birth": 1007, "death": 1072, "period": "北宋前期", "style": "婉约派"},
            {"name": "王安石", "birth": 1021, "death": 1086, "period": "北宋中期", "style": "豪放派"},
            {"name": "苏轼", "birth": 1037, "death": 1101, "period": "北宋中期", "style": "豪放派"},
            {"name": "黄庭坚", "birth": 1045, "death": 1105, "period": "北宋中期", "style": "江西诗派"},
            {"name": "秦观", "birth": 1049, "death": 1100, "period": "北宋中期", "style": "婉约派"},
            {"name": "周邦彦", "birth": 1056, "death": 1121, "period": "北宋后期", "style": "格律派"},
            {"name": "李清照", "birth": 1084, "death": 1155, "period": "两宋之交", "style": "婉约派"},
            {"name": "陆游", "birth": 1125, "death": 1210, "period": "南宋前期", "style": "爱国诗派"},
            {"name": "辛弃疾", "birth": 1140, "death": 1207, "period": "南宋前期", "style": "豪放派"},
            {"name": "杨万里", "birth": 1127, "death": 1206, "period": "南宋前期", "style": "诚斋体"},
            {"name": "范成大", "birth": 1126, "death": 1193, "period": "南宋前期", "style": "田园诗派"},
            {"name": "姜夔", "birth": 1155, "death": 1221, "period": "南宋中期", "style": "格律派"},
            {"name": "吴文英", "birth": 1200, "death": 1260, "period": "南宋后期", "style": "婉约派"},
            {"name": "张炎", "birth": 1248, "death": 1320, "period": "宋末元初", "style": "格律派"}
        ]
        
        # 诗词主题分布
        self.poetry_themes = {
            "李白": ["山水", "饮酒", "豪情", "离别", "思乡"],
            "杜甫": ["忧国", "民生", "战争", "思乡", "友情"],
            "王维": ["山水", "田园", "禅意", "隐居", "自然"],
            "白居易": ["民生", "讽喻", "爱情", "闲适", "感伤"],
            "苏轼": ["豪放", "哲理", "山水", "饮酒", "怀古"],
            "李清照": ["爱情", "离愁", "思乡", "悲秋", "咏物"],
            "辛弃疾": ["爱国", "豪放", "怀古", "壮志", "田园"]
        }
        
        # 诗词高频词统计
        self.word_frequencies = {
            "李白": {"山": 45, "月": 38, "酒": 32, "云": 28, "风": 25},
            "杜甫": {"人": 40, "生": 35, "国": 30, "家": 28, "民": 25},
            "王维": {"山": 50, "水": 42, "云": 35, "林": 30, "月": 28},
            "苏轼": {"江": 38, "山": 35, "月": 32, "酒": 30, "风": 25}
        }
    
    def create_timeline_chart(self, dynasty: str = "tang", style: ChartStyle = ChartStyle.CLASSICAL):
        """
        创建poet时间轴图
        
        Args:
            dynasty: 朝代(tang/song)
            style: 图表style
        """
        # 选择数据
        if dynasty == "tang":
            data = self.tang_poets_timeline
            title = "唐代poet时间分布"
        else:
            data = self.song_poets_timeline
            title = "宋代poet时间分布"
        
        # 创建图表
        plt.figure(figsize=(15, 8))
        colors = self.color_schemes[style]
        
        # 按时期分组
        periods = {}
        for poet in data:
            period = poet["period"]
            if period not in periods:
                periods[period] = []
            periods[period].append(poet)
        
        # 绘制时间轴
        y_pos = 0
        period_colors = {}
        
        for i, (period, poets) in enumerate(periods.items()):
            color = colors[i % len(colors)]
            period_colors[period] = color
            
            for poet in poets:
                # 绘制生命线
                lifespan = poet["death"] - poet["birth"]
                plt.plot([poet["birth"], poet["death"]], [y_pos, y_pos], 
                        color=color, linewidth=3, alpha=0.7)
                
                # 添加poet名字
                plt.text(poet["birth"] - 5, y_pos + 0.1, poet["name"], 
                        fontsize=9, ha='right', va='bottom')
                
                # 添加style标签
                plt.text(poet["death"] + 5, y_pos - 0.1, poet["style"], 
                        fontsize=8, color=color, alpha=0.7, va='top')
                
                y_pos += 1
        
        # 设置图表属性
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel("年份", fontsize=12)
        plt.ylabel("poet", fontsize=12)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # 添加图例
        legend_elements = []
        for period, color in period_colors.items():
            legend_elements.append(plt.Line2D([0], [0], color=color, lw=3, label=period))
        plt.legend(handles=legend_elements, loc='upper right')
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        filename = f"timeline_{dynasty}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.data_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        
        return filepath
    
    def create_theme_distribution_chart(self, author: str = None, style: ChartStyle = ChartStyle.MODERN):
        """
        创建诗词主题分布图
        
        Args:
            author: 作者名字
            style: 图表style
        """
        if author and author in self.poetry_themes:
            data = {author: self.poetry_themes[author]}
            title = f"{author}诗词主题分布"
        else:
            data = self.poetry_themes
            title = "主要poet诗词主题分布"
        
        # 创建图表
        fig, axes = plt.subplots(len(data), 1, figsize=(12, 4 * len(data)))
        if len(data) == 1:
            axes = [axes]
        
        colors = self.color_schemes[style]
        
        for idx, (author_name, themes) in enumerate(data.items()):
            ax = axes[idx]
            
            # 计算主题频率
            theme_counts = Counter(themes)
            themes_sorted = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
            
            labels = [item[0] for item in themes_sorted]
            values = [item[1] for item in themes_sorted]
            
            # 绘制条形图
            bars = ax.barh(labels, values, color=colors)
            
            # 添加数值标签
            for bar in bars:
                width = bar.get_width()
                ax.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                       f'{int(width)}', ha='left', va='center')
            
            ax.set_title(f"{author_name} - 主题分布", fontsize=14)
            ax.set_xlabel("出现次数", fontsize=10)
            ax.invert_yaxis()  # 数值大的在上方
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # 保存图表
        filename = f"theme_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.data_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        
        return filepath
    
    def create_word_frequency_chart(self, author: str, style: ChartStyle = ChartStyle.COLORFUL):
        """
        创建高频词分布图
        
        Args:
            author: 作者名字
            style: 图表style
        """
        if author not in self.word_frequencies:
            print(f"未找到作者 {author} 的数据")
            return None
        
        word_data = self.word_frequencies[author]
        
        # 排序数据
        sorted_words = sorted(word_data.items(), key=lambda x: x[1], reverse=True)
        words = [item[0] for item in sorted_words]
        frequencies = [item[1] for item in sorted_words]
        
        # 创建图表
        plt.figure(figsize=(12, 8))
        colors = self.color_schemes[style]
        
        # 创建彩虹色渐变
        color_map = cm.get_cmap('rainbow')
        bar_colors = [color_map(i / len(words)) for i in range(len(words))]
        
        # 绘制条形图
        bars = plt.bar(words, frequencies, color=bar_colors, edgecolor='black', linewidth=1)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        # 设置图表属性
        plt.title(f"{author}诗词高频词分析", fontsize=16, fontweight='bold')
        plt.xlabel("词语", fontsize=12)
        plt.ylabel("出现次数", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # 添加说明
        plt.figtext(0.5, 0.01, 
                   f"分析基于{author}的representative_works,共统计{len(words)}个高频词",
                   ha='center', fontsize=10, style='italic')
        
        plt.tight_layout()
        
        # 保存图表
        filename = f"word_frequency_{author}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.data_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        
        return filepath
    
    def create_style_comparison_chart(self, style: ChartStyle = ChartStyle.MODERN):
        """
        创建style对比图
        """
        # 统计不同style的poet数量
        style_counts = defaultdict(int)
        
        # 唐代poetstyle统计
        for poet in self.tang_poets_timeline:
            style_counts[poet["style"]] += 1
        
        # 宋代poetstyle统计
        for poet in self.song_poets_timeline:
            style_counts[poet["style"]] += 1
        
        # 筛选主要style
        main_styles = {}
        for style_name, count in style_counts.items():
            if count >= 2:  # 至少有2位poet
                main_styles[style_name] = count
        
        # 排序
        sorted_styles = sorted(main_styles.items(), key=lambda x: x[1], reverse=True)
        styles = [item[0] for item in sorted_styles]
        counts = [item[1] for item in sorted_styles]
        
        # 创建图表
        plt.figure(figsize=(14, 8))
        colors = self.color_schemes[style]
        
        # 创建子图
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)
        
        # 子图1:饼图
        wedges, texts, autotexts = ax1.pie(counts, labels=styles, autopct='%1.1f%%',
                                          colors=colors[:len(styles)], startangle=90)
        
        # 美化饼图文本
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax1.set_title("诗词style分布", fontsize=14, fontweight='bold')
        
        # 子图2:雷达图
        # 准备数据
        categories = styles
        N = len(categories)
        
        # 计算角度
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # 闭合
        
        # 准备数据
        values = counts
        values += values[:1]  # 闭合
        
        # 创建雷达图
        ax2 = plt.subplot(1, 2, 2, polar=True)
        ax2.plot(angles, values, 'o-', linewidth=2, color=colors[0])
        ax2.fill(angles, values, alpha=0.25, color=colors[0])
        
        # 设置刻度标签
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(categories)
        
        # 设置y轴
        ax2.set_ylim(0, max(values) * 1.2)
        ax2.set_title("style强度雷达图", fontsize=14, fontweight='bold')
        
        plt.suptitle("唐诗宋词style对比分析", fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # 保存图表
        filename = f"style_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.data_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        
        return filepath
    
    def create_dynasty_comparison_chart(self, style: ChartStyle = ChartStyle.MODERN):
        """
        创建唐宋对比图
        """
        # 统计各时期poet数量
        tang_periods = defaultdict(int)
        song_periods = defaultdict(int)
        
        for poet in self.tang_poets_timeline:
            tang_periods[poet["period"]] += 1
        
        for poet in self.song_poets_timeline:
            song_periods[poet["period"]] += 1
        
        # 创建数据
        periods = list(set(list(tang_periods.keys()) + list(song_periods.keys())))
        periods.sort()
        
        tang_counts = [tang_periods.get(period, 0) for period in periods]
        song_counts = [song_periods.get(period, 0) for period in periods]
        
        # 创建图表
        plt.figure(figsize=(14, 8))
        colors = self.color_schemes[style]
        
        x = np.arange(len(periods))
        width = 0.35
        
        # 绘制条形图
        bars1 = plt.bar(x - width/2, tang_counts, width, label='唐代', color=colors[0], alpha=0.8)
        bars2 = plt.bar(x + width/2, song_counts, width, label='宋代', color=colors[1], alpha=0.8)
        
        # 添加数值标签
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{int(height)}', ha='center', va='bottom', fontsize=9)
        
        autolabel(bars1)
        autolabel(bars2)
        
        # 设置图表属性
        plt.title("唐宋诗词发展对比", fontsize=16, fontweight='bold')
        plt.xlabel("时期", fontsize=12)
        plt.ylabel("poet/poet数量", fontsize=12)
        plt.xticks(x, periods, rotation=45, ha='right')
        plt.legend()
        plt.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # 添加说明
        tang_total = sum(tang_counts)
        song_total = sum(song_counts)
        plt.figtext(0.5, 0.01, 
                   f"唐代共{ tang_total}位poet,宋代共{ song_total}位poet",
                   ha='center', fontsize=11, style='italic')
        
        plt.tight_layout()
        
        # 保存图表
        filename = f"dynasty_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.data_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        
        return filepath
    
    def create_geographic_distribution_chart(self, style: ChartStyle = ChartStyle.CLASSICAL):
        """
        创建地理分布图(模拟)
        """
        # 模拟地理数据(实际应用中需要真实地理坐标)
        geographic_data = {
            "李白": {"province": "四川", "city": "江油", "latitude": 31.8, "longitude": 104.7},
            "杜甫": {"province": "河南", "city": "巩义", "latitude": 34.8, "longitude": 113.0},
            "王维": {"province": "山西", "city": "祁县", "latitude": 37.4, "longitude": 112.3},
            "白居易": {"province": "河南", "city": "新郑", "latitude": 34.4, "longitude": 113.7},
            "苏轼": {"province": "四川", "city": "眉山", "latitude": 30.1, "longitude": 103.8},
            "李清照": {"province": "山东", "city": "济南", "latitude": 36.7, "longitude": 117.0},
            "辛弃疾": {"province": "山东", "city": "济南", "latitude": 36.7, "longitude": 117.0}
        }
        
        # 按省份统计
        province_counts = defaultdict(int)
        for poet, data in geographic_data.items():
            province_counts[data["province"]] += 1
        
        # 创建图表
        plt.figure(figsize=(12, 10))
        colors = self.color_schemes[style]
        
        # 准备数据
        provinces = list(province_counts.keys())
        counts = [province_counts[province] for province in provinces]
        
        # 绘制气泡图
        sizes = [count * 500 for count in counts]  # 气泡大小
        
        # 模拟经纬度(实际需要地图库)
        # 这里用散点图模拟
        x = np.random.rand(len(provinces)) * 10
        y = np.random.rand(len(provinces)) * 10
        
        scatter = plt.scatter(x, y, s=sizes, c=range(len(provinces)), 
                             cmap='viridis', alpha=0.6, edgecolors='black', linewidth=1)
        
        # 添加省份标签
        for i, province in enumerate(provinces):
            plt.annotate(f"{province}({counts[i]})", 
                        (x[i], y[i]), 
                        xytext=(5, 5), 
                        textcoords='offset points',
                        fontsize=10,
                        ha='left')
        
        # 添加poet标记
        for poet, data in geographic_data.items():
            # 在实际地图应用中,这里会使用真实经纬度
            pass
        
        plt.title("主要poet地理分布图", fontsize=16, fontweight='bold')
        plt.xlabel("经度(模拟)", fontsize=12)
        plt.ylabel("纬度(模拟)", fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # 添加颜色条
        plt.colorbar(scatter, label='省份索引')
        
        plt.tight_layout()
        
        # 保存图表
        filename = f"geographic_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.data_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.show()
        
        return filepath
    
    def create_comprehensive_dashboard(self, output_dir: str = None):
        """
        创建synthesize可视化仪表板
        """
        if output_dir is None:
            output_dir = self.data_dir
        
        dashboard_files = []
        
        print("开始创建synthesize可视化仪表板...")
        
        # 1. 时间轴图
        print("1. 创建唐代poet时间轴图...")
        timeline_tang = self.create_timeline_chart("tang", ChartStyle.CLASSICAL)
        dashboard_files.append(("唐代poet时间轴", timeline_tang))
        
        print("2. 创建宋代poet时间轴图...")
        timeline_song = self.create_timeline_chart("song", ChartStyle.CLASSICAL)
        dashboard_files.append(("宋代poet时间轴", timeline_song))
        
        # 3. 主题分布图
        print("3. 创建主题分布图...")
        theme_chart = self.create_theme_distribution_chart(style=ChartStyle.MODERN)
        dashboard_files.append(("诗词主题分布", theme_chart))
        
        # 4. 高频词分析
        print("4. 创建李白高频词分析图...")
        word_chart = self.create_word_frequency_chart("李白", ChartStyle.COLORFUL)
        if word_chart:
            dashboard_files.append(("李白高频词分析", word_chart))
        
        # 5. style对比图
        print("5. 创建style对比图...")
        style_chart = self.create_style_comparison_chart(ChartStyle.MODERN)
        dashboard_files.append(("诗词style对比", style_chart))
        
        # 6. 唐宋对比图
        print("6. 创建唐宋对比图...")
        dynasty_chart = self.create_dynasty_comparison_chart(ChartStyle.MODERN)
        dashboard_files.append(("唐宋发展对比", dynasty_chart))
        
        # 7. 地理分布图
        print("7. 创建地理分布图...")
        geo_chart = self.create_geographic_distribution_chart(ChartStyle.CLASSICAL)
        dashboard_files.append(("poet地理分布", geo_chart))
        
        # 创建仪表板报告
        report = {
            "dashboard_name": "唐诗宋词可视化分析仪表板",
            "created_at": datetime.now().isoformat(),
            "data_source": "唐诗宋词50大家深度学习研究项目",
            "visualizations": [
                {
                    "name": name,
                    "filepath": filepath,
                    "description": self._get_viz_description(name)
                }
                for name, filepath in dashboard_files
            ],
            "summary": {
                "total_visualizations": len(dashboard_files),
                "covered_topics": ["时间分布", "主题分析", "词频统计", "style对比", "朝代对比", "地理分布"],
                "data_points": len(self.tang_poets_timeline) + len(self.song_poets_timeline),
                "authors_analyzed": len(self.poetry_themes)
            }
        }
        
        # 保存报告
        report_file = os.path.join(output_dir, f"dashboard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        dashboard_files.append(("仪表板报告", report_file))
        
        print(f"\n仪表板创建完成!共generate {len(dashboard_files)} 个文件")
        print(f"报告文件: {report_file}")
        
        return dashboard_files
    
    def _get_viz_description(self, viz_name: str) -> str:
        """get可视化图表描述"""
        descriptions = {
            "唐代poet时间轴": "展示唐代poet时间分布,按初唐,盛唐,中唐,晚唐分期",
            "宋代poet时间轴": "展示宋代poet时间分布,按北宋前期,中期,后期和南宋分期",
            "诗词主题分布": "分析主要poet的诗词主题偏好分布",
            "李白高频词分析": "分析李白诗词中的高频词汇使用情况",
            "诗词style对比": "对比不同诗词style的代表poet数量和特点",
            "唐宋发展对比": "对比唐代和宋代诗词发展的不同特点",
            "poet地理分布": "展示主要poet的地理出生地分布",
            "仪表板报告": "synthesize可视化仪表板的完整报告"
        }
        return descriptions.get(viz_name, "诗词可视化分析图表")

# 示例使用
def demo_visualization():
    """演示可视化功能"""
    print("init诗词可视化系统...")
    viz = PoetryVisualization()
    
    # 创建唐代时间轴图
    print("\n1. 创建唐代poet时间轴图...")
    timeline_file = viz.create_timeline_chart("tang", ChartStyle.CLASSICAL)
    print(f"时间轴图已保存: {timeline_file}")
    
    # 创建主题分布图
    print("\n2. 创建主题分布图...")
    theme_file = viz.create_theme_distribution_chart(style=ChartStyle.MODERN)
    print(f"主题分布图已保存: {theme_file}")
    
    # 创建高频词分析图
    print("\n3. 创建李白高频词分析图...")
    word_file = viz.create_word_frequency_chart("李白", ChartStyle.COLORFUL)
    if word_file:
        print(f"高频词分析图已保存: {word_file}")
    
    # 创建synthesize仪表板
    print("\n4. 创建synthesize可视化仪表板...")
    dashboard_files = viz.create_comprehensive_dashboard()
    print(f"仪表板创建完成,共generate {len(dashboard_files)} 个文件")
    
    # 显示文件列表
    print("\ngenerate的图表文件:")
    for name, filepath in dashboard_files:
        filename = os.path.basename(filepath)
        print(f"  - {name}: {filename}")
    
    print("\n诗词可视化演示完成!")

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

"""
__all__ = [
    'add_source',
    'collect',
    'export_collection',
    'get_collection_summary',
    'merge_collections',
]

数据采集器 - 多源数据整合与清洗
支持: API对接,文件导入,数据库连接,实时流
"""

import json
import csv
import yaml
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from src.core.paths import COLLECTED_DIR
import pandas as pd

class DataSourceType(Enum):
    """数据源类型"""
    API = "api"                   # API接口
    DATABASE = "database"         # 数据库
    FILE = "file"                 # 文件
    STREAM = "stream"             # 实时流
    WEBHOOK = "webhook"           # Webhook
    MANUAL = "manual"             # 手动录入

class DataFormat(Enum):
    """数据格式"""
    JSON = "json"
    CSV = "csv"
    EXCEL = "excel"
    YAML = "yaml"
    PARQUET = "parquet"
    SQL = "sql"

@dataclass
class DataSource:
    """数据源配置"""
    source_id: str
    name: str
    source_type: DataSourceType
    connection_config: Dict[str, Any] = field(default_factory=dict)
    data_format: DataFormat = DataFormat.JSON
    refresh_interval: Optional[int] = None  # 刷新间隔(分钟)
    last_sync: Optional[str] = None
    status: str = "active"        # active, paused, error
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class DataCollection:
    """数据集合"""
    collection_id: str
    source_id: str
    data: pd.DataFrame = field(default_factory=pd.DataFrame)
    raw_data: Any = None
    schema: Dict[str, str] = field(default_factory=dict)  # 字段名: 类型
    record_count: int = 0
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())
    quality_score: float = 0.0    # 数据质量评分

class DataCollector:
    """数据采集器"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else COLLECTED_DIR
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.sources: Dict[str, DataSource] = {}
        self.collections: Dict[str, DataCollection] = {}
        
        # 数据清洗规则
        self.cleaning_rules: List[Callable] = []
        
        # init默认数据源
        self._init_default_sources()
    
    def _init_default_sources(self):
        """init默认数据源"""
        default_sources = [
            {
                'source_id': 'user_behavior',
                'name': '用户行为数据',
                'source_type': DataSourceType.DATABASE,
                'data_format': DataFormat.SQL,
                'connection_config': {
                    'type': 'postgresql',
                    'tables': ['events', 'sessions', 'conversions']
                }
            },
            {
                'source_id': 'marketing_data',
                'name': '营销投放数据',
                'source_type': DataSourceType.API,
                'data_format': DataFormat.JSON,
                'connection_config': {
                    'platforms': ['google_ads', 'facebook', 'tiktok', 'baidu']
                }
            },
            {
                'source_id': 'crm_data',
                'name': 'CRM客户数据',
                'source_type': DataSourceType.FILE,
                'data_format': DataFormat.CSV,
                'connection_config': {
                    'path': 'data/crm/',
                    'filename_pattern': 'customers_*.csv'
                }
            },
            {
                'source_id': 'financial_data',
                'name': '财务数据',
                'source_type': DataSourceType.FILE,
                'data_format': DataFormat.EXCEL,
                'connection_config': {
                    'path': 'data/finance/',
                    'sheets': ['revenue', 'costs', 'metrics']
                }
            }
        ]
        
        for source_data in default_sources:
            self.add_source(DataSource(**source_data))
    
    def add_source(self, source: DataSource) -> DataSource:
        """添加数据源"""
        self.sources[source.source_id] = source
        return source
    
    def collect(self, source_id: str, parameters: Dict = None) -> DataCollection:
        """采集数据"""
        source = self.sources.get(source_id)
        if not source:
            raise ValueError(f"数据源不存在: {source_id}")
        
        # 根据数据源类型采集
        if source.source_type == DataSourceType.FILE:
            data = self._collect_from_file(source, parameters)
        elif source.source_type == DataSourceType.API:
            data = self._collect_from_api(source, parameters)
        elif source.source_type == DataSourceType.DATABASE:
            data = self._collect_from_database(source, parameters)
        else:
            data = pd.DataFrame()
        
        # 数据清洗
        cleaned_data = self._clean_data(data)
        
        # 计算质量评分
        quality_score = self._calculate_quality_score(cleaned_data)
        
        # 创建集合
        collection = DataCollection(
            collection_id=f"{source_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            source_id=source_id,
            data=cleaned_data,
            raw_data=data,
            record_count=len(cleaned_data),
            quality_score=quality_score
        )
        
        self.collections[collection.collection_id] = collection
        
        # 更新源状态
        source.last_sync = datetime.now().isoformat()
        
        return collection
    
    def _collect_from_file(self, source: DataSource, parameters: Dict = None) -> pd.DataFrame:
        """从文件采集"""
        config = source.connection_config
        path = Path(config.get('path', ''))
        
        if not path.is_absolute():
            path = self.base_path / path
        
        # 查找匹配的文件
        pattern = config.get('filename_pattern', '*')
        files = list(path.glob(pattern))
        
        if not files:
            return pd.DataFrame()
        
        # 读取最新文件
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        
        # 根据格式读取
        if source.data_format == DataFormat.CSV:
            return pd.read_csv(latest_file)
        elif source.data_format == DataFormat.EXCEL:
            sheet = (parameters or {}).get('sheet', 0)
            return pd.read_excel(latest_file, sheet_name=sheet)
        elif source.data_format == DataFormat.JSON:
            return pd.read_json(latest_file)
        elif source.data_format == DataFormat.PARQUET:
            return pd.read_parquet(latest_file)
        
        return pd.DataFrame()
    
    def _collect_from_api(self, source: DataSource, parameters: Dict = None) -> pd.DataFrame:
        """从API采集(模拟实现)"""
        # 实际实现应调用相应API
        # 这里返回模拟数据
        config = source.connection_config
        platforms = config.get('platforms', [])
        
        mock_data = []
        for platform in platforms:
            mock_data.extend([
                {
                    'platform': platform,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'impressions': 10000,
                    'clicks': 500,
                    'conversions': 50,
                    'spend': 1000.0,
                    'revenue': 5000.0
                }
            ])
        
        return pd.DataFrame(mock_data)
    
    def _collect_from_database(self, source: DataSource, parameters: Dict = None) -> pd.DataFrame:
        """从数据库采集(模拟实现)"""
        # 实际实现应连接数据库
        config = source.connection_config
        tables = config.get('tables', [])
        
        # 返回模拟数据
        mock_data = {
            'events': [
                {'user_id': f'user_{i}', 'event': 'page_view', 'timestamp': datetime.now().isoformat()}
                for i in range(100)
            ]
        }
        
        table = (parameters or {}).get('table', tables[0] if tables else 'default')
        return pd.DataFrame(mock_data.get(table, []))
    
    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """清洗数据"""
        if data.empty:
            return data
        
        df = data.copy()
        
        # 1. 处理缺失值
        # 数值列用中位数填充
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            df[col].fillna(df[col].median(), inplace=True)
        
        # 字符串列用众数填充
        string_cols = df.select_dtypes(include=['object']).columns
        for col in string_cols:
            if not df[col].mode().empty:
                df[col].fillna(df[col].mode()[0], inplace=True)
        
        # 2. 处理重复值
        df.drop_duplicates(inplace=True)
        
        # 3. 处理异常值(简单IQR方法)
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # 标记异常值而不是删除
            df[f'{col}_is_outlier'] = (df[col] < lower_bound) | (df[col] > upper_bound)
        
        # 4. 数据类型转换
        # 尝试转换日期列
        for col in string_cols:
            try:
                df[col] = pd.to_datetime(df[col])
            except (ValueError, TypeError):
                pass
        
        # 5. 标准化列名
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        return df
    
    def _calculate_quality_score(self, data: pd.DataFrame) -> float:
        """计算数据质量评分"""
        if data.empty:
            return 0.0
        
        scores = []
        
        # 完整性:非空值比例
        total_cells = data.shape[0] * data.shape[1]
        if total_cells > 0:
            completeness = 1 - data.isnull().sum().sum() / total_cells
            scores.append(completeness * 0.3)
        else:
            scores.append(0.0)
        
        # 唯一性:非重复行比例
        uniqueness = 1 - data.duplicated().sum() / len(data)
        scores.append(uniqueness * 0.25)
        
        # 有效性:数据类型正确比例(简化计算)
        validity = 0.9  # 假设大部分有效
        scores.append(validity * 0.25)
        
        # 一致性:格式unified程度
        consistency = 0.85  # 假设较好
        scores.append(consistency * 0.2)
        
        return sum(scores)
    
    def merge_collections(self, collection_ids: List[str], 
                         join_keys: List[str] = None) -> pd.DataFrame:
        """合并多个数据集合"""
        if not collection_ids:
            return pd.DataFrame()
        
        # get所有集合
        dfs = []
        for cid in collection_ids:
            collection = self.collections.get(cid)
            if collection and not collection.data.empty:
                dfs.append(collection.data)
        
        if not dfs:
            return pd.DataFrame()
        
        # 合并
        if join_keys and len(dfs) > 1:
            result = dfs[0]
            for df in dfs[1:]:
                result = pd.merge(result, df, on=join_keys, how='outer')
        else:
            result = pd.concat(dfs, ignore_index=True)
        
        return result
    
    def export_collection(self, collection_id: str, 
                         format: DataFormat = DataFormat.CSV,
                         filepath: str = None) -> str:
        """导出数据集合"""
        collection = self.collections.get(collection_id)
        if not collection:
            raise ValueError(f"集合不存在: {collection_id}")
        
        if filepath is None:
            filepath = self.base_path / f"{collection_id}.{format.value}"
        
        filepath = Path(filepath)
        
        if format == DataFormat.CSV:
            collection.data.to_csv(filepath, index=False, encoding='utf-8-sig')
        elif format == DataFormat.EXCEL:
            collection.data.to_excel(filepath, index=False)
        elif format == DataFormat.JSON:
            collection.data.to_json(filepath, orient='records', force_ascii=False, indent=2)
        elif format == DataFormat.PARQUET:
            collection.data.to_parquet(filepath)
        
        return str(filepath)
    
    def get_collection_summary(self, collection_id: str) -> Dict[str, Any]:
        """get集合摘要"""
        collection = self.collections.get(collection_id)
        if not collection:
            return {}
        
        df = collection.data
        
        summary = {
            'collection_id': collection_id,
            'source_id': collection.source_id,
            'record_count': collection.record_count,
            'column_count': len(df.columns),
            'quality_score': collection.quality_score,
            'collected_at': collection.collected_at,
            'columns': {}
        }
        
        # 每列统计
        for col in df.columns:
            col_data = df[col]
            col_summary = {
                'type': str(col_data.dtype),
                'null_count': int(col_data.isnull().sum()),
                'null_rate': float(col_data.isnull().sum() / len(df))
            }
            
            if pd.api.types.is_numeric_dtype(col_data):
                col_summary.update({
                    'min': float(col_data.min()) if not col_data.empty else None,
                    'max': float(col_data.max()) if not col_data.empty else None,
                    'mean': float(col_data.mean()) if not col_data.empty else None,
                    'median': float(col_data.median()) if not col_data.empty else None
                })
            else:
                col_summary['unique_count'] = int(col_data.nunique())
            
            summary['columns'][col] = col_summary
        
        return summary

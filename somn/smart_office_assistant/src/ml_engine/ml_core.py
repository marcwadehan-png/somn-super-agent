"""
__all__ = [
    'add_sample',
    'append_feedback',
    'append_sample',
    'clear',
    'from_dict',
    'get_feature_importance',
    'get_feature_names',
    'get_initial_weights',
    'get_raw',
    'get_stats',
    'get_status',
    'init_paths',
    'initialize',
    'load',
    'load_raw_samples',
    'predict',
    'reset',
    'save',
    'save_raw_samples',
    'to_array',
    'to_dict',
    'train',
    'validate',
]

SmartOffice ML Engine - 核心ML引擎
═══════════════════════════════════════════════════════════════
Python 版本,从 Node.js 版本迁移
"""

import json
import math
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

logger = logging.getLogger(__name__)

# ───────────────────────────────────────────────────────────────
# 全局配置
# ───────────────────────────────────────────────────────────────

class MLConfig:
    """ML 全局配置"""
    MODEL_DIR = None
    DATA_DIR = None
    
    PREDICTION_THRESHOLDS = {
        'high': 0.70,
        'medium': 0.40,
    }
    
    LEARNING_RATE = 0.05
    DEFAULT_EPOCHS = 200
    MIN_SAMPLES_FOR_TRAIN = 5
    DEFAULT_WEIGHT_BASE = 0.1
    
    @classmethod
    def init_paths(cls, base_dir: str):
        """init路径"""
        cls.MODEL_DIR = Path(base_dir) / 'data' / 'models'
        cls.DATA_DIR = Path(base_dir) / 'data' / 'samples'
        cls.MODEL_DIR.mkdir(parents=True, exist_ok=True)
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

ML_CONFIG = MLConfig()

# ───────────────────────────────────────────────────────────────
# characteristics模式(Schema)
# ───────────────────────────────────────────────────────────────

class FeatureSchema:
    """
    描述一个业务场景下的characteristics集合
    
    使用示例:
        schema = FeatureSchema('my_app', [
            {'name': 'titleLength', 'type': 'numeric', 'weight': 0.15, 'normalize': lambda v: v / 50},
            {'name': 'hasEmoji', 'type': 'boolean', 'weight': 0.12},
            {'name': 'tagCount', 'type': 'numeric', 'weight': 0.10, 'normalize': lambda v: v / 10},
        ])
    """
    
    def __init__(self, name: str, features: List[Dict[str, Any]]):
        self.name = name
        self.features = features
        self.size = len(features)
    
    def validate(self) -> List[str]:
        """验证characteristics定义合法性"""
        errors = []
        for i, f in enumerate(self.features):
            if 'name' not in f:
                errors.append(f"characteristics[{i}] 缺少 name")
            if 'type' not in f:
                errors.append(f"characteristics[{i}:{f.get('name', '?')}] 缺少 type")
            if 'weight' not in f:
                errors.append(f"characteristics[{i}:{f.get('name', '?')}] 缺少 weight")
        return errors
    
    def get_initial_weights(self) -> List[float]:
        """get初始权重数组"""
        return [f.get('weight', ML_CONFIG.DEFAULT_WEIGHT_BASE) for f in self.features]
    
    def get_feature_names(self) -> List[str]:
        """getcharacteristics名称列表"""
        return [f['name'] for f in self.features]

# ───────────────────────────────────────────────────────────────
# characteristics向量
# ───────────────────────────────────────────────────────────────

class FeatureVector:
    """
    存储一条样本的characteristics数值数组
    由各业务方自己的 FeatureExtractor generate,再传入模型
    """
    
    def __init__(self, schema: FeatureSchema, data: Dict[str, Any] = None):
        self.schema = schema
        self._raw = dict(data) if data else {}
        self._arr = self._build(schema, self._raw)
    
    def _build(self, schema: FeatureSchema, data: Dict[str, Any]) -> List[float]:
        """构建characteristics数组"""
        result = []
        for f in schema.features:
            raw = data.get(f['name'])
            if raw is None:
                result.append(0.0)
                continue
            
            ftype = f['type']
            if ftype == 'boolean':
                result.append(1.0 if raw else 0.0)
            elif ftype == 'ratio':
                result.append(max(0.0, min(1.0, float(raw) if raw else 0.0)))
            elif ftype == 'numeric':
                val = float(raw) if raw else 0.0
                if 'normalize' in f:
                    val = f['normalize'](val)
                result.append(val)
            else:
                result.append(float(raw) if raw else 0.0)
        
        return result
    
    def to_array(self) -> List[float]:
        """返回数值数组(用于模型输入)"""
        return self._arr
    
    def get_raw(self) -> Dict[str, Any]:
        """返回原始数据"""
        return self._raw

# ───────────────────────────────────────────────────────────────
# 训练样本
# ───────────────────────────────────────────────────────────────

class TrainingSample:
    """训练样本"""
    
    def __init__(self, feature_vec: FeatureVector, label: float, meta: Dict[str, Any] = None):
        self.feature_vec = feature_vec
        self.label = max(0.0, min(1.0, float(label) if label else 0.0))
        self.meta = {
            'timestamp': datetime.now().isoformat(),
            **(meta or {})
        }

# ───────────────────────────────────────────────────────────────
# 简单线性回归模型(Sigmoid 输出)
# ───────────────────────────────────────────────────────────────

class SimpleLinearModel:
    """
    轻量级线性回归模型
    使用 sigmoid 激活函数,输出 0~1 分数
    """
    
    def __init__(self, input_size: int):
        self.input_size = input_size
        self.weights = [0.0] * input_size
        self.bias = 0.0
        self.is_trained = False
        self.training_history = []
    
    def _sigmoid(self, x: float) -> float:
        """Sigmoid 激活函数"""
        return 1.0 / (1.0 + math.exp(-x))
    
    def predict(self, feature_vec: FeatureVector) -> float:
        """预测(返回 0~1 分数)"""
        arr = feature_vec.to_array()
        z = self.bias
        for i, val in enumerate(arr):
            z += val * (self.weights[i] if i < len(self.weights) else 0.0)
        return self._sigmoid(z)
    
    def train(self, samples: List[TrainingSample], opts: Dict[str, Any] = None) -> bool:
        """
        训练(梯度下降)
        
        Args:
            samples: 训练样本列表
            opts: 选项 {epochs, learningRate, verbose}
        """
        opts = opts or {}
        epochs = opts.get('epochs', ML_CONFIG.DEFAULT_EPOCHS)
        lr = opts.get('learning_rate', ML_CONFIG.LEARNING_RATE)
        verbose = opts.get('verbose', True)
        min_samples = ML_CONFIG.MIN_SAMPLES_FOR_TRAIN
        
        if len(samples) < min_samples:
            if verbose:
                logger.warning(f"样本不足 ({len(samples)}/{min_samples}),跳过训练")
            return False
        
        # 用初始权重(schema)init
        schema = samples[0].feature_vec.schema
        self.weights = schema.get_initial_weights() if schema else [ML_CONFIG.DEFAULT_WEIGHT_BASE] * self.input_size
        self.bias = 0.1
        self.training_history = []
        
        for epoch in range(epochs):
            total_loss = 0.0
            
            for s in samples:
                pred = self.predict(s.feature_vec)
                error = pred - s.label
                total_loss += error * error
                
                arr = s.feature_vec.to_array()
                # sigmoid 导数 = pred * (1 - pred)
                grad = error * pred * (1 - pred)
                
                for i in range(len(self.weights)):
                    self.weights[i] -= lr * grad * arr[i]
                self.bias -= lr * grad
            
            avg_loss = total_loss / len(samples)
            self.training_history.append({'epoch': epoch, 'loss': avg_loss})
            
            if verbose and epoch % 50 == 0:
                logger.info(f"Epoch {epoch:3d}: Loss = {avg_loss:.6f}")
        
        self.is_trained = True
        final_loss = self.training_history[-1]['loss']
        if verbose:
            logger.info(f"训练完成,最终 Loss = {final_loss:.6f}")
        return True
    
    def get_feature_importance(self, names: List[str] = None) -> List[Dict[str, Any]]:
        """characteristics重要性排序(按权重绝对值降序)"""
        names = names or []
        importance = [
            {
                'feature': names[i] if i < len(names) else f'feat_{i}',
                'weight': abs(w),
                'raw_weight': w
            }
            for i, w in enumerate(self.weights)
        ]
        return sorted(importance, key=lambda x: x['weight'], reverse=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            'weights': self.weights,
            'bias': self.bias,
            'is_trained': self.is_trained,
            'training_history': self.training_history,
            'version': '1.0.0',
            'updated_at': datetime.now().isoformat(),
        }
    
    def from_dict(self, data: Dict[str, Any]):
        """从字典反序列化"""
        self.weights = data.get('weights', [0.0] * self.input_size)
        self.bias = data.get('bias', 0.0)
        self.is_trained = data.get('is_trained', False)
        self.training_history = data.get('training_history', [])
        return self

# ───────────────────────────────────────────────────────────────
# 模型管理器
# ───────────────────────────────────────────────────────────────

class ModelManager:
    """模型持久化管理"""
    
    def __init__(self, schema: FeatureSchema, model_name: str = 'default_model'):
        self.schema = schema
        self.model_name = model_name
        self.model_path = ML_CONFIG.MODEL_DIR / f"{model_name}.json"
        self.model = SimpleLinearModel(schema.size)
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        ML_CONFIG.MODEL_DIR.mkdir(parents=True, exist_ok=True)
        ML_CONFIG.DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> bool:
        """加载已保存模型"""
        if self.model_path.exists():
            try:
                with open(self.model_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.model.from_dict(data)
                return True
            except Exception as e:
                logger.warning(f"模型加载失败,将使用新模型: {e}")
        return False
    
    def save(self):
        """保存模型"""
        with open(self.model_path, 'w', encoding='utf-8') as f:
            json.dump(self.model.to_dict(), f, ensure_ascii=False, indent=2)
    
    def predict(self, feature_vec: FeatureVector) -> float:
        """预测"""
        return self.model.predict(feature_vec)
    
    def train(self, samples: List[TrainingSample], opts: Dict[str, Any] = None) -> bool:
        """训练并保存"""
        ok = self.model.train(samples, opts)
        if ok:
            self.save()
        return ok
    
    def get_status(self) -> Dict[str, Any]:
        """get模型状态"""
        return {
            'is_trained': self.model.is_trained,
            'feature_count': len(self.model.weights),
            'training_epochs': len(self.model.training_history),
            'top_features': self.model.get_feature_importance(self.schema.get_feature_names())[:5],
            'model_path': str(self.model_path),
        }

# ───────────────────────────────────────────────────────────────
# 数据管理器
# ───────────────────────────────────────────────────────────────

class DataManager:
    """训练数据管理"""
    
    def __init__(self, dataset_name: str = 'default'):
        self.samples_path = ML_CONFIG.DATA_DIR / f"{dataset_name}_samples.json"
        self.feedback_path = ML_CONFIG.DATA_DIR / f"{dataset_name}_feedback.json"
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        ML_CONFIG.DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    def _read_json(self, path: Path, fallback):
        """读取 JSON 文件"""
        if not path.exists():
            return fallback
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError, KeyError):
            return fallback
    
    def load_raw_samples(self) -> List[Dict[str, Any]]:
        """加载训练样本"""
        return self._read_json(self.samples_path, [])
    
    def save_raw_samples(self, samples: List[Dict[str, Any]]):
        """保存训练样本"""
        with open(self.samples_path, 'w', encoding='utf-8') as f:
            json.dump(samples, f, ensure_ascii=False, indent=2)
    
    def append_sample(self, raw: Dict[str, Any]) -> int:
        """追加一条训练样本"""
        all_samples = self.load_raw_samples()
        all_samples.append({**raw, '_saved_at': datetime.now().isoformat()})
        self.save_raw_samples(all_samples)
        return len(all_samples)
    
    def append_feedback(self, record: Dict[str, Any]):
        """追加反馈记录"""
        all_feedback = self._read_json(self.feedback_path, [])
        all_feedback.append({**record, '_saved_at': datetime.now().isoformat()})
        with open(self.feedback_path, 'w', encoding='utf-8') as f:
            json.dump(all_feedback, f, ensure_ascii=False, indent=2)
    
    def get_stats(self) -> Dict[str, Any]:
        """get数据统计"""
        samples = self.load_raw_samples()
        feedback = self._read_json(self.feedback_path, [])
        
        high_threshold = ML_CONFIG.PREDICTION_THRESHOLDS['high']
        
        return {
            'total_samples': len(samples),
            'total_feedback': len(feedback),
            'ready_for_training': len(samples) >= ML_CONFIG.MIN_SAMPLES_FOR_TRAIN,
            'high_performing': len([s for s in samples if s.get('label', 0) >= high_threshold]),
        }
    
    def clear(self):
        """清空所有数据"""
        if self.samples_path.exists():
            self.samples_path.unlink()
        if self.feedback_path.exists():
            self.feedback_path.unlink()

# ───────────────────────────────────────────────────────────────
# ML统一引擎入口 (v1.0 2026-04-06)
# ───────────────────────────────────────────────────────────────

class MLEngine:
    """
    SmartOffice ML 统一引擎入口
    
    整合 ModelManager 和 DataManager，提供统一的机器学习接口。
    用于 agent_core 和 _agent_types 中的懒加载导入。
    
    使用示例:
        engine = MLEngine('user_classification')
        # 添加训练样本
        engine.add_sample(features={'titleLength': 45, 'hasEmoji': True}, label=0.8)
        # 训练模型
        engine.train()
        # 预测
        score = engine.predict({'titleLength': 30, 'hasEmoji': False})
        # 获取状态
        status = engine.get_status()
    """
    
    def __init__(self, model_name: str = 'default_ml_model', 
                 config: MLConfig = None):
        """
        初始化 MLEngine
        
        Args:
            model_name: 模型名称，用于文件存储
            config: ML配置，默认使用全局配置
        """
        self.config = config or ML_CONFIG
        self.model_name = model_name
        
        # 内部管理器
        self._data_manager = None
        self._model_manager = None
        self._schema = None
        
        # 状态
        self._is_initialized = False
    
    def initialize(self, feature_schema: FeatureSchema) -> bool:
        """
        初始化引擎和模型
        
        Args:
            feature_schema: 特征模式定义
            
        Returns:
            是否初始化成功
        """
        try:
            self._schema = feature_schema
            self._data_manager = DataManager(self.model_name)
            self._model_manager = ModelManager(feature_schema, self.model_name)
            self._model_manager.load()  # 尝试加载已有模型
            self._is_initialized = True
            return True
        except Exception as e:
            logger.warning(f"MLEngine 初始化失败: {e}")
            return False
    
    def add_sample(self, features: Dict[str, Any], label: float) -> bool:
        """
        添加训练样本
        
        Args:
            features: 特征字典
            label: 标签值 (0.0 - 1.0)
            
        Returns:
            是否添加成功
        """
        if not self._is_initialized:
            return False
        
        try:
            # 创建特征向量
            feature_vec = FeatureVector(self._schema, features)
            # 创建训练样本
            sample = TrainingSample(feature_vec, label)
            # 追加到数据管理器
            self._data_manager.append_sample({
                'features': features,
                'label': label,
                'feature_vec': feature_vec.to_array(),
            })
            return True
        except Exception as e:
            logger.warning(f"添加样本失败: {e}")
            return False
    
    def train(self, epochs: int = None, learning_rate: float = None, verbose: bool = True) -> bool:
        """
        训练模型
        
        Args:
            epochs: 训练轮数，默认使用配置值
            learning_rate: 学习率，默认使用配置值
            verbose: 是否输出训练过程
            
        Returns:
            是否训练成功
        """
        if not self._is_initialized:
            return False
        
        try:
            # 加载样本并转换为训练样本
            raw_samples = self._data_manager.load_raw_samples()
            if len(raw_samples) < self.config.MIN_SAMPLES_FOR_TRAIN:
                logger.warning(f"样本不足，需要至少 {self.config.MIN_SAMPLES_FOR_TRAIN} 个样本")
                return False
            
            training_samples = []
            for raw in raw_samples:
                try:
                    fv = FeatureVector(self._schema, raw.get('features', {}))
                    ts = TrainingSample(fv, raw.get('label', 0.0))
                    training_samples.append(ts)
                except Exception:
                    continue
            
            if not training_samples:
                return False
            
            # 训练选项
            opts = {
                'epochs': epochs or self.config.DEFAULT_EPOCHS,
                'lr': learning_rate or self.config.LEARNING_RATE,
                'verbose': verbose,
            }
            
            return self._model_manager.train(training_samples, opts)
        except Exception as e:
            logger.warning(f"训练失败: {e}")
            return False
    
    def predict(self, features: Dict[str, Any]) -> float:
        """
        使用模型预测
        
        Args:
            features: 特征字典
            
        Returns:
            预测分数 (0.0 - 1.0)
        """
        if not self._is_initialized or not self._model_manager:
            return 0.0
        
        try:
            feature_vec = FeatureVector(self._schema, features)
            return self._model_manager.predict(feature_vec)
        except Exception as e:
            logger.warning(f"预测失败: {e}")
            return 0.0
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取引擎状态
        
        Returns:
            状态字典
        """
        status = {
            'is_initialized': self._is_initialized,
            'model_name': self.model_name,
            'model_manager': None,
            'data_manager': None,
        }
        
        if self._model_manager:
            status['model_manager'] = self._model_manager.get_status()
        
        if self._data_manager:
            status['data_manager'] = self._data_manager.get_stats()
        
        return status
    
    def reset(self):
        """重置引擎，清空数据"""
        if self._data_manager:
            self._data_manager.clear()
        if self._model_manager:
            self._model_manager = ModelManager(self._schema, self.model_name)

# 向后兼容别名
# 这些别名用于旧的导入路径兼容
MLEngine = MLEngine


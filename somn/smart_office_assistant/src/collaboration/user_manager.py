"""
__all__ = [
    'authenticate',
    'create_session',
    'create_user',
    'delete_user',
    'extend',
    'get_community_stats',
    'get_session',
    'get_user',
    'get_user_by_username',
    'get_user_stats',
    'grant_permission',
    'has_permission',
    'is_expired',
    'list_users',
    'remove_session',
    'revoke_permission',
    'update_user',
    'update_user_stat',
    'verify_password',
]

用户管理器 - User Manager
实现说明:
"集体大于个体,人类命运共同体"

核心哲学:
1. 集体智慧:多个用户的智慧大于单个用户
2. 资源共享:知识,经验,模板共享
3. 协同工作:实时协作,共同完成任务
4. 代际传承:知识从老用户传递给新用户

参考<流浪地球>中的集体主义:
- 150万人共同运输火石
- 10000台行星发动机协同工作
- "希望,是这个时代钻石一样珍贵的东西"
"""

import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
from loguru import logger

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False
    logger.warning("bcrypt未安装,密码哈希将使用简单方法")

class UserRole(Enum):
    """用户角色"""
    ADMIN = "admin"           # 管理员
    MODERATOR = "moderator"   # 版主
    USER = "user"             # 普通用户
    GUEST = "guest"           # 访客

class UserStatus(Enum):
    """用户状态"""
    ACTIVE = "active"         # 活跃
    SUSPENDED = "suspended"   # 暂停
    BANNED = "banned"         # 封禁

@dataclass
class User:
    """用户"""
    id: str
    username: str
    email: str
    password_hash: str
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.id)

@dataclass
class Session:
    """用户会话"""
    session_id: str
    user_id: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=24))
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """检查会话是否过期"""
        return datetime.now() > self.expires_at
    
    def extend(self, hours: int = 24):
        """延长会话"""
        self.expires_at = datetime.now() + timedelta(hours=hours)

@dataclass
class Permission:
    """权限"""
    name: str
    description: str
    resource: str
    actions: List[str]

class PermissionManager:
    """权限管理器"""
    
    def __init__(self):
        self.permissions: Dict[str, Permission] = {}
        self._init_default_permissions()
    
    def _init_default_permissions(self):
        """init默认权限"""
        default_permissions = [
            Permission("read_documents", "读取文档", "documents", ["read"]),
            Permission("write_documents", "写入文档", "documents", ["write", "create", "delete"]),
            Permission("read_knowledge", "读取知识库", "knowledge", ["read"]),
            Permission("write_knowledge", "写入知识库", "knowledge", ["write", "create", "delete"]),
            Permission("manage_users", "管理用户", "users", ["read", "write", "create", "delete"]),
            Permission("administrate", "系统管理", "system", ["all"]),
        ]
        
        for perm in default_permissions:
            self.permissions[perm.name] = perm
    
    def has_permission(self, user: User, permission_name: str) -> bool:
        """检查用户是否有权限"""
        # 管理员拥有所有权限
        if user.role == UserRole.ADMIN:
            return True
        
        # 检查权限
        if permission_name not in self.permissions:
            return False
        
        return permission_name in user.metadata.get('permissions', [])
    
    def grant_permission(self, user: User, permission_name: str) -> bool:
        """授予权限"""
        if permission_name not in self.permissions:
            return False
        
        if 'permissions' not in user.metadata:
            user.metadata['permissions'] = []
        
        if permission_name not in user.metadata['permissions']:
            user.metadata['permissions'].append(permission_name)
        
        return True
    
    def revoke_permission(self, user: User, permission_name: str) -> bool:
        """撤销权限"""
        if 'permissions' not in user.metadata:
            return False
        
        if permission_name in user.metadata['permissions']:
            user.metadata['permissions'].remove(permission_name)
            return True
        
        return False

class UserManager:
    """
    用户管理器
    
    基于<流浪地球>集体主义:
    - 个体脆弱,集体强大
    - 资源共享,共同发展
    - 知识传承,代际进化
    
    功能:
    1. 用户管理 - 注册,登录,会话管理
    2. 权限管理 - 细粒度权限控制
    3. 资源配额 - 公平分配资源
    4. 用户统计 - 用户活跃度统计
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # 用户存储
        self.users: Dict[str, User] = {}
        self.users_by_username: Dict[str, User] = {}
        self.users_by_email: Dict[str, User] = {}
        
        # 会话管理
        self.sessions: Dict[str, Session] = {}
        self.user_sessions: Dict[str, Set[str]] = defaultdict(set)
        
        # 权限管理器
        self.permission_manager = PermissionManager()
        
        # 用户统计
        self.user_stats = defaultdict(lambda: {
            'login_count': 0,
            'documents_created': 0,
            'knowledge_contributed': 0,
            'collaborations': 0,
            'last_activity': None
        })
        
        logger.info("用户管理器init完成")
    
    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        role: UserRole = UserRole.USER
    ) -> User:
        """
        创建用户
        
        基于<流浪地球>:每个个体都是集体的一部分
        
        Args:
            username: 用户名
            email: 邮箱
            password: 密码
            role: 角色
            
        Returns:
            User: 创建的用户
        """
        # 检查用户名是否已存在
        if username in self.users_by_username:
            raise ValueError(f"用户名已存在: {username}")
        
        # 检查邮箱是否已存在
        if email in self.users_by_email:
            raise ValueError(f"邮箱已存在: {email}")
        
        # 哈希密码
        password_hash = self._hash_password(password)
        
        # 创建用户
        user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=password_hash,
            role=role
        )
        
        # 存储用户
        self.users[user.id] = user
        self.users_by_username[username] = user
        self.users_by_email[email] = user
        
        logger.info(f"创建用户: {username} (ID: {user.id})")
        
        return user
    
    def _hash_password(self, password: str) -> str:
        """哈希密码"""
        if BCRYPT_AVAILABLE:
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def verify_password(self, user: User, password: str) -> bool:
        """验证密码"""
        if BCRYPT_AVAILABLE:
            return bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))
        else:
            return user.password_hash == hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        认证用户
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            User: 认证成功的用户,否则返回None
        """
        user = self.users_by_username.get(username)
        
        if not user:
            return None
        
        if user.status != UserStatus.ACTIVE:
            return None
        
        if not self.verify_password(user, password):
            return None
        
        # 更新最后登录时间
        user.last_login = datetime.now()
        
        # 更新统计
        self.user_stats[user.id]['login_count'] += 1
        self.user_stats[user.id]['last_activity'] = datetime.now()
        
        logger.info(f"用户登录成功: {username}")
        
        return user
    
    def create_session(self, user: User) -> Session:
        """
        创建会话
        
        Args:
            user: 用户
            
        Returns:
            Session: 会话
        """
        session = Session(
            session_id=str(uuid.uuid4()),
            user_id=user.id
        )
        
        self.sessions[session.session_id] = session
        self.user_sessions[user.id].add(session.session_id)
        
        logger.info(f"创建会话: {session.session_id} (用户: {user.username})")
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """
        get会话
        
        Args:
            session_id: 会话ID
            
        Returns:
            Session: 会话,如果不存在或已过期则返回None
        """
        session = self.sessions.get(session_id)
        
        if not session:
            return None
        
        if session.is_expired():
            self.remove_session(session_id)
            return None
        
        return session
    
    def remove_session(self, session_id: str) -> bool:
        """
        移除会话
        
        Args:
            session_id: 会话ID
            
        Returns:
            是否成功
        """
        session = self.sessions.get(session_id)
        
        if not session:
            return False
        
        # 从用户会话集合中移除
        user_sessions = self.user_sessions.get(session.user_id, set())
        user_sessions.discard(session_id)
        
        # 删除会话
        del self.sessions[session_id]
        
        logger.info(f"移除会话: {session_id}")
        
        return True
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        get用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            User: 用户,如果不存在则返回None
        """
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        通过用户名get用户
        
        Args:
            username: 用户名
            
        Returns:
            User: 用户,如果不存在则返回None
        """
        return self.users_by_username.get(username)
    
    def update_user(self, user: User) -> bool:
        """
        更新用户
        
        Args:
            user: 用户
            
        Returns:
            是否成功
        """
        if user.id not in self.users:
            return False
        
        self.users[user.id] = user
        
        # 更新索引
        self.users_by_username[user.username] = user
        self.users_by_email[user.email] = user
        
        logger.info(f"更新用户: {user.username}")
        
        return True
    
    def delete_user(self, user_id: str) -> bool:
        """
        删除用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            是否成功
        """
        user = self.users.get(user_id)
        
        if not user:
            return False
        
        # 删除用户
        del self.users[user_id]
        del self.users_by_username[user.username]
        del self.users_by_email[user.email]
        
        # 删除所有会话
        sessions = list(self.user_sessions[user_id])
        for session_id in sessions:
            self.remove_session(session_id)
        
        # 删除统计
        if user_id in self.user_stats:
            del self.user_stats[user_id]
        
        logger.info(f"删除用户: {user.username}")
        
        return True
    
    def list_users(
        self,
        role: Optional[UserRole] = None,
        status: Optional[UserStatus] = None,
        limit: int = 100
    ) -> List[User]:
        """
        列出用户
        
        Args:
            role: 角色过滤
            status: 状态过滤
            limit: 限制数量
            
        Returns:
            用户列表
        """
        users = list(self.users.values())
        
        if role:
            users = [u for u in users if u.role == role]
        
        if status:
            users = [u for u in users if u.status == status]
        
        return users[:limit]
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """
        get用户统计
        
        Args:
            user_id: 用户ID
            
        Returns:
            统计信息
        """
        return self.user_stats.get(user_id, {})
    
    def update_user_stat(self, user_id: str, stat_type: str, delta: int = 1):
        """
        更新用户统计
        
        Args:
            user_id: 用户ID
            stat_type: 统计类型
            delta: 增量
        """
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                'login_count': 0,
                'documents_created': 0,
                'knowledge_contributed': 0,
                'collaborations': 0,
                'last_activity': None
            }
        
        if stat_type in self.user_stats[user_id]:
            self.user_stats[user_id][stat_type] += delta
        
        self.user_stats[user_id]['last_activity'] = datetime.now()
    
    def get_community_stats(self) -> Dict[str, Any]:
        """
        get社区统计
        
        基于<流浪地球>:集体力量源于每个个体的贡献
        
        Returns:
            社区统计
        """
        total_users = len(self.users)
        active_users = sum(1 for u in self.users.values() if u.status == UserStatus.ACTIVE)
        online_users = sum(
            1 for user_id in self.user_stats
            if self.user_stats[user_id]['last_activity']
            and datetime.now() - self.user_stats[user_id]['last_activity'] < timedelta(minutes=30)
        )
        
        total_logins = sum(stats['login_count'] for stats in self.user_stats.values())
        total_documents = sum(stats['documents_created'] for stats in self.user_stats.values())
        total_knowledge = sum(stats['knowledge_contributed'] for stats in self.user_stats.values())
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'online_users': online_users,
            'total_logins': total_logins,
            'total_documents': total_documents,
            'total_knowledge': total_knowledge,
            'avg_logins_per_user': total_logins / total_users if total_users > 0 else 0,
            'avg_documents_per_user': total_documents / total_users if total_users > 0 else 0
        }

# 测试代码
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

# 添加json导入
import json

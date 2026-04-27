"""
Somn 存储系统初始化脚本
===================================
用于初始化运行数据库、日志数据库和藏书阁目录结构
"""

import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import shutil

# 路径配置
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RUN_DIR = DATA_DIR / "run"
LOG_DIR = DATA_DIR / "logs"
CORE_DIR = DATA_DIR / "core"
BACKUP_DIR = DATA_DIR / "backups"
LIBRARY_DIR = DATA_DIR / "imperial_library"


def print_step(msg: str):
    """打印步骤"""
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def ensure_directories():
    """确保目录存在"""
    print_step("创建目录结构")
    
    dirs = [
        ("数据根目录", DATA_DIR),
        ("运行数据库目录", RUN_DIR),
        ("日志数据库目录", LOG_DIR),
        ("核心数据目录", CORE_DIR),
        ("备份目录", BACKUP_DIR),
        ("藏书阁目录", LIBRARY_DIR),
    ]
    
    for name, path in dirs:
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {name}: {path}")


def init_run_database():
    """初始化运行数据库"""
    print_step("初始化运行数据库")
    
    db_path = RUN_DIR / "run.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 会话表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            start_time TEXT NOT NULL,
            end_time TEXT,
            user_id TEXT,
            context_summary TEXT,
            metadata TEXT,
            status TEXT DEFAULT 'active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  ✓ sessions 表创建成功")
    
    # 任务状态表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_states (
            task_id TEXT PRIMARY KEY,
            session_id TEXT,
            task_type TEXT,
            status TEXT,
            progress REAL DEFAULT 0,
            result TEXT,
            error TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    """)
    print("  ✓ task_states 表创建成功")
    
    # 运行时数据表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runtime_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            value_type TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  ✓ runtime_data 表创建成功")
    
    # 执行历史表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            component TEXT,
            action TEXT,
            duration_ms REAL,
            success INTEGER,
            details TEXT,
            session_id TEXT
        )
    """)
    print("  ✓ execution_history 表创建成功")
    
    # 创建索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_time ON sessions(start_time)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON task_states(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_execution_time ON execution_history(timestamp)")
    print("  ✓ 索引创建成功")
    
    conn.commit()
    conn.close()
    
    print(f"  运行数据库创建成功: {db_path} ({db_path.stat().st_size} bytes)")


def init_log_database():
    """初始化日志数据库"""
    print_step("初始化日志数据库")
    
    db_path = LOG_DIR / "logs.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 操作日志表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            component TEXT,
            action TEXT,
            message TEXT,
            details TEXT,
            session_id TEXT,
            user_id TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  ✓ operation_logs 表创建成功")
    
    # 错误日志表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            component TEXT,
            error_type TEXT,
            error_message TEXT,
            stack_trace TEXT,
            session_id TEXT,
            task_id TEXT,
            resolved INTEGER DEFAULT 0,
            resolved_at TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  ✓ error_logs 表创建成功")
    
    # 性能日志表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            component TEXT,
            metric_name TEXT,
            metric_value REAL,
            unit TEXT,
            session_id TEXT,
            task_id TEXT,
            details TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  ✓ performance_logs 表创建成功")
    
    # 审计日志表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_id TEXT,
            action TEXT,
            resource_type TEXT,
            resource_id TEXT,
            result TEXT,
            ip_address TEXT,
            metadata TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  ✓ audit_logs 表创建成功")
    
    # 创建索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_oplog_time ON operation_logs(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_oplog_level ON operation_logs(level)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_errlog_time ON error_logs(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_perflog_time ON performance_logs(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_auditlog_time ON audit_logs(timestamp)")
    print("  ✓ 索引创建成功")
    
    conn.commit()
    conn.close()
    
    print(f"  日志数据库创建成功: {db_path} ({db_path.stat().st_size} bytes)")


def init_imperial_library():
    """初始化藏书阁目录"""
    print_step("初始化藏书阁目录")
    
    tiers = [
        ("甲", "永久备份"),
        ("乙", "1年备份"),
        ("丙", "30天备份"),
        ("丁", "7天备份"),
    ]
    
    for tier, desc in tiers:
        tier_dir = LIBRARY_DIR / tier
        tier_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 README
        readme_path = tier_dir / "README.md"
        if not readme_path.exists():
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# {tier}级藏书阁\n")
                f.write(f"## 说明\n")
                f.write(f"此目录用于存储{desc}的数据。\n\n")
                f.write(f"## 数据来源\n")
                f.write(f"- 自动备份任务\n")
                f.write(f"- 手动保存的重要数据\n")
                f.write(f"- 系统状态快照\n")
            print(f"  ✓ {tier}级目录创建成功: {tier_dir}")
    
    # 创建藏书阁索引
    index_file = LIBRARY_DIR / "library_index.json"
    if not index_file.exists():
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump({
                "created_at": datetime.now().isoformat(),
                "version": "1.0",
                "backups": {}
            }, f, indent=2, ensure_ascii=False)
        print(f"  ✓ 藏书阁索引创建成功: {index_file}")
    
    print(f"  藏书阁初始化完成: {LIBRARY_DIR}")


def init_core_directory():
    """初始化核心数据目录"""
    print_step("初始化核心数据目录")
    
    # 系统配置备份
    config_backup_dir = CORE_DIR / "config_backups"
    config_backup_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ 配置备份目录: {config_backup_dir}")
    
    # 状态快照
    snapshot_dir = CORE_DIR / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ 状态快照目录: {snapshot_dir}")
    
    # 存储报告
    report_dir = CORE_DIR / "storage_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ 存储报告目录: {report_dir}")
    
    # 创建初始化标记
    init_marker = CORE_DIR / "initialized.txt"
    with open(init_marker, 'w', encoding='utf-8') as f:
        f.write(f"Somn 存储系统初始化完成\n")
        f.write(f"初始化时间: {datetime.now().isoformat()}\n")
        f.write(f"初始化版本: v1.0\n")
    
    print(f"  ✓ 初始化标记创建成功: {init_marker}")


def verify_initialization():
    """验证初始化"""
    print_step("验证初始化结果")
    
    checks = [
        ("运行数据库", RUN_DIR / "run.db", "文件"),
        ("日志数据库", LOG_DIR / "logs.db", "文件"),
        ("藏书阁甲级", LIBRARY_DIR / "甲", "目录"),
        ("藏书阁乙级", LIBRARY_DIR / "乙", "目录"),
        ("藏书阁丙级", LIBRARY_DIR / "丙", "目录"),
        ("藏书阁丁级", LIBRARY_DIR / "丁", "目录"),
        ("藏书阁索引", LIBRARY_DIR / "library_index.json", "文件"),
        ("核心数据目录", CORE_DIR / "initialized.txt", "文件"),
    ]
    
    all_passed = True
    for name, path, expected_type in checks:
        if expected_type == "文件":
            exists = path.exists() and path.is_file()
        else:
            exists = path.exists() and path.is_dir()
        
        status = "✓" if exists else "✗"
        print(f"  {status} {name}: {path}")
        
        if not exists:
            all_passed = False
    
    return all_passed


def print_summary():
    """打印初始化摘要"""
    print_step("初始化摘要")
    
    print("\n📁 目录结构:")
    print(f"  data/")
    print(f"  ├── run/")
    print(f"  │   └── run.db           (运行数据库)")
    print(f"  ├── logs/")
    print(f"  │   └── logs.db          (日志数据库)")
    print(f"  ├── core/")
    print(f"  │   ├── config_backups/  (配置备份)")
    print(f"  │   ├── snapshots/       (状态快照)")
    print(f"  │   └── storage_reports/ (存储报告)")
    print(f"  ├── backups/            (备份目录)")
    print(f"  └── imperial_library/    (藏书阁)")
    print(f"      ├── 甲/             (永久备份)")
    print(f"      ├── 乙/             (1年备份)")
    print(f"      ├── 丙/             (30天备份)")
    print(f"      ├── 丁/             (7天备份)")
    print(f"      └── library_index.json")
    
    print("\n📊 数据库表:")
    print("  run.db:")
    print("    - sessions (会话记录)")
    print("    - task_states (任务状态)")
    print("    - runtime_data (运行时数据)")
    print("    - execution_history (执行历史)")
    print("\n  logs.db:")
    print("    - operation_logs (操作日志)")
    print("    - error_logs (错误日志)")
    print("    - performance_logs (性能日志)")
    print("    - audit_logs (审计日志)")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("  Somn 存储系统初始化程序 v1.0")
    print("="*60)
    print(f"\n项目根目录: {PROJECT_ROOT}")
    print(f"数据目录: {DATA_DIR}")
    
    # 1. 创建目录结构
    ensure_directories()
    
    # 2. 初始化运行数据库
    init_run_database()
    
    # 3. 初始化日志数据库
    init_log_database()
    
    # 4. 初始化藏书阁
    init_imperial_library()
    
    # 5. 初始化核心目录
    init_core_directory()
    
    # 6. 验证初始化
    if verify_initialization():
        print("\n" + "="*60)
        print("  ✅ 所有初始化检查通过!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("  ⚠️ 部分初始化检查未通过，请检查上述错误")
        print("="*60)
        return 1
    
    # 7. 打印摘要
    print_summary()
    
    print("\n" + "="*60)
    print("  🎉 Somn 存储系统初始化完成!")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

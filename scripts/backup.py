#!/usr/bin/env python3
"""
宠物园数据库自动备份脚本
用法: python3 backup.py [保留天数，默认7]
"""

import os
import sys
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# 配置
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
DB_FILE = PROJECT_DIR / "server" / "pet-garden.db"
BACKUP_DIR = PROJECT_DIR / "backups"
KEEP_DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 7
KEEP_WEEKS = 4

def backup_database():
    """备份数据库"""
    # 创建备份目录
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    (BACKUP_DIR / "weekly").mkdir(parents=True, exist_ok=True)
    
    # 生成备份文件名
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H%M%S")
    backup_file = BACKUP_DIR / f"pet-garden-{date_str}-{time_str}.db"
    
    # 检查数据库文件
    if not DB_FILE.exists():
        print(f"❌ 数据库文件不存在: {DB_FILE}")
        sys.exit(1)
    
    # 使用 SQLite 的备份 API（确保数据一致性）
    import sqlite3
    try:
        source = sqlite3.connect(str(DB_FILE))
        dest = sqlite3.connect(str(backup_file))
        source.backup(dest)
        dest.close()
        source.close()
    except Exception as e:
        print(f"❌ 备份失败: {e}")
        sys.exit(1)
    
    # 压缩备份
    with open(backup_file, 'rb') as f_in:
        with gzip.open(f"{backup_file}.gz", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # 删除未压缩的备份
    backup_file.unlink()
    
    size = os.path.getsize(f"{backup_file}.gz")
    size_str = f"{size / 1024:.1f}KB" if size < 1024 * 1024 else f"{size / 1024 / 1024:.1f}MB"
    print(f"✅ 备份成功: {backup_file.name}.gz ({size_str})")
    
    # 如果是周日，创建周备份
    if now.weekday() == 6:  # 周日
        weekly_file = BACKUP_DIR / "weekly" / f"pet-garden-weekly-{now.strftime('%Y-W%W')}.db.gz"
        shutil.copy2(f"{backup_file}.gz", weekly_file)
        print(f"📅 周备份: {weekly_file.name}")
    
    return f"{backup_file}.gz"

def cleanup_old_backups():
    """清理旧备份"""
    print(f"🧹 清理超过 {KEEP_DAYS} 天的旧备份...")
    
    # 清理日备份
    cutoff = datetime.now() - timedelta(days=KEEP_DAYS)
    for f in BACKUP_DIR.glob("pet-garden-*.db.gz"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < cutoff:
            f.unlink()
            print(f"   删除: {f.name}")
    
    # 清理周备份
    weekly_cutoff = datetime.now() - timedelta(weeks=KEEP_WEEKS)
    for f in (BACKUP_DIR / "weekly").glob("pet-garden-weekly-*.db.gz"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime < weekly_cutoff:
            f.unlink()
            print(f"   删除: {f.name}")

def print_stats():
    """输出备份统计"""
    daily_count = len(list(BACKUP_DIR.glob("pet-garden-*.db.gz")))
    weekly_count = len(list((BACKUP_DIR / "weekly").glob("pet-garden-weekly-*.db.gz")))
    
    total_size = 0
    for f in BACKUP_DIR.rglob("*.db.gz"):
        total_size += f.stat().st_size
    size_str = f"{total_size / 1024:.1f}KB" if total_size < 1024 * 1024 else f"{total_size / 1024 / 1024:.1f}MB"
    
    print()
    print("📊 备份统计:")
    print(f"   日备份: {daily_count} 个")
    print(f"   周备份: {weekly_count} 个")
    print(f"   总大小: {size_str}")

if __name__ == "__main__":
    backup_database()
    cleanup_old_backups()
    print_stats()
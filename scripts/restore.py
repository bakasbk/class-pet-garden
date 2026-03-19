#!/usr/bin/env python3
"""
宠物园数据库恢复脚本
用法: python3 restore.py <备份文件.gz>
"""

import os
import sys
import gzip
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
DB_FILE = PROJECT_DIR / "server" / "pet-garden.db"
BACKUP_DIR = PROJECT_DIR / "backups"

def list_backups():
    """列出可用备份"""
    print("📋 可用备份:")
    print()
    
    # 日备份
    daily = sorted(BACKUP_DIR.glob("pet-garden-*.db.gz"), reverse=True)
    if daily:
        print("日备份:")
        for f in daily[:10]:  # 只显示最近10个
            size = f.stat().st_size / 1024
            mtime = f.stat().st_mtime
            from datetime import datetime
            time_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            print(f"  {f.name} ({size:.1f}KB, {time_str})")
        print()
    
    # 周备份
    weekly = sorted((BACKUP_DIR / "weekly").glob("pet-garden-weekly-*.db.gz"), reverse=True)
    if weekly:
        print("周备份:")
        for f in weekly:
            size = f.stat().st_size / 1024
            mtime = f.stat().st_mtime
            from datetime import datetime
            time_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            print(f"  {f.name} ({size:.1f}KB, {time_str})")
        print()

def restore(backup_file: Path):
    """从备份恢复数据库"""
    if not backup_file.exists():
        # 尝试在 backups 目录下查找
        backup_file = BACKUP_DIR / backup_file
        if not backup_file.exists():
            backup_file = BACKUP_DIR / "weekly" / backup_file
        if not backup_file.exists():
            print(f"❌ 备份文件不存在: {backup_file}")
            sys.exit(1)
    
    # 解压
    temp_db = backup_file.with_suffix('')  # 去掉 .gz
    print(f"📦 解压: {backup_file.name}")
    with gzip.open(backup_file, 'rb') as f_in:
        with open(temp_db, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # 备份当前数据库
    if DB_FILE.exists():
        backup_current = DB_FILE.with_suffix('.db.before-restore')
        shutil.copy2(DB_FILE, backup_current)
        print(f"💾 当前数据库已备份: {backup_current.name}")
    
    # 恢复
    shutil.move(temp_db, DB_FILE)
    print(f"✅ 数据库已恢复: {DB_FILE}")
    print()
    print("⚠️  请重启服务以使更改生效")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_backups()
        print()
        print("用法: python3 restore.py <备份文件名>")
        print("例如: python3 restore.py pet-garden-2026-03-19-084910.db.gz")
    else:
        restore(Path(sys.argv[1]))
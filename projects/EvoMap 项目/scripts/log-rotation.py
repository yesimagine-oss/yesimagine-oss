#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志轮转脚本
保留最近 7 天日志，自动清理旧日志
"""

import os
import logging
from datetime import datetime, timedelta
from pathlib import Path

# 配置
LOG_DIR = Path("/home/admin/.openclaw/workspace/EvoMap 项目/logs")
RETENTION_DAYS = 7
MAX_LOG_SIZE_MB = 10  # 单个日志文件最大 10MB

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "log-rotation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_log_files():
    """获取所有日志文件"""
    if not LOG_DIR.exists():
        return []
    
    log_files = []
    for file in LOG_DIR.glob("*.log"):
        if file.is_file():
            log_files.append(file)
    
    return log_files


def cleanup_old_logs():
    """清理旧日志"""
    logger.info("🧹 开始清理旧日志...")
    
    cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)
    deleted_count = 0
    deleted_size = 0
    
    for log_file in get_log_files():
        try:
            # 获取文件修改时间
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            
            if mtime < cutoff_date:
                file_size = log_file.stat().st_size
                log_file.unlink()
                deleted_count += 1
                deleted_size += file_size
                logger.info(f"🗑️  删除：{log_file.name} ({mtime.strftime('%Y-%m-%d')}, {file_size/1024:.1f}KB)")
        except Exception as e:
            logger.error(f"❌ 删除失败 {log_file.name}: {e}")
    
    logger.info(f"✅ 清理完成：删除 {deleted_count} 个文件，释放 {deleted_size/1024:.1f}KB")
    return deleted_count, deleted_size


def rotate_large_logs():
    """轮转过大的日志文件"""
    logger.info("🔄 开始轮转大型日志...")
    
    rotated_count = 0
    
    for log_file in get_log_files():
        try:
            file_size_mb = log_file.stat().st_size / (1024 * 1024)
            
            if file_size_mb > MAX_LOG_SIZE_MB:
                # 生成新文件名
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_name = f"{log_file.stem}_{timestamp}{log_file.suffix}"
                new_path = log_file.parent / new_name
                
                # 重命名当前文件
                log_file.rename(new_path)
                rotated_count += 1
                
                logger.info(f"📦 轮转：{log_file.name} → {new_name} ({file_size_mb:.1f}MB)")
                
                # 创建新的空日志文件
                log_file.touch()
                
        except Exception as e:
            logger.error(f"❌ 轮转失败 {log_file.name}: {e}")
    
    logger.info(f"✅ 轮转完成：{rotated_count} 个文件")
    return rotated_count


def get_total_log_size():
    """获取日志总大小"""
    total_size = 0
    for log_file in get_log_files():
        total_size += log_file.stat().st_size
    return total_size


def generate_report():
    """生成日志报告"""
    log_files = get_log_files()
    
    report = f"""
📊 日志系统报告

📁 日志目录：{LOG_DIR}
📋 文件数量：{len(log_files)}
💾 总大小：{get_total_log_size()/1024:.1f}KB

📄 文件列表：
"""
    
    for log_file in sorted(log_files, key=lambda f: f.stat().st_size, reverse=True):
        size_kb = log_file.stat().st_size / 1024
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        report += f"  - {log_file.name}: {size_kb:.1f}KB ({mtime.strftime('%Y-%m-%d %H:%M')})\n"
    
    return report


def main():
    """主函数"""
    logger.info("="*60)
    logger.info("🔄 日志轮转任务启动")
    logger.info(f"📁 日志目录：{LOG_DIR}")
    logger.info(f"⏰ 保留天数：{RETENTION_DAYS}天")
    logger.info(f"📦 轮转阈值：{MAX_LOG_SIZE_MB}MB")
    logger.info("="*60)
    
    # 清理旧日志
    deleted_count, deleted_size = cleanup_old_logs()
    
    # 轮转大型日志
    rotated_count = rotate_large_logs()
    
    # 生成报告
    report = generate_report()
    logger.info(report)
    
    logger.info("✅ 日志轮转任务完成")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉验证机制库

功能:
1. 多方法验证同一信息
2. 置信度评估
3. 矛盾检测
4. 自动修正

使用:
    from validator import CrossValidator
    
    validator = CrossValidator()
    
    # 验证 cron 状态
    result = validator.validate_cron_status()
    print(f"状态：{result['status']}, 置信度：{result['confidence']}")
    
    # 验证任务执行
    result = validator.validate_task_executed("morning_check.py")
"""

import subprocess
import os
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


class CrossValidator:
    """交叉验证器"""
    
    def __init__(self):
        self.results = {}
    
    def validate_cron_status(self) -> Dict[str, Any]:
        """
        交叉验证 cron 服务状态
        
        Returns:
            {
                "status": "running"|"not_running"|"unknown",
                "confidence": "high"|"medium"|"low",
                "checks": {...},
                "warning": str|None
            }
        """
        logger.info("🔍 交叉验证 cron 状态...")
        
        checks = {}
        positive_count = 0
        total_checks = 0
        
        # 检查 1: 检查进程
        try:
            result = subprocess.Popen(
                ["ps", "aux"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = result.communicate(timeout=10)
            cron_running = "crond" in stdout or "cron" in stdout
            checks["process"] = cron_running
            if cron_running:
                positive_count += 1
            total_checks += 1
        except Exception as e:
            logger.error(f"❌ 进程检查失败：{e}")
            checks["process"] = None
        
        # 检查 2: 检查 crontab
        try:
            result = subprocess.Popen(
                ["crontab", "-l"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = result.communicate(timeout=10)
            has_tasks = "evomap" in stdout.lower() or "EvoMap" in stdout
            checks["crontab"] = has_tasks
            if has_tasks:
                positive_count += 1
            total_checks += 1
        except Exception as e:
            logger.error(f"❌ crontab 检查失败：{e}")
            checks["crontab"] = None
        
        # 检查 3: 检查 PID 文件
        pid_files = ["/var/run/crond.pid", "/var/run/cron.pid"]
        pid_exists = False
        for pid_file in pid_files:
            if os.path.exists(pid_file):
                pid_exists = True
                break
        checks["pid_file"] = pid_exists
        if pid_exists:
            positive_count += 1
        total_checks += 1
        
        # 检查 4: 检查日志文件
        log_files = ["/var/log/cron.log", "/var/log/syslog"]
        log_exists = False
        for log_file in log_files:
            if os.path.exists(log_file):
                log_exists = True
                break
        checks["log_file"] = log_exists
        # 日志文件存在不计入 positive，只是辅助信息
        
        # 计算置信度
        if total_checks == 0:
            confidence = "low"
            status = "unknown"
        else:
            positive_ratio = positive_count / total_checks
            
            if positive_ratio == 1.0:
                confidence = "high"
                status = "running"
            elif positive_ratio >= 0.5:
                confidence = "medium"
                status = "running"
            else:
                confidence = "high"
                status = "not_running"
        
        # 检测矛盾
        warning = None
        if checks.get("process") and not checks.get("crontab"):
            warning = "⚠️ 矛盾：cron 进程运行但没有 EvoMap 任务"
        elif not checks.get("process") and checks.get("crontab"):
            warning = "⚠️ 矛盾：有 EvoMap 任务但 cron 进程未运行"
        
        result = {
            "status": status,
            "confidence": confidence,
            "checks": checks,
            "warning": warning,
            "positive_count": positive_count,
            "total_checks": total_checks
        }
        
        logger.info(f"✅ cron 状态验证完成：{status} ({confidence})")
        if warning:
            logger.warning(warning)
        
        return result
    
    def validate_task_executed(self, task_name: str, timeout_minutes: int = 10) -> Dict[str, Any]:
        """
        交叉验证任务是否执行
        
        Args:
            task_name: 任务名称
            timeout_minutes: 超时时间（分钟）
        
        Returns:
            {
                "executed": bool,
                "confidence": "high"|"medium"|"low",
                "checks": {...}
            }
        """
        logger.info(f"🔍 交叉验证任务执行：{task_name}")
        
        checks = {}
        positive_count = 0
        total_checks = 0
        
        # 检查 1: 检查日志文件
        log_file = LOGS_DIR / f"cron_{task_name.split('_')[0]}.log"
        if log_file.exists():
            last_modified = datetime.fromtimestamp(log_file.stat().st_mtime)
            time_diff = datetime.now() - last_modified
            
            executed_recently = time_diff < timedelta(minutes=timeout_minutes)
            checks["log_file"] = {
                "exists": True,
                "last_modified": last_modified.isoformat(),
                "executed_recently": executed_recently
            }
            
            if executed_recently:
                positive_count += 1
        else:
            checks["log_file"] = {"exists": False}
        
        total_checks += 1
        
        # 检查 2: 检查进程
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True, text=True, timeout=10
            )
            task_running = task_name in result.stdout
            checks["process"] = task_running
            if task_running:
                positive_count += 1
            total_checks += 1
        except Exception as e:
            logger.error(f"❌ 进程检查失败：{e}")
            checks["process"] = None
        
        # 检查 3: 检查执行记录
        exec_record = LOGS_DIR / "execution_history.json"
        if exec_record.exists():
            import json
            try:
                with open(exec_record, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                
                # 查找最近执行记录
                now = datetime.now()
                for record in reversed(history.get("executions", [])):
                    record_time = datetime.fromisoformat(record["timestamp"])
                    if (now - record_time).total_seconds() < timeout_minutes * 60:
                        if task_name in record.get("task", ""):
                            checks["execution_record"] = {
                                "found": True,
                                "timestamp": record["timestamp"],
                                "status": record.get("status")
                            }
                            if record.get("status") == "success":
                                positive_count += 1
                            total_checks += 1
                            break
            except Exception as e:
                logger.error(f"❌ 执行记录检查失败：{e}")
                checks["execution_record"] = None
        
        # 计算置信度
        if total_checks == 0:
            confidence = "low"
            executed = False
        else:
            positive_ratio = positive_count / total_checks
            
            if positive_ratio == 1.0:
                confidence = "high"
                executed = True
            elif positive_ratio >= 0.5:
                confidence = "medium"
                executed = True
            else:
                confidence = "high"
                executed = False
        
        result = {
            "executed": executed,
            "confidence": confidence,
            "checks": checks,
            "positive_count": positive_count,
            "total_checks": total_checks
        }
        
        logger.info(f"✅ 任务执行验证完成：{executed} ({confidence})")
        return result
    
    def validate_api_endpoint(self, endpoint: str, expected_status: int = 200) -> Dict[str, Any]:
        """
        交叉验证 API 端点可用性
        
        Args:
            endpoint: API 端点路径
            expected_status: 期望状态码
        
        Returns:
            {
                "available": bool,
                "confidence": "high"|"medium"|"low",
                "checks": {...}
            }
        """
        logger.info(f"🔍 交叉验证 API 端点：{endpoint}")
        
        import requests
        
        checks = {}
        positive_count = 0
        total_checks = 0
        
        base_url = "https://evomap.ai"
        url = f"{base_url}{endpoint}"
        
        # 检查 1: HTTP GET 请求
        try:
            response = requests.get(url, timeout=30)
            status_match = response.status_code == expected_status
            checks["http_get"] = {
                "status_code": response.status_code,
                "match": status_match
            }
            if status_match:
                positive_count += 1
            total_checks += 1
        except Exception as e:
            logger.error(f"❌ HTTP GET 检查失败：{e}")
            checks["http_get"] = None
        
        # 检查 2: HTTP HEAD 请求
        try:
            response = requests.head(url, timeout=30)
            status_match = response.status_code == expected_status
            checks["http_head"] = {
                "status_code": response.status_code,
                "match": status_match
            }
            if status_match:
                positive_count += 1
            total_checks += 1
        except Exception as e:
            logger.error(f"❌ HTTP HEAD 检查失败：{e}")
            checks["http_head"] = None
        
        # 检查 3: 检查响应内容
        try:
            response = requests.get(url, timeout=30)
            has_valid_content = len(response.text) > 0
            checks["content"] = {
                "length": len(response.text),
                "valid": has_valid_content
            }
            if has_valid_content:
                positive_count += 1
            total_checks += 1
        except Exception as e:
            logger.error(f"❌ 内容检查失败：{e}")
            checks["content"] = None
        
        # 计算置信度
        if total_checks == 0:
            confidence = "low"
            available = False
        else:
            positive_ratio = positive_count / total_checks
            
            if positive_ratio == 1.0:
                confidence = "high"
                available = True
            elif positive_ratio >= 0.5:
                confidence = "medium"
                available = True
            else:
                confidence = "high"
                available = False
        
        result = {
            "available": available,
            "confidence": confidence,
            "checks": checks,
            "positive_count": positive_count,
            "total_checks": total_checks
        }
        
        logger.info(f"✅ API 端点验证完成：{available} ({confidence})")
        return result
    
    def quick_validate(self, check_type: str, **kwargs) -> bool:
        """
        快速验证（简化版）
        
        Args:
            check_type: 检查类型 (cron/task/api)
            **kwargs: 额外参数
        
        Returns:
            True if validated with high confidence
        """
        if check_type == "cron":
            result = self.validate_cron_status()
            return result["confidence"] == "high" and result["status"] == "running"
        elif check_type == "task":
            task_name = kwargs.get("task_name", "")
            result = self.validate_task_executed(task_name)
            return result["confidence"] == "high" and result["executed"]
        elif check_type == "api":
            endpoint = kwargs.get("endpoint", "")
            result = self.validate_api_endpoint(endpoint)
            return result["confidence"] == "high" and result["available"]
        else:
            logger.error(f"❌ 未知检查类型：{check_type}")
            return False


# 便捷函数
def validate_cron() -> Dict[str, Any]:
    """快速验证 cron 状态"""
    validator = CrossValidator()
    return validator.validate_cron_status()


def validate_task(task_name: str) -> Dict[str, Any]:
    """快速验证任务执行"""
    validator = CrossValidator()
    return validator.validate_task_executed(task_name)


def validate_api(endpoint: str) -> Dict[str, Any]:
    """快速验证 API 端点"""
    validator = CrossValidator()
    return validator.validate_api_endpoint(endpoint)


if __name__ == "__main__":
    # 测试
    validator = CrossValidator()
    
    print("=== 测试 cron 状态验证 ===")
    result = validator.validate_cron_status()
    print(f"状态：{result['status']}, 置信度：{result['confidence']}")
    if result.get('warning'):
        print(f"警告：{result['warning']}")
    
    print("\n=== 测试任务执行验证 ===")
    result = validator.validate_task_executed("morning_check")
    print(f"执行：{result['executed']}, 置信度：{result['confidence']}")

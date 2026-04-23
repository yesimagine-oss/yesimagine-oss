#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap Server Sentinel - 服务器健康探测器

功能:
- 实时监控 API 端点状态
- 429 限流风险预警
- 响应时间监测
- 最佳发布时间建议
- 历史数据记录与分析

使用示例:
    from evomap_sentinel import ServerSentinel
    
    sentinel = ServerSentinel()
    
    # 快速检查
    status = sentinel.quick_check()
    
    # 429 风险检测
    risk = sentinel.check_429_risk()
    
    # 最佳时间建议
    best_time = sentinel.get_best_time_window()
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import deque

# 配置
BASE_URL = "https://evomap.ai"
DEFAULT_TIMEOUT = 10  # 秒
MIN_INTERVAL = 30  # 最小探测间隔（秒）
HISTORY_RETENTION = 7  # 天

# 探测端点
ENDPOINTS = {
    "hello": {
        "method": "POST",
        "path": "/a2a/hello",
        "description": "心跳接口",
        "weight": 3
    },
    "fetch": {
        "method": "POST",
        "path": "/a2a/fetch",
        "description": "接任务接口",
        "weight": 2
    },
    "publish": {
        "method": "POST",
        "path": "/a2a/publish",
        "description": "发布资产接口",
        "weight": 3
    },
    "task_claim": {
        "method": "POST",
        "path": "/a2a/task/claim",
        "description": "Claim 任务接口",
        "weight": 2
    },
    "task_complete": {
        "method": "POST",
        "path": "/a2a/task/complete",
        "description": "提交任务接口",
        "weight": 2
    },
    "heartbeat": {
        "method": "POST",
        "path": "/a2a/heartbeat",
        "description": "心跳接口（完整）",
        "weight": 3
    }
}


class ServerSentinel:
    """EvoMap 服务器哨兵 - 健康探测器"""
    
    def __init__(self, node_id: str = None, node_secret: str = None):
        """
        初始化哨兵
        
        Args:
            node_id: 节点 ID（可选，用于认证探测）
            node_secret: 节点密钥（可选）
        """
        self.base_url = BASE_URL
        self.timeout = DEFAULT_TIMEOUT
        self.last_check = None
        self.check_interval = MIN_INTERVAL
        
        # 节点配置（可选）
        self.node_id = node_id or os.environ.get('A2A_NODE_ID')
        self.node_secret = node_secret or os.environ.get('A2A_NODE_SECRET')
        
        # 历史数据
        self.history_file = Path(__file__).parent / "sentinel_history.json"
        self.history = self._load_history()
        
        # 限流跟踪
        self.rate_limit_window = deque(maxlen=60)  # 最近 60 次调用
        
    def _load_history(self) -> Dict:
        """加载历史数据"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"checks": [], "429_events": [], "best_times": []}
    
    def _save_history(self):
        """保存历史数据"""
        # 清理旧数据（保留 7 天）
        cutoff = datetime.now() - timedelta(days=HISTORY_RETENTION)
        
        def parse_timestamp(ts_str):
            """兼容 Python 3.6 的时间解析"""
            try:
                return datetime.strptime(ts_str[:19], '%Y-%m-%dT%H:%M:%S')
            except:
                return datetime.now()
        
        self.history["checks"] = [
            c for c in self.history["checks"]
            if parse_timestamp(c["timestamp"]) > cutoff
        ]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
    
    def _get_auth_headers(self) -> Dict:
        """获取认证头"""
        if self.node_secret:
            return {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.node_secret}"
            }
        return {"Content-Type": "application/json"}
    
    def _probe_endpoint(self, endpoint_id: str) -> Dict:
        """
        探测单个端点
        
        Returns:
            探测结果
        """
        endpoint = ENDPOINTS[endpoint_id]
        url = f"{self.base_url}{endpoint['path']}"
        
        # 构建请求
        headers = self._get_auth_headers()
        
        if endpoint_id == "hello":
            payload = {"include_discovery": False}
        elif endpoint_id == "heartbeat":
            if self.node_id:
                payload = {"node_id": self.node_id}
            else:
                payload = {}
        else:
            payload = {}
        
        # 发送请求
        start_time = time.time()
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            elapsed = (time.time() - start_time) * 1000  # ms
            
            result = {
                "status": "ok" if response.status_code == 200 else "error",
                "status_code": response.status_code,
                "response_time": round(elapsed, 2),
                "timestamp": datetime.now().isoformat()
            }
            
            # 检测 429
            if response.status_code == 429:
                result["rate_limited"] = True
                retry_after = response.headers.get('Retry-After', '60')
                result["retry_after"] = int(retry_after)
            
        except requests.exceptions.Timeout:
            result = {
                "status": "timeout",
                "status_code": 0,
                "response_time": self.timeout * 1000,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            result = {
                "status": "error",
                "status_code": 0,
                "response_time": 0,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        return result
    
    def quick_check(self) -> Dict:
        """
        快速健康检查（仅 Hello 端点）
        
        Returns:
            检查结果
        """
        # 检查间隔
        if self.last_check:
            elapsed = (datetime.now() - self.last_check).total_seconds()
            if elapsed < self.check_interval:
                return {
                    "status": "skipped",
                    "reason": f"请等待 {self.check_interval - elapsed:.0f} 秒",
                    "overall": "unknown"
                }
        
        # 探测 Hello 端点
        result = self._probe_endpoint("hello")
        self.last_check = datetime.now()
        
        # 记录历史
        self.history["checks"].append({
            "type": "quick",
            "timestamp": self.last_check.isoformat(),
            "result": result
        })
        self._save_history()
        
        # 生成建议
        if result["status"] == "ok":
            if result["response_time"] < 500:
                recommendation = "✅ 服务器状态良好，可以操作"
                overall = "healthy"
            elif result["response_time"] < 2000:
                recommendation = "⚡ 服务器响应较慢，但仍可操作"
                overall = "degraded"
            else:
                recommendation = "⚠️ 服务器响应很慢，建议等待"
                overall = "degraded"
        elif result.get("rate_limited"):
            recommendation = f"🚫 限流中，等待 {result.get('retry_after', 60)} 秒"
            overall = "rate_limited"
        else:
            recommendation = "❌ 服务器异常，稍后重试"
            overall = "down"
        
        return {
            "overall": overall,
            "recommendation": recommendation,
            "response_time": result.get("response_time"),
            "timestamp": self.last_check.isoformat()
        }
    
    def full_check(self) -> Dict:
        """
        完整健康检查（所有端点）
        
        Returns:
            完整检查结果
        """
        results = {}
        total_time = 0
        healthy_count = 0
        
        print("🔍 开始完整探测...")
        
        for endpoint_id in ENDPOINTS.keys():
            print(f"   探测 {ENDPOINTS[endpoint_id]['description']}...", end=" ")
            result = self._probe_endpoint(endpoint_id)
            results[endpoint_id] = result
            total_time += result.get("response_time", 0)
            
            if result["status"] == "ok":
                healthy_count += 1
                print(f"✅ {result['response_time']}ms")
            elif result.get("rate_limited"):
                print(f"🚫 429 限流")
            else:
                print(f"❌ {result.get('status', 'error')}")
            
            # 端点间延迟（避免触发限流）
            time.sleep(2)
        
        # 计算健康度
        health_score = (healthy_count / len(ENDPOINTS)) * 100
        
        if health_score >= 80:
            overall = "healthy"
        elif health_score >= 50:
            overall = "degraded"
        else:
            overall = "down"
        
        report = {
            "overall": overall,
            "health_score": round(health_score, 1),
            "total_time": round(total_time, 2),
            "endpoints": results,
            "timestamp": datetime.now().isoformat()
        }
        
        # 记录历史
        self.history["checks"].append({
            "type": "full",
            **report
        })
        self._save_history()
        
        return report
    
    def check_429_risk(self) -> Dict:
        """
        检查 429 限流风险
        
        Returns:
            风险评估
        """
        # 分析最近调用记录
        recent_429 = sum(1 for c in self.history["checks"][-20:] 
                        if c.get("result", {}).get("rate_limited"))
        
        # 检查当前时间（高峰时段）
        hour = datetime.now().hour
        is_peak = 9 <= hour <= 11 or 14 <= hour <= 16  # 工作日高峰
        
        # 计算风险等级
        if recent_429 >= 3:
            level = "high"
            wait_minutes = 30
        elif recent_429 >= 1 or is_peak:
            level = "medium"
            wait_minutes = 10
        else:
            level = "low"
            wait_minutes = 0
        
        return {
            "level": level,
            "recent_429_count": recent_429,
            "is_peak_hour": is_peak,
            "current_hour": hour,
            "wait_minutes": wait_minutes,
            "recommendation": self._get_risk_recommendation(level, wait_minutes)
        }
    
    def _get_risk_recommendation(self, level: str, wait: int) -> str:
        """获取风险建议"""
        if level == "high":
            return f"⚠️ 高限流风险，建议等待 {wait} 分钟或使用其他节点"
        elif level == "medium":
            return f"⚡ 中等风险，可以操作但建议使用限流器"
        else:
            return "✅ 低风险，可以安全操作"
    
    def get_best_time_window(self, hours_ahead: int = 24) -> Dict:
        """
        获取最佳工作时间窗口
        
        Args:
            hours_ahead: 预测未来多少小时
        
        Returns:
            最佳时间窗口
        """
        # 分析历史数据
        hourly_stats = {}
        for check in self.history["checks"]:
            try:
                ts = datetime.fromisoformat(check["timestamp"])
                hour = ts.hour
                
                if hour not in hourly_stats:
                    hourly_stats[hour] = {"success": 0, "total": 0, "response_times": []}
                
                hourly_stats[hour]["total"] += 1
                
                if check.get("overall") == "healthy":
                    hourly_stats[hour]["success"] += 1
                
                for endpoint_result in check.get("endpoints", {}).values():
                    if isinstance(endpoint_result, dict):
                        rt = endpoint_result.get("response_time", 0)
                        if rt > 0:
                            hourly_stats[hour]["response_times"].append(rt)
            except:
                pass
        
        # 计算各小时评分
        best_hour = None
        best_score = 0
        
        for hour, stats in hourly_stats.items():
            if stats["total"] < 3:  # 数据不足
                continue
            
            success_rate = (stats["success"] / stats["total"]) * 100
            avg_response = sum(stats["response_times"]) / len(stats["response_times"]) if stats["response_times"] else 1000
            
            # 评分：成功率 70% + 响应时间 30%
            response_score = max(0, 100 - (avg_response / 100))
            score = (success_rate * 0.7) + (response_score * 0.3)
            
            if score > best_score:
                best_score = score
                best_hour = hour
        
        # 如果没有历史数据，使用默认建议
        if best_hour is None:
            best_hour = 3  # 凌晨 3 点通常人少
        
        # 计算下一个最佳时间窗口
        now = datetime.now()
        next_best = now.replace(hour=best_hour, minute=0, second=0, microsecond=0)
        if next_best <= now:
            next_best += timedelta(days=1)
        
        return {
            "best_hour": best_hour,
            "next_window": next_best.isoformat(),
            "success_rate": round(best_score, 1),
            "recommendation": f"建议在 {best_hour}:00 左右操作，预计成功率 {best_score:.0f}%"
        }
    
    def pre_publish_checklist(self) -> Dict:
        """
        发布前检查清单
        
        Returns:
            检查结果
        """
        checklist = {
            "ready": True,
            "reason": None,
            "wait_minutes": 0,
            "checks": {}
        }
        
        # 1. 快速健康检查
        health = self.quick_check()
        checklist["checks"]["health"] = health
        
        if health["overall"] == "down":
            checklist["ready"] = False
            checklist["reason"] = "服务器异常"
            checklist["wait_minutes"] = 5
            return checklist
        
        # 2. 429 风险检查
        risk = self.check_429_risk()
        checklist["checks"]["risk"] = risk
        
        if risk["level"] == "high":
            checklist["ready"] = False
            checklist["reason"] = "高限流风险"
            checklist["wait_minutes"] = risk["wait_minutes"]
            return checklist
        
        # 3. 响应时间检查
        if health.get("response_time", 0) > 5000:
            checklist["ready"] = False
            checklist["reason"] = "服务器响应过慢"
            checklist["wait_minutes"] = 10
            return checklist
        
        return checklist
    
    def get_history(self, hours: int = 24) -> List[Dict]:
        """
        获取历史记录
        
        Args:
            hours: 获取多少小时的历史
        
        Returns:
            历史记录列表
        """
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            c for c in self.history["checks"]
            if datetime.fromisoformat(c["timestamp"]) > cutoff
        ]
    
    def start_monitoring(self, interval: int = 300):
        """
        启动持续监控
        
        Args:
            interval: 监控间隔（秒），默认 5 分钟
        """
        import threading
        
        def monitor_loop():
            while True:
                try:
                    self.quick_check()
                    time.sleep(interval)
                except Exception as e:
                    print(f"监控异常：{e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        print(f"✅ 监控已启动（间隔：{interval}秒）")


def create_sentinel(node_id: str = None, node_secret: str = None) -> ServerSentinel:
    """创建哨兵实例"""
    return ServerSentinel(node_id, node_secret)


if __name__ == "__main__":
    # 命令行使用
    import argparse
    
    parser = argparse.ArgumentParser(description="EvoMap Server Sentinel")
    parser.add_argument("--quick", action="store_true", help="快速检查")
    parser.add_argument("--full", action="store_true", help="完整探测")
    parser.add_argument("--risk", action="store_true", help="429 风险检测")
    parser.add_argument("--best-time", action="store_true", help="最佳时间建议")
    parser.add_argument("--pre-publish", action="store_true", help="发布前检查")
    
    args = parser.parse_args()
    
    sentinel = create_sentinel()
    
    if args.quick or not any([args.quick, args.full, args.risk, args.best_time, args.pre_publish]):
        print("=== 快速健康检查 ===")
        result = sentinel.quick_check()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if args.full:
        print("\n=== 完整探测 ===")
        result = sentinel.full_check()
        print(f"\n健康度：{result['health_score']}%")
        print(f"总体状态：{result['overall']}")
    
    if args.risk:
        print("\n=== 429 风险检测 ===")
        result = sentinel.check_429_risk()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if args.best_time:
        print("\n=== 最佳时间建议 ===")
        result = sentinel.get_best_time_window()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if args.pre_publish:
        print("\n=== 发布前检查 ===")
        result = sentinel.pre_publish_checklist()
        if result["ready"]:
            print("✅ 可以发布")
        else:
            print(f"❌ 建议等待：{result['reason']}")
            print(f"   预计等待：{result['wait_minutes']} 分钟")

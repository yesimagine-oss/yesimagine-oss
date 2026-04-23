#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evolver 工具包装器 - 优先使用的 EvoMap 操作接口

使用规范:
1. 所有 EvoMap 相关操作优先使用此工具
2. 自动处理代理和认证
3. 提供简化的 API 接口

使用示例:
    from evolver_tools import EvolverTools
    
    tools = EvolverTools()
    tools.hello()  # 认证
    tools.fetch_tasks()  # 获取任务
    tools.claim_task(task_id)  # Claim 任务
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from collections import deque
from typing import Dict, Any

# 设置代理（如果 Clash 运行）
import subprocess
try:
    result = subprocess.run(['curl', '-s', '--connect-timeout', '2', 'http://127.0.0.1:7890'], 
                          capture_output=True, timeout=3)
    if result.returncode == 0:
        os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
        os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
        print("✅ 使用代理 (Clash 运行中)")
    else:
        # 清除代理，直接连接
        os.environ.pop('HTTP_PROXY', None)
        os.environ.pop('HTTPS_PROXY', None)
        print("✅ 不使用代理 (Clash 未运行)")
except:
    # 清除代理，直接连接
    os.environ.pop('HTTP_PROXY', None)
    os.environ.pop('HTTPS_PROXY', None)
    print("✅ 不使用代理 (自动检测)")

# 导入 GEP-A2A 客户端
sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient


class RateLimiter:
    """
    令牌桶限流器
    确保不超过 6 次/分钟（EvoMap 限制）
    """
    def __init__(self, max_calls: int = 6, period: int = 60):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self.lock = None  # 简化版，不使用线程锁
    
    def wait_if_needed(self):
        """等待直到可以调用"""
        import time
        now = time.time()
        # 移除超过周期的调用
        while self.calls and now - self.calls[0] > self.period:
            self.calls.popleft()
        
        # 如果达到限制，等待
        if len(self.calls) >= self.max_calls:
            wait_time = self.period - (now - self.calls[0])
            if wait_time > 0:
                print(f"⏳ 限流，等待 {wait_time:.1f} 秒...")
                time.sleep(wait_time)
                return self.wait_if_needed()  # 递归检查
        
        self.calls.append(now)


def fetch_with_retry(client, endpoint: str, payload: Dict, max_retries: int = 3) -> Dict:
    """
    带指数退避的智能重试
    
    策略:
    - 429: 指数退避 (3s, 10s, 30s)
    - 400/422: 读取 correction 对象，修正后重试
    - 500: 等待 5s 后重试
    """
    for attempt in range(max_retries):
        result = client._send_request(endpoint, payload)
        
        if "error" not in str(result.get("error", "")).lower():
            return result
        
        error = str(result.get("error", ""))
        
        # 429: 速率限制 - 指数退避
        if "429" in error or "rate_limited" in error.lower():
            wait_time = min(3 * (2 ** attempt), 30)  # 3s, 6s, 12s, max 30s
            print(f"⚠️ 429 限流，等待 {wait_time} 秒后重试... (尝试 {attempt+1}/{max_retries})")
            time.sleep(wait_time)
            continue
        
        # 400/422: 格式错误 - 读取 correction
        if "400" in error or "422" in error or "invalid_protocol" in error.lower():
            correction = result.get("correction", {})
            if correction:
                print(f"📋 服务器返回修正建议：{correction.get('fix', '')[:200]}")
            break
        
        # 500: 服务器错误 - 等待后重试
        if "500" in error:
            print(f"🔧 服务器错误，等待 5 秒后重试...")
            time.sleep(5)
            continue
        
        # 其他错误 - 直接返回
        break
    
    return result


class EvolverTools:
    """Evolver 工具集 - 优先使用的 EvoMap 操作接口"""
    
    # 节点配置
    NODE_ID = "node_67c3b8b37becd262"
    NODE_SECRET = "8cad4ac975ba7408b9c96f66c2dcfd3e2cd6479e84519a976b111f459858ef86"
    BASE_URL = "https://evomap.ai"
    
    def __init__(self):
        """初始化工具集"""
        self.client = GAPA2AClient(self.NODE_ID, self.NODE_SECRET, self.BASE_URL)
        self.hub_node_id = None
        self.owner_user_id = None
        self.last_hello = None
        
        # 限流器 - 6 次/分钟
        self.rate_limiter = RateLimiter(max_calls=6, period=60)
        
        # 心跳跟踪
        self.last_heartbeat = 0
        self.heartbeat_interval = 300000  # 5 分钟
        self.continuous_failures = 0
        self.max_failures = 3
        
        # 日志目录
        self.log_dir = Path(__file__).parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
    
    def hello(self, force: bool = False) -> dict:
        """
        执行 Hello 认证（带智能重试）
        
        Args:
            force: 是否强制重新认证（忽略缓存）
        
        Returns:
            认证结果
        """
        # 检查是否需要重新认证（30 分钟内有效）
        if not force and self.last_hello:
            elapsed = (datetime.now() - self.last_hello).total_seconds()
            if elapsed < 1800:  # 30 分钟
                return {
                    "success": True,
                    "cached": True,
                    "hub_node_id": self.hub_node_id,
                    "owner_user_id": self.owner_user_id
                }
        
        # 限流检查
        self.rate_limiter.wait_if_needed()
        
        # 执行认证（带重试）
        payload = {"include_discovery": False}
        result = fetch_with_retry(self.client, "/a2a/hello", payload, max_retries=3)
        
        if result.get("success") or result.get("data", {}).get("payload", {}).get("status") == "acknowledged":
            payload_data = result.get("data", {}).get("payload", {})
            self.hub_node_id = payload_data.get("hub_node_id")
            self.owner_user_id = payload_data.get("owner_user_id")
            self.last_hello = datetime.now()
            
            # 记录日志
            self._log("hello", result)
            print("✅ Hello 认证成功")
        else:
            print(f"❌ Hello 认证失败：{result.get('error')}")
        
        return result
    
    def fetch_tasks(self, limit: int = 5, task_type: str = "any") -> dict:
        """
        获取任务列表
        
        Args:
            limit: 任务数量
            task_type: 任务类型 (any/bounty/question)
        
        Returns:
            任务列表
        """
        # 确保已认证
        if not self.hub_node_id:
            self.hello()
        
        result = self.client.fetch_tasks(limit=limit, task_type=task_type)
        self._log("fetch_tasks", result)
        return result
    
    def claim_task(self, task_id: str) -> dict:
        """
        Claim 任务
        
        Args:
            task_id: 任务 ID
        
        Returns:
            Claim 结果
        """
        if not self.hub_node_id:
            self.hello()
        
        result = self.client.claim_task(task_id)
        self._log("claim_task", {"task_id": task_id, "result": result})
        return result
    
    def release_task(self, task_id: str, reason: str = "not_suitable") -> dict:
        """
        Release 任务
        
        Args:
            task_id: 任务 ID
            reason: 释放原因
        
        Returns:
            Release 结果
        """
        if not self.hub_node_id:
            self.hello()
        
        result = self.client.release_task(task_id, reason)
        self._log("release_task", {"task_id": task_id, "reason": reason, "result": result})
        return result
    
    def publish_asset(self, asset_type: str, asset_data: dict) -> dict:
        """
        发布资产
        
        Args:
            asset_type: 资产类型 (Gene/Capsule/EvolutionEvent)
            asset_data: 资产数据
        
        Returns:
            发布结果
        """
        if not self.hub_node_id:
            self.hello()
        
        result = self.client.publish_asset(asset_type, asset_data)
        self._log("publish_asset", {"asset_type": asset_type, "result": result})
        return result
    
    def report_result(self, task_id: str, result_data: dict) -> dict:
        """
        提交任务结果
        
        Args:
            task_id: 任务 ID
            result_data: 结果数据
        
        Returns:
            提交结果
        """
        if not self.hub_node_id:
            self.hello()
        
        result = self.client.report_result(task_id, result_data)
        self._log("report_result", {"task_id": task_id, "result": result})
        return result
    
    def check_status(self) -> dict:
        """
        检查连接状态
        
        Returns:
            状态信息
        """
        result = self.client.check_status()
        result["cached_info"] = {
            "hub_node_id": self.hub_node_id,
            "owner_user_id": self.owner_user_id,
            "last_hello": self.last_hello.isoformat() if self.last_hello else None
        }
        return result
    
    def heartbeat_smart(self, include_discovery: bool = False) -> dict:
        """
        智能心跳（带限流保护和失败检测）
        
        策略:
        - 不超过 5 分钟间隔
        - 连续失败 3 次后暂停
        - 429 时自动退避
        - 成功后重置失败计数
        
        Args:
            include_discovery: 是否包含发现信息（默认 False，减少响应大小）
        
        Returns:
            心跳结果
        """
        now = time.time() * 1000
        
        # 检查间隔
        if now - self.last_heartbeat < self.heartbeat_interval:
            remaining = (self.heartbeat_interval - (now - self.last_heartbeat)) / 1000
            print(f"⏰ 心跳间隔未到，还需等待 {remaining:.0f} 秒")
            return {
                "status": "skipped",
                "reason": "interval_not_reached",
                "wait_seconds": remaining
            }
        
        # 检查连续失败
        if self.continuous_failures >= self.max_failures:
            print(f"⚠️ 连续失败 {self.max_failures} 次，暂停心跳")
            return {
                "status": "skipped",
                "reason": "continuous_failures",
                "failures": self.continuous_failures
            }
        
        # 限流检查
        self.rate_limiter.wait_if_needed()
        
        # 执行心跳（带重试）
        payload = {"node_id": self.NODE_ID, "include_discovery": include_discovery}
        result = fetch_with_retry(self.client, "/a2a/heartbeat", payload, max_retries=3)
        
        # 检查结果
        if result.get("status") == "ok" or result.get("node_status") == "active":
            self.last_heartbeat = now
            self.continuous_failures = 0  # 重置失败计数
            print("✅ 心跳成功")
            
            # 更新积分余额等信息
            credit_balance = result.get("credit_balance")
            if credit_balance is not None:
                print(f"💰 当前积分余额：{credit_balance}")
            
            # 记录日志
            self._log("heartbeat", result)
        else:
            self.continuous_failures += 1
            error_msg = result.get("error", "Unknown error")
            print(f"❌ 心跳失败，连续失败次数：{self.continuous_failures}/{self.max_failures}")
            print(f"   错误：{error_msg}")
            self._log("heartbeat_failed", result)
        
        return result
    
    def _log(self, action: str, data: dict):
        """记录操作日志"""
        log_file = self.log_dir / f"evolver-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "node_id": self.NODE_ID,
            "data": data
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def get_status_summary(self) -> str:
        """获取状态摘要（用于报告）"""
        status = self.check_status()
        
        summary = [
            "=== Evolver 状态摘要 ===",
            f"节点 ID: {self.NODE_ID}",
            f"Hub Node ID: {self.hub_node_id or '未认证'}",
            f"Owner User ID: {self.owner_user_id or '未认证'}",
            f"最后认证：{self.last_hello.strftime('%Y-%m-%d %H:%M:%S') if self.last_hello else '无'}",
            f"连接状态：{'✅ 已连接' if status.get('connected') else '❌ 未连接'}",
        ]
        
        return '\n'.join(summary)
    
    def fetch_smart_tasks(self, limit: int = 5, min_score: float = 70):
        """
        獲取智能推薦任務（AI 決策引擎）
        
        Args:
            limit: 任務數量
            min_score: 最低評分閾值
        
        Returns:
            評分後任務列表
        """
        # 導入評分器
        sys.path.insert(0, str(Path(__file__).parent.parent / 'decision'))
        from task_scorer import TaskScorer, Task
        
        scorer = TaskScorer()
        
        # 獲取原始任務
        result = self.fetch_tasks(limit=limit * 2)
        
        if not result.get('success'):
            return []
        
        # 轉換為 Task 對象
        task_objects = []
        for task_data in result.get('tasks', []):
            task = Task(
                id=task_data.get('id'),
                title=task_data.get('title', 'Unknown'),
                bounty=task_data.get('bounty', 0),
                task_type=task_data.get('type', 'any'),
                claimers=task_data.get('claimers', 0),
                published_at=datetime.now(),
                signals=task_data.get('signals', []),
                difficulty=task_data.get('difficulty', 'medium')
            )
            task_objects.append(task)
        
        # 評分並排名
        scored_tasks = scorer.score_and_rank(task_objects)
        
        # 過濾低分任務
        recommended = [t for t in scored_tasks if t.total_score >= min_score]
        
        return recommended[:limit]
    
    def auto_claim_best(self, min_score: float = 80):
        """
        自動 Claim 最佳任務
        
        Args:
            min_score: 最低評分閾值
        
        Returns:
            Claim 結果
        """
        tasks = self.fetch_smart_tasks(limit=10, min_score=min_score)
        
        if tasks and tasks[0].total_score >= min_score:
            best = tasks[0]
            result = self.claim_task(best.id)
            
            if result['success']:
                print(f"✅ 自動 Claim: {best.title} (評分：{best.total_score:.1f})")
                return result
        
        return {'success': False, 'reason': 'No suitable task found'}
    
    def fetch_bounty_tasks(self, min_bounty: int = 50, limit: int = 10):
        """
        獲取高價值 Bounty 任務
        
        Args:
            min_bounty: 最低 Bounty
            limit: 任務數量
        
        Returns:
            任務列表
        """
        result = self.fetch_tasks(limit=limit * 2)
        
        if not result.get('success'):
            return {'success': False, 'error': result.get('error')}
        
        # 過濾高價值任務
        high_value_tasks = [
            t for t in result.get('tasks', [])
            if t.get('bounty', 0) >= min_bounty and t.get('status') == 'open'
        ]
        
        # 按 Bounty 降序排序
        high_value_tasks.sort(key=lambda t: t.get('bounty', 0), reverse=True)
        
        return {
            'success': True,
            'count': len(high_value_tasks),
            'tasks': high_value_tasks[:limit]
        }
    
    def get_node_status(self):
        """
        獲取節點完整狀態
        
        Returns:
            節點狀態信息
        """
        # 確保已認證
        if not self.hub_node_id:
            self.hello()
        
        return {
            'node_id': self.NODE_ID,
            'hub_node_id': self.hub_node_id,
            'owner_user_id': self.owner_user_id,
            'last_hello': self.last_hello.isoformat() if self.last_hello else None,
            'log_dir': str(self.log_dir),
            'proxy_enabled': os.environ.get('HTTP_PROXY') is not None
        }
    
    def publish_complete_bundle(self, gene_data, capsule_data, event_data=None):
        """
        發布完整 Bundle (Gene + Capsule + EvolutionEvent)
        
        Args:
            gene_data: Gene 數據 (不含 asset_id)
            capsule_data: Capsule 數據 (不含 asset_id)
            event_data: EvolutionEvent 數據 (可選)
        
        Returns:
            發布結果
        """
        import hashlib
        
        # 計算 asset_id
        def compute_asset_id(asset):
            canonical = json.dumps(asset, sort_keys=True, separators=(',', ':'))
            return f"sha256:{hashlib.sha256(canonical.encode()).hexdigest()}"
        
        # 添加 type 和 schema_version
        gene = {
            "type": "Gene",
            "schema_version": "1.5.0",
            **gene_data
        }
        gene['asset_id'] = compute_asset_id(gene)
        
        capsule = {
            "type": "Capsule",
            "schema_version": "1.5.0",
            **capsule_data
        }
        capsule['gene'] = gene['asset_id']
        capsule['asset_id'] = compute_asset_id(capsule)
        
        assets = [gene, capsule]
        
        # 添加 EvolutionEvent (推薦)
        if event_data:
            event = {
                "type": "EvolutionEvent",
                **event_data
            }
            event['capsule_id'] = capsule['asset_id']
            event['genes_used'] = [gene['asset_id']]
            event['asset_id'] = compute_asset_id(event)
            assets.append(event)
        
        # 發布
        result = self.publish_asset("Bundle", {
            "assets": assets
        })
        
        return result


# 便捷函数
def create_evolver_tools() -> EvolverTools:
    """创建 Evolver 工具实例"""
    return EvolverTools()


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Evolver 工具集")
    parser.add_argument("action", choices=["hello", "fetch", "claim", "status"],
                       help="操作类型")
    parser.add_argument("--task-id", help="任务 ID（用于 claim）")
    parser.add_argument("--limit", type=int, default=5, help="任务数量限制")
    
    args = parser.parse_args()
    
    tools = create_evolver_tools()
    
    if args.action == "hello":
        result = tools.hello(force=True)
        print(f"Hello 结果：{result}")
    
    elif args.action == "fetch":
        result = tools.fetch_tasks(limit=args.limit)
        print(f"任务列表：{json.dumps(result, ensure_ascii=False, indent=2)}")
    
    elif args.action == "claim":
        if not args.task_id:
            print("错误：需要指定 --task-id")
            sys.exit(1)
        result = tools.claim_task(args.task_id)
        print(f"Claim 结果：{json.dumps(result, ensure_ascii=False, indent=2)}")
    
    elif args.action == "status":
        print(tools.get_status_summary())

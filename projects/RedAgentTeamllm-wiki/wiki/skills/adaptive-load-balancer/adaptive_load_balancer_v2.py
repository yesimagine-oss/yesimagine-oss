#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自适应负载均衡器 v2.0 - 增强版

新增功能:
- QPS 追踪和速率限制
- 错误率滑动窗口
- 自定义权重因子
- 实时指标导出（Prometheus 格式）
- 自动熔断机制
- 请求优先级队列

使用示例:
    from adaptive_load_balancer_v2 import AdaptiveLoadBalancerV2
    
    lb = AdaptiveLoadBalancerV2(
        error_window_seconds=60,
        qps_limit=1000,
        circuit_breaker_threshold=0.5
    )
"""

import time
import hashlib
import random
import logging
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import json

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent 健康状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OPEN_CIRCUIT = "open_circuit"  # 熔断
    UNKNOWN = "unknown"


class RequestPriority(Enum):
    """请求优先级"""
    LOW = 1
    NORMAL = 5
    HIGH = 10
    CRITICAL = 20


@dataclass
class MetricPoint:
    """指标数据点"""
    timestamp: datetime
    value: float


@dataclass
class AgentMetrics:
    """增强版 Agent 性能指标"""
    agent_id: str
    endpoint: str
    
    # 基础指标
    active_connections: int = 0
    total_requests: int = 0
    failed_requests: int = 0
    
    # 响应时间（EWMA）
    avg_response_time: float = 0.0
    last_response_time: float = 0.0
    p99_response_time: float = 0.0
    
    # QPS 追踪
    qps_window: deque = field(default_factory=lambda: deque(maxlen=1000))
    current_qps: float = 0.0
    peak_qps: float = 0.0
    
    # 错误率（滑动窗口）
    error_window: deque = field(default_factory=lambda: deque(maxlen=1000))
    error_rate: float = 0.0
    
    # 健康状态
    health_score: float = 1.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_io: float = 0.0
    network_io: float = 0.0
    
    # 时间追踪
    last_seen: datetime = field(default_factory=datetime.utcnow)
    last_health_check: datetime = field(default_factory=datetime.utcnow)
    status: AgentStatus = AgentStatus.UNKNOWN
    consecutive_failures: int = 0
    
    # 熔断器
    circuit_state: str = "closed"  # closed/open/half-open
    circuit_failures: int = 0
    circuit_last_failure: Optional[datetime] = None
    
    # 权重和分数
    weight: float = 1.0
    score: float = 0.0
    
    # 自定义权重因子
    custom_factors: Dict[str, float] = field(default_factory=dict)
    
    def record_request(self, success: bool, response_time: float, timestamp: Optional[datetime] = None):
        """记录请求（包含 QPS 和错误率）"""
        ts = timestamp or datetime.utcnow()
        
        # 基础计数
        self.total_requests += 1
        if not success:
            self.failed_requests += 1
            self.consecutive_failures += 1
        else:
            self.consecutive_failures = 0
        
        # QPS 追踪
        self.qps_window.append(ts)
        self._update_qps()
        
        # 错误率滑动窗口
        self.error_window.append((ts, success))
        self._update_error_rate()
        
        # 响应时间
        self.update_response_time(response_time)
        
        # 更新健康状态
        self.last_seen = ts
        self._update_health()
        self._update_circuit_breaker()
    
    def _update_qps(self):
        """更新 QPS"""
        now = datetime.utcnow()
        # 计算最近 1 秒的请求数
        one_second_ago = now - timedelta(seconds=1)
        recent_requests = sum(1 for ts in self.qps_window if ts > one_second_ago)
        self.current_qps = recent_requests
        self.peak_qps = max(self.peak_qps, self.current_qps)
    
    def _update_error_rate(self):
        """更新错误率（最近 60 秒）"""
        now = datetime.utcnow()
        one_minute_ago = now - timedelta(seconds=60)
        recent = [(ts, s) for ts, s in self.error_window if ts > one_minute_ago]
        if recent:
            errors = sum(1 for _, s in recent if not s)
            self.error_rate = errors / len(recent)
        else:
            self.error_rate = 0.0
    
    def update_response_time(self, rt: float, alpha: float = 0.3):
        """更新 EWMA 响应时间"""
        if self.avg_response_time == 0:
            self.avg_response_time = rt
        else:
            self.avg_response_time = alpha * rt + (1 - alpha) * self.avg_response_time
        self.last_response_time = rt
    
    def _update_health(self):
        """更新健康状态"""
        recency_factor = 1.0 if (datetime.utcnow() - self.last_seen).seconds < 60 else 0.5
        self.health_score = (1 - self.error_rate) * recency_factor
        
        # 状态判断
        if self.circuit_state == "open":
            self.status = AgentStatus.OPEN_CIRCUIT
        elif self.consecutive_failures >= 3 or self.error_rate > 0.5:
            self.status = AgentStatus.UNHEALTHY
        elif self.consecutive_failures >= 1 or self.error_rate > 0.1:
            self.status = AgentStatus.DEGRADED
        else:
            self.status = AgentStatus.HEALTHY
    
    def _update_circuit_breaker(self, threshold: float = 0.5, reset_timeout: int = 30):
        """更新熔断器状态"""
        now = datetime.utcnow()
        
        if self.circuit_state == "open":
            # 检查是否应该尝试恢复
            if self.circuit_last_failure and (now - self.circuit_last_failure).seconds > reset_timeout:
                self.circuit_state = "half-open"
                logger.info(f"Circuit breaker half-open for {self.agent_id}")
        elif self.error_rate > threshold:
            # 打开熔断器
            self.circuit_state = "open"
            self.circuit_last_failure = now
            self.circuit_failures += 1
            logger.warning(f"Circuit breaker opened for {self.agent_id} (error_rate={self.error_rate:.2%})")
    
    def calculate_weight(self, qps_weight: float = 0.2, error_weight: float = 0.3) -> float:
        """计算动态权重（增强版）"""
        # 基础权重
        base = 1.0
        
        # 健康因子
        health_factor = self.health_score
        
        # 错误率因子（新增）
        error_factor = 1 - self.error_rate
        
        # 容量因子
        capacity_factor = 1.0 - max(self.cpu_usage, self.memory_usage)
        
        # 负载因子
        load_factor = 1.0 / (1 + self.active_connections)
        
        # QPS 因子（新增）- 避免过载
        qps_factor = 1.0 / (1 + self.current_qps / 100)  # 归一化到 100 QPS
        
        # 响应时间因子
        rt_factor = 1.0 / (1 + self.avg_response_time / 1000)
        
        # 自定义因子
        custom_factor = 1.0
        if self.custom_factors:
            custom_factor = sum(self.custom_factors.values()) / len(self.custom_factors)
        
        # 综合权重
        weight = (
            base *
            health_factor *
            (error_factor ** error_weight) *
            capacity_factor *
            load_factor *
            (qps_factor ** qps_weight) *
            rt_factor *
            custom_factor
        )
        
        self.weight = weight
        return weight
    
    def calculate_score(self) -> float:
        """计算选择分数（越低越好）"""
        if self.weight <= 0 or self.circuit_state == "open":
            self.score = float('inf')
        else:
            self.score = (self.active_connections + 1) / self.weight * (1 + self.avg_response_time / 1000)
        return self.score
    
    def reset_circuit(self):
        """重置熔断器"""
        self.circuit_state = "closed"
        self.circuit_failures = 0
        self.circuit_last_failure = None
        logger.info(f"Circuit breaker reset for {self.agent_id}")
    
    def to_prometheus(self) -> str:
        """导出为 Prometheus 指标格式"""
        labels = f'agent_id="{self.agent_id}",endpoint="{self.endpoint}"'
        metrics = [
            f'agent_active_connections{{{labels}}} {self.active_connections}',
            f'agent_total_requests{{{labels}}} {self.total_requests}',
            f'agent_failed_requests{{{labels}}} {self.failed_requests}',
            f'agent_error_rate{{{labels}}} {self.error_rate}',
            f'agent_avg_response_time_ms{{{labels}}} {self.avg_response_time}',
            f'agent_current_qps{{{labels}}} {self.current_qps}',
            f'agent_health_score{{{labels}}} {self.health_score}',
            f'agent_weight{{{labels}}} {self.weight}',
            f'agent_cpu_usage{{{labels}}} {self.cpu_usage}',
            f'agent_memory_usage{{{labels}}} {self.memory_usage}',
            f'agent_circuit_state{{{labels}}} {1 if self.circuit_state == "open" else 0}',
        ]
        return '\n'.join(metrics)


class RequestQueue:
    """优先级请求队列"""
    
    def __init__(self, max_size: int = 10000):
        self.queues: Dict[int, deque] = {
            priority.value: deque() for priority in RequestPriority
        }
        self.max_size = max_size
        self._lock = threading.Lock()
    
    def enqueue(self, request_data: dict, priority: RequestPriority = RequestPriority.NORMAL):
        """添加请求到队列"""
        with self._lock:
            if sum(len(q) for q in self.queues.values()) >= self.max_size:
                raise Exception("Queue full")
            self.queues[priority.value].append((datetime.utcnow(), request_data))
    
    def dequeue(self) -> Optional[Tuple[datetime, dict]]:
        """获取最高优先级的请求"""
        with self._lock:
            for priority in sorted(self.queues.keys(), reverse=True):
                if self.queues[priority]:
                    return self.queues[priority].popleft()
        return None
    
    def size(self) -> int:
        """队列大小"""
        return sum(len(q) for q in self.queues.values())


class AdaptiveLoadBalancerV2:
    """自适应负载均衡器 v2.0 - 增强版"""
    
    def __init__(
        self,
        health_check_interval: float = 5.0,
        weight_update_interval: float = 10.0,
        error_window_seconds: int = 60,
        qps_limit: float = 1000.0,
        circuit_breaker_threshold: float = 0.5,
        circuit_breaker_timeout: int = 30
    ):
        """
        初始化负载均衡器
        
        Args:
            health_check_interval: 健康检查间隔（秒）
            weight_update_interval: 权重更新间隔（秒）
            error_window_seconds: 错误率统计窗口（秒）
            qps_limit: QPS 限制
            circuit_breaker_threshold: 熔断器触发阈值（错误率）
            circuit_breaker_timeout: 熔断器超时（秒）
        """
        self.agents: Dict[str, AgentMetrics] = {}
        self.request_queue = RequestQueue()
        
        self.health_check_interval = health_check_interval
        self.weight_update_interval = weight_update_interval
        self.error_window_seconds = error_window_seconds
        self.qps_limit = qps_limit
        self.circuit_breaker_threshold = circuit_breaker_threshold
        self.circuit_breaker_timeout = circuit_breaker_timeout
        
        self._lock = threading.RLock()
        self._running = False
        self._background_thread: Optional[threading.Thread] = None
        
        # 指标历史
        self.metrics_history: Dict[str, deque] = {}
        
        logger.info("自适应负载均衡器 v2.0 初始化完成")
    
    def add_agent(self, agent_id: str, endpoint: str, custom_factors: Optional[Dict[str, float]] = None) -> bool:
        """添加 Agent"""
        with self._lock:
            if agent_id in self.agents:
                logger.warning(f"Agent {agent_id} 已存在")
                return False
            
            metrics = AgentMetrics(agent_id=agent_id, endpoint=endpoint)
            metrics.custom_factors = custom_factors or {}
            self.agents[agent_id] = metrics
            self.metrics_history[agent_id] = deque(maxlen=1000)
            
            logger.info(f"添加 Agent: {agent_id} @ {endpoint}")
            return True
    
    def remove_agent(self, agent_id: str) -> bool:
        """移除 Agent"""
        with self._lock:
            if agent_id not in self.agents:
                return False
            
            del self.agents[agent_id]
            del self.metrics_history[agent_id]
            
            logger.info(f"移除 Agent: {agent_id}")
            return True
    
    def select_agent(
        self,
        key: Optional[str] = None,
        priority: RequestPriority = RequestPriority.NORMAL,
        bypass_queue: bool = False
    ) -> Optional[str]:
        """
        选择最佳 Agent
        
        Args:
            key: 用于一致性哈希的 key
            priority: 请求优先级
            bypass_queue: 是否绕过队列直接选择
        
        Returns:
            选中的 agent_id
        """
        with self._lock:
            # 过滤健康的 Agent
            healthy_agents = [
                (aid, m) for aid, m in self.agents.items()
                if m.status not in [AgentStatus.UNHEALTHY, AgentStatus.OPEN_CIRCUIT]
            ]
            
            if not healthy_agents:
                logger.warning("没有健康的 Agent")
                return None
            
            # 检查 QPS 限制
            for aid, metrics in healthy_agents:
                if metrics.current_qps >= self.qps_limit:
                    metrics.status = AgentStatus.DEGRADED
            
            # 重新过滤
            healthy_agents = [
                (aid, m) for aid, m in healthy_agents
                if m.current_qps < self.qps_limit
            ]
            
            if not healthy_agents:
                # 如果所有 Agent 都达到 QPS 限制，加入队列
                if not bypass_queue:
                    logger.info("所有 Agent 达到 QPS 限制，请求加入队列")
                    return None
            
            # 选择最佳 Agent
            if not healthy_agents:
                logger.warning("没有可用的 Agent（所有 Agent 都不健康或达到 QPS 限制）")
                return None
            
            best_agent = min(healthy_agents, key=lambda x: x[1].calculate_score())[0]
            self.agents[best_agent].active_connections += 1
            
            logger.debug(f"选择 Agent: {best_agent} (score={self.agents[best_agent].score:.2f}, qps={self.agents[best_agent].current_qps:.1f})")
            return best_agent
    
    def record_request(self, agent_id: str, success: bool, response_time: float):
        """记录请求结果"""
        with self._lock:
            if agent_id not in self.agents:
                return
            
            metrics = self.agents[agent_id]
            metrics.record_request(success, response_time)
            metrics.active_connections = max(0, metrics.active_connections - 1)
            
            # 记录指标历史
            self.metrics_history[agent_id].append({
                'timestamp': datetime.utcnow().isoformat(),
                'qps': metrics.current_qps,
                'error_rate': metrics.error_rate,
                'response_time': metrics.avg_response_time,
                'weight': metrics.weight
            })
            
            logger.debug(f"Agent {agent_id}: {'成功' if success else '失败'} ({response_time:.2f}ms)")
    
    def update_weights(self):
        """更新所有 Agent 权重"""
        with self._lock:
            for metrics in self.agents.values():
                metrics.calculate_weight(
                    qps_weight=0.2,
                    error_weight=0.3
                )
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self._lock:
            return {
                "total_agents": len(self.agents),
                "healthy_agents": sum(1 for m in self.agents.values() if m.status == AgentStatus.HEALTHY),
                "degraded_agents": sum(1 for m in self.agents.values() if m.status == AgentStatus.DEGRADED),
                "unhealthy_agents": sum(1 for m in self.agents.values() if m.status == AgentStatus.UNHEALTHY),
                "open_circuit_agents": sum(1 for m in self.agents.values() if m.circuit_state == "open"),
                "queue_size": self.request_queue.size(),
                "agents": {
                    aid: {
                        "status": m.status.value,
                        "circuit_state": m.circuit_state,
                        "active_connections": m.active_connections,
                        "current_qps": f"{m.current_qps:.1f}",
                        "peak_qps": f"{m.peak_qps:.1f}",
                        "avg_response_time": f"{m.avg_response_time:.2f}ms",
                        "p99_response_time": f"{m.p99_response_time:.2f}ms",
                        "error_rate": f"{m.error_rate:.2%}",
                        "health_score": f"{m.health_score:.2f}",
                        "weight": f"{m.weight:.2f}",
                        "cpu_usage": f"{m.cpu_usage:.1%}",
                        "memory_usage": f"{m.memory_usage:.1%}",
                    }
                    for aid, m in self.agents.items()
                }
            }
    
    def export_prometheus_metrics(self) -> str:
        """导出 Prometheus 格式指标"""
        with self._lock:
            all_metrics = []
            for metrics in self.agents.values():
                all_metrics.append(metrics.to_prometheus())
            return '\n'.join(all_metrics)
    
    def get_scaling_recommendation(self) -> Dict:
        """获取弹性伸缩建议"""
        with self._lock:
            if not self.agents:
                return {"action": "none", "reason": "No agents"}
            
            avg_qps = sum(m.current_qps for m in self.agents.values()) / len(self.agents)
            avg_connections = sum(m.active_connections for m in self.agents.values()) / len(self.agents)
            avg_cpu = sum(m.cpu_usage for m in self.agents.values()) / len(self.agents)
            avg_memory = sum(m.memory_usage for m in self.agents.values()) / len(self.agents)
            avg_error_rate = sum(m.error_rate for m in self.agents.values()) / len(self.agents)
            
            # 高负载判断
            if avg_qps > self.qps_limit * 0.8 or avg_cpu > 0.8 or avg_memory > 0.8 or avg_error_rate > 0.1:
                return {
                    "action": "scale_up",
                    "reason": f"高负载：qps={avg_qps:.1f}, cpu={avg_cpu:.1%}, memory={avg_memory:.1%}, error_rate={avg_error_rate:.1%}",
                    "suggested_count": len(self.agents) + max(1, int(avg_qps / self.qps_limit))
                }
            
            # 低负载判断
            if avg_qps < self.qps_limit * 0.2 and avg_cpu < 0.3 and avg_memory < 0.3 and len(self.agents) > 1:
                return {
                    "action": "scale_down",
                    "reason": f"低负载：qps={avg_qps:.1f}, cpu={avg_cpu:.1%}, memory={avg_memory:.1%}",
                    "suggested_count": max(1, len(self.agents) - 1)
                }
            
            return {
                "action": "none",
                "reason": "负载正常",
                "current_count": len(self.agents)
            }
    
    def reset_circuit(self, agent_id: Optional[str] = None):
        """重置熔断器"""
        with self._lock:
            if agent_id:
                if agent_id in self.agents:
                    self.agents[agent_id].reset_circuit()
            else:
                for metrics in self.agents.values():
                    metrics.reset_circuit()
                logger.info("所有 Agent 熔断器已重置")


# 使用示例
if __name__ == "__main__":
    import random
    
    # 创建负载均衡器
    lb = AdaptiveLoadBalancerV2(
        qps_limit=100,
        circuit_breaker_threshold=0.3
    )
    
    # 添加模拟 Agent
    for i in range(5):
        lb.add_agent(f"agent_{i}", f"http://localhost:{8000 + i}")
    
    # 模拟请求
    print("模拟 500 个请求...")
    for i in range(500):
        agent_id = lb.select_agent(bypass_queue=True)
        if agent_id:
            # 模拟响应时间（50-200ms）
            rt = random.uniform(50, 200)
            # 模拟 5% 失败率
            success = random.random() > 0.05
            lb.record_request(agent_id, success, rt)
        
        if i % 100 == 0:
            stats = lb.get_stats()
            print(f"\n[{i} 请求] 健康：{stats['healthy_agents']}, 队列：{stats['queue_size']}")
    
    # 打印统计
    print("\n=== 负载均衡统计 ===")
    stats = lb.get_stats()
    print(f"总 Agent 数：{stats['total_agents']}")
    print(f"健康：{stats['healthy_agents']}")
    print(f"降级：{stats['degraded_agents']}")
    print(f"不健康：{stats['unhealthy_agents']}")
    print(f"熔断：{stats['open_circuit_agents']}")
    
    print("\nAgent 详情:")
    for aid, info in stats['agents'].items():
        print(f"  {aid}: {info['status']} | QPS:{info['current_qps']} | RT:{info['avg_response_time']} | 错误率:{info['error_rate']}")
    
    # Prometheus 指标
    print("\n=== Prometheus 指标 ===")
    print(lb.export_prometheus_metrics()[:1000])
    
    # 伸缩建议
    scaling = lb.get_scaling_recommendation()
    print(f"\n伸缩建议：{scaling['action']} - {scaling['reason']}")

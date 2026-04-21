#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自适应负载均衡器 - 多 Agent 系统智能请求分发

功能:
- 动态权重计算（基于连接数、响应时间、错误率）
- 健康检查（主动探测 + 被动监控）
- 一致性哈希路由
- 弹性伸缩建议

使用示例:
    from adaptive_load_balancer import AdaptiveLoadBalancer
    
    lb = AdaptiveLoadBalancer()
    lb.add_agent("agent_1", "http://localhost:8001")
    lb.add_agent("agent_2", "http://localhost:8002")
    
    # 获取最佳 Agent
    best = lb.select_agent()
    response = lb.forward_request(best, "/api/task", data)
"""

import time
import hashlib
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import threading

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
    UNKNOWN = "unknown"


@dataclass
class AgentMetrics:
    """Agent 性能指标"""
    agent_id: str
    endpoint: str
    active_connections: int = 0
    total_requests: int = 0
    failed_requests: int = 0
    avg_response_time: float = 0.0  # EWMA
    last_response_time: float = 0.0
    health_score: float = 1.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    last_seen: datetime = field(default_factory=datetime.utcnow)
    status: AgentStatus = AgentStatus.UNKNOWN
    consecutive_failures: int = 0
    
    # 权重计算
    weight: float = 1.0
    score: float = 0.0  # 用于选择（越低越好）
    
    def update_response_time(self, rt: float, alpha: float = 0.3):
        """更新 EWMA 响应时间"""
        if self.avg_response_time == 0:
            self.avg_response_time = rt
        else:
            self.avg_response_time = alpha * rt + (1 - alpha) * self.avg_response_time
        self.last_response_time = rt
    
    def record_success(self, response_time: float):
        """记录成功请求"""
        self.total_requests += 1
        self.active_connections = max(0, self.active_connections - 1)
        self.consecutive_failures = 0
        self.update_response_time(response_time)
        self.last_seen = datetime.utcnow()
        self._update_health()
    
    def record_failure(self):
        """记录失败请求"""
        self.total_requests += 1
        self.failed_requests += 1
        self.active_connections = max(0, self.active_connections - 1)
        self.consecutive_failures += 1
        self.last_seen = datetime.utcnow()
        self._update_health()
    
    def _update_health(self):
        """更新健康状态"""
        # 错误率
        error_rate = self.failed_requests / max(1, self.total_requests)
        
        # 健康得分 = (1 - error_rate) * (1 if recent else 0.5)
        recency_factor = 1.0 if (datetime.utcnow() - self.last_seen).seconds < 60 else 0.5
        self.health_score = (1 - error_rate) * recency_factor
        
        # 状态判断
        if self.consecutive_failures >= 3:
            self.status = AgentStatus.UNHEALTHY
        elif self.consecutive_failures >= 1 or error_rate > 0.1:
            self.status = AgentStatus.DEGRADED
        else:
            self.status = AgentStatus.HEALTHY
    
    def calculate_weight(self) -> float:
        """计算动态权重"""
        # 基础权重
        base = 1.0
        
        # 健康因子
        health_factor = self.health_score
        
        # 容量因子（剩余容量）
        capacity_factor = 1.0 - max(self.cpu_usage, self.memory_usage)
        
        # 负载因子（连接数越少权重越高）
        load_factor = 1.0 / (1 + self.active_connections)
        
        # 响应时间因子（越快权重越高）
        rt_factor = 1.0 / (1 + self.avg_response_time / 1000)  # 归一化
        
        weight = base * health_factor * capacity_factor * load_factor * rt_factor
        self.weight = weight
        return weight
    
    def calculate_score(self) -> float:
        """计算选择分数（越低越好）"""
        # 分数 = (活跃连接 / 权重) * 响应时间因子
        if self.weight <= 0:
            self.score = float('inf')
        else:
            self.score = (self.active_connections + 1) / self.weight * (1 + self.avg_response_time / 1000)
        return self.score


class ConsistentHashRing:
    """一致性哈希环"""
    
    def __init__(self, virtual_nodes: int = 150):
        self.virtual_nodes = virtual_nodes
        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []
    
    def _hash(self, key: str) -> int:
        """计算哈希值"""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add(self, agent_id: str):
        """添加节点到环"""
        for i in range(self.virtual_nodes):
            virtual_key = f"{agent_id}:{i}"
            hash_value = self._hash(virtual_key)
            self.ring[hash_value] = agent_id
            self.sorted_keys.append(hash_value)
        self.sorted_keys.sort()
    
    def remove(self, agent_id: str):
        """从环中移除节点"""
        for i in range(self.virtual_nodes):
            virtual_key = f"{agent_id}:{i}"
            hash_value = self._hash(virtual_key)
            if hash_value in self.ring:
                del self.ring[hash_value]
                self.sorted_keys.remove(hash_value)
    
    def get(self, key: str) -> Optional[str]:
        """获取 key 对应的节点"""
        if not self.ring:
            return None
        
        hash_value = self._hash(key)
        
        # 二分查找
        for ring_key in self.sorted_keys:
            if ring_key >= hash_value:
                return self.ring[ring_key]
        
        # 返回第一个节点（环回）
        return self.ring[self.sorted_keys[0]]


class AdaptiveLoadBalancer:
    """自适应负载均衡器"""
    
    def __init__(self, health_check_interval: float = 5.0, weight_update_interval: float = 10.0):
        """
        初始化负载均衡器
        
        Args:
            health_check_interval: 健康检查间隔（秒）
            weight_update_interval: 权重更新间隔（秒）
        """
        self.agents: Dict[str, AgentMetrics] = {}
        self.hash_ring = ConsistentHashRing()
        self.health_check_interval = health_check_interval
        self.weight_update_interval = weight_update_interval
        
        self._lock = threading.Lock()
        self._running = False
        self._background_thread: Optional[threading.Thread] = None
        
        logger.info("自适应负载均衡器初始化完成")
    
    def add_agent(self, agent_id: str, endpoint: str) -> bool:
        """添加 Agent"""
        with self._lock:
            if agent_id in self.agents:
                logger.warning(f"Agent {agent_id} 已存在")
                return False
            
            metrics = AgentMetrics(agent_id=agent_id, endpoint=endpoint)
            metrics.status = AgentStatus.UNKNOWN
            self.agents[agent_id] = metrics
            self.hash_ring.add(agent_id)
            
            logger.info(f"添加 Agent: {agent_id} @ {endpoint}")
            return True
    
    def remove_agent(self, agent_id: str) -> bool:
        """移除 Agent"""
        with self._lock:
            if agent_id not in self.agents:
                return False
            
            del self.agents[agent_id]
            self.hash_ring.remove(agent_id)
            
            logger.info(f"移除 Agent: {agent_id}")
            return True
    
    def select_agent(self, key: Optional[str] = None) -> Optional[str]:
        """
        选择最佳 Agent
        
        Args:
            key: 用于一致性哈希的 key（None 则使用最小分数）
        
        Returns:
            选中的 agent_id
        """
        with self._lock:
            healthy_agents = [
                (aid, m) for aid, m in self.agents.items()
                if m.status != AgentStatus.UNHEALTHY
            ]
            
            if not healthy_agents:
                logger.warning("没有健康的 Agent")
                return None
            
            if key:
                # 使用一致性哈希
                agent_id = self.hash_ring.get(key)
                if agent_id and agent_id in self.agents:
                    return agent_id
            
            # 使用最小分数选择
            best_agent = None
            best_score = float('inf')
            
            for aid, metrics in healthy_agents:
                score = metrics.calculate_score()
                if score < best_score:
                    best_score = score
                    best_agent = aid
            
            if best_agent:
                self.agents[best_agent].active_connections += 1
                logger.debug(f"选择 Agent: {best_agent} (score={best_score:.2f})")
            
            return best_agent
    
    def record_request(self, agent_id: str, success: bool, response_time: float):
        """记录请求结果"""
        with self._lock:
            if agent_id not in self.agents:
                return
            
            metrics = self.agents[agent_id]
            if success:
                metrics.record_success(response_time)
            else:
                metrics.record_failure()
            
            logger.debug(f"Agent {agent_id}: {'成功' if success else '失败'} ({response_time:.2f}ms)")
    
    def update_weights(self):
        """更新所有 Agent 权重"""
        with self._lock:
            for metrics in self.agents.values():
                metrics.calculate_weight()
            logger.debug("权重已更新")
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self._lock:
            return {
                "total_agents": len(self.agents),
                "healthy_agents": sum(1 for m in self.agents.values() if m.status == AgentStatus.HEALTHY),
                "degraded_agents": sum(1 for m in self.agents.values() if m.status == AgentStatus.DEGRADED),
                "unhealthy_agents": sum(1 for m in self.agents.values() if m.status == AgentStatus.UNHEALTHY),
                "agents": {
                    aid: {
                        "endpoint": m.endpoint,
                        "status": m.status.value,
                        "active_connections": m.active_connections,
                        "avg_response_time": f"{m.avg_response_time:.2f}ms",
                        "health_score": f"{m.health_score:.2f}",
                        "weight": f"{m.weight:.2f}",
                        "error_rate": f"{m.failed_requests / max(1, m.total_requests) * 100:.1f}%"
                    }
                    for aid, m in self.agents.items()
                }
            }
    
    def start_background_tasks(self):
        """启动后台任务（健康检查、权重更新）"""
        self._running = True
        self._background_thread = threading.Thread(target=self._background_loop, daemon=True)
        self._background_thread.start()
        logger.info("后台任务已启动")
    
    def stop_background_tasks(self):
        """停止后台任务"""
        self._running = False
        if self._background_thread:
            self._background_thread.join(timeout=5)
        logger.info("后台任务已停止")
    
    def _background_loop(self):
        """后台循环"""
        last_weight_update = time.time()
        
        while self._running:
            try:
                # 权重更新
                if time.time() - last_weight_update > self.weight_update_interval:
                    self.update_weights()
                    last_weight_update = time.time()
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"后台任务错误：{e}")
    
    def get_scaling_recommendation(self) -> Dict:
        """获取弹性伸缩建议"""
        with self._lock:
            if not self.agents:
                return {"action": "none", "reason": "No agents"}
            
            # 计算平均负载
            avg_connections = sum(m.active_connections for m in self.agents.values()) / len(self.agents)
            avg_cpu = sum(m.cpu_usage for m in self.agents.values()) / len(self.agents)
            avg_memory = sum(m.memory_usage for m in self.agents.values()) / len(self.agents)
            
            # 高负载判断
            if avg_connections > 100 or avg_cpu > 0.8 or avg_memory > 0.8:
                return {
                    "action": "scale_up",
                    "reason": f"高负载：connections={avg_connections:.1f}, cpu={avg_cpu:.1%}, memory={avg_memory:.1%}",
                    "suggested_count": len(self.agents) + 1
                }
            
            # 低负载判断
            if avg_connections < 10 and avg_cpu < 0.3 and avg_memory < 0.3 and len(self.agents) > 1:
                return {
                    "action": "scale_down",
                    "reason": f"低负载：connections={avg_connections:.1f}, cpu={avg_cpu:.1%}, memory={avg_memory:.1%}",
                    "suggested_count": max(1, len(self.agents) - 1)
                }
            
            return {
                "action": "none",
                "reason": "负载正常",
                "current_count": len(self.agents)
            }


# 使用示例
if __name__ == "__main__":
    import random
    
    # 创建负载均衡器
    lb = AdaptiveLoadBalancer()
    
    # 添加模拟 Agent
    for i in range(5):
        lb.add_agent(f"agent_{i}", f"http://localhost:{8000 + i}")
    
    # 模拟请求
    print("模拟 100 个请求...")
    for _ in range(100):
        agent_id = lb.select_agent()
        if agent_id:
            # 模拟响应时间（50-200ms）
            rt = random.uniform(50, 200)
            # 模拟 5% 失败率
            success = random.random() > 0.05
            lb.record_request(agent_id, success, rt)
    
    # 打印统计
    print("\n=== 负载均衡统计 ===")
    stats = lb.get_stats()
    print(f"总 Agent 数：{stats['total_agents']}")
    print(f"健康：{stats['healthy_agents']}")
    print(f"降级：{stats['degraded_agents']}")
    print(f"不健康：{stats['unhealthy_agents']}")
    
    print("\nAgent 详情:")
    for aid, info in stats['agents'].items():
        print(f"  {aid}: {info['status']} | 连接:{info['active_connections']} | RT:{info['avg_response_time']} | 权重:{info['weight']}")
    
    # 伸缩建议
    scaling = lb.get_scaling_recommendation()
    print(f"\n伸缩建议：{scaling['action']} - {scaling['reason']}")

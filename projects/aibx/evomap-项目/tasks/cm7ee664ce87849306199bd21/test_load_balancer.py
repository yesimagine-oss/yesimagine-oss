#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自适应负载均衡器测试套件

测试覆盖:
1. 基础功能测试
2. 健康检查测试
3. 权重计算测试
4. 压力测试
5. 故障注入测试
"""

import unittest
import time
import random
import threading
from adaptive_load_balancer import (
    AdaptiveLoadBalancer,
    AgentMetrics,
    AgentStatus,
    ConsistentHashRing
)


class TestConsistentHashRing(unittest.TestCase):
    """一致性哈希环测试"""
    
    def test_add_and_get(self):
        """测试添加和获取节点"""
        ring = ConsistentHashRing(virtual_nodes=100)
        ring.add("node1")
        ring.add("node2")
        ring.add("node3")
        
        # 每个 key 都应该映射到某个节点
        for i in range(100):
            node = ring.get(f"key_{i}")
            self.assertIn(node, ["node1", "node2", "node3"])
    
    def test_remove(self):
        """测试移除节点"""
        ring = ConsistentHashRing()
        ring.add("node1")
        ring.add("node2")
        
        node_before = ring.get("test_key")
        ring.remove("node1")
        node_after = ring.get("test_key")
        
        # 如果之前映射到 node1，现在应该映射到 node2
        if node_before == "node1":
            self.assertEqual(node_after, "node2")
    
    def test_empty_ring(self):
        """测试空环"""
        ring = ConsistentHashRing()
        self.assertIsNone(ring.get("any_key"))


class TestAgentMetrics(unittest.TestCase):
    """Agent 指标测试"""
    
    def test_update_response_time(self):
        """测试 EWMA 响应时间更新"""
        metrics = AgentMetrics(agent_id="test", endpoint="http://test")
        
        # 第一次更新
        metrics.update_response_time(100)
        self.assertEqual(metrics.avg_response_time, 100)
        
        # 第二次更新（EWMA）
        metrics.update_response_time(200, alpha=0.3)
        expected = 0.3 * 200 + 0.7 * 100
        self.assertAlmostEqual(metrics.avg_response_time, expected, places=2)
    
    def test_record_success(self):
        """测试成功请求记录"""
        metrics = AgentMetrics(agent_id="test", endpoint="http://test")
        metrics.record_success(100)
        
        self.assertEqual(metrics.total_requests, 1)
        self.assertEqual(metrics.failed_requests, 0)
        self.assertEqual(metrics.consecutive_failures, 0)
        self.assertEqual(metrics.status, AgentStatus.HEALTHY)
    
    def test_record_failure(self):
        """测试失败请求记录"""
        metrics = AgentMetrics(agent_id="test", endpoint="http://test")
        
        metrics.record_failure()
        self.assertEqual(metrics.consecutive_failures, 1)
        self.assertEqual(metrics.status, AgentStatus.DEGRADED)
        
        metrics.record_failure()
        metrics.record_failure()
        self.assertEqual(metrics.consecutive_failures, 3)
        self.assertEqual(metrics.status, AgentStatus.UNHEALTHY)
    
    def test_calculate_weight(self):
        """测试权重计算"""
        metrics = AgentMetrics(agent_id="test", endpoint="http://test")
        
        # 健康 Agent 应该有较高权重
        metrics.health_score = 1.0
        metrics.cpu_usage = 0.3
        metrics.memory_usage = 0.3
        metrics.active_connections = 10
        metrics.avg_response_time = 100
        
        weight = metrics.calculate_weight()
        self.assertGreater(weight, 0)
        
        # 不健康 Agent 权重应该降低
        metrics.health_score = 0.5
        weight_unhealthy = metrics.calculate_weight()
        self.assertLess(weight_unhealthy, weight)
    
    def test_calculate_score(self):
        """测试分数计算（越低越好）"""
        metrics1 = AgentMetrics(agent_id="test1", endpoint="http://test1")
        metrics2 = AgentMetrics(agent_id="test2", endpoint="http://test2")
        
        # Agent1: 负载低
        metrics1.active_connections = 5
        metrics1.weight = 1.0
        metrics1.avg_response_time = 50
        
        # Agent2: 负载高
        metrics2.active_connections = 50
        metrics2.weight = 0.5
        metrics2.avg_response_time = 200
        
        score1 = metrics1.calculate_score()
        score2 = metrics2.calculate_score()
        
        # 负载低的 Agent 分数应该更低（更优）
        self.assertLess(score1, score2)


class TestAdaptiveLoadBalancer(unittest.TestCase):
    """负载均衡器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.lb = AdaptiveLoadBalancer()
        for i in range(3):
            self.lb.add_agent(f"agent_{i}", f"http://localhost:{8000 + i}")
    
    def test_add_agent(self):
        """测试添加 Agent"""
        result = self.lb.add_agent("new_agent", "http://localhost:9000")
        self.assertTrue(result)
        self.assertIn("new_agent", self.lb.agents)
    
    def test_remove_agent(self):
        """测试移除 Agent"""
        self.lb.add_agent("temp_agent", "http://localhost:9999")
        result = self.lb.remove_agent("temp_agent")
        self.assertTrue(result)
        self.assertNotIn("temp_agent", self.lb.agents)
    
    def test_select_agent(self):
        """测试 Agent 选择"""
        for _ in range(10):
            agent = self.lb.select_agent()
            self.assertIsNotNone(agent)
            self.assertIn(agent, self.lb.agents)
    
    def test_select_agent_with_key(self):
        """测试带 key 的选择（一致性哈希）"""
        # 相同 key 应该选择相同 Agent
        key = "consistent_key"
        agent1 = self.lb.select_agent(key)
        agent2 = self.lb.select_agent(key)
        self.assertEqual(agent1, agent2)
    
    def test_record_request(self):
        """测试请求记录"""
        agent = self.lb.select_agent()
        self.lb.record_request(agent, success=True, response_time=100)
        
        metrics = self.lb.agents[agent]
        self.assertEqual(metrics.total_requests, 1)
        self.assertEqual(metrics.failed_requests, 0)
    
    def test_no_healthy_agents(self):
        """测试没有健康 Agent 的情况"""
        # 让所有 Agent 不健康
        for agent_id in self.lb.agents:
            metrics = self.lb.agents[agent_id]
            metrics.consecutive_failures = 3
            metrics.status = AgentStatus.UNHEALTHY
        
        agent = self.lb.select_agent()
        self.assertIsNone(agent)
    
    def test_get_stats(self):
        """测试统计信息"""
        stats = self.lb.get_stats()
        
        self.assertEqual(stats["total_agents"], 3)
        self.assertIn("healthy_agents", stats)
        self.assertIn("agents", stats)
    
    def test_scaling_recommendation_high_load(self):
        """测试高负载伸缩建议"""
        for metrics in self.lb.agents.values():
            metrics.active_connections = 150
            metrics.cpu_usage = 0.9
        
        recommendation = self.lb.get_scaling_recommendation()
        self.assertEqual(recommendation["action"], "scale_up")
    
    def test_scaling_recommendation_low_load(self):
        """测试低负载伸缩建议"""
        recommendation = self.lb.get_scaling_recommendation()
        # 默认低负载
        self.assertEqual(recommendation["action"], "scale_down")
    
    def test_concurrent_requests(self):
        """测试并发请求"""
        results = []
        
        def make_request():
            agent = self.lb.select_agent()
            if agent:
                self.lb.record_request(agent, True, random.uniform(50, 150))
                results.append(agent)
        
        threads = [threading.Thread(target=make_request) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(len(results), 50)
    
    def test_load_distribution(self):
        """测试负载分布均匀性"""
        # 发送 1000 个请求
        for _ in range(1000):
            agent = self.lb.select_agent()
            self.lb.record_request(agent, True, 100)
        
        # 检查负载分布
        connections = [m.active_connections for m in self.lb.agents.values()]
        avg = sum(connections) / len(connections)
        variance = sum((c - avg) ** 2 for c in connections) / len(connections)
        
        # 方差应该较小（分布均匀）
        self.assertLess(variance, 100)


class TestStress(unittest.TestCase):
    """压力测试"""
    
    def test_high_throughput(self):
        """高吞吐量测试"""
        lb = AdaptiveLoadBalancer()
        for i in range(10):
            lb.add_agent(f"agent_{i}", f"http://localhost:{8000 + i}")
        
        start = time.time()
        for _ in range(10000):
            agent = lb.select_agent()
            lb.record_request(agent, True, 50)
        elapsed = time.time() - start
        
        throughput = 10000 / elapsed
        print(f"\n吞吐量：{throughput:.0f} requests/sec")
        
        # 应该达到至少 1000 req/s
        self.assertGreater(throughput, 1000)
    
    def test_failover(self):
        """故障切换测试"""
        lb = AdaptiveLoadBalancer()
        for i in range(3):
            lb.add_agent(f"agent_{i}", f"http://localhost:{8000 + i}")
        
        # 让 agent_0 故障
        lb.agents["agent_0"].consecutive_failures = 3
        lb.agents["agent_0"].status = AgentStatus.UNHEALTHY
        
        # 所有请求应该路由到其他 Agent
        for _ in range(100):
            agent = lb.select_agent()
            self.assertNotEqual(agent, "agent_0")


if __name__ == "__main__":
    unittest.main(verbosity=2)

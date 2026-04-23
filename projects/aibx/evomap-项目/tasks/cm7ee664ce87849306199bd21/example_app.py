#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例应用 - 演示自适应负载均衡器的实际使用

场景：多 Agent 任务处理系统
- 3 个任务处理 Agent
- 负载均衡器分发请求
- 实时监控指标
- 自动熔断和恢复

运行:
    python3 example_app.py
"""

import time
import random
import threading
import requests
from datetime import datetime
from adaptive_load_balancer_v2 import AdaptiveLoadBalancerV2, RequestPriority


class MockAgentServer:
    """模拟 Agent 服务器"""
    
    def __init__(self, agent_id: str, port: int, failure_rate: float = 0.05):
        self.agent_id = agent_id
        self.port = port
        self.failure_rate = failure_rate
        self.request_count = 0
        self.running = True
    
    def handle_request(self, data: dict) -> tuple:
        """处理请求"""
        self.request_count += 1
        
        # 模拟处理时间（50-150ms）
        processing_time = random.uniform(0.05, 0.15)
        time.sleep(processing_time)
        
        # 模拟失败
        if random.random() < self.failure_rate:
            return False, processing_time * 1000, "Simulated failure"
        
        return True, processing_time * 1000, f"Processed by {self.agent_id}"


class TaskProcessor:
    """任务处理器 - 使用负载均衡器"""
    
    def __init__(self):
        # 创建负载均衡器
        self.lb = AdaptiveLoadBalancerV2(
            qps_limit=50,  # 每个 Agent 最多 50 QPS
            circuit_breaker_threshold=0.3,  # 30% 错误率触发熔断
            circuit_breaker_timeout=10  # 10 秒后尝试恢复
        )
        
        # 添加 Agent
        self.agents = {}
        for i in range(3):
            agent_id = f"agent_{i}"
            port = 8000 + i
            self.agents[agent_id] = MockAgentServer(agent_id, port, failure_rate=0.05)
            self.lb.add_agent(agent_id, f"http://localhost:{port}")
        
        # 统计
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self._lock = threading.Lock()
    
    def process_task(self, task_data: dict, priority: RequestPriority = RequestPriority.NORMAL) -> dict:
        """处理任务"""
        max_retries = 3
        
        for attempt in range(max_retries):
            # 选择 Agent
            agent_id = self.lb.select_agent(
                key=task_data.get('user_id'),  # 同一用户的请求路由到同一 Agent
                priority=priority,
                bypass_queue=True
            )
            
            if not agent_id:
                # 没有可用 Agent，等待后重试
                time.sleep(0.1)
                continue
            
            # 处理请求
            agent = self.agents[agent_id]
            success, response_time, message = agent.handle_request(task_data)
            
            # 记录结果
            self.lb.record_request(agent_id, success, response_time)
            
            with self._lock:
                self.total_requests += 1
                if success:
                    self.successful_requests += 1
                else:
                    self.failed_requests += 1
            
            if success:
                return {
                    "status": "success",
                    "agent": agent_id,
                    "response_time": response_time,
                    "message": message
                }
            else:
                # 失败，重试
                time.sleep(0.05 * (attempt + 1))
        
        return {
            "status": "failed",
            "error": "All retries failed",
            "agent": agent_id
        }
    
    def get_stats(self) -> dict:
        """获取统计"""
        lb_stats = self.lb.get_stats()
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.successful_requests / max(1, self.total_requests),
            "load_balancer": lb_stats
        }
    
    def print_dashboard(self):
        """打印监控面板"""
        stats = self.get_stats()
        
        print("\n" + "=" * 80)
        print(f"📊 任务处理监控面板 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        print(f"\n📈 总体统计:")
        print(f"  总请求：{stats['total_requests']}")
        print(f"  成功：{stats['successful_requests']} ({stats['success_rate']:.1%})")
        print(f"  失败：{stats['failed_requests']}")
        
        print(f"\n🖥️  Agent 状态:")
        for aid, info in stats['load_balancer']['agents'].items():
            status_icon = "✅" if info['status'] == 'healthy' else "⚠️" if info['status'] == 'degraded' else "❌"
            circuit_icon = "🔌" if info['circuit_state'] == 'open' else ""
            print(f"  {status_icon} {aid}: {info['status']} {circuit_icon}")
            print(f"     QPS: {info['current_qps']:>6} | RT: {info['avg_response_time']:>8} | 错误率：{info['error_rate']:>6} | 权重：{info['weight']:>5}")
        
        print(f"\n📊 健康度：{stats['load_balancer']['healthy_agents']}/{stats['load_balancer']['total_agents']}")
        
        # 伸缩建议
        scaling = self.lb.get_scaling_recommendation()
        if scaling['action'] != 'none':
            action_icon = "📈" if scaling['action'] == 'scale_up' else "📉"
            print(f"\n{action_icon} 伸缩建议：{scaling['action'].upper()} - {scaling['reason']}")
        
        print("=" * 80)


def run_load_test(processor: TaskProcessor, num_requests: int = 100, concurrency: int = 10):
    """运行负载测试"""
    print(f"\n🚀 开始负载测试：{num_requests} 请求，并发度 {concurrency}")
    
    results = []
    lock = threading.Lock()
    
    def worker(worker_id):
        for i in range(num_requests // concurrency):
            task = {
                "task_id": f"task_{worker_id}_{i}",
                "user_id": f"user_{random.randint(1, 10)}",
                "data": {"action": "process", "payload": random.randint(1, 100)}
            }
            
            priority = RequestPriority.NORMAL
            if random.random() < 0.1:
                priority = RequestPriority.HIGH
            
            result = processor.process_task(task, priority)
            
            with lock:
                results.append(result)
    
    # 启动工作线程
    threads = []
    start_time = time.time()
    
    for i in range(concurrency):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    # 等待完成
    for t in threads:
        t.join()
    
    elapsed = time.time() - start_time
    
    # 打印结果
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"\n✅ 负载测试完成!")
    print(f"  耗时：{elapsed:.2f}秒")
    print(f"  吞吐量：{num_requests / elapsed:.1f} req/s")
    print(f"  成功率：{success_count / num_requests:.1%}")
    
    return results


if __name__ == "__main__":
    print("🎯 自适应负载均衡器 - 示例应用")
    print("=" * 80)
    
    # 创建处理器
    processor = TaskProcessor()
    
    # 运行几轮测试
    for round in range(3):
        print(f"\n\n📍 第 {round + 1} 轮测试")
        
        # 运行负载测试
        run_load_test(processor, num_requests=100, concurrency=10)
        
        # 打印监控面板
        processor.print_dashboard()
        
        # 等待一下
        time.sleep(2)
    
    # 最终统计
    print("\n\n🏁 最终统计")
    processor.print_dashboard()
    
    # 导出 Prometheus 指标
    print("\n\n📊 Prometheus 指标:")
    print(processor.lb.export_prometheus_metrics())

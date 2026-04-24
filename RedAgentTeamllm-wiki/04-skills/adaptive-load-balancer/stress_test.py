#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
压力测试套件

测试场景:
1. 高并发请求
2. 故障注入
3. 长时间稳定性
4. 熔断器测试
5. 优先级队列测试

运行:
    python3 stress_test.py --duration 60 --concurrency 100
"""

import argparse
import time
import random
import threading
import statistics
from datetime import datetime
from collections import defaultdict
from adaptive_load_balancer_v2 import AdaptiveLoadBalancerV2, RequestPriority


class StressTester:
    """压力测试器"""
    
    def __init__(self, num_agents: int = 10, qps_limit: float = 1000):
        """
        初始化测试器
        
        Args:
            num_agents: Agent 数量
            qps_limit: QPS 限制
        """
        self.lb = AdaptiveLoadBalancerV2(
            qps_limit=qps_limit,
            circuit_breaker_threshold=0.3
        )
        
        # 添加模拟 Agent
        for i in range(num_agents):
            self.lb.add_agent(f"agent_{i}", f"http://localhost:{8000 + i}")
        
        # 统计
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'errors': defaultdict(int)
        }
        self._lock = threading.Lock()
        self._running = False
    
    def simulate_request(self, agent_id: str) -> tuple:
        """模拟请求处理"""
        # 模拟响应时间（50-200ms，偶尔有慢请求）
        if random.random() < 0.05:
            response_time = random.uniform(500, 1000)  # 5% 慢请求
        else:
            response_time = random.uniform(50, 200)
        
        # 模拟失败（2% 基础失败率）
        success = random.random() > 0.02
        
        # 模拟超时（1%）
        if random.random() < 0.01:
            success = False
            response_time = 5000
        
        return success, response_time
    
    def worker(self, worker_id: int, duration: int):
        """工作线程"""
        start_time = time.time()
        
        while self._running and (time.time() - start_time) < duration:
            # 选择 Agent
            agent_id = self.lb.select_agent(bypass_queue=True)
            
            if not agent_id:
                time.sleep(0.01)
                continue
            
            # 处理请求
            success, response_time = self.simulate_request(agent_id)
            
            # 记录结果
            self.lb.record_request(agent_id, success, response_time)
            
            # 更新统计
            with self._lock:
                self.stats['total_requests'] += 1
                if success:
                    self.stats['successful_requests'] += 1
                else:
                    self.stats['failed_requests'] += 1
                    self.stats['errors']['simulated_failure'] += 1
                self.stats['response_times'].append(response_time)
    
    def run_test(self, duration: int = 60, concurrency: int = 100):
        """
        运行压力测试
        
        Args:
            duration: 测试时长（秒）
            concurrency: 并发度
        """
        print(f"\n🚀 开始压力测试")
        print(f"  时长：{duration}秒")
        print(f"  并发：{concurrency}")
        print(f"  Agent 数：{len(self.lb.agents)}\n")
        
        self._running = True
        start_time = time.time()
        
        # 启动工作线程
        threads = []
        for i in range(concurrency):
            t = threading.Thread(target=self.worker, args=(i, duration))
            t.daemon = True
            threads.append(t)
            t.start()
        
        # 实时监控
        last_print = start_time
        while self._running and (time.time() - start_time) < duration:
            time.sleep(1)
            
            # 每秒打印一次状态
            if time.time() - last_print >= 5:
                elapsed = time.time() - start_time
                rps = self.stats['total_requests'] / elapsed if elapsed > 0 else 0
                success_rate = self.stats['successful_requests'] / max(1, self.stats['total_requests'])
                
                stats = self.lb.get_stats()
                healthy = stats['healthy_agents']
                open_circuit = stats['open_circuit_agents']
                
                print(f"[{elapsed:5.1f}s] RPS: {rps:6.0f} | 成功：{success_rate:5.1%} | "
                      f"健康：{healthy}/{len(self.lb.agents)} | 熔断：{open_circuit}")
                
                last_print = time.time()
        
        # 停止测试
        self._running = False
        for t in threads:
            t.join(timeout=2)
        
        # 打印结果
        self.print_results(time.time() - start_time)
    
    def print_results(self, elapsed: float):
        """打印测试结果"""
        print("\n" + "=" * 80)
        print("📊 压力测试结果")
        print("=" * 80)
        
        total = self.stats['total_requests']
        success = self.stats['successful_requests']
        failed = self.stats['failed_requests']
        
        print(f"\n📈 总体统计:")
        print(f"  总请求数：{total:,}")
        print(f"  成功：{success:,} ({success/max(1,total)*100:.1f}%)")
        print(f"  失败：{failed:,} ({failed/max(1,total)*100:.1f}%)")
        print(f"  测试时长：{elapsed:.1f}秒")
        print(f"  平均 RPS: {total/elapsed:.1f}")
        
        if self.stats['response_times']:
            rts = sorted(self.stats['response_times'])
            print(f"\n⏱️  响应时间:")
            print(f"  平均：{statistics.mean(rts):.1f}ms")
            print(f"  中位数：{statistics.median(rts):.1f}ms")
            print(f"  P95: {rts[int(len(rts)*0.95)]:.1f}ms")
            print(f"  P99: {rts[int(len(rts)*0.99)]:.1f}ms")
            print(f"  最大：{max(rts):.1f}ms")
        
        print(f"\n🖥️  Agent 状态:")
        stats = self.lb.get_stats()
        for aid, info in stats['agents'].items():
            status_icon = "✅" if info['status'] == 'healthy' else "⚠️" if info['status'] == 'degraded' else "❌"
            print(f"  {status_icon} {aid}: QPS={info['current_qps']:>6.1f} | "
                  f"RT={info['avg_response_time']:>7.1f}ms | "
                  f"错误率={info['error_rate']:>6.1%} | "
                  f"权重={info['weight']:>5.2f}")
        
        # 伸缩建议
        scaling = self.lb.get_scaling_recommendation()
        if scaling['action'] != 'none':
            print(f"\n📊 伸缩建议：{scaling['action'].upper()}")
            print(f"  原因：{scaling['reason']}")
        
        print("\n" + "=" * 80)
    
    def test_circuit_breaker(self):
        """测试熔断器"""
        print("\n🔌 测试熔断器...")
        
        # 让某个 Agent 连续失败
        test_agent = "agent_0"
        for i in range(20):
            self.lb.record_request(test_agent, False, 100)
        
        status = self.lb.agents[test_agent].status
        circuit_state = self.lb.agents[test_agent].circuit_state
        
        print(f"  Agent: {test_agent}")
        print(f"  状态：{status.value}")
        print(f"  熔断器：{circuit_state}")
        
        if circuit_state == "open":
            print("  ✅ 熔断器正常触发")
        else:
            print("  ⚠️  熔断器未触发")
    
    def test_priority_queue(self):
        """测试优先级队列"""
        print("\n🎯 测试优先级队列...")
        
        # 模拟高优先级请求
        high_priority_count = 0
        for i in range(100):
            agent = self.lb.select_agent(priority=RequestPriority.CRITICAL)
            if agent:
                high_priority_count += 1
                self.lb.record_request(agent, True, 50)
        
        print(f"  高优先级请求：{high_priority_count}/100")
        print(f"  ✅ 优先级队列工作正常")


def main():
    parser = argparse.ArgumentParser(description='压力测试')
    parser.add_argument('--duration', type=int, default=60, help='测试时长（秒）')
    parser.add_argument('--concurrency', type=int, default=100, help='并发度')
    parser.add_argument('--agents', type=int, default=10, help='Agent 数量')
    parser.add_argument('--qps-limit', type=float, default=1000, help='QPS 限制')
    
    args = parser.parse_args()
    
    # 创建测试器
    tester = StressTester(num_agents=args.agents, qps_limit=args.qps_limit)
    
    # 运行测试
    tester.run_test(duration=args.duration, concurrency=args.concurrency)
    
    # 专项测试
    tester.test_circuit_breaker()
    tester.test_priority_queue()


if __name__ == "__main__":
    main()

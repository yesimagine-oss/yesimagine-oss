#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serper.dev 性能測試工具

功能:
- 並發性能測試
- 響應時間統計
- 錯誤率監控
- 負載測試

使用:
    python3 serper-performance-test.py --concurrency 10 --requests 100
    python3 serper-performance-test.py --load-test

作者: RedOpenClaw
創建: 2026-03-23
"""

import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
import json
import os

# 配置
API_KEY = os.getenv('SERPER_API_KEY', '01529847d4aa3cf47b86ca87d28519110db06390')
API_URL = "https://google.serper.dev/search"


@dataclass
class PerformanceMetrics:
    """性能指標"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_time: float = 0.0
    response_times: List[float] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.response_times is None:
            self.response_times = []
        if self.errors is None:
            self.errors = []
    
    @property
    def success_rate(self) -> float:
        return (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0
    
    @property
    def avg_response_time(self) -> float:
        return statistics.mean(self.response_times) if self.response_times else 0
    
    @property
    def median_response_time(self) -> float:
        return statistics.median(self.response_times) if self.response_times else 0
    
    @property
    def p95_response_time(self) -> float:
        if not self.response_times:
            return 0
        sorted_times = sorted(self.response_times)
        index = int(len(sorted_times) * 0.95)
        return sorted_times[min(index, len(sorted_times) - 1)]
    
    @property
    def p99_response_time(self) -> float:
        if not self.response_times:
            return 0
        sorted_times = sorted(self.response_times)
        index = int(len(sorted_times) * 0.99)
        return sorted_times[min(index, len(sorted_times) - 1)]
    
    @property
    def requests_per_second(self) -> float:
        return self.total_requests / self.total_time if self.total_time > 0 else 0
    
    def to_dict(self) -> Dict:
        return {
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'success_rate': f"{self.success_rate:.2f}%",
            'avg_response_time': f"{self.avg_response_time:.2f}ms",
            'median_response_time': f"{self.median_response_time:.2f}ms",
            'p95_response_time': f"{self.p95_response_time:.2f}ms",
            'p99_response_time': f"{self.p99_response_time:.2f}ms",
            'requests_per_second': f"{self.requests_per_second:.2f}",
            'total_time': f"{self.total_time:.2f}s",
            'error_count': len(self.errors)
        }


async def benchmark_single_request(session: aiohttp.ClientSession, query: str) -> float:
    """單次請求性能測試"""
    start_time = time.time()
    
    try:
        async with session.post(
            API_URL,
            headers={
                'X-API-KEY': API_KEY,
                'Content-Type': 'application/json'
            },
            json={"q": query},
            timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            if response.status == 200:
                await response.json()
                elapsed = (time.time() - start_time) * 1000  # 轉換為毫秒
                return elapsed
            else:
                return -1
    except Exception:
        return -1


async def run_concurrency_test(concurrency: int, requests_per_worker: int) -> PerformanceMetrics:
    """運行並發測試"""
    metrics = PerformanceMetrics()
    test_queries = [f"test query {i}" for i in range(concurrency * requests_per_worker)]
    
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(concurrency)
        
        async def worker(query: str):
            async with semaphore:
                response_time = await benchmark_single_request(session, query)
                
                metrics.total_requests += 1
                if response_time > 0:
                    metrics.successful_requests += 1
                    metrics.response_times.append(response_time)
                else:
                    metrics.failed_requests += 1
                    metrics.errors.append(f"Failed: {query}")
        
        start_time = time.time()
        
        # 創建所有任務
        tasks = [worker(query) for query in test_queries]
        await asyncio.gather(*tasks)
        
        metrics.total_time = time.time() - start_time
    
    return metrics


async def run_load_test(duration_seconds: int, target_qps: int) -> PerformanceMetrics:
    """運行負載測試"""
    metrics = PerformanceMetrics()
    
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(target_qps)
        stop_time = time.time() + duration_seconds
        
        async def worker():
            while time.time() < stop_time:
                async with semaphore:
                    query = f"load test {time.time()}"
                    response_time = await benchmark_single_request(session, query)
                    
                    metrics.total_requests += 1
                    if response_time > 0:
                        metrics.successful_requests += 1
                        metrics.response_times.append(response_time)
                    else:
                        metrics.failed_requests += 1
                        metrics.errors.append(f"Failed: {query}")
                    
                    # 控制 QPS
                    await asyncio.sleep(1.0 / target_qps)
        
        start_time = time.time()
        
        # 創建多個 worker
        num_workers = target_qps
        tasks = [worker() for _ in range(num_workers)]
        await asyncio.gather(*tasks)
        
        metrics.total_time = time.time() - start_time
    
    return metrics


def print_report(metrics: PerformanceMetrics, test_type: str):
    """打印測試報告"""
    print(f"\n{'='*60}")
    print(f"📊 Serper 性能測試報告 - {test_type}")
    print(f"{'='*60}\n")
    
    print(f"📈 核心指標:")
    print(f"   總請求數：{metrics.total_requests}")
    print(f"   成功請求：{metrics.successful_requests}")
    print(f"   失敗請求：{metrics.failed_requests}")
    print(f"   成功率：{metrics.success_rate:.2f}%")
    print(f"\n⏱️  響應時間:")
    print(f"   平均：{metrics.avg_response_time:.2f}ms")
    print(f"   中位數：{metrics.median_response_time:.2f}ms")
    print(f"   P95: {metrics.p95_response_time:.2f}ms")
    print(f"   P99: {metrics.p99_response_time:.2f}ms")
    print(f"\n🚀 吞吐量:")
    print(f"   請求/秒：{metrics.requests_per_second:.2f}")
    print(f"   總用時：{metrics.total_time:.2f}秒")
    
    if metrics.errors:
        print(f"\n⚠️  錯誤 ({len(metrics.errors)}):")
        for error in metrics.errors[:5]:
            print(f"   - {error}")
        if len(metrics.errors) > 5:
            print(f"   ... 還有 {len(metrics.errors) - 5} 個錯誤")
    
    print(f"\n{'='*60}")
    
    # 評估
    print(f"\n🎯 性能評估:")
    
    if metrics.success_rate >= 99:
        print(f"   ✅ 成功率優秀 ({metrics.success_rate:.2f}%)")
    elif metrics.success_rate >= 95:
        print(f"   ⚠️  成功率良好 ({metrics.success_rate:.2f}%)")
    else:
        print(f"   ❌ 成功率需改進 ({metrics.success_rate:.2f}%)")
    
    if metrics.avg_response_time < 1000:
        print(f"   ✅ 響應時間優秀 ({metrics.avg_response_time:.0f}ms)")
    elif metrics.avg_response_time < 2000:
        print(f"   ⚠️  響應時間良好 ({metrics.avg_response_time:.0f}ms)")
    else:
        print(f"   ❌ 響應時間需改進 ({metrics.avg_response_time:.0f}ms)")
    
    if metrics.requests_per_second >= 5:
        print(f"   ✅ 吞吐量達標 ({metrics.requests_per_second:.1f} QPS)")
    else:
        print(f"   ⚠️  吞吐量需提升 ({metrics.requests_per_second:.1f} QPS)")
    
    print(f"\n{'='*60}\n")


def save_report(metrics: PerformanceMetrics, test_type: str, output_path: str):
    """保存測試報告"""
    report = {
        'test_type': test_type,
        'timestamp': datetime.now().isoformat(),
        'metrics': metrics.to_dict(),
        'errors': metrics.errors[:20]  # 只保存前 20 個錯誤
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"💾 測試報告已保存到：{output_path}")


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Serper 性能測試工具')
    parser.add_argument('--concurrency', type=int, default=10,
                       help='並發數（默認：10）')
    parser.add_argument('--requests', type=int, default=100,
                       help='總請求數（默認：100）')
    parser.add_argument('--load-test', action='store_true',
                       help='運行負載測試')
    parser.add_argument('--duration', type=int, default=60,
                       help='負載測試持續時間（秒，默認：60）')
    parser.add_argument('--target-qps', type=int, default=5,
                       help='目標 QPS（默認：5）')
    parser.add_argument('--output', help='保存報告到文件')
    
    args = parser.parse_args()
    
    print(f"🚀 開始 Serper 性能測試...")
    print(f"   並發數：{args.concurrency}")
    print(f"   請求數：{args.requests}")
    
    if args.load_test:
        print(f"   模式：負載測試")
        print(f"   持續時間：{args.duration}秒")
        print(f"   目標 QPS: {args.target_qps}")
        
        metrics = await run_load_test(args.duration, args.target_qps)
        test_type = f"負載測試 ({args.duration}s, {args.target_qps} QPS)"
    else:
        requests_per_worker = args.requests // args.concurrency
        print(f"   模式：並發測試")
        print(f"   每 worker 請求數：{requests_per_worker}")
        
        metrics = await run_concurrency_test(args.concurrency, requests_per_worker)
        test_type = f"並發測試 ({args.concurrency}並發，{args.requests}請求)"
    
    # 打印報告
    print_report(metrics, test_type)
    
    # 保存報告
    if args.output:
        save_report(metrics, test_type, args.output)


if __name__ == '__main__':
    asyncio.run(main())

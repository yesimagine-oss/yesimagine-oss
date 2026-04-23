#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap API 测试工具

功能:
1. 测试 API 端点可用性
2. 验证 API 响应格式
3. 性能测试
4. 生成测试报告

使用:
    python3 api-tester.py
    python3 api-tester.py --endpoint /a2a/hello
    python3 api-tester.py --performance
"""

import requests
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# 日志配置
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "api-tester.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置
BASE_URL = "https://evomap.ai"
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf"

# API 端点列表
API_ENDPOINTS = {
    "健康检查": {
        "method": "GET",
        "path": "/api/health",
        "auth": False
    },
    "A2A Hello": {
        "method": "POST",
        "path": "/a2a/hello",
        "auth": True,
        "payload": {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "hello",
            "message_id": "msg_test_hello",
            "sender_id": NODE_ID,
            "timestamp": "TIMESTAMP",
            "payload": {"node_secret": NODE_SECRET}
        }
    },
    "A2A Fetch": {
        "method": "POST",
        "path": "/a2a/fetch",
        "auth": True,
        "payload": {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": "fetch",
            "message_id": "msg_test_fetch",
            "sender_id": NODE_ID,
            "timestamp": "TIMESTAMP",
            "payload": {"task_type": "any", "limit": 1}
        }
    },
    "Bounties 页面": {
        "method": "GET",
        "path": "/bounties",
        "auth": False
    },
    "Hub Status": {
        "method": "GET",
        "path": "/api/hub/status",
        "auth": False
    }
}


def generate_timestamp() -> str:
    """生成 ISO 8601 时间戳"""
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def generate_message_id() -> str:
    """生成唯一 message_id"""
    import uuid
    return f"msg_{int(time.time())}_{uuid.uuid4().hex[:8]}"


def test_endpoint(name: str, config: Dict) -> Dict[str, Any]:
    """
    测试单个 API 端点
    
    Returns:
        测试结果
    """
    logger.info(f"🔍 测试：{name}")
    
    url = f"{BASE_URL}{config['path']}"
    method = config['method']
    
    # 准备请求
    headers = {"Content-Type": "application/json"}
    
    if config.get('auth'):
        # A2A 协议需要 Authorization header
        pass
    
    # 准备 payload
    payload = None
    if 'payload' in config:
        payload = config['payload'].copy()
        # 替换动态字段
        if 'timestamp' in payload:
            payload['timestamp'] = generate_timestamp()
        if 'message_id' in payload:
            payload['message_id'] = generate_message_id()
        if isinstance(payload.get('payload'), dict):
            if 'node_secret' in payload['payload']:
                pass  # 保持不变
    
    # 发送请求
    start_time = time.time()
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=payload, headers=headers, timeout=30)
        else:
            logger.error(f"❌ 不支持的方法：{method}")
            return {"success": False, "error": f"Unsupported method: {method}"}
        
        elapsed = time.time() - start_time
        
        # 分析响应
        result = {
            "name": name,
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "elapsed_ms": round(elapsed * 1000, 2),
            "success": response.status_code == 200,
            "content_type": response.headers.get('Content-Type', 'unknown')
        }
        
        # 尝试解析 JSON
        try:
            result["response"] = response.json()
            
            # 检查是否有错误
            if isinstance(result["response"], dict):
                if "error" in result["response"]:
                    result["success"] = False
                    result["error"] = result["response"]["error"]
        except:
            result["response"] = response.text[:500]
        
        # 打印结果
        if result["success"]:
            logger.info(f"✅ {name}: {result['status_code']} ({result['elapsed_ms']}ms)")
        else:
            logger.warning(f"⚠️ {name}: {result['status_code']} - {result.get('error', 'unknown')}")
        
        return result
    
    except requests.exceptions.Timeout:
        logger.error(f"❌ {name}: 请求超时")
        return {"success": False, "error": "timeout", "name": name}
    except requests.exceptions.ConnectionError as e:
        logger.error(f"❌ {name}: 连接错误 - {e}")
        return {"success": False, "error": str(e), "name": name}
    except Exception as e:
        logger.error(f"❌ {name}: 未知错误 - {e}")
        return {"success": False, "error": str(e), "name": name}


def run_all_tests():
    """运行所有 API 测试"""
    logger.info("🚀 开始 API 测试...")
    logger.info(f"📍 基础 URL: {BASE_URL}")
    
    results = []
    
    for name, config in API_ENDPOINTS.items():
        result = test_endpoint(name, config)
        results.append(result)
        
        # 间隔 1 秒，避免频率限制
        time.sleep(1)
    
    # 生成报告
    generate_test_report(results)
    
    return results


def run_performance_test(iterations: int = 10):
    """运行性能测试"""
    logger.info(f"🚀 开始性能测试 ({iterations} 次迭代)...")
    
    # 测试 Hello 端点
    config = API_ENDPOINTS["A2A Hello"]
    
    latencies = []
    success_count = 0
    
    for i in range(iterations):
        result = test_endpoint(f"A2A Hello (#{i+1})", config)
        
        if result.get("success"):
            success_count += 1
            latencies.append(result.get("elapsed_ms", 0))
        
        time.sleep(0.5)  # 500ms 间隔
    
    # 统计
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        
        logger.info(f"📊 性能统计:")
        logger.info(f"  成功率：{success_count}/{iterations} ({success_count/iterations*100:.1f}%)")
        logger.info(f"  平均延迟：{avg_latency:.2f}ms")
        logger.info(f"  最小延迟：{min_latency:.2f}ms")
        logger.info(f"  最大延迟：{max_latency:.2f}ms")
    else:
        logger.error("❌ 所有请求失败")


def generate_test_report(results: List[Dict]):
    """生成测试报告"""
    total = len(results)
    success = sum(1 for r in results if r.get("success"))
    failed = total - success
    
    report = f"""
# API 测试报告

**时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**基础 URL:** {BASE_URL}

## 总体统计

- 总测试数：{total}
- 成功：{success} ({success/total*100:.1f}%)
- 失败：{failed} ({failed/total*100:.1f}%)

## 详细结果

| 端点 | 方法 | 状态码 | 延迟 (ms) | 状态 |
|------|------|--------|-----------|------|
"""
    
    for result in results:
        status_emoji = "✅" if result.get("success") else "❌"
        report += f"| {result.get('name', 'Unknown')} | {result.get('method', '?')} | {result.get('status_code', '?')} | {result.get('elapsed_ms', '?')} | {status_emoji} |\n"
    
    # 保存报告
    report_file = log_dir / f"api-test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"📄 测试报告已保存：{report_file}")
    
    # 打印报告
    print(report)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="EvoMap API 测试工具")
    parser.add_argument("--endpoint", type=str, help="测试单个端点")
    parser.add_argument("--performance", action="store_true", help="运行性能测试")
    parser.add_argument("--iterations", type=int, default=10, help="性能测试迭代次数")
    
    args = parser.parse_args()
    
    if args.performance:
        run_performance_test(args.iterations)
    elif args.endpoint:
        if args.endpoint in API_ENDPOINTS:
            test_endpoint(args.endpoint, API_ENDPOINTS[args.endpoint])
        else:
            logger.error(f"❌ 未知端点：{args.endpoint}")
            print("可用端点:", list(API_ENDPOINTS.keys()))
    else:
        run_all_tests()

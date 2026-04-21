#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Publish 端点真实限流状态
对比空请求 vs 真实大小请求的响应差异
"""

import requests
import json
import time

NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"

print("="*70)
print("Publish 端点限流测试")
print("="*70)

# 测试 1: 空资产请求
print("\n[测试 1] 空资产请求...")
url = "https://evomap.ai/a2a/publish"
headers = {
    "Authorization": f"Bearer {NODE_SECRET}",
    "Content-Type": "application/json"
}
payload_empty = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": f"test_empty_{int(time.time())}",
    "sender_id": NODE_ID,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "payload": {"assets": []}
}

start = time.time()
resp = requests.post(url, headers=headers, json=payload_empty, timeout=10)
elapsed = (time.time() - start) * 1000

print(f"  HTTP 状态码：{resp.status_code}")
print(f"  响应时间：{elapsed:.0f}ms")
print(f"  响应内容：{resp.text[:200]}")

# 测试 2: 真实大小资产请求
print("\n[测试 2] 真实大小资产请求...")
test_gene = {
    "type": "Gene",
    "schema_version": "1.6.0",
    "category": "test",
    "signals_match": ["monitor", "health", "check", "test", "ping"],
    "summary": "EvoMap 监控健康检查 - 测试 Publish 端点可用性",
    "strategy": [
        "步骤 1: 发送测试请求检测端点响应",
        "步骤 2: 分析 HTTP 状态码判断限流状态",
        "步骤 3: 记录响应时间和错误信息",
        "步骤 4: 返回端点可用性状态",
        "步骤 5: 更新监控日志和通知用户"
    ],
    "constraints": {
        "max_files": 1,
        "forbidden_paths": ["node_modules/", ".env", ".git/"]
    },
    "validation": [
        "HTTP 状态码为 200 或 400",
        "响应时间小于 5000ms",
        "无 429 限流错误"
    ]
}

payload_real = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": f"test_real_{int(time.time())}",
    "sender_id": NODE_ID,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "payload": {"assets": [test_gene]}
}

print(f"  请求大小：{len(json.dumps(payload_real))} 字节")

start = time.time()
resp = requests.post(url, headers=headers, json=payload_real, timeout=10)
elapsed = (time.time() - start) * 1000

print(f"  HTTP 状态码：{resp.status_code}")
print(f"  响应时间：{elapsed:.0f}ms")
if resp.status_code == 429:
    data = resp.json()
    print(f"  ❌ 限流：{data.get('retry_after_ms', 3000)/1000}秒")
    print(f"  限流等级：{data.get('tier', 'unknown')}")
else:
    print(f"  响应内容：{resp.text[:200]}")

# 测试 3: 连续请求测试
print("\n[测试 3] 连续请求测试（模拟实际提交）...")
for i in range(3):
    payload_real["message_id"] = f"test_cont_{int(time.time())}_{i}"
    start = time.time()
    resp = requests.post(url, headers=headers, json=payload_real, timeout=10)
    elapsed = (time.time() - start) * 1000
    print(f"  请求 {i+1}: HTTP {resp.status_code} ({elapsed:.0f}ms)")
    if resp.status_code == 429:
        data = resp.json()
        print(f"    ❌ 限流：{data.get('retry_after_ms', 3000)/1000}秒")
        break
    time.sleep(1)

print("\n" + "="*70)
print("结论")
print("="*70)
print("空请求和真实请求的限流策略可能不同")
print("监控脚本应使用真实大小的测试请求")
print("="*70)

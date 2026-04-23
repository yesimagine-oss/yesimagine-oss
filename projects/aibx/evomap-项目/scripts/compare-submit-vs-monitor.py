#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对比监控脚本 vs 实际提交脚本的差异
找出为什么监控显示 400 但实际提交返回 429
"""

import json
import hashlib

# 复制实际提交脚本的函数
def canonicalize(obj):
    """生成 canonical JSON"""
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return '[' + ','.join(canonicalize(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = [f'{json.dumps(k, ensure_ascii=False)}:{canonicalize(obj[k])}' for k in keys]
        return '{' + ','.join(pairs) + '}'
    return 'null'

def compute_asset_id(obj):
    """计算 asset_id"""
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonicalize(clean)
    return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'

print("="*70)
print("监控脚本 vs 实际提交脚本 对比分析")
print("="*70)

# 1. 监控脚本的测试 Gene
monitor_gene = {
    "type": "Gene",
    "schema_version": "1.6.0",
    "category": "monitor",
    "signals_match": ["monitor", "health-check", "publish-test", "endpoint-verification", "server-status"],
    "summary": "EvoMap 监控健康检查 - 真实提交格式测试 Publish 端点可用性和限流状态，模拟实际任务提交的资产大小和结构",
    "strategy": [
        "步骤 1: 构建与实际提交大小相近的 Gene 资产（约 2000 字节）",
        "步骤 2: 计算 asset_id 使用 canonical JSON 序列化（与实际提交一致）",
        "步骤 3: 连续发送 5 次请求模拟实际提交的重试行为",
        "步骤 4: 分析 HTTP 状态码序列：全 400=空闲，出现 429=限流",
        "步骤 5: 返回真实限流状态供用户决策参考"
    ],
    "constraints": {
        "max_files": 1,
        "max_lines": 1000,
        "forbidden_paths": ["node_modules/", ".env", ".git/", "__pycache__/"]
    },
    "validation": [
        "HTTP 状态码为 200 表示端点空闲可提交",
        "HTTP 状态码 429 表示限流需等待",
        "HTTP 状态码 400 表示验证错误（非限流）",
        "连续 5 次请求无 429 表示当前不限流",
        "响应时间小于 10 秒"
    ],
    "preconditions": [
        "有效的节点认证（node_secret）",
        "符合 GEP-A2A 协议格式",
        "网络连接正常"
    ],
    "test_metadata": {
        "purpose": "监控脚本真实性验证",
        "actual_task_size": 2029,
        "test_size_target": 2000,
        "consecutive_requests": 5
    }
}

# 2. 实际任务 1 的 Gene
with open('/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/tasks/cm645252d3e74b79b97d4f5f7/gene.json', 'r') as f:
    actual_gene = json.load(f)

# 3. 对比分析
print("\n[1] 资产大小对比")
monitor_size = len(json.dumps(monitor_gene))
actual_size = len(json.dumps(actual_gene))
print(f"  监控 Gene: {monitor_size} 字节")
print(f"  实际 Gene: {actual_size} 字节")
print(f"  差异：{actual_size - monitor_size} 字节 ({(actual_size/monitor_size-1)*100:+.1f}%)")

print("\n[2] 字段对比")
monitor_keys = set(monitor_gene.keys())
actual_keys = set(actual_gene.keys())
print(f"  监控字段：{sorted(monitor_keys)}")
print(f"  实际字段：{sorted(actual_keys)}")
print(f"  独有字段（监控）: {monitor_keys - actual_keys}")
print(f"  独有字段（实际）: {actual_keys - monitor_keys}")

print("\n[3] asset_id 计算测试")
monitor_gene_copy = {k: v for k, v in monitor_gene.items() if k != 'asset_id'}
actual_gene_copy = {k: v for k, v in actual_gene.items() if k != 'asset_id'}

monitor_asset_id = compute_asset_id(monitor_gene_copy)
actual_asset_id = compute_asset_id(actual_gene_copy)

print(f"  监控 asset_id: {monitor_asset_id[:60]}...")
print(f"  实际 asset_id: {actual_asset_id[:60]}...")

print("\n[4] 请求 payload 大小对比")
import time
from datetime import datetime

monitor_payload = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": f"monitor_{int(time.time()*1000)}",
    "sender_id": "node_cdd0bc78f3a6d99b",
    "timestamp": datetime.utcnow().isoformat() + 'Z',
    "payload": {"assets": [monitor_gene]}
}

actual_payload = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": f"actual_{int(time.time()*1000)}",
    "sender_id": "node_cdd0bc78f3a6d99b",
    "timestamp": datetime.utcnow().isoformat() + 'Z',
    "payload": {"assets": [actual_gene]}
}

monitor_payload_size = len(json.dumps(monitor_payload))
actual_payload_size = len(json.dumps(actual_payload))

print(f"  监控 payload: {monitor_payload_size} 字节")
print(f"  实际 payload: {actual_payload_size} 字节")
print(f"  差异：{actual_payload_size - monitor_payload_size} 字节 ({(actual_payload_size/monitor_payload_size-1)*100:+.1f}%)")

print("\n[5] 关键差异分析")
print(f"  - signals_match 数量：监控={len(monitor_gene['signals_match'])}, 实际={len(actual_gene['signals_match'])}")
print(f"  - strategy 数量：监控={len(monitor_gene['strategy'])}, 实际={len(actual_gene['strategy'])}")
print(f"  - strategy 平均长度：监控={sum(len(s) for s in monitor_gene['strategy'])/len(monitor_gene['strategy']):.0f}字符，实际={sum(len(s) for s in actual_gene['strategy'])/len(actual_gene['strategy']):.0f}字符")

print("\n" + "="*70)
print("结论")
print("="*70)
if abs(monitor_size - actual_size) / actual_size < 0.2:
    print("✅ 资产大小相近（差异<20%），大小不是限流原因")
else:
    print("⚠️ 资产大小差异较大，可能是限流原因之一")

if monitor_keys == actual_keys:
    print("✅ 字段结构一致")
else:
    print("⚠️ 字段结构有差异")

print("\n建议：")
print("1. 使用实际任务的 Gene 进行测试（而非模拟数据）")
print("2. 检查是否是资产内容/信号触发限流（而非大小）")
print("3. 检查是否是时间窗口内的累积请求数触发限流")
print("="*70)

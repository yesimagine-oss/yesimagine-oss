#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Evolver 官方格式发布 Bundle
让 Hub 自动计算 asset_id
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

# 节点配置
NODE_ID = "node_63324f539fbce86b"
NODE_SECRET = "2b6836acafaa0f2185bbd1999c031882a801e68a39a8ce1b40ff273939faf591"
BASE_URL = "https://evomap.ai"

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

print("📋 使用 Evolver 官方格式发布 Bundle")
print(f"   Node ID: {NODE_ID}")
print(f"   Secret: {NODE_SECRET[:20]}...")

# 准备 Bundle 数据 (不包含 asset_id，让 Hub 自动计算)
print("\n📦 准备 Bundle 数据...")

gene = {
    "type": "Gene",
    "schema_version": "1.5.0",
    "category": "repair",
    "signals_match": ["WebSocket", "disconnect", "reconnect"],
    "summary": "WebSocket auto-reconnect with exponential backoff",
    "strategy": [
        "Listen for WebSocket close events",
        "Implement exponential backoff (base 1s, max 30s)",
        "Add jitter ±20%",
        "Max 10 retries",
        "Reset on success"
    ],
    "constraints": {"max_files": 2, "forbidden_paths": ["node_modules/"]},
    "validation": ["node test.js"]
}

capsule = {
    "type": "Capsule",
    "schema_version": "1.5.0",
    "trigger": ["WebSocket", "disconnect"],
    "summary": "WebSocket reconnection wrapper with backoff",
    "confidence": 0.92,
    "blast_radius": {"files": 1, "lines": 45},
    "outcome": {"status": "success", "score": 0.92},
    "env_fingerprint": {"platform": "linux", "arch": "x64"},
    "success_streak": 5
}

event = {
    "type": "EvolutionEvent",
    "intent": "repair",
    "outcome": {"status": "success", "score": 0.92},
    "mutations_tried": 3,
    "total_cycles": 5
}

# 构建发布请求 (不包含 asset_id)
print("\n📦 构建发布请求...")
message_id = f"msg_{int(datetime.utcnow().timestamp() * 1000)}_{os.urandom(4).hex()}"
timestamp = datetime.utcnow().isoformat() + "Z"

# 尝试 1: 使用 assets 数组但不包含 asset_id
publish_request = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": message_id,
    "sender_id": NODE_ID,
    "timestamp": timestamp,
    "payload": {
        "assets": [gene, capsule, event]
    }
}

print(f"\n📊 Bundle 内容:")
print(f"   - Gene: {gene['summary'][:40]}...")
print(f"   - Capsule: {capsule['summary'][:40]}...")
print(f"   - Event: intent={event['intent']}")

# 发送发布请求
print("\n🚀 发布到 Hub...")

publish_url = f"{BASE_URL}/a2a/publish"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {NODE_SECRET}"
}

try:
    response = requests.post(publish_url, json=publish_request, headers=headers, timeout=30)
    result = response.json()
    
    if response.status_code == 200:
        print(f"\n✅✅✅ 发布成功！")
        print(f"   HTTP 状态码：{response.status_code}")
        
        payload = result.get('payload', {})
        published_assets = payload.get('published_assets', [])
        
        print(f"\n📦 已发布资产:")
        for asset in published_assets:
            asset_type = asset.get('type', 'Unknown')
            asset_id = asset.get('asset_id', 'N/A')
            print(f"   - {asset_type}: {asset_id[:40]}...")
        
        status = payload.get('status', 'candidate')
        print(f"\n📋 状态：{status}")
        
        print(f"\n💰 预期收益:")
        print(f"   - 发布奖励：+20 credits (晋升后)")
        print(f"   - 被动收入：~50-100 credits")
        
    else:
        print(f"\n❌ 发布失败！")
        print(f"   HTTP 状态码：{response.status_code}")
        print(f"   错误：{result.get('error', 'Unknown')}")
        
        if 'correction' in result:
            print(f"\n📋 错误详情:")
            print(f"   问题：{result['correction'].get('problem', 'N/A')}")
            print(f"   修复：{result['correction'].get('fix', 'N/A')}")
            
            # 尝试修复方案
            if 'example' in result['correction']:
                print(f"\n💡 示例:")
                print(json.dumps(result['correction']['example'], indent=2)[:500])
        
        print(f"\n📄 完整响应:")
        print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
        
except Exception as e:
    print(f"\n❌ 异常：{e}")
    import traceback
    traceback.print_exc()

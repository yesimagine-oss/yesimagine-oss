#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 validate 接口 - 查看详细错误
"""

import json
import sys
import hashlib
import time
import random
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)

# 读取一个 Gene 资产
asset_file = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略/gene.json")
with open(asset_file, 'r', encoding='utf-8') as f:
    asset_data = json.load(f)

print("📋 资产数据:")
print(json.dumps(asset_data, indent=2, ensure_ascii=False)[:500])

# 创建信封
timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
message_id = f"msg_{int(time.time() * 1000)}_{hashlib.md5(timestamp.encode()).hexdigest()[:8]}"

envelope = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": message_id,
    "sender_id": NODE_ID,
    "timestamp": timestamp,
    "payload": {
        "action": "publish",
        "asset_type": "Gene",
        "asset": asset_data
    }
}

print("\n📦 信封结构:")
print(json.dumps(envelope, indent=2, ensure_ascii=False)[:800])

# 调用 validate
print("\n🔍 调用 /a2a/validate...")
result = client._send_request('/a2a/validate', envelope)

print("\n📊 响应结果:")
print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])

# 检查是否有 computed_assets
if result.get('data', {}).get('payload', {}).get('computed_assets'):
    print("\n✅ computed_assets:")
    for asset in result['data']['payload']['computed_assets']:
        print(f"  - {asset.get('computed_asset_id', 'N/A')[:80]}...")

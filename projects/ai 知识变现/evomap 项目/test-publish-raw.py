#!/usr/bin/env python3
import json
import sys
import requests
from pathlib import Path
from datetime import datetime

NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"

# 加载资产包
asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")

with open(asset_dir / 'gene.json', 'r', encoding='utf-8') as f:
    gene = json.load(f)

with open(asset_dir / 'capsule.json', 'r', encoding='utf-8') as f:
    capsule = json.load(f)

with open(asset_dir / 'event.json', 'r', encoding='utf-8') as f:
    event = json.load(f)

# 构建请求
req = {
    'protocol': 'gep-a2a',
    'protocol_version': '1.0.0',
    'message_type': 'publish',
    'message_id': f'msg_{int(datetime.utcnow().timestamp()*1000)}',
    'sender_id': NODE_ID,
    'timestamp': datetime.utcnow().isoformat() + 'Z',
    'payload': {
        'assets': [gene, capsule, event]
    }
}

# 直接发送 HTTP 请求
url = "https://evomap.ai/a2a/publish"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {NODE_SECRET}"
}

print("发送请求...")
response = requests.post(url, json=req, headers=headers, timeout=30)

print(f"\nHTTP 状态码：{response.status_code}")
print(f"\n原始响应:")
print(response.text[:3000])

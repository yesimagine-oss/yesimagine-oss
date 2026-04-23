#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用现有资产包测试发布
"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"

# 加载现有资产包
asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")

with open(asset_dir / 'gene.json', 'r', encoding='utf-8') as f:
    gene = json.load(f)

with open(asset_dir / 'capsule.json', 'r', encoding='utf-8') as f:
    capsule = json.load(f)

with open(asset_dir / 'event.json', 'r', encoding='utf-8') as f:
    event = json.load(f)

print("使用现有资产包测试:")
print(f"Gene: {gene.get('summary', '')[:100]}...")
print(f"Capsule: {capsule.get('summary', '')[:100]}...")
print(f"Event: {event.get('intent', '')}")

# 构建发布请求
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

print("\n发送发布请求...")

client = GAPA2AClient(NODE_ID, NODE_SECRET)
client.hello()

result = client._send_request('/a2a/publish', req)

print("\n" + "="*60)
print("响应结果")
print("="*60)

if result.get('error'):
    print(f"❌ 错误：{result.get('error')}")
    print(f"\n详细信息:")
    if result.get('data', {}).get('details'):
        try:
            details = json.loads(result['data']['details'])
            print(json.dumps(details, indent=2, ensure_ascii=False))
        except:
            print(result['data']['details'][:1000])
    
    if result.get('data', {}).get('correction'):
        print(f"\n修复建议:")
        correction = result['data']['correction']
        if isinstance(correction, str):
            try:
                correction = json.loads(correction)
            except:
                pass
        print(json.dumps(correction, indent=2, ensure_ascii=False)[:2000])
else:
    print(f"✅ 成功！")
    print(json.dumps(result, indent=2, ensure_ascii=False))

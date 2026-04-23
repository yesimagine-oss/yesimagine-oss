#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试发布 - 获取详细错误
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"

def canonicalize(obj):
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
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonicalize(clean)
    return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'

client = GAPA2AClient(NODE_ID, NODE_SECRET)
client.hello()

# 创建最小 Gene
gene = {
    'type': 'Gene',
    'schema_version': '1.5.0',
    'category': 'test',
    'signals_match': ['test'],
    'summary': '测试资产 - 验证发布功能是否正常 (这个描述已经超过 10 个字符了)',
    'strategy': [
        '第一步：检查环境连接并确认',
        '第二步：执行 Hello 认证流程',
        '第三步：创建测试资产数据包',
        '第四步：尝试发布到平台'
    ],
    'constraints': {'max_files': 1, 'forbidden_paths': ['node_modules/']},
    'validation': ['echo "test passed"']
}
gene['asset_id'] = compute_asset_id(gene)

capsule = {
    'type': 'Capsule',
    'schema_version': '1.5.0',
    'trigger': ['test'],
    'gene': gene['asset_id'],
    'summary': '测试胶囊 - 用于验证发布流程的完整性 (这个描述已经超过 20 个字符了)',
    'confidence': 0.9,
    'blast_radius': {'files': 1, 'lines': 10},
    'outcome': {'status': 'success', 'score': 0.9},
    'code_snippet': '# Test code snippet\nprint("Hello, EvoMap!")\n# This is a test\n# Line 4\n# Line 5\n# Line 6\n# Line 7\n# Line 8\n# Line 9\n# Line 10',
    'success_streak': 1,
    'env_fingerprint': {'platform': 'linux', 'arch': 'x64', 'node_version': 'v24.14.0'}
}
capsule['asset_id'] = compute_asset_id(capsule)

event = {
    'type': 'EvolutionEvent',
    'intent': 'test',
    'capsule_id': capsule['asset_id'],
    'genes_used': [gene['asset_id']],
    'outcome': {'status': 'success', 'score': 0.9},
    'mutations_tried': 1,
    'total_cycles': 1
}
event['asset_id'] = compute_asset_id(event)

print("测试资产:")
print(f"Gene: {json.dumps(gene, indent=2, ensure_ascii=False)[:1000]}")
print(f"\nCapsule: {json.dumps(capsule, indent=2, ensure_ascii=False)[:1000]}")
print(f"\nEvent: {json.dumps(event, indent=2, ensure_ascii=False)[:500]}")

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

print("\n发送请求...")
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
        print(json.dumps(result['data']['correction'], indent=2, ensure_ascii=False))
else:
    print(f"✅ 成功！")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试发布环境 - 最小化测试

验证：
1. 能否连接 EvoMap
2. 能否通过认证
3. 能否发布资产
4. 是否被限流
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

# 节点配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"
BASE_URL = "https://evomap.ai"

def canonicalize(obj):
    """生成 canonical JSON 字符串"""
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

def test_publish():
    """测试发布功能"""
    print("="*60)
    print("EvoMap 发布环境测试")
    print("="*60)
    
    # 1. 初始化客户端
    print("\n[1/4] 初始化客户端...")
    client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)
    
    # 2. 认证
    print("[2/4] 执行 Hello 认证...")
    result = client.hello()
    
    if not result.get('success'):
        print(f"❌ 认证失败：{result.get('error')}")
        return False
    
    payload = result.get('data', {}).get('payload', {})
    print(f"✅ 认证成功")
    print(f"   Hub Node ID: {payload.get('hub_node_id')}")
    print(f"   积分余额：{payload.get('credit_balance')}")
    print(f"   声誉等级：Level {payload.get('capability_profile', {}).get('level')}")
    
    # 3. 创建测试资产
    print("\n[3/4] 创建测试资产...")
    
    gene = {
        'type': 'Gene',
        'schema_version': '1.5.0',
        'category': 'test',
        'signals_match': ['test_signal'],
        'summary': '测试资产 - 验证发布功能是否正常',
        'strategy': [
            '第一步：检查环境连接',
            '第二步：执行 Hello 认证',
            '第三步：创建测试资产',
            '第四步：尝试发布'
        ],
        'constraints': {'max_files': 1},
        'validation': ['echo "test passed"']
    }
    gene['asset_id'] = compute_asset_id(gene)
    
    capsule = {
        'type': 'Capsule',
        'schema_version': '1.5.0',
        'trigger': ['test_signal'],
        'gene': gene['asset_id'],
        'summary': '测试胶囊 - 用于验证发布流程',
        'confidence': 0.9,
        'blast_radius': {'files': 1, 'lines': 10},
        'outcome': {'status': 'success', 'score': 0.9},
        'code_snippet': 'print("Hello, EvoMap!")',
        'success_streak': 1
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
    
    print(f"   Gene: {gene['asset_id'][:50]}...")
    print(f"   Capsule: {capsule['asset_id'][:50]}...")
    print(f"   Event: {event['asset_id'][:50]}...")
    
    # 4. 发布测试
    print("\n[4/4] 尝试发布...")
    
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
    
    result = client._send_request('/a2a/publish', req)
    
    # 分析结果
    print("\n" + "="*60)
    print("测试结果")
    print("="*60)
    
    if result.get('error'):
        error = result.get('error')
        print(f"❌ 发布失败")
        print(f"   错误：{error}")
        
        if '429' in str(error) or 'server_busy' in str(result):
            print(f"\n⚠️  服务器限流（免费用户高峰期）")
            print(f"   建议：等待 23:00 后重试，或升级付费计划")
            return 'rate_limited'
        elif '400' in str(error):
            print(f"\n⚠️  请求格式错误")
            details = result.get('data', {}).get('details', '未知')
            print(f"   详情：{str(details)[:200]}")
            return 'validation_error'
        else:
            print(f"\n⚠️  未知错误")
            print(f"   响应：{json.dumps(result, ensure_ascii=False)[:500]}")
            return 'unknown_error'
    else:
        print(f"✅ 发布成功！")
        published = result.get('payload', {}).get('published_assets', [])
        print(f"   发布资产数：{len(published)}")
        for asset in published:
            print(f"   - {asset.get('type')}: {asset.get('asset_id', '')[:50]}...")
        
        status = result.get('payload', {}).get('status', 'unknown')
        print(f"   状态：{status}")
        return 'success'

if __name__ == '__main__':
    result = test_publish()
    
    print("\n" + "="*60)
    print("测试结论")
    print("="*60)
    
    if result == 'success':
        print("✅ 环境正常，可以发布资产")
        print("\n下一步：批量发布 21 个资产包")
    elif result == 'rate_limited':
        print("⚠️  环境可用，但被限流")
        print("\n建议：")
        print("1. 等待 23:00-06:00 低峰期重试")
        print("2. 或升级 Premium/Ultra 计划")
        print("3. 或单个发布（间隔 5 分钟）")
    elif result == 'validation_error':
        print("❌ 资产格式有问题，需要修复")
        print("\n建议：检查 Gene/Capsule/Event 字段")
    else:
        print("❌ 环境异常，无法发布")
        print("\n建议：检查网络连接或联系平台支持")
    
    sys.exit(0 if result == 'success' else 1)

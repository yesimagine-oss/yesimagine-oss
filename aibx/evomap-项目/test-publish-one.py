#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试发布单个资产包
处理状态码：
- 429 → 等待重试
- 409 → 跳过（已存在）
- 422 → 检查格式
- 200 → 确认 decision
"""

import json
import hashlib
import sys
import time
import requests
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

def publish_bundle(client, bundle_dir, max_retries=5):
    """发布单个资产包"""
    print(f"\n{'='*60}")
    print(f"发布：{bundle_dir.name}")
    print(f"{'='*60}")
    
    # 加载资产
    gene_path = bundle_dir / 'gene.json'
    capsule_path = bundle_dir / 'capsule.json'
    event_path = bundle_dir / 'event.json'
    
    if not all([gene_path.exists(), capsule_path.exists(), event_path.exists()]):
        print(f"❌ 资产包不完整")
        return False
    
    with open(gene_path, 'r', encoding='utf-8') as f:
        gene = json.load(f)
    with open(capsule_path, 'r', encoding='utf-8') as f:
        capsule = json.load(f)
    with open(event_path, 'r', encoding='utf-8') as f:
        event = json.load(f)
    
    # 计算 asset_id
    gene['asset_id'] = compute_asset_id(gene)
    capsule['gene'] = gene['asset_id']
    capsule['asset_id'] = compute_asset_id(capsule)
    event['capsule_id'] = capsule['asset_id']
    event['genes_used'] = [gene['asset_id']]
    event['asset_id'] = compute_asset_id(event)
    
    print(f"Gene: {gene['asset_id'][:60]}...")
    print(f"Capsule: {capsule['asset_id'][:60]}...")
    print(f"Event: {event['asset_id'][:60]}...")
    
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
    
    # 发布（带重试）
    for attempt in range(max_retries):
        print(f"\n尝试 {attempt + 1}/{max_retries}...")
        
        result = client._send_request('/a2a/publish', req)
        
        # 处理状态码
        error = result.get('error', '')
        
        if '200' in str(error) or result.get('success'):
            # ✅ 200 → 确认 decision
            print(f"\n✅ HTTP 200 成功！")
            published = result.get('payload', {}).get('published_assets', [])
            for asset in published:
                print(f"  - {asset.get('type')}: {asset.get('asset_id', '')[:60]}...")
            
            # 检查 decision 状态
            # 注意：publish 响应可能不直接返回 decision，需要后续查询
            print(f"\n📊 发布成功，资产已提交审核")
            return True
            
        elif '429' in str(error) or 'server_busy' in str(result):
            # ⚠️ 429 → 等待重试
            retry_after = result.get('data', {}).get('retry_after_ms', 3000)
            print(f"\n⚠️  HTTP 429 限流，等待 {retry_after}ms...")
            time.sleep(retry_after / 1000 + 2)
            continue
            
        elif '409' in str(error) or 'conflict' in str(error).lower():
            # ⚠️ 409 → 跳过（已存在）
            print(f"\n⚠️  HTTP 409 资产已存在，跳过")
            return True
            
        elif '422' in str(error) or 'validation' in str(error).lower():
            # ❌ 422 → 检查格式
            print(f"\n❌ HTTP 422 格式错误")
            details = result.get('data', {}).get('details', '未知')
            print(f"   详情：{str(details)[:500]}")
            
            correction = result.get('data', {}).get('correction')
            if correction:
                print(f"\n🔧 修复建议:")
                print(json.dumps(correction, indent=2, ensure_ascii=False)[:1000])
            return False
            
        else:
            # ❌ 其他错误
            print(f"\n❌ HTTP 错误：{error}")
            print(f"   响应：{json.dumps(result, ensure_ascii=False)[:500]}")
            return False
    
    print(f"\n❌ 达到最大重试次数")
    return False

# 主程序
print("="*60)
print("EvoMap 发布测试")
print("="*60)
print(f"节点：{NODE_ID}")
print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 初始化客户端
client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)

# 认证
print("\n[1/3] 认证...")
hello_result = client.hello()
if not hello_result.get('success'):
    print(f"❌ 认证失败：{hello_result.get('error')}")
    sys.exit(1)

payload = hello_result.get('data', {}).get('payload', {})
print(f"✅ 认证成功")
print(f"   Hub Node ID: {payload.get('hub_node_id')}")
print(f"   积分余额：{payload.get('credit_balance')}")
print(f"   声誉等级：Level {payload.get('capability_profile', {}).get('level')}")

# 选择测试资产包
assets_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会")
test_bundle = assets_dir / "15-短视频爆款"  # 选择一个完整的资产包

if not test_bundle.exists():
    print(f"❌ 测试资产包不存在：{test_bundle}")
    sys.exit(1)

# 发布测试
print(f"\n[2/3] 发布测试资产包...")
success = publish_bundle(client, test_bundle)

# 总结
print(f"\n[3/3] 测试总结")
print(f"{'='*60}")
if success:
    print(f"✅ 测试成功！平台适合发布资产")
    print(f"\n建议：")
    print(f"1. 可以继续发布剩余 20 个资产包")
    print(f"2. 建议分批发布（每次 5-10 个）")
    print(f"3. 遇到 429 限流时等待后重试")
else:
    print(f"❌ 测试失败！平台可能不适合发布")
    print(f"\n建议：")
    print(f"1. 检查资产格式")
    print(f"2. 等待低峰期（23:00-06:00）")
    print(f"3. 或升级 Premium 计划")

print(f"{'='*60}")

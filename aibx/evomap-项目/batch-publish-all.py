#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量发布所有资产包

使用方法:
    python3 batch-publish-all.py
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime

# 添加 lib 目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

# 节点配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"
BASE_URL = "https://evomap.ai"

# 资产包目录
ASSETS_DIR = Path(__file__).parent / '资产包'

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

def load_asset(filepath):
    """加载资产文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def publish_bundle(client, bundle_dir):
    """发布单个资产包"""
    print(f"\n{'='*60}")
    print(f"发布：{bundle_dir.name}")
    print(f"{'='*60}")
    
    # 加载资产
    gene = load_asset(bundle_dir / 'gene.json')
    capsule = load_asset(bundle_dir / 'capsule.json')
    event = load_asset(bundle_dir / 'event.json')
    
    # 设置类型和版本
    gene['type'] = 'Gene'
    gene['schema_version'] = '1.5.0'
    
    capsule['type'] = 'Capsule'
    capsule['schema_version'] = '1.5.0'
    
    event['type'] = 'EvolutionEvent'
    
    # 计算 asset_id
    gene['asset_id'] = compute_asset_id(gene)
    capsule['gene'] = gene['asset_id']
    capsule['asset_id'] = compute_asset_id(capsule)
    event['capsule_id'] = capsule['asset_id']
    event['genes_used'] = [gene['asset_id']]
    event['asset_id'] = compute_asset_id(event)
    
    print(f"Gene: {gene['asset_id'][:50]}...")
    print(f"Capsule: {capsule['asset_id'][:50]}...")
    print(f"Event: {event['asset_id'][:50]}...")
    
    # 发布 Bundle
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
    
    if result.get('error'):
        print(f"❌ 发布失败：{result.get('error')}")
        return False
    else:
        print(f"✅ 发布成功！")
        published = result.get('payload', {}).get('published_assets', [])
        for asset in published:
            print(f"  - {asset.get('type')}: {asset.get('asset_id', '')[:50]}...")
        return True

def main():
    """主函数"""
    print("="*60)
    print("EvoMap 批量资产发布工具")
    print("="*60)
    
    # 初始化客户端
    print("\n🔐 正在认证...")
    client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)
    result = client.hello()
    
    if not result.get('success'):
        print(f"❌ 认证失败：{result.get('error')}")
        sys.exit(1)
    
    print(f"✅ 认证成功！Hub Node ID: {result.get('data', {}).get('payload', {}).get('hub_node_id')}")
    
    # 获取所有资产包目录
    p0_dir = ASSETS_DIR / 'P0-机会'
    p1_dir = ASSETS_DIR / 'P1-机会'
    
    bundles = []
    
    if p0_dir.exists():
        for d in sorted(p0_dir.iterdir()):
            if d.is_dir() and (d / 'gene.json').exists():
                bundles.append(('P0', d))
    
    if p1_dir.exists():
        for d in sorted(p1_dir.iterdir()):
            if d.is_dir() and (d / 'gene.json').exists():
                bundles.append(('P1', d))
    
    print(f"\n📦 找到 {len(bundles)} 个资产包")
    print(f"   P0: {len([b for b in bundles if b[0] == 'P0'])} 个")
    print(f"   P1: {len([b for b in bundles if b[0] == 'P1'])} 个")
    
    # 批量发布
    success_count = 0
    fail_count = 0
    
    for priority, bundle_dir in bundles:
        try:
            if publish_bundle(client, bundle_dir):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"❌ 异常：{e}")
            fail_count += 1
        
        # 防止限流，每个资产包间隔 2 秒
        import time
        time.sleep(2)
    
    # 汇总报告
    print(f"\n{'='*60}")
    print("发布完成！")
    print(f"{'='*60}")
    print(f"✅ 成功：{success_count} 个")
    print(f"❌ 失败：{fail_count} 个")
    print(f"📊 总计：{len(bundles)} 个")
    
    # 保存发布结果
    result_file = Path(__file__).parent / f'发布结果 -{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total': len(bundles),
            'success': success_count,
            'failed': fail_count,
            'bundles': [
                {
                    'priority': p,
                    'name': d.name,
                    'path': str(d)
                }
                for p, d in bundles
            ]
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 结果已保存到：{result_file}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 资产发布 - 最终解决方案

根据范老师指引修复：
1. schema_version = "1.6.0"
2. Capsule 添加 gene 引用和 diff 字段
3. 使用 ensure_ascii=False 计算哈希
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


def compute_asset_id_canonical(asset: dict) -> str:
    """
    官方 canonical JSON 计算 asset_id
    
    关键：ensure_ascii=False 匹配 JS 的 JSON.stringify
    """
    asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    return f"sha256:{hash_hex}"


def create_publish_envelope(assets: list) -> dict:
    """创建 publish 信封"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
    message_id = f"msg_{int(time.time() * 1000)}_{hashlib.md5(timestamp.encode()).hexdigest()[:8]}"
    
    return {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": message_id,
        "sender_id": NODE_ID,
        "timestamp": timestamp,
        "payload": {
            "assets": assets
        }
    }


def publish_bundle(assets: list) -> dict:
    """发布 Bundle"""
    envelope = create_publish_envelope(assets)
    result = client._send_request('/a2a/publish', envelope)
    return result


def main():
    """主函数"""
    print("="*60)
    print("🚀 EvoMap 资产发布 - 最终解决方案")
    print("="*60)
    
    # 认证
    hello_result = client.hello()
    if not hello_result.get('success'):
        print(f"❌ 认证失败")
        return
    
    print(f"✅ 认证成功")
    
    # 资产目录
    asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会")
    bundle_name = "01-抖音带货选品策略"
    bundle_path = asset_dir / bundle_name
    
    print(f"\n📦 发布 Bundle: {bundle_name}")
    
    # 读取 3 个组件
    assets = []
    asset_files = [
        ('gene.json', 'Gene'),
        ('capsule.json', 'Capsule'),
        ('event.json', 'EvolutionEvent')
    ]
    
    gene_asset_id = None
    
    for filename, asset_type in asset_files:
        asset_file = bundle_path / filename
        with open(asset_file, 'r', encoding='utf-8') as f:
            asset_data = json.load(f)
        
        # 确保 type 正确
        asset_data['type'] = asset_type
        
        # 确保 schema_version 是 1.6.0（关键修复！）
        asset_data['schema_version'] = '1.6.0'
        
        # 对于 Capsule，需要添加 gene 引用
        if asset_type == 'Capsule' and gene_asset_id:
            asset_data['gene'] = gene_asset_id
        
        # 计算 asset_id
        asset_id = compute_asset_id_canonical(asset_data)
        
        # 对于 Gene，保存 asset_id 供 Capsule 引用
        if asset_type == 'Gene':
            gene_asset_id = asset_id
        
        asset_data['asset_id'] = asset_id
        assets.append(asset_data)
        
        print(f"\n📋 {asset_type}:")
        print(f"   asset_id: {asset_id[:60]}...")
        if asset_type == 'Capsule':
            print(f"   gene: {gene_asset_id[:60]}...")
            print(f"   diff: {'✅ 已添加' if 'diff' in asset_data else '❌ 缺失'}")
    
    # 发布
    print(f"\n🚀 发布 Bundle...")
    result = publish_bundle(assets)
    
    if result.get('error'):
        print(f"\n❌ 发布失败：{result.get('error')}")
        # 尝试解析 details 查找 computed_asset_id
        if result.get('data', {}).get('details'):
            try:
                details = json.loads(result['data']['details'])
                print(f"\n详细错误:")
                print(json.dumps(details, indent=2, ensure_ascii=False))
                
                # 查找 computed_asset_id
                if 'computed_asset_id' in details.get('correction', {}):
                    print(f"\n✅ Hub 返回的正确 asset_id:")
                    print(details['correction']['computed_asset_id'])
            except Exception as e:
                print(f"\n解析失败：{e}")
                print(f"原始详情：{result['data']['details'][:500]}")
    else:
        print(f"\n✅ 发布成功！")
        print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])


if __name__ == '__main__':
    main()

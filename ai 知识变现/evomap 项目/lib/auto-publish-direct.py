#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 资产发布 - 直接发布模式

根据错误信息，Hub 已经告诉我们正确的 canonical JSON 格式。
让我们尝试直接使用我们计算的 asset_id 发布。
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
    """计算 asset_id - 不包含 asset_id 字段"""
    asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'))
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
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
    
    # 打印信封用于调试
    print("\n📦 发送的请求:")
    print(json.dumps(envelope, indent=2, ensure_ascii=False)[:2000])
    
    result = client._send_request('/a2a/publish', envelope)
    return result


def main():
    """主函数"""
    print("="*60)
    print("🚀 EvoMap 资产发布 - 直接发布模式")
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
    
    for filename, asset_type in asset_files:
        asset_file = bundle_path / filename
        with open(asset_file, 'r', encoding='utf-8') as f:
            asset_data = json.load(f)
        
        # 确保 type 正确
        asset_data['type'] = asset_type
        
        # 确保 schema_version 是 1.5.0
        asset_data['schema_version'] = '1.5.0'
        
        # 计算 asset_id
        asset_id = compute_asset_id_canonical(asset_data)
        asset_data['asset_id'] = asset_id
        
        assets.append(asset_data)
        print(f"\n📋 {asset_type}:")
        print(f"   asset_id: {asset_id[:60]}...")
    
    # 发布
    print(f"\n🚀 发布 Bundle...")
    result = publish_bundle(assets)
    
    if result.get('error'):
        print(f"\n❌ 发布失败：{result.get('error')}")
        details = result.get('details', '')
        if isinstance(details, str):
            try:
                details_json = json.loads(details)
                print(f"\n详细错误:")
                print(json.dumps(details_json, indent=2, ensure_ascii=False))
            except:
                print(f"详情：{details[:500]}")
    else:
        print(f"\n✅ 发布成功！")
        print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])


if __name__ == '__main__':
    main()

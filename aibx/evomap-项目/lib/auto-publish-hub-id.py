#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 资产自动发布工具 - 使用 Hub 计算的 asset_id

修复方案：
1. 调用 validate 获取 Hub 官方计算的 computed_asset_id
2. 用正确的 asset_id 替换
3. 再次调用 publish 发布
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


def validate_and_get_computed_ids(assets: list) -> dict:
    """调用 validate 获取 Hub 计算的 asset_id"""
    # 先移除 asset_id 字段（让 Hub 计算）
    assets_without_id = []
    for asset in assets:
        asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
        assets_without_id.append(asset_copy)
    
    envelope = create_publish_envelope(assets_without_id)
    result = client._send_request('/a2a/validate', envelope)
    return result


def publish_with_correct_ids(assets_with_correct_ids: list) -> dict:
    """使用正确的 asset_id 发布"""
    envelope = create_publish_envelope(assets_with_correct_ids)
    result = client._send_request('/a2a/publish', envelope)
    return result


def main():
    """主函数"""
    print("="*60)
    print("🚀 EvoMap 资产自动发布工具（Hub ID 修复版）")
    print("="*60)
    
    # 认证
    print(f"\n🔐 正在认证...")
    hello_result = client.hello()
    if not hello_result.get('success'):
        print(f"❌ 认证失败：{hello_result}")
        return
    
    print(f"✅ 认证成功：{hello_result.get('data', {}).get('payload', {}).get('hub_node_id')}")
    
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
        
        # 添加 type（如果不存在）
        if 'type' not in asset_data:
            asset_data['type'] = asset_type
        
        # 确保 schema_version 是 1.5.0
        if 'schema_version' not in asset_data:
            asset_data['schema_version'] = '1.5.0'
        
        assets.append(asset_data)
        print(f"✅ 读取 {asset_type}")
    
    # 步骤 1: 调用 validate 获取 Hub 计算的 asset_id
    print(f"\n🔍 步骤 1: 调用 validate 获取 Hub 计算的 asset_id...")
    validate_result = validate_and_get_computed_ids(assets)
    
    if validate_result.get('error'):
        print(f"❌ Validate 失败：{validate_result.get('error')}")
        print(f"详情：{str(validate_result.get('details', ''))[:500]}")
        return
    
    # 提取 computed_asset_id
    payload = validate_result.get('payload', {})
    computed_assets = payload.get('computed_assets', [])
    
    if not computed_assets:
        print(f"❌ 未找到 computed_assets")
        print(f"响应：{json.dumps(validate_result, indent=2)[:500]}")
        return
    
    print(f"✅ Validate 成功！获取到 {len(computed_assets)} 个 computed_asset_id")
    
    # 步骤 2: 将正确的 asset_id 添加到资产
    print(f"\n🔧 步骤 2: 添加 Hub 计算的 asset_id...")
    assets_with_ids = []
    for i, asset in enumerate(assets):
        computed_id = computed_assets[i].get('computed_asset_id')
        if computed_id:
            asset_copy = asset.copy()
            asset_copy['asset_id'] = computed_id
            assets_with_ids.append(asset_copy)
            print(f"   {asset['type']}: {computed_id[:60]}...")
        else:
            print(f"❌ 未找到第 {i+1} 个资产的 computed_asset_id")
            return
    
    # 步骤 3: 发布
    print(f"\n🚀 步骤 3: 调用 publish 发布 Bundle...")
    publish_result = publish_with_correct_ids(assets_with_ids)
    
    if publish_result.get('error'):
        print(f"❌ Publish 失败：{publish_result.get('error')}")
        print(f"详情：{str(publish_result.get('details', ''))[:500]}")
    else:
        print(f"✅ Publish 成功！")
        print(f"结果：{json.dumps(publish_result, indent=2, ensure_ascii=False)[:1000]}")


if __name__ == '__main__':
    main()

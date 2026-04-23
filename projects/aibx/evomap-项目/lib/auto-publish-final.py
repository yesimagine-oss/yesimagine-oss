#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 资产自动发布工具 - 最终修复版

根据 Hub 官方 skill.md 文档修复：
1. 使用 validate 接口预验证
2. 正确的 canonical JSON 计算
3. Bundle 格式：assets 数组
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
    
    1. 移除 asset_id 字段
    2. 使用 sort_keys=True, separators=(',', ':')
    3. SHA256 哈希
    4. 添加 sha256: 前缀
    """
    asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'))
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
    return f"sha256:{hash_hex}"


def create_publish_envelope(assets: list) -> dict:
    """
    创建 publish 信封（7 要素）
    
    assets: [Gene, Capsule, EvolutionEvent] 数组
    """
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
            "assets": assets  # 注意：是 assets 数组，不是单个 asset
        }
    }


def validate_bundle(assets: list) -> dict:
    """调用 validate 接口验证 Bundle"""
    envelope = create_publish_envelope(assets)
    result = client._send_request('/a2a/validate', envelope)
    return result


def publish_bundle(assets: list) -> dict:
    """发布完整 Bundle"""
    envelope = create_publish_envelope(assets)
    result = client._send_request('/a2a/publish', envelope)
    return result


def main():
    """主函数"""
    print("="*60)
    print("🚀 EvoMap 资产自动发布工具（最终修复版）")
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
    
    # 先测试第一个 Bundle
    bundle_name = "01-抖音带货选品策略"
    bundle_path = asset_dir / bundle_name
    
    print(f"\n📦 测试 Bundle: {bundle_name}")
    
    # 读取 3 个组件
    assets = []
    asset_files = [
        ('gene.json', 'Gene'),
        ('capsule.json', 'Capsule'),
        ('event.json', 'EvolutionEvent')
    ]
    
    for filename, asset_type in asset_files:
        asset_file = bundle_path / filename
        if not asset_file.exists():
            print(f"❌ 文件不存在：{asset_file}")
            return
        
        with open(asset_file, 'r', encoding='utf-8') as f:
            asset_data = json.load(f)
        
        # 计算正确的 asset_id
        asset_id = compute_asset_id_canonical(asset_data)
        print(f"\n📋 {asset_type}:")
        print(f"   计算的 asset_id: {asset_id[:60]}...")
        
        # 添加 asset_id 和 type
        asset_data['asset_id'] = asset_id
        asset_data['type'] = asset_type
        
        # 确保 schema_version 是 1.5.0（根据已发布资产的版本）
        if 'schema_version' not in asset_data:
            asset_data['schema_version'] = '1.5.0'
        
        assets.append(asset_data)
    
    # 调用 validate 验证
    print(f"\n🔍 调用 /a2a/validate 验证 Bundle...")
    validate_result = validate_bundle(assets)
    
    if validate_result.get('error'):
        print(f"❌ Validate 失败：{validate_result.get('error')}")
        print(f"详情：{str(validate_result.get('details', ''))[:500]}")
    else:
        print(f"✅ Validate 成功！")
        
        # 发布
        print(f"\n🚀 调用 /a2a/publish 发布 Bundle...")
        publish_result = publish_bundle(assets)
        
        if publish_result.get('error'):
            print(f"❌ Publish 失败：{publish_result.get('error')}")
            print(f"详情：{str(publish_result.get('details', ''))[:500]}")
        else:
            print(f"✅ Publish 成功！")
            print(f"结果：{json.dumps(publish_result, indent=2, ensure_ascii=False)[:1000]}")


if __name__ == '__main__':
    main()

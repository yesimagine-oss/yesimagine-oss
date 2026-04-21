#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 资产自动发布工具 - 使用官方 canonical JSON 计算 asset_id

修复方案：
1. 使用官方方法计算 asset_id（canonical JSON + SHA256）
2. 添加到资产数据中
3. 调用 publish 发布
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


def compute_asset_id(asset: dict) -> str:
    """
    计算 asset_id（官方方法）
    
    1. 移除 asset_id 字段（如果存在）
    2. Canonical JSON（sorted keys, no spaces）
    3. SHA256 哈希
    4. 添加 sha256: 前缀
    """
    # 创建副本并移除 asset_id
    asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
    
    # Canonical JSON
    canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'))
    
    # SHA256
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
    
    return f"sha256:{hash_hex}"


def publish_asset_with_computed_id(asset_type: str, asset_data: dict) -> dict:
    """
    计算 asset_id 并发布资产
    """
    # 计算 asset_id
    asset_id = compute_asset_id(asset_data)
    print(f"   计算的 asset_id: {asset_id[:50]}...")
    
    # 添加到资产数据
    asset_data_with_id = asset_data.copy()
    asset_data_with_id['asset_id'] = asset_id
    
    # 确保 type 字段正确
    asset_data_with_id['type'] = asset_type
    
    # 确保 schema_version 存在
    if 'schema_version' not in asset_data_with_id:
        asset_data_with_id['schema_version'] = '1.6.0'
    
    print(f"\n🚀 发布 {asset_type}...")
    
    # 发布资产
    result = client.publish_asset(asset_type, asset_data_with_id)
    
    return result


def main():
    """主函数"""
    print("="*60)
    print("🚀 EvoMap 资产自动发布工具（Canonical JSON 修复版）")
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
    
    bundles = [
        "01-抖音带货选品策略",
        "02-直播间搭建指南",
    ]
    
    print(f"\n📦 准备发布 {len(bundles)} 个 Bundle（先测试前 2 个）...\n")
    
    # 发布统计
    stats = {'total': 0, 'success': 0, 'failed': 0}
    
    # 发布每个 Bundle
    for bundle_idx, bundle_name in enumerate(bundles):
        bundle_path = asset_dir / bundle_name
        
        print(f"\n{'='*60}")
        print(f"📦 Bundle {bundle_idx + 1}/{len(bundles)}: {bundle_name}")
        print(f"{'='*60}")
        
        assets_map = [
            ('Gene', 'gene.json'),
            ('Capsule', 'capsule.json'),
            ('EvolutionEvent', 'event.json')
        ]
        
        for asset_type, filename in assets_map:
            asset_file = bundle_path / filename
            
            if not asset_file.exists():
                print(f"\n⚠️ 跳过：{filename} 不存在")
                continue
            
            with open(asset_file, 'r', encoding='utf-8') as f:
                asset_data = json.load(f)
            
            print(f"\n🔹 发布 {asset_type} ({filename})...")
            stats['total'] += 1
            
            result = publish_asset_with_computed_id(asset_type, asset_data)
            
            if result.get('success'):
                print(f"✅ {asset_type} 发布成功！")
                print(f"   Asset ID: {result.get('asset_id', 'N/A')[:50]}...")
                stats['success'] += 1
            else:
                print(f"❌ {asset_type} 发布失败")
                print(f"   错误：{result.get('error', 'Unknown')}")
                print(f"   详情：{str(result.get('data', {}))[:200]}")
                stats['failed'] += 1
            
            # 速率限制：等待 7 秒
            if asset_type != 'EvolutionEvent':
                wait_time = 7 + random.uniform(0.5, 1.5)
                print(f"⏳ 等待 {wait_time:.1f} 秒...")
                time.sleep(wait_time)
        
        if bundle_idx < len(bundles) - 1:
            print(f"\n⏳ Bundle 间等待 15 秒...")
            time.sleep(15)
    
    # 最终统计
    print(f"\n{'='*60}")
    print("📊 发布统计")
    print(f"{'='*60}")
    print(f"总计：{stats['total']} 个组件")
    print(f"成功：{stats['success']} 个 ✅")
    print(f"失败：{stats['failed']} 个 ❌")
    
    if stats['success'] > 0:
        print(f"\n🎉 发布完成！成功率：{stats['success']/stats['total']*100:.1f}%")
        
        # 检查积分
        print(f"\n📊 检查积分余额...")
        final_hello = client.hello()
        credit_balance = final_hello.get('data', {}).get('payload', {}).get('credit_balance', 'Unknown')
        print(f"积分余额：{credit_balance}")
    else:
        print(f"\n❌ 全部失败，需要进一步调试")


if __name__ == '__main__':
    main()

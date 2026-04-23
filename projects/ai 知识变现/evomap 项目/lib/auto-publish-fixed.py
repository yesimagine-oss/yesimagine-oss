#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 资产自动发布工具 - 使用 validate 接口修复 asset_id

修复方案：
1. 调用 /a2a/validate 获取 Hub 官方计算的 computed_asset_id
2. 用正确的 asset_id 替换
3. 调用 /a2a/publish 发布
"""

import json
import sys
import hashlib
import time
import random
from datetime import datetime
from pathlib import Path

# 导入 GEP-A2A 客户端
sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

# 节点配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

# 初始化客户端
client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)


def create_envelope(asset_type: str, asset_data: dict) -> dict:
    """创建 A2A 协议信封（7 要素）"""
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
            "action": "publish",
            "asset_type": asset_type,
            "asset": asset_data
        }
    }


def validate_asset(asset_type: str, asset_data: dict) -> dict:
    """调用 validate 接口获取正确的 asset_id"""
    envelope = create_envelope(asset_type, asset_data)
    
    # 调用 validate 接口
    result = client._send_request('/a2a/validate', envelope)
    
    if result.get('success'):
        data = result.get('data', {})
        payload = data.get('payload', {})
        computed_assets = payload.get('computed_assets', [])
        
        if computed_assets:
            computed_asset_id = computed_assets[0].get('computed_asset_id')
            return {
                'success': True,
                'computed_asset_id': computed_asset_id,
                'raw_response': result
            }
    
    return {
        'success': False,
        'error': result.get('error', 'Unknown error'),
        'raw_response': result
    }


def publish_asset_with_fix(asset_type: str, asset_data: dict) -> dict:
    """
    修复 asset_id 并发布资产
    
    步骤：
    1. 调用 validate 获取正确的 computed_asset_id
    2. 将正确的 asset_id 添加到 asset_data
    3. 调用 publish 发布
    """
    print(f"\n🔍 步骤 1: 调用 validate 获取正确的 asset_id...")
    
    # 步骤 1: 获取正确的 asset_id
    validate_result = validate_asset(asset_type, asset_data)
    
    if not validate_result['success']:
        print(f"❌ validate 失败：{validate_result['error']}")
        return validate_result
    
    computed_asset_id = validate_result['computed_asset_id']
    print(f"✅ 获取到正确的 asset_id: {computed_asset_id[:50]}...")
    
    # 步骤 2: 添加 asset_id 到资产数据
    asset_data_with_id = asset_data.copy()
    asset_data_with_id['asset_id'] = computed_asset_id
    
    # 确保包含 strategy 字段（Gene 必需）
    if asset_type == 'Gene' and 'strategy' not in asset_data_with_id:
        print(f"⚠️ 警告：Gene 缺少 strategy 字段")
    
    print(f"\n🚀 步骤 2: 调用 publish 发布资产...")
    
    # 步骤 3: 发布资产
    envelope = create_envelope(asset_type, asset_data_with_id)
    publish_result = client._send_request('/a2a/publish', envelope)
    
    return {
        'success': publish_result.get('success', False),
        'asset_id': computed_asset_id,
        'publish_result': publish_result
    }


def main():
    """主函数"""
    print("="*60)
    print("🚀 EvoMap 资产自动发布工具（修复版）")
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
        "03-短视频爆款公式",
        "04-达人合作流程"
    ]
    
    print(f"\n📦 准备发布 {len(bundles)} 个 Bundle...\n")
    
    # 发布统计
    stats = {
        'total': 0,
        'success': 0,
        'failed': 0
    }
    
    # 发布每个 Bundle
    for bundle_idx, bundle_name in enumerate(bundles):
        bundle_path = asset_dir / bundle_name
        
        print(f"\n{'='*60}")
        print(f"📦 Bundle {bundle_idx + 1}/{len(bundles)}: {bundle_name}")
        print(f"{'='*60}")
        
        # 资产类型和文件映射
        assets_map = [
            ('Gene', 'gene.json'),
            ('Capsule', 'capsule.json'),
            ('EvolutionEvent', 'event.json')
        ]
        
        # 发布每个组件
        for asset_type, filename in assets_map:
            asset_file = bundle_path / filename
            
            if not asset_file.exists():
                print(f"\n⚠️ 跳过：{filename} 不存在")
                continue
            
            # 读取资产数据
            with open(asset_file, 'r', encoding='utf-8') as f:
                asset_data = json.load(f)
            
            print(f"\n🔹 发布 {asset_type} ({filename})...")
            stats['total'] += 1
            
            # 发布资产（带修复）
            result = publish_asset_with_fix(asset_type, asset_data)
            
            if result['success']:
                print(f"✅ {asset_type} 发布成功！")
                print(f"   Asset ID: {result['asset_id'][:50]}...")
                stats['success'] += 1
            else:
                print(f"❌ {asset_type} 发布失败")
                print(f"   错误：{result.get('publish_result', {}).get('error', 'Unknown')}")
                stats['failed'] += 1
            
            # 速率限制：等待 7 秒（10 次/分钟 = 6 秒/次，加 1 秒缓冲）
            if asset_type != 'EvolutionEvent':
                wait_time = 7 + random.uniform(0.5, 1.5)
                print(f"⏳ 等待 {wait_time:.1f} 秒（避免速率限制）...")
                time.sleep(wait_time)
        
        # Bundle 间等待更长时间
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
    print(f"成功率：{stats['success']/stats['total']*100:.1f}%")
    
    # 检查最终状态
    print(f"\n📊 检查最终状态...")
    final_hello = client.hello()
    credit_balance = final_hello.get('data', {}).get('payload', {}).get('credit_balance', 'Unknown')
    print(f"积分余额：{credit_balance}")
    
    print(f"\n🎉 发布完成！")


if __name__ == '__main__':
    main()

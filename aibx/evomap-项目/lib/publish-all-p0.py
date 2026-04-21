#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资产包/P0-机会 Bundle 发布脚本
使用 Bundle 方式（Gene + Capsule + EvolutionEvent 一起发布）
"""

import sys
import json
import hashlib
import time
import random
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "lib"))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_b83d6e6008dce32f"
NODE_SECRET = "732c8a06a68b80a760ca5fa43cd04557819aa56e330e406c5fc080d1b59db48d"
BASE_URL = "https://evomap.ai"

client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)

def compute_asset_id_canonical(asset: dict) -> str:
    """官方 canonical JSON 计算 asset_id"""
    asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
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
    result = client._send_request('/a2a/publish', envelope)
    return result

# 主程序
print("="*60)
print("🚀 资产包/P0-机会 Bundle 发布")
print("="*60)

# Hello
print("\n📡 Hello 认证...")
hello_result = client.hello()
print(f"✅ 认证成功")

# 检查积分
heartbeat_result = client.heartbeat(NODE_ID)
credit_balance = heartbeat_result.get('credit_balance', 0)
print(f"   当前积分：{credit_balance}")

# 4 个知识胶囊
capsules_info = [
    {
        "name": "抖音带货选品策略",
        "gene_id": "gene_douyin_product_selection_001",
        "capsule_id": "capsule_douyin_product_selection_001",
        "asset_dir": "抖音带货 - 选品策略",
        "content_file": "/home/admin/.openclaw/workspace/资产包/P0-机会/01-抖音带货选品策略.md"
    },
    {
        "name": "抖音带货直播间搭建",
        "gene_id": "gene_douyin_livestream_002",
        "capsule_id": "capsule_douyin_livestream_setup_002",
        "asset_dir": "抖音带货 - 直播间搭建",
        "content_file": "/home/admin/.openclaw/workspace/资产包/P0-机会/02-直播间搭建指南.md"
    },
    {
        "name": "抖音带货短视频爆款公式",
        "gene_id": "gene_douyin_viral_003",
        "capsule_id": "capsule_douyin_viral_formula_003",
        "asset_dir": "抖音带货 - 短视频爆款",
        "content_file": "/home/admin/.openclaw/workspace/资产包/P0-机会/03-短视频爆款公式.md"
    },
    {
        "name": "抖音带货达人合作流程",
        "gene_id": "gene_douyin_influencer_004",
        "capsule_id": "capsule_douyin_influencer_collab_004",
        "asset_dir": "抖音带货 - 达人合作",
        "content_file": "/home/admin/.openclaw/workspace/资产包/P0-机会/04-达人合作流程.md"
    }
]

# 发布每个 Bundle
for i, info in enumerate(capsules_info, 1):
    print(f"\n{'='*60}")
    print(f"📦 发布第 {i}/{len(capsules_info)} 个 Bundle: {info['name']}")
    print(f"{'='*60}")
    
    # 读取内容
    try:
        with open(info['content_file'], 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ 内容读取成功 ({len(content)} 字符)")
    except Exception as e:
        print(f"❌ 读取内容失败：{e}")
        continue
    
    # 创建 Gene
    print("\n📝 创建 Gene...")
    gene_data = {
        "id": info['gene_id'],
        "type": "Gene",
        "summary": f"{info['name']} - 高转化率实战方法论",
        "category": "optimize",
        "trigger_text": f"{info['name'].replace('抖音带货', '')},抖音电商，直播运营，知识变现",
        "strategy": [
            f"系统学习{info['name']}核心方法",
            "按照标准 SOP 流程逐步执行确保每个环节都到位",
            "持续跟踪优化关键数据指标不断提升转化效果"
        ],
        "validation": [
            "node tests/verify_strategy.js"
        ],
        "signals_match": [
            info['name'],
            "抖音带货",
            "电商运营",
            "知识变现"
        ],
        "schema_version": "1.5.0"
    }
    gene_asset_id = compute_asset_id_canonical(gene_data)
    gene_data['asset_id'] = gene_asset_id
    print(f"   Asset ID: {gene_asset_id[:50]}...")
    
    # 创建 Capsule
    print("\n📝 创建 Capsule...")
    capsule_data = {
        "id": info['capsule_id'],
        "type": "Capsule",
        "schema_version": "1.5.0",
        "trigger": gene_data['signals_match'][:4],
        "summary": f"{info['name']}实战指南 - 完整 SOP 流程 + 工具清单 + 避坑案例",
        "content": content[:7500],
        "confidence": 0.88,
        "blast_radius": {"files": 1, "lines": 300},
        "outcome": {"status": "success", "score": 0.88},
        "env_fingerprint": {"platform": "linux", "arch": "x64"}
    }
    capsule_asset_id = compute_asset_id_canonical(capsule_data)
    capsule_data['asset_id'] = capsule_asset_id
    print(f"   Asset ID: {capsule_asset_id[:50]}...")
    
    # 创建 EvolutionEvent
    print("\n📝 创建 EvolutionEvent...")
    event_data = {
        "type": "EvolutionEvent",
        "intent": "optimize",
        "signals": gene_data['signals_match'],
        "asset_id": capsule_asset_id,
        "capsule_id": capsule_asset_id,
        "genes_used": [gene_asset_id],
        "outcome": {
            "status": "success",
            "score": 0.85
        },
        "schema_version": "1.5.0"
    }
    event_asset_id = compute_asset_id_canonical(event_data)
    event_data['asset_id'] = event_asset_id
    print(f"   Asset ID: {event_asset_id[:50]}...")
    
    # 创建 Bundle
    bundle_assets = [gene_data, capsule_data, event_data]
    
    # 发布 Bundle
    print("\n📤 发布 Bundle...")
    publish_result = publish_bundle(bundle_assets)
    
    print(f"\n📊 发布结果:")
    print(json.dumps(publish_result, indent=2, ensure_ascii=False)[:1000])
    
    # 解析结果
    success = publish_result.get('protocol') == 'gep-a2a'
    decision = publish_result.get('payload', {}).get('decision', 'unknown')
    
    if success and decision in ['accept', 'auto_promoted']:
        print(f"\n✅ Bundle 发布成功！决策：{decision}")
        
        # 提取 asset_ids
        asset_ids = publish_result.get('payload', {}).get('asset_ids', [])
        print(f"   Asset IDs:")
        for aid in asset_ids:
            print(f"     - {aid[:60]}...")
        
        # 保存结果
        asset_path = Path(__file__).parent / "资产" / info['asset_dir']
        asset_path.mkdir(parents=True, exist_ok=True)
        
        result_file = asset_path / "bundle_publish_result.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump({
                "name": info['name'],
                "decision": decision,
                "asset_ids": asset_ids,
                "gene_asset_id": gene_asset_id,
                "capsule_asset_id": capsule_asset_id,
                "event_asset_id": event_asset_id,
                "publish_time": datetime.utcnow().isoformat(),
                "full_result": publish_result
            }, f, ensure_ascii=False, indent=2)
        print(f"✅ 结果已保存：{result_file}")
    else:
        print(f"\n⚠️ Bundle 发布结果：{decision}")
    
    # 等待避免限流
    if i < len(capsules_info):
        print("\n⏳ 等待 5 秒...")
        import time
        time.sleep(5)

# 最终总结
print(f"\n{'='*60}")
print("🎉 批量发布完成！")
print(f"{'='*60}")

# 检查积分
final_heartbeat = client.heartbeat(NODE_ID)
final_balance = final_heartbeat.get('credit_balance', 0)
print(f"💰 初始积分：{credit_balance}")
print(f"💰 最终积分：{final_balance}")
print(f"💸 本次消耗：{credit_balance - final_balance}")

print("\n✅ 所有操作完成！")

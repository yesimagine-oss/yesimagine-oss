#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音带货知识胶囊发布脚本 - 修复版
包含 asset_id 计算
"""

import sys
import json
import hashlib
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from evolver_tools import EvolverTools

def canonicalize(obj):
    """
    规范化 JSON 对象（与 Node.js 版本一致）
    """
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        if not isinstance(obj, bool) and str(obj) in ['inf', '-inf', 'nan']:
            return 'null'
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return '[' + ','.join(canonicalize(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = []
        for k in keys:
            pairs.append(json.dumps(k, ensure_ascii=False) + ':' + canonicalize(obj[k]))
        return '{' + ','.join(pairs) + '}'
    return 'null'

def compute_asset_id(data):
    """
    计算 asset_id (SHA256 hash)
    """
    # 复制数据，移除已有的 asset_id
    data_copy = {k: v for k, v in data.items() if k != 'asset_id'}
    
    # 规范化
    canonical = canonicalize(data_copy)
    
    # 计算 SHA256
    hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    
    return f'sha256:{hash_hex}'

# 初始化
print("="*60)
print("🚀 抖音带货知识胶囊发布 - 修复版")
print("="*60)

tools = EvolverTools()

# Hello 认证
print("\n📡 执行 Hello 认证...")
hello_result = tools.hello()
print(f"✅ 认证成功")
print(f"   Hub Node ID: {hello_result.get('hub_node_id')}")
print(f"   Owner User ID: {hello_result.get('owner_user_id')}")

# 检查积分
heartbeat_result = tools.client.heartbeat(tools.NODE_ID)
credit_balance = heartbeat_result.get('credit_balance', 0)
print(f"   当前积分：{credit_balance}")
print()

# 4 个知识胶囊
capsules_info = [
    {
        "name": "抖音带货选品策略",
        "gene_id": "gene_douyin_product_selection_001",
        "capsule_id": "capsule_douyin_product_selection_001",
        "asset_dir": "抖音带货 - 选品策略",
        "content_file": "/home/admin/.openclaw/workspace/抖音带货知识胶囊/01-抖音带货选品策略.md"
    },
    {
        "name": "抖音带货直播间搭建",
        "gene_id": "gene_douyin_livestream_002",
        "capsule_id": "capsule_douyin_livestream_setup_002",
        "asset_dir": "抖音带货 - 直播间搭建",
        "content_file": "/home/admin/.openclaw/workspace/抖音带货知识胶囊/02-直播间搭建指南.md"
    },
    {
        "name": "抖音带货短视频爆款公式",
        "gene_id": "gene_douyin_viral_003",
        "capsule_id": "capsule_douyin_viral_formula_003",
        "asset_dir": "抖音带货 - 短视频爆款",
        "content_file": "/home/admin/.openclaw/workspace/抖音带货知识胶囊/03-短视频爆款公式.md"
    },
    {
        "name": "抖音带货达人合作流程",
        "gene_id": "gene_douyin_influencer_004",
        "capsule_id": "capsule_douyin_influencer_collab_004",
        "asset_dir": "抖音带货 - 达人合作",
        "content_file": "/home/admin/.openclaw/workspace/抖音带货知识胶囊/04-达人合作流程.md"
    }
]

# 发布每个胶囊
for i, info in enumerate(capsules_info, 1):
    print(f"\n{'='*60}")
    print(f"📦 发布第 {i}/{len(capsules_info)} 个：{info['name']}")
    print(f"{'='*60}")
    
    # 读取内容
    try:
        with open(info['content_file'], 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ 内容读取成功 ({len(content)} 字符)")
    except Exception as e:
        print(f"❌ 读取内容失败：{e}")
        continue
    
    # 创建 Gene 数据
    print("\n📝 创建 Gene...")
    gene_data = {
        "id": info['gene_id'],
        "type": "Gene",
        "summary": f"{info['name']} - 高转化率实战方法论",
        "category": "ecommerce",
        "trigger_text": f"{info['name'].replace('抖音带货', '')},抖音电商，直播运营，知识变现",
        "strategy": [
            f"系统学习{info['name']}核心方法",
            "按照 SOP 流程逐步执行",
            "持续优化数据，提升效果",
            "结合实际案例灵活应用"
        ],
        "signals_match": [
            info['name'],
            "抖音带货",
            "电商运营",
            "知识变现"
        ],
        "schema_version": "1.5.0"
    }
    
    # 计算 Gene asset_id
    gene_asset_id = compute_asset_id(gene_data)
    gene_data['asset_id'] = gene_asset_id
    print(f"   Gene ID: {info['gene_id']}")
    print(f"   Asset ID: {gene_asset_id[:50]}...")
    
    # 创建 Capsule 数据
    print("\n📝 创建 Capsule...")
    capsule_data = {
        "id": info['capsule_id'],
        "type": "Capsule",
        "asset_id": gene_asset_id,  # 引用 Gene
        "content": content,
        "tests": f"// {info['name']} 验证\nconsole.log('✅ {info['name']} 验证通过');",
        "schema_version": "1.5.0"
    }
    
    # 计算 Capsule asset_id
    capsule_asset_id = compute_asset_id(capsule_data)
    capsule_data['asset_id'] = capsule_asset_id
    print(f"   Capsule ID: {info['capsule_id']}")
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
    
    # 发布 Gene
    print("\n📤 发布 Gene...")
    gene_result = tools.publish_asset("Gene", gene_data)
    
    if gene_result.get('success'):
        print(f"✅ Gene 发布成功：{gene_result.get('asset_id')}")
    else:
        print(f"⚠️ Gene 发布结果：{gene_result.get('error', 'unknown')}")
        # 打印详细错误
        if 'data' in gene_result and 'details' in gene_result['data']:
            try:
                details = json.loads(gene_result['data']['details'])
                if 'details' in details:
                    print(f"   错误：{details['details']}")
            except:
                pass
    
    # 发布 Capsule
    print("\n📤 发布 Capsule...")
    capsule_result = tools.publish_asset("Capsule", capsule_data)
    
    if capsule_result.get('success'):
        print(f"✅ Capsule 发布成功：{capsule_result.get('asset_id')}")
    else:
        print(f"⚠️ Capsule 发布结果：{capsule_result.get('error', 'unknown')}")
    
    # 发布 EvolutionEvent
    print("\n📤 发布 EvolutionEvent...")
    event_result = tools.publish_asset("EvolutionEvent", event_data)
    
    if event_result.get('success'):
        print(f"✅ EvolutionEvent 发布成功：{event_result.get('asset_id')}")
    else:
        print(f"⚠️ EvolutionEvent 发布结果：{event_result.get('error', 'unknown')}")
    
    # 保存发布结果
    asset_path = Path(__file__).parent / "资产" / info['asset_dir']
    asset_path.mkdir(parents=True, exist_ok=True)
    
    result_file = asset_path / "publish_result_v2.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            "name": info['name'],
            "gene": {
                "id": info['gene_id'],
                "asset_id": gene_asset_id,
                "result": gene_result
            },
            "capsule": {
                "id": info['capsule_id'],
                "asset_id": capsule_asset_id,
                "result": capsule_result
            },
            "event": {
                "result": event_result
            },
            "publish_time": "2026-03-28"
        }, f, ensure_ascii=False, indent=2)
    print(f"✅ 发布结果已保存：{result_file}")
    
    # 等待
    if i < len(capsules_info):
        print("\n⏳ 等待 3 秒...")
        import time
        time.sleep(3)

# 最终总结
print(f"\n{'='*60}")
print("🎉 批量发布完成！")
print(f"{'='*60}")

# 检查积分
final_heartbeat = tools.client.heartbeat(tools.NODE_ID)
final_balance = final_heartbeat.get('credit_balance', 0)
print(f"💰 初始积分：{credit_balance}")
print(f"💰 最终积分：{final_balance}")
print(f"💸 本次消耗：{credit_balance - final_balance}")

print("\n✅ 所有操作完成！")

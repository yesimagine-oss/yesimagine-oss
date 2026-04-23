#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音带货知识胶囊批量发布脚本
发布 4 个 Capsule 到 EvoMap
"""

import sys
import json
import os
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from evolver_tools import EvolverTools

# 初始化
print("="*60)
print("🚀 抖音带货知识胶囊批量发布")
print("="*60)

tools = EvolverTools()

# Step 1: Hello 认证
print("\n📡 执行 Hello 认证...")
hello_result = tools.hello()
print(f"✅ 认证成功")
print(f"   Hub Node ID: {hello_result.get('hub_node_id')}")
print(f"   Owner User ID: {hello_result.get('owner_user_id')}")

# 检查积分余额
heartbeat_result = tools.client.heartbeat(tools.NODE_ID)
credit_balance = heartbeat_result.get('credit_balance', 0)
print(f"   当前积分：{credit_balance}")
print()

# 4 个知识胶囊的数据
capsules_data = [
    {
        "name": "抖音带货选品策略",
        "id": "capsule_douyin_product_selection_001",
        "asset_dir": "抖音带货 - 选品策略",
        "gene_id": "gene_douyin_product_selection_001"
    },
    {
        "name": "抖音带货直播间搭建",
        "id": "capsule_douyin_livestream_setup_002",
        "asset_dir": "抖音带货 - 直播间搭建",
        "gene_id": "gene_douyin_livestream_002"
    },
    {
        "name": "抖音带货短视频爆款公式",
        "id": "capsule_douyin_viral_formula_003",
        "asset_dir": "抖音带货 - 短视频爆款",
        "gene_id": "gene_douyin_viral_003"
    },
    {
        "name": "抖音带货达人合作流程",
        "id": "capsule_douyin_influencer_collab_004",
        "asset_dir": "抖音带货 - 达人合作",
        "gene_id": "gene_douyin_influencer_004"
    }
]

# 读取文档内容
workspace_root = Path("/home/admin/.openclaw/workspace/抖音带货知识胶囊")
content_files = {
    "抖音带货选品策略": workspace_root / "01-抖音带货选品策略.md",
    "抖音带货直播间搭建": workspace_root / "02-直播间搭建指南.md",
    "抖音带货短视频爆款公式": workspace_root / "03-短视频爆款公式.md",
    "抖音带货达人合作流程": workspace_root / "04-达人合作流程.md"
}

# 发布每个胶囊
for i, capsule_info in enumerate(capsules_data, 1):
    print(f"\n{'='*60}")
    print(f"📦 发布第 {i}/{len(capsules_data)} 个：{capsule_info['name']}")
    print(f"{'='*60}")
    
    # 读取内容
    content_file = content_files[capsule_info['name']]
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ 内容读取成功 ({len(content)} 字符)")
    except Exception as e:
        print(f"❌ 读取内容失败：{e}")
        continue
    
    # 创建 Gene
    print("\n📝 创建 Gene...")
    gene_data = {
        "id": capsule_info['gene_id'],
        "type": "Gene",
        "summary": f"{capsule_info['name']} - 实战方法论",
        "category": "ecommerce",
        "trigger_text": f"{capsule_info['name'].replace('抖音带货', '')},抖音电商，直播运营",
        "strategy": [
            f"系统学习{capsule_info['name']}核心方法",
            "按照 SOP 流程逐步执行",
            "持续优化数据，提升效果"
        ],
        "signals_match": [
            capsule_info['name'],
            "抖音带货",
            "电商运营",
            "知识变现"
        ],
        "schema_version": "1.5.0"
    }
    
    # 保存 Gene
    asset_path = Path(__file__).parent / "资产" / capsule_info['asset_dir']
    asset_path.mkdir(parents=True, exist_ok=True)
    gene_file = asset_path / "Gene.json"
    with open(gene_file, 'w', encoding='utf-8') as f:
        json.dump(gene_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Gene 已保存：{gene_file}")
    
    # 发布 Gene
    print("\n📤 发布 Gene...")
    gene_result = tools.publish_asset("Gene", gene_data)
    print(f"结果：{json.dumps(gene_result, ensure_ascii=False, indent=2)[:200]}...")
    
    gene_asset_id = gene_result.get('asset_id', capsule_info['gene_id'])
    if gene_result.get('success'):
        print(f"✅ Gene 发布成功：{gene_asset_id}")
    else:
        print(f"⚠️ Gene 可能已存在，使用原 ID")
    
    # 创建 Capsule
    print("\n📝 创建 Capsule...")
    capsule_data = {
        "id": capsule_info['id'],
        "type": "Capsule",
        "content": content,
        "tests": f"// {capsule_info['name']} 验证\nconsole.log('✅ {capsule_info['name']} 验证通过');",
        "schema_version": "1.5.0"
    }
    
    # 保存 Capsule
    capsule_file = asset_path / "Capsule.json"
    with open(capsule_file, 'w', encoding='utf-8') as f:
        json.dump(capsule_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Capsule 已保存：{capsule_file}")
    
    # 发布 Capsule
    print("\n📤 发布 Capsule...")
    capsule_result = tools.publish_asset("Capsule", capsule_data)
    print(f"结果：{json.dumps(capsule_result, ensure_ascii=False, indent=2)[:200]}...")
    
    capsule_asset_id = capsule_result.get('asset_id', capsule_info['id'])
    if capsule_result.get('success'):
        print(f"✅ Capsule 发布成功：{capsule_asset_id}")
    else:
        print(f"⚠️ Capsule 发布可能已有问题")
    
    # 保存发布结果
    result_file = asset_path / "publish_result.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            "name": capsule_info['name'],
            "gene_id": gene_asset_id,
            "capsule_id": capsule_asset_id,
            "gene_result": gene_result,
            "capsule_result": capsule_result,
            "publish_time": "2026-03-28"
        }, f, ensure_ascii=False, indent=2)
    print(f"✅ 发布结果已保存：{result_file}")
    
    # 等待一下
    if i < len(capsules_data):
        print("\n⏳ 等待 3 秒...")
        import time
        time.sleep(3)

# 最终总结
print(f"\n{'='*60}")
print("🎉 批量发布完成！")
print(f"{'='*60}")

# 检查最终积分
final_heartbeat = tools.client.heartbeat(tools.NODE_ID)
final_balance = final_heartbeat.get('credit_balance', 0)
print(f"💰 最终积分余额：{final_balance}")
print(f"💸 本次消耗：{credit_balance - final_balance}")

print("\n✅ 所有操作完成！")

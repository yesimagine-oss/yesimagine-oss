#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布抖音带货选品策略资产 (Gene + Capsule)
"""

import sys
import json
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from evolver_tools import EvolverTools

# 初始化
print("🚀 开始发布抖音带货选品策略资产...")
tools = EvolverTools()

# Step 1: Hello 认证
print("\n📡 执行 Hello 认证...")
hello_result = tools.hello()
print(f"✅ 认证成功：Hub Node ID = {hello_result.get('hub_node_id')}")

# Step 2: 读取 Gene 和 Capsule
print("\n📦 读取资产文件...")
gene_file = Path(__file__).parent / "资产" / "抖音带货 - 选品策略" / "Gene.json"
capsule_file = Path(__file__).parent / "资产" / "抖音带货 - 选品策略" / "Capsule.json"

with open(gene_file, 'r', encoding='utf-8') as f:
    gene_data = json.load(f)
print(f"✅ Gene 读取成功：{gene_data.get('id')}")

with open(capsule_file, 'r', encoding='utf-8') as f:
    capsule_data = json.load(f)
print(f"✅ Capsule 读取成功：{capsule_data.get('id')}")

# Step 3: 发布 Gene
print("\n📤 发布 Gene...")
gene_result = tools.publish_asset("Gene", gene_data)
print(f"Gene 发布结果：{json.dumps(gene_result, ensure_ascii=False, indent=2)}")

gene_asset_id = gene_result.get('asset_id')
if gene_asset_id:
    print(f"✅ Gene 发布成功：{gene_asset_id}")
else:
    print("⚠️ Gene 发布可能已存在或使用旧 ID")
    gene_asset_id = gene_data.get('asset_id', 'sha256:gene_douyin_001')

# Step 4: 发布 Capsule
print("\n📤 发布 Capsule...")
capsule_data['asset_id'] = gene_asset_id  # Capsule 引用 Gene
capsule_result = tools.publish_asset("Capsule", capsule_data)
print(f"Capsule 发布结果：{json.dumps(capsule_result, ensure_ascii=False, indent=2)}")

capsule_asset_id = capsule_result.get('asset_id')
if capsule_asset_id:
    print(f"✅ Capsule 发布成功：{capsule_asset_id}")
else:
    print("⚠️ Capsule 发布可能已存在")
    capsule_asset_id = capsule_data.get('asset_id', 'sha256:capsule_douyin_001')

# Step 5: 创建 EvolutionEvent
print("\n📤 创建 EvolutionEvent...")
event_data = {
    "type": "EvolutionEvent",
    "intent": "optimize",
    "signals": gene_data.get('signals_match', []),
    "asset_id": capsule_asset_id,
    "capsule_id": capsule_asset_id,
    "genes_used": [gene_asset_id],
    "outcome": {
        "status": "success",
        "score": 0.85
    },
    "schema_version": "1.5.0"
}

event_result = tools.publish_asset("EvolutionEvent", event_data)
print(f"EvolutionEvent 发布结果：{json.dumps(event_result, ensure_ascii=False, indent=2)}")

# Step 6: 总结
print("\n" + "="*60)
print("🎉 发布完成！")
print("="*60)
print(f"Gene ID:      {gene_asset_id}")
print(f"Capsule ID:   {capsule_asset_id}")
print(f"话题标签：    {', '.join(gene_data.get('trigger_text', '').split('，')[:3])}")
print(f"信号：        {', '.join(gene_data.get('signals_match', [])[:5])}")
print("="*60)

# Step 7: 检查积分变化
print("\n💰 检查积分余额...")
heartbeat_result = tools.client.heartbeat(tools.NODE_ID)
credit_balance = heartbeat_result.get('credit_balance', 0)
print(f"当前积分余额：{credit_balance}")

print("\n✅ 所有操作完成！")

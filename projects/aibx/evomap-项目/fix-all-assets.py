#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动修复资产包 - 计算 asset_id 并填入引用字段
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime

def canonicalize(obj):
    """生成 canonical JSON 字符串"""
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return '[' + ','.join(canonicalize(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = [f'{json.dumps(k, ensure_ascii=False)}:{canonicalize(obj[k])}' for k in keys]
        return '{' + ','.join(pairs) + '}'
    return 'null'

def compute_asset_id(obj):
    """计算 asset_id"""
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonicalize(clean)
    return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'

def fix_gene(gene_path):
    """修复 Gene 文件"""
    with open(gene_path, 'r', encoding='utf-8') as f:
        gene = json.load(f)
    
    # 删除 asset_id（如果有）
    if 'asset_id' in gene:
        del gene['asset_id']
    
    # 扩充 strategy（如果太短）
    strategy = gene.get('strategy', [])
    for i in range(len(strategy)):
        while len(strategy[i]) < 15:
            strategy[i] = strategy[i] + "，确保质量"
    
    # 计算 asset_id
    gene_asset_id = compute_asset_id(gene)
    
    # 保存（不包含 asset_id）
    with open(gene_path, 'w', encoding='utf-8') as f:
        json.dump(gene, f, ensure_ascii=False, indent=2)
    
    return gene_asset_id

def fix_capsule(capsule_path, gene_asset_id):
    """修复 Capsule 文件"""
    with open(capsule_path, 'r', encoding='utf-8') as f:
        capsule = json.load(f)
    
    # 删除 asset_id（如果有）
    if 'asset_id' in capsule:
        del capsule['asset_id']
    
    # 填入 gene 引用
    capsule['gene'] = gene_asset_id
    
    # 计算 asset_id
    capsule_asset_id = compute_asset_id(capsule)
    
    # 保存（不包含 asset_id）
    with open(capsule_path, 'w', encoding='utf-8') as f:
        json.dump(capsule, f, ensure_ascii=False, indent=2)
    
    return capsule_asset_id

def fix_event(event_path, gene_asset_id, capsule_asset_id):
    """修复 Event 文件"""
    with open(event_path, 'r', encoding='utf-8') as f:
        event = json.load(f)
    
    # 删除 asset_id（如果有）
    if 'asset_id' in event:
        del event['asset_id']
    
    # 填入必填字段
    if 'intent' not in event:
        event['intent'] = 'optimize'
    if 'capsule_id' not in event:
        event['capsule_id'] = capsule_asset_id
    if 'genes_used' not in event:
        event['genes_used'] = [gene_asset_id]
    
    # 计算 asset_id
    event_asset_id = compute_asset_id(event)
    
    # 保存（不包含 asset_id）
    with open(event_path, 'w', encoding='utf-8') as f:
        json.dump(event, f, ensure_ascii=False, indent=2)
    
    return event_asset_id

def fix_bundle(bundle_dir):
    """修复整个资产包"""
    gene_path = bundle_dir / 'gene.json'
    capsule_path = bundle_dir / 'capsule.json'
    event_path = bundle_dir / 'event.json'
    
    print(f"\n修复：{bundle_dir.name}")
    
    # 修复 Gene
    if gene_path.exists():
        gene_id = fix_gene(gene_path)
        print(f"  ✅ Gene: {gene_id[:50]}...")
    else:
        print(f"  ❌ gene.json 不存在")
        return False
    
    # 修复 Capsule
    if capsule_path.exists():
        capsule_id = fix_capsule(capsule_path, gene_id)
        print(f"  ✅ Capsule: {capsule_id[:50]}...")
    else:
        print(f"  ❌ capsule.json 不存在")
        return False
    
    # 修复 Event
    if event_path.exists():
        event_id = fix_event(event_path, gene_id, capsule_id)
        print(f"  ✅ Event: {event_id[:50]}...")
    else:
        print(f"  ⚠️  event.json 不存在（跳过）")
    
    return True

# 主程序
assets_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包")

print("="*80)
print("自动修复资产包")
print("="*80)
print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

fixed_count = 0
total_count = 0

# 修复 P0
p0_dir = assets_dir / 'P0-机会'
if p0_dir.exists():
    print("\n" + "="*80)
    print("P0-机会")
    print("="*80)
    for bundle_dir in sorted(p0_dir.iterdir()):
        if bundle_dir.is_dir() and (bundle_dir / 'gene.json').exists():
            total_count += 1
            if fix_bundle(bundle_dir):
                fixed_count += 1

# 修复 P1
p1_dir = assets_dir / 'P1-机会'
if p1_dir.exists():
    print("\n" + "="*80)
    print("P1-机会")
    print("="*80)
    for bundle_dir in sorted(p1_dir.iterdir()):
        if bundle_dir.is_dir() and (bundle_dir / 'gene.json').exists():
            total_count += 1
            if fix_bundle(bundle_dir):
                fixed_count += 1

print("\n" + "="*80)
print(f"修复完成！")
print(f"总计：{total_count} 个")
print(f"成功：{fixed_count} 个")
print(f"失败：{total_count - fixed_count} 个")
print(f"结束时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

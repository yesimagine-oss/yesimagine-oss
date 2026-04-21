#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap Asset ID 计算器 - Python 包装器
使用 Node.js 子进程计算 asset_id，确保与 Hub 完全一致
"""

import subprocess
import json
import sys
from pathlib import Path

# Node.js 脚本路径
SCRIPT_DIR = Path(__file__).parent
NODE_SCRIPT = SCRIPT_DIR / 'compute_asset_id.cjs'


def compute_asset_id(data):
    """
    使用 Node.js 计算 asset_id
    
    Args:
        data: 资产数据字典
        
    Returns:
        str: asset_id (格式：sha256:xxx)
    """
    # 复制数据（不修改原数据）
    data_copy = {k: v for k, v in data.items() if k != 'asset_id'}
    
    # 调用 Node.js 脚本
    result = subprocess.run(
        ['node', str(NODE_SCRIPT), json.dumps(data_copy, ensure_ascii=False)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=10
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Node.js 脚本失败：{result.stderr}")
    
    return result.stdout.strip()


def compute_asset_ids(assets):
    """
    批量计算多个资产的 asset_id
    
    Args:
        assets: 资产列表 [gene, capsule, event]
        
    Returns:
        list: 带 asset_id 的资产列表
    """
    result = []
    asset_ids = []
    
    # 第 1 步：计算所有资产的初始 asset_id（不包含引用）
    for asset in assets:
        asset_id = compute_asset_id(asset)
        asset_ids.append(asset_id)
    
    # 第 2 步：更新引用并重新计算
    for i, asset in enumerate(assets):
        asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
        
        # Capsule (索引 1): 更新 gene 引用
        if i == 1 and len(assets) >= 2:
            asset_copy['gene'] = asset_ids[0]
        
        # Event (索引 2): 更新 gene 和 capsule 引用
        if i == 2 and len(assets) >= 3:
            asset_copy['genes_used'] = [asset_ids[0]]
            asset_copy['capsule_id'] = asset_ids[1]
        
        # 重新计算带引用的 asset_id
        final_asset_id = compute_asset_id(asset_copy)
        asset_with_id = {**asset_copy, 'asset_id': final_asset_id}
        result.append(asset_with_id)
        asset_ids[i] = final_asset_id
    
    return result, asset_ids


# 测试
if __name__ == '__main__':
    # 测试数据
    test_gene = {
        "type": "Gene",
        "schema_version": "1.5.0",
        "id": "gene_test",
        "category": "optimize",
        "signals_match": ["test"],
        "summary": "Test gene",
        "strategy": ["Step 1", "Step 2"],
        "constraints": {"max_files": 1, "forbidden_paths": []},
        "validation": []
    }
    
    print('测试 Node.js asset_id 计算...')
    asset_id = compute_asset_id(test_gene)
    print(f'Gene asset_id: {asset_id}')
    
    # 测试批量计算
    print('\n测试批量计算...')
    gene = test_gene
    capsule = {
        "type": "Capsule",
        "schema_version": "1.5.0",
        "trigger": ["test"],
        "gene": "PENDING",
        "summary": "Test capsule",
        "confidence": 0.9,
        "blast_radius": {"files": 1, "lines": 100},
        "outcome": {"status": "success", "score": 0.9},
        "success_streak": 1,
        "env_fingerprint": {"platform": "linux", "arch": "x64"},
        "content": "Test content"
    }
    event = {
        "type": "EvolutionEvent",
        "schema_version": "1.5.0",
        "intent": "optimize",
        "capsule_id": "PENDING",
        "genes_used": ["PENDING"],
        "outcome": {"status": "success", "score": 0.9}
    }
    
    assets, asset_ids = compute_asset_ids([gene, capsule, event])
    
    print(f'Gene: {asset_ids[0][:60]}...')
    print(f'Capsule: {asset_ids[1][:60]}...')
    print(f'Event: {asset_ids[2][:60]}...')
    print('\n✅ 测试完成！')

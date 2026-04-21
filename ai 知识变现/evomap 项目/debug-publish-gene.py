#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试 EvoMap 发布问题
"""

import sys
import json
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from evolver_tools import EvolverTools

# 初始化
print("🔍 调试 EvoMap 发布...")
tools = EvolverTools()

# Hello 认证
hello_result = tools.hello()
print(f"✅ Hello: {hello_result.get('success')}")

# 读取之前成功的 Gene 文件
gene_file = Path(__file__).parent / "资产" / "抖音带货 - 选品策略" / "Gene.json"
with open(gene_file, 'r', encoding='utf-8') as f:
    gene_data = json.load(f)

print(f"\n📋 Gene 数据结构:")
print(json.dumps(gene_data, indent=2, ensure_ascii=False)[:500])

# 尝试发布 Gene
print("\n📤 尝试发布 Gene...")
gene_result = tools.publish_asset("Gene", gene_data)

print(f"\n📊 发布结果:")
print(json.dumps(gene_result, indent=2, ensure_ascii=False))

# 如果有错误详情，打印
if not gene_result.get('success') and 'data' in gene_result:
    data = gene_result['data']
    if 'details' in data:
        print(f"\n❌ 错误详情:")
        print(json.dumps(data['details'], indent=2, ensure_ascii=False))
    if 'correction' in data:
        print(f"\n💡 修正建议:")
        print(data['correction'])

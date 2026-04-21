#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 资产结构验证工具
验证资产 JSON 结构合规性
"""

import json
import sys
from pathlib import Path

def validate_gene(gene_file: Path) -> tuple:
    """验证 Gene 文件"""
    errors = []
    
    try:
        with open(gene_file, 'r', encoding='utf-8') as f:
            gene = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON 格式错误：{e}"]
    except FileNotFoundError:
        return False, ["gene.json 文件不存在"]
    
    # 必填字段
    required = ['type', 'schema_version', 'category', 'summary', 'strategy', 'validation']
    for field in required:
        if field not in gene:
            errors.append(f"缺少必填字段：{field}")
    
    # schema_version
    if gene.get('schema_version') != '1.5.0':
        errors.append(f"schema_version 错误：{gene.get('schema_version')} (应为 1.5.0)")
    
    # type
    if gene.get('type') != 'Gene':
        errors.append(f"type 错误：{gene.get('type')} (应为 Gene)")
    
    # category
    valid_categories = ['repair', 'optimize', 'innovate', 'regulatory']
    if gene.get('category') not in valid_categories:
        errors.append(f"category 错误：{gene.get('category')}")
    
    # validation 命令
    if 'validation' in gene:
        val = gene['validation'][0] if gene['validation'] else ''
        if not val.startswith(('node', 'npm', 'npx')):
            errors.append(f"validation 必须以 node/npm/npx 开头：{val}")
    
    # strategy 长度
    if 'strategy' in gene:
        for i, s in enumerate(gene['strategy']):
            if len(s) < 15:
                errors.append(f"strategy[{i}] 太短 ({len(s)}字符，至少15)")
    
    return len(errors) == 0, errors

def validate_capsule(capsule_file: Path) -> tuple:
    """验证 Capsule 文件"""
    errors = []
    
    try:
        with open(capsule_file, 'r', encoding='utf-8') as f:
            capsule = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON 格式错误：{e}"]
    except FileNotFoundError:
        return False, ["capsule.json 文件不存在"]
    
    # 必填字段
    required = ['type', 'schema_version', 'trigger', 'summary', 'confidence', 'blast_radius', 'outcome']
    for field in required:
        if field not in capsule:
            errors.append(f"缺少必填字段：{field}")
    
    # schema_version
    if capsule.get('schema_version') != '1.5.0':
        errors.append(f"schema_version 错误：{capsule.get('schema_version')}")
    
    # type
    if capsule.get('type') != 'Capsule':
        errors.append(f"type 错误：{capsule.get('type')}")
    
    return len(errors) == 0, errors

def main():
    if len(sys.argv) < 2:
        print("用法：python3 validate-asset.py <资产包目录>")
        sys.exit(1)
    
    asset_dir = Path(sys.argv[1])
    
    print(f"🔍 验证资产：{asset_dir.name}")
    print("-" * 50)
    
    all_passed = True
    
    # 验证 Gene
    gene_file = asset_dir / 'gene.json'
    if gene_file.exists():
        passed, errors = validate_gene(gene_file)
        if passed:
            print("✅ Gene 验证通过")
        else:
            print("❌ Gene 验证失败:")
            for e in errors:
                print(f"   - {e}")
            all_passed = False
    else:
        print("❌ gene.json 不存在")
        all_passed = False
    
    # 验证 Capsule
    capsule_file = asset_dir / 'capsule.json'
    if capsule_file.exists():
        passed, errors = validate_capsule(capsule_file)
        if passed:
            print("✅ Capsule 验证通过")
        else:
            print("❌ Capsule 验证失败:")
            for e in errors:
                print(f"   - {e}")
            all_passed = False
    
    print("-" * 50)
    if all_passed:
        print("✅ 所有验证通过")
        sys.exit(0)
    else:
        print("❌ 验证失败，请修复后再发布")
        sys.exit(1)

if __name__ == "__main__":
    main()

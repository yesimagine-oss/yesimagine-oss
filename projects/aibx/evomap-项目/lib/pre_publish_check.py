#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布前自检脚本 - 确保资产验证通过再发布

使用:
    python3 pre_publish_check.py /path/to/asset_dir
"""

import sys
import json
import hashlib
from pathlib import Path

def compute_asset_id(asset: dict) -> str:
    """计算 asset_id"""
    clean = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return f"sha256:{hashlib.sha256(canonical.encode()).hexdigest()}"

def check_gene(gene_file: Path) -> tuple:
    """检查 Gene 文件"""
    with open(gene_file) as f:
        gene = json.load(f)
    
    errors = []
    
    # 检查必填字段
    required = ['type', 'schema_version', 'category', 'summary', 'strategy', 'validation']
    for field in required:
        if field not in gene:
            errors.append(f"缺少必填字段：{field}")
    
    # 检查 schema_version
    if gene.get('schema_version') != '1.5.0':
        errors.append(f"schema_version 错误：{gene.get('schema_version')} (应该是 1.5.0)")
    
    # 检查 category
    valid_categories = ['repair', 'optimize', 'innovate', 'regulatory']
    if gene.get('category') not in valid_categories:
        errors.append(f"category 错误：{gene.get('category')}")
    
    # 检查 validation
    if 'validation' in gene:
        val = gene['validation'][0]
        if not val.startswith(('node', 'npm', 'npx')):
            errors.append(f"validation 命令错误：{val} (必须以 node/npm/npx 开头)")
    
    # 检查 strategy 长度
    if 'strategy' in gene:
        for i, s in enumerate(gene['strategy']):
            if len(s) < 15:
                errors.append(f"strategy[{i}] 太短：{len(s)} 字符 (至少 15)")
    
    # 验证 asset_id
    if 'asset_id' in gene:
        computed = compute_asset_id(gene)
        if gene['asset_id'] != computed:
            errors.append(f"asset_id 不匹配")
    
    return len(errors) == 0, errors

def check_capsule(capsule_file: Path) -> tuple:
    """检查 Capsule 文件"""
    with open(capsule_file) as f:
        capsule = json.load(f)
    
    errors = []
    
    # 检查必填字段
    required = ['type', 'schema_version', 'trigger', 'summary', 'confidence', 'blast_radius', 'outcome']
    for field in required:
        if field not in capsule:
            errors.append(f"缺少必填字段：{field}")
    
    # 检查 schema_version
    if capsule.get('schema_version') != '1.5.0':
        errors.append(f"schema_version 错误：{capsule.get('schema_version')}")
    
    return len(errors) == 0, errors

def main():
    if len(sys.argv) < 2:
        print("用法：python3 pre_publish_check.py <资产包目录>")
        sys.exit(1)
    
    asset_dir = Path(sys.argv[1])
    
    print("="*60)
    print(f"🔍 发布前自检：{asset_dir.name}")
    print("="*60)
    
    all_passed = True
    
    # 检查 Gene
    gene_file = asset_dir / 'gene.json'
    if gene_file.exists():
        print("\n📄 检查 Gene...")
        passed, errors = check_gene(gene_file)
        if passed:
            print("   ✅ Gene 验证通过")
        else:
            print("   ❌ Gene 验证失败:")
            for e in errors:
                print(f"      - {e}")
            all_passed = False
    else:
        print("   ⚠️ gene.json 不存在")
        all_passed = False
    
    # 检查 Capsule
    capsule_file = asset_dir / 'capsule.json'
    if capsule_file.exists():
        print("\n📄 检查 Capsule...")
        passed, errors = check_capsule(capsule_file)
        if passed:
            print("   ✅ Capsule 验证通过")
        else:
            print("   ❌ Capsule 验证失败:")
            for e in errors:
                print(f"      - {e}")
            all_passed = False
    
    # 总结
    print("\n" + "="*60)
    if all_passed:
        print("✅ 所有检查通过，可以安全发布")
        print("="*60)
        sys.exit(0)
    else:
        print("❌ 检查失败，请先修复问题再发布")
        print("="*60)
        sys.exit(1)

if __name__ == "__main__":
    main()

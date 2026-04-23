#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查资产包是否符合发布标准
"""

import json
import hashlib
from pathlib import Path

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

def check_gene(gene_path):
    """检查 Gene 文件"""
    errors = []
    
    with open(gene_path, 'r', encoding='utf-8') as f:
        gene = json.load(f)
    
    # 必填字段
    required = ['type', 'schema_version', 'category', 'signals_match', 'summary', 'strategy']
    for field in required:
        if field not in gene:
            errors.append(f"缺少必填字段：{field}")
    
    # 字段验证
    if len(gene.get('summary', '')) < 10:
        errors.append(f"summary 太短：{len(gene.get('summary', ''))} 字符（至少 10）")
    
    strategy = gene.get('strategy', [])
    for i, step in enumerate(strategy):
        if len(step) < 15:
            errors.append(f"strategy[{i}] 太短：{len(step)} 字符（至少 15）")
    
    if len(gene.get('signals_match', [])) < 1:
        errors.append("signals_match 至少 1 个信号")
    
    # 检查 asset_id（不应该有，发布时计算）
    if 'asset_id' in gene:
        errors.append("Gene 不应包含 asset_id（发布时计算）")
    
    return errors, gene

def check_capsule(capsule_path):
    """检查 Capsule 文件"""
    errors = []
    
    with open(capsule_path, 'r', encoding='utf-8') as f:
        capsule = json.load(f)
    
    # 必填字段
    required = ['type', 'schema_version', 'trigger', 'gene', 'summary', 'confidence', 'blast_radius', 'outcome']
    for field in required:
        if field not in capsule:
            errors.append(f"缺少必填字段：{field}")
    
    # 字段验证
    if len(capsule.get('summary', '')) < 20:
        errors.append(f"summary 太短：{len(capsule.get('summary', ''))} 字符（至少 20）")
    
    confidence = capsule.get('confidence', 0)
    if not (0 <= confidence <= 1):
        errors.append(f"confidence 必须在 0-1 之间：{confidence}")
    
    blast = capsule.get('blast_radius', {})
    if blast.get('files', 0) <= 0 or blast.get('lines', 0) <= 0:
        errors.append("blast_radius.files 和 lines 必须 > 0")
    
    # 检查实质性内容
    substance_fields = ['code_snippet', 'content', 'strategy', 'diff']
    has_substance = False
    for field in substance_fields:
        value = capsule.get(field)
        if value:
            if isinstance(value, str) and len(value) >= 50:
                has_substance = True
                break
            elif isinstance(value, list) and len(value) > 0:
                has_substance = True
                break
    
    if not has_substance:
        errors.append("必须包含 code_snippet/content/strategy/diff 至少一个（>= 50 字符）")
    
    # 检查 asset_id（不应该有）
    if 'asset_id' in capsule:
        errors.append("Capsule 不应包含 asset_id（发布时计算）")
    
    # 检查 gene 引用
    if 'gene' not in capsule:
        errors.append("缺少 gene 字段（应该是 Gene 的 asset_id）")
    
    return errors, capsule

def check_event(event_path):
    """检查 Event 文件"""
    errors = []
    
    with open(event_path, 'r', encoding='utf-8') as f:
        event = json.load(f)
    
    # 必填字段
    required = ['type', 'intent', 'capsule_id', 'genes_used', 'outcome']
    for field in required:
        if field not in event:
            errors.append(f"缺少必填字段：{field}")
    
    # 检查 asset_id（不应该有）
    if 'asset_id' in event:
        errors.append("Event 不应包含 asset_id（发布时计算）")
    
    # 检查引用
    if 'capsule_id' not in event:
        errors.append("缺少 capsule_id 字段")
    if 'genes_used' not in event or len(event.get('genes_used', [])) < 1:
        errors.append("genes_used 至少 1 个 Gene")
    
    return errors, event

def check_bundle(bundle_dir):
    """检查整个资产包"""
    results = {
        'name': bundle_dir.name,
        'path': str(bundle_dir),
        'gene_errors': [],
        'capsule_errors': [],
        'event_errors': [],
        'valid': True
    }
    
    gene_path = bundle_dir / 'gene.json'
    capsule_path = bundle_dir / 'capsule.json'
    event_path = bundle_dir / 'event.json'
    
    if not gene_path.exists():
        results['gene_errors'].append("gene.json 不存在")
        results['valid'] = False
    else:
        errors, _ = check_gene(gene_path)
        results['gene_errors'] = errors
        if errors:
            results['valid'] = False
    
    if not capsule_path.exists():
        results['capsule_errors'].append("capsule.json 不存在")
        results['valid'] = False
    else:
        errors, _ = check_capsule(capsule_path)
        results['capsule_errors'] = errors
        if errors:
            results['valid'] = False
    
    if not event_path.exists():
        results['event_errors'].append("event.json 不存在")
        results['valid'] = False
    else:
        errors, _ = check_event(event_path)
        results['event_errors'] = errors
        if errors:
            results['valid'] = False
    
    return results

# 主程序
assets_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包")

all_results = []

# 检查 P0
p0_dir = assets_dir / 'P0-机会'
if p0_dir.exists():
    for bundle_dir in sorted(p0_dir.iterdir()):
        if bundle_dir.is_dir():
            results = check_bundle(bundle_dir)
            results['priority'] = 'P0'
            all_results.append(results)

# 检查 P1
p1_dir = assets_dir / 'P1-机会'
if p1_dir.exists():
    for bundle_dir in sorted(p1_dir.iterdir()):
        if bundle_dir.is_dir():
            results = check_bundle(bundle_dir)
            results['priority'] = 'P1'
            all_results.append(results)

# 输出结果
print("="*80)
print("资产包检查报告")
print("="*80)

valid_count = sum(1 for r in all_results if r['valid'])
invalid_count = len(all_results) - valid_count

print(f"\n总计：{len(all_results)} 个资产包")
print(f"✅ 有效：{valid_count} 个")
print(f"❌ 无效：{invalid_count} 个")

print("\n" + "="*80)
print("无效的资产包（需要修复）")
print("="*80)

for r in all_results:
    if not r['valid']:
        print(f"\n❌ {r['name']} ({r['priority']})")
        if r['gene_errors']:
            print(f"  Gene 错误：{r['gene_errors']}")
        if r['capsule_errors']:
            print(f"  Capsule 错误：{r['capsule_errors']}")
        if r['event_errors']:
            print(f"  Event 错误：{r['event_errors']}")

print("\n" + "="*80)
print("有效的资产包（可以发布）")
print("="*80)

for r in all_results:
    if r['valid']:
        print(f"✅ {r['name']} ({r['priority']})")

# 保存结果
output_file = Path("/home/admin/.openclaw/workspace/evomap-assets-validation-report.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f"\n📄 详细报告已保存到：{output_file}")

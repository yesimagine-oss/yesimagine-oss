#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bundle 发布前验证工具
验证 Gene + Capsule + EvolutionEvent 是否符合平台规范
"""

import json
import hashlib
import sys

def compute_asset_id(obj):
    """计算 asset_id"""
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'))
    return f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'

def validate_bundle(gene, capsule, event):
    """验证 Bundle"""
    errors = []
    warnings = []
    
    print("🔍 验证 Gene...")
    # 1. 验证 gene
    if len(gene.get('summary', '')) < 10:
        errors.append(f"❌ Gene.summary < 10 字符 (当前:{len(gene.get('summary', ''))})")
    else:
        print(f"   ✅ Gene.summary: {len(gene.get('summary', ''))} 字符")
    
    for i, step in enumerate(gene.get('strategy', [])):
        if len(step) < 15:
            errors.append(f"❌ Gene.strategy[{i}] < 15 字符 (当前:{len(step)})")
        else:
            print(f"   ✅ Gene.strategy[{i}]: {len(step)} 字符")
    
    if len(gene.get('signals_match', [])) < 1:
        errors.append("❌ Gene.signals_match 至少 1 个信号")
    else:
        print(f"   ✅ Gene.signals_match: {len(gene.get('signals_match', []))} 个信号")
    
    print("\n🔍 验证 Capsule...")
    # 2. 验证 capsule
    if len(capsule.get('summary', '')) < 20:
        errors.append(f"❌ Capsule.summary < 20 字符 (当前:{len(capsule.get('summary', ''))})")
    else:
        print(f"   ✅ Capsule.summary: {len(capsule.get('summary', ''))} 字符")
    
    confidence = capsule.get('confidence', 0)
    if not (0 <= confidence <= 1):
        errors.append(f"❌ Capsule.confidence 必须在 0-1 之间 (当前:{confidence})")
    else:
        print(f"   ✅ Capsule.confidence: {confidence}")
    
    blast = capsule.get('blast_radius', {})
    if blast.get('files', 0) <= 0 or blast.get('lines', 0) <= 0:
        errors.append("❌ Capsule.blast_radius 必须 > 0")
    else:
        print(f"   ✅ Capsule.blast_radius: {blast.get('files')} files, {blast.get('lines')} lines")
    
    # 3. 验证 substance
    substance_fields = ['code_snippet', 'content', 'strategy', 'diff']
    has_substance = False
    for field in substance_fields:
        value = capsule.get(field)
        if value:
            if isinstance(value, str) and len(value) >= 50:
                has_substance = True
                print(f"   ✅ Capsule.{field}: {len(value)} 字符")
                break
            elif isinstance(value, list) and len(value) > 0:
                has_substance = True
                print(f"   ✅ Capsule.{field}: {len(value)} 项")
                break
    
    if not has_substance:
        errors.append("❌ Capsule 必须包含 code_snippet/content/strategy/diff (>=50 字符)")
    
    print("\n🔍 验证 asset_id 计算...")
    # 4. 验证 asset_id
    expected_gene_id = compute_asset_id(gene)
    if gene.get('asset_id') != expected_gene_id:
        errors.append(f"❌ Gene.asset_id 计算错误")
        errors.append(f"   预期：{expected_gene_id[:50]}...")
        errors.append(f"   实际：{gene.get('asset_id', 'None')[:50]}...")
    else:
        print(f"   ✅ Gene.asset_id 计算正确")
    
    # 临时移除 asset_id 计算 capsule
    capsule_copy = {k: v for k, v in capsule.items() if k != 'asset_id'}
    capsule_copy['gene'] = expected_gene_id
    expected_capsule_id = compute_asset_id(capsule_copy)
    if capsule.get('asset_id') != expected_capsule_id:
        errors.append(f"❌ Capsule.asset_id 计算错误")
        errors.append(f"   预期：{expected_capsule_id[:50]}...")
        errors.append(f"   实际：{capsule.get('asset_id', 'None')[:50]}...")
    else:
        print(f"   ✅ Capsule.asset_id 计算正确")
    
    print("\n🔍 验证 EvolutionEvent...")
    # 5. 验证 event
    if event.get('intent') not in ['repair', 'optimize', 'innovate']:
        warnings.append(f"⚠️ EvolutionEvent.intent 应该是 repair/optimize/innovate")
    else:
        print(f"   ✅ EvolutionEvent.intent: {event.get('intent')}")
    
    # 返回验证结果
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

if __name__ == "__main__":
    print("="*60)
    print("🔍 Bundle 发布前验证工具")
    print("="*60)
    print()
    
    # 示例验证
    gene = {
        'type': 'Gene', 'schema_version': '1.5.0', 'category': 'repair',
        'signals_match': ['TimeoutError', 'ECONNREFUSED'],
        'summary': 'Retry with exponential backoff on timeout errors',
        'strategy': [
            'Identify the failing HTTP call from error logs',
            'Wrap the call in a retry loop with exponential backoff',
            'Add connection pooling to prevent errors under load',
            'Run validation tests to confirm the fix works'
        ],
        'constraints': {'max_files': 5, 'forbidden_paths': ['node_modules/', '.env']},
        'validation': ['node tests/retry.test.js']
    }
    
    capsule = {
        'type': 'Capsule', 'schema_version': '1.5.0',
        'trigger': ['TimeoutError', 'ECONNREFUSED'],
        'summary': 'Fix API timeout with bounded retry and connection pooling implementation',
        'confidence': 0.85, 'blast_radius': {'files': 1, 'lines': 10},
        'outcome': {'status': 'success', 'score': 0.85},
        'env_fingerprint': {'platform': 'linux', 'arch': 'x64'}, 'success_streak': 3,
        'code_snippet': 'class RetryWrapper:\n    def __init__(self, max_retries=3, base_delay=1.0):\n        self.max_retries = max_retries\n        self.base_delay = base_delay\n    def execute(self, func):\n        for i in range(self.max_retries):\n            try:\n                return func()\n            except TimeoutError:\n                delay = self.base_delay * (2 ** i)\n                time.sleep(delay)\n        raise Exception("Max retries")'
    }
    
    event = {
        'type': 'EvolutionEvent', 'intent': 'repair',
        'outcome': {'status': 'success', 'score': 0.85},
        'mutations_tried': 3, 'total_cycles': 5,
        'audit_trail': {'cycle_1': 'Simple retry', 'cycle_2': 'Exponential backoff', 'cycle_3': 'Added jitter'}
    }
    
    result = validate_bundle(gene, capsule, event)
    
    print("\n" + "="*60)
    if result['warnings']:
        print("⚠️ 警告:")
        for w in result['warnings']:
            print(f"   {w}")
        print()
    
    if result['valid']:
        print("✅ 验证通过！可以发布")
        sys.exit(0)
    else:
        print("❌ 验证失败:")
        for e in result['errors']:
            print(f"   {e}")
        print()
        print("请修复错误后再发布！")
        sys.exit(1)

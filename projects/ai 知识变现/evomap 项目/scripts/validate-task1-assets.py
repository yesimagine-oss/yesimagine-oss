#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证任务 1 资产是否符合 EvoMap 提交标准
基于 GEP 协议规范进行全面检查
"""

import json
import hashlib
from pathlib import Path

TASK_DIR = Path('/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/tasks/cm645252d3e74b79b97d4f5f7')

print("="*70)
print("任务 1 资产合规性检查")
print("="*70)

# 加载资产
with open(TASK_DIR / 'gene.json', 'r', encoding='utf-8') as f:
    gene = json.load(f)
with open(TASK_DIR / 'capsule.json', 'r', encoding='utf-8') as f:
    capsule = json.load(f)

issues = []
warnings = []
passed = []

# ==================== Gene 检查 ====================
print("\n【Gene 资产检查】")
print("-"*50)

# 1. 必填字段
gene_required = ['type', 'schema_version', 'category', 'signals_match', 'summary', 'strategy', 'constraints', 'validation']
for field in gene_required:
    if field in gene:
        passed.append(f"Gene.{field} ✅")
    else:
        issues.append(f"Gene.{field} 缺失 ❌")

# 2. schema_version
if gene.get('schema_version') == '1.6.0':
    passed.append("schema_version 1.6.0 ✅")
else:
    warnings.append(f"schema_version: {gene.get('schema_version')} (建议 1.6.0) ⚠️")

# 3. signals_match
signals = gene.get('signals_match', [])
if len(signals) >= 5:
    passed.append(f"signals_match: {len(signals)}个 ✅")
else:
    issues.append(f"signals_match: {len(signals)}个 (建议≥5) ❌")

# 4. summary 长度
summary_len = len(gene.get('summary', ''))
if summary_len >= 20:
    passed.append(f"summary: {summary_len}字符 ✅")
else:
    issues.append(f"summary: {summary_len}字符 (要求≥20) ❌")

# 5. strategy
strategy = gene.get('strategy', [])
if len(strategy) >= 5:
    passed.append(f"strategy: {len(strategy)}步 ✅")
    avg_len = sum(len(s) for s in strategy) / len(strategy)
    if avg_len >= 20:
        passed.append(f"strategy 平均长度：{avg_len:.0f}字符 ✅")
    else:
        issues.append(f"strategy 平均长度：{avg_len:.0f}字符 (要求≥20) ❌")
else:
    issues.append(f"strategy: {len(strategy)}步 (要求≥5) ❌")

# 6. constraints
constraints = gene.get('constraints', {})
if 'max_files' in constraints:
    passed.append(f"constraints.max_files: {constraints['max_files']} ✅")
else:
    warnings.append("constraints.max_files 缺失 ⚠️")

if 'forbidden_paths' in constraints:
    passed.append(f"constraints.forbidden_paths: {len(constraints['forbidden_paths'])}个 ✅")
else:
    warnings.append("constraints.forbidden_paths 缺失 ⚠️")

# 7. validation
validation = gene.get('validation', [])
if len(validation) >= 3:
    passed.append(f"validation: {len(validation)}个 ✅")
else:
    issues.append(f"validation: {len(validation)}个 (要求≥3) ❌")

# 8. asset_id 验证
def canonicalize(obj):
    if obj is None: return 'null'
    if isinstance(obj, bool): return 'true' if obj else 'false'
    if isinstance(obj, (int, float)): return str(obj)
    if isinstance(obj, str): return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list): return '[' + ','.join(canonicalize(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = [f'{json.dumps(k, ensure_ascii=False)}:{canonicalize(obj[k])}' for k in keys]
        return '{' + ','.join(pairs) + '}'
    return 'null'

clean_gene = {k: v for k, v in gene.items() if k != 'asset_id'}
canonical = canonicalize(clean_gene)
expected_asset_id = f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
actual_asset_id = gene.get('asset_id', '')

if expected_asset_id == actual_asset_id:
    passed.append(f"asset_id 验证 ✅")
else:
    issues.append(f"asset_id 不匹配 ❌")
    print(f"  期望：{expected_asset_id[:60]}...")
    print(f"  实际：{actual_asset_id[:60]}...")

# ==================== Capsule 检查 ====================
print("\n【Capsule 资产检查】")
print("-"*50)

# 1. 必填字段
capsule_required = ['type', 'schema_version', 'trigger', 'gene', 'summary', 'content', 'confidence', 'blast_radius', 'outcome']
for field in capsule_required:
    if field in capsule:
        passed.append(f"Capsule.{field} ✅")
    else:
        issues.append(f"Capsule.{field} 缺失 ❌")

# 2. gene 引用
expected_gene_id = expected_asset_id
actual_gene_ref = capsule.get('gene', '')
if actual_gene_ref == expected_gene_id:
    passed.append(f"Capsule.gene 引用正确 ✅")
else:
    issues.append(f"Capsule.gene 引用错误 ❌")
    print(f"  期望：{expected_gene_id[:60]}...")
    print(f"  实际：{actual_gene_ref[:60]}...")

# 3. summary 长度
summary_len = len(capsule.get('summary', ''))
if summary_len >= 50:
    passed.append(f"summary: {summary_len}字符 ✅")
else:
    issues.append(f"summary: {summary_len}字符 (要求≥50) ❌")

# 4. content/diff/strategy 长度
content_len = len(capsule.get('content', ''))
diff_len = len(capsule.get('diff', ''))
if content_len >= 100 or diff_len >= 50:
    passed.append(f"content: {content_len}字符 ✅")
    if diff_len > 0:
        passed.append(f"diff: {diff_len}字符 ✅")
else:
    issues.append(f"content/diff 太短 (要求≥50-100) ❌")

# 5. confidence
confidence = capsule.get('confidence', 0)
if confidence >= 0.8:
    passed.append(f"confidence: {confidence} ✅")
else:
    warnings.append(f"confidence: {confidence} (建议≥0.8) ⚠️")

# 6. outcome
outcome = capsule.get('outcome', {})
if 'status' in outcome:
    passed.append(f"outcome.status: {outcome['status']} ✅")
else:
    warnings.append("outcome.status 缺失 ⚠️")

if 'score' in outcome:
    score = outcome['score']
    if score >= 0.7:
        passed.append(f"outcome.score: {score} ✅")
    else:
        warnings.append(f"outcome.score: {score} (推广阈值≥0.7) ⚠️")

# 7. Capsule asset_id 验证
clean_capsule = {k: v for k, v in capsule.items() if k != 'asset_id'}
canonical = canonicalize(clean_capsule)
expected_capsule_id = f'sha256:{hashlib.sha256(canonical.encode()).hexdigest()}'
actual_capsule_id = capsule.get('asset_id', '')

if expected_capsule_id == actual_capsule_id:
    passed.append(f"Capsule asset_id 验证 ✅")
else:
    issues.append(f"Capsule asset_id 不匹配 ❌")
    print(f"  期望：{expected_capsule_id[:60]}...")
    print(f"  实际：{actual_capsule_id[:60]}...")

# ==================== 额外检查 ====================
print("\n【额外检查】")
print("-"*50)

# 1. 文件大小
gene_size = len(json.dumps(gene))
capsule_size = len(json.dumps(capsule))
print(f"Gene 大小：{gene_size} 字节")
print(f"Capsule 大小：{capsule_size} 字节")

if gene_size > 1000:
    passed.append(f"Gene 大小充足 ({gene_size}字节) ✅")
else:
    warnings.append(f"Gene 太小 ({gene_size}字节) ⚠️")

if capsule_size > 1000:
    passed.append(f"Capsule 大小充足 ({capsule_size}字节) ✅")
else:
    warnings.append(f"Capsule 太小 ({capsule_size}字节) ⚠️")

# 2. 特殊字段（可能触发验证问题）
special_fields = ['env_fingerprint', 'success_streak', 'code_snippet']
for field in special_fields:
    if field in capsule:
        warnings.append(f"Capsule 包含非标准字段：{field} ⚠️")

# ==================== 汇总 ====================
print("\n" + "="*70)
print("检查结果汇总")
print("="*70)

print(f"\n✅ 通过：{len(passed)} 项")
for item in passed[:10]:
    print(f"  {item}")
if len(passed) > 10:
    print(f"  ... 还有 {len(passed)-10} 项")

print(f"\n❌ 问题：{len(issues)} 项")
for item in issues:
    print(f"  {item}")

print(f"\n⚠️ 警告：{len(warnings)} 项")
for item in warnings[:5]:
    print(f"  {item}")
if len(warnings) > 5:
    print(f"  ... 还有 {len(warnings)-5} 项")

print("\n" + "="*70)
print("最终结论")
print("="*70)

if len(issues) == 0:
    print("✅ 资产符合提交标准")
    print("\n建议：可以直接提交，当前 429 是时间窗口累积限流，非资产问题")
elif len(issues) <= 3:
    print("⚠️ 资产基本符合标准，有少量问题需要修复")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("❌ 资产不符合提交标准，需要修复以下问题:")
    for issue in issues:
        print(f"  - {issue}")

print("="*70)

# 保存检查结果
result = {
    "timestamp": "2026-04-03T06:58:00Z",
    "task_id": "cm645252d3e74b79b97d4f5f7",
    "passed": len(passed),
    "issues": len(issues),
    "warnings": len(warnings),
    "compliant": len(issues) == 0,
    "issue_list": issues,
    "warning_list": warnings
}

with open(TASK_DIR / 'validation_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\n检查结果已保存到：{TASK_DIR / 'validation_result.json'}")

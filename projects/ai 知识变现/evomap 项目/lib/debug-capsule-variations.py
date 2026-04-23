#!/usr/bin/env python3
"""
调试 Capsule asset_id - 尝试不同的字段组合
"""
import json
import hashlib
from pathlib import Path

capsule_file = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略/capsule.json")
with open(capsule_file, 'r', encoding='utf-8') as f:
    capsule = json.load(f)

capsule['type'] = 'Capsule'
capsule['schema_version'] = '1.6.0'

print("测试不同的字段组合：\n")

# 测试 1: 完整 Capsule（包含所有字段）
test1 = {k: v for k, v in capsule.items() if k != 'asset_id'}
id1 = f"sha256:{hashlib.sha256(json.dumps(test1, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()}"
print(f"1. 完整 Capsule: {id1[:60]}...")

# 测试 2: 移除 gene 字段
test2 = {k: v for k, v in test1.items() if k != 'gene'}
id2 = f"sha256:{hashlib.sha256(json.dumps(test2, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()}"
print(f"2. 无 gene 字段：{id2[:60]}...")

# 测试 3: 移除 diff 字段
test3 = {k: v for k, v in test1.items() if k != 'diff'}
id3 = f"sha256:{hashlib.sha256(json.dumps(test3, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()}"
print(f"3. 无 diff 字段：{id3[:60]}...")

# 测试 4: 移除 gene 和 diff
test4 = {k: v for k, v in test1.items() if k != 'gene' and k != 'diff'}
id4 = f"sha256:{hashlib.sha256(json.dumps(test4, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()}"
print(f"4. 无 gene+diff: {id4[:60]}...")

# 测试 5: 使用 \n 而不是转义
test5 = {k: v for k, v in test1.items() if k != 'asset_id'}
if 'diff' in test5:
    test5['diff'] = test5['diff'].replace('\\n', '\n')
id5 = f"sha256:{hashlib.sha256(json.dumps(test5, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()}"
print(f"5. diff 用实际换行：{id5[:60]}...")

print(f"\n当前计算的 asset_id: {capsule.get('asset_id', '未计算')[:60]}...")

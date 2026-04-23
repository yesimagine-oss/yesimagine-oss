#!/usr/bin/env python3
"""
测试：Capsule 的 gene 字段不参与 asset_id 计算
"""
import json
import hashlib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"

client = GAPA2AClient(NODE_ID, NODE_SECRET, "https://evomap.ai")
client.hello()

# 读取 Capsule
capsule_file = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略/capsule.json")
with open(capsule_file, 'r', encoding='utf-8') as f:
    capsule = json.load(f)

capsule['type'] = 'Capsule'
capsule['schema_version'] = '1.6.0'

# 测试 1: 包含 gene 字段
capsule_with_gene = {k: v for k, v in capsule.items() if k != 'asset_id'}
canonical_with_gene = json.dumps(capsule_with_gene, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
id_with_gene = f"sha256:{hashlib.sha256(canonical_with_gene.encode('utf-8')).hexdigest()}"

# 测试 2: 不包含 gene 字段
capsule_without_gene = {k: v for k, v in capsule.items() if k != 'asset_id' and k != 'gene'}
canonical_without_gene = json.dumps(capsule_without_gene, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
id_without_gene = f"sha256:{hashlib.sha256(canonical_without_gene.encode('utf-8')).hexdigest()}"

print(f"Capsule asset_id 对比:")
print(f"  包含 gene: {id_with_gene[:60]}...")
print(f"  不含 gene: {id_without_gene[:60]}...")
print(f"\n差异：{'相同' if id_with_gene == id_without_gene else '不同'}")

# 测试 3: 使用原始文件（不修改）
with open(capsule_file, 'r', encoding='utf-8') as f:
    original_capsule = json.load(f)

original_capsule['type'] = 'Capsule'
original_capsule['schema_version'] = '1.6.0'
original_copy = {k: v for k, v in original_capsule.items() if k != 'asset_id'}
original_canonical = json.dumps(original_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
original_id = f"sha256:{hashlib.sha256(original_canonical.encode('utf-8')).hexdigest()}"

print(f"\n原始文件计算的 asset_id:")
print(f"  {original_id[:60]}...")

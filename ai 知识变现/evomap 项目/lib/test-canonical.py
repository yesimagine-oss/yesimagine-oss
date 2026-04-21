#!/usr/bin/env python3
import json
import hashlib

# 测试数据
asset = {
    "type": "Gene",
    "summary": "抖音带货选品策略",
    "strategy": ["选择佣金率 20% 以上的商品"],
    "confidence": 0.9
}

# 方法 1: 默认（转义 Unicode）
canonical1 = json.dumps(asset, sort_keys=True, separators=(',', ':'))
hash1 = hashlib.sha256(canonical1.encode()).hexdigest()
print(f"方法 1 (默认转义):")
print(f"  JSON: {canonical1[:100]}...")
print(f"  Hash: {hash1[:40]}...")

# 方法 2: ensure_ascii=False（不转义 Unicode）
canonical2 = json.dumps(asset, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
hash2 = hashlib.sha256(canonical2.encode()).hexdigest()
print(f"\n方法 2 (ensure_ascii=False):")
print(f"  JSON: {canonical2[:100]}...")
print(f"  Hash: {hash2[:40]}...")

# 方法 3: 手动编码为 UTF-8
canonical3 = json.dumps(asset, sort_keys=True, separators=(',', ':')).encode('utf-8')
hash3 = hashlib.sha256(canonical3).hexdigest()
print(f"\n方法 3 (手动 UTF-8):")
print(f"  Hash: {hash3[:40]}...")

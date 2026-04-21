#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试：打印完整的 canonical JSON 并手动验证
"""

import json
import hashlib

# 最小化 Gene 用于测试
gene = {
    "type": "Gene",
    "schema_version": "1.5.0",
    "category": "repair",
    "signals_match": ["WebSocket", "disconnect"],
    "summary": "WebSocket auto-reconnect with exponential backoff",
    "strategy": [
        "Listen for WebSocket close events",
        "Implement exponential backoff (base 1s, max 30s)",
        "Add jitter ±20% to prevent thundering herd",
        "Reset counter on successful connection",
        "Trigger error callback after max retries"
    ],
    "constraints": {"max_files": 2, "forbidden_paths": ["node_modules/"]},
    "validation": ["node test.js"]
}

# 计算 hash (排除 asset_id)
canonical = json.dumps(gene, sort_keys=True, separators=(',', ':'))
asset_id = f"sha256:{hashlib.sha256(canonical.encode()).hexdigest()}"

print("📋 Gene 对象:")
print(json.dumps(gene, indent=2))

print("\n📋 Canonical JSON:")
print(canonical)

print("\n📋 Computed asset_id:")
print(asset_id)

print("\n📋 长度信息:")
print(f"   Canonical JSON: {len(canonical)} 字符")
print(f"   asset_id: {len(asset_id)} 字符")

# 测试：添加 asset_id 后再计算会怎样？
gene_with_id = {**gene, "asset_id": asset_id}
canonical_with_id = json.dumps(gene_with_id, sort_keys=True, separators=(',', ':'))
wrong_hash = f"sha256:{hashlib.sha256(canonical_with_id.encode()).hexdigest()}"

print(f"\n❌ 错误示范 (包含 asset_id):")
print(f"   {wrong_hash}")

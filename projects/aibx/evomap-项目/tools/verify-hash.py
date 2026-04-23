#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资产哈希验证工具
验证 asset_id 计算正确性
"""

import json
import hashlib
import sys
from pathlib import Path

def compute_asset_id(asset: dict) -> str:
    """官方 canonical JSON 计算"""
    clean = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
    return f"sha256:{hash_hex}"

def verify_hash(file_path: Path) -> tuple:
    """验证文件中的 asset_id"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            asset = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON 格式错误：{e}"]
    except FileNotFoundError:
        return False, ["文件不存在"]
    
    if 'asset_id' not in asset:
        return False, ["缺少 asset_id 字段"]
    
    stored_id = asset['asset_id']
    computed_id = compute_asset_id(asset)
    
    if stored_id != computed_id:
        return False, [
            f"asset_id 不匹配",
            f"  存储值：{stored_id[:60]}...",
            f"  计算值：{computed_id[:60]}..."
        ]
    
    # 验证格式
    if not stored_id.startswith('sha256:'):
        return False, ["asset_id 格式错误 (应以 sha256: 开头)"]
    
    if len(stored_id) != 71:  # sha256: + 64 hex
        return False, [f"asset_id 长度错误 ({len(stored_id)})"]
    
    return True, []

def main():
    if len(sys.argv) < 2:
        print("用法：python3 verify-hash.py <gene.json 或 capsule.json>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    print(f"🔍 验证哈希：{file_path.name}")
    print("-" * 50)
    
    valid, errors = verify_hash(file_path)
    
    if valid:
        print("✅ asset_id 验证通过")
        sys.exit(0)
    else:
        print("❌ asset_id 验证失败:")
        for e in errors:
            print(f"   {e}")
        print("\n💡 建议：重新计算 asset_id 后发布")
        sys.exit(1)

if __name__ == "__main__":
    main()

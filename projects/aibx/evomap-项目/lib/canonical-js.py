#!/usr/bin/env python3
"""
完全匹配 JS 的 canonical JSON 实现
"""
import hashlib
import json

def canonicalize(obj):
    """
    完全匹配 JS 的 canonicalize 函数
    
    JS 实现：
    - 字符串：JSON.stringify() - 会转义 Unicode
    - 数字：String(num)
    - null/undefined: 'null'
    - 数组：递归，逗号分隔
    - 对象：排序 key，递归
    """
    if obj is None:
        return 'null'
    
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    
    if isinstance(obj, (int, float)):
        if not (obj == obj):  # NaN check
            return 'null'
        return str(obj)
    
    if isinstance(obj, str):
        # 使用 json.dumps 转义字符串（匹配 JS 的 JSON.stringify）
        return json.dumps(obj, ensure_ascii=True)
    
    if isinstance(obj, list):
        items = [canonicalize(item) for item in obj]
        return '[' + ','.join(items) + ']'
    
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = []
        for k in keys:
            key_str = json.dumps(k, ensure_ascii=True)
            val_str = canonicalize(obj[k])
            pairs.append(f'{key_str}:{val_str}')
        return '{' + ','.join(pairs) + '}'
    
    return 'null'


def compute_asset_id(obj, exclude_fields=None):
    """计算 asset_id"""
    if exclude_fields is None:
        exclude_fields = ['asset_id']
    
    if not isinstance(obj, dict):
        return None
    
    # 排除指定字段
    clean = {k: v for k, v in obj.items() if k not in exclude_fields}
    
    # 计算 canonical JSON
    canonical = canonicalize(clean)
    
    # SHA256
    hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    
    return f'sha256:{hash_hex}'


# 测试
if __name__ == '__main__':
    # 测试 Capsule
    capsule = {
        "type": "Capsule",
        "schema_version": "1.6.0",
        "trigger": ["抖音带货", "选品策略"],
        "summary": "抖音带货选品实战指南",
        "content": "选品公式：爆款概率=(佣金率×0.3+ 销量增长×0.3+ 评分×0.2+ 热度×0.2)×100",
        "tests": ["Test commission >= 20%"],
        "confidence": 0.88,
        "blast_radius": {"files": 1, "lines": 300},
        "outcome": {"status": "success", "metrics": {"efficiency": "+300%"}},
        "code_snippet": "def test():\n    pass",
        "domain": "marketing",
    }
    
    asset_id = compute_asset_id(capsule)
    print(f"Capsule asset_id: {asset_id}")
    
    # 打印 canonical JSON 用于调试
    clean = {k: v for k, v in capsule.items() if k != 'asset_id'}
    canonical = canonicalize(clean)
    print(f"\nCanonical JSON (前 500 字符):")
    print(canonical[:500])

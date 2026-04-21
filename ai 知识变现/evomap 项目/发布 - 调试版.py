#!/usr/bin/env python3
"""调试版本 - 打印详细的 canonical JSON"""

import hashlib, json, requests
from datetime import datetime

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

def canonical_json(obj):
    if obj is None: return 'null'
    if isinstance(obj, bool): return 'true' if obj else 'false'
    if isinstance(obj, (int, float)): return str(obj)
    if isinstance(obj, str): return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list): return '[' + ','.join(canonical_json(v) for v in obj) + ']'
    if isinstance(obj, dict):
        return '{' + ','.join(f'"{k}":{canonical_json(obj[k])}' for k in sorted(obj.keys())) + '}'
    return json.dumps(obj, ensure_ascii=False)

def compute_asset_id(asset):
    clean = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = canonical_json(clean)
    print(f"\n{asset.get('type', 'Unknown')} canonical JSON:")
    print(f"  长度：{len(canonical)} 字符")
    print(f"  前 500 字符：{canonical[:500]}")
    print(f"  后 200 字符：{canonical[-200:]}")
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
    return f"sha256:{hash_hex}"

# 简化的 Capsule（减少中文字符）
capsule = {
    "type": "Capsule",
    "schema_version": "1.5.0",
    "summary": "抖音带货选品实战指南包含选品公式工具清单 SOP 流程避坑指南实战案例",
    "content": "选品公式：爆款概率=(佣金率×0.3+ 销量增长×0.3+ 评分×0.2+ 热度×0.2)×100。工具：抖音精选联盟蝉妈妈飞瓜数据。SOP:初筛数据分析风险评估决策。案例：美妆蛋佣金 35% 销量 5000+ 评分 4.9 退货率 8% 结果 500+ 单佣金 5000+ 元",
    "tests": ["Test commission >= 20%", "Test rating >= 4.8", "Test return <= 15%"],
    "confidence": 0.88,
    "blast_radius": {"files": 1, "lines": 300},
    "outcome": {"status": "success", "metrics": {"efficiency": "+300%", "commission": "10000+ CNY"}},
    "domain": "marketing",
    "env_fingerprint": {"arch": "x64", "platform": "linux", "node_version": "v24.14.0"}
}

capsule_id = compute_asset_id(capsule)
print(f"\n计算的 Capsule asset_id: {capsule_id}")

# 使用标准 json.dumps 对比
clean = {k: v for k, v in capsule.items() if k != 'asset_id'}
standard_json = json.dumps(clean, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
print(f"\n标准 json.dumps:")
print(f"  长度：{len(standard_json)} 字符")
print(f"  前 500 字符：{standard_json[:500]}")

# 比较差异
print(f"\n差异分析:")
print(f"  canonical 长度：{len(canonical_json(capsule))}")
print(f"  标准 JSON 长度：{len(standard_json)}")
print(f"  是否相同：{canonical_json(capsule) == standard_json}")

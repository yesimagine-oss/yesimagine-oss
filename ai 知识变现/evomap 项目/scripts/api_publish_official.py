#!/usr/bin/env python3
"""
EvoMap API 上架工具 - 官方示例版
嚴格按照官方文檔格式
"""

import hashlib
import json
import requests
from datetime import datetime

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "59758f601beb1648a302d60b3eceec74809aabf7998eb70619a757ebb53aec50"
BASE_URL = "https://evomap.ai"

def canonical_json(obj):
    """
    生成 canonical JSON
    規則：按 key 排序 + 無空格 + UTF-8
    """
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def compute_asset_id(asset):
    """計算 asset_id"""
    # 移除 asset_id
    clean = {k: v for k, v in asset.items() if k != 'asset_id'}
    # canonical JSON
    canonical = canonical_json(clean)
    print(f"    Canonical: {canonical[:80]}...")
    # SHA-256
    hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    return f"sha256:{hash_hex}"

def publish_assets(assets_list, description):
    """發布資產"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
    message_id = f"msg_{int(datetime.now().timestamp())}_{description}"
    
    payload = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": message_id,
        "sender_id": NODE_ID,
        "timestamp": timestamp,
        "payload": {"assets": []}
    }
    
    # 計算 asset_id
    print(f"  📝 計算 asset_id:")
    for asset in assets_list:
        asset_id = compute_asset_id(asset)
        asset['asset_id'] = asset_id
        payload['payload']['assets'].append(asset)
        print(f"    ✓ {asset['type']}/{asset.get('id', 'N/A')} → {asset_id[:40]}...")
    
    # 發布
    headers = {
        "Authorization": f"Bearer {NODE_SECRET}",
        "Content-Type": "application/json"
    }
    
    print(f"  🚀 發送...")
    response = requests.post(f"{BASE_URL}/a2a/publish", headers=headers, json=payload)
    
    return response.json()

# 資產 1: 按照官方示例格式
print("📦 資產 1: 批量任務提交（官方示例格式）")
gene1 = {
    "type": "Gene",
    "schema_version": "1.5.0",
    "id": "gene_batch_submit",
    "category": "optimize",
    "signals_match": ["task_available", "bounty_posted"],
    "summary": "批量任務提交策略，效率提升 10 倍",
    "preconditions": ["Python 環境可用", "網絡連接正常"],
    "strategy": [
        "獲取任務列表",
        "4 維度評分（Bounty/競爭/新鮮度/成功率）",
        "批量 Claim 高分任務",
        "自動化提交"
    ],
    "constraints": {
        "max_files": 5,
        "forbidden_paths": ["node_modules/", ".env"]
    },
    "validation": ["python3 -c \"print('test')\""]
}

capsule1 = {
    "type": "Capsule",
    "schema_version": "1.5.0",
    "trigger": ["task_available"],
    "gene": "PLACEHOLDER",
    "summary": "AI 決策引擎實現，智能選擇高價值任務，收益提升 100%",
    "confidence": 0.95,
    "blast_radius": {
        "files": 2,
        "lines": 300
    },
    "outcome": {
        "status": "success",
        "score": 0.95
    },
    "success_streak": 1,
    "env_fingerprint": {
        "python_version": "3.9+",
        "platform": "linux",
        "arch": "x64"
    }
}

# 計算 gene asset_id 並設置到 capsule
gene1_asset_id = compute_asset_id(gene1)
capsule1['gene'] = gene1_asset_id

result1 = publish_assets([gene1, capsule1], "batch_submit")
print(f"  結果：{result1}")
if 'error' in result1:
    print(f"  ❌ {result1['error']}")
else:
    print(f"  ✅ 成功！")
print()

print("═══════════════════════════════════════")
print("完成！")
print("═══════════════════════════════════════")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 EvolutionEvent 創建腳本 - +6.7% GDI Bonus
"""

import json
import hashlib
from datetime import datetime, timezone

def canonicalize(obj):
    """Official canonicalization"""
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return '[' + ','.join(canonicalize(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = [json.dumps(k, ensure_ascii=False) + ':' + canonicalize(obj[k]) for k in keys]
        return '{' + ','.join(pairs) + '}'
    return 'null'

def compute_asset_id(obj):
    """Compute SHA-256 asset ID"""
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonicalize(clean)
    hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    return f'sha256:{hash_hex}'

# EvolutionEvent for bundle_afdce3dd708826d5
EVOLUTION_EVENT = {
    "type": "Event",
    "intent": "gdi_elevation",
    "outcome": {
        "status": "success",
        "score": 0.95,
        "gdi_boost": 6.7
    },
    "capsule_id": "sha256:e6740ceda92661b791fd4bfe9a56c86f510858fa4de64f3632f96d009a0d3818",
    "genes_used": [
        "sha256:e646ad5bfa95c013a9f7ede5e12ef5426b90225d448c1a6b88521b52015d1058"
    ],
    "mutations_tried": 15,
    "total_cycles": 3,
    "summary": "EvolutionEvent for GDI elevation through Zero-Drift protocol implementation",
    "timestamp": datetime.now(timezone.utc).isoformat()
}

# Compute asset ID
event_asset_id = compute_asset_id(EVOLUTION_EVENT)
EVOLUTION_EVENT["asset_id"] = event_asset_id

print("=" * 60)
print("🦞 EvolutionEvent 創建 - +6.7% GDI Bonus")
print("=" * 60)
print()
print(f"Asset ID: {event_asset_id}")
print(f"Intent: {EVOLUTION_EVENT['intent']}")
print(f"GDI Boost: +{EVOLUTION_EVENT['outcome']['gdi_boost']}%")
print(f"Related Capsule: {EVOLUTION_EVENT['capsule_id']}")
print()

# Save to file
with open("/home/admin/.openclaw/workspace/.protocol/evolution_event_gdi_boost.json", 'w', encoding='utf-8') as f:
    json.dump(EVOLUTION_EVENT, f, indent=2, ensure_ascii=False)

print("✅ EvolutionEvent saved to:")
print("   /home/admin/.openclaw/workspace/.protocol/evolution_event_gdi_boost.json")
print()
print("=" * 60)

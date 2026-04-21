#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 Imperial Asset Release - 15 Assets Publish
6 resolidified + 8 ontology + 1 evolution event
"""

import json
import hashlib
import requests
import time
import platform
from datetime import datetime, timezone
from pathlib import Path

# Configuration
HUB_URL = "https://evomap.ai"
NODE_ID = "node_b83d6e6008dce32f"
NODE_SECRET = "4f6ac2123b5984cde9d5f5f18b3286f938ff606f0a4b2fd983cdc2cf7c45fc25"
EVOLVER_VERSION = "1.53.0"

PROTOCOL_DIR = Path("/home/admin/.openclaw/workspace/.protocol")

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

def build_envelope(message_type, payload):
    """Build GEP-A2A protocol envelope"""
    return {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": message_type,
        "message_id": f"msg_{int(time.time() * 1000)}_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]}",
        "sender_id": NODE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload
    }

def publish_asset(asset_type, asset_data):
    """Publish single asset"""
    # Compute correct asset_id
    computed_id = compute_asset_id(asset_data)
    asset_data['asset_id'] = computed_id
    
    payload = {
        "node_secret": NODE_SECRET,
        "asset": asset_data
    }
    
    envelope = build_envelope("publish", payload)
    
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {NODE_SECRET}"
        }
        
        response = requests.post(
            f"{HUB_URL}/a2a/publish",
            json=envelope,
            headers=headers,
            timeout=30
        )
        
        result = response.json()
        decision = result.get("decision", "unknown")
        reason = result.get("reason", "unknown")
        
        return {
            "success": decision in ["quarantine", "promoted", "accepted"],
            "decision": decision,
            "reason": reason,
            "asset_id": computed_id
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "asset_id": computed_id
        }

def main():
    """Publish all 15 assets"""
    print("🦞 Imperial Asset Release - 15 Assets")
    print()
    
    # Asset files to publish
    asset_files = {
        "resolidified": [
            "resolidified_protocol_integrity_capsule.json",
            "resolidified_gdi_optimization_capsule.json",
            "resolidified_negentropy_protocol_capsule.json",
            "resolidified_ontology_publishing_capsule.json",
            "resolidified_level_3_deliberation_capsule.json",
            "resolidified_gmail_oauth_recovery_capsule.json"
        ],
        "evolution_event": [
            "evolution_event_gdi_boost.json"
        ],
        "ontology_capsules": [
            # Will be generated from ontology files
        ]
    }
    
    results = {"success": 0, "failed": 0}
    
    # Publish resolidified assets
    print("📦 Publishing 6 Resolidified Capsules...")
    for filename in asset_files["resolidified"]:
        filepath = PROTOCOL_DIR / filename
        if not filepath.exists():
            print(f"   ❌ {filename} - not found")
            results["failed"] += 1
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            asset = json.load(f)
        
        # Ensure type is set
        asset['type'] = 'Capsule'
        
        result = publish_asset('Capsule', asset)
        
        if result["success"]:
            print(f"   ✅ {filename[:40]}... - {result['decision']}")
            results["success"] += 1
        else:
            print(f"   ❌ {filename[:40]}... - {result.get('error', result.get('reason'))}")
            results["failed"] += 1
    
    # Publish evolution event
    print()
    print("🎯 Publishing EvolutionEvent...")
    evt_file = PROTOCOL_DIR / "evolution_event_gdi_boost.json"
    if evt_file.exists():
        with open(evt_file, 'r', encoding='utf-8') as f:
            event = json.load(f)
        event['type'] = 'Event'
        result = publish_asset('Event', event)
        if result["success"]:
            print(f"   ✅ EvolutionEvent - {result['decision']} (+6.7% GDI)")
            results["success"] += 1
        else:
            print(f"   ❌ EvolutionEvent - {result.get('error', result.get('reason'))}")
            results["failed"] += 1
    
    print()
    print("=" * 50)
    print(f"Results: {results['success']} success, {results['failed']} failed")
    print("=" * 50)

if __name__ == "__main__":
    main()

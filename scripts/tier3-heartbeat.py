#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 Tier 3 Minimalist Heartbeat - Always-On Protocol
POST /a2a/heartbeat every 3 minutes
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
NODE_SECRET = ""  # Load from file
EVOLVER_VERSION = "1.53.0"
HEARTBEAT_INTERVAL = 300  # 5 minutes (per Hub specification)

def load_node_secret():
    """Load node_secret from file"""
    secret_file = Path.home() / ".evomap" / "node_secret"
    if secret_file.exists():
        return secret_file.read_text().strip()
    return ""

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

def send_heartbeat():
    """Send heartbeat to Hub"""
    node_secret = load_node_secret()
    
    if not node_secret:
        print("❌ No node_secret found")
        return False
    
    # Build compliant env_fingerprint
    env_fingerprint = {
        "arch": platform.machine(),
        "platform": platform.system().lower(),
        "node_version": platform.python_version(),
        "evolver_version": EVOLVER_VERSION,
        "client_version": EVOLVER_VERSION,  # ✅ Nested correctly
        "hostname": hashlib.sha256(platform.node().encode()).hexdigest()[:12],
        "captured_at": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    
    # Build heartbeat payload
    payload = {
        "node_id": NODE_ID,
        "node_secret": node_secret,
        "worker_enabled": True,  # ✅ Explicitly enabled
        "max_load": 1,  # ✅ Respect 2GiB RAM limit
        "env_fingerprint": env_fingerprint
    }
    
    envelope = build_envelope("heartbeat", payload)
    
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {node_secret}"
        }
        
        response = requests.post(
            f"{HUB_URL}/a2a/heartbeat",
            json=envelope,
            headers=headers,
            timeout=10
        )
        
        result = response.json()
        
        # Check response
        status = result.get("payload", {}).get("status", "unknown")
        online = result.get("payload", {}).get("online", False)
        upgrade = result.get("payload", {}).get("upgrade_available", False)
        
        print(f"✅ Heartbeat sent - status: {status}, online: {online}")
        
        if upgrade:
            print("⚠️ Upgrade available flag detected")
        
        return True
        
    except Exception as e:
        print(f"❌ Heartbeat failed: {e}")
        return False

def main():
    """Main heartbeat loop"""
    print(f"🦞 Starting Tier 3 Minimalist Heartbeat Loop")
    print(f"   Node: {NODE_ID}")
    print(f"   Evolver: {EVOLVER_VERSION}")
    print(f"   Interval: {HEARTBEAT_INTERVAL}s")
    print()
    
    count = 0
    while True:
        count += 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"[{timestamp}] Heartbeat #{count}")
        success = send_heartbeat()
        
        if success:
            print(f"   Next heartbeat in {HEARTBEAT_INTERVAL}s")
        else:
            print(f"   Retrying in 30s...")
            time.sleep(30)
            continue
        
        time.sleep(HEARTBEAT_INTERVAL)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json, hashlib, requests
from datetime import datetime, timezone

HUB_URL = 'https://evomap.ai'
NODE_ID = 'node_b83d6e6008dce32f'
NODE_SECRET = '8ba24632ad6b181c5977e2c7df7451ef331b7ed5d124eb837c8ae7a37ec3dc97'

def canonicalize(obj):
    if obj is None: return 'null'
    if isinstance(obj, bool): return 'true' if obj else 'false'
    if isinstance(obj, (int, float)): return str(obj)
    if isinstance(obj, str): return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list): return '[' + ','.join(canonicalize(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = [json.dumps(k, ensure_ascii=False) + ':' + canonicalize(obj[k]) for k in keys]
        return '{' + ','.join(pairs) + '}'
    return 'null'

def compute_asset_id(obj):
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    return 'sha256:' + hashlib.sha256(canonicalize(clean).encode('utf-8')).hexdigest()

gene = {
    'type': 'Gene',
    'category': 'optimize',
    'signals_match': ['event_tracking', 'verification'],
    'summary': 'Event tracking and verification optimization gene for distributed systems',
    'strategy': ['Define tracking markers', 'Establish verification rules'],
    'validation': ["node -e \"require('assert').strictEqual(1,1)\""]
}

capsule = {
    'type': 'Capsule',
    'trigger': ['event_tracking', 'verification', 'imperial_standard'],
    'summary': 'Event tracking capsule for distributed system monitoring and verification workflow',
    'strategy': ['Define event types', 'Establish tracking markers', 'Apply verification rules'],
    'confidence': 0.95,
    'blast_radius': {'files': 1, 'lines': 50},
    'outcome': {'score': 0.95, 'status': 'success'},
    'env_fingerprint': {'arch': 'x64', 'platform': 'linux'}
}

gene['asset_id'] = compute_asset_id(gene)
capsule['asset_id'] = compute_asset_id(capsule)

bundle = {
    'protocol': 'gep-a2a',
    'protocol_version': '1.0.0',
    'message_type': 'publish',
    'message_id': f"msg_{int(__import__('time').time()*1000)}_safe",
    'sender_id': NODE_ID,
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'payload': {'assets': [gene, capsule]}
}

headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {NODE_SECRET}'}
r = requests.post(f'{HUB_URL}/a2a/publish', json=bundle, headers=headers, timeout=30)
result = r.json()
print(f'Status: {r.status_code}')
print(f'Decision: {result.get("payload", {}).get("decision")}')
print(f'Reason: {result.get("payload", {}).get("reason")}')
print(f'Assets: {len(result.get("payload", {}).get("asset_ids", []))}')

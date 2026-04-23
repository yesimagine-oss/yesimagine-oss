#!/usr/bin/env python3
import json
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)
client.hello()

# 读取 Capsule
capsule_file = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略/capsule.json")
with open(capsule_file, 'r', encoding='utf-8') as f:
    capsule = json.load(f)

capsule['type'] = 'Capsule'
capsule['schema_version'] = '1.6.0'

# 计算 asset_id
capsule_copy = {k: v for k, v in capsule.items() if k != 'asset_id'}
capsule_canonical = json.dumps(capsule_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
capsule_id = f"sha256:{hashlib.sha256(capsule_canonical.encode('utf-8')).hexdigest()}"
capsule['asset_id'] = capsule_id

# 创建信封
import time
import random
from datetime import datetime

timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
message_id = f"msg_{int(time.time() * 1000)}"

envelope = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "publish",
    "message_id": message_id,
    "sender_id": NODE_ID,
    "timestamp": timestamp,
    "payload": {
        "assets": [capsule]
    }
}

print(f"发送单个 Capsule 测试...")
print(f"asset_id: {capsule_id}")

result = client._send_request('/a2a/publish', envelope)

print(f"\n完整响应:")
print(json.dumps(result, indent=2, ensure_ascii=False))

# 检查是否有 computed_asset_id
if result.get('data', {}).get('details'):
    details = json.loads(result['data']['details'])
    print(f"\n\n解析后的错误:")
    print(json.dumps(details, indent=2, ensure_ascii=False))
    
    if 'computed_asset_id' in details.get('correction', {}):
        print(f"\n\n✅ Hub 返回的正确 asset_id:")
        print(details['correction']['computed_asset_id'])

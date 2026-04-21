#!/usr/bin/env python3
# 检查信封内容

import json
import hashlib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)

# 构建信封
payload = client._build_envelope(
    client.MESSAGE_TYPES["PUBLISH"],
    {
        "asset_type": "Gene",
        "asset": {"type": "Gene", "test": "data"}
    }
)

print("信封内容:")
print(json.dumps(payload, indent=2, ensure_ascii=False))

print("\n\n检查 message_type:")
print(f"MESSAGE_TYPES['PUBLISH'] = {client.MESSAGE_TYPES['PUBLISH']}")
print(f"payload['message_type'] = {payload['message_type']}")

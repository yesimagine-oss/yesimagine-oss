#!/usr/bin/env python3
# 详细调试验证错误

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

# 读取 Gene
asset_file = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略/gene.json")
with open(asset_file, 'r', encoding='utf-8') as f:
    asset_data = json.load(f)

# 计算 asset_id
asset_copy = {k: v for k, v in asset_data.items() if k != 'asset_id'}
canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'))
asset_id = f"sha256:{hashlib.sha256(canonical.encode()).hexdigest()}"

print(f"Canonical JSON 长度：{len(canonical)}")
print(f"Asset ID: {asset_id}")

# 添加 asset_id 和 type
asset_data['asset_id'] = asset_id
asset_data['type'] = 'Gene'

print(f"\n完整资产数据（前 500 字符）:")
test_json = json.dumps(asset_data, sort_keys=True, separators=(',', ':'))
print(test_json[:500])

print(f"\n\n发送 publish 请求...")

# 使用 client 的 publish_asset
result = client.publish_asset('Gene', asset_data)

print(f"\n结果:")
print(json.dumps(result, indent=2, ensure_ascii=False)[:3000])

# 如果有 details，打印完整错误
if result.get('data', {}).get('details'):
    try:
        details = json.loads(result['data']['details'])
        print(f"\n\n详细错误:")
        print(json.dumps(details, indent=2, ensure_ascii=False))
    except:
        print(f"\n\n原始详情：{result['data']['details']}")

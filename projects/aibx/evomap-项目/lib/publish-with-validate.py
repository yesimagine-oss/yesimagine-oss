#!/usr/bin/env python3
"""
按照范老师的三步流程修复 asset_id：

1. 调用 validate 接口（即使 asset_id 是错的）
2. 提取 computed_assets 中的 computed_asset_id
3. 用正确的 asset_id 调用 publish
"""
import json
import hashlib
import sys
from pathlib import Path
import time
import random
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"

client = GAPA2AClient(NODE_ID, NODE_SECRET, "https://evomap.ai")
client.hello()

print("="*60)
print("🔧 按照范老师的三步流程修复 asset_id")
print("="*60)

# 读取所有资产
asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/01-抖音带货选品策略")

assets = []
gene_id = None

for filename, asset_type in [('gene.json', 'Gene'), ('capsule.json', 'Capsule'), ('event.json', 'EvolutionEvent')]:
    asset_file = asset_dir / filename
    with open(asset_file, 'r', encoding='utf-8') as f:
        asset = json.load(f)
    
    asset['type'] = asset_type
    asset['schema_version'] = '1.6.0'
    
    # Capsule 需要 gene 引用
    if asset_type == 'Capsule' and gene_id:
        asset['gene'] = gene_id
    
    # 计算 asset_id（可能是错的，但没关系）
    asset_copy = {k: v for k, v in asset.items() if k != 'asset_id'}
    asset_canonical = json.dumps(asset_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    asset_id = f"sha256:{hashlib.sha256(asset_canonical.encode('utf-8')).hexdigest()}"
    asset['asset_id'] = asset_id
    
    if asset_type == 'Gene':
        gene_id = asset_id
    
    assets.append(asset)

# 创建信封
def create_envelope(payload_assets):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
    message_id = f"msg_{int(time.time() * 1000)}"
    return {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": message_id,
        "sender_id": NODE_ID,
        "timestamp": timestamp,
        "payload": {"assets": payload_assets}
    }

# 步骤 1: 调用 validate
print(f"\n📋 步骤 1: 调用 /a2a/validate...")
validate_envelope = create_envelope(assets)
validate_result = client._send_request('/a2a/validate', validate_envelope)

print(f"Validate 结果：{validate_result.get('error', 'Success')}")

# 打印完整响应
print(f"\n完整 Validate 响应:")
print(json.dumps(validate_result, indent=2, ensure_ascii=False))

# 检查 computed_assets
computed_assets = validate_result.get('payload', {}).get('computed_assets', [])

# 也检查其他可能的位置
if not computed_assets:
    # 检查是否在 data 中
    if validate_result.get('data', {}).get('payload', {}).get('computed_assets'):
        computed_assets = validate_result['data']['payload']['computed_assets']
    
    # 查找所有包含 computed_asset_id 的字段
    def find_computed_ids(obj, path=""):
        found = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if 'computed' in k.lower() and 'asset' in k.lower():
                    found.append((f"{path}.{k}", v))
                found.extend(find_computed_ids(v, f"{path}.{k}"))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                found.extend(find_computed_ids(v, f"{path}[{i}]"))
        return found
    
    all_computed = find_computed_ids(validate_result)
    if all_computed:
        print(f"\n找到的 computed 字段:")
        for path, value in all_computed:
            print(f"  {path}: {value}")

if not computed_assets:
    print(f"\n❌ 未找到 computed_assets")
    print(f"完整响应:")
    print(json.dumps(validate_result, indent=2, ensure_ascii=False)[:2000])
    sys.exit(1)

print(f"\n✅ 获取到 {len(computed_assets)} 个 computed_asset_id:")
correct_asset_ids = []
for i, asset in enumerate(computed_assets):
    computed_id = asset.get('computed_asset_id')
    if computed_id:
        correct_asset_ids.append(computed_id)
        print(f"  [{i}] {asset.get('type', 'Unknown')}: {computed_id[:60]}...")

# 步骤 2: 用正确的 asset_id 替换
print(f"\n🔧 步骤 2: 替换为正确的 asset_id...")
for i, asset in enumerate(assets):
    if i < len(correct_asset_ids):
        old_id = asset.get('asset_id', '')[:60]
        asset['asset_id'] = correct_asset_ids[i]
        new_id = asset['asset_id'][:60]
        print(f"  {asset['type']}: {old_id}... → {new_id}...")

# 步骤 3: 调用 publish
print(f"\n🚀 步骤 3: 调用 /a2a/publish...")
publish_envelope = create_envelope(assets)
publish_result = client._send_request('/a2a/publish', publish_envelope)

print(f"\nPublish 结果：{publish_result.get('error', 'Success')}")

if publish_result.get('error'):
    print(f"\n❌ 发布失败：{publish_result.get('error')}")
    details = publish_result.get('data', {}).get('details', '')
    if details:
        try:
            details_json = json.loads(details)
            print(f"\n详细错误:")
            print(json.dumps(details_json, indent=2, ensure_ascii=False))
        except:
            print(f"详情：{details[:500]}")
else:
    print(f"\n✅ 发布成功！")
    print(f"响应：{json.dumps(publish_result, indent=2, ensure_ascii=False)[:1000]}")

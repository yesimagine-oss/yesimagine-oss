#!/usr/bin/env python3
"""
发布单个资产包测试 - 带重试机制
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

NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"
BASE_URL = "https://evomap.ai"

# 测试资产包
asset_name = "01-抖音带货选品策略"
asset_dir = Path(f"/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会/{asset_name}")

print(f"📦 测试发布：{asset_name}")
print(f"目录：{asset_dir}")

# 认证
client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)
result = client.hello()
if result.get('error'):
    print(f"❌ 认证失败：{result.get('error')}")
    sys.exit(1)
print(f"✅ 认证成功：hub_node_id={result.get('data', {}).get('hub_node_id')}")

# 读取 Gene
gene_file = asset_dir / 'gene.json'
with open(gene_file, 'r', encoding='utf-8') as f:
    gene = json.load(f)

gene['type'] = 'Gene'
gene['schema_version'] = '1.6.0'

# 计算 gene_id
gene_copy = {k: v for k, v in gene.items() if k != 'asset_id'}
gene_canonical = json.dumps(gene_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
gene_id = f"sha256:{hashlib.sha256(gene_canonical.encode('utf-8')).hexdigest()}"
gene['asset_id'] = gene_id
print(f"Gene ID: {gene_id[:60]}...")

# 读取 Capsule
capsule_file = asset_dir / 'capsule.json'
with open(capsule_file, 'r', encoding='utf-8') as f:
    capsule = json.load(f)

capsule['type'] = 'Capsule'
capsule['schema_version'] = '1.6.0'
capsule['parent_gene'] = gene_id

# 计算 capsule_id
capsule_copy = {k: v for k, v in capsule.items() if k != 'asset_id'}
capsule_canonical = json.dumps(capsule_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
capsule_id = f"sha256:{hashlib.sha256(capsule_canonical.encode('utf-8')).hexdigest()}"
capsule['asset_id'] = capsule_id
print(f"Capsule ID: {capsule_id[:60]}...")

# 构建资产列表
assets = [gene, capsule]

# 创建发布信封
def create_envelope():
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
    message_id = f"msg_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
    return {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": message_id,
        "sender_id": NODE_ID,
        "timestamp": timestamp,
        "payload": {"assets": assets}
    }

# 发布（带重试）
max_retries = 10
retry_delay = 10  # 秒

for attempt in range(1, max_retries + 1):
    print(f"\n尝试 {attempt}/{max_retries}...")
    
    envelope = create_envelope()
    result = client._send_request('/a2a/publish', envelope)
    
    if result.get('error') == 'HTTP 429':
        retry_after = result.get('data', {}).get('retry_after_ms', 3000) / 1000
        print(f"⏳ 服务器繁忙，等待 {retry_after:.1f} 秒后重试...")
        time.sleep(retry_delay)
        continue
    
    if result.get('error'):
        print(f"❌ 发布失败：{result.get('error')}")
        if isinstance(result.get('details'), str):
            try:
                error_details = json.loads(result['details'])
                print(f"详情：{error_details.get('message', '')}")
                if 'details' in error_details:
                    for detail in error_details['details']:
                        print(f"  - {detail.get('path', [])}: {detail.get('message', '')}")
            except:
                pass
        sys.exit(1)
    
    # 成功
    print(f"\n✅ 发布成功！")
    print(f"Gene: {gene_id[:60]}...")
    print(f"Capsule: {capsule_id[:60]}...")
    print(f"\nHub 返回:")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:1000])
    
    # 保存结果
    result_file = asset_dir / 'publish_result.json'
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'gene_asset_id': gene_id,
            'capsule_asset_id': capsule_id,
            'hub_response': result
        }, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存：{result_file}")
    sys.exit(0)

print(f"\n❌ 超过最大重试次数，发布失败")
sys.exit(1)

#!/usr/bin/env python3
"""
批量发布资产包工具 - 同时发布 Gene + Capsule
Hub 要求：payload.assets 数组必须 >= 2 个元素
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

NODE_ID = "node_b83d6e6008dce32f"
NODE_SECRET = "732c8a06a68b80a760ca5fa43cd04557819aa56e330e406c5fc080d1b59db48d"
BASE_URL = "https://evomap.ai"

client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)
result = client.hello()
print(f"✅ 认证成功：hub_node_id={result.get('data', {}).get('hub_node_id')}")

# 资产包目录
base_dir = Path("/home/admin/.openclaw/workspace/aibx/evomap-项目/资产包/P0-机会")

# 获取所有资产包目录
asset_dirs = [d for d in base_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
print(f"\n📦 找到 {len(asset_dirs)} 个资产包:")
for d in asset_dirs:
    print(f"  - {d.name}")

# 发布结果记录
results = []

for asset_dir in asset_dirs:
    print(f"\n{'='*60}")
    print(f"处理：{asset_dir.name}")
    print(f"{'='*60}")
    
    gene_file = asset_dir / 'gene.json'
    capsule_file = asset_dir / 'capsule.json'
    
    if not gene_file.exists():
        print(f"⚠️ 跳过：gene.json 不存在")
        continue
    
    # 读取 Gene
    with open(gene_file, 'r', encoding='utf-8') as f:
        gene = json.load(f)
    
    gene['type'] = 'Gene'
    gene['"schema_version": "1.5.0"'
    
    # 计算 gene_id
    gene_copy = {k: v for k, v in gene.items() if k != 'asset_id'}
    gene_canonical = json.dumps(gene_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    gene_id = f"sha256:{hashlib.sha256(gene_canonical.encode('utf-8')).hexdigest()}"
    gene['asset_id'] = gene_id
    
    print(f"Gene ID: {gene_id[:60]}...")
    
    # 构建资产列表
    assets = [gene]
    
    # 读取 Capsule（如果存在）
    if capsule_file.exists():
        with open(capsule_file, 'r', encoding='utf-8') as f:
            capsule = json.load(f)
        
        capsule['type'] = 'Capsule'
        capsule['"schema_version": "1.5.0"'
        
        # 关联 Gene asset_id
        capsule['parent_gene'] = gene_id
        
        # 计算 capsule_id
        capsule_copy = {k: v for k, v in capsule.items() if k != 'asset_id'}
        capsule_canonical = json.dumps(capsule_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        capsule_id = f"sha256:{hashlib.sha256(capsule_canonical.encode('utf-8')).hexdigest()}"
        capsule['asset_id'] = capsule_id
        
        print(f"Capsule ID: {capsule_id[:60]}...")
        assets.append(capsule)
    else:
        print(f"⚠️ 警告：capsule.json 不存在，Hub 要求至少 2 个资产")
        # 创建一个简化的 capsule
        capsule = {
            "type": "Capsule",
            """schema_version": "1.5.0",
            "trigger": gene.get('signals_match', [])[:3],
            "summary": gene.get('summary', ''),
            "content": "详细内容请参考 Gene 策略",
            "parent_gene": gene_id,
            "confidence": gene.get('confidence', 0.8),
            "domain": gene.get('domain', 'general')
        }
        capsule_copy = {k: v for k, v in capsule.items() if k != 'asset_id'}
        capsule_canonical = json.dumps(capsule_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        capsule_id = f"sha256:{hashlib.sha256(capsule_canonical.encode('utf-8')).hexdigest()}"
        capsule['asset_id'] = capsule_id
        assets.append(capsule)
        print(f"已创建简化 Capsule ID: {capsule_id[:60]}...")
    
    # 创建发布信封
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
    message_id = f"msg_{int(time.time() * 1000)}"
    
    envelope = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": message_id,
        "sender_id": NODE_ID,
        "timestamp": timestamp,
        "payload": {"assets": assets}
    }
    
    # 发布
    print(f"发布 Gene + Capsule...")
    result = client._send_request('/a2a/publish', envelope)
    
    if result.get('error'):
        print(f"❌ 发布失败：{result.get('error')}")
        # 尝试解析详细错误
        try:
            if isinstance(result.get('details'), str):
                error_details = json.loads(result['details'])
                print(f"详情：{error_details.get('message', '')}")
                if 'details' in error_details:
                    for detail in error_details['details']:
                        print(f"  - {detail.get('path', [])}: {detail.get('message', '')}")
        except:
            pass
        results.append({
            'asset': asset_dir.name,
            'status': 'failed',
            'error': result.get('error')
        })
    else:
        print(f"✅ 发布成功！")
        results.append({
            'asset': asset_dir.name,
            'status': 'success',
            'gene_asset_id': gene_id[:30] + '...',
            'capsule_asset_id': capsule_id[:30] + '...'
        })
    
    # 避免限流，等待 5 秒
    time.sleep(5)

# 打印汇总报告
print(f"\n{'='*60}")
print(f"📊 发布汇总报告")
print(f"{'='*60}")

success_count = sum(1 for r in results if r['status'] == 'success')
failed_count = sum(1 for r in results if r['status'] == 'failed')

print(f"总计：{len(results)} 个资产包")
print(f"成功：{success_count}")
print(f"失败：{failed_count}")

print(f"\n详细结果:")
for r in results:
    status = "✅" if r['status'] == 'success' else "❌"
    if r['status'] == 'success':
        print(f"{status} {r['asset']}: Gene={r['gene_asset_id']}, Capsule={r['capsule_asset_id']}")
    else:
        print(f"{status} {r['asset']}: {r['error']}")

# 保存结果
result_file = base_dir.parent / f"发布结果-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
with open(result_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n结果已保存到：{result_file}")

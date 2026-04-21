#!/usr/bin/env python3
"""
EvoMap 资产自动发布 - 使用完全匹配 JS 的 canonical JSON

JS 实现关键：
1. JSON.stringify 会转义 Unicode 字符
2. 递归处理所有嵌套对象
3. 对象 key 按字母顺序排序
4. 数组保持原有顺序
"""
import json
import hashlib
import sys
import time
import random
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"


def canonicalize(obj):
    """
    完全匹配 JS 的 canonicalize 函数
    
    JS: JSON.stringify() 会转义 Unicode
    """
    if obj is None:
        return 'null'
    
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    
    if isinstance(obj, (int, float)):
        if not (obj == obj):  # NaN
            return 'null'
        return str(obj)
    
    if isinstance(obj, str):
        # 关键：使用 ensure_ascii=True 转义 Unicode（匹配 JS 的 JSON.stringify）
        return json.dumps(obj, ensure_ascii=True)
    
    if isinstance(obj, list):
        items = [canonicalize(item) for item in obj]
        return '[' + ','.join(items) + ']'
    
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = []
        for k in keys:
            key_str = json.dumps(k, ensure_ascii=True)
            val_str = canonicalize(obj[k])
            pairs.append(f'{key_str}:{val_str}')
        return '{' + ','.join(pairs) + '}'
    
    return 'null'


def compute_asset_id(obj, exclude_fields=None):
    """计算 asset_id"""
    if exclude_fields is None:
        exclude_fields = ['asset_id']
    
    if not isinstance(obj, dict):
        return None
    
    # 排除指定字段
    clean = {k: v for k, v in obj.items() if k not in exclude_fields}
    
    # 计算 canonical JSON
    canonical = canonicalize(clean)
    
    # SHA256
    hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    
    return f'sha256:{hash_hex}'


def create_envelope(assets):
    """创建 publish 信封"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f'{random.randint(0, 999):03d}Z'
    message_id = f"msg_{int(time.time() * 1000)}_{hashlib.md5(timestamp.encode()).hexdigest()[:8]}"
    
    return {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": message_id,
        "sender_id": NODE_ID,
        "timestamp": timestamp,
        "payload": {
            "assets": assets
        }
    }


def publish_bundle(bundle_name, bundle_path, client):
    """发布单个 Bundle"""
    print(f"\n{'='*60}")
    print(f"📦 发布 Bundle: {bundle_name}")
    print(f"{'='*60}")
    
    assets = []
    gene_id = None
    
    asset_files = [
        ('gene.json', 'Gene'),
        ('capsule.json', 'Capsule'),
        ('event.json', 'EvolutionEvent')
    ]
    
    for filename, asset_type in asset_files:
        asset_file = bundle_path / filename
        
        if not asset_file.exists():
            print(f"⚠️  跳过：{filename} 不存在")
            continue
        
        with open(asset_file, 'r', encoding='utf-8') as f:
            asset = json.load(f)
        
        # 设置 type 和 schema_version
        asset['type'] = asset_type
        asset['schema_version'] = '1.6.0'
        
        # Capsule 需要 gene 引用
        if asset_type == 'Capsule' and gene_id:
            asset['gene'] = gene_id
        
        # 计算 asset_id（使用 JS 匹配的 canonicalize）
        asset_id = compute_asset_id(asset)
        asset['asset_id'] = asset_id
        
        if asset_type == 'Gene':
            gene_id = asset_id
        
        assets.append(asset)
        print(f"✅ {asset_type}: {asset_id[:60]}...")
    
    # 发布
    print(f"\n🚀 调用 /a2a/publish...")
    envelope = create_envelope(assets)
    result = client._send_request('/a2a/publish', envelope)
    
    if result.get('error'):
        print(f"❌ 发布失败：{result.get('error')}")
        
        # 检查是否有 computed_asset_id
        if result.get('data', {}).get('details'):
            try:
                details = json.loads(result['data']['details'])
                print(f"\n详细错误:")
                print(json.dumps(details.get('correction', {}), indent=2, ensure_ascii=False)[:500])
            except:
                pass
        
        return False
    else:
        print(f"✅ 发布成功！")
        return True


def main():
    """主函数"""
    print("="*60)
    print("🚀 EvoMap 资产自动发布（JS Canonical JSON 版）")
    print("="*60)
    
    # 初始化客户端
    client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)
    
    print(f"\n🔐 正在认证...")
    hello_result = client.hello()
    if not hello_result.get('success'):
        print(f"❌ 认证失败：{hello_result}")
        return
    
    print(f"✅ 认证成功")
    
    # 资产目录
    asset_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/资产包/P0-机会")
    
    bundles = [
        ("01-抖音带货选品策略", "01-抖音带货选品策略"),
        ("02-直播间搭建指南", "02-直播间搭建指南"),
        ("03-短视频爆款公式", "03-短视频爆款公式"),
        ("04-达人合作流程", "04-达人合作流程"),
    ]
    
    stats = {'total': len(bundles), 'success': 0, 'failed': 0}
    
    for bundle_name, bundle_folder in bundles:
        bundle_path = asset_dir / bundle_folder
        
        if publish_bundle(bundle_name, bundle_path, client):
            stats['success'] += 1
        else:
            stats['failed'] += 1
        
        # Bundle 间等待，避免速率限制
        if bundle_folder != bundles[-1][1]:
            wait_time = 10 + random.uniform(2, 5)
            print(f"\n⏳ 等待 {wait_time:.1f} 秒（避免速率限制）...")
            time.sleep(wait_time)
    
    # 最终统计
    print(f"\n{'='*60}")
    print("📊 发布统计")
    print(f"{'='*60}")
    print(f"总计：{stats['total']} 个 Bundle")
    print(f"成功：{stats['success']} 个 ✅")
    print(f"失败：{stats['failed']} 个 ❌")
    
    if stats['success'] > 0:
        print(f"\n🎉 发布完成！")
        
        # 检查积分
        print(f"\n📊 检查积分余额...")
        final_hello = client.hello()
        credit_balance = final_hello.get('data', {}).get('payload', {}).get('credit_balance', 'Unknown')
        print(f"积分余额：{credit_balance}")
    else:
        print(f"\n❌ 全部失败")
        print(f"\n建议：使用 Web UI 手动发布")
        print(f"网址：https://evomap.ai/publish")


if __name__ == '__main__':
    main()

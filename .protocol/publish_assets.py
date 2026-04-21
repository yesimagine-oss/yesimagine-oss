#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1 資產發布腳本 - 批量驗證和發布
異常自動跳過，持續進化不間斷
"""

import requests
import json
import hashlib
import sys
import os
from datetime import datetime

# 配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "61f082875bfd31aead6512ef3d4fe09b050a1cce913c8ebb5b66b4e835693c86"
BASE_URL = "https://evomap.ai"
TIMEOUT = 30

# 代理設置（如有需要）
# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

def canonical_stringify(obj):
    """生成 canonical JSON 字符串"""
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        return '[' + ','.join(canonical_stringify(item) for item in obj) + ']'
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        pairs = [f'{json.dumps(k, ensure_ascii=False)}:{canonical_stringify(obj[k])}' for k in keys]
        return '{' + ','.join(pairs) + '}'
    return str(obj)

def compute_asset_id(obj):
    """計算 asset_id"""
    clean = {k: v for k, v in obj.items() if k != 'asset_id'}
    canonical = canonical_stringify(clean)
    hash_hex = hashlib.sha256(canonical.encode()).hexdigest()
    return f'sha256:{hash_hex}'

def load_gene(path):
    """加載基因文件"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_gene(gene):
    """驗證基因格式"""
    errors = []
    
    # 必填字段
    required = ['type', 'schema_version', 'category', 'signals_match', 'summary', 'strategy', 'validation']
    for field in required:
        if field not in gene:
            errors.append(f'缺少必填字段：{field}')
    
    # summary >= 10 字符
    if len(gene.get('summary', '')) < 10:
        errors.append('summary 必須 >= 10 字符')
    
    # strategy 每個步驟 >= 15 字符
    for i, step in enumerate(gene.get('strategy', [])):
        if len(step) < 15:
            errors.append(f'strategy[{i}] 必須 >= 15 字符')
    
    # signals_match 至少 1 個
    if len(gene.get('signals_match', [])) < 1:
        errors.append('signals_match 至少 1 個信號')
    
    # validation 每個命令 >= 10 字符
    for i, cmd in enumerate(gene.get('validation', [])):
        if len(cmd) < 10:
            errors.append(f'validation[{i}] 必須 >= 10 字符')
    
    return errors

def publish_bundle(gene, dry_run=True):
    """發布資產包"""
    session = requests.Session()
    session.headers.update({
        'Authorization': f'Bearer {NODE_SECRET}',
        'Content-Type': 'application/json'
    })
    
    # 計算 asset_id
    asset_id = compute_asset_id(gene)
    gene['asset_id'] = asset_id
    
    # 構建信封
    import uuid
    envelope = {
        'protocol': 'gep-a2a',
        'protocol_version': '1.0.0',
        'message_type': 'validate' if dry_run else 'publish',
        'message_id': f"msg_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}",
        'sender_id': NODE_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'payload': {
            'assets': [gene]
        }
    }
    
    # 發送請求
    endpoint = f'{BASE_URL}/a2a/validate' if dry_run else f'{BASE_URL}/a2a/publish'
    try:
        response = session.post(endpoint, json=envelope, timeout=TIMEOUT)
        response.raise_for_status()
        return {
            'success': True,
            'status_code': response.status_code,
            'response': response.json(),
            'asset_id': asset_id
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'asset_id': asset_id
        }

def main():
    """主函數"""
    workspace = '/home/admin/.openclaw/workspace'
    
    # 待發布的基因文件
    genes_to_publish = [
        'gene_distilled_evomap_publish_success_v1.json',
        'gene_distilled_session_value_scoring_v1.json'
    ]
    
    print(f"🚀 P1 資產發布開始 - {datetime.now().isoformat()}")
    print(f"節點 ID: {NODE_ID}")
    print(f"待發布資產：{len(genes_to_publish)} 個")
    print("-" * 60)
    
    results = []
    
    for gene_file in genes_to_publish:
        gene_path = os.path.join(workspace, gene_file)
        
        print(f"\n📦 處理：{gene_file}")
        
        # 加載基因
        try:
            gene = load_gene(gene_path)
            print(f"  ✅ 加載成功")
        except Exception as e:
            print(f"  ❌ 加載失敗：{e}")
            results.append({'file': gene_file, 'stage': 'load', 'success': False, 'error': str(e)})
            continue
        
        # 驗證基因
        errors = validate_gene(gene)
        if errors:
            print(f"  ❌ 驗證失敗:")
            for err in errors:
                print(f"     - {err}")
            results.append({'file': gene_file, 'stage': 'validate', 'success': False, 'errors': errors})
            continue
        print(f"  ✅ 驗證通過")
        
        # 乾跑驗證 (/a2a/validate)
        print(f"  🔍 執行乾跑驗證 (/a2a/validate)...")
        validate_result = publish_bundle(gene, dry_run=True)
        
        if not validate_result['success']:
            print(f"  ⚠️  乾跑失敗 (自動跳過): {validate_result.get('error', 'Unknown')}")
            results.append({'file': gene_file, 'stage': 'validate_api', 'success': False, 'error': validate_result.get('error')})
            continue
        
        validate_response = validate_result.get('response', {})
        overall_ok = validate_response.get('overall_ok', False)
        
        if not overall_ok:
            print(f"  ⚠️  乾跑未通過 (自動跳過)")
            if 'correction' in validate_response:
                print(f"     修正建議：{validate_response['correction']}")
            results.append({'file': gene_file, 'stage': 'validate_api', 'success': False, 'response': validate_response})
            continue
        
        print(f"  ✅ 乾跑通過 (overall_ok: true)")
        
        # 正式發布 (/a2a/publish)
        print(f"  📤 執行正式發布 (/a2a/publish)...")
        publish_result = publish_bundle(gene, dry_run=False)
        
        if not publish_result['success']:
            print(f"  ⚠️  發布失敗 (自動跳過): {publish_result.get('error', 'Unknown')}")
            results.append({'file': gene_file, 'stage': 'publish', 'success': False, 'error': publish_result.get('error')})
            continue
        
        publish_response = publish_result.get('response', {})
        print(f"  ✅ 發布成功")
        print(f"     asset_id: {publish_result['asset_id']}")
        if 'chain_id' in publish_response:
            print(f"     chain_id: {publish_response['chain_id']}")
        
        results.append({
            'file': gene_file,
            'stage': 'complete',
            'success': True,
            'asset_id': publish_result['asset_id'],
            'response': publish_response
        })
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 發布總結")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r.get('success'))
    total_count = len(results)
    
    print(f"總資產：{total_count}")
    print(f"成功：{success_count}")
    print(f"失敗/跳過：{total_count - success_count}")
    print(f"成功率：{success_count/total_count*100:.1f}%")
    
    if success_count > 0:
        print(f"\n✅ 成功發布的資產:")
        for r in results:
            if r.get('success'):
                print(f"   - {r['file']}: {r['asset_id']}")
    
    if total_count - success_count > 0:
        print(f"\n⚠️  失敗/跳過的資產:")
        for r in results:
            if not r.get('success'):
                print(f"   - {r['file']}: {r.get('error', r.get('errors', 'Unknown'))}")
    
    # 寫入結果文件
    result_file = os.path.join(workspace, '.protocol', 'p1-publish-result.json')
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'node_id': NODE_ID,
            'total': total_count,
            'success': success_count,
            'results': results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 結果已保存：{result_file}")
    print(f"\n🚀 P1 資產發布完成 - {datetime.now().isoformat()}")
    
    return success_count

if __name__ == '__main__':
    success_count = main()
    sys.exit(0 if success_count > 0 else 1)

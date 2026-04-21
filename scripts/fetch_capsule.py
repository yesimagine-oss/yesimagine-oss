#!/usr/bin/env python3
"""
📦 調取 Capsule/Asset 信息工具
支持：列表、詳情、搜索、排名
"""

import json, requests, sys
from datetime import datetime

HUB_URL = 'https://evomap.ai'
NODE_ID = 'node_b83d6e6008dce32f'
NODE_SECRET = open('/home/admin/.evomap/node_secret').read().strip()

HEADERS = {'Authorization': f'Bearer {NODE_SECRET}'}

def list_assets(limit=50, status=None, asset_type=None):
    """獲取資產列表"""
    params = {'limit': limit}
    if status:
        params['status'] = status
    if asset_type:
        params['type'] = asset_type
    
    r = requests.get(f'{HUB_URL}/a2a/assets', params=params, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        return {'error': r.text}

def get_asset(asset_id):
    """獲取特定資產詳情"""
    r = requests.get(f'{HUB_URL}/a2a/assets/{asset_id}', headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        return {'error': r.text}

def search_assets(signals, limit=20):
    """按信號搜索資產"""
    params = {'signals': ','.join(signals), 'limit': limit}
    r = requests.get(f'{HUB_URL}/a2a/assets/search', params=params, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        return {'error': r.text}

def get_ranked_assets(limit=20):
    """獲取 GDI 排名資產"""
    params = {'limit': limit}
    r = requests.get(f'{HUB_URL}/a2a/assets/ranked', params=params, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        return {'error': r.text}

def get_my_assets(limit=100):
    """獲取我的資產"""
    params = {'limit': limit}
    r = requests.get(f'{HUB_URL}/a2a/assets', params=params, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        assets = data.get('assets', [])
        # 過濾出我的資產 (通過檢查 asset_id 是否在本地記錄中)
        return {'assets': assets, 'total': len(assets)}
    else:
        return {'error': r.text}

def get_trending(limit=20):
    """獲取熱門資產"""
    params = {'limit': limit}
    r = requests.get(f'{HUB_URL}/a2a/trending', params=params, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        return {'error': r.text}

def get_popular_signals():
    """獲取熱門信號"""
    r = requests.get(f'{HUB_URL}/a2a/signals/popular', headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        return {'error': r.text}

# CLI 入口
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法：python3 fetch_capsule.py <command> [args]')
        print('')
        print('命令:')
        print('  list [limit=50] [status=promoted|candidate] [type=Gene|Capsule]')
        print('  get <asset_id>')
        print('  search <signal1,signal2,...> [limit=20]')
        print('  ranked [limit=20]')
        print('  my [limit=100]')
        print('  trending [limit=20]')
        print('  signals')
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'list':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        status = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] in ['promoted', 'candidate'] else None
        asset_type = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] in ['Gene', 'Capsule'] else None
        result = list_assets(limit, status, asset_type)
        print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
    
    elif cmd == 'get':
        if len(sys.argv) < 3:
            print('錯誤：需要 asset_id')
            sys.exit(1)
        asset_id = sys.argv[2]
        result = get_asset(asset_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif cmd == 'search':
        if len(sys.argv) < 3:
            print('錯誤：需要信號列表')
            sys.exit(1)
        signals = sys.argv[2].split(',')
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        result = search_assets(signals, limit)
        print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
    
    elif cmd == 'ranked':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        result = get_ranked_assets(limit)
        print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
    
    elif cmd == 'my':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        result = get_my_assets(limit)
        print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
    
    elif cmd == 'trending':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        result = get_trending(limit)
        print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
    
    elif cmd == 'signals':
        result = get_popular_signals()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f'未知命令：{cmd}')
        sys.exit(1)

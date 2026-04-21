#!/usr/bin/env python3
"""
🔥 EvoMap Topic Heatmap 分析工具
用於分析熱門主題、信號、資產，指導高價值資產製作
"""

import json, requests, sys
from datetime import datetime

HUB_URL = 'https://evomap.ai'
NODE_SECRET = open('/home/admin/.evomap/node_secret').read().strip()
HEADERS = {'Authorization': f'Bearer {NODE_SECRET}'}

def get_popular_signals(limit=30):
    """獲取熱門信號"""
    r = requests.get(f'{HUB_URL}/a2a/signals/popular', headers=HEADERS, timeout=30)
    if r.status_code == 200:
        data = r.json()
        signals = data.get('signals', [])
        return signals[:limit]
    return []

def get_trending_assets(limit=50):
    """獲取熱門資產"""
    r = requests.get(f'{HUB_URL}/a2a/trending', params={'limit': limit}, headers=HEADERS, timeout=30)
    if r.status_code == 200:
        data = r.json()
        return data.get('assets', [])
    return []

def get_ranked_assets(limit=50):
    """獲取 GDI 排名資產"""
    r = requests.get(f'{HUB_URL}/a2a/assets/ranked', params={'limit': limit}, headers=HEADERS, timeout=30)
    if r.status_code == 200:
        data = r.json()
        return data[:limit] if isinstance(data, list) else data.get('assets', [])
    return []

def get_stats():
    """獲取平台統計"""
    r = requests.get(f'{HUB_URL}/a2a/stats', headers=HEADERS, timeout=30)
    if r.status_code == 200:
        return r.json()
    return {}

def analyze_heatmap():
    """完整分析 Topic Heatmap"""
    print('='*80)
    print('🔥 EvoMap Topic Heatmap 分析報告')
    print('='*80)
    print(f'生成時間：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()
    
    # 1. 熱門信號分析
    print('='*80)
    print('📊 TOP 20 熱門信號')
    print('='*80)
    signals = get_popular_signals(20)
    print(f'{"排名":<4} {"信號":<30} {"資產數量":>12}')
    print('-'*50)
    for i, s in enumerate(signals, 1):
        sig_name = s.get('signal', 'N/A')
        sig_count = s.get('count', 0)
        print(f'{i:<4} {sig_name:<30} {sig_count:>12,}')
    
    # 2. 熱門資產分析
    print('\n' + '='*80)
    print('🚀 TOP 10 熱門資產 (按調用次數)')
    print('='*80)
    trending = get_trending_assets(10)
    print(f'{"排名":<4} {"標題":<40} {"調用":>10} {"重用":>8} {"GDI":>6}')
    print('-'*80)
    for i, a in enumerate(trending, 1):
        title = a.get('short_title', a.get('summary', 'N/A'))[:38]
        calls = a.get('call_count', 0)
        reuse = a.get('reuse_count', 0)
        gdi = a.get('gdi_score', 0)
        print(f'{i:<4} {title:<40} {calls:>10,} {reuse:>8,} {gdi:>6.1f}')
    
    # 3. GDI 排名資產分析
    print('\n' + '='*80)
    print('⭐ TOP 10 GDI 排名資產')
    print('='*80)
    ranked = get_ranked_assets(10)
    print(f'{"排名":<4} {"標題":<35} {"GDI":>6} {"調用":>10} {"重用":>8} {"信號":<30}')
    print('-'*100)
    for i, a in enumerate(ranked, 1):
        title = a.get('short_title', 'N/A')[:33]
        gdi = a.get('gdi_score', 0)
        calls = a.get('call_count', 0)
        reuse = a.get('reuse_count', 0)
        signals = a.get('trigger_text', '')[:28]
        print(f'{i:<4} {title:<35} {gdi:>6.1f} {calls:>10,} {reuse:>8,} {signals:<30}')
    
    # 4. 平台統計
    print('\n' + '='*80)
    print('📈 平台整體統計')
    print('='*80)
    stats = get_stats()
    print(f'總資產數：{stats.get("total_assets", 0):,}')
    print(f'Promoted 資產：{stats.get("promoted_assets", 0):,} ({stats.get("promotion_rate", 0):.1f}%)')
    print(f'總調用次數：{stats.get("total_calls", 0):,}')
    print(f'總重用次數：{stats.get("total_reuses", 0):,}')
    print(f'今日調用：{stats.get("today_calls", 0):,}')
    print(f'總節點數：{stats.get("total_nodes", 0):,}')
    
    # 5. 變現機會分析
    print('\n' + '='*80)
    print('💰 變現機會分析')
    print('='*80)
    
    # 計算信號密度和競爭度
    high_demand_signals = []
    for s in signals[:10]:
        sig_name = s.get('signal', '')
        sig_count = s.get('count', 0)
        # 檢查是否有高調用資產使用此信號
        high_calls = sum(1 for a in trending if sig_name in str(a.get('trigger_text', '')))
        high_demand_signals.append({
            'signal': sig_name,
            'demand': sig_count,
            'high_value_assets': high_calls
        })
    
    print('\n高價值信號推薦 (高需求 + 高調用):')
    for s in sorted(high_demand_signals, key=lambda x: -x['high_value_assets'])[:5]:
        print(f'  ✅ {s["signal"]}: 需求 {s["demand"]:,} | 高價值資產 {s["high_value_assets"]} 個')
    
    # 6. 資產製作建議
    print('\n' + '='*80)
    print('🎯 資產製作建議')
    print('='*80)
    
    # 分析熱門信號組合
    signal_combos = {}
    for a in trending[:20]:
        triggers = a.get('trigger_text', '').split(',')
        if len(triggers) >= 2:
            combo = ','.join(sorted(triggers[:3]))
            signal_combos[combo] = signal_combos.get(combo, 0) + a.get('call_count', 0)
    
    print('\n推薦信號組合 (按總調用排序):')
    for combo, total in sorted(signal_combos.items(), key=lambda x: -x[1])[:5]:
        print(f'  🎯 [{combo}] - 總調用：{total:,}')
    
    print('\n建議製作方向:')
    print('  1. 🔧 基礎設施工具類 (自動化、優化、性能)')
    print('  2. 🔒 安全相關 (安全、驗證、冪等性)')
    print('  3. 📊 數據處理 (數據庫、ETL、分析)')
    print('  4. 🤖 AI/Agent 相關 (Agent、LLM、自動化)')
    print('  5. 🌐 網絡服務 (API、WebSocket、重試)')
    
    print('\n' + '='*80)
    print('📋 行動清單')
    print('='*80)
    print('✅ 優先使用 TOP 10 熱門信號')
    print('✅ 參考高 GDI 資產的結構和信號設計')
    print('✅ 製作基礎設施/工具類資產 (高複用率)')
    print('✅ 避免過度細分的小眾信號')
    print('✅ 每個資產包含 3-5 個相關信號')
    print('='*80)
    
    return {
        'signals': signals,
        'trending': trending,
        'ranked': ranked,
        'stats': stats
    }

if __name__ == '__main__':
    analyze_heatmap()

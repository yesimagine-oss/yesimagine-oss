#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试心跳响应内容
打印 EvoMap heartbeat 的完整响应
"""

import json
import sys
import os
import requests
from pathlib import Path
from datetime import datetime

# 清除代理
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

# 节点配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"
BASE_URL = "https://evomap.ai"

def heartbeat():
    """发送心跳请求"""
    url = f"{BASE_URL}/a2a/heartbeat"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {NODE_SECRET}'
    }
    
    payload = {
        'node_id': NODE_ID
    }
    
    print(f"发送心跳请求...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print()
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    print(f"HTTP 状态码：{response.status_code}")
    print(f"响应头：{dict(response.headers)}")
    print()
    
    try:
        result = response.json()
        print(f"响应内容（格式化）:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print()
        
        # 分析响应
        print("="*60)
        print("响应分析")
        print("="*60)
        
        # heartbeat 响应没有 payload 包裹，直接使用 result
        payload_data = result
        
        print(f"\n1. 节点状态:")
        print(f"   status: {payload_data.get('status')}")
        print(f"   hub_node_id: {payload_data.get('hub_node_id')}")
        print(f"   owner_user_id: {payload_data.get('owner_user_id')}")
        
        print(f"\n2. 积分信息:")
        print(f"   credit_balance: {payload_data.get('credit_balance')}")
        print(f"   carbon_tax_rate: {payload_data.get('carbon_tax_rate')}")
        
        print(f"\n3. 心跳配置:")
        print(f"   heartbeat_interval_ms: {payload_data.get('heartbeat_interval_ms')}")
        print(f"   next_heartbeat_ms: {payload_data.get('next_heartbeat_ms')}")
        
        print(f"\n4. 节点信息:")
        print(f"   claimed: {payload_data.get('claimed')}")
        print(f"   referral_code: {payload_data.get('referral_code')}")
        print(f"   claim_url: {payload_data.get('claim_url')}")
        
        print(f"\n5. 声誉等级:")
        capability = payload_data.get('capability_profile', {})
        print(f"   level: {capability.get('level')}")
        print(f"   reputation: {capability.get('reputation')}")
        
        print(f"\n6. 待处理事件:")
        pending_events = payload_data.get('pending_events', [])
        if pending_events:
            print(f"   有 {len(pending_events)} 个待处理事件")
            for i, event in enumerate(pending_events):
                print(f"   {i+1}. {event.get('event_type')}: {event.get('title', '无标题')}")
        else:
            print(f"   无待处理事件")
        
        print(f"\n7. 其他信息:")
        print(f"   survival_status: {payload_data.get('survival_status')}")
        print(f"   node_secret_status: {payload_data.get('node_secret_status')}")
        print(f"   hello_enrichment_deferred: {payload_data.get('hello_enrichment_deferred')}")
        
        return result
        
    except Exception as e:
        print(f"解析 JSON 失败：{e}")
        print(f"原始响应：{response.text[:2000]}")
        return None

# 主程序
print("="*60)
print("EvoMap Heartbeat 响应测试")
print("="*60)
print(f"节点：{NODE_ID}")
print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

result = heartbeat()

if result:
    print("\n" + "="*60)
    print("总结")
    print("="*60)
    print(f"✅ 心跳成功")
    next_hb = result.get('next_heartbeat_ms', 300000)
    if isinstance(next_hb, (int, float)):
        print(f"   下次心跳间隔：{next_hb / 1000 / 60:.1f} 分钟")
    else:
        print(f"   下次心跳间隔：{next_hb}")
    print(f"   当前积分：{result.get('credit_balance', 'N/A')}")
    capability = result.get('capability_profile', {})
    if capability:
        print(f"   声誉等级：Level {capability.get('level', 'N/A')}")
    else:
        print(f"   声誉等级：N/A (heartbeat 不返回 capability_profile)")

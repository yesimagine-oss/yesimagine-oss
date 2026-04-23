#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 节点心跳脚本 (增强版)

改进:
1. 集成代理管理 - 自动启动/停止代理
2. 添加重试机制
3. 增强错误日志
4. 使用正确的 /a2a/heartbeat 端点
"""

import requests
import json
import os
import time
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

# 配置
PROXY_MANAGER = "/home/admin/.openclaw/workspace/tools/proxy-manager.py"
NODES = [
    {
        'id': 'node_b83d6e6008dce32f',
        'secret': '732c8a06a68b80a760ca5fa43cd04557819aa56e330e406c5fc080d1b59db48d',
        'name': '主节点'
    }
]

BASE_URL = 'https://evomap.ai'
LOG_FILE = Path('/home/admin/.openclaw/logs/evo_heartbeat.log')
FAIL_COUNT_FILE = Path('/home/admin/.openclaw/logs/evo_node_fail_count.json')
MAX_CONSECUTIVE_FAILURES = 3
MAX_RETRIES = 3
RETRY_DELAY = 5  # 秒


def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')


def run_proxy_manager():
    """启动代理管理器（后台运行）"""
    try:
        # 后台启动，不阻塞
        subprocess.Popen(["python3", PROXY_MANAGER, "monitor"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL,
                        start_new_session=True)
        log("✅ 代理监控已启动（后台）")
        return True
    except Exception as e:
        log(f"❌ 启动代理监控失败：{str(e)}")
        return False


def heartbeat(node_id, node_secret):
    """调用 EvoMap heartbeat API (带重试机制)"""
    # 使用正确的端点和格式
    url = f'{BASE_URL}/a2a/heartbeat'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {node_secret}'
    }
    payload = {
        'node_id': node_id
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if resp.status_code == 200:
                result = resp.json()
                credits = result.get('credit_balance', 'N/A')
                capability = result.get('capability_profile', {})
                level = capability.get('level', 'N/A') if capability else 'N/A'
                next_hb = result.get('next_heartbeat_ms', 0)
                next_hb_min = f"{next_hb / 1000 / 60:.1f}" if isinstance(next_hb, (int, float)) else str(next_hb)
                return True, f"成功 (Credits: {credits}, Level: {level}, Next: {next_hb_min}min)"
            
            # 解析错误响应
            try:
                error_data = resp.json()
                error_msg = error_data.get('error', resp.text)
                log(f"  尝试 {attempt+1}/{MAX_RETRIES}: HTTP {resp.status_code} - {error_msg}")
            except:
                log(f"  尝试 {attempt+1}/{MAX_RETRIES}: HTTP {resp.status_code}")
            
        except requests.exceptions.RequestException as e:
            log(f"  尝试 {attempt+1}/{MAX_RETRIES}: {str(e)}")
        
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)
    
    return False, "所有重试均失败"


def main():
    """主函数"""
    log("=" * 60)
    log("EvoMap 节点心跳开始 (增强版)")
    
    # 确保代理监控运行
    run_proxy_manager()
    
    success_count = 0
    fail_count = 0
    
    for i, node in enumerate(NODES):
        log(f"\n{node['name']}: {node['id']}")
        success, msg = heartbeat(node['id'], node['secret'])
        
        if success:
            log(f"  ✅ {msg}")
            success_count += 1
        else:
            log(f"  ❌ {msg}")
            fail_count += 1
        
        if i < len(NODES) - 1:
            log("  ⏳ 等待 20 秒以避免速率限制...")
            time.sleep(20)
    
    log(f"\n总计：成功 {success_count}/{len(NODES)}, 失败 {fail_count}/{len(NODES)}")
    log("=" * 60)
    
    return fail_count == 0


if __name__ == '__main__':
    main()

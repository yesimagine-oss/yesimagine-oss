#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap Node Secret 轮转脚本

用于在 node_secret_invalid 错误时获取新的节点密钥
"""

import requests
import json
from datetime import datetime, timezone

# 配置
BASE_URL = "https://evomap.ai"

NODES = [
    {
        'id': 'node_cdd0bc78f3a6d99b',
        'secret': '9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711',
        'name': '新节点'
    },
    {
        'id': 'node_67c3b8b37becd262',
        'secret': '8cad4ac975ba7408b9c96f66c2dcfd3e2cd6479e84519a976b111f459858ef86',
        'name': '旧节点'
    }
]


def rotate_secret(node_id, node_secret, node_name):
    """轮转节点密钥"""
    print(f"\n{'='*60}")
    print(f"🔄 轮转 {node_name}: {node_id}")
    print(f"{'='*60}")
    
    # 构建 Hello 请求（带 rotate_secret）
    payload = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "hello",
        "message_id": f"msg_{int(datetime.now().timestamp())}_rotate",
        "sender_id": node_id,
        "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "payload": {
            "rotate_secret": True
        }
    }
    
    headers = {
        "Authorization": f"Bearer {node_secret}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/a2a/hello",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"响应状态：{response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            new_secret = result.get("payload", {}).get("node_secret")
            
            if new_secret:
                print(f"\n✅ 获取新的 Node Secret:")
                print(f"  {new_secret}")
                return new_secret
            else:
                print(f"\n❌ 未获取到新的 Node Secret")
                print(f"响应：{json.dumps(result, indent=2)}")
                return None
        else:
            print(f"\n❌ Hello 失败：{response.status_code}")
            print(f"响应：{response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"\n❌ 异常：{e}")
        return None


def update_heartbeat_script(new_secrets):
    """更新心跳脚本中的密钥"""
    script_path = "/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/lib/node_heartbeat.py"
    
    print(f"\n📝 更新心跳脚本：{script_path}")
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新每个节点的密钥
    for i, (node, new_secret) in enumerate(zip(NODES, new_secrets)):
        if new_secret:
            old_secret = node['secret']
            content = content.replace(f"'secret': '{old_secret}'", f"'secret': '{new_secret}'")
            print(f"  ✅ {node['name']} 密钥已更新")
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 心跳脚本已更新")


def main():
    """主函数"""
    print("="*60)
    print("🔑 EvoMap Node Secret 轮转")
    print("="*60)
    
    new_secrets = []
    
    for node in NODES:
        new_secret = rotate_secret(node['id'], node['secret'], node['name'])
        new_secrets.append(new_secret)
        
        if new_secret:
            # 等待一下避免速率限制
            print(f"  ⏳ 等待 5 秒...")
            import time
            time.sleep(5)
    
    # 更新心跳脚本
    if any(new_secrets):
        update_heartbeat_script(new_secrets)
    
    print(f"\n{'='*60}")
    print("📊 轮转结果")
    print(f"{'='*60}")
    for node, new_secret in zip(NODES, new_secrets):
        status = "✅ 成功" if new_secret else "❌ 失败"
        print(f"  {node['name']}: {status}")
        if new_secret:
            print(f"    新密钥：{new_secret[:16]}...{new_secret[-16:]}")
    
    print(f"\n💡 提示：请运行心跳脚本验证新密钥是否有效")
    print(f"   python3 lib/node_heartbeat.py")


if __name__ == '__main__':
    main()

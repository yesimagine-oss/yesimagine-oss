#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
輪轉 Node Secret 並發布第一個 Capsule
"""

import requests
from datetime import datetime

# 配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf"
BASE_URL = "https://evomap.ai"

print("=" * 60)
print("🔄 輪轉 Node Secret")
print("=" * 60)

# 執行帶 rotate_secret 的 Hello
hello_payload = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "hello",
    "message_id": f"msg_{int(datetime.now().timestamp())}_rotate",
    "sender_id": NODE_ID,
    "timestamp": datetime.utcnow().isoformat() + 'Z',
    "payload": {
        "rotate_secret": True
    }
}

headers = {
    "Authorization": f"Bearer {NODE_SECRET}",
    "Content-Type": "application/json"
}

print("\n📡 發送 Hello 請求（帶 rotate_secret）...")

try:
    response = requests.post(
        f"{BASE_URL}/a2a/hello",
        headers=headers,
        json=hello_payload,
        timeout=30
    )
    
    print(f"響應狀態：{response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        new_secret = result.get("payload", {}).get("node_secret")
        
        if new_secret:
            print(f"\n✅ 獲取新的 Node Secret:")
            print(f"  {new_secret}")
            
            # 保存到文件
            with open("/tmp/new_node_secret.txt", "w") as f:
                f.write(new_secret)
            
            print(f"\n💾 已保存到：/tmp/new_node_secret.txt")
            
            # 更新發布腳本
            print(f"\n📝 更新發布腳本...")
            with open("publish-first-capsule.py", "r") as f:
                content = f.read()
            
            # 替換 Node Secret
            old_secret_line = f'NODE_SECRET = "{NODE_SECRET}"'
            new_secret_line = f'NODE_SECRET = "{new_secret}"'
            content = content.replace(old_secret_line, new_secret_line)
            
            with open("publish-first-capsule.py", "w") as f:
                f.write(content)
            
            print(f"✅ 發布腳本已更新")
            
            # 現在發布 Capsule
            print(f"\n🚀 立即發布 Capsule...")
            import subprocess
            subprocess.run(["python3", "publish-first-capsule.py"], cwd=".")
            
        else:
            print(f"\n❌ 未獲取到新的 Node Secret")
            print(f"響應：{result}")
    else:
        print(f"\n❌ Hello 失敗：{response.status_code}")
        print(f"響應：{response.text[:500]}")
        
except Exception as e:
    print(f"\n❌ 異常：{e}")

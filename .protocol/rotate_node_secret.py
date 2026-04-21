#!/usr/bin/env python3
"""
🔧 獲取新的 Node Secret - 通過 /a2a/hello endpoint
"""

import json
import requests
import secrets
from datetime import datetime, timezone

# 配置
NODE_ID = "node_cdd0bc78f3a6d99b"
HUB_URL = "https://evomap.ai"

def generate_message_id():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    random_hex = secrets.token_hex(4)
    return f"msg_{timestamp}_{random_hex}"

def get_utc_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def hello_with_rotate():
    """發送 hello 請求並旋轉 secret"""
    url = f"{HUB_URL}/a2a/hello"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    envelope = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "hello",
        "message_id": generate_message_id(),
        "sender_id": NODE_ID,
        "timestamp": get_utc_timestamp(),
        "payload": {
            "rotate_secret": True
        }
    }
    
    print(f"📤 發送 hello 請求到 {url}...")
    print(f"📤 Payload: {json.dumps(envelope, indent=2)}")
    
    response = requests.post(url, json=envelope, headers=headers)
    
    print(f"\n📥 狀態碼：{response.status_code}")
    print(f"📥 響應：{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        data = response.json()
        node_secret = data.get('payload', {}).get('node_secret')
        if node_secret:
            print(f"\n✅ 新 Node Secret: {node_secret}")
            return node_secret
        else:
            print("\n⚠️  響應中沒有 node_secret")
            return None
    else:
        print(f"\n❌ 請求失敗")
        return None

def update_secret_file(secret):
    """更新 evomap-account.md 文件"""
    account_file = "/home/admin/.openclaw/workspace/evomap-account.md"
    
    with open(account_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替換舊的 secret
    import re
    old_secret_pattern = r'Node Secret\*\*: `[a-f0-9]+`'
    new_content = re.sub(
        old_secret_pattern,
        f'Node Secret**: `{secret}`',
        content
    )
    
    with open(account_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\n✅ 已更新 evomap-account.md")

def update_scripts(secret):
    """更新所有腳本中的 node_secret"""
    import subprocess
    result = subprocess.run(
        f'grep -rl "61f082875bfd31aead6512ef3d4fe09b050a1cce913c8ebb5b66b4e835693c86" /home/admin/.openclaw/workspace/.protocol/ 2>/dev/null | xargs -I{{}} sed -i "s/61f082875bfd31aead6512ef3d4fe09b050a1cce913c8ebb5b66b4e835693c86/{secret}/g" {{}}',
        shell=True,
        capture_output=True,
        text=True
    )
    print(f"✅ 已更新腳本中的 node_secret")

if __name__ == "__main__":
    print("=" * 60)
    print("🔑 獲取新的 Node Secret")
    print("=" * 60)
    
    new_secret = hello_with_rotate()
    
    if new_secret:
        update_secret_file(new_secret)
        update_scripts(new_secret)
        
        print("\n" + "=" * 60)
        print("✅ Node Secret 更新完成！")
        print("=" * 60)
        print(f"\n新 Secret: {new_secret}")
        print("\n請在後續發布中使用此 Secret")
    else:
        print("\n" + "=" * 60)
        print("❌ 獲取 Node Secret 失敗")
        print("=" * 60)

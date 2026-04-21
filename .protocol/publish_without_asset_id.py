#!/usr/bin/env python3
"""
🚀 發布時不包含 asset_id - 讓 Hub 計算
"""

import json
import requests
import secrets
from datetime import datetime, timezone

# 配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "26bc1b176e2d9a482078f3c47b7b46bed695b96b7342552e3dc71141a4e0de19"
HUB_URL = "https://evomap.ai"

def generate_message_id():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    random_hex = secrets.token_hex(4)
    return f"msg_{timestamp}_{random_hex}"

def get_utc_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

def main():
    print("=" * 60)
    print("🚀 發布時不包含 asset_id - 讓 Hub 計算")
    print("=" * 60)
    
    # 讀取成功的模板
    with open('/home/admin/.openclaw/workspace/evomap_hello_bundle_1775503401.json', 'r') as f:
        template = json.load(f)
    
    # 移除所有 asset_id 字段
    for asset in template['assets']:
        asset.pop('asset_id', None)
    
    print("\n📦 已移除 asset_id 字段")
    print(f"  Gene 字段：{list(template['assets'][0].keys())}")
    print(f"  Capsule 字段：{list(template['assets'][1].keys())}")
    
    # 創建協議信封
    envelope = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": generate_message_id(),
        "sender_id": NODE_ID,
        "timestamp": get_utc_timestamp(),
        "payload": template
    }
    
    # 發送發布請求
    url = f"{HUB_URL}/a2a/publish"
    headers = {
        "Content-Type": "application/json",
        "X-Node-ID": NODE_ID,
        "Authorization": f"Bearer {NODE_SECRET}"
    }
    
    print(f"\n📤 發送發布請求...")
    response = requests.post(url, json=envelope, headers=headers)
    
    print(f"\n📥 狀態碼：{response.status_code}")
    print(f"📥 響應：{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        print("\n" + "=" * 60)
        print("✅ 發布成功！")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("⚠️  發布失敗")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断 Hello 响应
"""

import requests
import json
from datetime import datetime
import os

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

NODE_ID = "node_67c3b8b37becd262"
BASE_URL = "https://evomap.ai"

hello_request = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "hello",
    "message_id": f"msg_{int(datetime.utcnow().timestamp() * 1000)}_{os.urandom(4).hex()}",
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "payload": {}
}

print("📋 发送 Hello 请求...")
print(f"请求内容:\n{json.dumps(hello_request, indent=2)}\n")

response = requests.post(f"{BASE_URL}/a2a/hello", json=hello_request, timeout=30)
result = response.json()

print(f"HTTP 状态码：{response.status_code}")
print(f"\n完整响应:\n{json.dumps(result, indent=2, ensure_ascii=False)}")

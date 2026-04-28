#!/usr/bin/env python3
"""Hub 积分检查 - 被 health-check.sh 调用"""
import sys, json, urllib.request, time

NODE_SECRET = "41d3e627a4fee83351274562ff11cec398885bdf023b1fa9da19cf690926010c"
NODE_ID = "node_b83d6e6008dce32f"
BASE_URL = "https://evomap.ai"

ts = int(time.time())
envelope = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "hello",
    "message_id": f"msg_{ts}_health",
    "sender_id": NODE_ID,
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "payload": {
        "capabilities": {
            "evolver": {
                "version": "1.69.21",
                "installed_at": "/usr/lib/node_modules/@evomap/evolver",
                "binary": "/usr/bin/evolver"
            }
        },
        "env_fingerprint": {
            "device_id": "iZm5ei3ekpe8wbnvf7snni",
            "node_version": "v24.14.0",
            "platform": "linux",
            "arch": "x64",
            "os_release": "5.10.134",
            "hostname": "iZm5ei3ekpe8wbnvf7snni",
            "evolver_version": "1.69.21",
            "client": "openclaw",
            "client_version": "2026.3.3",
            "region": "cn-shanghai",
            "cwd": "/home/admin/.openclaw/workspace",
            "container": False,
            "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    }
}

req = urllib.request.Request(
    f"{BASE_URL}/a2a/hello",
    data=json.dumps(envelope).encode(),
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {NODE_SECRET}"},
    method="POST"
)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode())
        credits = result.get('payload', {}).get('credit_balance', 'N/A')
        print(credits)
except Exception as e:
    print(f"ERROR:{e}")

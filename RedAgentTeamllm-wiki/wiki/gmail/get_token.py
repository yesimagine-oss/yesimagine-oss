#!/usr/bin/env python3
import requests
import json
import os

# 配置
CREDENTIALS_PATH = 'credentials.json'
TOKEN_PATH = 'token.json'
AUTH_CODE = '4/0AfrIepC7-TMepQWhLBgXu4s7AgcuQtf2BRbueJ74aXiy9AvEhwc2b9oIZ8wSKDtahV4yiQ'

# 代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

# 加载凭据
with open(CREDENTIALS_PATH, 'r') as f:
    credentials = json.load(f)

client_id = credentials['installed']['client_id']
client_secret = credentials['installed']['client_secret']

print('🔐 正在获取 Token...')
print(f'使用代理：{proxies["https"]}')
print()

try:
    response = requests.post(
        'https://oauth2.googleapis.com/token',
        data={
            'code': AUTH_CODE,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': 'http://localhost',
            'grant_type': 'authorization_code',
        },
        proxies=proxies,
        timeout=60
    )
    
    if response.status_code == 200:
        tokens = response.json()
        with open(TOKEN_PATH, 'w') as f:
            json.dump(tokens, f, indent=2)
        
        print('✅ Gmail API 授权成功！')
        print(f'📍 Token 已保存到：{TOKEN_PATH}')
        print()
        print('Token 内容:')
        print(json.dumps(tokens, indent=2))
    else:
        print(f'❌ 授权失败：{response.status_code}')
        print(response.text)
        
except Exception as e:
    print(f'❌ 错误：{e}')

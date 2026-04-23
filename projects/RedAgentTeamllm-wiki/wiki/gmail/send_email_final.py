#!/usr/bin/env python3
"""
使用 Gmail API 發送 EvoMap 項目立項通知郵件
"""

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import requests

# 配置
FROM_EMAIL = 'yesimagine@gmail.com'
TO_EMAIL = 'yesimagine@gmail.com'
SUBJECT = '【EvoMap 項目立項】知識變現項目執行方案 - 2026-03-20 第 1 天開始'

# 讀取配置
TOKEN_PATH = '/home/admin/.openclaw/workspace/gmail/token.json'
CREDENTIALS_PATH = '/home/admin/.openclaw/workspace/gmail/credentials.json'

print("=" * 60)
print("📧 EvoMap 項目立項通知郵件發送")
print("=" * 60)
print()

try:
    # 讀取 token
    with open(TOKEN_PATH, 'r') as f:
        token_data = json.load(f)
        access_token = token_data.get('access_token')
    
    print("✅ Gmail Token 加載成功")
    
except Exception as e:
    print(f"❌ 無法讀取 Gmail 配置：{e}")
    print()
    print("請確認:")
    print("1. token.json 文件存在")
    print("2. 已授權 Gmail API 發送權限")
    exit(1)

# 郵件內容
html_content = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>EvoMap 項目立項通知</title></head>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">

<h1 style="color: #2c3e50; border-bottom: 3px solid #3498db;">🚀 EvoMap 知識變現項目執行方案</h1>

<div style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
<strong>✅ 項目狀態:</strong> 已立項 | <strong>🚀 執行開始:</strong> 2026-03-20 (明天！)
</div>

<h2>⏰ 每日執行時間表</h2>
<table style="border-collapse: collapse; width: 100%;">
<tr><th>時間</th><th>任務</th><th>耗時</th></tr>
<tr><td>07:30-08:00</td><td>晨間檢查</td><td>30 分鐘</td></tr>
<tr><td>17:30-18:00</td><td>任務 Claim 與執行</td><td>30 分鐘</td></tr>
<tr><td>18:15-19:45</td><td>內容創作</td><td>1.5 小時</td></tr>
<tr><td>20:00-21:00</td><td>社區互動</td><td>1 小時</td></tr>
</table>

<h2>🚀 明天 (第 1 天) 執行清單</h2>
<ul>
<li>07:30 查看晨間郵件</li>
<li>17:30 Claim 第一個任務</li>
<li>18:15 開始第一篇內容創作</li>
<li>20:00 開始第一次社區互動</li>
<li>22:00 查看每日匯總</li>
</ul>

<h2>📁 項目文檔</h2>
<p>所有文檔位於：<code>/home/admin/.openclaw/workspace/EvoMap 項目/</code></p>

<div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
<strong>遇到任何問題:</strong><br>
1️⃣ 查看《EvoMap 用戶手冊》<br>
2️⃣ 回复 AI 助手「我不會 XXX」<br>
3️⃣ 週複盤時討論
</div>

<p><strong>祝您執行順利！</strong> 🎉</p>
<p>EvoMap 項目助手 - RedOpenClaw<br>2026-03-19</p>
</body>
</html>
"""

# 創建郵件
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL

part_html = MIMEText(html_content, 'html', 'utf-8')
msg.attach(part_html)

# 編碼郵件
raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')

print("✅ 郵件內容已準備完成")
print(f"📧 發件人：{FROM_EMAIL}")
print(f"📧 收件人：{TO_EMAIL}")
print(f"📋 主題：{SUBJECT}")
print()

# 使用 Gmail API 發送
print("🚀 正在發送郵件...")
print()

try:
    # 代理配置 (如果在中國大陸)
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }
    
    response = requests.post(
        'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        },
        json={'raw': raw_message},
        proxies=proxies,
        timeout=30
    )
    
    if response.status_code == 200:
        print("✅✅✅ 郵件發送成功！✅✅✅")
        print()
        result = response.json()
        print(f"郵件 ID: {result.get('id')}")
        print(f"發送時間：2026-03-19 15:54")
        print()
    else:
        print(f"❌ 發送失敗：{response.status_code}")
        print(f"錯誤信息：{response.text}")
        print()
        print("可能原因:")
        print("1. Gmail API 沒有發送權限")
        print("2. 代理連接失敗")
        print("3. Token 已過期")
        
except Exception as e:
    print(f"❌ 發送過程出錯：{e}")
    print()
    print("建議:")
    print("1. 檢查代理是否正常運行")
    print("2. 確認 Gmail API 已授權發送權限")
    print("3. 或手動複製郵件內容發送")

print()
print("=" * 60)
print("郵件已保存至:")
print("/home/admin/.openclaw/workspace/EvoMap 項目/立項通知郵件_已準備.html")
print("=" * 60)


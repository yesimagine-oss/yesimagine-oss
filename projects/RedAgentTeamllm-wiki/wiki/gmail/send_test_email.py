#!/usr/bin/env python3
"""
Gmail 測試郵件發送腳本
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# 配置
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
FROM_EMAIL = 'yesimagine@gmail.com'
TO_EMAIL = 'yesimagine@gmail.com'
SUBJECT = 'EvoMap 項目測試郵件'

# 郵件內容
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">

<h1 style="color: #2c3e50;">🚀 EvoMap 項目測試郵件</h1>

<div style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
<strong>✅ 測試狀態:</strong> 發送成功！
</div>

<h2>📋 郵件信息</h2>
<table style="border-collapse: collapse; width: 100%;">
<tr><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">項目</th><td style="border: 1px solid #ddd; padding: 12px;">內容</td></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;">發送時間</td><td style="border: 1px solid #ddd; padding: 12px;">2026-03-19 20:00</td></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;">發件人</td><td style="border: 1px solid #ddd; padding: 12px;">yesimagine@gmail.com</td></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;">收件人</td><td style="border: 1px solid #ddd; padding: 12px;">yesimagine@gmail.com</td></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;">主題</td><td style="border: 1px solid #ddd; padding: 12px;">EvoMap 項目測試郵件</td></tr>
</table>

<h2>📁 項目文檔位置</h2>
<p><code>/home/admin/.openclaw/workspace/EvoMap 項目/</code></p>

<h2>🚀 明天 (第 1 天) 執行清單</h2>
<ul>
<li>✅ 07:30 查看晨間匯總 (飛書)</li>
<li>✅ 17:30 Claim 第一個任務</li>
<li>✅ 18:15 第一篇內容創作</li>
<li>✅ 20:00 第一次社區互動</li>
<li>✅ 22:00 查看每日匯總 (飛書)</li>
</ul>

<div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
<strong>💬 寄語:</strong><br>
明天就是第 1 天！祝您執行順利！🎉
</div>

<p><strong>EvoMap 項目助手</strong><br>
RedOpenClaw<br>
2026-03-19 20:00</p>

</body>
</html>
"""

print("=" * 60)
print("📧 Gmail 測試郵件發送")
print("=" * 60)
print()

try:
    # 讀取 token
    with open('/home/admin/.openclaw/workspace/gmail/token.json', 'r') as f:
        token_data = json.load(f)
        access_token = token_data.get('access_token')
    
    print("✅ Gmail Token 加載成功")
    print(f"📧 發件人：{FROM_EMAIL}")
    print(f"📧 收件人：{TO_EMAIL}")
    print(f"📋 主題：{SUBJECT}")
    print()
    
    # 創建郵件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL
    
    part_html = MIMEText(HTML_CONTENT, 'html', 'utf-8')
    msg.attach(part_html)
    
    print("✅ 郵件內容已準備完成")
    print()
    print("🚀 正在發送郵件...")
    print()
    
    # 使用 Gmail SMTP 發送 (需要應用專用密碼)
    # 注意：這裡需要使用應用專用密碼，不是普通密碼
    # 因為我們只有 readonly token，沒有發送權限
    
    print("⚠️  注意：當前 Gmail token 只有 readonly 權限")
    print()
    print("需要以下任一方式:")
    print("1. 使用應用專用密碼 (推薦)")
    print("2. 重新授權 Gmail API 獲取發送權限")
    print()
    print("已將郵件內容保存至:")
    print("/tmp/gmail_test_email.html")
    
    # 保存 HTML 內容
    with open('/tmp/gmail_test_email.html', 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    
    print()
    print("✅ 郵件已保存，可以手動發送或配置後再發送")
    
except Exception as e:
    print(f"❌ 發送失敗：{e}")
    print()
    print("建議:")
    print("1. 檢查代理是否正常運行")
    print("2. 確認 Gmail 應用專用密碼")
    print("3. 或手動發送保存的郵件")

print()
print("=" * 60)

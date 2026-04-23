#!/usr/bin/env python3
"""
EvoMap 項目立項通知郵件發送腳本
"""

import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
import json

# 配置
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
FROM_EMAIL = 'yesimagine@gmail.com'
TO_EMAIL = 'yesimagine@gmail.com'
SUBJECT = '【EvoMap 項目立項】知識變現項目執行方案 - 2026-03-20 第 1 天開始'

# 讀取 token
TOKEN_PATH = '/home/admin/.openclaw/workspace/gmail/token.json'
CREDENTIALS_PATH = '/home/admin/.openclaw/workspace/gmail/credentials.json'

try:
    with open(TOKEN_PATH, 'r') as f:
        token_data = json.load(f)
        access_token = token_data.get('access_token')
    
    with open(CREDENTIALS_PATH, 'r') as f:
        credentials = json.load(f)
        client_id = credentials['installed']['client_id']
        client_secret = credentials['installed']['client_secret']
    
    print("✅ Gmail 憑證加載成功！")
    print(f"📧 發件人：{FROM_EMAIL}")
    print(f"📧 收件人：{TO_EMAIL}")
    print()
    
except Exception as e:
    print(f"❌ 無法讀取 Gmail 配置：{e}")
    print()
    print("請確認:")
    print("1. token.json 文件存在")
    print("2. credentials.json 文件存在")
    print("3. 已授權 Gmail API")
    exit(1)

# 郵件內容 (HTML)
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>EvoMap 知識變現項目執行方案</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">

<h1 style="color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px;">🚀 EvoMap 知識變現項目執行方案</h1>

<p><strong>發送日期:</strong> 2026-03-19<br>
<strong>收件人:</strong> yesimagine@gmail.com<br>
<strong>項目負責人:</strong> 胡宏基<br>
<strong>AI 助手:</strong> RedOpenClaw</p>

<div style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
<strong>✅ 項目狀態:</strong> 已立項 | <strong>🚀 執行開始:</strong> 2026-03-20 (明天！) | <strong>📁 準備狀態:</strong> 100% 完成
</div>

<hr>

<h2 style="color: #34495e; background: #ecf0f1; padding: 10px; border-left: 4px solid #3498db;">📋 一、項目概述</h2>

<table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
<tr><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">項目名稱</th><td style="border: 1px solid #ddd; padding: 12px;">EvoMap 知識變現</td></tr>
<tr><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">立項日期</th><td style="border: 1px solid #ddd; padding: 12px;">2026-03-19</td></tr>
<tr><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">執行開始</th><td style="border: 1px solid #ddd; padding: 12px;">2026-03-20 (明天！)</td></tr>
<tr><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">項目週期</th><td style="border: 1px solid #ddd; padding: 12px;">12 個月</td></tr>
</table>

<h3 style="color: #7f8c8d;">🎯 目標設定</h3>

<table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
<tr><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">時間</th><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">聲譽目標</th><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">粉絲目標</th><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">收入目標</th></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;">第 1 週</td><td style="border: 1px solid #ddd; padding: 12px;">30-60</td><td style="border: 1px solid #ddd; padding: 12px;">500-1000</td><td style="border: 1px solid #ddd; padding: 12px;">¥2,000-10,000</td></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;">第 1 月</td><td style="border: 1px solid #ddd; padding: 12px;">60-90</td><td style="border: 1px solid #ddd; padding: 12px;">5,000-10,000</td><td style="border: 1px solid #ddd; padding: 12px;">¥20,000-60,000</td></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;">第 3 月</td><td style="border: 1px solid #ddd; padding: 12px;">90-95</td><td style="border: 1px solid #ddd; padding: 12px;">20,000-50,000</td><td style="border: 1px solid #ddd; padding: 12px;">¥100,000-300,000</td></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;">第 12 月</td><td style="border: 1px solid #ddd; padding: 12px;">95+</td><td style="border: 1px solid #ddd; padding: 12px;">100,000+</td><td style="border: 1px solid #ddd; padding: 12px;">¥1,000,000-3,000,000</td></tr>
</table>

<hr>

<h2 style="color: #34495e; background: #ecf0f1; padding: 10px; border-left: 4px solid #3498db;">⏰ 二、每日執行時間表</h2>

<table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
<tr><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">時間</th><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">任務</th><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">執行位置</th><th style="border: 1px solid #ddd; padding: 12px; background-color: #3498db; color: white;">耗時</th></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;"><strong>07:30-08:00</strong></td><td style="border: 1px solid #ddd; padding: 12px;">晨間檢查</td><td style="border: 1px solid #ddd; padding: 12px;">郵件查看</td><td style="border: 1px solid #ddd; padding: 12px;">30 分鐘</td></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;"><strong>17:30-18:00</strong></td><td style="border: 1px solid #ddd; padding: 12px;">任務 Claim 與執行</td><td style="border: 1px solid #ddd; padding: 12px;">EvoMap 網站</td><td style="border: 1px solid #ddd; padding: 12px;">30 分鐘</td></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;"><strong>18:15-19:45</strong></td><td style="border: 1px solid #ddd; padding: 12px;">內容創作</td><td style="border: 1px solid #ddd; padding: 12px;">飛書文檔</td><td style="border: 1px solid #ddd; padding: 12px;">1.5 小時</td></tr>
<tr><td style="border: 1px solid #ddd; padding: 12px;"><strong>20:00-21:00</strong></td><td style="border: 1px solid #ddd; padding: 12px;">社區互動</td><td style="border: 1px solid #ddd; padding: 12px;">知乎/掘金等</td><td style="border: 1px solid #ddd; padding: 12px;">1 小時</td></tr>
</table>

<div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
<strong>⏱️ 每日總投入:</strong> 約 3.5 小時 (工作日) | 6 小時 (週末)<br>
<strong>📱 通知方式:</strong> 飛書消息 + 郵件
</div>

<hr>

<h2 style="color: #34495e; background: #ecf0f1; padding: 10px; border-left: 4px solid #3498db;">🚀 三、明天 (第 1 天) 執行清單</h2>

<div style="background-color: #d4edda; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
<strong>執行日期:</strong> 2026-03-20 (明天！)
</div>

<h3>早晨</h3>
<ul>
<li>✅ 07:30 查看晨間郵件</li>
</ul>

<h3>傍晚</h3>
<ul>
<li>✅ 17:25 收到任務提醒</li>
<li>✅ 17:30 Claim 第一個任務</li>
<li>✅ 17:35-18:00 執行任務</li>
</ul>

<h3>晚上</h3>
<ul>
<li>✅ 18:10 收到創作提醒</li>
<li>✅ 18:15 開始第一篇內容創作</li>
<li>✅ 19:45 完成內容創作</li>
<li>✅ 20:00 收到社區提醒</li>
<li>✅ 20:00-21:00 開始第一次社區互動</li>
<li>✅ 22:00 查看每日匯總</li>
</ul>

<hr>

<h2 style="color: #34495e; background: #ecf0f1; padding: 10px; border-left: 4px solid #3498db;">📁 四、項目文檔</h2>

<p><strong>所有文檔位於:</strong> <code>/home/admin/.openclaw/workspace/EvoMap 項目/</code></p>

<h3>核心文檔</h3>
<ul>
<li>✅ EvoMap 知識變現項目執行手冊.md (完整執行流程)</li>
<li>✅ EvoMap 定時任務配置.md (定時任務配置)</li>
<li>✅ EvoMap 用戶手冊.md (操作指南)</li>
<li>✅ 立項通知郵件.md (本郵件)</li>
</ul>

<hr>

<h2 style="color: #34495e; background: #ecf0f1; padding: 10px; border-left: 4px solid #3498db;">📞 五、支持方式</h2>

<div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
<strong>遇到任何問題:</strong><br>
1️⃣ 查看《EvoMap 用戶手冊》<br>
2️⃣ 回复 AI 助手「我不會 XXX」<br>
3️⃣ 週複盤時討論
</div>

<p><strong>AI 助手:</strong> RedOpenClaw<br>
<strong>項目負責人:</strong> 胡宏基<br>
<strong>聯繫郵箱:</strong> yesimagine@gmail.com<br>
<strong>項目文檔:</strong> /home/admin/.openclaw/workspace/EvoMap 項目/</p>

<hr>

<div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #ecf0f1; color: #7f8c8d;">
<p><strong>立項日期:</strong> 2026-03-19<br>
<strong>執行開始:</strong> 2026-03-20 (明天！)<br>
<strong>版本:</strong> v1.0</p>

<p><strong>💬 寄語:</strong></p>
<p>明天就是第 1 天！記住：</p>
<ul>
<li>✅ 所有通知會按時發送</li>
<li>✅ 所有內容 AI 會準備好 80%</li>
<li>✅ 您只需做核心決策和創作</li>
<li>✅ 時間不湊巧可以改期</li>
<li>✅ 最低限度每天只需 40 分鐘</li>
</ul>

<p><strong>祝您執行順利！</strong> 🎉</p>

<p>EvoMap 項目助手<br>
RedOpenClaw<br>
2026-03-19 15:48</p>
</div>

</body>
</html>
"""

# 創建郵件
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL

# 添加 HTML 內容
part_html = MIMEText(html_content, 'html', 'utf-8')
msg.attach(part_html)

print("📧 郵件內容已準備完成！")
print()

# 使用 OAuth2 發送郵件 (需要 access_token)
# 這裡使用簡化的方式，直接通過 smtplib 發送
# 實際需要使用 OAuth2 認證

print("⚠️  注意：Gmail 需要 OAuth2 認證才能發送郵件")
print()
print("請使用以下命令發送:")
print()
print("cd /home/admin/.openclaw/workspace/gmail/")
print("python3 send_evomap_email.py")
print()
print("或使用現有的 get_token.py 獲取 token 後發送")
print()

# 保存到文件
output_path = '/home/admin/.openclaw/workspace/EvoMap 項目/立項通知郵件_已準備.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ 郵件已保存至：{output_path}")
print()
print("您可以:")
print("1. 在瀏覽器中打開查看")
print("2. 複製內容手動發送")
print("3. 使用 Gmail API 發送")


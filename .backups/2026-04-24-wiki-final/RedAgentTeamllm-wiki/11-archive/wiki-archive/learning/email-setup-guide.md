---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 郵件檢查功能配置指南
- api
- guide
- setup
title: Email Setup Guide
type: general
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# 📧 郵件檢查功能配置指南

**創建時間**: 2026-03-16  
**狀態**: 配置中

---

## 🎯 當前狀態

| 郵件服務 | 狀態 | 說明 |
|----------|------|------|
| **騰訊企業郵** (red@unvw.com) | ⚠️ 需更新密碼 | IMAP 登錄失敗 |
| **Gmail** (yesimagine@gmail.com) | ❌ OAuth 未完成 | 授權流程未完成 |
| **飛書郵箱** | ⚠️ API 限制 | 需要額外權限 |

---

## ✅ 方案選擇

### 方案 1：更新騰訊企業郵授權碼（推薦）

**優點**：
- ✅ 立即可用
- ✅ 功能完整
- ✅ 配置簡單

**步驟**：

#### 1. 獲取授權碼

```
1. 訪問騰訊企業郵網頁版
   https://exmail.qq.com

2. 登錄 red@unvw.com

3. 進入設置 → 賬戶

4. 開啟 IMAP/SMTP 服務

5. 生成授權碼（不是登錄密碼）

6. 複製授權碼
```

#### 2. 更新配置

```bash
# 編輯配置文件
vim /home/admin/.openclaw/workspace/email-monitor/check-mail.js

# 修改第 18 行
const IMAP_CONFIG = {
  user: 'red@unvw.com',
  password: '您的授權碼',  // 替換這裡
  host: 'imap.exmail.qq.com',
  port: 993,
  tls: true,
};
```

#### 3. 測試

```bash
cd /home/admin/.openclaw/workspace/email-monitor
node check-mail.js
```

---

### 方案 2：完成 Gmail OAuth 配置

**優點**：
- ✅ 全球訪問
- ✅ 功能強大
- ✅ 與 gog 集成

**步驟**：

#### 1. 在本地 Mac 上完成授權

```bash
# Mac 上安裝 gog
brew install steipete/tap/gogcli

# 配置 credentials
gog auth credentials ~/Downloads/client_secret_xxx.json

# 授權賬戶
gog auth add yesimagine@gmail.com --services gmail

# 瀏覽器打開授權 URL
# 完成授權
```

#### 2. 複製 token 到服務器

```bash
# Mac 上找到 token 文件
ls ~/Library/Application\ Support/gogcli/

# 複製到服務器
scp ~/Library/Application\ Support/gogcli/tokens.json \
  admin@47.104.30.181:~/.config/gogcli/tokens.json
```

#### 3. 測試

```bash
# 服務器上測試
export https_proxy=http://127.0.0.1:7890
gog gmail list --max 5
```

---

### 方案 3：使用簡單 IMAP 腳本（快速測試）

**創建測試腳本**：

```bash
cat > /tmp/test-imap.py << 'EOF'
#!/usr/bin/env python3
import imaplib
import email

# 配置
IMAP_SERVER = 'imap.exmail.qq.com'
IMAP_PORT = 993
EMAIL = 'red@unvw.com'
PASSWORD = '您的授權碼'  # 替換為授權碼

# 連接
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

# 搜索未讀郵件
status, messages = mail.search(None, 'UNSEEN')
email_ids = messages[0].split()

print(f"發現 {len(email_ids)} 封未讀郵件")

# 顯示最新 5 封
for eid in email_ids[-5:]:
    status, msg = mail.fetch(eid, '(RFC822)')
    email_msg = email.message_from_bytes(msg[0][1])
    print(f"\n主題：{email_msg['subject']}")
    print(f"發件人：{email_msg['from']}")
    print(f"時間：{email_msg['date']}")

mail.close()
mail.logout()
EOF

python3 /tmp/test-imap.py
```

---

## 🔧 立即可用的郵件通知

### 創建郵件檢查 + 飛書通知腳本

```bash
cat > /home/admin/.openclaw/workspace/tools/mail-notifier.py << 'EOF'
#!/usr/bin/env python3
"""
郵件檢查 + 飛書通知
"""

import imaplib
import email
import requests
import json
import sys

# 郵件配置
IMAP_SERVER = 'imap.exmail.qq.com'
IMAP_PORT = 993
EMAIL = 'red@unvw.com'
PASSWORD = '您的授權碼'  # 替換

# 飛書配置
APP_ID = "cli_a929676f8bf81cc7"
APP_SECRET = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"

def get_feishu_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    return resp.json()["app_access_token"]

def send_feishu_msg(token, title, content):
    url = "https://open.feishu.cn/open-apis/message/v4/send"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "chat_id": "oc_XXXXX",  # 替換為實際聊天 ID
        "msg_type": "text",
        "content": {
            "text": f"{title}\n{content}"
        }
    }
    requests.post(url, headers=headers, json=payload)

def check_mail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()
    
    if not email_ids:
        return []
    
    new_mails = []
    for eid in email_ids[-5:]:
        status, msg = mail.fetch(eid, '(RFC822)')
        email_msg = email.message_from_bytes(msg[0][1])
        new_mails.append({
            'subject': email_msg['subject'],
            'from': email_msg['from'],
            'date': email_msg['date']
        })
    
    mail.close()
    mail.logout()
    return new_mails

def main():
    try:
        mails = check_mail()
        if mails:
            token = get_feishu_token()
            for mail in mails:
                send_feishu_msg(
                    token,
                    "📬 新郵件通知",
                    f"主題：{mail['subject']}\n發件人：{mail['from']}"
                )
            print(f"✅ 發送 {len(mails)} 封郵件通知")
        else:
            print("✅ 沒有新郵件")
    except Exception as e:
        print(f"❌ 錯誤：{e}")

if __name__ == "__main__":
    main()
EOF
```

---

## 📋 配置檢查清單

### 騰訊企業郵

- [ ] 登錄網頁版郵箱
- [ ] 開啟 IMAP/SMTP 服務
- [ ] 獲取授權碼
- [ ] 更新配置文件
- [ ] 測試連接

### Gmail

- [ ] Mac 上安裝 gog
- [ ] 完成 OAuth 授權
- [ ] 複製 token 到服務器
- [ ] 測試 gog 命令

### 飛書通知

- [ ] 獲取聊天 ID
- [ ] 配置通知腳本
- [ ] 測試通知發送
- [ ] 設置定時任務

---

## 🚀 快速開始

**最簡單的方案**（推薦）：

```bash
# 1. 獲取騰訊企業郵授權碼
# 訪問 https://exmail.qq.com

# 2. 更新密碼
vim /home/admin/.openclaw/workspace/email-monitor/check-mail.js
# 修改 password 字段

# 3. 測試
cd /home/admin/.openclaw/workspace/email-monitor
node check-mail.js
```

---

## 📞 需要幫助？

請告訴我：

1. **選擇哪個方案？**
   - `方案 1` → 騰訊企業郵授權碼
   - `方案 2` → Gmail OAuth
   - `方案 3` → 簡單測試

2. **需要我協助哪步？**
   - 獲取授權碼
   - 更新配置
   - 測試連接
   - 設置通知

---

**準備好後告訴我，我會一步步指導您完成！** 📧

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[INSTALL-VALIDATOR-GUIDE]]
- [[21-user_guide_image_analysis_skill]]
- [[session-manager-ai-guide]]

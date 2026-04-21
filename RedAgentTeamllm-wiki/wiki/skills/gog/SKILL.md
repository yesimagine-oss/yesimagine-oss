---
author: steipete (via ClawHub)
description: Google 生態系統集成技能。使用 gogcli 管理 Gmail/Calendar/Drive/Contacts/Sheets/Docs。需要
  OAuth 配置。
license: MIT-0
name: gog
version: 1.0.0

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
# Gog Skill 🎮

使用 `gog` CLI 工具集成 Google 服務。

## 安裝

### 1. 安裝 gogcli (一次性)

```bash
# ✅ 已安裝！版本：v0.12.0
# 位置：~/bin/gog

# 如需重新安裝（手動下載）：
curl -sLo /tmp/gogcli.tar.gz "https://github.com/steipete/gogcli/releases/download/v0.12.0/gogcli_0.12.0_linux_amd64.tar.gz"
cd /tmp && tar -xzf gogcli.tar.gz
mkdir -p ~/bin && mv gog ~/bin/ && chmod +x ~/bin/gog

# 驗證安裝
gog version
```

### 2. OAuth 配置（一次性）

```bash
# 準備 Google Cloud credentials (client_secret.json)
# 從 Google Cloud Console 獲取：https://console.cloud.google.com/apis/credentials

# 配置 credentials
gog auth credentials /path/to/client_secret.json

# 添加賬戶並授權服務
gog auth add you@gmail.com --services gmail,calendar,drive,contacts,sheets,docs

# 查看已授權賬戶
gog auth list
```

### 3. 環境變量（可選）

```bash
# 設置默認賬戶，避免每次重複 --account
export GOG_ACCOUNT=you@gmail.com
```

## 常用命令

### 📧 Gmail

```bash
# 搜索郵件
gog gmail search 'newer_than:7d' --max 10

# 獲取郵件詳情
gog gmail get MESSAGE_ID

# 發送郵件
gog gmail send --to a@b.com --subject "Hi" --body "Hello"

# 標記為已讀
gog gmail mark --read MESSAGE_ID

# 刪除郵件
gog gmail delete MESSAGE_ID
```

### 📅 Calendar

```bash
# 查看事件
gog calendar events --from 2026-03-16 --to 2026-03-23

# 創建事件
gog calendar create --summary "會議" --start 2026-03-16T14:00:00 --end 2026-03-16T15:00:00

# 刪除事件
gog calendar delete EVENT_ID
```

### 📁 Drive

```bash
# 搜索文件
gog drive search "query" --max 10

# 下載文件
gog drive download FILE_ID --out /path/to/file

# 上傳文件
gog drive upload /path/to/file

# 刪除文件
gog drive delete FILE_ID
```

### 👥 Contacts

```bash
# 列出聯繫人
gog contacts list --max 20

# 搜索聯繫人
gog contacts search "name"

# 添加聯繫人
gog contacts create --name "Name" --email "email@example.com"
```

### 📊 Sheets

```bash
# 獲取數據
gog sheets get "Tab!A1:D10" --json

# 更新數據
gog sheets update "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED

# 追加數據
gog sheets append "Tab!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS

# 清除數據
gog sheets clear "Tab!A2:Z"

# 獲取元數據
gog sheets metadata --json
```

### 📄 Docs

```bash
# 導出文檔
gog docs export --format txt --out /tmp/doc.txt

# 查看文檔內容
gog docs cat DOC_ID
```

## 腳本化建議

```bash
# 使用 --json 輸出便於解析
gog gmail search 'is:unread' --json --max 5

# 使用 --no-input 避免交互提示
gog gmail send --to a@b.com --subject "Hi" --body "Hello" --no-input

# 設置默認賬戶
export GOG_ACCOUNT=you@gmail.com
```

## 安全注意事項

⚠️ **重要：**
- 確認後再發送郵件或創建事件
- 保護好 OAuth credentials (client_secret.json)
- 定期檢查授權的應用和權限
- 不要將 credentials 提交到版本控制

## 故障排除

### 問題：OAuth 授權失敗
```bash
# 重新授權
gog auth remove you@gmail.com
gog auth add you@gmail.com --services gmail,calendar,drive
```

### 問題：找不到命令
```bash
# 檢查安裝
which gog
# 如果沒有，重新安裝
brew install steipete/tap/gogcli
```

### 問題：權限不足
```bash
# 檢查授權的服務
gog auth list
# 重新添加需要的服務
gog auth add you@gmail.com --services gmail,calendar,drive,contacts,sheets,docs
```

## 相關資源

- GitHub: https://github.com/steipete/gog
- Google Cloud Console: https://console.cloud.google.com/
- Google API 文檔: https://developers.google.com/

---

*最後更新：2026-03-16*

## 參考

- [[Final-Skills-Status-Report]]
- [[首发帖子-Github-Skill-安装教程]]
- [[Skills-Installation-Status]]

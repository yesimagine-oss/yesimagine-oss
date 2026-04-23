---
category: llm
created_at: '2026-04-14'
tags:
- llm
- content
- collector
- cookie
- 配置總結
- guide
title: Readme Cookie Setup
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
# 📦 Content Collector - Cookie 配置總結

**當前狀態**: 萬事俱備，只欠 Cookie 🍪

---

## ✅ 已完成的工作

| 項目 | 狀態 | 位置 |
|------|------|------|
| **Docker 化** | ✅ 完成 | `Dockerfile`, `docker-compose.yml` |
| **Cookie 注入功能** | ✅ 完成 | `index.js`（已修改） |
| **Cookie 導出工具** | ✅ 完成 | `export-cookies.js` |
| **圖文教程** | ✅ 完成 | `QUICK-COOKIE-GUIDE.md` |
| **檢查腳本** | ✅ 完成 | `check-cookies.sh` |
| **服務器版指南** | ✅ 完成 | `COOKIE-GUIDE-SERVER.md` |
| **Docker 文檔** | ✅ 完成 | `DOCKER-README.md` |

---

## 🎯 你需要做的事（只需 5 分鐘）

### 步驟 1: 在本地電腦導出 Cookie

**在你的 Windows/Mac 電腦上：**

1. **安裝 Chrome 擴展**（1 分鐘）
   - 訪問 Chrome 網上應用店
   - 搜索 "EditThisCookie" 並安裝
   - 或直接訪問：https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg

2. **登錄微信公眾號**（2 分鐘）
   - 打開 https://mp.weixin.qq.com
   - 用微信掃碼或賬號密碼登錄
   - 確保能正常進入後台

3. **導出 Cookie**（1 分鐘）
   - 點擊瀏覽器右上角的 🍪 Cookie 圖標
   - 點擊 "Export" 按鈕
   - 選擇 "JSON" 格式
   - 文件會自動下載（通常是 `cookies.txt` 或 `cookies.json`）

4. **重命名文件**（30 秒）
   ```bash
   # Windows PowerShell:
   Rename-Item $env:USERPROFILE\Downloads\cookies.txt wechat-cookies.json
   
   # Mac Terminal:
   mv ~/Downloads/cookies.txt ~/Downloads/wechat-cookies.json
   ```

---

### 步驟 2: 上傳到服務器

**方法 A: 使用 SCP（推薦）**

```bash
# Windows PowerShell（替換成你的服務器 IP）:
scp $env:USERPROFILE\Downloads\wechat-cookies.json admin@你的服務器 IP:/home/admin/.openclaw/workspace/cookies/

# Mac Terminal:
scp ~/Downloads/wechat-cookies.json admin@你的服務器 IP:/home/admin/.openclaw/workspace/cookies/
```

**方法 B: 使用飛書**

1. 在本地電腦打開飛書
2. 上傳 `wechat-cookies.json` 到任意聊天
3. 在服務器上打開飛書下載
4. 移動到正確位置：
   ```bash
   mkdir -p ~/.openclaw/workspace/cookies
   mv ~/Downloads/wechat-cookies.json ~/.openclaw/workspace/cookies/
   ```

---

### 步驟 3: 驗證配置

**在服務器上執行：**

```bash
# 運行檢查腳本
cd ~/.openclaw/workspace/skills/content-collector
bash check-cookies.sh
```

腳本會自動：
- ✅ 檢查 Cookie 文件是否存在
- ✅ 驗證 JSON 格式
- ✅ 檢查關鍵 Cookie（slave_user, slave_sid）
- ✅ 設置安全權限
- ✅ 可選：測試抓取功能

---

## 📖 完整教程位置

| 教程 | 用途 | 文件 |
|------|------|------|
| **快速指南** | 5 分鐘圖文教程 | `QUICK-COOKIE-GUIDE.md` |
| **服務器版** | 詳細技術指南 | `COOKIE-GUIDE-SERVER.md` |
| **Docker 指南** | Docker 部署文檔 | `DOCKER-README.md` |

**查看教程：**
```bash
cd ~/.openclaw/workspace/skills/content-collector
cat QUICK-COOKIE-GUIDE.md
```

---

## 🚀 使用方式

### 配置完成後：

```bash
# 1. 設置環境變量
export WECHAT_COOKIES_ENABLED=true

# 2. 抓取任意微信文章
cd ~/.openclaw/workspace/skills/content-collector
node index.js "https://mp.weixin.qq.com/s/文章 ID"

# 3. 或使用 Docker
docker run --rm \
  -v ~/.openclaw/workspace/collections:/app/collections \
  -v ~/.openclaw/workspace/cookies:/root/.openclaw/workspace/cookies \
  -e WECHAT_COOKIES_ENABLED=true \
  content-collector:latest \
  node index.js "https://mp.weixin.qq.com/s/文章 ID"
```

---

## 🐛 常見問題

### Q: 文件下載後叫 `cookies.txt` 而不是 `cookies.json`？

**A:** 沒關係，內容是 JSON 格式就行。可以重命名：
```bash
mv cookies.txt wechat-cookies.json
```

### Q: 上傳後檢查還是說文件不存在？

**A:** 確認上傳路徑正確：
```bash
# 檢查文件
ls -la ~/.openclaw/workspace/cookies/

# 應該看到：
# -rw-r--r-- 1 admin admin 12345 Mar 19 17:30 wechat-cookies.json
```

### Q: Cookie 無效怎麼辦？

**A:** Cookie 有效期 7-30 天，過期後重新導出即可：
```bash
# 刪除舊 Cookie
rm ~/.openclaw/workspace/cookies/wechat-cookies.json

# 重新在本地電腦導出並上傳
```

---

## 📞 需要幫助？

如果遇到任何問題，請提供：

1. **檢查腳本輸出**：
   ```bash
   bash check-cookies.sh 2>&1
   ```

2. **Cookie 文件前 20 行**（隱藏敏感值）：
   ```bash
   cat ~/.openclaw/workspace/cookies/wechat-cookies.json | head -20
   ```

3. **錯誤信息**：
   ```bash
   export WECHAT_COOKIES_ENABLED=true
   node index.js "https://mp.weixin.qq.com/s/EAqEwRJEqqXJWBVrr9U2pw" 2>&1
   ```

---

## 🎉 完成後的效果

配置成功後，抓取微信文章就像這樣：

```
📦 開始收藏：https://mp.weixin.qq.com/s/EAqEwRJEqqXJWBVrr9U2pw
📋 內容類型：wechat
🍪 正在載入 Cookie...
🔍 找到 15/150 個微信相關 Cookie
✅ 已載入 15 個 Cookie
🚀 啟動瀏覽器抓取微信文章...
✅ 找到正文選擇器：#js_content
✅ 標題：文章真實標題
✅ 作者：作者名字
📝 轉換為 Markdown...
✅ 提取完成！正文 3500 字符，5 張圖片
💾 已保存：/home/admin/.openclaw/workspace/collections/wechat/2026-03-19-文章標題.md
📑 已更新索引

✅ 收藏成功！
```

---

**準備好了嗎？** 現在開始吧！

1. 打開你的本地電腦瀏覽器
2. 安裝 EditThisCookie 擴展
3. 登錄微信公眾號
4. 導出 Cookie
5. 上傳到服務器
6. 運行 `bash check-cookies.sh`

**5 分鐘後，微信文章抓取就能正常工作了！** 🎊

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[README]]
- [[clawbrowser-readme]]
- [[README]]

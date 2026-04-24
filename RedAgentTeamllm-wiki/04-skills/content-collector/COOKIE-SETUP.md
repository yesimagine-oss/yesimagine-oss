---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 微信
- cookie
- 注入配置指南
- setup
- openclaw
title: Cookie Setup
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
# 🍪 微信 Cookie 注入配置指南

**版本**: 1.0  
**創建**: 2026-03-19  
**用途**: 配置微信公眾號 Cookie，繞過反爬蟲驗證

---

## 📋 為什麼需要 Cookie？

微信公眾號有反爬蟲機制，直接抓取會遇到：

```
環境異常
當前環境異常，完成驗證後即可繼續訪問。
```

**解決方案：** 使用已登錄的 Cookie，讓微信認為你是真實用戶。

---

## 🔧 配置步驟

### 步驟 1: 導出 Cookie

```bash
# 進入技能目錄
cd ~/.openclaw/workspace/skills/content-collector

# 運行導出工具
node export-cookies.js
```

**會發生什麼：**
1. 自動打開瀏覽器
2. 訪問微信公眾號後台 (mp.weixin.qq.com)
3. **你手動掃碼/輸入賬號登錄**
4. 登錄完成後按回車
5. Cookie 自動保存到 `~/.openclaw/workspace/cookies/wechat-cookies.json`

**安全提示：**
- ✅ Cookie 只保存在本地
- ✅ 不會上傳到任何服務器
- ✅ 只有你能訪問
- ⚠️ 不要分享給他人

---

### 步驟 2: 啟用 Cookie

#### 本地使用

```bash
# 設置環境變量
export WECHAT_COOKIES_ENABLED=true

# 測試抓取
node index.js "https://mp.weixin.qq.com/s/xxx"
```

#### Docker 使用

```bash
# 掛載 Cookie 文件 + 啟用
docker run --rm \
  -v ~/.openclaw/workspace/collections:/app/collections \
  -v ~/.openclaw/workspace/cookies:/root/.openclaw/workspace/cookies \
  -e COLLECTIONS_DIR=/app/collections \
  -e WECHAT_COOKIES_ENABLED=true \
  -e WECHAT_COOKIES_PATH=/root/.openclaw/workspace/cookies/wechat-cookies.json \
  --network host \
  content-collector:latest \
  node index.js "https://mp.weixin.qq.com/s/xxx"
```

---

### 步驟 3: 驗證是否成功

**成功標誌：**
```
🍪 正在載入 Cookie...
🔍 找到 15/150 個微信相關 Cookie
✅ 已載入 15 個 Cookie
✅ 找到正文選擇器：#js_content
✅ 標題：文章標題
```

**失敗標誌：**
```
⚠️  Cookie 文件不存在
⚠️  Cookie 載入失敗
❌ 環境異常（還是出現這個說明 Cookie 沒生效）
```

---

## 🔄 Cookie 續期

Cookie 會過期（通常 7-30 天），過期後需要重新導出：

```bash
# 刪除舊 Cookie
rm ~/.openclaw/workspace/cookies/wechat-cookies.json

# 重新導出
node export-cookies.js
```

**過期徵兆：**
- 抓取突然失敗
- 返回「環境異常」頁面
- Cookie 文件存在但無效

---

## 🛡️ 安全建議

### 存儲安全

```bash
# 限制 Cookie 文件權限（僅所有者可讀寫）
chmod 600 ~/.openclaw/workspace/cookies/wechat-cookies.json

# 查看權限
ls -la ~/.openclaw/workspace/cookies/
```

### 使用安全

- ✅ 只在可信環境使用
- ✅ 定期更新 Cookie
- ✅ 用完可刪除
- ❌ 不要上傳到 Git
- ❌ 不要分享給他人
- ❌ 不要在公共電腦使用

### .gitignore 配置

確保 Cookie 不被提交：

```bash
# 添加到 ~/.openclaw/workspace/.gitignore
cookies/
*.json
```

---

## 🐛 故障排查

### 問題 1: Cookie 文件不存在

```bash
# 確認目錄存在
ls -la ~/.openclaw/workspace/cookies/

# 如果不存在，重新導出
node export-cookies.js
```

### 問題 2: Cookie 無效

```bash
# 檢查 Cookie 內容
cat ~/.openclaw/workspace/cookies/wechat-cookies.json | head -20

# 應該看到類似：
# [
#   {
#     "name": "slave_user",
#     "value": "Mz...（很長的字符串）",
#     "domain": ".qq.com",
#     ...
#   }
# ]
```

### 問題 3: Docker 找不到 Cookie

確保路徑正確：

```bash
# 檢查容器內路徑
docker run --rm -it \
  -v ~/.openclaw/workspace/cookies:/root/.openclaw/workspace/cookies \
  content-collector:latest \
  ls -la /root/.openclaw/workspace/cookies/
```

### 問題 4: 還是顯示「環境異常」

可能原因：
1. Cookie 已過期 → 重新導出
2. 微信風控升級 → 等待一段時間再試
3. IP 被封 → 換網絡環境
4. 賬號異常 → 檢查微信公眾號後台是否正常

---

## 📖 進階使用

### 多賬號管理

```bash
# 保存多個賬號的 Cookie
~/.openclaw/workspace/cookies/
├── wechat-cookies-account1.json
├── wechat-cookies-account2.json
└── wechat-cookies.json  # 當前使用的

# 切換賬號
cp wechat-cookies-account2.json wechat-cookies.json
```

### 自動續期提醒

創建定時任務檢查 Cookie：

```bash
# 每週日檢查 Cookie 有效性
0 9 * * 0 node ~/.openclaw/workspace/skills/content-collector/check-cookies.js
```

---

## 📞 需要幫助？

如果以上方法都無效：

1. 檢查微信公眾號後台是否能正常訪問
2. 嘗試在瀏覽器中手動訪問目標文章
3. 查看調試日誌：`export DEBUG=true`
4. 聯繫技能作者反饋問題

---

**最後更新**: 2026-03-19  
**維護者**: 麻小 🦐

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[email-setup-guide]]
- [[feishu-at-mention-setup]]
- [[QUICK-COOKIE-GUIDE]]

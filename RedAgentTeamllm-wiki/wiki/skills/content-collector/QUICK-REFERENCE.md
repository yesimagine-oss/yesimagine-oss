---
category: llm
created_at: '2026-04-14'
tags:
- llm
- cookie
- 配置
- 快速參考卡
title: Quick Reference
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
# 🍪 Cookie 配置 - 快速參考卡

**打印這張紙，跟著做只需 5 分鐘！**

---

## 📍 你在哪裡？

- [ ] **在本地電腦前**（Windows/Mac） → 繼續 ↓
- [ ] **在服務器前** → 跳過到「上傳 Cookie」

---

## 🔧 步驟 1: 安裝擴展（1 分鐘）

**Chrome/Edge:**
1. 打開：https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg
2. 點擊「添加至 Chrome」
3. 確認安裝

**Firefox:**
1. 打開：https://addons.mozilla.org/firefox/addon/cookie-quick-manager/
2. 點擊「添加到 Firefox」
3. 確認安裝

---

## 🔐 步驟 2: 登錄微信（2 分鐘）

1. 打開瀏覽器
2. 訪問：**https://mp.weixin.qq.com**
3. 用微信掃碼或輸入賬號密碼
4. 確保進入後台（看到菜單）

---

## 📥 步驟 3: 導出 Cookie（1 分鐘）

**EditThisCookie (Chrome):**
1. 點擊右上角 🍪 圖標
2. 點擊「Export」按鈕（向下箭頭）
3. 選擇「JSON」格式
4. 文件自動下載

**Cookie Quick Manager (Firefox):**
1. 按 F12 打開開發者工具
2. 找到 Cookie Quick Manager
3. 選擇所有 .qq.com 的 Cookie
4. 右鍵 → Export → JSON

---

## 📤 步驟 4: 上傳到服務器（1 分鐘）

**Windows PowerShell:**
```powershell
scp $env:USERPROFILE\Downloads\wechat-cookies.json admin@服務器 IP:/home/admin/.openclaw/workspace/cookies/
```

**Mac Terminal:**
```bash
scp ~/Downloads/wechat-cookies.json admin@服務器 IP:/home/admin/.openclaw/workspace/cookies/
```

**沒有 SCP？** 用飛書：
1. 本地電腦上傳文件到飛書
2. 服務器下載
3. 移動到：`~/.openclaw/workspace/cookies/`

---

## ✅ 步驟 5: 驗證（30 秒）

**在服務器上：**
```bash
cd ~/.openclaw/workspace/skills/content-collector
bash check-cookies.sh
```

看到 ✅ 就是成功！

---

## 🚀 開始使用

```bash
export WECHAT_COOKIES_ENABLED=true
node index.js "https://mp.weixin.qq.com/s/文章 ID"
```

---

## 📞 出問題了？

**檢查 Cookie 文件：**
```bash
cat ~/.openclaw/workspace/cookies/wechat-cookies.json | head -20
```

**應該看到：**
- JSON 格式（`[{...}]`）
- `slave_user` 和 `slave_sid`
- 至少 10 個 Cookie

**重新檢查：**
```bash
bash check-cookies.sh
```

---

## 🔒 安全提醒

- ✅ 設置權限：`chmod 600 ~/.openclaw/workspace/cookies/wechat-cookies.json`
- ❌ 不要分享給他人
- ❌ 不要上傳到 GitHub

---

## 📖 完整教程

```bash
cd ~/.openclaw/workspace/skills/content-collector
cat QUICK-COOKIE-GUIDE.md
```

---

**需要幫助？** 提供檢查腳本輸出和錯誤信息

**維護者**: 麻小 🦐 | **版本**: 1.0 | **日期**: 2026-03-19

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[feishu-quick-reference]]
- [[api-reference]]
- [[openclaw-doctor-reference]]

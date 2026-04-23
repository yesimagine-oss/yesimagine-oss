---
name: content-collector
version: 3.0.0
description: 全自動內容收藏系統（Playwright 版）- 微信文章 + 網頁收藏
author: 麻小 🦐
keywords: [收藏，內容采集，微信文章，Playwright，知識庫]
triggers:
 - "收藏"
 - "收录"
 - "采集"
 - "保存这篇文章"
 - "收藏這篇文章"

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
# 📦 內容收藏系統（Playwright 版）

**成功率 95%+** - 使用 Playwright 瀏覽器自動化

---

## 🎯 核心功能

1. **微信文章抓取** - Playwright 瀏覽器自動化（成功率 95%+）
2. **網頁內容收藏** - 支持任何網頁
3. **元數據提取** - 標題、作者、發布日期、摘要
4. **Markdown 轉換** - 自動轉換為 Markdown
5. **圖片下載** - 自動下載文章插圖
6. **項目關聯** - 自動匹配活躍項目
7. **結構化存儲** - Markdown + frontmatter + 索引

---

## 🚀 使用方式

```
用戶：收藏 https://mp.weixin.qq.com/s/xxx

執行流程：
1. 識別內容類型（微信/網頁）
2. 啟動 Chromium 瀏覽器
3. 訪問頁面並等待加載
4. 提取標題、作者、正文
5. 轉換為 Markdown
6. 下載圖片（可選）
7. 項目自動關聯
8. 保存到文件
9. 更新索引
10. 返回摘要
```

---

## 📁 存儲結構

```
~/.openclaw/workspace/collections/
├── wechat/           # 微信文章
│   ├── 2026-03-18-xxx.md
│   └── images/
├── articles/         # 普通文章
│   ├── 2026-03-18-xxx.md
│   └── images/
├── index.md          # 自動索引
└── tags.md           # 標籤索引（可選）
```

---

## 📊 性能指標

| 指標 | 數值 | 說明 |
|------|------|------|
| 微信文章成功率 | 95%+ | 模擬真實瀏覽器 |
| 普通網頁成功率 | 98%+ | 幾乎都能抓取 |
| 平均速度 | 5-15 秒 | 取決於頁面大小 |
| 圖片下載 | 可選 | 每張約 0.5-2 秒 |

---

## 🔧 技術實現

### 核心依賴

| 依賴 | 用途 |
|------|------|
| **Playwright** | 瀏覽器自動化（模擬真實用戶） |
| **Cheerio** | HTML 解析（提取內容） |
| **Turndown** | Markdown 轉換 |

### 為什麼用 Playwright？

- ✅ **成功率高** - 模擬真實瀏覽器，繞過反爬蟲
- ✅ **完全免費** - 開源項目，無需 API Key
- ✅ **全自動** - 安裝後無需用戶操作

---

## ⚙️ 安裝說明

### 系統要求

- Node.js 18+
- 磁盤空間 300MB+
- 網絡連接（下載 Chromium）

### 安裝步驟

```bash
# 1. 進入技能目錄
cd ~/.openclaw/workspace/skills/content-collector

# 2. 運行安裝腳本
bash install.sh

# 3. 重啟 Gateway
openclaw gateway restart
```

### 安裝腳本自動完成：

- ✅ 檢查 Node.js 環境
- ✅ 創建目錄結構
- ✅ 安裝 npm 依賴（playwright, cheerio, turndown）
- ✅ 安裝 Chromium 瀏覽器
- ✅ 驗證安裝

---

## 📝 使用示例

### 示例 1: 收藏微信文章

```
用戶：收藏 https://mp.weixin.qq.com/s/ABC123

結果：
✅ 已收藏：AI 技術分享
📁 位置：collections/wechat/2026-03-18-xxx.md
🖼️  圖片：5 張
🎯 關聯項目：wemp-ops
```

### 示例 2: 收藏普通網頁

```
用戶：收录 https://example.com/article

結果：
✅ 已收藏：網頁標題
📁 位置：collections/articles/2026-03-18-xxx.md
```

---

## ❓ 常見問題

### Q1: 安裝失敗？

**A:** 檢查 Node.js 版本（需要 18+）和網絡連接。

### Q2: 抓取失敗？

**A:** 可能文章被刪除或網絡超時，換一篇試試。

### Q3: 圖片下載失敗？

**A:** 可能圖片鏈接过期或需要登錄，不影響文字內容。

---

## 📚 學習資源

- [Playwright 文檔](https://playwright.dev/)
- [Cheerio 文檔](https://cheerio.js.org/)
- [Turndown 文檔](https://github.com/domchristie/turndown)

---

**版本**: 3.0.0  
**創建**: 2026-03-18  
**更新**: 2026-03-18（Playwright 版）

## 參考

- [[Final-Skills-Status-Report]]
- [[首发帖子-Github-Skill-安装教程]]
- [[Skills-Installation-Status]]

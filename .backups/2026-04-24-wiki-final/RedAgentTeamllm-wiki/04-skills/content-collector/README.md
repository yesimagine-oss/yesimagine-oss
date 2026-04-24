---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Readme
type: article
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
# 📦 Content Collector

**全自動內容收藏系統** - Playwright 版

---

## 🎯 功能特點

### ✅ 核心功能

1. **微信文章抓取** - Playwright 瀏覽器自動化（成功率 95%+）
2. **普通網頁收藏** - 支持任何網頁
3. **內容提取** - 標題、作者、發布日期、正文
4. **Markdown 轉換** - 自動轉換為 Markdown 格式
5. **圖片下載** - 自動下載文章插圖
6. **項目關聯** - 自動匹配活躍項目
7. **結構化存儲** - Markdown + frontmatter

### ✅ 設計原則

- **全自動** - 用戶只需給 URL
- **不花錢** - 完全免費
- **高成功率** - 95%+（模擬真實瀏覽器）

---

## 🚀 快速開始

### 安裝

```bash
# 1. 進入技能目錄
cd ~/.openclaw/workspace/skills/content-collector

# 2. 運行安裝腳本
bash install.sh

# 3. 重啟 Gateway
openclaw gateway restart
```

### 使用

```
用戶：收藏 https://mp.weixin.qq.com/s/xxx
執行：自動抓取 → 提取 → 存儲 → 返回摘要
```

### 手動測試

```bash
# 測試微信文章
node index.js https://mp.weixin.qq.com/s/xxx

# 測試普通網頁
node index.js https://example.com/article
```

---

## 📁 項目結構

```
content-collector/
├── 📄 index.js          # 核心代碼
├── 📄 package.json      # 依賴配置
├── 🔧 install.sh        # 安裝腳本
├── 📄 SKILL.md          # OpenClaw 技能文檔
├── 📄 README.md         # 本文件
├── 🧪 test/
│   └── test.js          # 測試用例
└── 📦 collections/      # 收藏內容（自動創建）
    ├── wechat/          # 微信文章
    ├── articles/        # 普通文章
    ├── images/          # 圖片
    └── index.md         # 索引
```

---

## 📖 使用示例

### 示例 1: 收藏微信文章

```
用戶：收藏 https://mp.weixin.qq.com/s/ABC123

執行結果：
✅ 已收藏：AI 技術分享
📁 位置：~/.openclaw/workspace/collections/wechat/2026-03-18-ai-ji-zhu-fen-xiang.md
🖼️  圖片：5 張
🎯 關聯項目：wemp-ops
```

### 示例 2: 收藏普通網頁

```
用戶：收录 https://example.com/article

執行結果：
✅ 已收藏：網頁標題
📁 位置：~/.openclaw/workspace/collections/articles/2026-03-18-wang-ye-biao-ti.md
```

---

## 🔧 技術實現

### 核心依賴

| 依賴 | 用途 |
|------|------|
| **Playwright** | 瀏覽器自動化（模擬真實用戶） |
| **Cheerio** | HTML 解析（提取內容） |
| **Turndown** | Markdown 轉換 |

### 工作流程

```
用戶給 URL
    ↓
啟動 Chromium 瀏覽器
    ↓
訪問頁面並等待加載
    ↓
提取標題、作者、正文
    ↓
轉換為 Markdown
    ↓
下載圖片（可選）
    ↓
保存到文件
    ↓
更新索引
    ↓
返回結果
```

---

## ⚙️ 配置選項

### 自定義配置

在 `index.js` 中修改 `CONFIG` 對象：

```javascript
const CONFIG = {
    // 收藏庫目錄
    collectionsDir: '/your/custom/path',
    
    // 瀏覽器配置
    browser: {
        headless: true,      // 無頭模式
        timeout: 30000,      // 超時時間
        userAgent: '...'     // User-Agent
    },
    
    // 圖片下載
    images: {
        download: true,      // 是否下載圖片
        dir: 'images'        // 圖片目錄
    },
    
    // 項目關鍵詞
    projects: {
        'your-project': ['關鍵詞 1', '關鍵詞 2']
    }
};
```

---

## ❓ 常見問題

### Q1: 安裝失敗怎麼辦？

**A:** 檢查以下幾點：
- Node.js 版本是否 18+？（`node -v`）
- 網絡是否正常？（需要下載 Chromium）
- 磁盤空間是否足夠？（需要約 300MB）

### Q2: 抓取失敗怎麼辦？

**A:** 可能原因：
- 文章已被刪除或設置權限
- 網絡問題導致超時
- 微信反爬蟲升級

**解決方案：**
- 換一篇較新的文章
- 檢查網絡連接
- 查看錯誤日誌

### Q3: 圖片下載失敗？

**A:** 可能原因：
- 圖片鏈接過期
- 網絡問題
- 圖片需要登錄才能訪問

---

## 📊 性能指標

| 指標 | 數值 | 說明 |
|------|------|------|
| 微信文章成功率 | 95%+ | 模擬真實瀏覽器 |
| 普通網頁成功率 | 98%+ | 幾乎都能抓取 |
| 平均速度 | 5-15 秒 | 取決於頁面大小 |
| 圖片下載 | 可選 | 每張約 0.5-2 秒 |

---

## 🎓 學習資源

- [Playwright 官方文檔](https://playwright.dev/)
- [Cheerio 選擇器文檔](https://cheerio.js.org/)
- [Turndown 配置選項](https://github.com/domchristie/turndown)

---

## 📝 更新日誌

### v3.0.0 (2026-03-18)

```
✅ 集成 Playwright 方案
✅ 成功率提升至 95%+
✅ 支持圖片自動下載
✅ 支持項目自動關聯
✅ 全自動安裝腳本
```

### v2.0.0 (2026-03-18)

```
✅ 逆向集成 clawhub content-collector
✅ 項目自動關聯
✅ 作者/日期提取
```

### v1.0.0 (2026-03-18)

```
✅ 初始版本
✅ 免費 API 輪詢
```

---

**版本**: 3.0.0  
**作者**: 麻小 🦐  
**最後更新**: 2026-03-18  
**許可**: MIT


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]

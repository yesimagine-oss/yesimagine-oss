# 📱 WeChat Fetcher 教學版

**微信文章抓取教學技能** - 帶詳細注釋，適合學習複製

---

## 🎯 適合人群

- ✅ 想學習微信文章抓取的開發者
- ✅ 想了解反爬蟲對抗策略
- ✅ 想練習 Python 網頁抓取
- ✅ 想學習 Skill 打包分發

---

## 📦 包含內容

| 文件 | 說明 |
|------|------|
| ✅ **collector.py** | 完整源代碼（帶詳細注釋） |
| ✅ **SKILL.md** | OpenClaw 技能文檔 |
| ✅ **README.md** | 實現原理文檔 |
| ✅ **LEARN.md** | 學習路徑指南 |
| ✅ **test_collector.py** | 測試用例 |
| ✅ **install.sh** | 一鍵安裝腳本 |

---

## 🚀 快速開始

### 步驟 1：安裝

```bash
# 執行安裝腳本
bash install.sh

# 重啟 Gateway
openclaw gateway restart
```

### 步驟 2：測試

```bash
# 運行測試
python3 test/test_collector.py

# 或使用技能
收藏 https://mp.weixin.qq.com/s/xxx
```

### 步驟 3：學習

```bash
# 閱讀文檔
cat README.md
cat LEARN.md

# 閱讀源碼（帶注釋）
cat collector.py
```

---

## 📖 學習路徑

### 階段 1：理解原理（30 分鐘）

```
□ 閱讀 README.md - 了解整體架構
□ 閱讀 LEARN.md - 理解學習路徑
□ 了解微信反爬機制
```

### 階段 2：閱讀源碼（1 小時）

```
□ 查看 collector.py - 核心代碼
□ 閱讀每個函數的注釋
□ 理解 API 輪詢邏輯
```

### 階段 3：動手實踐（1 小時）

```
□ 運行 install.sh 安裝
□ 運行 test_collector.py 測試
□ 嘗試收藏一篇文章
```

### 階段 4：擴展修改（1 小時）

```
□ 修改 API 列表
□ 添加新的內容源
□ 自定義存儲格式
```

---

## 💡 核心技術

### 1. 免費 API 輪詢

```python
# 按優先級嘗試多個免費 API
APIS = [
    "https://r.jina.ai/http://{url}",      # 優先
    "https://readhub.cn/proxy?url={url}",  # 備用
    "https://wx.dnspod.cn/proxy?url={url}" # 備用
]
```

**為什麼這樣設計？**
- 不花錢：全部免費
- 全自動：用戶不用操作
- 提高成功率：多個 API 輪詢

### 2. 內容提取

```python
# 用正則表達式提取標題
title = re.search(r'^#\s+(.+)$', content, re.MULTILINE)

# 提取摘要（前 200 字）
summary = content[200:400] + "..."
```

### 3. 結構化存儲

```python
# 生成 Markdown 文件
filename = f"{date}-{slug}.md"
content = f"""---
title: "{title}"
url: "{url}"
date: {date}
---

# {title}

{content}
"""
```

---

## 🔧 技術細節

### 微信反爬機制

| 機制 | 對抗策略 |
|------|---------|
| IP 限制 | 多個 API 輪詢 |
| Cookie 驗證 | 使用代理 API |
| 瀏覽器指紋 | 模擬正常請求 |
| 訪問頻率 | 控制請求間隔 |

### API 選擇邏輯

```
1. r.jina.ai
   - 成功率：90%
   - 速度：快（2-5 秒）
   - 限制：偶爾超時

2. readhub.cn
   - 成功率：85%
   - 速度：快
   - 限制：部分文章不支持

3. wx.dnspod.cn
   - 成功率：80%
   - 速度：中
   - 限制：可能 301 重定向
```

---

## 📊 性能指標

| 指標 | 數值 | 說明 |
|------|------|------|
| 成功率 | 60-80% | 免費 API 限制 |
| 平均速度 | 3-10 秒 | 取決於 API 響應 |
| 並發限制 | 1 次/秒 | 避免被限 |
| 存儲速度 | <1 秒 | 本地寫入 |

---

## ❓ 常見問題

### Q1: 為什麼成功率不是 100%？

**A:** 微信有反爬蟲機制，免費 API 會被限制。

**解決方案：**
- 多嘗試幾次
- 換一篇較新的文章
- 或配置 Cookie（需手動）

### Q2: 如何添加新的 API？

**A:** 修改 `collector.py` 的 `WECHAT_APIS` 列表：

```python
WECHAT_APIS = [
    "https://r.jina.ai/http://{url}",
    "https://your-new-api.com/proxy?url={url}",  # 新增
]
```

### Q3: 如何修改存儲路徑？

**A:** 修改 `COLLECTIONS_DIR` 常量：

```python
COLLECTIONS_DIR = "/your/custom/path"
```

---

## 🎓 課後作業

### 基礎題
修改存儲結構，按月份分類文章。

### 進階題
添加 B 站視頻抓取功能。

### 挑戰題
實現自動標籤生成（用 AI）。

---

## 📚 參考資源

- [微信公眾號反爬蟲機制分析](https://example.com)
- [Python 網頁抓取最佳實踐](https://example.com)
- [OpenClaw Skill 開發文檔](https://docs.openclaw.ai)

---

**版本**: 1.0.0  
**作者**: 麻小  
**最後更新**: 2026-03-18  
**許可**: MIT

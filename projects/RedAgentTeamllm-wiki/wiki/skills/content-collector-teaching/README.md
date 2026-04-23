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
# 📦 Content Collector 教學版

**全自動內容收藏系統** - 微信文章 + 網頁收藏

---

## 🎯 學習目標

完成本教程後，你將掌握：

| 知識點 | 掌握程度 |
|--------|---------|
| 微信反爬機制 | ⭐⭐⭐⭐⭐ |
| 免費 API 輪詢策略 | ⭐⭐⭐⭐⭐ |
| 內容提取技巧 | ⭐⭐⭐⭐⭐ |
| Markdown 轉換 | ⭐⭐⭐⭐⭐ |
| Skill 打包方法 | ⭐⭐⭐⭐⭐ |

---

## 📁 項目結構

```
content-collector-teaching/
├── 📄 README.md          # 本教程
├── 📄 SKILL.md           # OpenClaw 技能文檔
├── 🐍 collector.py       # 核心代碼（帶詳細注釋）
├── 🔧 install.sh         # 一鍵安裝腳本
├── 📦 requirements.txt   # Python 依賴
└── 🧪 test/
    └── test_collector.py # 測試用例
```

---

## 🚀 快速開始

### 階段 1：安裝（5 分鐘）

```bash
# 1. 執行安裝腳本
bash install.sh

# 2. 重啟 Gateway
openclaw gateway restart

# 3. 驗證安裝
openclaw skill list | grep content-collector
```

### 階段 2：測試（10 分鐘）

```bash
# 測試普通網頁收藏
收藏 https://example.com/article

# 測試微信文章收藏
收藏 https://mp.weixin.qq.com/s/xxx
```

### 階段 3：理解（30 分鐘）

閱讀 `collector.py` 源碼，理解：
- API 輪詢邏輯
- 內容提取方法
- 存儲結構設計

### 階段 4：擴展（1 小時）

根據你的需求修改：
- 添加新的內容源（B 站、知乎等）
- 自定義存儲格式
- 添加推送功能

---

## 📖 核心實現講解

### 1. 微信文章抓取（免費 API 輪詢）

```python
# 核心思路：按順序嘗試多個免費 API，直到成功
APIS = [
    "https://r.jina.ai/http://{url}",      # 優先
    "https://readhub.cn/proxy?url={url}",  # 備用 1
    "https://wx.dnspod.cn/proxy?url={url}" # 備用 2
]

def fetch_wechat(url):
    for api in APIS:
        try:
            response = requests.get(api.format(url=url))
            if response.status_code == 200 and response.text:
                return response.text  # 成功
        except:
            continue  # 失敗，嘗試下一個
    return None  # 全部失敗
```

**為什麼這樣設計？**
- ✅ 不花錢（全部免費 API）
- ✅ 全自動（用戶不用操作）
- ⚠️ 成功率 60-80%（微信反爬蟲限制）

### 2. 普通網頁抓取

```python
# 使用 OpenClaw 自帶的 web_fetch 工具
def fetch_webpage(url):
    # OpenClaw 會自動調用 web_fetch
    return web_fetch(url, extractMode="markdown")
```

### 3. 內容提取

```python
# 從 Markdown 提取元數據
def extract_metadata(content):
    # 用正則表達式提取標題
    title = re.search(r'^#\s+(.+)$', content, re.MULTILINE).group(1)
    
    # 提取前 200 字作為摘要
    summary = content[200:400] + "..."
    
    # 提取關鍵詞（簡單版：取前 5 個名詞）
    keywords = extract_keywords(content)[:5]
    
    return {
        "title": title,
        "summary": summary,
        "keywords": keywords
    }
```

### 4. 結構化存儲

```python
# 生成 Markdown 文件
def save_to_file(data):
    filename = f"{data['date']}-{data['slug']}.md"
    
    content = f"""---
title: "{data['title']}"
url: "{data['url']}"
date: {data['date']}
tags: [{', '.join(data['keywords'])}]
---

# {data['title']}

{data['content']}
"""
    
    with open(f"collections/{data['category']}/{filename}", "w") as f:
        f.write(content)
```

---

## 🎓 學習路徑

### 初學者（4 小時）

```
小時 1: 安裝並測試 → 理解基本功能
小時 2: 閱讀源碼 → 理解實現邏輯
小時 3: 修改參數 → 嘗試自定義
小時 4: 添加功能 → 實踐所學
```

### 進階者（2 小時）

```
小時 1: 審計代碼 → 找出可優化點
小時 2: 重構擴展 → 添加新特性
```

---

## ❓ 常見問題

### Q1: 微信文章抓取失敗怎麼辦？

**A:** 這是正常的，免費 API 成功率約 60-80%。

**解決方案：**
- 多嘗試幾次（不同 API）
- 換一篇較新的文章
- 或考慮配置 Cookie（需手動）

### Q2: 如何添加新的內容源？

**A:** 修改 `collector.py` 的 `fetch_content()` 函數：

```python
def fetch_content(url, source_type):
    if source_type == "wechat":
        return fetch_wechat(url)
    elif source_type == "zhihu":
        return fetch_zhihu(url)  # 新增
    else:
        return fetch_webpage(url)
```

### Q3: 如何修改存儲路徑？

**A:** 修改 `COLLECTIONS_DIR` 常量：

```python
COLLECTIONS_DIR = os.path.expanduser("~/.openclaw/workspace/collections")
```

---

## 📝 課後作業

1. **基礎題：** 修改存儲結構，按月份分類
2. **進階題：** 添加 B 站視頻收藏功能
3. **挑戰題：** 實現自動標籤生成（用 AI）

---

## 🎯 畢業標準

完成以下任務即視為掌握：

- ✅ 能獨立安裝並運行
- ✅ 能解釋核心代碼邏輯
- ✅ 能添加一個新的內容源
- ✅ 能修改存儲格式

---

**版本**: 1.0.0  
**作者**: 麻小  
**最後更新**: 2026-03-18


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]

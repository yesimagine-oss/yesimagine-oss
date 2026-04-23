# 🎓 學習路徑指南

**WeChat Fetcher 教學版** - 4 小時掌握微信抓取

---

## 📋 課程大綱

| 階段 | 內容 | 時間 | 目標 |
|------|------|------|------|
| 1 | 理解原理 | 30 分鐘 | 了解整體架構 |
| 2 | 閱讀源碼 | 1 小時 | 理解實現邏輯 |
| 3 | 動手實踐 | 1 小時 | 運行並測試 |
| 4 | 擴展修改 | 1.5 小時 | 自定義功能 |

---

## 階段 1：理解原理（30 分鐘）

### 閱讀材料

```bash
# 閱讀 README.md
cat README.md

# 閱讀 SKILL.md
cat SKILL.md
```

### 學習要點

- ✅ 微信文章抓取的基本原理
- ✅ 為什麼需要 API 輪詢
- ✅ 免費 API 的優缺點
- ✅ 存儲結構設計

### 理解檢查

完成後能回答：
1. 為什麼不直接訪問微信？
2. API 輪詢的好處是什麼？
3. 存儲結構為什麼這樣設計？

---

## 階段 2：閱讀源碼（1 小時）

### 閱讀順序

```bash
# 1. 主入口（最簡單）
cat collector.py | head -50

# 2. 核心抓取函數
cat collector.py | grep -A 30 "_fetch_content"

# 3. 元數據提取
cat collector.py | grep -A 20 "_extract_metadata"

# 4. 文件保存
cat collector.py | grep -A 20 "_save_to_file"
```

### 重點注釋

代碼中所有 `# 教學點：` 開頭的注釋都是重點。

### 理解檢查

完成後能解釋：
1. `_fetch_content()` 函數的邏輯
2. 如何識別反爬蟲頁面
3. Markdown frontmatter 的作用

---

## 階段 3：動手實踐（1 小時）

### 安裝

```bash
# 執行安裝腳本
bash install.sh

# 重啟 Gateway
openclaw gateway restart
```

### 測試

```bash
# 運行单元测试
python3 test/test_collector.py

# 測試抓取（用有效文章）
python3 collector.py
```

### 調試

```bash
# 開啟詳細日誌
python3 -c "
from collector import WeChatFetcher
fetcher = WeChatFetcher()
result = fetcher.fetch('https://mp.weixin.qq.com/s/xxx')
print(result)
"
```

### 實踐檢查

完成後能：
- ✅ 成功安裝技能
- ✅ 運行測試用例
- ✅ 抓取一篇文章

---

## 階段 4：擴展修改（1.5 小時）

### 練習 1：修改 API 列表（30 分鐘）

```python
# 在 collector.py 中添加新的 API
WECHAT_APIS = [
    {
        "name": "r.jina.ai",
        "url": "https://r.jina.ai/http://{url}",
        "success_rate": "90%",
        "speed": "快"
    },
    # 添加你的 API
    {
        "name": "your-api",
        "url": "https://your-api.com/proxy?url={url}",
        "success_rate": "??%",
        "speed": "?"
    }
]
```

### 練習 2：添加新字段（30 分鐘）

```python
# 在 _extract_metadata() 中添加作者提取
def _extract_metadata(self, content: str, url: str) -> Dict:
    # ... 現有代碼 ...
    
    # 提取作者
    author_match = re.search(r'作者：(.+)', content)
    author = author_match.group(1) if author_match else "未知"
    
    return {
        # ... 現有字段 ...
        "author": author,  # 新增
    }
```

### 練習 3：自定義存儲格式（30 分鐘）

```python
# 修改 _save_to_file() 改變輸出格式
def _save_to_file(self, metadata: Dict, content: str) -> str:
    # 改為 JSON 格式
    data = {
        "title": metadata['title'],
        "url": metadata['url'],
        "content": content
    }
    
    filename = f"{metadata['date']}-{metadata['slug']}.json"
    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

### 擴展檢查

完成後能：
- ✅ 添加新的 API
- ✅ 提取新的元數據字段
- ✅ 修改存儲格式

---

## 🎯 畢業標準

完成以下任務即視為掌握：

### 基礎要求
- ✅ 能解釋整體架構
- ✅ 能閱讀並理解源碼
- ✅ 能運行測試用例

### 進階要求
- ✅ 能添加新的 API
- ✅ 能修改存儲格式
- ✅ 能調試常見問題

### 挑戰要求
- ✅ 能添加新的內容源（如 B 站）
- ✅ 能實現自動標籤生成
- ✅ 能優化性能（並發、緩存等）

---

## 📚 參考資源

### Python 基礎
- [Python 正則表達式教程](https://docs.python.org/zh-cn/3/library/re.html)
- [Python 請求庫文檔](https://requests.readthedocs.io/)

### 網頁抓取
- [網頁抓取最佳實踐](https://zhuanlan.zhihu.com/p/xxxxx)
- [反爬蟲對抗技巧](https://zhuanlan.zhihu.com/p/xxxxx)

### OpenClaw
- [Skill 開發文檔](https://docs.openclaw.ai)
- [工具使用指南](https://docs.openclaw.ai/tools)

---

## ❓ 常見問題

### Q: 代碼看不懂怎麼辦？

**A:** 
1. 先看注釋（`# 教學點：` 開頭）
2. 用 print() 調試每一步
3. 問其他機器人或查文檔

### Q: 測試失敗怎麼辦？

**A:**
1. 檢查錯誤信息
2. 確認 Python 版本（需要 3.7+）
3. 確認依賴已安裝（`pip3 install requests`）

### Q: 抓取失敗怎麼辦？

**A:**
1. 確認文章鏈接有效
2. 檢查 API 是否可用
3. 查看日誌了解具體錯誤

---

**版本**: 1.0.0  
**作者**: 麻小  
**最後更新**: 2026-03-18

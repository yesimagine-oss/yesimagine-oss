# Asset ID 計算問題記錄

**時間**: 2026-04-13T08:20:00+08:00  
**類型**: 技術障礙  
**嚴重性**: 🟠 高

---

## 問題描述

Hub 計算的 asset_id 與本地計算不匹配，即使使用相同的 canonical JSON 方法。

### 測試結果

使用成功發布的資產 `evomap_hello_bundle_1775503401.json`：

```python
# 方法 1: sort_keys=True
Stored:   483e8be597f8412350b44ae593e949203eb986b7cef4e8a829d6225e9ba318ff
Computed: ca019bd5ba8b53c5d7e7122c80c43842b3a916b36ff0b6f42f3c732a3e97794a
Match: False

# 方法 2: 不排序 (preserve order)
Stored:   483e8be597f8412350b44ae593e949203eb986b7cef4e8a829d6225e9ba318ff
Computed: 03126b5d1be6fc979cabd5ee5bd4a43e9e432c1d81e0e197919194e54b50a8f7
Match: False
```

---

## 可能原因

1. **Hub 使用不同的 JSON 序列化庫**
   - 可能是 Node.js 的 JSON.stringify()
   - 可能是 Go 的 encoding/json
   - 可能是 Python 的不同版本

2. **Unicode 處理差異**
   - ensure_ascii=True vs False
   - 不同的 Unicode 轉義方式

3. **空白字符處理**
   - 分隔符可能不同
   - 可能有額外的空格或換行

4. **字段過濾**
   - Hub 可能排除某些字段
   - 可能只 hash 部分內容

---

## 解決方案

### 方案 A: 使用 Hub 的計算方法
- 需要查看 Hub 源代碼或文檔
- 或通過試錯找到正確方法

### 方案 B: 讓 Hub 計算
- 發布時不包含 asset_id
- 但測試顯示 asset_id 是必填字段

### 方案 C: 使用已有的成功資產
- 複製成功資產的格式
- 只修改必要字段
- 讓 Hub 重新計算

### 方案 D: 請求 Hub 文檔
- 查看 /a2a/skill?topic=publish
- 查找 canonical JSON 的準確定義

---

## 下一步

1. 查看 EvoMap 文檔
2. 嘗試使用 Node.js 計算 hash
3. 或聯繫 Hub 管理員獲取正確方法

---

**RedAgent Team | 🦞RedOpenClaw ...生活太快⚡️...老逼快跑💨...**

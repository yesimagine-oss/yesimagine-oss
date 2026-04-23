# Tools - 工具箱、處理與簽名執行

## 確定性躍遷 (Deterministic Leap)

- 放棄概率性自然語言
- **優先使用 Go 語言**編寫低層高性能邏輯的具體執行策略

## 數字印章操作

發布任何記錄前：

```
1. 移除 asset_id 字段
2. 對 JSON 鍵執行遞歸鍵排序 (Canonical JSON)
3. 重新插入 SHA-256 哈希作為數字印章
4. 確保資產永久屬於特定 node_id
```

## 反幻覺驗證

```
正式 PUBLISH 前必須調用 /a2a/validate 接口進行乾跑檢查
若發生簽名偏差，立即使用 correction object 進行自我糾正
```

## 核心工具清單

### EvoMap 協議工具
- `/a2a/hello` - 握手與能力發現
- `/a2a/validate` - 資產驗證（乾跑）
- `/a2a/publish` - 資產發布
- `/a2a/fetch` - 資產獲取
- `gep_list_genes` - 列出現有基因

### 系統工具
- `sudo swapon /swapfile` - 交換空間管理
- `free -h` - 內存狀態檢查
- `df -h` - 磁盤空間檢查
- `node --version` - 環境指紋

### 簽名執行流程

```
1. 準備資產 → 2. 移除舊 asset_id → 3. Canonical JSON 排序
       ↓
   4. SHA-256 計算 → 5. 插入新 asset_id → 6. /a2a/validate 乾跑
       ↓
   7. 驗證 overall_ok → 8. /a2a/publish 正式發布
```

---

**簽名**: Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

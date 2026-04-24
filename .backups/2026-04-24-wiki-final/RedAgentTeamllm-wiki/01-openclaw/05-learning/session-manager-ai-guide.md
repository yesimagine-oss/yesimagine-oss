# 會話管理系統 v3.0 - AI 決策型使用指南

**創建時間**: 2026-03-24 20:15  
**版本**: 3.0 (AI 決策型)  
**狀態**: ✅ 已部署並運行

---

## 🚀 核心突破

v3.0 實現了**AI 決策型進化**，讓系統像人類一樣思考和決策：

| 突破 | v2.0 Pro | v3.0 AI |
|------|----------|---------|
| **決策方式** | 規則評分 | 🧠 AI 智能決策 |
| **上下文** | 無視關聯 | 🔗 理解會話關聯 |
| **學習** | 靜態規則 | 📚 持續學習優化 |
| **預測** | 無 | 🔮 預測未來價值 |
| **解釋** | 簡單理由 | 💬 清晰解釋 |
| **執行** | 自動 | 🤖 自主執行（需確認） |

---

## 🧠 AI 決策引擎

### 決策流程

```
1. 提取會話摘要
   ↓
2. AI 分析內容類型
   ├─ 代碼片段
   ├─ 敏感配置
   ├─ 教程文檔
   ├─ 問題解決
   └─ 重要討論
   ↓
3. 上下文感知分析
   ├─ 查找相關會話
   ├─ 計算關鍵詞重疊
   └─ 上下文加分
   ↓
4. 綜合決策
   ├─ 保留 (≥60 分)
   ├─ 歸檔 (40-59 分)
   └─ 刪除 (<40 分)
   ↓
5. 生成解釋
   └─ 清晰的決策理由
```

### 評分維度

| 維度 | 權重 | 說明 |
|------|------|------|
| **內容類型** | 50 分 | 代碼/配置/教程等 |
| **長度** | 15 分 | 長會話更有價值 |
| **新近度** | 15 分 | 越新越有價值 |
| **上下文** | 10 分 | 相關會話加分 |
| **關鍵詞** | 10 分 | 重要詞彙加分 |

---

## 📖 命令說明

### 1️⃣ decide - AI 決策分析（核心）

```bash
python3 tools/session-manager-ai.py decide
```

**功能**:
- AI 分析所有會話
- 理解內容類型
- 上下文感知
- 給出決策建議
- 清晰的決策理由

**輸出示例**:
```
🧠 AI 決策分析引擎

加載 9 個會話...

決策總覽:
  總會話：9 個
  總體積：2.36MB
  可釋放：0.00MB

決策分佈:
  ✅ 保留：9 個

詳細決策:

 1. 9fbeaa27-8d3b-400b-9512-946d5652e11a.jsonl
    決策：✅ 保留 | 分數：100/100 | 0.01MB | 0 天前
    理由：包含敏感配置，問題解決，26 行，0 天前 + 上下文 (4 分)
    標籤：敏感配置，問題解決，最新
    未來價值：高 | 信心：70%
    相關：4 個會話 (+4 分)
```

---

### 2️⃣ explain - 解釋決策理由

```bash
python3 tools/session-manager-ai.py explain [會話名稱]
```

**功能**:
- 詳細解釋特定會話的決策
- 展示 AI 分析過程
- 上下文關聯說明
- 未來價值預測

**示例**:
```bash
python3 tools/session-manager-ai.py explain 4f90cb74
```

**輸出**:
```
🔍 決策解釋：4f90cb74-45c8-4c61-b910-21f4bc90b682.jsonl

會話信息:
  文件：4f90cb74-45c8-4c61-b910-21f4bc90b682.jsonl
  大小：1.59MB
  行數：427
  年齡：0 天
  類型：敏感配置，教程文檔，問題解決

AI 分析:
  原始分數：85/100
  原始建議：keep
  分析理由：包含敏感配置，教程文檔，問題解決，427 行，0 天前

上下文感知:
  相關會話：3 個
    - e2bc04f8... (重疊 25 個關鍵詞)
    - 1a9a21fe... (重疊 18 個關鍵詞)
  上下文加分：+3 分

最終決策:
  決策：✅ 保留
  最終分數：88/100
  決策理由：包含敏感配置，教程文檔，問題解決，427 行，0 天前 + 上下文 (3 分)

未來預測:
  未來價值：高
  AI 信心：85%
  標籤：敏感配置，教程文檔，問題解決，最新
```

---

### 3️⃣ predict - 預測未來價值

```bash
python3 tools/session-manager-ai.py predict
```

**功能**:
- 預測每個會話的未來價值
- 分類為高/中/低價值
- 給出保留建議

**輸出**:
```
🔮 未來價值預測

高價值預測 (建議永久保留):

  4f90cb74-45c8-4c61-b910-21f4bc90b682.jsonl
    分數：85 | 1.59MB | 標籤：敏感配置，教程文檔

中價值預測 (建議歸檔):

  30cf9bc9-d367-4668-ac08-9e546dcb44a9.jsonl
    分數：55 | 0.03MB

低價值預測 (可安全刪除):

  1c9ef9da-cfa1-4a03-aeec-267ae7005c45.jsonl
    分數：25 | 0.00MB

總計：高價值 5 個 | 中價值 2 個 | 低價值 2 個
```

---

### 4️⃣ learn - 學習用戶反饋

```bash
python3 tools/session-manager-ai.py learn
```

**功能**:
- 記錄用戶對決策的反饋
- 自動調整決策權重
- 持續優化 AI 決策

**使用方式**:
```
反饋格式：會話名稱 實際操作 評價 (好/壞)
例如：abc123.jsonl keep 好
```

**示例**:
```bash
python3 tools/session-manager-ai.py learn

當前偏好:
  preserve_code: True
  preserve_config: True
  ...

反饋歷史：5 條

輸入反饋格式：會話名稱 實際操作 評價 (好/壞)
例如：abc123.jsonl keep 好
或直接回車跳过

反饋：4f90cb74 keep 好

✅ 已記錄正面反饋，將強化類似決策
```

---

### 5️⃣ autonomous - 自主執行

```bash
# 預覽
python3 tools/session-manager-ai.py autonomous --dry-run

# 執行（需確認）
python3 tools/session-manager-ai.py autonomous
```

**功能**:
- 根據 AI 決策自動執行
- 安全限制（體積限制）
- 需要用戶確認

**配置**:
```json
{
  "autonomous": {
    "enabled": false,
    "require_confirmation": true,
    "max_auto_delete_mb": 10
  }
}
```

---

### 6️⃣ brain - 查看 AI 決策大腦

```bash
python3 tools/session-manager-ai.py brain
```

**功能**:
- 查看 AI 配置
- 用戶偏好
- 學習狀態
- 決策歷史

**輸出**:
```
🧠 AI 決策大腦

配置:
  AI 模型：dashscope-coding/qwen3.5-plus
  保留閾值：60 分
  歸檔閾值：40 分
  刪除閾值：20 分

用戶偏好:
  ✅ preserve_code: True
  ✅ preserve_config: True
  ✅ preserve_tutorials: True
  ❌ aggressive_cleanup: False
  ✅ prefer_archive_over_delete: True

學習狀態:
  啟用：是
  自動調整：是
  反饋權重：30%
  反饋歷史：5 條

決策歷史:
  總決策次數：10
  保留：45 個
  歸檔：30 個
  刪除：15 個
```

---

## ⚙️ 配置文件

### 主配置

**位置**: `tools/session-manager-ai-config.json`

```json
{
  "ai_model": "dashscope-coding/qwen3.5-plus",
  "decision_threshold": {
    "keep_score": 60,
    "archive_score": 40,
    "delete_score": 20
  },
  "context_awareness": {
    "enabled": true,
    "lookback_days": 7,
    "min_related_sessions": 2
  },
  "learning": {
    "enabled": true,
    "auto_adjust": true,
    "feedback_weight": 0.3
  },
  "autonomous": {
    "enabled": false,
    "require_confirmation": true,
    "max_auto_delete_mb": 10
  }
}
```

### 用戶偏好

**位置**: `tools/session-manager-ai-preferences.json`

```json
{
  "version": 1,
  "preferences": {
    "preserve_code": true,
    "preserve_config": true,
    "preserve_tutorials": true,
    "aggressive_cleanup": false,
    "prefer_archive_over_delete": true
  },
  "learning": {
    "enabled": true,
    "auto_adjust": true,
    "feedback_weight": 0.3
  },
  "feedback_history": [],
  "adjusted_weights": {}
}
```

---

## 🎯 使用場景

### 場景 1：日常 AI 決策

```bash
# 每天查看 AI 決策
python3 tools/session-manager-ai.py decide
```

---

### 場景 2：理解特定決策

```bash
# 為什麼這個會話被建議保留？
python3 tools/session-manager-ai.py explain abc123.jsonl
```

---

### 場景 3：預測未來價值

```bash
# 哪些會話未來可能有價值？
python3 tools/session-manager-ai.py predict
```

---

### 場景 4：學習優化

```bash
# 告訴 AI 哪些決策是對的
python3 tools/session-manager-ai.py learn

# 輸入：abc123.jsonl keep 好
```

---

### 場景 5：自主執行

```bash
# 預覽 AI 會做什麼
python3 tools/session-manager-ai.py autonomous --dry-run

# 執行（需確認）
python3 tools/session-manager-ai.py autonomous
```

---

## 📊 與 v2.0 對比

| 維度 | v2.0 Pro | v3.0 AI |
|------|----------|---------|
| **決策方式** | 規則評分 | AI 智能決策 |
| **上下文理解** | ❌ | ✅ 關聯分析 |
| **學習能力** | ❌ | ✅ 持續優化 |
| **預測能力** | ⚠️ 簡單 | ✅ 多維預測 |
| **解釋能力** | ⚠️ 簡單 | ✅ 詳細解釋 |
| **用戶反饋** | ❌ | ✅ 學習反饋 |
| **自主執行** | ⚠️ 機械 | ✅ 智能決策 |

---

## 🕐 定時任務

### 推薦配置

```bash
# 每天 03:00 - AI 決策分析
0 3 * * * cd /home/admin/.openclaw/workspace && python3 tools/session-manager-ai.py decide >> /tmp/session-ai-decide.log 2>&1

# 每週一 08:00 - 未來價值預測
0 8 * * 1 cd /home/admin/.openclaw/workspace && python3 tools/session-manager-ai.py predict >> /tmp/session-ai-predict.log 2>&1

# 每週日 23:00 - 學習用戶反饋（可選）
0 23 * * 0 cd /home/admin/.openclaw/workspace && python3 tools/session-manager-ai.py learn >> /tmp/session-ai-learn.log 2>&1
```

---

## 🎓 最佳實踐

### 1️⃣ 每天查看 AI 決策

```bash
python3 tools/session-manager-ai.py decide
```

了解 AI 如何決策，建立信任。

---

### 2️⃣ 提供反饋

```bash
python3 tools/session-manager-ai.py learn
# 輸入：abc123.jsonl keep 好
```

幫助 AI 學習你的偏好。

---

### 3️⃣ 定期預測

```bash
python3 tools/session-manager-ai.py predict
```

了解哪些會話未來有價值。

---

### 4️⃣ 解釋疑問

```bash
python3 tools/session-manager-ai.py explain abc123.jsonl
```

理解 AI 的決策理由。

---

### 5️⃣ 謹慎自主執行

```bash
# 先預覽
python3 tools/session-manager-ai.py autonomous --dry-run

# 確認後執行
python3 tools/session-manager-ai.py autonomous
```

---

## 📈 預期效果

### 短期（1 週）

- ✅ AI 理解你的會話內容
- ✅ 建立決策信任
- ✅ 開始學習偏好

### 中期（1 月）

- ✅ AI 決策準確率 >90%
- ✅ 理解上下文關聯
- ✅ 預測未來價值

### 長期（3 月）

- ✅ AI 完全理解你的工作風格
- ✅ 自主決策可信賴
- ✅ 持續學習優化

---

## 📚 相關文件

| 文件 | 路徑 | 說明 |
|------|------|------|
| **核心工具** | `tools/session-manager-ai.py` | AI 決策工具 |
| **配置文件** | `tools/session-manager-ai-config.json` | AI 配置 |
| **偏好文件** | `tools/session-manager-ai-preferences.json` | 用戶偏好 |
| **決策日誌** | `~/.openclaw/ai/decisions.jsonl` | 決策歷史 |
| **使用指南** | `docs/session-manager-ai-guide.md` | 本文檔 |

---

## 🆘 快速命令參考

```bash
# AI 決策（核心）
python3 tools/session-manager-ai.py decide

# 解釋決策
python3 tools/session-manager-ai.py explain abc123.jsonl

# 預測未來
python3 tools/session-manager-ai.py predict

# 學習反饋
python3 tools/session-manager-ai.py learn

# 自主執行
python3 tools/session-manager-ai.py autonomous --dry-run

# 查看大腦
python3 tools/session-manager-ai.py brain

# 查看日誌
tail /tmp/session-ai-decide.log
```

---

**維護者**: RedOpenClaw  
**版本**: 3.0 AI  
**最後更新**: 2026-03-24 20:15  
**狀態**: ✅ 運行正常

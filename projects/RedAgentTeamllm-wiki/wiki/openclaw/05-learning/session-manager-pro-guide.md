# 會話管理系統 Pro v2.0 - 核心突破版使用指南

**創建時間**: 2026-03-24 20:00  
**版本**: 2.0 (核心突破版)  
**狀態**: ✅ 已部署並運行

---

## 🚀 核心突破

相比 v1.0，v2.0 實現了**五大核心突破**：

| 突破 | v1.0 | v2.0 Pro |
|------|------|----------|
| **清理策略** | 按時間機械清理 | 🧠 AI 智能價值評分 |
| **存儲方式** | 直接刪除 | 📦 壓縮歸檔保存 |
| **會話管理** | 一視同仁 | 🎯 分級管理（關鍵/重要/普通/臨時） |
| **數據安全** | 無備份 | 💾 關鍵會話自動備份 |
| **歷史追溯** | 刪除即消失 | 🔍 可搜索歸檔內容 |

---

## 🎯 AI 智能價值評分系統

### 評分維度（總分 100）

| 維度 | 權重 | 說明 |
|------|------|------|
| **代碼含量** | 30 分 | 檢測是否包含代碼片段 |
| **配置信息** | 25 分 | 檢測是否包含 API Key、配置等 |
| **會話長度** | 20 分 | 長會話通常更有價值 |
| **新近度** | 15 分 | 越新越有價值 |
| **關鍵詞** | 10 分 | 包含「重要」「關鍵」「教程」等 |

### 會話分級

| 等級 | 分數範圍 | 保留期 | 說明 |
|------|---------|--------|------|
| 🔴 **關鍵** | ≥80 分 | 90 天 | 包含核心代碼、配置，極高價值 |
| 🟡 **重要** | 60-79 分 | 30 天 | 包含代碼或配置，高價值 |
| 🟢 **普通** | 40-59 分 | 7 天 | 一般對話，中等價值 |
| ⚪ **臨時** | <40 分 | 1 天 | 簡單問答，低價值 |

---

## 📖 命令說明

### 1️⃣ analyze - AI 智能分析（核心）

```bash
python3 tools/session-manager-pro.py analyze
```

**功能**:
- 分析所有會話的價值分數
- 自動分級（關鍵/重要/普通/臨時）
- 顯示評分原因
- 按價值排序

**輸出示例**:
```
🧠 AI 智能會話價值分析

總會話：10 個 | 總體積：2.28MB

價值分佈:
  🟡 重要：5 個
  🟢 普通：2 個
  ⚪ 臨時：3 個

會話詳情 (按價值排序):

 1. e2bc04f8-a400-44a3-90be-318fa571b30a.jsonl
    分數：73/100 | 🟡 重要 | 0.17MB | 0 天前
    原因：包含代碼片段 (+18) | 包含配置信息 (+25) | 長度 77 行 (+5)
```

---

### 2️⃣ smart - 智能清理（推薦）

```bash
# 預覽清理效果
python3 tools/session-manager-pro.py smart --dry-run

# 實際執行清理
python3 tools/session-manager-pro.py smart
```

**智能清理邏輯**:
1. AI 分析所有會話價值
2. 根據分級和保留期判斷是否清理
3. 優先歸檔而非刪除（30 天內）
4. 超過 60 天的低價值會話才刪除
5. 關鍵會話永不刪除

**清理策略**:
```
臨時會話 (>1 天)   → 歸檔
普通會話 (>7 天)   → 歸檔
重要會話 (>30 天)  → 歸檔
關鍵會話 (>90 天)  → 歸檔
任何會話 (>60 天)  → 刪除（關鍵除外）
```

---

### 3️⃣ archive - 歸檔舊會話

```bash
# 預覽歸檔
python3 tools/session-manager-pro.py archive --dry-run

# 執行歸檔
python3 tools/session-manager-pro.py archive
```

**歸檔特點**:
- 使用 gzip 壓縮（節省 70-90% 空間）
- 保留元數據（評分、原因等）
- 原文件刪除，歸檔到 `~/.openclaw/archive/sessions/`
- 可隨時解壓查看

**歸檔文件結構**:
```
~/.openclaw/archive/sessions/
├── [會話 ID]_archived_20260324.jsonl.gz    # 壓縮的會話
└── [會話 ID]_archived_20260324.meta.json   # 元數據
```

---

### 4️⃣ backup - 備份關鍵會話

```bash
python3 tools/session-manager-pro.py backup
```

**備份特點**:
- 自動識別關鍵會話（≥80 分）
- 備份到 `~/.openclaw/backup/sessions/`
- 包含 MD5 校驗碼
- 保留元數據

**備份文件結構**:
```
~/.openclaw/backup/sessions/
├── [會話 ID]_backup_20260324_120000.jsonl    # 備份文件
└── [會話 ID]_backup_20260324_120000.meta.json # 元數據
```

---

### 5️⃣ search - 搜索歷史內容

```bash
# 搜索關鍵詞
python3 tools/session-manager-pro.py search "API key"
python3 tools/session-manager-pro.py search "配置"
python3 tools/session-manager-pro.py search "def "
```

**搜索特點**:
- 跨所有會話搜索
- 顯示匹配次數
- 顯示上下文片段
- 按相關度排序

**輸出示例**:
```
🔍 搜索會話：'配置'

找到 7 個匹配結果:

1. 4f90cb74-45c8-4c61-b910-21f4bc90b682.jsonl
   匹配次數：368 | 大小：1.59MB
   片段：...这个项目对你有帮助，请给我们一个 Star！⭐\n[plugins] 下一步（配置引导）:...
```

---

### 6️⃣ lifecycle - 查看生命週期

```bash
python3 tools/session-manager-pro.py lifecycle
```

**功能**:
- 顯示每個會話的剩餘保留天數
- 標記已過期和即將到期的會話
- 按到期時間排序

**輸出示例**:
```
📊 會話生命週期管理

即將到期的會話:

  6806099c-e072-424d-a19b-e5eca5306741.jso
    ⚪ 臨時 | 1 天 / 1 天 | 剩餘：已過期 0 天

  9fbeaa27-8d3b-400b-9512-946d5652e11a.jso
    🟢 普通 | 0 天 / 7 天 | 剩餘：7 天

  e2bc04f8-a400-44a3-90be-318fa571b30a.jso
    🟡 重要 | 0 天 / 30 天 | 剩餘：30 天
```

---

## ⚙️ 配置文件

**位置**: `/home/admin/.openclaw/workspace/tools/session-manager-pro-config.json`

**完整配置**:
```json
{
  "value_scoring": {
    "code_weight": 30,
    "config_weight": 25,
    "length_weight": 20,
    "recency_weight": 15,
    "frequency_weight": 10
  },
  "retention": {
    "critical_days": 90,
    "important_days": 30,
    "normal_days": 7,
    "temp_days": 1
  },
  "archive": {
    "enabled": true,
    "compress": true,
    "before_delete_days": 30
  },
  "backup": {
    "enabled": true,
    "auto_backup_critical": true,
    "backup_to_feishu": false
  },
  "thresholds": {
    "critical_score": 80,
    "important_score": 60,
    "normal_score": 40,
    "max_bytes_mb": 100
  }
}
```

**調整建議**:

### 如果想保留更多會話
```json
{
  "retention": {
    "critical_days": 180,
    "important_days": 60,
    "normal_days": 14,
    "temp_days": 3
  },
  "thresholds": {
    "critical_score": 70,
    "important_score": 50,
    "normal_score": 30
  }
}
```

### 如果想節省空間
```json
{
  "retention": {
    "critical_days": 60,
    "important_days": 14,
    "normal_days": 3,
    "temp_days": 1
  },
  "archive": {
    "before_delete_days": 7
  }
}
```

---

## 🕐 定時任務

### v2.0 推薦配置

```bash
# 智能清理（每天凌晨 3:00）
0 3 * * * cd /home/admin/.openclaw/workspace && python3 tools/session-manager-pro.py smart >> /tmp/session-pro-cleanup.log 2>&1

# AI 分析報告（每週一 8:00）
0 8 * * 1 cd /home/admin/.openclaw/workspace && python3 tools/session-manager-pro.py analyze >> /tmp/session-pro-analyze.log 2>&1

# 自動備份（每週日 23:00）
0 23 * * 0 cd /home/admin/.openclaw/workspace && python3 tools/session-manager-pro.py backup >> /tmp/session-pro-backup.log 2>&1
```

**查看日誌**:
```bash
tail /tmp/session-pro-cleanup.log
tail /tmp/session-pro-analyze.log
tail /tmp/session-pro-backup.log
```

---

## 🎯 使用場景

### 場景 1：日常使用（全自動）

**無需手動操作**，系統會：
- 每天 03:00 自動智能清理
- 每週一 08:00 自動分析報告
- 每週日 23:00 自動備份關鍵會話

---

### 場景 2：查找歷史配置

```bash
# 搜索 API 配置
python3 tools/session-manager-pro.py search "API key"

# 搜索代碼片段
python3 tools/session-manager-pro.py search "def "

# 搜索特定命令
python3 tools/session-manager-pro.py search "openclaw sessions"
```

---

### 場景 3：查看哪些會話快到期

```bash
python3 tools/session-manager-pro.py lifecycle
```

---

### 場景 4：手動智能清理

```bash
# 預覽
python3 tools/session-manager-pro.py smart --dry-run

# 執行
python3 tools/session-manager-pro.py smart
```

---

### 場景 5：緊急備份

```bash
# 立即備份所有關鍵會話
python3 tools/session-manager-pro.py backup
```

---

## 📊 與 v1.0 對比

### 空間效率

| 指標 | v1.0 | v2.0 Pro | 提升 |
|------|------|----------|------|
| **歸檔壓縮率** | 無 | 70-90% | ✅ 節省 3-10 倍 |
| **清理精度** | 按時間 | AI 智能 | ✅ 保留高價值 |
| **備份機制** | 無 | 自動備份 | ✅ 數據安全 |

### 功能對比

| 功能 | v1.0 | v2.0 Pro |
|------|------|----------|
| AI 價值評分 | ❌ | ✅ |
| 分級管理 | ❌ | ✅ 4 級 |
| 壓縮歸檔 | ❌ | ✅ gzip |
| 自動備份 | ❌ | ✅ |
| 全文搜索 | ❌ | ✅ |
| 生命週期 | ❌ | ✅ |
| 智能清理 | ⚠️ 基礎 | ✅ 高級 |

---

## 🔧 故障排除

### 問題 1：AI 評分不準確

**原因**: 評分規則可能需要調整

**解決**:
```bash
# 編輯配置文件
nano tools/session-manager-pro-config.json

# 調整權重（如增加代碼權重）
{
  "value_scoring": {
    "code_weight": 40  // 從 30 提高到 40
  }
}
```

---

### 問題 2：歸檔文件太大

**原因**: 壓縮率不夠

**解決**:
```bash
# 檢查壓縮是否啟用
cat tools/session-manager-pro-config.json | grep compress

# 確保為 true
"compress": true
```

---

### 問題 3：搜索不到內容

**原因**: 可能已被歸檔

**解決**:
```bash
# 搜索歸檔文件
zcat ~/.openclaw/archive/sessions/*.jsonl.gz | grep "關鍵詞"
```

---

## 🎓 最佳實踐

### 1️⃣ 定期查看分析報告

```bash
# 每週查看一次
python3 tools/session-manager-pro.py analyze
```

了解會話價值分佈，調整評分策略。

---

### 2️⃣ 重要會話手動備份

```bash
# 在重大項目結束後
python3 tools/session-manager-pro.py backup
```

---

### 3️⃣ 搜索優先於清理

清理前先搜索，確保沒有遺漏重要內容：

```bash
python3 tools/session-manager-pro.py search "關鍵詞"
python3 tools/session-manager-pro.py smart --dry-run
```

---

### 4️⃣ 定期檢查歸檔

```bash
# 查看歸檔目錄
ls -lh ~/.openclaw/archive/sessions/

# 查看歸檔統計
du -sh ~/.openclaw/archive/sessions/
```

---

### 5️⃣ 備份歸檔目錄

```bash
# 每月備份一次歸檔
tar -czf ~/backup/session-archive-$(date +%Y%m).tar.gz \
  ~/.openclaw/archive/sessions/
```

---

## 📈 預期效果

### 短期（1 週）

- ✅ 自動識別並保護高價值會話
- ✅ 歸檔 5-10 個低價值舊會話
- ✅ 節省 30-50% 空間

### 中期（1 月）

- ✅ 建立完整的會話價值數據庫
- ✅ 歸檔 20-50 個會話
- ✅ 備份 5-10 個關鍵會話
- ✅ 節省 60-80% 空間

### 長期（1 年）

- ✅ 累積歸檔 200-500 個會話
- ✅ 備份 50-100 個關鍵會話
- ✅ 總空間控制在 50-100MB
- ✅ 所有歷史內容可搜索

---

## 📚 相關文件

| 文件 | 路徑 | 說明 |
|------|------|------|
| **核心工具** | `tools/session-manager-pro.py` | Pro 版管理腳本 |
| **配置文件** | `tools/session-manager-pro-config.json` | Pro 版配置 |
| **歸檔目錄** | `~/.openclaw/archive/sessions/` | 壓縮歸檔 |
| **備份目錄** | `~/.openclaw/backup/sessions/` | 關鍵備份 |
| **使用指南** | `docs/session-manager-pro-guide.md` | 本文檔 |
| **v1 文檔** | `docs/session-management-guide.md` | v1.0 文檔 |

---

## 🆘 快速命令參考

```bash
# AI 分析
python3 tools/session-manager-pro.py analyze

# 智能清理（預覽）
python3 tools/session-manager-pro.py smart --dry-run

# 智能清理（執行）
python3 tools/session-manager-pro.py smart

# 搜索歷史
python3 tools/session-manager-pro.py search "關鍵詞"

# 生命週期
python3 tools/session-manager-pro.py lifecycle

# 備份關鍵
python3 tools/session-manager-pro.py backup

# 歸檔舊會話
python3 tools/session-manager-pro.py archive

# 查看日誌
tail /tmp/session-pro-cleanup.log
```

---

**維護者**: RedOpenClaw  
**版本**: 2.0 Pro  
**最後更新**: 2026-03-24 20:00  
**狀態**: ✅ 運行正常

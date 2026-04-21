# RedAgentTeamllm-wiki Crontab 配置
# 配置時間：2026-04-21 11:16
# 維護者：Red Agent Team

---

## 📋 完整 Crontab 配置

**安裝命令:** `crontab -e`

```bash
# ============= 現有任務 (保留) =============

# EvoMap 監控 (原有)
*/30 * * * * cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目 && python3 scripts/evomap-monitor.py >> logs/evomap-monitor.log 2>&1
0 * * * * cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目 && python3 monitor-skill-downloads.py >> monitoring/cron.log 2>&1

# AgentTeamllm-wiki 自動化任務 (原有 - 已更新路徑)
0 2 * * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/auto-backup.sh >> /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/backup.log 2>&1
0 5 * * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/auto-ingest.py >> /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/ingest.log 2>&1
0 1 * * 0 /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/auto-lint.sh >> /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/lint.log 2>&1

# ============= 新增任務 (健康監測) =============

# 每日 06:00 - 健康告警檢查 (健康分<80 自動通知)
0 6 * * * cd /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki && ./scripts/health-alert.sh >> /tmp/wiki-alert.log 2>&1

# 每週日 06:00 - 週報生成
0 6 * * 0 cd /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki && ./scripts/generate-weekly-report.sh >> /tmp/wiki-report.log 2>&1

# 每月 1 日 02:00 - 深度審計 + 歸檔
0 2 1 * * cd /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki && ./scripts/auto-audit.sh >> /tmp/wiki-audit.log 2>&1

# 每月 1 日 06:00 - 月報生成
0 6 1 * * cd /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki && ./scripts/generate-monthly-report.sh >> /tmp/wiki-report.log 2>&1

# 每月 21 日 09:00 - SOP 審查 (健康監測 SOP 月度回顧)
0 9 21 * * cd /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki && ./scripts/review-health-sop.sh >> /tmp/wiki-sop-review.log 2>&1
```

---

## 📊 任務統計

| 類型 | 數量 | 說明 |
|------|------|------|
| **現有任務** | 5 個 | EvoMap 監控 + Wiki 自動化 |
| **新增任務** | 5 個 | 健康監測相關 |
| **總計** | 10 個 | - |

---

## 🔧 安裝步驟

### 步驟 1: 備份現有 Crontab

```bash
crontab -l > ~/cron-backup-$(date +%Y%m%d-%H%M%S).txt
```

### 步驟 2: 編輯 Crontab

```bash
crontab -e
```

### 步驟 3: 粘貼配置

粘貼上方「完整 Crontab 配置」區塊

### 步驟 4: 驗證配置

```bash
# 查看已安裝的 Crontab
crontab -l

# 檢查 Cron 服務狀態
systemctl status cron  # Debian/Ubuntu
```

---

## 📝 任務說明

### 現有任務 (保留)

| 頻率 | 任務 | 說明 |
|------|------|------|
| 每 30 分鐘 | evomap-monitor.py | EvoMap 資產監控 |
| 每小時 | monitor-skill-downloads.py | Skill 下載統計 |
| 每日 02:00 | auto-backup.sh | 自動備份 |
| 每日 05:00 | auto-ingest.py | 自動 Ingest |
| 每週日 01:00 | auto-lint.sh | 完整 Lint 檢查 |

### 新增任務 (健康監測)

| 頻率 | 任務 | 說明 |
|------|------|------|
| 每日 06:00 | health-alert.sh | 健康分告警 (<80 通知) |
| 每週日 06:00 | generate-weekly-report.sh | 週報生成 |
| 每月 1 日 02:00 | auto-audit.sh | 深度審計 |
| 每月 1 日 06:00 | generate-monthly-report.sh | 月報生成 |
| 每月 21 日 09:00 | review-health-sop.sh | SOP 月度審查 |

---

## ⚙️ 通知配置 (可選)

### 飛書 Webhook

編輯 `scripts/health-alert.sh` L15:

```bash
FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_KEY"
```

### 郵件通知 (可選)

編輯 `scripts/health-alert.sh` L16:

```bash
EMAIL_RECIPIENT="red@unvw.com"
```

---

## 📈 驗證方法

### 立即測試

```bash
# 測試健康告警腳本
./scripts/health-alert.sh

# 查看日誌
tail -f /tmp/wiki-alert.log
```

### 檢查 Cron 執行

```bash
# 查看 Cron 日誌
grep CRON /var/log/syslog | tail -20
```

---

## 🎯 健康分閾值

| 分數 | 等級 | 通知 |
|------|------|------|
| ≥90 | 🟢 优秀 | 無通知 |
| 80-89 | 🟡 良好 | 無通知 |
| 75-79 | 🟠 一般 | ⚠️ 飛書通知 |
| <75 | 🔴 警告 | 🔴 飛書 + 郵件 |

---

**首次審查日期:** 2026-05-21 09:00  
**配置狀態:** 🟡 Pending → ✅ Active (用戶確認後)

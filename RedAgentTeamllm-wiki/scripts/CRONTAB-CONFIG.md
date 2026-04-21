# RedAgentTeamllm-wiki 定時任務配置

**配置時間**: 2026-04-21 11:10  
**維護者**: Red Agent Team

---

## 📋 Crontab 配置

### 編輯命令

```bash
crontab -e
```

### 配置內容

```bash
# RedAgentTeamllm-wiki 定時任務

# 每日 05:30 - 簡化 Lint 檢查
30 5 * * * cd /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki && ./scripts/auto-lint.sh --mode=daily >> /tmp/wiki-lint.log 2>&1

# 每日 06:00 - 健康告警檢查
0 6 * * * cd /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki && ./scripts/health-alert.sh >> /tmp/wiki-alert.log 2>&1

# 每週日 01:00 - 完整 Lint 檢查
0 1 * * 0 cd /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki && ./scripts/auto-lint.sh --mode=weekly >> /tmp/wiki-lint.log 2>&1

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

## 🔧 安裝步驟

### 步驟 1: 備份現有 Crontab

```bash
crontab -l > ~/cron-backup-$(date +%Y%m%d).txt
```

### 步驟 2: 編輯 Crontab

```bash
crontab -e
```

### 步驟 3: 粘貼配置

粘貼上方「配置內容」區塊

### 步驟 4: 驗證配置

```bash
# 查看已安裝的 Crontab
crontab -l

# 檢查 Cron 服務狀態
systemctl status cron  # Debian/Ubuntu
# 或
systemctl status crond  # CentOS/RHEL
```

---

## 📊 驗證方法

### 立即測試 (不等待定時)

```bash
# 測試 Lint 腳本
./scripts/auto-lint.sh --mode=daily

# 測試健康告警
./scripts/health-alert.sh

# 查看日誌
tail -f /tmp/wiki-lint.log
tail -f /tmp/wiki-alert.log
```

### 檢查執行記錄

```bash
# 查看 Cron 執行日誌
grep CRON /var/log/syslog | tail -20  # Debian/Ubuntu
# 或
grep CRON /var/log/cron | tail -20    # CentOS/RHEL
```

---

## ⚙️ 通知配置 (可選)

### 飛書 Webhook 配置

編輯 `scripts/health-alert.sh`:

```bash
FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_KEY"
```

### 郵件通知配置

編輯 `scripts/health-alert.sh`:

```bash
EMAIL_RECIPIENT="red@unvw.com"
```

確保系統已安裝 mail 命令:

```bash
# 安裝 mail (如需要)
sudo apt-get install mailutils  # Debian/Ubuntu
# 或
sudo yum install mailx          # CentOS/RHEL
```

---

## 📝 月度審查流程

### 審查時間

**每月 21 日 09:00** (自動執行)

### 審查內容

1. **健康分趨勢**
   - 本月平均健康分
   - 對比上月 (↑/↓/→)
   - 連續趨勢 (連續 N 月上昇/下降)

2. **指標達成率**
   - 日更新量達標天數 (%)
   - 周 Lint 完成率 (%)
   - 自動化率 (%)

3. **SOP 有效性**
   - 異常響應時間是否達標
   - 告警準確率 (有無誤報/漏報)
   - 用戶滿意度 (主觀評分)

4. **優化建議**
   - 需要調整的閾值
   - 需要新增的指標
   - 需要優化的流程

### 審查輸出

**報告位置**: `reports/sop-review-YYYY-MM.md`

**報告模板**:

```markdown
# 健康監測 SOP 月度審查

**審查日期**: YYYY-MM-21  
**審查者**: Red Agent Team

## 本月健康分趨勢

| 週次 | 健康分 | 等級 |
|------|--------|------|
| W1 | XX | 🟢/🟡/🟠/🔴 |
| W2 | XX | 🟢/🟡/🟠/🔴 |
| W3 | XX | 🟢/🟡/🟠/🔴 |
| W4 | XX | 🟢/🟡/🟠/🔴 |

## 指標達成率

- 日更新量：XX% (目標≥80%)
- 周 Lint: XX% (目標 100%)
- 自動化率：XX% (目標≥80%)

## 告警統計

- P0 告警：X 次
- P1 告警：X 次
- P2 告警：X 次

## SOP 優化建議

- [ ] 調整閾值：...
- [ ] 新增指標：...
- [ ] 優化流程：...

## 下月重點

- [ ] ...
```

---

## 🔔 首次審查日期

**2026-05-21 09:00** (首次月度審查)

---

**配置狀態**: 🟡 Pending → ✅ Active (用戶確認後)

#!/bin/bash
# RedAgentTeamllm-wiki 月报生成脚本
# 执行时间：每月 1 日 06:00
# 功能：汇总本月增长率、自动化率、SOP 审查提醒

set -e

# 配置
WIKI_ROOT="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki"
REPORTS_DIR="$WIKI_ROOT/reports"
LOG_FILE="$WIKI_ROOT/logs/monthly-report.log"
MONTH=$(date +%Y-%m)
LAST_MONTH=$(date -d "last month" +%Y-%m 2>/dev/null || date -v-1m +%Y-%m 2>/dev/null || echo "unknown")

# 确保目录存在
mkdir -p "$REPORTS_DIR"
mkdir -p "$(dirname $LOG_FILE)"

log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

log "🚀 开始生成月报 ($MONTH)"

# 1. 统计文件总数
log "  统计文件数量..."
TOTAL_FILES=$(find "$WIKI_ROOT" -name "*.md" -type f | wc -l)
WIKI_FILES=$(find "$WIKI_ROOT/wiki" -name "*.md" -type f | wc -l)
RAW_FILES=$(find "$WIKI_ROOT/raw" -name "*.md" -type f | wc -l)

# 2. 统计本月新增 (30 天内)
NEW_FILES=$(find "$WIKI_ROOT" -name "*.md" -type f -mtime -30 | wc -l)
GROWTH_RATE=$(awk "BEGIN {printf \"%.1f\", ($NEW_FILES / ($TOTAL_FILES - $NEW_FILES + 1)) * 100}")

# 3. 获取最新健康分
log "  获取健康数据..."
LATEST_LINT=$(ls -t "$REPORTS_DIR"/lint-weekly-*.md 2>/dev/null | head -1)
if [ -n "$LATEST_LINT" ] && [ -f "$LATEST_LINT" ]; then
    HEALTH_STATUS=$(grep "評級:" "$LATEST_LINT" 2>/dev/null | cut -d':' -f2 | xargs || echo "Unknown")
else
    HEALTH_STATUS="No lint report"
fi

# 4. 自动化率估算 (基于 Crontab 任务数)
CRON_TASKS=$(crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | wc -l)
AUTO_RATE=$(awk "BEGIN {printf \"%.0f\", ($CRON_TASKS / 10.0) * 100}")

# 5. 生成月报
REPORT_FILE="$REPORTS_DIR/monthly-report-$MONTH.md"
log "  生成报告：$REPORT_FILE"

cat > "$REPORT_FILE" << EOF
# RedAgentTeamllm-wiki 月报

**月份**: $MONTH  
**生成時間**: $(date -Iseconds)  
**上月**: $LAST_MONTH

---

## 📊 核心指標

| 指標 | 本月 | 說明 |
|------|------|------|
| **文件總數** | $TOTAL_FILES | - |
| **本月新增** | $NEW_FILES | - |
| **月增長率** | ${GROWTH_RATE}% | 目標≥30% |
| **自動化率** | ${AUTO_RATE}% | 目標≥80% |
| **健康評級** | $HEALTH_STATUS | - |

---

## 📁 文件分佈

| 目錄 | 文件數 | 佔比 |
|------|--------|------|
| wiki/ | $WIKI_FILES | $(awk "BEGIN {printf \"%.1f\", ($WIKI_FILES / $TOTAL_FILES) * 100}")% |
| raw/ | $RAW_FILES | $(awk "BEGIN {printf \"%.1f\", ($RAW_FILES / $TOTAL_FILES) * 100}")% |
| 其他 | $((TOTAL_FILES - WIKI_FILES - RAW_FILES)) | $(awk "BEGIN {printf \"%.1f\", (($TOTAL_FILES - $WIKI_FILES - $RAW_FILES) / $TOTAL_FILES) * 100}")% |

---

## 🏥 健康狀態

**評級**: $HEALTH_STATUS

<!-- 詳細健康數據參見 Lint 報告 -->

---

## 📝 本月重點

<!-- 手動填寫本月重點工作 -->

- [ ] ...

---

## 📋 下月目標

<!-- 手動填寫下月目標 -->

- [ ] ...

---

## ⚠️ SOP 審查提醒

**下次審查日期**: $(date -d "+20 days" +%Y-%m-%d 2>/dev/null || date -v+20d +%Y-%m-%d 2>/dev/null || echo "本月 21 日")

**審查內容**:
- [ ] 健康分趨勢分析
- [ ] 指標達成率回顧
- [ ] SOP 優化建議

---

**生成**: RedAgentTeamllm-wiki Auto-Reporter
EOF

log "✅ 月报生成完成"
log "  文件：$REPORT_FILE"
log "  文件总数：$TOTAL_FILES"
log "  月增长率：${GROWTH_RATE}%"
log "  自动化率：${AUTO_RATE}%"

exit 0

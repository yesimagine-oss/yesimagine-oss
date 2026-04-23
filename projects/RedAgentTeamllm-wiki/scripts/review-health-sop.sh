#!/bin/bash
# RedAgentTeamllm-wiki SOP 月度审查脚本
# 执行时间：每月 21 日 09:00
# 功能：SOP 审查 + 优化建议 + 飞书通知

set -e

# 配置
WIKI_ROOT="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki"
REPORTS_DIR="$WIKI_ROOT/reports"
LOG_FILE="$WIKI_ROOT/logs/sop-review.log"
REVIEW_MONTH=$(date +%Y-%m)
REVIEW_DATE=$(date +%Y-%m-%d)

# 飞书配置 (可选)
FEISHU_WEBHOOK="${FEISHU_WEBHOOK:-}"

# 确保目录存在
mkdir -p "$REPORTS_DIR"
mkdir -p "$(dirname $LOG_FILE)"

log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

log "🚀 开始 SOP 月度审查 ($REVIEW_MONTH)"

# 1. 获取健康趋势
log "  分析健康趋势..."
LATEST_LINT=$(ls -t "$REPORTS_DIR"/lint-weekly-*.md 2>/dev/null | head -1)
if [ -n "$LATEST_LINT" ] && [ -f "$LATEST_LINT" ]; then
    HEALTH_STATUS=$(grep "評級:" "$LATEST_LINT" 2>/dev/null | cut -d':' -f2 | xargs || echo "Unknown")
    ORPHAN_COUNT=$(grep "孤頁：" "$LATEST_LINT" 2>/dev/null | grep -oP '\d+' | head -1 || echo 0)
else
    HEALTH_STATUS="No data"
    ORPHAN_COUNT=0
fi

# 2. 统计任务执行情况
log "  统计任务执行..."
CRON_TASKS=$(crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | wc -l)
BACKUP_DAYS=$(find "$WIKI_ROOT/backups" -name "*.bak" -mtime -7 2>/dev/null | wc -l)
INGEST_LOG="$WIKI_ROOT/logs/ingest.log"
if [ -f "$INGEST_LOG" ]; then
    INGEST_COUNT=$(grep -c "已處理" "$INGEST_LOG" 2>/dev/null || echo 0)
else
    INGEST_COUNT=0
fi

# 3. 检查脚本完整性
log "  检查脚本..."
MISSING_SCRIPTS=()
for script in generate-weekly-report.sh generate-monthly-report.sh auto-audit.sh review-health-sop.sh; do
    if [ ! -x "$WIKI_ROOT/scripts/$script" ]; then
        MISSING_SCRIPTS+=("$script")
    fi
done

# 4. 生成审查报告
REPORT_FILE="$REPORTS_DIR/sop-review-$REVIEW_MONTH.md"
log "  生成报告：$REPORT_FILE"

cat > "$REPORT_FILE" << EOF
# RedAgentTeamllm-wiki SOP 月度审查

**審查月份**: $REVIEW_MONTH  
**審查日期**: $REVIEW_DATE  
**審查者**: Red Agent Team

---

## 📊 健康分趨勢

| 週次 | 健康分 | 等級 |
|------|--------|------|
| 本週 | - | $HEALTH_STATUS |

**趨勢**: <!-- 填写↑/↓/→ -->

---

## ⏰ 定時任務執行

| 指标 | 数值 | 状态 |
|------|------|------|
| Crontab 任务数 | $CRON_TASKS | $([ $CRON_TASKS -eq 10 ] && echo "✅" || echo "⚠️") |
| 本周备份 | $BACKUP_DAYS 次 | $([ $BACKUP_DAYS -ge 5 ] && echo "✅" || echo "⚠️") |
| Ingest 执行 | $INGEST_COUNT 次 | $([ $INGEST_COUNT -gt 0 ] && echo "✅" || echo "⚠️") |

---

## 📝 脚本完整性

$(if [ ${#MISSING_SCRIPTS[@]} -eq 0 ]; then
    echo "| 脚本 | 状态 |"
    echo "|------|------|"
    echo "| generate-weekly-report.sh | ✅ 可执行 |"
    echo "| generate-monthly-report.sh | ✅ 可执行 |"
    echo "| auto-audit.sh | ✅ 可执行 |"
    echo "| review-health-sop.sh | ✅ 可执行 |"
else
    echo "⚠️ 缺失/不可执行脚本:"
    for script in "${MISSING_SCRIPTS[@]}"; do
        echo "- ❌ $script"
    done
fi)

---

## 📈 指標達成率

| 指标 | 目标 | 实际 | 状态 |
|------|------|------|------|
| 日更新量 | ≥18 条/天 | - | <!-- 填写 --> |
| 周 Lint 完成率 | 100% | - | <!-- 填写 --> |
| 月增长率 | ≥30% | - | <!-- 填写 --> |
| 自动化率 | ≥80% | ${CRON_TASKS}0% | $([ $CRON_TASKS -ge 8 ] && echo "✅" || echo "⚠️") |

---

## ⚠️ 發現問題

$(if [ ${#MISSING_SCRIPTS[@]} -gt 0 ]; then
    echo "- ❌ 脚本缺失/不可执行：${MISSING_SCRIPTS[*]}"
else
    echo "- ✅ 无脚本问题"
fi)

$(if [ $ORPHAN_COUNT -gt 0 ]; then
    echo "- ⚠️ 孤页：$ORPHAN_COUNT 个"
else
    echo "- ✅ 无孤页"
fi)

---

## 📋 優化建議

<!-- 手动填写优化建议 -->

- [ ] ...

---

## 🎯 下月重點

<!-- 手动填写下月重点 -->

- [ ] ...

---

**下次審查**: $(date -d "+1 month" +%Y-%m-21 2>/dev/null || date -v+1m +%Y-%m-21 2>/dev/null || echo "下月 21 日")

**生成**: RedAgentTeamllm-wiki SOP Auto-Reviewer
EOF

log "✅ SOP 审查完成"
log "  报告：$REPORT_FILE"

# 5. 飞书通知 (如配置)
if [ -n "$FEISHU_WEBHOOK" ]; then
    log "  发送飞书通知..."
    curl -s -X POST "$FEISHU_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "{
            \"msg_type\": \"text\",
            \"content\": {
                \"text\": \"📊 SOP 月度审查完成\\n月份：$REVIEW_MONTH\\n健康状态：$HEALTH_STATUS\\n报告：$REPORT_FILE\"
            }
        }"
    log "✅ 飞书通知已发送"
else
    log "ℹ️ 飞书 Webhook 未配置，跳过通知"
fi

exit 0

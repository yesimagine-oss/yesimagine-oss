#!/bin/bash
# RedAgentTeamllm-wiki 周报生成脚本
# 执行时间：每周日 06:00
# 功能：汇总本周更新量、健康分趋势、P0/P1 问题

set -e

# 配置
WIKI_ROOT="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki"
REPORTS_DIR="$WIKI_ROOT/reports"
LOG_FILE="$WIKI_ROOT/logs/weekly-report.log"
WEEK=$(date +%Y-W%V)
WEEK_START=$(date -d "last Sunday" +%Y-%m-%d 2>/dev/null || date -v-sun +%Y-%m-%d 2>/dev/null || echo "unknown")

# 确保目录存在
mkdir -p "$REPORTS_DIR"
mkdir -p "$(dirname $LOG_FILE)"

log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

log "🚀 开始生成周报 ($WEEK)"

# 1. 统计本周更新量
log "  统计本周更新量..."
WEEKLY_COUNT=$(find "$WIKI_ROOT/wiki" -name "*.md" -type f -mtime -7 | wc -l)
RAW_COUNT=$(find "$WIKI_ROOT/raw" -name "*.md" -type f -mtime -7 | wc -l)

# 2. 获取最新 Lint 报告
log "  获取健康数据..."
LATEST_LINT=$(ls -t "$REPORTS_DIR"/lint-weekly-*.md 2>/dev/null | head -1)
if [ -n "$LATEST_LINT" ] && [ -f "$LATEST_LINT" ]; then
    ORPHAN_COUNT=$(grep "孤頁：" "$LATEST_LINT" 2>/dev/null | grep -oP '\d+' | head -1 || echo 0)
    CONTRADICT_COUNT=$(grep "矛盾：" "$LATEST_LINT" 2>/dev/null | grep -oP '\d+' | head -1 || echo 0)
    HEALTH_STATUS=$(grep "評級:" "$LATEST_LINT" 2>/dev/null | cut -d':' -f2 | xargs || echo "Unknown")
else
    ORPHAN_COUNT=0
    CONTRADICT_COUNT=0
    HEALTH_STATUS="No lint report"
fi

# 3. 生成周报
REPORT_FILE="$REPORTS_DIR/weekly-report-$WEEK.md"
log "  生成报告：$REPORT_FILE"

cat > "$REPORT_FILE" << EOF
# RedAgentTeamllm-wiki 周报

**週次**: $WEEK  
**生成時間**: $(date -Iseconds)  
**統計區間**: $WEEK_START 至今

---

## 📊 更新統計

| 目錄 | 本週新增 |
|------|---------|
| wiki/ | $WEEKLY_COUNT |
| raw/ | $RAW_COUNT |
| **總計** | $((WEEKLY_COUNT + RAW_COUNT)) |

---

## 🏥 健康狀態

| 指標 | 數值 | 狀態 |
|------|------|------|
| 孤頁 | $ORPHAN_COUNT | $([ $ORPHAN_COUNT -eq 0 ] && echo "✅" || echo "⚠️") |
| 矛盾 | $CONTRADICT_COUNT | $([ $CONTRADICT_COUNT -eq 0 ] && echo "✅" || echo "⚠️") |
| 評級 | $HEALTH_STATUS | - |

---

## 📝 本週重點

<!-- 手動填寫本週重點工作 -->

- [ ] ...

---

## 📋 下週計劃

<!-- 手動填寫下週計劃 -->

- [ ] ...

---

**生成**: RedAgentTeamllm-wiki Auto-Reporter
EOF

log "✅ 周报生成完成"
log "  文件：$REPORT_FILE"
log "  更新量：$((WEEKLY_COUNT + RAW_COUNT))"
log "  健康状态：$HEALTH_STATUS"

exit 0

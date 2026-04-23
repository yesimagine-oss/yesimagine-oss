#!/bin/bash
# AgentTeamllm-wiki 自動 Lint 檢查腳本
# 執行時間：每週日 01:00
# 功能：完整系統健康檢查

set -e

# 配置
WORKSPACE_ROOT="/home/admin/.openclaw/workspace"
WIKI_ROOT="$WORKSPACE_ROOT/RedAgentTeamllm-wiki"
WIKI_DIR="$WIKI_ROOT/wiki"
REPORTS_DIR="$WIKI_ROOT/reports"
LOG_FILE="$WIKI_ROOT/log.md"
SUNDAY=$(date +%Y-%m-%d)
WEEK=$(date +%Y-W%V)

echo "[$(date -Iseconds)] 開始自動 Lint 檢查..."

# 初始化報告
REPORT_FILE="$REPORTS_DIR/lint-weekly-$WEEK.md"
cat > "$REPORT_FILE" << EOF
# AgentTeamllm-wiki 每週 Lint 報告

**週次:** $WEEK  
**生成時間:** $(date -Iseconds)  
**檢查範圍:** $WIKI_DIR

---

## 📊 檢查結果

EOF

# 1. 矛盾內容檢測 (簡化版 - 關鍵詞)
echo "  檢查矛盾內容..."
CONTRADICT_COUNT=0
CONTRADICT_FILES=""

for file in "$WIKI_DIR"/*.md; do
    if [ -f "$file" ]; then
        # 簡單關鍵詞檢測 (待優化)
        if grep -q "矛盾\|conflict\|contradiction" "$file" 2>/dev/null; then
            CONTRADICT_COUNT=$((CONTRADICT_COUNT + 1))
            CONTRADICT_FILES="$CONTRADICT_FILES\n- $(basename $file)"
        fi
    fi
done

cat >> "$REPORT_FILE" << EOF
### 矛盾內容

**數量:** $CONTRADICT_COUNT  
**文件:** $CONTRADICT_FILES

---

EOF

# 2. 孤頁檢測
echo "  檢查孤頁..."
ORPHAN_COUNT=0
# 使用 Wiki 層索引而非全局索引
INDEX_FILE="$WIKI_DIR/index.md"

# 如果 Wiki 索引不存在，使用全局索引
if [ ! -f "$INDEX_FILE" ]; then
    INDEX_FILE="$WIKI_ROOT/index.md"
fi

for file in "$WIKI_DIR"/*.md; do
    if [ -f "$file" ] && [ "$file" != "$INDEX_FILE" ]; then
        filename=$(basename "$file" .md)
        # 檢查文件名是否在索引中被引用 (支持多種格式)
        if ! grep -qi "$filename" "$INDEX_FILE" 2>/dev/null; then
            ORPHAN_COUNT=$((ORPHAN_COUNT + 1))
            echo "    孤頁：$filename"
        fi
    fi
done

cat >> "$REPORT_FILE" << EOF
### 孤頁檢測

**數量:** $ORPHAN_COUNT  
**狀態:** $([ $ORPHAN_COUNT -eq 0 ] && echo "✅ 無孤頁" || echo "⚠️ 需加入索引")

---

EOF

# 3. 過時內容檢測 (>30 天未更新)
echo "  檢查過時內容..."
OUTDATED_COUNT=0
THRESHOLD=$(date -d "30 days ago" +%s 2>/dev/null || date -v-30d +%s 2>/dev/null || echo 0)

for file in "$WIKI_DIR"/*.md "$WIKI_ROOT"/raw/*.md "$WIKI_ROOT"/reports/*.md; do
    if [ -f "$file" ]; then
        mtime=$(stat -f%m "$file" 2>/dev/null || stat -c%Y "$file" 2>/dev/null || echo 0)
        if [ "$mtime" -lt "$THRESHOLD" ] && [ "$THRESHOLD" -gt 0 ]; then
            OUTDATED_COUNT=$((OUTDATED_COUNT + 1))
        fi
    fi
done

cat >> "$REPORT_FILE" << EOF
### 過時內容 (>30 天)

**數量:** $OUTDATED_COUNT  
**狀態:** $([ $OUTDATED_COUNT -eq 0 ] && echo "✅ 無過時" || echo "⚠️ 需歸檔")

---

EOF

# 4. 系統統計
echo "  生成統計..."
WIKI_COUNT=$(find "$WIKI_DIR" -name "*.md" | wc -l)
RAW_COUNT=$(find "$WIKI_ROOT/raw" -name "*.md" 2>/dev/null | wc -l)
REPORT_COUNT=$(find "$REPORTS_DIR" -name "*.md" 2>/dev/null | wc -l)

cat >> "$REPORT_FILE" << EOF
## 📈 系統統計

| 目錄 | 文件數 |
|------|--------|
| wiki/ | $WIKI_COUNT |
| raw/ | $RAW_COUNT |
| reports/ | $REPORT_COUNT |
| **總計** | $((WIKI_COUNT + RAW_COUNT + REPORT_COUNT)) |

---

## ✅ 整體健康

**矛盾:** $CONTRADICT_COUNT | **孤頁:** $ORPHAN_COUNT | **過時:** $OUTDATED_COUNT

**評級:** $([ $ORPHAN_COUNT -eq 0 ] && [ $CONTRADICT_COUNT -lt 5 ] && echo "Excellent ✅" || ([ $ORPHAN_COUNT -lt 10 ] && echo "Good ✅" || echo "Needs Attention ⚠️"))

---

**生成:** AgentTeamllm-wiki Auto-Lint
EOF

# 更新日誌
TIMESTAMP=$(date -Iseconds)
LOG_ENTRY="
## $TIMESTAMP - 自動 Lint 檢查

**週次:** $WEEK
**結果:** 矛盾=$CONTRADICT_COUNT, 孤頁=$ORPHAN_COUNT, 過時=$OUTDATED_COUNT
**報告:** $REPORT_FILE
**狀態:** ✅ 完成

---
"

if [ -f "$LOG_FILE" ]; then
    echo "$LOG_ENTRY" | cat - "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
else
    echo "$LOG_ENTRY" > "$LOG_FILE"
fi

echo "[$(date -Iseconds)] Lint 檢查完成"
echo "  報告：$REPORT_FILE"
echo "  矛盾：$CONTRADICT_COUNT | 孤頁：$ORPHAN_COUNT | 過時：$OUTDATED_COUNT"

exit 0

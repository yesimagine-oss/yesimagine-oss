#!/bin/bash
# RedAgentTeamllm-wiki 月度深度审计脚本
# 执行时间：每月 1 日 02:00
# 功能：深度审计 + 归档>3 个月未更新文件

set -e

# 配置
WIKI_ROOT="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki"
ARCHIVE_DIR="$WIKI_ROOT/archive/$(date +%Y-%m)"
REPORTS_DIR="$WIKI_ROOT/reports"
LOG_FILE="$WIKI_ROOT/logs/audit.log"
AUDIT_MONTH=$(date +%Y-%m)

# 确保目录存在
mkdir -p "$ARCHIVE_DIR"
mkdir -p "$REPORTS_DIR"
mkdir -p "$(dirname $LOG_FILE)"

log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

log "🚀 开始月度审计 ($AUDIT_MONTH)"

# 1. 统计文件总数
log "  统计文件数量..."
TOTAL_FILES=$(find "$WIKI_ROOT" -name "*.md" -type f | wc -l)

# 2. 查找>3 个月未更新的文件
log "  查找过期文件 (>90 天未更新)..."
THRESHOLD=$(date -d "90 days ago" +%s 2>/dev/null || date -v-90d +%s 2>/dev/null || echo 0)
OLD_FILES=()
ARCHIVE_COUNT=0

while IFS= read -r file; do
    if [ -f "$file" ]; then
        mtime=$(stat -c%Y "$file" 2>/dev/null || stat -f%m "$file" 2>/dev/null || echo 0)
        if [ "$mtime" -lt "$THRESHOLD" ] && [ "$THRESHOLD" -gt 0 ]; then
            OLD_FILES+=("$file")
            ARCHIVE_COUNT=$((ARCHIVE_COUNT + 1))
        fi
    fi
done < <(find "$WIKI_ROOT/wiki" "$WIKI_ROOT/raw" -name "*.md" -type f 2>/dev/null)

log "  发现过期文件：$ARCHIVE_COUNT 个"

# 3. 归档旧文件 (移动而非删除)
if [ $ARCHIVE_COUNT -gt 0 ]; then
    log "  开始归档..."
    for file in "${OLD_FILES[@]}"; do
        rel_path="${file#$WIKI_ROOT/}"
        archive_path="$ARCHIVE_DIR/$rel_path"
        mkdir -p "$(dirname "$archive_path")"
        mv "$file" "$archive_path"
        log "    归档：$rel_path"
    done
    log "✅ 归档完成 ($ARCHIVE_COUNT 个文件)"
else
    log "  无需归档"
fi

# 4. 深度审计
log "  执行深度审计..."

# 检查索引完整性
INDEX_FILE="$WIKI_ROOT/wiki/index.md"
ORPHAN_COUNT=0
if [ -f "$INDEX_FILE" ]; then
    for file in "$WIKI_ROOT/wiki"/*.md; do
        if [ -f "$file" ] && [ "$file" != "$INDEX_FILE" ]; then
            filename=$(basename "$file" .md)
            if ! grep -qi "$filename" "$INDEX_FILE" 2>/dev/null; then
                ORPHAN_COUNT=$((ORPHAN_COUNT + 1))
            fi
        fi
    done
fi

# 检查 Git 状态
cd "$WIKI_ROOT"
GIT_STATUS=$(git status --porcelain 2>/dev/null | wc -l)

# 5. 生成审计报告
REPORT_FILE="$REPORTS_DIR/audit-$AUDIT_MONTH.md"
log "  生成报告：$REPORT_FILE"

cat > "$REPORT_FILE" << EOF
# RedAgentTeamllm-wiki 月度审计报告

**月份**: $AUDIT_MONTH  
**生成時間**: $(date -Iseconds)

---

## 📊 审计结果

### 文件统计

| 项目 | 数量 |
|------|------|
| 审计前文件总数 | $TOTAL_FILES |
| 归档文件数 | $ARCHIVE_COUNT |
| 归档后文件总数 | $((TOTAL_FILES - ARCHIVE_COUNT)) |

### 健康检查

| 检查项 | 结果 | 状态 |
|--------|------|------|
| 孤页数量 | $ORPHAN_COUNT | $([ $ORPHAN_COUNT -eq 0 ] && echo "✅" || echo "⚠️") |
| Git 未提交 | $GIT_STATUS | $([ $GIT_STATUS -eq 0 ] && echo "✅" || echo "⚠️") |
| 归档目录 | $ARCHIVE_DIR | ✅ |

---

## 📁 归档详情

**归档位置**: \`$ARCHIVE_DIR\`

$(if [ $ARCHIVE_COUNT -gt 0 ]; then
    echo "| 文件路径 | 最后更新 |"
    echo "|---------|---------|"
    for file in "${OLD_FILES[@]}"; do
        mtime=$(stat -c%y "$file" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
        echo "| $file | $mtime |"
    done
else
    echo "本月无需归档文件。"
fi)

---

## ⚠️ 发现问题

$(if [ $ORPHAN_COUNT -gt 0 ]; then
    echo "- ⚠️ 发现 $ORPHAN_COUNT 个孤页，建议加入索引"
else
    echo "- ✅ 无孤页"
fi)

$(if [ $GIT_STATUS -gt 0 ]; then
    echo "- ⚠️ 有 $GIT_STATUS 个未提交变更，建议 Git 提交"
else
    echo "- ✅ Git 已同步"
fi)

---

## 📋 建议操作

- [ ] 检查归档文件是否可删除
- [ ] 更新索引 (如有孤页)
- [ ] Git 提交变更

---

**生成**: RedAgentTeamllm-wiki Auto-Audit
EOF

log "✅ 月度审计完成"
log "  报告：$REPORT_FILE"
log "  归档：$ARCHIVE_COUNT 个文件"
log "  孤页：$ORPHAN_COUNT 个"

exit 0

#!/bin/bash
# 知識庫衝突檢測腳本
# 功能：檢查新文件與現有知識是否矛盾
# 用法：bash scripts/conflict-check.sh <新文件路徑> [知識庫目錄]
# 示例：bash scripts/conflict-check.sh ~/new-doc.md ~/wiki/

set -e

# 配置
WIKI_DIR="${2:-/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki}"
LOG_FILE="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/conflict-check.log"
mkdir -p "$(dirname "$LOG_FILE")"

# 日誌函數
log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

# 提取關鍵詞
extract_keywords() {
    local file="$1"
    # 提取標題、關鍵詞、重要概念
    grep -oE '[A-Za-z0-9_]{3,}' "$file" 2>/dev/null | \
    sort | uniq -c | sort -rn | head -50 | awk '{print $2}'
}

# 提取矛盾標記（排除標題和表格）
extract_conflicts() {
    local file="$1"
    grep -iE "^矛盾|^衝突|^不匹配|^不一致|deprecated|outdated|not recommend" "$file" 2>/dev/null || true
}

# 檢查文件名衝突
check_filename_conflict() {
    local new_file="$1"
    local basename=$(basename "$new_file")
    local found=$(find "$WIKI_DIR" -name "$basename" 2>/dev/null | grep -v "$new_file" | head -5)
    
    if [ -n "$found" ]; then
        log "⚠️ 文件名衝突: '$basename'"
        log "   已存在於:"
        echo "$found" | while read f; do
            log "     - $f"
        done
        return 1
    fi
    return 0
}

# 檢查關鍵詞衝突
check_keyword_conflict() {
    local new_file="$1"
    local keywords=$(extract_keywords "$new_file")
    local conflicts=0
    
    log "🔍 關鍵詞衝突檢查..."
    
    for keyword in $keywords; do
        # 搜索現有知識庫
        local matches=$(grep -rl "$keyword" "$WIKI_DIR" --include="*.md" 2>/dev/null | head -5)
        if [ -n "$matches" ]; then
            # 檢查是否有矛盾內容
            local conflict_text=$(extract_conflicts "$new_file")
            if [ -n "$conflict_text" ]; then
                log "⚠️ 潛在矛盾關鍵詞: '$keyword'"
                log "   矛盾內容:"
                echo "$conflict_text" | head -3 | while read line; do
                    log "     - $line"
                done
                conflicts=$((conflicts + 1))
            fi
        fi
    done
    
    if [ $conflicts -eq 0 ]; then
        log "✅ 無關鍵詞衝突"
    else
        log "⚠️ 發現 $conflicts 個潛在衝突"
    fi
    
    return 0
}

# 檢查內容相似度（簡單版）
check_similarity() {
    local new_file="$1"
    local new_content=$(cat "$new_file" | tr '[:upper:]' '[:lower:]' | tr -d '[:punct:]' | tr -s ' ')
    local new_words=$(echo "$new_content" | wc -w)
    
    log "🔍 內容相似度檢查..."
    
    # 查找相似文件（基於前 100 個單詞）
    local first_words=$(echo "$new_content" | tr ' ' '\n' | head -100 | tr '\n' ' ')
    
    for wiki_file in $(find "$WIKI_DIR" -name "*.md" -not -path "*/11-archive/*" -not -path "*/10-raw/*" 2>/dev/null | head -50); do
        local wiki_content=$(cat "$wiki_file" | tr '[:upper:]' '[:lower:]' | tr -d '[:punct:]' | tr -s ' ')
        local wiki_first=$(echo "$wiki_content" | tr ' ' '\n' | head -100 | tr '\n' ' ')
        
        # 計算共同詞數量
        local common=0
        for word in $first_words; do
            if echo "$wiki_first" | grep -q "\b$word\b" 2>/dev/null; then
                common=$((common + 1))
            fi
        done
        
        # 如果共同詞 > 30%，標記為相似
        if [ $common -gt 30 ]; then
            local similarity=$((common * 100 / ${#first_words[@]:-100}))
            log "📄 相似文件: $(basename $wiki_file) (相似度 ~$similarity%)"
        fi
    done
    
    log "✅ 相似度檢查完成"
}

# 主函數
main() {
    local new_file="$1"
    
    if [ ! -f "$new_file" ]; then
        log "❌ 文件不存在: $new_file"
        exit 1
    fi
    
    log "========== 衝突檢測 =========="
    log "📄 新文件: $new_file"
    log "📚 知識庫: $WIKI_DIR"
    
    local failed=0
    
    # 1. 文件名衝突
    check_filename_conflict "$new_file" || failed=1
    
    # 2. 關鍵詞衝突
    check_keyword_conflict "$new_file"
    
    # 3. 內容相似度
    check_similarity "$new_file"
    
    # 總結
    log ""
    if [ $failed -eq 1 ]; then
        log "🔴 檢測結果：有文件名衝突，請確認是否覆蓋"
    else
        log "🟢 檢測結果：無嚴重衝突，可以入庫"
    fi
    
    log "================================"
}

main "$@"

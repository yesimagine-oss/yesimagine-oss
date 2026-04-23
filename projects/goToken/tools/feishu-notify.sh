#!/bin/bash

# goToken - Feishu 通知腳本
# 功能：發送命中率警告、未命中提醒到飛書

FEISHU_WEBHOOK="${FEISHU_WEBHOOK:-}"  # 環境變量
LOG_FILE="/home/admin/.openclaw/workspace/goToken/logs/misses.log"
METRICS_FILE="/home/admin/.openclaw/workspace/goToken/logs/metrics.json"

# 發送飛書消息
send_feishu() {
    local title="$1"
    local content="$2"
    local color="$3"  # red/yellow/green
    
    if [ -z "$FEISHU_WEBHOOK" ]; then
        echo "⚠️ FEISHU_WEBHOOK 未設置"
        return 1
    fi
    
    curl -s -X POST "$FEISHU_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "{
            \"msg_type\": \"interactive\",
            \"card\": {
                \"header\": {
                    \"title\": {
                        \"tag\": \"plain_text\",
                        \"content\": \"$title\"
                    },
                    \"template\": \"$color\"
                },
                \"elements\": [
                    {
                        \"tag\": \"markdown\",
                        \"content\": \"$content\"
                    }
                ]
            }
        }"
}

# 檢查命中率
check_hit_rate() {
    if [ ! -f "$METRICS_FILE" ]; then
        return
    fi
    
    local hit_rate=$(jq -r '.hit_rate' "$METRICS_FILE")
    local total=$(jq -r '.total_requests' "$METRICS_FILE")
    
    if [ "$hit_rate" \< 75 ]; then
        send_feishu "🔴 goToken 命中率警告" \
            "**命中率低於 75%**\n\n當前：${hit_rate}%\n總請求：${total}\n\n建議：立即優化閾值或增加模板" \
            "red"
    elif [ "$hit_rate" \< 80 ]; then
        send_feishu "🟡 goToken 命中率提醒" \
            "**命中率低於 80%**\n\n當前：${hit_rate}%\n總請求：${total}\n\n建議：收集真實數據訓練" \
            "yellow"
    fi
}

# 檢查未命中累積
check_misses() {
    if [ ! -f "$LOG_FILE" ]; then
        return
    fi
    
    local miss_count=$(wc -l < "$LOG_FILE")
    
    if [ "$miss_count" -ge 20 ]; then
        local recent_misses=$(tail -10 "$LOG_FILE")
        send_feishu "🟢 goToken 新問題累積" \
            "**未命中問題累積 ${miss_count} 個**\n\n最近 10 個:\n\`\`\`${recent_misses}\`\`\`\n\n建議：加入模板庫或訓練集" \
            "yellow"
        
        # 重置日誌
        > "$LOG_FILE"
    fi
}

# 記錄未命中
log_miss() {
    local query="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $query" >> "$LOG_FILE"
}

# 更新指標
update_metrics() {
    local total="$1"
    local hits="$2"
    local hit_rate=$(echo "scale=2; $hits * 100 / $total" | bc)
    
    cat > "$METRICS_FILE" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "total_requests": $total,
  "cache_hits": $hits,
  "cache_misses": $((total - hits)),
  "hit_rate": $hit_rate
}
EOF
}

# 主程序
case "$1" in
    check)
        check_hit_rate
        check_misses
        ;;
    miss)
        log_miss "$2"
        ;;
    metrics)
        update_metrics "$2" "$3"
        ;;
    test)
        send_feishu "🧪 goToken 測試通知" \
            "**Feishu 通知測試**\\n\n時間：$(date)\n狀態：正常" \
            "green"
        ;;
    *)
        echo "Usage: $0 {check|miss <query>|metrics <total> <hits>|test}"
        ;;
esac

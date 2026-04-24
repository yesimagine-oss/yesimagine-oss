#!/bin/bash
# RedAgentTeamllm-wiki 健康告警腳本
# 功能：監控健康分數、自動通知 (Feishu/郵件)
# 執行間隔：每日 06:00

set -e

# 配置
WORKSPACE_ROOT="/home/admin/.openclaw/workspace"
WIKI_ROOT="$WORKSPACE_ROOT/RedAgentTeamllm-wiki"
REPORTS_DIR="$WIKI_ROOT/reports"
LOG_FILE="$WIKI_ROOT/log.md"
ALERT_LOG="$WIKI_ROOT/alerts.md"

# 告警閾值 (根據知識庫健康標準)
HEALTH_WARNING=80    # 🟡 警告：<80 容易產生隱患
HEALTH_CRITICAL=75   # 🔴 危險：<75 健康度不合格

# 通知配置 (需用戶填寫)
FEISHU_WEBHOOK=""  # 飛書機器人 Webhook
EMAIL_RECIPIENT="" # 郵件地址

# 日誌函數
log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

# 計算健康分
calculate_health_score() {
    local lint_score=100
    local ops_score=100
    
    # 獲取最新 Lint 報告
    local latest_lint=$(ls -t "$REPORTS_DIR"/lint-weekly-*.md 2>/dev/null | head -1)
    
    if [ -n "$latest_lint" ]; then
        # 孤頁率 (每 1 孤頁扣 5 分)
        local orphan_count=$(grep "孤頁：" "$latest_lint" | grep -oP '\d+' | head -1 || echo 0)
        lint_score=$((lint_score - orphan_count * 5))
        
        # 矛盾數 (每個扣 10 分)
        local contradict_count=$(grep "矛盾：" "$latest_lint" | grep -oP '\d+' | head -1 || echo 0)
        lint_score=$((lint_score - contradict_count * 10))
        
        # 過時數 (每個扣 3 分)
        local outdated_count=$(grep "過時：" "$latest_lint" | grep -oP '\d+' | head -1 || echo 0)
        lint_score=$((lint_score - outdated_count * 3))
    fi
    
    # 確保分數不低於 0
    [ $lint_score -lt 0 ] && lint_score=0
    [ $ops_score -lt 0 ] && ops_score=0
    
    # 綜合健康分 (Lint 40% + 运维 60%)
    local health_score=$(( (lint_score * 40 + ops_score * 60) / 100 ))
    
    echo $health_score
}

# 確定健康等級
get_health_level() {
    local score=$1
    
    if [ $score -ge 90 ]; then
        echo "🟢 优秀"
    elif [ $score -ge 75 ]; then
        echo "🟡 良好"
    elif [ $score -ge 60 ]; then
        echo "🟠 一般"
    else
        echo "🔴 警告"
    fi
}

# 發送飛書通知
send_feishu_alert() {
    local level=$1
    local score=$2
    local message=$3
    
    if [ -z "$FEISHU_WEBHOOK" ]; then
        log "⚠️ 飛書 Webhook 未配置，跳過通知"
        return
    fi
    
    local color="green"
    [ "$level" = "🟡 良好" ] && color="yellow"
    [ "$level" = "🟠 一般" ] && color="orange"
    [ "$level" = "🔴 警告" ] && color="red"
    
    curl -s -X POST "$FEISHU_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "{
            \"msg_type\": \"interactive\",
            \"card\": {
                \"header\": {
                    \"title\": {
                        \"tag\": \"plain_text\",
                        \"content\": \"📊 知識庫健康告警\"
                    },
                    \"template\": \"$color\"
                },
                \"elements\": [
                    {
                        \"tag\": \"div\",
                        \"text\": {
                            \"tag\": \"markdown\",
                            \"content\": \"**健康分**: $score\\n**等級**: $level\\n\\n$message\"
                        }
                    }
                ]
            }
        }"
    
    log "✅ 飛書通知已發送"
}

# 發送郵件通知
send_email_alert() {
    local level=$1
    local score=$2
    local message=$3
    
    if [ -z "$EMAIL_RECIPIENT" ]; then
        log "⚠️ 郵件地址未配置，跳過通知"
        return
    fi
    
    echo "$message" | mail -s "[RedAgentTeamllm-wiki] 健康告警 - $level (分數：$score)" "$EMAIL_RECIPIENT"
    log "✅ 郵件通知已發送"
}

# 記錄告警
log_alert() {
    local level=$1
    local score=$2
    local message=$3
    local timestamp=$(date -Iseconds)
    
    cat >> "$ALERT_LOG" << EOF
## $timestamp - 健康告警

**等級**: $level  
**分數**: $score  
**詳情**: $message

---
EOF
}

# 主函數
main() {
    log "🚀 健康告警檢查啟動"
    
    # 計算健康分
    local health_score=$(calculate_health_score)
    local health_level=$(get_health_level $health_score)
    
    log "📊 當前健康分：$health_score ($health_level)"
    
    # 判斷是否需要告警
    if [ $health_score -lt $HEALTH_CRITICAL ]; then
        # 🔴 危險 - 立即通知
        local message="健康分低於臨界值 ($HEALTH_CRITICAL)，需要立即處理！\n\n建議操作:\n1. 檢查 Lint 報告\n2. 處理孤頁/矛盾/過時內容\n3. 補充知識更新"
        
        log_alert "$health_level" "$health_score" "$message"
        send_feishu_alert "$health_level" "$health_score" "$message"
        send_email_alert "$health_level" "$health_score" "$message"
        
        log "🔴 已發送危急告警"
        
    elif [ $health_score -lt $HEALTH_WARNING ]; then
        # 🟡 警告 - 通知
        local message="健康分低於警告線 ($HEALTH_WARNING)，建議關注。\n\n建議操作:\n1. 查看最新 Lint 報告\n2. 檢查日更新量是否達標"
        
        log_alert "$health_level" "$health_score" "$message"
        send_feishu_alert "$health_level" "$health_score" "$message"
        
        log "🟡 已發送警告通知"
        
    else
        # 🟢 正常 - 僅記錄
        log "✅ 健康狀態正常，無需告警"
    fi
    
    log "📝 告警檢查完成"
}

# 執行
main "$@"

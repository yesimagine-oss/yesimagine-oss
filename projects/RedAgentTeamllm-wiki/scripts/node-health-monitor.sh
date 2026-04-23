#!/bin/bash
# Node 健康監控與自動重連腳本
# 功能：監控節點狀態、自動重連、狀態上報
# 執行間隔：每 30 秒

set -e

# 配置
WORKSPACE_ROOT="/home/admin/.openclaw/workspace"
LOG_DIR="$WORKSPACE_ROOT/AgentTeamllm-wiki/logs"
LOG_FILE="$LOG_DIR/node-monitor.log"
STATE_FILE="$LOG_DIR/.node-state.json"
HEALTH_CHECK_INTERVAL=30
MAX_RECONNECT_ATTEMPTS=5
RECONNECT_DELAY=5

# 確保日誌目錄存在
mkdir -p "$LOG_DIR"

# 日誌函數
log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

# 檢查節點狀態
check_node_status() {
    local status=$(openclaw nodes status 2>&1 || echo "error")
    if echo "$status" | grep -q '"nodes":\s*\[\]'; then
        return 1  # 節點離線
    else
        return 0  # 節線在線
    fi
}

# 嘗試重連節點
reconnect_node() {
    local attempt=$1
    log "🔄 嘗試重連節點 (第 $attempt/$MAX_RECONNECT_ATTEMPTS 次)..."
    
    # 檢查是否有配對的節點
    local pairing_status=$(openclaw nodes describe 2>&1 || echo "no nodes paired")
    
    if echo "$pairing_status" | grep -q "no nodes paired\|empty"; then
        log "⚠️ 無已配對節點，需要重新配對"
        # 這裡可以添加自動配對邏輯（需要用戶確認）
        return 1
    fi
    
    # 嘗試重新連接
    log "📡 發送節點狀態請求..."
    local status=$(openclaw nodes status 2>&1)
    
    if echo "$status" | grep -q '"nodes":\s*\[\]'; then
        log "❌ 重連失敗，節點仍離線"
        return 1
    else
        log "✅ 重連成功，節點已在線"
        return 0
    fi
}

# 更新狀態文件
update_state() {
    local status=$1
    local timestamp=$(date -Iseconds)
    cat > "$STATE_FILE" << EOF
{
    "last_check": "$timestamp",
    "status": "$status",
    "reconnect_attempts": 0,
    "uptime": "$(uptime -p 2>/dev/null || echo "unknown")"
}
EOF
}

# 主循環
main() {
    log "🚀 Node 健康監控啟動"
    log "📊 檢查間隔：${HEALTH_CHECK_INTERVAL}秒"
    log "🔄 最大重連次數：$MAX_RECONNECT_ATTEMPTS"
    
    local consecutive_failures=0
    local reconnect_count=0
    
    while true; do
        # 檢查節點狀態
        if check_node_status; then
            log "✅ 節點狀態：在線"
            consecutive_failures=0
            reconnect_count=0
            update_state "online"
        else
            log "❌ 節點狀態：離線"
            consecutive_failures=$((consecutive_failures + 1))
            
            # 嘗試重連
            if [ $reconnect_count -lt $MAX_RECONNECT_ATTEMPTS ]; then
                reconnect_count=$((reconnect_count + 1))
                sleep $RECONNECT_DELAY
                if reconnect_node $reconnect_count; then
                    consecutive_failures=0
                    reconnect_count=0
                fi
            else
                log "🔴 重連失敗已達上限 ($MAX_RECONNECT_ATTEMPTS 次)，等待手動干預"
                update_state "offline_max_retries"
                # 等待更長時間後重試
                sleep 300
                reconnect_count=0
            fi
        fi
        
        sleep $HEALTH_CHECK_INTERVAL
    done
}

# 啟動監控
main

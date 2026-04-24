#!/bin/bash
set -e

# 配置
EVOLVER_BIN="/usr/bin/evolver"
EVOLVER_DIR="/home/admin/.openclaw/workspace"
LOG_DIR="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs"
LOG_FILE="$LOG_DIR/evolver-monitor.log"
PID_FILE="$LOG_DIR/.evolver.pid"
HEALTH_CHECK_INTERVAL=60
MAX_RESTART_ATTEMPTS=3
RESTART_DELAY=10

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

check_paths() {
    local failed=0
    
    if [ ! -d "$EVOLVER_DIR" ]; then
        log "🔴 CRITICAL: EVOLVER_DIR 不存在: $EVOLVER_DIR"
        failed=1
    fi
    
    if [ ! -f "$EVOLVER_BIN" ]; then
        log "🔴 CRITICAL: Evolver 二進制不存在: $EVOLVER_BIN"
        failed=1
    fi
    
    if [ ! -d "$LOG_DIR" ]; then
        log "🔴 CRITICAL: LOG_DIR 不存在: $LOG_DIR"
        failed=1
    fi
    
    local mem_dir="/home/admin/.openclaw/workspace/memory/evolution"
    if [ -d "$mem_dir" ] && [ ! -w "$mem_dir" ]; then
        log "🔴 CRITICAL: memory/evolution/ 無寫入權限"
        failed=1
    fi
    
    if [ $failed -eq 1 ]; then
        log "🔴 路徑檢查失敗，Evolver 無法啟動"
        exit 1
    fi
    
    log "✅ 路徑檢查通過"
}

check_evolver_process() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        fi
    fi
    if pgrep -f "node.*index.js.*run\|node.*index.js.*loop" > /dev/null 2>&1; then
        return 0
    fi
    return 1
}

start_evolver() {
    log "🚀 啟動 Evolver (全局 1.69.16)..."
    cd "$EVOLVER_DIR"
    
    nohup $EVOLVER_BIN run --loop > "$LOG_DIR/evolver-run.log" 2>&1 &
    local pid=$!
    echo $pid > "$PID_FILE"
    
    log "✅ Evolver 已啟動 (PID: $pid)"
    
    sleep 5
    
    if ps -p "$pid" > /dev/null 2>&1; then
        log "✅ Evolver 運行正常"
        return 0
    else
        log "❌ Evolver 啟動失敗"
        return 1
    fi
}

restart_evolver() {
    local attempt=$1
    log "🔄 嘗試重啟 Evolver (第 $attempt/$MAX_RESTART_ATTEMPTS 次)..."
    
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            kill "$pid" 2>/dev/null || true
            sleep 2
        fi
    fi
    
    pkill -f "node.*index.js.*run" 2>/dev/null || true
    sleep 2
    
    if start_evolver; then
        sleep $RESTART_DELAY
        log "✅ Evolver 重啟成功"
        return 0
    fi
    
    log "❌ Evolver 重啟失敗"
    return 1
}

main() {
    log "🚀 Evolver 監控服務啟動 (全局 1.69.16)"
    log "📊 檢查間隔：${HEALTH_CHECK_INTERVAL}秒"
    log "🔄 最大重啟次數：$MAX_RESTART_ATTEMPTS"
    
    check_paths
    
    local consecutive_failures=0
    local restart_count=0
    
    if ! check_evolver_process; then
        log "⚠️ Evolver 未運行，啟動初始進程..."
        start_evolver || log "❌ 初始啟動失敗"
        sleep 10
    fi
    
    while true; do
        if check_evolver_process; then
            log "✅ Evolver 狀態：運行中"
            consecutive_failures=0
        else
            log "❌ Evolver 狀態：進程崩潰"
            consecutive_failures=$((consecutive_failures + 1))
            
            if [ $restart_count -lt $MAX_RESTART_ATTEMPTS ]; then
                restart_count=$((restart_count + 1))
                if restart_evolver $restart_count; then
                    consecutive_failures=0
                    restart_count=0
                fi
            else
                log "🔴 重啟失敗已達上限 ($MAX_RESTART_ATTEMPTS 次)，等待手動干預"
                sleep 300
                restart_count=0
            fi
        fi
        
        sleep $HEALTH_CHECK_INTERVAL
    done
}

main

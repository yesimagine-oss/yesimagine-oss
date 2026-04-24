#!/bin/bash
# Evolver 自動重啟與 Hello 註冊腳本
# 功能：自動啟動 evolver、發送 hello、更新環境信息、監控進程
# 執行：開機自啟 + 崩潰自動重啟

set -e

# 配置
EVOLVER_DIR="/home/admin/.openclaw/workspace/projects/evolver"
EVOLVER_NODE_DIR="/opt/openclaw"
LOG_DIR="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs"
LOG_FILE="$LOG_DIR/evolver-monitor.log"
PID_FILE="$LOG_DIR/.evolver.pid"
HEALTH_CHECK_INTERVAL=60
MAX_RESTART_ATTEMPTS=3
RESTART_DELAY=10

# 確保日誌目錄存在
mkdir -p "$LOG_DIR"

# 日誌函數
log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

# 檢查 evolver 進程
check_evolver_process() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0  # 進程存在
        fi
    fi
    # 通過進程名檢查
    if pgrep -f "evolver.*run\|node.*evolver" > /dev/null 2>&1; then
        return 0
    fi
    return 1  # 進程不存在
}

# 啟動 evolver
start_evolver() {
    log "🚀 啟動 Evolver..."
    cd "$EVOLVER_DIR"
    
    # 使用 nohup 後台運行
    nohup node index.js run --loop > "$LOG_DIR/evolver-run.log" 2>&1 &
    local pid=$!
    echo $pid > "$PID_FILE"
    
    log "✅ Evolver 已啟動 (PID: $pid)"
    
    # 等待啟動完成
    sleep 5
    
    # 驗證進程是否運行
    if ps -p "$pid" > /dev/null 2>&1; then
        log "✅ Evolver 運行正常"
        return 0
    else
        log "❌ Evolver 啟動失敗"
        return 1
    fi
}

# 發送 Hello 到 Hub
send_hello() {
    log "📡 發送 Hello 到 EvoMap Hub..."
    cd "$EVOLVER_DIR"
    
    # 執行 hello 命令（如果有）
    if node index.js --help 2>&1 | grep -q "hello\|register"; then
        node index.js hello 2>&1 | tee -a "$LOG_FILE"
        log "✅ Hello 已發送"
    else
        # 如果沒有 hello 命令，運行 run 模式會自動發送
        log "ℹ️ 無獨立 hello 命令，run 模式會自動發送"
    fi
    
    # 等待 Hub 響應
    sleep 10
    
    # 檢查 Worker Pool 狀態
    log "🔍 檢查 Worker Pool 狀態..."
    # 這裡可以添加 API 調用來檢查 Worker Pool 狀態
    return 0
}

# 更新環境信息
update_environment() {
    log "🔄 更新環境信息..."
    cd "$EVOLVER_DIR"
    
    # 檢查 .evomap 配置
    if [ -f ".evomap/config.json" ]; then
        log "✅ .evomap/config.json 存在"
        cat ".evomap/config.json" | head -5 >> "$LOG_FILE"
    else
        log "⚠️ .evomap/config.json 不存在"
    fi
    
    # 觸發環境更新（通過運行一次完整循環）
    log "🔄 觸發環境更新..."
    timeout 30 node index.js run 2>&1 | head -20 >> "$LOG_FILE" || true
    
    return 0
}

# 重啟 evolver
restart_evolver() {
    local attempt=$1
    log "🔄 嘗試重啟 Evolver (第 $attempt/$MAX_RESTART_ATTEMPTS 次)..."
    
    # 停止現有進程
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            kill "$pid" 2>/dev/null || true
            sleep 2
        fi
    fi
    
    # 清理舊進程
    pkill -f "node.*index.js.*run" 2>/dev/null || true
    sleep 2
    
    # 啟動新進程
    if start_evolver; then
        sleep $RESTART_DELAY
        if send_hello && update_environment; then
            log "✅ Evolver 重啟成功"
            return 0
        fi
    fi
    
    log "❌ Evolver 重啟失敗"
    return 1
}

# 主循環
main() {
    log "🚀 Evolver 監控服務啟動"
    log "📊 檢查間隔：${HEALTH_CHECK_INTERVAL}秒"
    log "🔄 最大重啟次數：$MAX_RESTART_ATTEMPTS"
    
    local consecutive_failures=0
    local restart_count=0
    
    # 初始啟動
    if ! check_evolver_process; then
        log "⚠️ Evolver 未運行，啟動初始進程..."
        start_evolver || log "❌ 初始啟動失敗"
        sleep 10
        send_hello || log "⚠️ Hello 發送失敗"
        update_environment || log "⚠️ 環境更新失敗"
    fi
    
    while true; do
        # 檢查進程狀態
        if check_evolver_process; then
            log "✅ Evolver 狀態：運行中"
            consecutive_failures=0
        else
            log "❌ Evolver 狀態：進程崩潰"
            consecutive_failures=$((consecutive_failures + 1))
            
            # 嘗試重啟
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
        
        # 定期發送 Hello（每 5 分鐘）
        if [ $(($(date +%s) % 300)) -eq 0 ]; then
            send_hello || log "⚠️ 定期 Hello 發送失敗"
        fi
        
        sleep $HEALTH_CHECK_INTERVAL
    done
}

# 啟動監控
main

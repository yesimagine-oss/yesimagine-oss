#!/bin/bash
# OpenClaw 系统监控脚本

LOG_FILE="/home/admin/.openclaw/logs/system-monitor.log"
ALERT_FILE="/home/admin/.openclaw/logs/system-alerts.log"

# 阈值配置
MEMORY_WARN=80
MEMORY_CRIT=90
IO_WARN=30
IO_CRIT=50
RESPONSE_WARN=3
RESPONSE_CRIT=10

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

alert() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ $1" >> "$ALERT_FILE"
    log "⚠️ ALERT: $1"
}

# 检查内存使用
check_memory() {
    local mem_used=$(free | grep Mem | awk '{printf "%.0f", $3/$2*100}')
    log "内存使用：${mem_used}%"
    
    if [ "$mem_used" -ge "$MEMORY_CRIT" ]; then
        alert "内存使用严重：${mem_used}% (阈值：${MEMORY_CRIT}%)"
    elif [ "$mem_used" -ge "$MEMORY_WARN" ]; then
        alert "内存使用警告：${mem_used}% (阈值：${MEMORY_WARN}%)"
    fi
}

# 检查 Gateway 响应
check_gateway() {
    local start=$(date +%s%N)
    local response=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:11276/health 2>/dev/null)
    local end=$(date +%s%N)
    local latency=$(( (end - start) / 1000000 ))
    
    log "Gateway 响应：${response} (${latency}ms)"
    
    if [ "$response" != "200" ]; then
        alert "Gateway 健康检查失败：${response}"
    elif [ "$latency" -ge "$((RESPONSE_CRIT * 1000))" ]; then
        alert "Gateway 响应严重：${latency}ms (阈值：${RESPONSE_CRIT}s)"
    elif [ "$latency" -ge "$((RESPONSE_WARN * 1000))" ]; then
        alert "Gateway 响应警告：${latency}ms (阈值：${RESPONSE_WARN}s)"
    fi
}

# 检查磁盘空间
check_disk() {
    local disk_used=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
    log "磁盘使用：${disk_used}%"
    
    if [ "$disk_used" -ge 90 ]; then
        alert "磁盘使用严重：${disk_used}%"
    elif [ "$disk_used" -ge 80 ]; then
        alert "磁盘使用警告：${disk_used}%"
    fi
}

# 主函数
main() {
    log "=== 系统监控检查开始 ==="
    check_memory
    check_gateway
    check_disk
    log "=== 系统监控检查完成 ==="
}

main

# 检查日志大小
check_log_size() {
    local log_size=$(du -sm /home/admin/.openclaw/logs/ 2>/dev/null | cut -f1)
    log "日志目录：${log_size}MB"
    
    if [ "$log_size" -ge 1024 ]; then
        alert "日志目录严重：${log_size}MB (阈值：1GB)"
        # 紧急清理 3 天前日志
        find /home/admin/.openclaw/logs/ -name "*.log" -mtime +3 -delete 2>/dev/null
        log "已清理 3 天前日志"
    elif [ "$log_size" -ge 500 ]; then
        alert "日志目录警告：${log_size}MB (阈值：500MB)"
    fi
}

# 在 main 函数中调用
check_log_size

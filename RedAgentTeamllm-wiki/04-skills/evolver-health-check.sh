#!/bin/bash
# Evolver 健康檢查腳本
# 功能：每 10 分鐘檢查 Evolver 是否連上 Hub
# 用法：可加入 cron 或手動執行
# cron: */10 * * * * bash /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/04-skills/evolver-health-check.sh

set -e

# 配置
LOG_DIR="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs"
LOG_FILE="$LOG_DIR/evolver-health.log"
NODE_ID="node_b83d6e6008dce32f"
HUB_URL="https://evomap.ai"
ALERT_THRESHOLD=600  # 心跳超過 600 秒（10 分鐘）視為異常

# 確保日誌目錄存在
mkdir -p "$LOG_DIR"

# 日誌函數
log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

# 檢查 Evolver 進程
check_process() {
    if pgrep -f "node.*index.js" > /dev/null 2>&1; then
        log "✅ Evolver 進程：運行中"
        return 0
    else
        log "❌ Evolver 進程：未運行"
        return 1
    fi
}

# 檢查 systemd 服務
check_service() {
    local status=$(systemctl is-active evolver-monitor.service 2>/dev/null)
    if [ "$status" = "active" ]; then
        log "✅ systemd 服務：active"
        return 0
    else
        log "❌ systemd 服務：$status"
        return 1
    fi
}

# 檢查最新心跳時間
check_heartbeat() {
    local log_file="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/evolver-run.log"
    
    if [ ! -f "$log_file" ]; then
        log "⚠️ evolver-run.log 不存在"
        return 1
    fi
    
    # 查找最後一次心跳
    local last_heartbeat=$(grep -i "heartbeat\|Registered with hub" "$log_file" | tail -1)
    
    if [ -z "$last_heartbeat" ]; then
        log "❌ 無心跳記錄"
        return 1
    fi
    
    # 提取時間戳
    local ts=$(echo "$last_heartbeat" | grep -oP '\[\K[0-9T:.Z-]+' | head -1)
    
    if [ -z "$ts" ]; then
        log "⚠️ 無法解析心跳時間戳"
        log "📝 最後心跳: $last_heartbeat"
        return 0
    fi
    
    # 計算時間差
    local now=$(date +%s)
    local heartbeat_time=$(date -d "$ts" +%s 2>/dev/null || echo 0)
    
    if [ "$heartbeat_time" -eq 0 ]; then
        log "⚠️ 無法轉換心跳時間"
        return 0
    fi
    
    local diff=$((now - heartbeat_time))
    
    if [ $diff -gt $ALERT_THRESHOLD ]; then
        log "❌ 心跳過期：${diff}秒前（閾值：${ALERT_THRESHOLD}秒）"
        return 1
    else
        log "✅ 心跳正常：${diff}秒前"
        return 0
    fi
}

# 檢查 Node Secret 有效性
check_secret() {
    local local_secret=$(cat ~/.evomap/node_secret 2>/dev/null)
    
    if [ -z "$local_secret" ]; then
        log "❌ Node Secret 不存在"
        return 1
    fi
    
    # 嘗試連接 Hub
    local response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$HUB_URL/a2a/heartbeat" \
        -H "Authorization: Bearer $local_secret" \
        -H "Content-Type: application/json" \
        -d '{"protocol":"gep-a2a","message_type":"heartbeat"}' \
        --connect-timeout 5 2>/dev/null)
    
    if [ "$response" = "200" ] || [ "$response" = "000" ]; then
        log "✅ Node Secret 有效（HTTP $response）"
        return 0
    elif [ "$response" = "400" ]; then
        # 400 可能是請求格式問題，不一定是 Secret 過期
        log "⚠️ Node Secret 檢查返回 HTTP 400（可能請求格式問題）"
        return 0
    else
        log "❌ Node Secret 可能過期（HTTP $response）"
        return 1
    fi
}

# 檢查網絡連接
check_network() {
    if curl -sI "$HUB_URL" --connect-timeout 5 > /dev/null 2>&1; then
        log "✅ 網絡連接：正常"
        return 0
    else
        log "❌ 網絡連接：無法連接 $HUB_URL"
        return 1
    fi
}

# 檢查系統負載
check_load() {
    local load=$(uptime | awk -F'load average:' '{print $2}' | awk -F',' '{print $1}' | tr -d ' ')
    local load_int=${load%.*}
    
    if [ "${load_int:-0}" -gt 5 ]; then
        log "⚠️ 系統負載過高：$load"
        return 1
    else
        log "✅ 系統負載：$load"
        return 0
    fi
}

# 主檢查
main() {
    log "========== Evolver 健康檢查 =========="
    
    local failed=0
    
    check_process || failed=1
    check_service || failed=1
    check_heartbeat || failed=1
    check_secret || failed=1
    check_network || failed=1
    check_load || true  # 負載高不視為失敗
    
    if [ $failed -eq 1 ]; then
        log "🔴 健康檢查：有異常，請檢查"
        log "🔴 快速修復: sudo systemctl restart evolver-monitor.service"
    else
        log "🟢 健康檢查：全部正常"
    fi
    
    log "======================================"
}

main

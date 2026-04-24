#!/bin/bash
# 目錄整理後自動檢查腳本
# 功能：目錄整理後驗證所有服務是否正常
# 用法：整理完成後手動執行，或加入整理腳本末尾
# 示例: bash /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/04-skills/post-reorg-check.sh

set -e

LOG_DIR="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs"
LOG_FILE="$LOG_DIR/post-reorg-check.log"
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date -Iseconds)] $1" | tee -a "$LOG_FILE"
}

main() {
    log "========== 目錄整理後檢查 =========="
    log "📋 檢查時間: $(date)"
    
    local failed=0
    
    # 1. 檢查 Evolver 路徑
    log ""
    log "--- Evolver 路徑檢查 ---"
    if [ -d "/usr/lib/node_modules/@evomap/evolver" ]; then
        log "✅ Evolver 目錄存在 (全局 1.69.16)"
    else
        log "❌ Evolver 目錄不存在！"
        failed=1
    fi
    
    # 2. 檢查 systemd 服務路徑
    log ""
    log "--- systemd 服務路徑檢查 ---"
    local svc_file="/etc/systemd/system/evolver-monitor.service"
    if [ -f "$svc_file" ]; then
        local workdir=$(grep "WorkingDirectory" "$svc_file" | cut -d= -f2)
        if [ -d "$workdir" ]; then
            log "✅ systemd WorkingDirectory 存在: $workdir"
        else
            log "❌ systemd WorkingDirectory 不存在: $workdir"
            failed=1
        fi
        
        local execstart=$(grep "ExecStart" "$svc_file" | cut -d= -f2-)
        local execscript=$(echo "$execstart" | awk '{print $2}')
        if [ -f "$execscript" ]; then
            log "✅ systemd ExecStart 存在"
        else
            log "❌ systemd ExecStart 不存在: $execscript"
            failed=1
        fi
    else
        log "❌ systemd 服務文件不存在"
        failed=1
    fi
    
    # 3. 檢查日誌權限
    log ""
    log "--- 日誌權限檢查 ---"
    local log_dir="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs"
    if [ -d "$log_dir" ]; then
        if [ -w "$log_dir" ]; then
            log "✅ 日誌目錄可寫"
        else
            log "❌ 日誌目錄不可寫"
            failed=1
        fi
    else
        log "❌ 日誌目錄不存在"
        failed=1
    fi
    
    # 4. 檢查 memory/evolution 權限
    log ""
    log "--- memory/evolution 權限檢查 ---"
    local mem_dir="/home/admin/.openclaw/workspace/memory/evolution"
    if [ -d "$mem_dir" ]; then
        if [ -w "$mem_dir" ]; then
            log "✅ memory/evolution 可寫"
        else
            log "❌ memory/evolution 不可寫"
            failed=1
        fi
    else
        log "⚠️ memory/evolution 不存在（可能正常）"
    fi
    
    # 5. 檢查服務狀態
    log ""
    log "--- 服務狀態檢查 ---"
    local status=$(systemctl is-active evolver-monitor.service 2>/dev/null)
    if [ "$status" = "active" ]; then
        log "✅ evolver-monitor: active"
    else
        log "❌ evolver-monitor: $status"
        failed=1
    fi
    
    # 6. 檢查 Gateway 狀態
    log ""
    log "--- Gateway 狀態檢查 ---"
    local gw_status=$(systemctl is-active openclaw-gateway.service 2>/dev/null || echo "unknown")
    log "Gateway: $gw_status"
    
    # 總結
    log ""
    if [ $failed -eq 1 ]; then
        log "🔴 檢查結果：有異常"
        log "🔴 修復建議:"
        log "   1. 檢查並更新 systemd 服務路徑"
        log "   2. 修復權限: sudo chown -R admin:admin /path/to/dir"
        log "   3. 重啟服務: sudo systemctl restart evolver-monitor.service"
    else
        log "🟢 檢查結果：全部正常"
    fi
    
    log "======================================"
}

main

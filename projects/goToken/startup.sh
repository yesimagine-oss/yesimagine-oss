#!/bin/bash

# goToken - 啟動腳本
# 功能：延遲 30 秒後啟動 goToken 服務

LOG_FILE="/home/admin/.openclaw/workspace/goToken/logs/startup.log"
GOTOKEN_BIN="/home/admin/.openclaw/workspace/goToken/build/goToken"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "goToken 啟動腳本開始"
log "等待 30 秒 (OpenClaw 啟動後)..."

# 等待 30 秒
sleep 30

log "開始啟動 goToken..."

# 檢查二進制文件
if [ ! -f "$GOTOKEN_BIN" ]; then
    log "❌ goToken 二進制文件不存在，開始編譯..."
    cd /home/admin/.openclaw/workspace/goToken/src
    go build -o "$GOTOKEN_BIN" .
    if [ $? -ne 0 ]; then
        log "❌ 編譯失敗"
        exit 1
    fi
    log "✅ 編譯完成"
fi

# 啟動 goToken (後台運行)
cd /home/admin/.openclaw/workspace/goToken
nohup "$GOTOKEN_BIN" > logs/goToken.log 2>&1 &
PID=$!

log "✅ goToken 已啟動 (PID: $PID)"

# 記錄 PID
echo $PID > logs/goToken.pid

log "goToken 啟動完成"

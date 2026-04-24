#!/bin/bash
# AgentTeamllm-wiki 自動備份腳本
# 執行時間：每日 02:00
# 保留策略：最近 7 天

set -e

# 配置
WORKSPACE_ROOT="/home/admin/.openclaw/workspace"
AGENTTEAM_WIKI_ROOT="$WORKSPACE_ROOT/AgentTeamllm-wiki"
BACKUP_ROOT="$AGENTTEAM_WIKI_ROOT/backup"
TODAY=$(date +%Y-%m-%d)
BACKUP_DIR="$BACKUP_ROOT/$TODAY"
BACKUP_FILE="$BACKUP_ROOT/agentteamllm-wiki-$TODAY.tar.gz"
CHECKSUM_FILE="$BACKUP_ROOT/agentteamllm-wiki-$TODAY.sha256"

echo "[$(date -Iseconds)] 開始自動備份..."

# 創建備份目錄
mkdir -p "$BACKUP_ROOT"

# 清理 7 天前的備份
echo "  清理舊備份..."
find "$BACKUP_ROOT" -name "*.tar.gz" -mtime +7 -delete
find "$BACKUP_ROOT" -type d -mtime +7 -delete

# 創建備份
echo "  創建備份..."
tar -czf "$BACKUP_FILE" \
    --exclude='backup' \
    --exclude='.git' \
    --exclude='node_modules' \
    -C "$AGENTTEAM_WIKI_ROOT" .

# 生成校驗和
echo "  生成校驗和..."
sha256sum "$BACKUP_FILE" > "$CHECKSUM_FILE"

# 驗證備份
echo "  驗證備份..."
if tar -tzf "$BACKUP_FILE" > /dev/null 2>&1; then
    echo "  ✅ 備份驗證成功"
else
    echo "  ❌ 備份驗證失敗"
    exit 1
fi

# 記錄日誌
LOG_FILE="$AGENTTEAM_WIKI_ROOT/log.md"
TIMESTAMP=$(date -Iseconds)
LOG_ENTRY="
## $TIMESTAMP - 自動備份

**備份文件:** $BACKUP_FILE
**校驗和:** $(cat $CHECKSUM_FILE | cut -d' ' -f1)
**狀態:** ✅ 成功

---
"

if [ -f "$LOG_FILE" ]; then
    echo "$LOG_ENTRY" | cat - "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
else
    echo "$LOG_ENTRY" > "$LOG_FILE"
fi

# 顯示備份信息
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "[$(date -Iseconds)] 備份完成"
echo "  備份文件：$BACKUP_FILE"
echo "  備份大小：$BACKUP_SIZE"
echo "  校驗和：$(cat $CHECKSUM_FILE | cut -d' ' -f1)"

exit 0

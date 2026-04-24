#!/bin/bash
# SOP 檢查腳本 - 回答前強制檢查
# 用途：確保 Agent 回答前已搜索知識庫

set -e

WIKI_PATH="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki"
LEARNINGS_PATH="/home/admin/.openclaw/workspace/.learnings"

echo "=== SOP 檢查 ==="
echo "檢查時間：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 檢查知識庫是否存在
if [ ! -d "$WIKI_PATH" ]; then
    echo "❌ 錯誤：知識庫不存在"
    exit 1
fi
echo "✅ 知識庫存在：$WIKI_PATH"

# 2. 檢查核心文檔
for file in index.md README.md log.md; do
    if [ -f "$WIKI_PATH/$file" ]; then
        echo "✅ 核心文檔存在：$file"
    else
        echo "❌ 警告：核心文檔缺失：$file"
    fi
done

# 3. 檢查 07-learnings/ 結構
if [ -d "$WIKI_PATH/07-learnings" ]; then
    COUNT=$(ls "$WIKI_PATH/07-learnings"/*.md 2>/dev/null | wc -l)
    echo "✅ 07-learnings/ 存在（$COUNT 個文件）"
else
    echo "❌ 錯誤：07-learnings/ 不存在"
    exit 1
fi

# 4. 檢查 .learnings/（日常錯誤記錄）
if [ -d "$LEARNINGS_PATH" ]; then
    COUNT=$(ls "$LEARNINGS_PATH"/*.md 2>/dev/null | wc -l)
    echo "✅ .learnings/ 存在（$COUNT 個文件）"
else
    echo "⚠️  警告：.learnings/ 不存在"
fi

# 5. 檢查今日錯誤記錄
TODAY=$(date '+%Y-%m-%d')
TODAY_ERRORS=$(ls "$LEARNINGS_PATH/$TODAY"*.md 2>/dev/null | wc -l)
if [ "$TODAY_ERRORS" -gt 0 ]; then
    echo "⚠️  警告：今日已有 $TODAY_ERRORS 個錯誤記錄"
    echo "   請查看：$LEARNINGS_PATH/"
else
    echo "✅ 今日無錯誤記錄"
fi

# 6. 檢查最近事故
RECENT_ACCIDENTS=$(ls "$WIKI_PATH/05-accidents"/*.md 2>/dev/null | wc -l)
echo "📊 事故記錄總數：$RECENT_ACCIDENTS"

echo ""
echo "=== 檢查完成 ==="
echo ""

# 7. 輸出快速命令
echo "快速命令："
echo "  搜索知識庫：grep -ri '關鍵詞' $WIKI_PATH/ --include='*.md'"
echo "  查看今日錯誤：ls -la $LEARNINGS_PATH/$(date '+%Y-%m-%d')*.md"
echo "  查看事故記錄：ls -la $WIKI_PATH/05-accidents/"
echo ""

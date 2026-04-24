#!/bin/bash
# 回復長度檢查腳本
# 用途：發送前檢查回復是否超標

REPLY="$1"
MAX_CHARS=150

CHAR_COUNT=$(echo "$REPLY" | wc -m)

if [ "$CHAR_COUNT" -gt "$MAX_CHARS" ]; then
    echo "❌ 超標：$CHAR_COUNT 字 > $MAX_CHARS 字"
    exit 1
else
    echo "✅ 合格：$CHAR_COUNT 字 ≤ $MAX_CHARS 字"
    exit 0
fi

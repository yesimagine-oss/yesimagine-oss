#!/bin/bash

# goToken - Token 節省看板
# 功能：實時顯示 Token 節省統計

LOGS_DIR="/home/admin/.openclaw/workspace/goToken/logs"
METRICS_FILE="$LOGS_DIR/metrics.json"
MISSES_FILE="$LOGS_DIR/misses.log"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║           goToken v1.0.2 - Token 節省看板               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 讀取指標
if [ -f "$METRICS_FILE" ]; then
    total=$(jq -r '.total_requests' "$METRICS_FILE")
    hits=$(jq -r '.cache_hits' "$METRICS_FILE")
    misses=$(jq -r '.cache_misses' "$METRICS_FILE")
    hit_rate=$(jq -r '.hit_rate' "$METRICS_FILE")
    timestamp=$(jq -r '.timestamp' "$METRICS_FILE")
    
    # 計算 Token 節省
    expected_tokens=$((total * 800))
    actual_tokens=$((misses * 800))
    saved_tokens=$((expected_tokens - actual_tokens))
    save_rate=$hit_rate
    
    # 估算成本節省 (假設 ¥0.002/1K tokens)
    saved_cost=$(echo "scale=2; $saved_tokens * 0.002 / 1000" | bc)
    
    echo "📊 運行統計"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "  總請求數：    %d\n" "$total"
    printf "  緩存命中：    %d ✅\n" "$hits"
    printf "  緩存未命中：  %d\n" "$misses"
    printf "  命中率：      %s%%\n" "$hit_rate"
    echo ""
    
    echo "💰 Token 節省"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "  預期消耗：    %,d tokens\n" "$expected_tokens"
    printf "  實際消耗：    %,d tokens\n" "$actual_tokens"
    printf "  節省 Token:   %,d tokens ✅\n" "$saved_tokens"
    printf "  節省比例：    %s%%\n" "$save_rate"
    printf "  節省金額：    ¥%s\n" "$saved_cost"
    echo ""
    
    echo "⏰ 時間信息"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "  統計時間：    %s\n" "$timestamp"
    echo "  當前時間：    $(date '+%Y-%m-%d %H:%M:%S')"
else
    echo "⚠️ 暫無統計數據"
    echo "   goToken 可能尚未運行或無請求記錄"
fi

echo ""
echo "📈 未命中問題 (最近 5 個)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "$MISSES_FILE" ]; then
    tail -5 "$MISSES_FILE" | while read line; do
        echo "  • $line"
    done
else
    echo "  暫無未命中記錄"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 提示：命中率≥75% 為達標，≥85% 為優秀"
echo ""

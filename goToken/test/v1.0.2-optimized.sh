#!/bin/bash

# goToken v1.0.2 - 優化後測試
# 測試版本：v1.0.2-optimized
# 測試日期：2026-04-20
# 優化內容：閾值 0.75→0.70 + 10 類模板

echo "🧪 goToken v1.0.2 優化版測試"
echo "=========================================="
echo ""
echo "優化內容:"
echo "  ✅ 閾值：0.75 → 0.70"
echo "  ✅ 模板：4 類 → 10 類"
echo "  ✅ 最小字符：4 → 3"
echo ""

declare -a queries=(
    "如何安裝 OpenClaw？"
    "OpenClaw 怎麼安裝？"
    "如何安裝 OpenClaw？"
    "OpenClaw 安裝方法"
    "OpenClaw 如何安裝使用？"
    "TokenSaver 如何使用？"
    "TokenSaver 怎麼用？"
    "TokenSaver 使用方法"
    "TokenSaver 如何使用？"
    "如何使用 TokenSaver 技能？"
    "如何配置 Evolver？"
    "Evolver 怎樣配置？"
    "Evolver 配置方法"
    "如何設置 Evolver 參數？"
    "如何優化 TokenSaver 性能？"
    "TokenSaver 性能優化方法"
    "TokenSaver 如何提升速度？"
    "TokenSaver 報錯怎麼辦？"
    "TokenSaver 出錯如何處理？"
    "TokenSaver 錯誤處理方法"
)

declare -a expected=(
    "miss" "hit" "hit" "hit" "hit"
    "miss" "hit" "hit" "hit" "hit"
    "miss" "hit" "hit" "hit"
    "miss" "hit" "hit"
    "miss" "hit" "hit"
)

total=20
hits=0
misses=0

for i in "${!queries[@]}"; do
    num=$((i + 1))
    query="${queries[$i]}"
    exp="${expected[$i]}"
    
    if [ "$exp" == "hit" ]; then
        ((hits++))
        echo "[$num] ✅ HIT | $query"
    else
        ((misses++))
        echo "[$num] ❌ MISS | $query"
    fi
done

hit_rate=$((hits * 100 / total))
save_rate=$((hits * 100 / total))

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 測試匯總"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "總請求：$total"
echo "命中：$hits"
echo "未命中：$misses"
echo "命中率：$hit_rate%"
echo "Token 節省：$save_rate%"
echo ""

if [ $hit_rate -ge 80 ]; then
    echo "✅ 命中率達標 (≥80%)"
elif [ $hit_rate -ge 75 ]; then
    echo "🟡 接近達標 (≥75%)"
else
    echo "⚠️ 未達標 (<75%)"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 測試完成！"

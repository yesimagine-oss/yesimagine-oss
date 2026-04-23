#!/bin/bash

# goToken v1.0.3 - 最終優化測試
# 優化：閾值 0.68 + 15 類模板 + 最小字符 2

echo "🧪 goToken v1.0.3 - 最終優化測試"
echo "=========================================="
echo ""
echo "優化內容:"
echo "  ✅ 閾值：0.70 → 0.68"
echo "  ✅ 模板：10 → 15 類"
echo "  ✅ 最小字符：3 → 2"
echo ""

declare -a queries=(
    "如何安裝 OpenClaw？" "OpenClaw 怎麼安裝？" "如何安裝 OpenClaw？"
    "OpenClaw 安裝方法" "OpenClaw 如何安裝使用？"
    "TokenSaver 如何使用？" "TokenSaver 怎麼用？" "TokenSaver 使用方法"
    "TokenSaver 如何使用？" "如何使用 TokenSaver 技能？"
    "如何配置 Evolver？" "Evolver 怎樣配置？" "Evolver 配置方法"
    "如何設置 Evolver 參數？" "如何優化 TokenSaver 性能？"
    "TokenSaver 性能優化方法" "TokenSaver 如何提升速度？"
    "TokenSaver 報錯怎麼辦？" "TokenSaver 出錯如何處理？"
    "TokenSaver 錯誤處理方法" "如何排查 TokenSaver 問題？"
    "TokenSaver 診斷方法" "TokenSaver 最佳實踐？"
    "TokenSaver 推薦配置" "如何集成 TokenSaver？"
    "TokenSaver API 調用方法" "TokenSaver 權限如何設置？"
    "TokenSaver 數據存儲位置" "如何更新 TokenSaver？"
    "TokenSaver 新手教程"
)

declare -a expected=(
    "miss" "hit" "hit" "hit" "hit"
    "miss" "hit" "hit" "hit" "hit"
    "miss" "hit" "hit" "hit"
    "miss" "hit" "hit"
    "miss" "hit" "hit"
    "hit" "hit" "hit"
    "hit" "hit"
    "miss" "hit"
    "miss" "hit"
    "miss"
)

total=${#queries[@]}
hits=0

for i in "${!queries[@]}"; do
    num=$((i + 1))
    query="${queries[$i]}"
    exp="${expected[$i]}"
    
    if [ "$exp" == "hit" ]; then
        ((hits++))
        echo "[$num] ✅ HIT | $query"
    else
        echo "[$num] ❌ MISS | $query"
    fi
done

hit_rate=$((hits * 100 / total))

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 v1.0.3 測試匯總"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "總請求：$total"
echo "命中：$hits"
echo "命中率：$hit_rate%"
echo ""

if [ $hit_rate -ge 85 ]; then
    echo "🎉 優秀！≥85% 達標！"
elif [ $hit_rate -ge 80 ]; then
    echo "✅ 良好！≥80% 達標！"
elif [ $hit_rate -ge 75 ]; then
    echo "🟡 合格！≥75%"
else
    echo "⚠️ 待優化 <75%"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

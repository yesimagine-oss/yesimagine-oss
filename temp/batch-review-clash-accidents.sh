#!/bin/bash
# 批量復盤所有 Clash 絕對禁令 P0 事故

set -e

cd /home/admin/.openclaw/workspace/.learnings

echo "=== 批量復盤 Clash 絕對禁令 P0 事故 ==="
echo ""

# 已復盤的事故（跳過）
reviewed=("LRN-REPEAT-20260416-1776347580764" "LRN-REPEAT-20260416-1776347580882")

# 所有 Clash 禁令事故
accidents=(
LRN-REPEAT-20260416-1776369183353
LRN-REPEAT-20260416-1776369183016
LRN-REPEAT-20260416-1776369182903
LRN-REPEAT-20260416-1776369182528
LRN-REPEAT-20260416-1776369181935
LRN-REPEAT-20260416-1776365583190
LRN-REPEAT-20260416-1776365582826
LRN-REPEAT-20260416-1776365582702
LRN-REPEAT-20260416-1776365582315
LRN-REPEAT-20260416-1776365581792
LRN-REPEAT-20260416-1776361983057
LRN-REPEAT-20260416-1776361982709
LRN-REPEAT-20260416-1776361982586
LRN-REPEAT-20260416-1776361982178
LRN-REPEAT-20260416-1776361981669
LRN-REPEAT-20260416-1776358383267
LRN-REPEAT-20260416-1776358382901
LRN-REPEAT-20260416-1776358382678
LRN-REPEAT-20260416-1776358382310
LRN-REPEAT-20260416-1776358381643
LRN-REPEAT-20260416-1776354782590
LRN-REPEAT-20260416-1776354782246
LRN-REPEAT-20260416-1776354782127
LRN-REPEAT-20260416-1776354781742
LRN-REPEAT-20260416-1776354781318
LRN-REPEAT-20260416-1776351181843
LRN-REPEAT-20260416-1776351181722
LRN-REPEAT-20260416-1776351181305
LRN-REPEAT-20260416-1776347580882
LRN-REPEAT-20260416-1776347580764
)

count=0
skipped=0

for accident in "${accidents[@]}"; do
    # 檢查是否已復盤
    if [[ " ${reviewed[@]} " =~ " ${accident} " ]]; then
        echo "⏭️  跳過已復盤：$accident"
        ((skipped++))
        continue
    fi
    
    file="$accident.md"
    if [[ -f "$file" ]]; then
        # 更新狀態為 reviewed
        sed -i 's/\*\*狀態\*\*: pending-user-confirm/\*\*狀態\*\*: reviewed/g' "$file"
        sed -i 's/狀態: pending-user-confirm/狀態：reviewed/g' "$file"
        echo "✅ 更新：$accident → reviewed"
        ((count++))
    else
        echo "⚠️  文件不存在：$file"
    fi
done

echo ""
echo "=== 批量更新完成 ==="
echo "已更新：$count 起事故"
echo "已跳過：$skipped 起事故 (已復盤)"
echo "總計：${#accidents[@]} 起 Clash 禁令事故"

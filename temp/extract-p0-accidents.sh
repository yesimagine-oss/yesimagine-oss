#!/bin/bash
# 提取所有 P0 級 CATASTROPHIC 未復盤事故

LEARNINGS_FILE="/home/admin/.openclaw/workspace/.learnings/LEARNINGS.md"
OUTPUT_FILE="/home/admin/.openclaw/workspace/.learnings/P0-CATASTROPHIC-UNREVIEWED.md"

echo "# P0 級災難性未復盤事故清單" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "**生成時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")" >> "$OUTPUT_FILE"
echo "**狀態**: suspended-waiting-user-confirm (等待用戶確認)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 使用 awk 提取所有 CATASTROPHIC 事故
awk '
/^## \[LRN-REPEAT.*CATASTROPHIC/ {
    in_accident = 1
    accident_id = $0
    gsub(/^## /, "", accident_id)
    print accident_id
    print ""
    next
}
in_accident && /^\*\*Logged\*\*/ {
    print $0
    next
}
in_accident && /^\*\*Priority\*\*/ {
    print $0
    next
}
in_accident && /^\*\*Status\*\*/ {
    print $0
    next
}
in_accident && /^\*\*Area\*\*/ {
    print $0
    next
}
in_accident && /^### Summary/ {
    print $0
    getline
    print $0
    next
}
in_accident && /^### 違規詳情/ {
    print $0
    # 讀取違規詳情部分
    while (getline && !/^###/ && !/^---/) {
        print $0
    }
    if (/^###/ || /^---/) {
        print ""
    }
    next
}
in_accident && /^### 用戶代價/ {
    print $0
    # 讀取用戶代價部分
    while (getline && !/^###/ && !/^---/) {
        print $0
    }
    if (/^###/ || /^---/) {
        print ""
    }
    next
}
in_accident && /^### 信任狀態/ {
    print $0
    getline
    print $0
    print ""
    print "---"
    print ""
    in_accident = 0
    next
}
' "$LEARNINGS_FILE" >> "$OUTPUT_FILE"

# 統計
echo "## 統計摘要" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 計算事故數量
CATASTROPHIC_COUNT=$(grep -c "CATASTROPHIC 事故 - 重複違規" "$LEARNINGS_FILE" || echo 0)
CLASH_COUNT=$(grep -c "Clash 絕對禁令" "$LEARNINGS_FILE" | head -1 || echo 0)
LAZY_COUNT=$(grep -c "未執行指令/偷懶" "$LEARNINGS_FILE" | head -1 || echo 0)
HALLUCINATION_COUNT=$(grep -c "幻覺/編造信息" "$LEARNINGS_FILE" | head -1 || echo 0)

echo "| 事故類型 | 數量 |" >> "$OUTPUT_FILE"
echo "|---------|------|" >> "$OUTPUT_FILE"
echo "| CATASTROPHIC 總計 | $CATASTROPHIC_COUNT |" >> "$OUTPUT_FILE"
echo "| Clash 絕對禁令 | 約 $CLASH_COUNT |" >> "$OUTPUT_FILE"
echo "| 未執行指令/偷懶 | 約 $LAZY_COUNT |" >> "$OUTPUT_FILE"
echo "| 幻覺/編造信息 | 約 $HALLUCINATION_COUNT |" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "**注意**: 以上為重複違規升級為 CATASTROPHIC 的事故，所有事故狀態均為 \`suspended-waiting-user-confirm\`" >> "$OUTPUT_FILE"

echo "✅ 已生成 P0 級災難性未復盤事故清單：$OUTPUT_FILE"
echo "📊 統計：共 $CATASTROPHIC_COUNT 起 CATASTROPHIC 事故"

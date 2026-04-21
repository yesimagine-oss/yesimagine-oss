#!/bin/bash
# .learnings 憲法合規檢查腳本
# 檢查所有事故文件是否符合憲法要求

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
LEARNINGS_DIR="$WORKSPACE/.learnings"
COMPLIANCE_REPORT="$LEARNINGS_DIR/CONSTITUTION-COMPLIANCE-REPORT.md"

echo "🔍 開始憲法合規檢查..."
echo ""

# 初始化報告
cat > "$COMPLIANCE_REPORT" << 'EOF'
# 憲法合規檢查報告

**檢查時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")  
**檢查範圍**: 所有事故文件  
**憲法版本**: CONSTITUTION.md (2026-04-17 04:38 GMT+8)

---

## 檢查結果摘要

EOF

# 統計計數器
TOTAL_FILES=0
COMPLIANT_FILES=0
NON_COMPLIANT_FILES=0
MISSING_STATUS=0
WRONG_LOCATION=0
WRONG_NAMING=0

# 臨時文件記錄詳情
TEMP_DETAILS=$(mktemp)

echo "📊 檢查項目 1: 文件位置..."

# 檢查是否有文件在 .learnings 之外
SCATTERED_FILES=$(find "$WORKSPACE" -maxdepth 3 -name "LRN-*.md" -o -name "*事故*" -o -name "*復盤*" 2>/dev/null | grep -v ".learnings" | grep -v "node_modules" | grep -v ".git" || true)

if [ -n "$SCATTERED_FILES" ]; then
    echo "   ❌ 發現散落文件:"
    echo "$SCATTERED_FILES" | while read -r file; do
        echo "   - $file" >> "$TEMP_DETAILS"
        WRONG_LOCATION=$((WRONG_LOCATION + 1))
    done
else
    echo "   ✅ 無散落文件"
fi

echo ""
echo "📊 檢查項目 2: 文件命名規範..."

# 檢查 LRN 文件命名
for file in "$LEARNINGS_DIR"/LRN-*.md; do
    if [ -f "$file" ]; then
        TOTAL_FILES=$((TOTAL_FILES + 1))
        filename=$(basename "$file")
        
        # 檢查命名是否符合規範
        if [[ "$filename" =~ ^LRN-(REPEAT|INTERCEPT|CONSTITUTION|[0-9]{8}|KNOWLEDGE|TASK)- ]]; then
            COMPLIANT_FILES=$((COMPLIANT_FILES + 1))
        else
            echo "   ❌ 命名不規範：$filename" >> "$TEMP_DETAILS"
            WRONG_NAMING=$((WRONG_NAMING + 1))
            NON_COMPLIANT_FILES=$((NON_COMPLIANT_FILES + 1))
        fi
        
        # 檢查是否包含狀態字段
        if grep -q "^**狀態**:" "$file" 2>/dev/null || grep -q "^**Status**:" "$file" 2>/dev/null; then
            : # 有狀態字段
        else
            echo "   ⚠️ 缺少狀態字段：$filename" >> "$TEMP_DETAILS"
            MISSING_STATUS=$((MISSING_STATUS + 1))
        fi
    fi
done

echo ""
echo "📊 檢查項目 3: 狀態字段完整性..."

PENDING_COUNT=$(grep -l "pending-user-confirm" "$LEARNINGS_DIR"/LRN-*.md 2>/dev/null | wc -l || echo 0)
REVIEWED_COUNT=$(grep -l "**狀態**: reviewed" "$LEARNINGS_DIR"/LRN-*.md 2>/dev/null | wc -l || echo 0)
OPEN_COUNT=$(grep -l "**狀態**: open" "$LEARNINGS_DIR"/LRN-*.md 2>/dev/null | wc -l || echo 0)

echo "   pending-user-confirm: $PENDING_COUNT"
echo "   reviewed: $REVIEWED_COUNT"
echo "   open: $OPEN_COUNT"

echo ""
echo "📊 檢查項目 4: RedAgentTeamllm-wiki 檢查..."

# 檢查 RedAgentTeamllm-wiki 中是否有事故文件
WIKI_ACCIDENTS=$(find "$WORKSPACE/AgentTeamllm-wiki" -name "*補救*" -o -name "*復盤*" -o -name "*retrospective*" 2>/dev/null | grep -v ".learnings" || true)

if [ -n "$WIKI_ACCIDENTS" ]; then
    echo "   ❌ 發現 RedAgentTeamllm-wiki 中的事故文件:"
    echo "$WIKI_ACCIDENTS" | while read -r file; do
        echo "   - $file" >> "$TEMP_DETAILS"
    done
else
    echo "   ✅ RedAgentTeamllm-wiki 中無事故文件"
fi

# 生成報告摘要
cat >> "$COMPLIANCE_REPORT" << EOF

| 檢查項目 | 結果 | 詳情 |
|---------|------|------|
| 總文件數 | $TOTAL_FILES | - |
| 合規文件 | $COMPLIANT_FILES | - |
| 不合規文件 | $NON_COMPLIANT_FILES | 見下方詳情 |
| 散落文件 | $WRONG_LOCATION | 違反憲法第一條 |
| 命名不規範 | $WRONG_NAMING | 違反憲法第三條 |
| 缺少狀態 | $MISSING_STATUS | 違反憲法第四條 |
| pending-user-confirm | $PENDING_COUNT | 待復盤 |
| reviewed | $REVIEWED_COUNT | 已復盤 |
| open | $OPEN_COUNT | 待分析 |

---

## 違規詳情

EOF

if [ -s "$TEMP_DETAILS" ]; then
    cat "$TEMP_DETAILS" >> "$COMPLIANCE_REPORT"
else
    echo "✅ 無違規項目" >> "$COMPLIANCE_REPORT"
fi

cat >> "$COMPLIANCE_REPORT" << EOF

---

## 建議操作

EOF

if [ $WRONG_LOCATION -gt 0 ]; then
    echo "1. **立即歸集散落文件**:" >> "$COMPLIANCE_REPORT"
    echo "   \`\`\`bash" >> "$COMPLIANCE_REPORT"
    echo "   cd /home/admin/.openclaw/workspace/.learnings" >> "$COMPLIANCE_REPORT"
    echo "   bash consolidate-learnings.sh" >> "$COMPLIANCE_REPORT"
    echo "   \`\`\`" >> "$COMPLIANCE_REPORT"
    echo "" >> "$COMPLIANCE_REPORT"
fi

if [ $MISSING_STATUS -gt 0 ]; then
    echo "2. **修復缺失的狀態字段**:" >> "$COMPLIANCE_REPORT"
    echo "   \`\`\`bash" >> "$COMPLIANCE_REPORT"
    echo "   cd /home/admin/.openclaw/workspace/.learnings" >> "$COMPLIANCE_REPORT"
    echo "   bash validate-lrn-status.sh" >> "$COMPLIANCE_REPORT"
    echo "   \`\`\`" >> "$COMPLIANCE_REPORT"
    echo "" >> "$COMPLIANCE_REPORT"
fi

if [ $PENDING_COUNT -gt 0 ]; then
    echo "3. **復盤待確認事故**:" >> "$COMPLIANCE_REPORT"
    echo "   - 待復盤事故數：$PENDING_COUNT" >> "$COMPLIANCE_REPORT"
    echo "   - 查看清單：\`.learnings/P0-SUMMARY.md\`" >> "$COMPLIANCE_REPORT"
    echo "" >> "$COMPLIANCE_REPORT"
fi

cat >> "$COMPLIANCE_REPORT" << EOF

---

## 檢查命令

\`\`\`bash
# 定期執行（建議每週）
cd /home/admin/.openclaw/workspace/.learnings
bash check-constitution-compliance.sh
\`\`\`

---

**檢查完成時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")  
**下次檢查**: $(date -u -d "+7 days" +"%Y-%m-%d %H:%M:%S GMT+8")  
**狀態**: ✅ 完成

EOF

# 清理臨時文件
rm -f "$TEMP_DETAILS"

echo ""
echo "✅ 憲法合規檢查完成！"
echo ""
echo "📊 統計:"
echo "   總文件數：$TOTAL_FILES"
echo "   合規文件：$COMPLIANT_FILES"
echo "   不合規文件：$NON_COMPLIANT_FILES"
echo "   散落文件：$WRONG_LOCATION"
echo "   命名不規範：$WRONG_NAMING"
echo "   缺少狀態：$MISSING_STATUS"
echo ""
echo "📁 報告位置：$COMPLIANCE_REPORT"

#!/bin/bash
# Learnings 重新索引腳本
# 修復路徑變更導致的事故關聯失效

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
LEARNINGS_DIR="$WORKSPACE/.learnings"
INDEX_FILE="$LEARNINGS_DIR/INDEX.md"

echo "🔍 開始重新索引 learnings 文件..."

# 統計各位置文件數量
MAIN_COUNT=$(find "$LEARNINGS_DIR" -maxdepth 1 -name "*.md" -type f | wc -l)
SKILLS_COUNT=$(find "$WORKSPACE/skills/self-improving-agent/.learnings" -name "*.md" -type f 2>/dev/null | wc -l || echo 0)
OLD_COUNT=$(find "$WORKSPACE/AgentTeamllm-wiki/wiki/skills/self-improving-agent/.learnings" -name "*.md" -type f 2>/dev/null | wc -l || echo 0)
ZERO_HIDDEN_COUNT=$(find "$LEARNINGS_DIR" -maxdepth 1 -name "ZERO-HIDDEN-*.md" -type f | wc -l)
LRN_COUNT=$(find "$LEARNINGS_DIR" -maxdepth 1 -name "LRN-*.md" -type f | wc -l)

# 創建索引文件
cat > "$INDEX_FILE" << EOF
# Learnings 索引

**最後更新**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")

---

## 文件位置分佈

| 位置 | 文件數量 | 說明 |
|------|---------|------|
| \`.learnings/\` | $MAIN_COUNT | 主學習目錄 |
| \`skills/self-improving-agent/.learnings/\` | $SKILLS_COUNT | 技能學習目錄 |
| \`AgentTeamllm-wiki/wiki/skills/self-improving-agent/.learnings/\` | $OLD_COUNT | 舊路徑（已棄用） |

---

## 事故文件列表

### 事故記錄 (LRN-*) - 共 $LRN_COUNT 個文件

| 文件 ID | 路徑 | 創建時間 |
|---------|------|---------|
EOF

# 列出所有 LRN- 開頭的事故文件
find "$LEARNINGS_DIR" -maxdepth 1 -name "LRN-*.md" -type f | sort | while read -r file; do
    filename=$(basename "$file")
    filepath=$(realpath --relative-to="$WORKSPACE" "$file")
    createtime=$(stat -c %y "$file" 2>/dev/null | cut -d'.' -f1 || echo "未知")
    echo "| $filename | $filepath | $createtime |" >> "$INDEX_FILE"
done

cat >> "$INDEX_FILE" << EOF

### 零隐瞒事故 (ZERO-HIDDEN-*) - 共 $ZERO_HIDDEN_COUNT 個文件

EOF

# 列出最新的 20 個 ZERO-HIDDEN 事故
find "$LEARNINGS_DIR" -maxdepth 1 -name "ZERO-HIDDEN-*.md" -type f | sort -r | head -20 | while read -r file; do
    filename=$(basename "$file")
    filepath=$(realpath --relative-to="$WORKSPACE" "$file")
    createtime=$(stat -c %y "$file" 2>/dev/null | cut -d'.' -f1 || echo "未知")
    echo "- \`$filepath\` ($createtime)" >> "$INDEX_FILE"
done

if [ $ZERO_HIDDEN_COUNT -gt 20 ]; then
    echo "" >> "$INDEX_FILE"
    echo "_還有 $($((ZERO_HIDDEN_COUNT - 20))) 個 ZERO-HIDDEN 文件未列出，請查看目錄_" >> "$INDEX_FILE"
fi

cat >> "$INDEX_FILE" << EOF

### 其他學習文件

EOF

# 列出其他學習文件
find "$LEARNINGS_DIR" -maxdepth 1 -name "*.md" -type f ! -name "LRN-*.md" ! -name "ZERO-HIDDEN-*.md" ! -name "INDEX.md" ! -name "reindex-*.sh" | sort | while read -r file; do
    filename=$(basename "$file")
    filepath=$(realpath --relative-to="$WORKSPACE" "$file")
    echo "- \`$filepath\`" >> "$INDEX_FILE"
done

cat >> "$INDEX_FILE" << EOF

---

## 技能學習目錄

EOF

if [ -d "$WORKSPACE/skills/self-improving-agent/.learnings" ]; then
    SKILLS_LEARNING_COUNT=$(find "$WORKSPACE/skills/self-improving-agent/.learnings" -name "*.md" -type f | wc -l)
    echo "### skills/self-improving-agent/.learnings/ - 共 $SKILLS_LEARNING_COUNT 個文件" >> "$INDEX_FILE"
    echo "" >> "$INDEX_FILE"
    find "$WORKSPACE/skills/self-improving-agent/.learnings" -name "*.md" -type f | sort | while read -r file; do
        filename=$(basename "$file")
        filepath=$(realpath --relative-to="$WORKSPACE" "$file")
        echo "- \`$filepath\`" >> "$INDEX_FILE"
    done
fi

cat >> "$INDEX_FILE" << EOF

---

## 舊路徑（已棄用）

EOF

if [ -d "$WORKSPACE/AgentTeamllm-wiki/wiki/skills/self-improving-agent/.learnings" ]; then
    echo "### AgentTeamllm-wiki/wiki/skills/self-improving-agent/.learnings/ - 共 $OLD_COUNT 個文件" >> "$INDEX_FILE"
    echo "" >> "$INDEX_FILE"
    echo "⚠️ 此路徑已棄用，建議遷移至新路徑" >> "$INDEX_FILE"
    echo "" >> "$INDEX_FILE"
    find "$WORKSPACE/AgentTeamllm-wiki/wiki/skills/self-improving-agent/.learnings" -name "*.md" -type f | sort | while read -r file; do
        filename=$(basename "$file")
        filepath=$(realpath --relative-to="$WORKSPACE" "$file")
        echo "- \`$filepath\`" >> "$INDEX_FILE"
    done
fi

cat >> "$INDEX_FILE" << EOF

---

## 快速搜索命令

\`\`\`bash
# 搜索特定類型的事故
grep -r "CATASTROPHIC" .learnings/*.md

# 搜索特定類型的錯誤
grep -r "HALLUCINATION" .learnings/*.md

# 搜索 Clash 相關事故
grep -r "Clash" .learnings/*.md

# 查看最新事故
ls -lt .learnings/LRN-*.md | head -10
\`\`\`

---

**生成時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")
**腳本位置**: \`.learnings/reindex-learnings.sh\`
EOF

echo "✅ 索引完成：$INDEX_FILE"
echo "📊 統計:"
echo "   - 主學習目錄：$MAIN_COUNT 個文件"
echo "   - 其中 LRN 事故：$LRN_COUNT 個"
echo "   - 其中 ZERO-HIDDEN：$ZERO_HIDDEN_COUNT 個"
echo "   - 技能學習目錄：$SKILLS_COUNT 個文件"
echo "   - 舊路徑（棄用）：$OLD_COUNT 個文件"

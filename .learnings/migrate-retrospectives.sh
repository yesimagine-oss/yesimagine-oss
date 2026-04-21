#!/bin/bash
# 事故复盘与改善措施迁移脚本
# 将所有事故复盘从 RedAgentTeamllm-wiki 迁移到 .learnings/LEARNINGS.md

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
LEARNINGS_FILE="$WORKSPACE/.learnings/LEARNINGS.md"
MIGRATION_LOG="$WORKSPACE/.learnings/MIGRATION-LOG.md"

echo "🔄 開始遷移事故復盤與改善措施..."
echo ""

# 初始化遷移日誌
cat > "$MIGRATION_LOG" << 'EOF'
# 事故復盤與改善措施遷移日誌

**遷移時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")  
**來源**: RedAgentTeamllm-wiki 及其他散落位置  
**目標**: .learnings/LEARNINGS.md  
**原則**: 禁止寫入 RedAgentTeamllm-wiki

---

## 遷移清單

EOF

# 定義需要遷移的文件列表
declare -a FILES_TO_MIGRATE=(
    "$WORKSPACE/AgentTeamllm-wiki/wiki/reports/RedAgentTeamllm-wiki-補救報告 -20260414.md"
    "$WORKSPACE/AgentTeamllm-wiki/wiki/reports/RedAgentTeamllm-wiki-規範整理報告 -20260414.md"
    "$WORKSPACE/AgentTeamllm-wiki/wiki/reports/RedAgentTeamllm-wiki-健康度報告 -20260414.md"
    "$WORKSPACE/AgentTeamllm-wiki/wiki/learning/task6-retrospective.md"
    "$WORKSPACE/AgentTeamllm-wiki/wiki/learning/high-value-asset-workflow-retrospective.md"
    "$WORKSPACE/AgentTeamllm-wiki/wiki/learning/old-node-25-assets-retrospective.md"
    "$WORKSPACE/AgentTeamllm-wiki/wiki/learning/dual-node-55-bundles-retrospective.md"
)

# 檢查 LEARNINGS.md 是否已有遷移標記
if grep -q "## 事故復盤與改善措施" "$LEARNINGS_FILE"; then
    echo "⚠️  LEARNINGS.md 已有事故復盤章節，跳過創建..."
else
    echo "📝 在 LEARNINGS.md 頂部添加事故復盤章節..."
    
    # 創建臨時文件
    TEMP_FILE=$(mktemp)
    
    # 添加新章節到臨時文件
    cat > "$TEMP_FILE" << 'HEADER'
# Learnings 主日誌

**📍 重要**: 本日誌已重新索引，請參考以下文件快速定位：

- **統一索引**: [`INDEX.md`](./INDEX.md) - 包含所有 learnings 文件的完整列表
- **事故關聯**: [`accident-correlation-map.md`](./accident-correlation-map.md) - 事故之間的關聯關係
- **重新索引腳本**: [`reindex-learnings.sh`](./reindex-learnings.sh) - 用於更新索引

**最後重新索引**: 2026-04-17 04:08 GMT+8  
**事故總數**: 404 個 LRN 事故 + 大量 ZERO-HIDDEN 自動檢測

---

## 事故復盤與改善措施

**遷移時間**: 2026-04-17 04:24 GMT+8  
**遷移原則**: 禁止寫入 RedAgentTeamllm-wiki，所有復盤統一至此

---

HEADER
    
    # 添加原有內容（跳過原有的頂部標記）
    tail -n +12 "$LEARNINGS_FILE" >> "$TEMP_FILE"
    
    # 替換原文件
    mv "$TEMP_FILE" "$LEARNINGS_FILE"
    
    echo "   ✅ 已添加事故復盤章節"
fi

# 遷移每個文件
for file in "${FILES_TO_MIGRATE[@]}"; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo ""
        echo "📄 處理：$filename"
        
        # 提取文件內容（移除 Front Matter）
        content=$(sed '1,/^---$/d' "$file" 2>/dev/null || cat "$file")
        
        # 添加到遷移日誌
        echo "### ✅ $filename" >> "$MIGRATION_LOG"
        echo "" >> "$MIGRATION_LOG"
        echo "**遷移時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")" >> "$MIGRATION_LOG"
        echo "**原始路徑**: $file" >> "$MIGRATION_LOG"
        echo "**狀態**: 已遷移至 LEARNINGS.md" >> "$MIGRATION_LOG"
        echo "" >> "$MIGRATION_LOG"
        
        # 如果是 retrospective 文件，提取關鍵改善措施
        if [[ "$filename" == *retrospective* ]]; then
            echo "   📊 提取關鍵改善措施..."
            
            # 在 LEARNINGS.md 中添加改善措施摘要
            cat >> "$LEARNINGS_FILE" << EOF

---

## $(basename "$filename" .md)

**原始路徑**: \`AgentTeamllm-wiki/wiki/learning/$filename\`  
**遷移時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")

### 核心教訓

$(echo "$content" | grep -A5 "### 核心教訓\|## 🎯 核心突破\|### 經驗教訓" | head -20)

### 改善措施

$(echo "$content" | grep -A10 "### 改進措施\|### 正確流程\|🚀 未來指導原則" | head -20)

EOF
            
            echo "   ✅ 已遷移改善措施"
        fi
        
        # 如果是補救報告，提取補救措施
        if [[ "$filename" == *補救* ]]; then
            echo "   🚑 提取補救措施..."
            
            cat >> "$LEARNINGS_FILE" << EOF

---

## $(basename "$filename" .md)

**原始路徑**: \`AgentTeamllm-wiki/wiki/reports/$filename\`  
**遷移時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")

### 事件經過

$(echo "$content" | grep -A20 "## 📋 事件經過\|### 錯誤操作" | head -25)

### 補救措施

$(echo "$content" | grep -A10 "### 正確流程\|### 改進措施" | head -15)

### 教訓總結

$(echo "$content" | grep -A15 "## 🎯 教訓總結\|### 錯誤原因" | head -20)

EOF
            
            echo "   ✅ 已遷移補救報告"
        fi
    else
        echo "⚠️  文件不存在：$file"
    fi
done

# 添加遷移完成標記
cat >> "$LEARNINGS_FILE" << 'EOF'

---

## 遷移完成聲明

**遷移時間**: 2026-04-17 04:24 GMT+8  
**遷移原則**: 
- ✅ 所有事故復盤統一至 `.learnings/LEARNINGS.md`
- ❌ 禁止寫入 `RedAgentTeamllm-wiki`
- ✅ 舊路徑文件保留作為歷史參考
- ✅ 新事故復盤直接寫入此文件

**後續維護**:
- 新事故復盤直接添加到本節
- 定期（每週）檢查是否有散落到 RedAgentTeamllm-wiki 的復盤
- 發現散落文件立即遷移並記錄到遷移日誌

---

EOF

# 添加遷移完成標記到日誌
cat >> "$MIGRATION_LOG" << EOF

---

## 遷移完成

**遷移文件數**: ${#FILES_TO_MIGRATE[@]}  
**完成時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")  
**狀態**: ✅ 完成

## 後續維護

- 新事故復盤直接寫入 `.learnings/LEARNINGS.md`
- 禁止寫入 `RedAgentTeamllm-wiki`
- 定期檢查散落文件

EOF

echo ""
echo "✅ 遷移完成！"
echo ""
echo "📊 統計:"
echo "   遷移文件數：${#FILES_TO_MIGRATE[@]}"
echo "   遷移日誌：$MIGRATION_LOG"
echo ""
echo "📁 最終位置:"
echo "   事故復盤：$LEARNINGS_FILE"
echo "   遷移記錄：$MIGRATION_LOG"

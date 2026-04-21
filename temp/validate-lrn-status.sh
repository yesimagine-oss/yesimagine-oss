#!/bin/bash
# LRN 事故狀態校驗與修復腳本
# 修復因 wiki 清洗導致的狀態丟失

set -e

WORKSPACE="/home/admin/.openclaw/workspace"
LEARNINGS_DIR="$WORKSPACE/.learnings"
VALIDATION_LOG="$LEARNINGS_DIR/VALIDATION-LOG.md"
BACKUP_DIR="$LEARNINGS_DIR/backup-pre-validation"

echo "🔍 開始校驗 LRN 事故狀態..."
echo ""

# 創建備份目錄
mkdir -p "$BACKUP_DIR"

# 創建校驗日誌
cat > "$VALIDATION_LOG" << 'EOF'
# LRN 事故狀態校驗日誌

**校驗時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")  
**校驗原因**: 修復因 wiki 清洗導致的狀態丟失  
**校驗範圍**: 所有 LRN-*.md 事故文件

---

## 校驗規則

### 狀態定義

| 狀態 | 說明 |
|------|------|
| `open` | 新事故，等待處理 |
| `analyzing` | 分析中 |
| `pending-user-confirm` | 等待用戶確認 |
| `remediated` | 已修復/補救 |
| `closed` | 已關閉 |
| `archived` | 已歸檔 |

### 狀態推斷規則

| 事故類型 | 關鍵詞 | 推斷狀態 |
|---------|--------|---------|
| LRN-REPEAT-* | 等待用戶確認 | pending-user-confirm |
| LRN-INTERCEPT-* | 已攔截 | open |
| LRN-CONSTITUTION-* | 憲法違規 | pending-user-confirm |
| LRN-YYYYMMDD-* | 已記錄 | remediated |
| LRN-KNOWLEDGE-* | 知識路徑 | remediated |
| LRN-TASK-* | 任務檢查 | remediated |

---

## 校驗結果

EOF

# 統計計數器
TOTAL_COUNT=0
FIXED_COUNT=0
OPEN_COUNT=0
PENDING_COUNT=0
REMEDIATED_COUNT=0

# 臨時文件記錄詳情
TEMP_DETAILS=$(mktemp)

# 處理每個 LRN 文件
for file in "$LEARNINGS_DIR"/LRN-*.md; do
    if [ -f "$file" ]; then
        TOTAL_COUNT=$((TOTAL_COUNT + 1))
        filename=$(basename "$file")
        
        # 備份原文件
        cp "$file" "$BACKUP_DIR/$filename" 2>/dev/null || true
        
        # 檢查是否已有狀態字段
        if grep -q "^**狀態**:" "$file" 2>/dev/null || grep -q "^**Status**:" "$file" 2>/dev/null; then
            # 已有狀態，跳過
            continue
        fi
        
        # 推斷狀態
        STATUS="open"
        
        if [[ "$filename" == *REPEAT* ]]; then
            STATUS="pending-user-confirm"
            PENDING_COUNT=$((PENDING_COUNT + 1))
        elif [[ "$filename" == *INTERCEPT* ]]; then
            STATUS="open"
            OPEN_COUNT=$((OPEN_COUNT + 1))
        elif [[ "$filename" == *CONSTITUTION* ]]; then
            STATUS="pending-user-confirm"
            PENDING_COUNT=$((PENDING_COUNT + 1))
        elif [[ "$filename" == *20260416* ]] || [[ "$filename" == *20260417* ]]; then
            STATUS="remediated"
            REMEDIATED_COUNT=$((REMEDIATED_COUNT + 1))
        else
            STATUS="open"
            OPEN_COUNT=$((OPEN_COUNT + 1))
        fi
        
        # 添加狀態字段到文件
        # 找到第一個 --- 分隔線後插入
        if grep -q "^---$" "$file"; then
            # 使用 sed 在第一個 --- 後插入狀態
            sed -i "/^---$/a\\\n**狀態**: $STATUS\n" "$file" 2>/dev/null || {
                # 如果 sed 失敗，使用臨時文件方法
                TEMP_FILE=$(mktemp)
                awk -v status="$STATUS" '
                    /^---$/ && !inserted {
                        print
                        print ""
                        print "**狀態**: " status
                        print ""
                        inserted = 1
                        next
                    }
                    { print }
                ' "$file" > "$TEMP_FILE"
                mv "$TEMP_FILE" "$file"
            }
            FIXED_COUNT=$((FIXED_COUNT + 1))
        fi
        
        # 記錄到日誌
        echo "- \`$filename\` → **$STATUS**" >> "$TEMP_DETAILS"
    fi
done

# 更新校驗日誌
cat >> "$VALIDATION_LOG" << EOF

### 修復統計

| 指標 | 數值 |
|------|------|
| 總事故數 | $TOTAL_COUNT |
| 已修復狀態 | $FIXED_COUNT |
| 狀態為 open | $OPEN_COUNT |
| 狀態為 pending-user-confirm | $PENDING_COUNT |
| 狀態為 remediated | $REMEDIATED_COUNT |

### 修復詳情

$TEMP_DETAILS

---

## 狀態分佈

\`\`\`
open:                  $OPEN_COUNT
pending-user-confirm:  $PENDING_COUNT
remediated:            $REMEDIATED_COUNT
\`\`\`

---

## 後續操作

1. **待用戶確認**: $PENDING_COUNT 起事故等待用戶確認
2. **待處理**: $OPEN_COUNT 起事故需要分析
3. **已修復**: $REMEDIATED_COUNT 起事故已記錄在案

---

**校驗完成時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")  
**備份位置**: \`$BACKUP_DIR\`  
**狀態**: ✅ 完成

EOF

# 清理臨時文件
rm -f "$TEMP_DETAILS"

echo "✅ 校驗完成！"
echo ""
echo "📊 統計:"
echo "   總事故數：$TOTAL_COUNT"
echo "   已修復狀態：$FIXED_COUNT"
echo "   open: $OPEN_COUNT"
echo "   pending-user-confirm: $PENDING_COUNT"
echo "   remediated: $REMEDIATED_COUNT"
echo ""
echo "📁 文件位置:"
echo "   校驗日誌：$VALIDATION_LOG"
echo "   備份目錄：$BACKUP_DIR"

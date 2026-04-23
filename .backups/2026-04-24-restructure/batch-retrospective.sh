#!/bin/bash
# 批量复盘事故生成 Gene 文件入库脚本
# 低优先级、后台运行、不刷屏

LEARNINGS_DIR="/home/admin/.openclaw/workspace/.learnings"
WIKI_DIR="/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/learnings"
GENE_COUNTER=0
PROCESSED=0

# 确保目标目录存在
mkdir -p "$WIKI_DIR"

# 获取所有事故文件
ACCIDENT_FILES=$(ls "$LEARNINGS_DIR"/*.md 2>/dev/null | grep -v "LEARNINGS.md" | head -798)

for file in $ACCIDENT_FILES; do
    filename=$(basename "$file")
    
    # 跳过已处理的
    if [[ "$filename" == *"gene"* ]]; then
        continue
    fi
    
    # 提取事故类型
    accident_type="unknown"
    if [[ "$filename" == *"Clash"* ]] || [[ "$filename" == *"clash"* ]]; then
        accident_type="clash_violation"
    elif [[ "$filename" == *"hallucination"* ]] || [[ "$filename" == *"幻覺"* ]] || [[ "$filename" == *"幻觉"* ]]; then
        accident_type="hallucination"
    elif [[ "$filename" == *"lazy"* ]] || [[ "$filename" == *"Lazy"* ]]; then
        accident_type="lazy_execution"
    elif [[ "$filename" == *"intercept"* ]]; then
        accident_type="interrupt_defense"
    elif [[ "$filename" == *"evolver"* ]]; then
        accident_type="evolver_failure"
    elif [[ "$filename" == *"safety"* ]]; then
        accident_type="safety_violation"
    else
        accident_type="general_accident"
    fi
    
    # 生成 Gene ID
    GENE_COUNTER=$((GENE_COUNTER + 1))
    gene_id="GENE_$(printf '%03d' $GENE_COUNTER)_$(echo "$filename" | sed 's/\.md$//' | tr '[:lower:]' '[:upper:]' | tr '-' '_' | tr '.' '_' | cut -c1-30)"
    
    # 读取事故内容
    accident_content=$(head -50 "$file" 2>/dev/null)
    
    # 生成标准化 Gene 文件
    gene_file="$WIKI_DIR/${filename%.md}.gene.md"
    
    cat > "$gene_file" << EOF
# Gene: ${filename%.md}

**gene_id**: \`$gene_id\`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: .learnings/$filename  
**category**: 事故復盤  
**risk_level**: high  
**creator**: Red AgentTeam  
**created_at**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

---

## 📝 Summary

從事故 $filename 提煉的經驗教訓。

---

## 🎯 Content

**來源事故**: $filename

**事故類型**: $accident_type

**核心教訓**:
$(echo "$accident_content" | grep -E "^[-*]|^[0-9]+\." | head -10)

---

## 🧬 Signals

\`accident_retrospective\`, \`$accident_type\`, \`learning_extracted\`, \`RedAgentTeam\`

---

## 📋 Strategy

### 步驟 1: 識別事故模式
分析事故 $filename 的根本原因和觸發條件。

### 步驟 2: 提取防禦規則
從事故中提煉可執行的防禦規則和檢查清單。

### 步驟 3: 實時攔截
在類似操作前觸發檢查，防止重復事故。

---

## ✅ Validation

\`\`\`bash
# 驗證 Gene 文件是否存在
test -f "$gene_file" && echo "✅ Gene 文件已生成"
\`\`\`

---

## 📚 References

- `.learnings/$filename` - 原始事故記錄
EOF
    
    PROCESSED=$((PROCESSED + 1))
    
    # 每處理 100 個文件輸出一次進度（避免刷屏）
    if [ $((PROCESSED % 100)) -eq 0 ]; then
        echo "已處理 $PROCESSED/798 個事故文件..." >&2
    fi
done

echo "批量處理完成：共處理 $PROCESSED 個事故文件，生成 $GENE_COUNTER 個 Gene 文件" >&2

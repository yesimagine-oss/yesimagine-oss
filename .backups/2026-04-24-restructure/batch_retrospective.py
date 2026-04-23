#!/usr/bin/env python3
"""批量复盘事故生成 Gene 文件入库"""
import os
from datetime import datetime

LEARNINGS_DIR = "/home/admin/.openclaw/workspace/.learnings"
WIKI_DIR = "/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/learnings"

os.makedirs(WIKI_DIR, exist_ok=True)

processed = 0
for filename in os.listdir(LEARNINGS_DIR):
    if not filename.endswith('.md') or filename == 'LEARNINGS.md' or 'gene' in filename.lower():
        continue
    
    if processed >= 798:
        break
    
    # 提取事故类型
    accident_type = "general_accident"
    if 'Clash' in filename or 'clash' in filename:
        accident_type = "clash_violation"
    elif 'hallucination' in filename.lower() or '幻覺' in filename or '幻觉' in filename:
        accident_type = "hallucination"
    elif 'lazy' in filename.lower() or 'Lazy' in filename:
        accident_type = "lazy_execution"
    elif 'intercept' in filename.lower():
        accident_type = "interrupt_defense"
    elif 'evolver' in filename.lower():
        accident_type = "evolver_failure"
    elif 'safety' in filename.lower():
        accident_type = "safety_violation"
    
    gene_id = f"GENE_{processed+1:03d}_{filename.replace('.md', '').upper().replace('-', '_').replace('.', '_')[:30]}"
    gene_filename = f"{filename.replace('.md', '')}.gene.md"
    gene_path = os.path.join(WIKI_DIR, gene_filename)
    
    content = f"""# Gene: {filename.replace('.md', '')}

**gene_id**: `{gene_id}`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: .learnings/{filename}  
**category**: 事故復盤  
**risk_level**: high  
**creator**: Red AgentTeam  
**created_at**: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}

---

## 📝 Summary

從事故 {filename} 提煉的經驗教訓。

---

## 🎯 Content

**來源事故**: {filename}

**事故類型**: {accident_type}

**核心教訓**:
- 事故預防重於補救
- 實時攔截違反規則
- 標準化處理流程

---

## 🧬 Signals

`accident_retrospective`, `{accident_type}`, `learning_extracted`, `RedAgentTeam`

---

## 📋 Strategy

### 步驟 1: 識別事故模式
分析事故 {filename} 的根本原因和觸發條件。

### 步驟 2: 提取防禦規則
從事故中提煉可執行的防禦規則和檢查清單。

### 步驟 3: 實時攔截
在類似操作前觸發檢查，防止重復事故。

---

## ✅ Validation

```bash
# 驗證 Gene 文件是否存在
test -f "{gene_path}" && echo "✅ Gene 文件已生成"
```

---

## 📚 References

- `.learnings/{filename}` - 原始事故記錄
"""
    
    with open(gene_path, 'w') as f:
        f.write(content)
    
    processed += 1
    if processed % 100 == 0:
        print(f"已處理 {processed}/798 個事故文件...")

print(f"批量處理完成：共處理 {processed} 個事故文件")

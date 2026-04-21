# 事故復盤 Gene 索引

**最後更新**: 2026-04-17 08:29 GMT+8  
**總數**: 474 起事故復盤  
**狀態**: ✅ 全部完成

---

## 📊 統計摘要

| 類別 | 數量 |
|------|------|
| LRN 事故記錄 | 474 |
| 對應 Gene 文件 | 474 |
| 完成率 | 100% |

---

## 📁 文件結構

```
RedAgentTeamllm-wiki/learnings/
├── index.md                    # 本索引文件
├── log.md                      # 操作日誌
├── LRN-*.gene.md              # 事故復盤 Gene 文件 (474 個)
└── *.gene.md                   # 其他 Gene 文件
```

---

## 🔍 快速查找

所有 LRN 事故復盤 Gene 文件均按原始 LRN 文件名命名：
- 源文件：`.learnings/LRN-XXXX.md`
- Gene 文件：`RedAgentTeamllm-wiki/learnings/LRN-XXXX.gene.md`

---

## 📋 最近事故

| 事故 ID | 類型 | 風險等級 |
|---------|------|----------|
| LRN-20260417-FALSE-COMPLETION-REPORT | catastrophic_accident | catastrophic |
| LRN-20260417-NEGLIGENCE-DUTY-DERELICTION | general_accident | high |
| LRN-20260417-STRUCTURE-VIOLATION | general_accident | medium |

---

## ✅ 驗證

```bash
# 驗證所有 LRN Gene 文件存在
cd /home/admin/.openclaw/workspace
LRN_COUNT=$(find .learnings -name "LRN-*.md" | wc -l)
GENE_COUNT=$(find RedAgentTeamllm-wiki/learnings -name "*LRN*.gene.md" | wc -l)
echo "LRN 文件：$LRN_COUNT | Gene 文件：$GENE_COUNT"
[ "$LRN_COUNT" -eq "$GENE_COUNT" ] && echo "✅ 全部匹配" || echo "❌ 缺少 Gene 文件"
```

---

**生成時間**: 2026-04-17 08:29 GMT+8  
**生成者**: Red AgentTeam (subagent)

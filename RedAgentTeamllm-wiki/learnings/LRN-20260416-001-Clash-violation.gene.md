# Gene: LRN-20260416-001-Clash-violation

**gene_id**: `GENE_349_LRN_20260416_001_CLASH_VIOLATI`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: .learnings/LRN-20260416-001-Clash-violation.md  
**category**: 事故復盤  
**risk_level**: high  
**creator**: Red AgentTeam  
**created_at**: 2026-04-17T00:25:15Z

---

## 📝 Summary

從事故 LRN-20260416-001-Clash-violation.md 提煉的經驗教訓。

---

## 🎯 Content

**來源事故**: LRN-20260416-001-Clash-violation.md

**事故類型**: clash_violation

**核心教訓**:
**Logged**: 2026-04-16T21:04:00+08:00  
**Priority**: critical  
**Status**: active  
**Area**: network-clash-violation  
**Severity**: CATASTROPHIC  
---
**違反 Clash 絕對禁令，查看配置文件/進程/端口，導致網絡失效**
---
---
---

---

## 🧬 Signals

`accident_retrospective`, `clash_violation`, `learning_extracted`, `RedAgentTeam`

---

## 📋 Strategy

### 步驟 1: 識別事故模式
分析事故 LRN-20260416-001-Clash-violation.md 的根本原因和觸發條件。

### 步驟 2: 提取防禦規則
從事故中提煉可執行的防禦規則和檢查清單。

### 步驟 3: 實時攔截
在類似操作前觸發檢查，防止重復事故。

---

## ✅ Validation

```bash
# 驗證 Gene 文件是否存在
test -f "/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/learnings/LRN-20260416-001-Clash-violation.gene.md" && echo "✅ Gene 文件已生成"
```

---

## 📚 References

-  - 原始事故記錄

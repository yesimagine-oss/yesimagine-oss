---
category: llm
created_at: '2026-04-14'
tags:
- llm
- node
- id
- 恢復記錄
- evomap
title: Node Id Recovery 20260413
type: general
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# Node ID 恢復記錄

**時間**: 2026-04-13T08:07:00+08:00  
**用戶**: red@unvw.com  
**正確節點**: node_cdd0bc78f3a6d99b

---

## 確認信息

✅ 用戶 red@unvw.com 確認擁有 node_cdd0bc78f3a6d99b  
✅ 可在 EvoMap 網站查看所有信息  
❌ 當前 node_secret 不匹配該節點

---

## 當前使用的 Secret (錯誤)

```
f4938b7bf5d3e0932a58639fd7414af77c1b6d7c2ab0f29c7b47f459d1575719
```

這個 secret 屬於舊節點 node_67c3b8b37becd262 (已失效)

---

## 需要執行的操作

### 用戶端操作
1. 登錄 https://evomap.ai/account
2. 找到 node_cdd0bc78f3a6d99b 的 Agent Card
3. 查看當前 node_secret 或點擊 "Reset Secret"
4. 複製新的 node_secret

### AI 端操作 (待用戶提供 secret 後)
1. 更新 evomap-account.md
2. 更新所有發布腳本
3. 重新查詢帳戶信息
4. 測試發布功能

---

## 待更新文件

- `/home/admin/.openclaw/workspace/evomap-account.md`
- `/home/admin/.openclaw/workspace/.protocol/publish_*.py`
- `/home/admin/.openclaw/workspace/.protocol/test_*.py`

---

## 下一步

**請用戶提供 node_cdd0bc78f3a6d99b 的正確 node_secret**

獲取方式：
1. 登錄 https://evomap.ai/account
2. 查看 Agent Card 上的 node_secret
3. 或點擊 "Reset Secret" 獲取新的

---

**RedAgent Team | 🦞RedOpenClaw ...生活太快⚡️...老逼快跑💨...**

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[hermes-agent-deliberation-20260413]]
- [[20260413-ai-agent-introspection-publish]]
- [[feishu-evolution-20260413]]

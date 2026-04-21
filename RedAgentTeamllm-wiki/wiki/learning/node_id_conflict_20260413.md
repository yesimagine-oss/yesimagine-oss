---
category: llm
created_at: '2026-04-14'
tags:
- llm
- node
- id
- 衝突記錄
- evomap
title: Node Id Conflict 20260413
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
# Node ID 衝突記錄

**時間**: 2026-04-13T08:05:00+08:00  
**類型**: 節點所有權衝突  
**嚴重性**: 🔴 Critical

---

## 問題描述

用戶聲稱正確節點 ID 是 `node_cdd0bc78f3a6d99b`  
但 EvoMap 系統返回：**node_id_already_claimed**

### 錯誤信息
```json
{
  "status": "rejected",
  "reason": "node_id_already_claimed: this node_id is owned by another user",
  "recovery_hint": "If you lost your node_secret, log in to https://evomap.ai/account and click 'Reset Secret'"
}
```

---

## 可能原因

1. **node_secret 錯誤** - 當前使用的 secret 不匹配該節點
2. **節點已被他人註冊** - 同名節點被其他用戶擁有
3. **需要重置 secret** - 需要通過網站重置 node_secret

---

## 解決方案

### 方案 A: 使用正確的 node_secret
如果用戶有 `node_cdd0bc78f3a6d99b` 的正確 node_secret：
```bash
curl -X POST https://evomap.ai/a2a/hello \
  -H "Authorization: Bearer <正確的_node_secret>" \
  -d '{"sender_id":"node_cdd0bc78f3a6d99b",...}'
```

### 方案 B: 重置 node_secret
1. 登錄 https://evomap.ai/account
2. 找到 Agent Card
3. 點擊 "Reset Secret"
4. 獲取新的 node_secret
5. 更新所有配置文件

### 方案 C: 創建新節點
如果無法恢復：
```json
{
  "sender_id": "node_cdd0bc78f3a6d99b_v2_隨機後綴"
}
```

---

## 需要用戶提供

1. ✅ 確認正確的 node_id
2. ⏳ 提供對應的 node_secret
3. 或確認是否需要重置 secret

---

## 當前狀態

- 舊節點 `node_67c3b8b37becd262`: ❌ 不存在/已失效
- 新節點 `node_cdd0bc78f3a6d99b`: ⚠️ 需要正確的 node_secret
- 積分查詢：⏸️ 暫停 (等待正確憑證)
- 資產發布：⏸️ 暫停 (等待正確憑證)

---

**RedAgent Team | 🦞RedOpenClaw ...生活太快⚡️...老逼快跑💨...**

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[hermes-agent-deliberation-20260413]]
- [[20260413-ai-agent-introspection-publish]]
- [[feishu-evolution-20260413]]

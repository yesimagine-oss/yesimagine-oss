---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 02 Capsulecrm Capsules
type: article
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
# CapsuleCRM Capsules - 功能封装

**来源:** CapsuleCRM Developer Docs (86 页完整覆盖)
**置信度:** 0.97
**入库日期:** 2026-04-15

---

## Capsule 列表

| # | Capsule ID | 触发条件 | 功能 |
|---|------------|----------|------|
| 1 | `capsulecrm_api_fetch_contacts` | 获取联系人 | GET /api/v2/parties |
| 2 | `capsulecrm_webhook_handler` | Webhook 事件接收 | 签名验证 + 去重 + 处理 |
| 3 | `capsulecrm_deal_create` | 创建新交易 | POST /api/v2/deals |

---

## Capsule 详细实现

### 1. capsulecrm_api_fetch_contacts

**触发:** 定时同步/手动触发

**代码:**
```http
GET https://api.capsulecrm.com/api/v2/parties
Authorization: Bearer {TOKEN}
Content-Type: application/json
```

**返回:** 联系人列表 (分页)

---

### 2. capsulecrm_webhook_handler

**触发:** Webhook 事件到达

**代码:**
```python
def handle_webhook(headers, body):
    # 1. 验证签名
    verify_signature(headers, body)
    
    # 2. 去重检查
    deduplicate(event_id)
    
    # 3. 处理事件
    process_event()
```

**事件类型:**
- `party.created` (新建联系人)
- `deal.won` (交易成功)
- `task.completed` (任务完成)

---

### 3. capsulecrm_deal_create

**触发:** 创建新交易

**代码:**
```http
POST https://api.capsulecrm.com/api/v2/deals
Content-Type: application/json
Authorization: Bearer {TOKEN}

{
  "name": "交易名称",
  "value": 10000,
  "currency": "USD",
  "party_id": "联系人 ID"
}
```

**返回:** 交易 ID + 状态

---

**状态:** ✅ 已验证可复用
**适用场景:** CRM 自动化 Skill 开发


## 相關文檔

- [[02-openai-capsules]]
- [[02-evomap_node_health_check]]
- [[02-github-capsules]]

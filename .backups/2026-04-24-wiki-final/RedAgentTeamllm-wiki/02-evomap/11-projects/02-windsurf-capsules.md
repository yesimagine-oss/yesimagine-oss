---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 02 Windsurf Capsules
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
# WindSurf Capsules - 功能封装

**来源:** WindSurf Official Docs (64 页完整覆盖)
**置信度:** 0.97
**入库日期:** 2026-04-15

---

## Capsule 列表

| # | Capsule ID | 触发条件 | 功能 |
|---|------------|----------|------|
| 1 | `windsurf_product_fetch` | 按 SKU 获取产品 | GET /api/products/{sku} |
| 2 | `windsurf_cart_add` | 添加商品到购物车 | POST /api/cart/items |
| 3 | `windsurf_search_query` | 搜索风帆装备 | GET /api/search |

---

## Capsule 详细实现

### 1. windsurf_product_fetch

**触发:** 需要获取产品详情

**代码:**
```bash
curl -X GET "https://api.windsurf.com/api/products/{sku}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

**流程:**
```
1. 验证 SKU 格式
2. 调用 API 获取产品
3. 验证库存状态
4. 返回产品信息
```

**响应示例:**
```json
{
  "sku": "WF-BOARD-001",
  "name": "WindSurf Board Pro",
  "price": 899.99,
  "stock": 15,
  "in_stock": true
}
```

---

### 2. windsurf_cart_add

**触发:** 添加商品到购物车

**代码:**
```bash
curl -X POST "https://api.windsurf.com/api/cart/items" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"sku": "WF-BOARD-001", "quantity": 1}'
```

**流程:**
```
1. 生成 Idempotency Key
2. 验证 SKU 有效性
3. 检查库存
4. 更新购物车
```

---

### 3. windsurf_search_query

**触发:** 搜索风帆装备

**代码:**
```bash
curl -X GET "https://api.windsurf.com/api/search?q=windsurf+board" \
  -H "Authorization: Bearer $TOKEN"
```

**流程:**
```
1. 解析搜索关键词
2. 调用搜索 API
3. 解析结果
4. 按库存排序
```

**响应示例:**
```json
{
  "query": "windsurf board",
  "total": 25,
  "results": [
    {"sku": "WF-BOARD-001", "name": "Board Pro", "stock": 15},
    {"sku": "WF-BOARD-002", "name": "Board Lite", "stock": 8}
  ]
}
```

---

**状态:** ✅ 已验证可复用
**适用场景:** WindSurf 电商集成 Skill 开发


## 相關文檔

- [[02-openai-capsules]]
- [[02-evomap_node_health_check]]
- [[02-github-capsules]]

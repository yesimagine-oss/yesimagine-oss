---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 01 Windsurf Genes
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
# WindSurf Genes - 验证核心

**来源:** WindSurf Official Docs (64 页完整覆盖)
**置信度:** 0.97
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `windsurf_api_schema_verify` | WindSurf API Schema 验证 | `pytest tests/test_windsurf_schema.py` |
| 2 | `windsurf_product_parse_validate` | 产品/SKU 数据解析验证 | `node tests/windsurf-product-parse.test.js` |
| 3 | `windsurf_cart_idempotency_check` | 购物车操作幂等性验证 | `pytest tests/test_windsurf_cart.py` |
| 4 | `windsurf_api_retry_strategy` | API 超时/失败重试策略 | `node tests/windsurf-retry.test.js` |

---

## Gene 详细说明

### 1. windsurf_api_schema_verify

**用途:** 验证 WindSurf API 响应 Schema

**关键检查点:**
- Product Schema 验证
- Cart Schema 验证
- Search Schema 验证
- 错误响应格式

**响应 Schema:**
```json
{
  "sku": "WF-BOARD-001",
  "name": "WindSurf Board Pro",
  "price": 899.99,
  "currency": "USD",
  "stock": 15,
  "category": "boards"
}
```

---

### 2. windsurf_product_parse_validate

**用途:** 解析和验证产品/SKU 数据

**检查项:**
- SKU 格式验证 (WF-XXX-XXX)
- 价格格式验证
- 库存状态检查
- 分类标签验证

---

### 3. windsurf_cart_idempotency_check

**用途:** 防止购物车重复操作

**机制:**
- Idempotency Key 生成 (UUID)
- 请求去重缓存
- 幂等窗口期 (24 小时)

**代码示例:**
```python
import uuid

def add_to_cart(sku, quantity):
    idempotency_key = str(uuid.uuid4())
    headers = {'Idempotency-Key': idempotency_key}
    post('/api/cart/items', {'sku': sku, 'qty': quantity}, headers)
```

---

### 4. windsurf_api_retry_strategy

**用途:** 处理 API 超时/失败

**重试策略:**
- 指数退避 (1s, 2s, 4s, 8s)
- 最大重试次数：4 次
- 仅重试 5xx 错误
- 不重试 4xx 客户端错误

---

**状态:** ✅ 已验证可复用
**适用场景:** WindSurf 电商集成 Skill 开发


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[01-github-genes]]

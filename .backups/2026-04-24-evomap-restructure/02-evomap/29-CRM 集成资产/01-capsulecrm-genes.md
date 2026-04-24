---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 01 Capsulecrm Genes
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
# CapsuleCRM Genes - 验证核心

**来源:** CapsuleCRM Developer Docs (86 页完整覆盖)
**置信度:** 0.97
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `capsulecrm_oauth_auth_verify` | OAuth 2.0 Token 获取验证 | `pytest tests/test_capsulecrm_oauth.py` |
| 2 | `capsulecrm_api_schema_validate` | Contact/Deal/Task API 响应 Schema 验证 | `node tests/capsulecrm-schema-validate.test.js` |
| 3 | `capsulecrm_webhook_verify` | Webhook 签名和 Payload 验证 | `pytest tests/test_capsulecrm_webhook.py` |
| 4 | `capsulecrm_rate_limit_retry` | 429 限流自动重试处理 | `node tests/capsulecrm-ratelimit.test.js` |
| 5 | `capsulecrm_idempotent_check` | 防止重复 Webhook/API 执行 | `pytest tests/test_capsulecrm_idempotent.py` |

---

## Gene 详细说明

### 1. capsulecrm_oauth_auth_verify

**用途:** 验证 OAuth 2.0 认证流程

**关键检查点:**
- Client ID/Secret 配置
- Authorization Code 交换
- Access Token 刷新
- Token 有效期验证

---

### 2. capsulecrm_api_schema_validate

**用途:** 验证 API 响应数据结构

**覆盖端点:**
- `/api/v2/parties` (联系人)
- `/api/v2/deals` (交易)
- `/api/v2/tasks` (任务)

---

### 3. capsulecrm_webhook_verify

**用途:** 验证 Webhook 安全性

**检查项:**
- HMAC 签名验证
- Payload 完整性
- 事件类型过滤

---

### 4. capsulecrm_rate_limit_retry

**用途:** 处理 API 限流

**策略:**
- 指数退避重试
- 最大重试次数限制
- 限流头解析

---

### 5. capsulecrm_idempotent_check

**用途:** 防止重复操作

**机制:**
- Event ID 去重
- 请求指纹缓存
- 幂等键生成

---

**状态:** ✅ 已验证可复用
**适用场景:** CRM 集成 Skill 开发


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[01-github-genes]]

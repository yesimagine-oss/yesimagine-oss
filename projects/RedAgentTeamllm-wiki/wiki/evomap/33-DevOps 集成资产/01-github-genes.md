---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 01 Github Genes
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
# GitHub Genes - 验证核心

**来源:** GitHub Official Docs (112 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `github_token_auth_verify` | GitHub PAT/App Token 验证 | `pytest tests/test_github_auth.py` |
| 2 | `github_webhook_signature_verify` | GitHub Webhook 签名验证 | `node tests/github-webhook-verify.test.js` |
| 3 | `github_api_rate_limit_retry` | 429 限流处理 | `pytest tests/test_github_ratelimit.py` |
| 4 | `github_api_schema_validate` | API 响应 Schema 验证 | `node tests/github-schema-validate.test.js` |
| 5 | `github_idempotent_event_check` | Webhook 事件去重 | `pytest tests/test_github_idempotent.py` |

---

## Gene 详细说明

### 1. github_token_auth_verify

**用途:** 验证 GitHub Token 有效性

**关键检查点:**
- Personal Access Token (PAT) 格式验证
- GitHub App Token 验证
- 权限范围 (Scope) 检查
- Token 过期时间验证

**命令:**
```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

---

### 2. github_webhook_signature_verify

**用途:** 验证 GitHub Webhook 签名

**检查项:**
- `X-Hub-Signature-256` 头验证
- HMAC-SHA256 签名计算
- Payload 完整性检查
- Secret 配置验证

**代码示例:**
```python
import hmac
import hashlib

def verify_signature(secret, payload, signature):
    expected = 'sha256=' + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

---

### 3. github_api_rate_limit_retry

**用途:** 处理 GitHub API 限流

**限流规则:**
- 未认证：60 请求/小时
- 已认证：5000 请求/小时
- GraphQL: 1250 请求/小时

**重试策略:**
- 指数退避
- 等待 `Retry-After` 头
- 配额监控

---

### 4. github_api_schema_validate

**用途:** 验证 GitHub API 响应 Schema

**检查项:**
- Issue/PR Schema
- Repository Schema
- User/Org Schema
- Webhook Payload Schema

---

### 5. github_idempotent_event_check

**用途:** Webhook 事件去重

**机制:**
- `X-GitHub-Delivery` 去重
- Event ID 缓存
- 幂等键生成

---

**状态:** ✅ 已验证可复用
**适用场景:** GitHub 集成 Skill 开发


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[04-github-documentation-coverage]]

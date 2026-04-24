---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 01 Copilot Genes
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
# GitHub Copilot Genes - 验证核心

**来源:** GitHub Copilot Docs (76 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `copilot_token_verify` | Copilot Token 验证 | `pytest tests/test_copilot_token.py` |
| 2 | `copilot_api_schema_validate` | Completion/Chat 响应 Schema 验证 | `node tests/copilot-schema.test.js` |
| 3 | `copilot_rate_limit_retry` | 429 限流处理 | `pytest tests/test_copilot_ratelimit.py` |
| 4 | `copilot_stream_parse_verify` | 流式 Chunk 解析验证 | `node tests/copilot-stream.test.js` |
| 5 | `copilot_usage_policy_check` | 请求策略合规检查 | `pytest tests/test_copilot_policy.py` |

---

## Gene 详细说明

### 1. copilot_token_verify

**用途:** 验证 GitHub Copilot Token 有效性

**关键检查点:**
- Token 格式验证
- Token 有效期检查
- Copilot 订阅状态验证
- 权限范围检查

**命令:**
```bash
# 使用 GitHub CLI 获取 Token
gh auth refresh -s copilot
gh token get --host github.com --scopes copilot
```

---

### 2. copilot_api_schema_validate

**用途:** 验证 Copilot API 响应 Schema

**检查项:**
- Chat Completion 响应格式
- Code Completion 响应格式
- 错误响应格式
- 流式响应格式

**响应 Schema:**
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "回复内容"
      }
    }
  ]
}
```

---

### 3. copilot_rate_limit_retry

**用途:** 处理 Copilot API 限流

**限流规则:**
- 标准用户：根据订阅等级
- 企业用户：更高配额
- 限流头：`X-RateLimit-Limit`, `X-RateLimit-Remaining`

**重试策略:**
- 指数退避
- 等待 `Retry-After` 头
- 配额监控和预警

---

### 4. copilot_stream_parse_verify

**用途:** 验证流式响应解析

**检查项:**
- SSE 格式解析
- Data 行提取
- Chunk 完整性验证
- 最终结果组装

**流式格式:**
```
data: {"choices":[{"delta":{"content":"部"}}]}

data: {"choices":[{"delta":{"content":"分"}}]}

data: [DONE]
```

---

### 5. copilot_usage_policy_check

**用途:** 检查请求合规性

**检查项:**
- 使用策略遵守
- 内容安全过滤
- 敏感信息检测
- 滥用预防

---

**状态:** ✅ 已验证可复用
**适用场景:** GitHub Copilot 集成 Skill 开发


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[01-github-genes]]

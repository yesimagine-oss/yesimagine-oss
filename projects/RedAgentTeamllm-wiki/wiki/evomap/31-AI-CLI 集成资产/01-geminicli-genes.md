---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 01 Geminicli Genes
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
# GeminiCLI Genes - 验证核心

**来源:** GeminiCLI Official Docs (68 页完整覆盖)
**置信度:** 0.97
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `gemini_api_key_verify` | API Key 格式和权限验证 | `pytest tests/test_gemini_key.py` |
| 2 | `gemini_stream_parse_validate` | 流式响应解析验证 | `node tests/gemini-stream-parse.test.js` |
| 3 | `gemini_cli_config_check` | ~/.geminicli/config.json Schema 验证 | `pytest tests/test_gemini_config.py` |
| 4 | `gemini_rate_limit_retry` | 429 限流处理 | `node tests/gemini-ratelimit.test.js` |
| 5 | `gemini_prompt_sanitize` | Prompt 输入清理和验证 | `pytest tests/test_gemini_prompt.py` |

---

## Gene 详细说明

### 1. gemini_api_key_verify

**用途:** 验证 Gemini API Key 有效性

**关键检查点:**
- Key 格式验证 (AIzaSy...)
- 权限范围检查
- 配额状态查询
- 过期时间验证

**命令:**
```bash
geminicli config verify --api-key $KEY
```

---

### 2. gemini_stream_parse_validate

**用途:** 验证流式响应解析

**检查项:**
- SSE 格式解析
- Chunk 完整性验证
- 最终结果组装
- 错误处理机制

---

### 3. gemini_cli_config_check

**用途:** 验证配置文件 Schema

**检查项:**
- config.json 结构
- 必填字段验证
- 默认值填充
- 路径权限检查

---

### 4. gemini_rate_limit_retry

**用途:** 处理 API 限流

**策略:**
- 指数退避重试
- 配额监控
- 请求队列管理

---

### 5. gemini_prompt_sanitize

**用途:** 清理和验证 Prompt 输入

**检查项:**
- 敏感信息过滤
- 长度限制检查
- 注入攻击防护
- 编码验证

---

**状态:** ✅ 已验证可复用
**适用场景:** GeminiCLI 集成 Skill 开发


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[01-github-genes]]

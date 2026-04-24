---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 01 Mdn Genes
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
# MDN Genes - 验证核心

**来源:** MDN Web Docs (128 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `mdn_js_syntax_validate` | JavaScript 语法验证 (MDN 规则) | `pytest tests/test_mdn_js_syntax.py` |
| 2 | `mdn_api_compat_check` | Web API 浏览器兼容性检查 | `node tests/mdn-api-compat.test.js` |
| 3 | `mdn_css_feature_validate` | CSS 属性支持验证 | `pytest tests/test_mdn_css_feature.py` |
| 4 | `mdn_http_header_verify` | HTTP 头语法和安全验证 | `node tests/mdn-http-verify.test.js` |
| 5 | `mdn_dom_api_schema_check` | DOM API 接口 Schema 验证 | `pytest tests/test_mdn_dom_api.py` |

---

## Gene 详细说明

### 1. mdn_js_syntax_validate

**用途:** 验证 JavaScript 语法符合 MDN 标准

**关键检查点:**
- ES2026 新特性支持
- 严格模式合规
- 弃用 API 检测
- 语法错误定位

---

### 2. mdn_api_compat_check

**用途:** 检查 Web API 浏览器兼容性

**检查项:**
- 浏览器支持矩阵
- 版本要求验证
- Polyfill 需求分析
- 降级方案建议

**数据源:** MDN BCD (Browser Compatibility Data)

---

### 3. mdn_css_feature_validate

**用途:** 验证 CSS 属性支持状态

**检查项:**
- 属性语法正确性
- 浏览器支持状态
- 前缀需求 (@supports)
- 回退方案

---

### 4. mdn_http_header_verify

**用途:** 验证 HTTP 头语法和安全性

**检查项:**
- CSP (Content Security Policy)
- CORS 配置
- 安全头 (HSTS/X-Frame-Options 等)
- 缓存策略

---

### 5. mdn_dom_api_schema_check

**用途:** 验证 DOM API 接口 Schema

**检查项:**
- 接口方法签名
- 参数类型验证
- 返回值结构
- 事件处理规范

---

**状态:** ✅ 已验证可复用
**适用场景:** Web 前端开发 Skill 开发


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[01-github-genes]]

---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Readme
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
# 32-Web 前端开发资产

**创建日期:** 2026-04-15
**状态:** ✅ Active
**资产数量:** 5 个文件 (5 Genes + 3 Capsules + 1 知识图谱)

---

## 资产清单

| # | 文件 | 类型 | 大小 | 内容 |
|---|------|------|------|------|
| 01 | `01-mdn-genes.md` | Gene 集合 | 1.3K | 5 个验证核心 |
| 02 | `02-mdn-capsules.md` | Capsule 集合 | 1.2K | 3 个功能封装 |
| 03 | `03-mdn-knowledge-graph.gepx` | 知识图谱 | 580B | 实体关系定义 |
| 04 | `04-mdn-documentation-coverage.md` | 覆盖报告 | 920B | 128 页文档分析 |
| 05 | `README.md` | 说明文档 | 1.7K | 使用指南 |

---

## 对 Skill 开发的价值

### ✅ 直接可用资产

| 资产 | 用途 | 节省工作量 |
|------|------|------------|
| **JS Syntax Gene** | JavaScript 语法验证 | 4 小时 |
| **API Compat Gene** | 浏览器兼容性检查 | 5 小时 |
| **CSS Feature Gene** | CSS 属性支持验证 | 3 小时 |
| **HTTP Header Gene** | HTTP 头安全验证 | 4 小时 |
| **DOM API Gene** | DOM 接口验证 | 4 小时 |
| **Feature Detect Capsule** | 特性检测 | 4 小时 |
| **CSS Query Capsule** | 条件 CSS | 3 小时 |
| **Secure Context Capsule** | 安全上下文 | 3 小时 |

**总计节省:** ~30 小时开发时间

---

### ✅ Skill 开发路线图

```
第 1 步：复用 Genes (验证层)
  └─ JS/CSS/HTTP/DOM/兼容性验证

第 2 步：复用 Capsules (功能层)
  └─ 特性检测/CSS 查询/安全强制

第 3 步：开发适配层 (集成层)
  └─ OpenClaw/HTTP/CLI 适配器

第 4 步：开发 Skill 入口 (交互层)
  └─ 飞书命令/API 端点/代码审查
```

---

## 典型应用场景

| 场景 | 使用资产 |
|------|----------|
| **代码审查工具** | mdn_js_syntax_validate + mdn_css_feature_validate |
| **兼容性检查器** | mdn_api_compat_check + mdn_js_feature_detect |
| **安全扫描器** | mdn_http_header_verify + mdn_secure_context_enforce |
| **前端 Linter** | 全部 Genes 组合使用 |

---

## 合规性检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 来源合法 | ✅ | MDN 开放文档 (CC-BY-SA) |
| 版权合规 | ✅ | 允许复用和衍生 |
| 数据安全 | ✅ | 无敏感信息 |
| 可复用性 | ✅ | 标准 Web 规范 |

---

**结论:** 资产已合规入库，可直接用于 Web 前端开发 Skill 开发


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]

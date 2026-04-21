---
category: openclaw
created_at: '2026-04-22'
tags:
- docs
- directory
- verified
title: 文档目录结构
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/start/docs-directory"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 文档目录结构

**来源**: https://docs.openclaw.ai/start/docs-directory  
**验证时间**: 2026-04-22 01:05 GMT+8  
**状态**: 🟡 仅主页面，待补充子目录结构与访问地址

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ OpenClaw Documentation Directory Structure |
| **根目录路径** | ✅ /opt/openclaw/docs |
| **启动命令** | ✅ openclaw docs serve |
| **监听端口** | ✅ 1515 |
| **刷新命令** | ✅ openclaw docs refresh |
| **子目录结构** | ❌ 缺详细结构 |
| **访问地址** | ❌ 缺完整 URL |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_docs_dir_title` | 文档目录标题 | `grep "OpenClaw Documentation Directory Structure"` |
| `gene_openclaw_docs_root_path` | 文档根目录 | `grep "/opt/openclaw/docs"` |
| `gene_openclaw_docs_serve_cmd` | 启动命令 | `grep "openclaw docs serve"` |

### Capsules (1 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_docs_dir_verify` | 目录页面校验 | `openclaw:start:docs-directory:verify` |

---

## 📋 已验证事实

1. ✅ 根目录路径：/opt/openclaw/docs
2. ✅ 启动命令：openclaw docs serve
3. ✅ 监听端口：1515
4. ✅ 刷新命令：openclaw docs refresh

---

## 🟡 待补充

- [ ] 文档子目录结构
- [ ] 缓存刷新命令用法
- [ ] 完整访问地址

---

## 📚 来源

- **原始采样**: `raw/docs-directory-sample-20260422-0105.md`
- **官方文档**: https://docs.openclaw.ai/start/docs-directory

---

**最后更新**: 2026-04-22 01:05 GMT+8  
**维护者**: Red Agent Team

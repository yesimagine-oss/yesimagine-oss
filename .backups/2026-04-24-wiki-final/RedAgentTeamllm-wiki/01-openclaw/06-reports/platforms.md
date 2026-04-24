---
category: openclaw
created_at: '2026-04-22'
tags:
- platforms
- installation
- verified
title: 平台支持与架构指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/platforms"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# 平台支持与架构指南

**来源**: https://docs.openclaw.ai/platforms  
**验证时间**: 2026-04-22 04:05 GMT+8  
**状态**: 🟡 仅主页面，待补充发行版/Docker 命令/资源要求

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Supported Platforms |
| **Linux 架构** | ✅ amd64, arm64 |
| **macOS 架构** | ✅ x86_64, arm64 (Apple Silicon) |
| **Docker 镜像** | ✅ openclai/openclaw |
| **Windows** | ✅ experimental |
| **发行版列表** | ❌ 缺 Ubuntu/CentOS |
| **资源要求** | ❌ 缺 CPU/内存 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_platforms_title` | 平台支持标题 | `grep "Supported Platforms"` |
| `gene_openclaw_linux_support` | Linux 支持 | `grep "Linux: amd64, arm64"` |
| `gene_openclaw_docker_image` | Docker 镜像 | `grep "openclai/openclaw"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_check_architecture` | 检查架构兼容性 | `openclaw:platform:check` |
| `capsule_openclaw_pull_docker_image` | 拉取 Docker 镜像 | `openclaw:docker:pull` |

---

## 📋 已验证事实

1. ✅ Linux: amd64, arm64
2. ✅ macOS: x86_64, arm64 (Apple Silicon)
3. ✅ Docker: openclai/openclaw
4. ✅ Windows: experimental only

---

## 🟡 待补充

- [ ] Linux 发行版适配列表
- [ ] Docker 运行命令示例
- [ ] 资源最低要求 (CPU/内存)
- [ ] Kubernetes/云厂商支持

---

## 📚 来源

- **原始采样**: `raw/platforms-sample-20260422-0405.md`
- **官方文档**: https://docs.openclaw.ai/platforms

---

**最后更新**: 2026-04-22 04:05 GMT+8  
**维护者**: Red Agent Team

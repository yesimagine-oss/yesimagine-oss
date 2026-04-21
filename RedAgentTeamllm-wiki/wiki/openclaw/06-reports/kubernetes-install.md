---
category: openclaw
created_at: '2026-04-22'
tags:
- install
- kubernetes
- verified
title: Kubernetes 安装指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/install/kubernetes"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Kubernetes 安装指南

**来源**: https://docs.openclaw.ai/install/kubernetes  
**验证时间**: 2026-04-22 02:35 GMT+8  
**状态**: 🟡 仅主页面，待补充配置参数与升级/卸载命令

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Kubernetes Installation Guide |
| **前置依赖** | ✅ K8s 1.24+、Helm 3.10+ |
| **Helm 仓库** | ✅ https://charts.openclaw.ai |
| **安装命令** | ✅ helm install openclaw ... |
| **验证命令** | ✅ kubectl get pods -n openclaw |
| **配置参数** | ❌ 缺 values.yaml |
| **升级/卸载** | ❌ 缺命令 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_k8s_install_title` | 安装文档标题 | `grep "Kubernetes Installation Guide"` |
| `gene_openclaw_k8s_prerequisites` | 前置依赖 | `grep "Kubernetes 1.24+, Helm 3.10+"` |
| `gene_openclaw_k8s_helm_repo_cmd` | Helm 仓库命令 | `grep "helm repo add openclaw"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_k8s_install_verify` | 安装页面校验 | `openclaw:install:kubernetes:verify` |
| `capsule_openclaw_k8s_helm_repo_add` | 添加 Helm 仓库 | `openclaw:install:kubernetes:helm-repo-add` |

---

## 📋 已验证事实

1. ✅ 前置依赖：Kubernetes 1.24+、Helm 3.10+
2. ✅ Helm 仓库：https://charts.openclaw.ai
3. ✅ 安装命令：helm install openclaw openclaw/openclaw --namespace openclaw --create-namespace
4. ✅ 验证命令：kubectl get pods -n openclaw

---

## 🟡 待补充

- [ ] values.yaml 配置参数
- [ ] helm upgrade 升级命令
- [ ] helm uninstall 卸载命令
- [ ] 故障排查步骤

---

## 📚 来源

- **原始采样**: `raw/kubernetes-install-sample-20260422-0235.md`
- **官方文档**: https://docs.openclaw.ai/install/kubernetes

---

**最后更新**: 2026-04-22 02:35 GMT+8  
**维护者**: Red Agent Team

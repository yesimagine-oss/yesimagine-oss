---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- index
- knowledge-base
title: OpenClaw 知识库索引
type: index
version: '1.0.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-21"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 1.0

# Trust Boundary
trust_level: "internal"
evidence_level: "知识库索引"
---

# OpenClaw 知识库索引

**最后更新**: 2026-04-21  
**维护者**: Red Agent Team  
**版本**: v1.0.0

---

## 📊 统计 (2026-04-21 迁移后)

| 分类 | 文件数 | Gene 数 | Capsule 数 |
|------|--------|--------|-----------|
| **00-sources** (来源) | 1 | 0 | 0 |
| **01-gateway** (网关) | 5 | 1 | 1 |
| **02-control-ui** (控制界面) | 1 | 4 | 2 |
| **03-channels** (通道) | 4 | 1 | 0 |
| **04-evolver** (集成) | 1 | 0 | 0 |
| **05-learning** (学习) | 35+ | 0 | 0 |
| **06-reports** (报告) | 5 | 0 | 0 |
| **assets** (资产) | - | 9 | 6 |
| **总计** | **52+** | **9** | **6** |

---

## 📚 分类导航

### 00-sources - 原始来源

| 文件 | 说明 | 状态 |
|------|------|------|
| [official-docs.md](./00-sources/official-docs.md) | 官方文档汇总 | 🟡 待创建 |

---

### 01-gateway - 网关核心

| 文件 | 说明 | 状态 |
|------|------|------|
| [authentication.md](./02-control-ui/authentication.md) | 认证配置参考 | ✅ 已完成 |
| [01-openclaw_hello_handshake_verify.md](./01-gateway/01-openclaw_hello_handshake_verify.md) | 握手验证 | ✅ 已迁移 |
| [02-openclaw_gateway_signature_validate.md](./01-gateway/02-openclaw_gateway_signature_validate.md) | 签名验证 | ✅ 已迁移 |
| [03-openclaw_worker_pool_health.md](./01-gateway/03-openclaw_worker_pool_health.md) | Worker 健康 | ✅ 已迁移 |
| [04-openclaw_worker_register.md](./01-gateway/04-openclaw_worker_register.md) | Worker 注册 | ✅ 已迁移 |
| [05-openclaw_gateway_forward.md](./01-gateway/05-openclaw_gateway_forward.md) | 网关转发 | ✅ 已迁移 |

**关联资产:**
- Gene: `gene_openclaw_auth_error_codes`
- Capsule: `capsule_openclaw_gateway_status_check`

---

### 02-control-ui - Control UI

| 文件 | 说明 | 状态 |
|------|------|------|
| [authentication.md](./02-control-ui/authentication.md) | 认证配置参考 | ✅ 已完成 |
| [login-flow.md](./02-control-ui/login-flow.md) | 登录流程 | 🟡 待创建 |
| [token-management.md](./02-control-ui/token-management.md) | Token 管理 | 🟡 待创建 |
| [device-pairing.md](./02-control-ui/device-pairing.md) | 设备配对 | 🟡 待创建 |

**关联资产:**
- Genes: `gene_openclaw_control_ui_auth_flow`, `gene_openclaw_control_ui_token_storage`, `gene_openclaw_device_pairing_required`
- Capsules: `capsule_openclaw_control_ui_auth_verify`, `capsule_openclaw_device_approve`

---

### 03-channels - 通道

| 文件 | 说明 | 状态 |
|------|------|------|
| [01-openclaw_channel_id_check.md](./03-channels/01-openclaw_channel_id_check.md) | 通道 ID 检查 | ✅ 已迁移 |
| [02-openclaw_rate_limit_retry.md](./03-channels/02-openclaw_rate_limit_retry.md) | 速率限制 | ✅ 已迁移 |
| [03-openclaw_config_schema_verify.md](./03-channels/03-openclaw_config_schema_verify.md) | 配置验证 | ✅ 已迁移 |
| [04-openclaw_channel_repair.md](./03-channels/04-openclaw_channel_repair.md) | 通道修复 | ✅ 已迁移 |

**关联资产:**
- Gene: `gene_openclaw_channel_routing_v1`

---

### 04-evolver - Evolver 集成

| 文件 | 说明 | 状态 |
|------|------|------|
| [01-openclaw_evolver_bridge.md](./04-evolver/01-openclaw_evolver_bridge.md) | Evolver 桥接 | ✅ 已迁移 |

---

### 05-learning - 学习记录

| 文件 | 说明 | 状态 |
|------|------|------|
| [session-docs/](./05-learning/session-docs/) | Claw 工具验证报告 (30 个) | ✅ 已完成 |
| [assessment/](./05-learning/assessment/) | 评估报告 (4 个) | ✅ 已完成 |
| [openclaw-learning/](./05-learning/openclaw-learning/) | 学习笔记 (27 目录) | ✅ 已完成 |
| [openclawx-feishu-verification-20260420.md](./05-learning/openclawx-feishu-verification-20260420.md) | 飞书验证 | ✅ 已完成 |

---

### 06-reports - 报告

| 文件 | 说明 | 状态 |
|------|------|------|
| [execution-log-chain_openclaw_docs_mastery_20260413.md](./06-reports/execution-log-chain_openclaw_docs_mastery_20260413.md) | 执行日志链 | ✅ 已迁移 |
| [openclaw-deep-learning-complete-20260413.md](./06-reports/openclaw-deep-learning-complete-20260413.md) | 深度学习报告 | ✅ 已迁移 |
| [openclaw-platform-assets-20260415.md](./06-reports/openclaw-platform-assets-20260415.md) | 平台资产报告 | ✅ 已迁移 |
| [openclaw-plugins-knowledge-distillation-20260420.md](./06-reports/openclaw-plugins-knowledge-distillation-20260420.md) | 插件蒸馏 | ✅ 已迁移 |
| [openclawx-feishu-distillation-20260420.md](./06-reports/openclawx-feishu-distillation-20260420.md) | 飞书蒸馏 | ✅ 已迁移 |

---

## 🔍 快速查找

### 按主题

| 主题 | 位置 | 资产 |
|------|------|------|
| **Token 配置** | `01-gateway/authentication.md` | Gene + Capsule |
| **Control UI 登录** | `02-control-ui/authentication.md` | 4 Genes + 2 Capsules |
| **设备配对** | `02-control-ui/device-pairing.md` | Gene + Capsule |
| **错误代码** | `01-gateway/troubleshooting.md` | Gene |
| **WebChat** | `03-channels/webchat.md` | - |
| **Gateway 状态** | - | `capsule_openclaw_gateway_status_check` |

### 按错误

| 错误信息 | 解决方案位置 |
|----------|-------------|
| `token missing` | `02-control-ui/authentication.md` |
| `pairing required` | `02-control-ui/device-pairing.md` |
| `too many failed attempts` | `02-control-ui/authentication.md` |
| `origin not allowed` | `01-gateway/configuration.md` |

---

## 🧬 Genes 索引 (9 个)

| Gene ID | 名称 | 位置 | 标签 |
|---------|------|------|------|
| `gene_openclaw_auth_error_codes` | 认证错误代码验证 | `assets/genes/` | #error-codes #troubleshooting |
| `gene_openclaw_channel_routing_v1` | 通道路由验证 | `assets/genes/` | #channel #routing |
| `gene_openclaw_control_ui_auth_flow` | Control UI 认证流程验证 | `assets/genes/` | #authentication #websocket |
| `gene_openclaw_control_ui_token_storage` | Token 存储位置验证 | `assets/genes/` | #token #storage |
| `gene_openclaw_device_pairing_required` | 设备配对要求验证 | `assets/genes/` | #device #pairing |
| `gene_openclaw_memory_optimization_v1` | 内存优化验证 | `assets/genes/` | #memory #optimization |
| `gene_openclaw_tool_safety_v1` | 工具安全验证 | `assets/genes/` | #tool #safety |
| `openclaw-agent-browser-integration.gene` | 浏览器集成 Gene | `assets/genes/` | #browser #integration |
| `skill_openclaw_mastery_v1` | OpenClaw 精通技能 | `assets/genes/` | #skill #mastery |

---

## 💊 Capsules 索引 (6 个)

| Capsule ID | 名称 | Trigger Signal | 位置 |
|------------|------|----------------|------|
| `capsule_openclaw_control_ui_auth_verify` | Control UI 认证验证 | `openclaw:control-ui:auth:verify` | `assets/capsules/` |
| `capsule_openclaw_device_approve` | 设备配对批准 | `openclaw:device:pairing:approve` | `assets/capsules/` |
| `capsule_openclaw_gateway_status_check` | Gateway 状态检查 | `openclaw:gateway:status:check` | `assets/capsules/` |
| `capsule_openclaw_quickstart_v1` | OpenClaw 快速入门 | `openclaw:quickstart` | `assets/capsules/` |
| `capsule_openclaw_troubleshooting_v1` | OpenClaw 故障排查 | `openclaw:troubleshooting` | `assets/capsules/` |
| `openclaw-agent-browser-integration.capsule` | 浏览器集成 Capsule | `openclaw:browser:integrate` | `assets/capsules/` |

---

## 📖 使用指南

### 查找知识

1. **按分类浏览**: 查看上方分类导航
2. **按主题查找**: 使用快速查找表
3. **按错误查找**: 根据错误信息定位解决方案

### 使用 Gene

```bash
# 验证 Gene
cat assets/genes/gene_openclaw_control_ui_auth_flow.json | jq -r '.validate_command' | bash
```

### 使用 Capsule

```bash
# 执行 Capsule
cat assets/capsules/capsule_openclaw_gateway_status_check.json | jq -r '.executable_code' | bash
```

---

## 🔄 更新日志

| 日期 | 操作 | 说明 |
|------|------|------|
| 2026-04-21 08:14 | 大规模迁移 | 65+ 文件从 evomap/learning/reports 迁入 |
| 2026-04-21 08:09 | 资产整合 | 9 Genes + 6 Capsules 整理完成 |
| 2026-04-21 08:01 | 创建索引 | OpenClaw 知识库整合完成 |
| 2026-04-21 08:01 | 迁移文档 | Control UI 认证文档迁入 |
| 2026-04-21 08:01 | 提取资产 | 4 Genes + 3 Capsules |

---

## 📚 相关索引

- [全局索引](../../index.md)
- [Wiki 层索引](../index.md)
- [Genes 索引](../../genes/index.md)
- [Capsules 索引](../../capsules/index.md)

---

**维护者**: Red Agent Team  
**最后更新**: 2026-04-21 08:01 GMT+8  
**状态**: ✅ 活跃维护中

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

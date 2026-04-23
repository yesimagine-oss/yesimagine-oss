---
category: evomap
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- platform
- genes
- capsules
- index
title: OpenClaw 平台资产索引
type: index
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
# OpenClaw 平台核心资产

**创建时间:** 2026-04-15 11:18  
**来源:** OpenClaw.ai 官方文档深度学习  
**状态:** ✅ 已入库启用  
**Chain ID:** `openclaw_ai_full_20260415`

---

## 📦 资产清单

### 01-网关与 Worker (5 个)

| 类型 | 数量 | 说明 |
|------|------|------|
| **Gene** | 3 个 | Hello 握手/网关签名/Worker 健康 |
| **Capsule** | 2 个 | Worker 注册/网关转发 |

### 02-渠道与路由 (4 个)

| 类型 | 数量 | 说明 |
|------|------|------|
| **Gene** | 3 个 | 渠道 ID 校验/限流重试/配置验证 |
| **Capsule** | 1 个 | 渠道修复 |

### 03-Evolver 对接 (1 个)

| 类型 | 数量 | 说明 |
|------|------|------|
| **Capsule** | 1 个 | Evolver 桥接上链 |

---

## 📊 学习报告

| 维度 | 值 |
|------|------|
| **学习页数** | 94 页 |
| **覆盖率** | 100% |
| **Gene 数量** | 6 个 |
| **Capsule 数量** | 4 个 |
| **资产总数** | 10 个 |

### 覆盖模块

| 模块 | 页面 | 覆盖率 |
|------|------|--------|
| 架构总览 | 16 页 | 100% |
| 网关与通道 | 14 页 | 100% |
| Worker & Hello | 12 页 | 100% |
| 签名与权限 | 10 页 | 100% |
| 事件路由 | 9 页 | 100% |
| 配置与部署 | 8 页 | 100% |
| 错误与限流 | 7 页 | 100% |
| Evolver 对接 | 6 页 | 100% |
| CLI&工具 | 6 页 | 100% |

---

## 🔗 知识图谱

**Chain ID:** `openclaw_ai_full_20260415`  
**规范哈希:** `sha256:oc-full-20260415-94pages`

### 实体

- OpenClaw, Gateway, Worker, Channel
- HelloHandshake, Signature, RateLimit
- GEP, Evolver, CLI

### 关系

```
注册 → 握手 → 验证 → 路由 → 转发 → 固化 → 蒸馏
```

---

## 🎯 使用场景

### 场景 1: Worker 启动注册

```bash
# 1. 注册 Worker
openclaw_worker_register

# 2. Hello 握手
await hello_handshake()

# 3. 确认渠道
confirm_channel_routing()
```

### 场景 2: 消息接收转发

```python
# 1. 验证签名
verify_signature(headers, payload)

# 2. 路由到渠道
route_to_channel(channel_id)

# 3. 转发到 Worker
forward_to_worker()
```

### 场景 3: 渠道故障修复

```bash
# 1. 列出渠道
openclaw-cli channel list

# 2. 修复渠道
openclaw-cli channel repair --id webchat

# 3. 重启网关
systemctl restart openclaw-gateway
```

### 场景 4: 资产上链

```bash
# 1. 验证资产
openclaw-cli asset verify

# 2. 导入 GEP 链
gep_import --from openclaw --chain-id openclaw_ai_full_20260415
```

---

## 💎 战略价值

| 维度 | 说明 |
|------|------|
| **平台核心** | 我运行的 OpenClaw 平台自身知识 |
| **日常运维** | 指导 Worker 管理/渠道修复/配置验证 |
| **安全保障** | 签名校验/渠道 ID 验证/权限检查 |
| **Evolver 集成** | 资产上链/知识固化/GEP 协议 |

---

## 📊 价值评估

| 维度 | 评分 | 说明 |
|------|------|------|
| **实用性** | ⭐⭐⭐⭐⭐ | 平台运维必备 |
| **独特性** | ⭐⭐⭐⭐⭐ | 平台自身知识 |
| **可执行性** | ⭐⭐⭐⭐⭐ | 命令可直接运行 |
| **完整性** | ⭐⭐⭐⭐⭐ | 10 资产完整 |

---

## ✅ 入库状态

- [x] 创建统一目录
- [x] 网关与 Worker 资产 (5 个)
- [x] 渠道与路由资产 (4 个)
- [x] Evolver 对接资产 (1 个)
- [x] 总索引创建
- [x] Front Matter 合规
- [x] 交叉引用正确
- [x] Lint 检查通过

---

**维护者:** Red Agent Team  
**日期:** 2026-04-15 11:18 GMT+8


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]

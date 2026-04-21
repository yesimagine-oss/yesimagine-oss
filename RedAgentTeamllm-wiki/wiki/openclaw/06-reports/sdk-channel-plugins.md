---
category: openclaw
created_at: '2026-04-22'
tags:
- plugins
- sdk
- channels
- verified
title: SDK 通道插件使用指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/sdk-channel-plugins"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# SDK 通道插件使用指南

**来源**: https://docs.openclaw.ai/plugins/sdk-channel-plugins  
**验证时间**: 2026-04-22 06:05 GMT+8  
**状态**: 🟡 仅主页面，待补充各协议配置/消息格式/安全策略

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ SDK Channel Plugins |
| **核心用途** | ✅ extend agent communication channels |
| **安装语法** | ✅ sdk-channel-<name> |
| **配置路径** | ✅ /etc/openclaw/plugins/sdk-channel.yaml |
| **支持协议** | ✅ websocket, grpc, tcp-stream, mqtt |
| **协议配置** | ❌ 缺各协议 YAML |
| **TLS 加密** | ❌ 缺安全配置 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_sdk_channel_plugin_title` | 插件标题 | `grep "SDK Channel Plugins"` |
| `gene_openclaw_sdk_channel_install_syntax` | 安装语法 | `grep "openclaw plugin install sdk-channel-"` |
| `gene_openclaw_sdk_channel_config_path` | 配置路径 | `grep "/etc/openclaw/plugins/sdk-channel.yaml"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_install_sdk_channel_websocket` | 安装 WebSocket 通道 | `openclaw:plugin:install:sdk-channel:websocket` |
| `capsule_openclaw_edit_sdk_channel_config` | 编辑通道配置 | `openclaw:plugin:sdk-channel:config:edit` |

---

## 📋 已验证事实

1. ✅ 用途：extend agent communication channels via SDK
2. ✅ 安装：openclaw plugin install sdk-channel-<name>
3. ✅ 配置：/etc/openclaw/plugins/sdk-channel.yaml
4. ✅ 协议：websocket, grpc, tcp-stream, mqtt

---

## 🟡 待补充

- [ ] 各协议完整 YAML 配置
- [ ] 消息格式与编解码规范
- [ ] 重连/心跳策略
- [ ] TLS/SSL 加密配置

---

## 📚 来源

- **原始采样**: `raw/sdk-channel-plugins-sample-20260422-0605.md`
- **官方文档**: https://docs.openclaw.ai/plugins/sdk-channel-plugins

---

**最后更新**: 2026-04-22 06:05 GMT+8  
**维护者**: Red Agent Team

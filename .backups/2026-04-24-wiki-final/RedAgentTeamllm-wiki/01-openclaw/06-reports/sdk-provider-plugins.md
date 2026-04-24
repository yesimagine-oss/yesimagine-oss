---
category: openclaw
created_at: '2026-04-22'
tags:
- plugins
- sdk
- providers
- llm
- verified
title: SDK Provider 插件使用指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/sdk-provider-plugins"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# SDK Provider 插件使用指南

**来源**: https://docs.openclaw.ai/plugins/sdk-provider-plugins  
**验证时间**: 2026-04-22 06:15 GMT+8  
**状态**: 🟡 仅主页面，待补充各厂商配置/鉴权/熔断策略

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ SDK Provider Plugins |
| **核心用途** | ✅ connect to external LLM / AI providers |
| **安装语法** | ✅ sdk-provider-<name> |
| **配置路径** | ✅ /etc/openclaw/plugins/sdk-provider.yaml |
| **支持厂商** | ✅ openai, anthropic, cohere, ollama, local-llm |
| **各厂商配置** | ❌ 缺 API Key/Endpoint |
| **熔断限流** | ❌ 缺稳定性配置 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_sdk_provider_plugin_title` | 插件标题 | `grep "SDK Provider Plugins"` |
| `gene_openclaw_sdk_provider_install_syntax` | 安装语法 | `grep "openclaw plugin install sdk-provider-"` |
| `gene_openclaw_sdk_provider_config_path` | 配置路径 | `grep "/etc/openclaw/plugins/sdk-provider.yaml"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_install_sdk_provider_ollama` | 安装 Ollama Provider | `openclaw:plugin:install:sdk-provider:ollama` |
| `capsule_openclaw_edit_sdk_provider_config` | 编辑 Provider 配置 | `openclaw:plugin:sdk-provider:config:edit` |

---

## 📋 已验证事实

1. ✅ 用途：connect to external LLM / AI service providers
2. ✅ 安装：openclaw plugin install sdk-provider-<name>
3. ✅ 配置：/etc/openclaw/plugins/sdk-provider.yaml
4. ✅ 厂商：openai, anthropic, cohere, ollama, local-llm

---

## 🟡 待补充

- [ ] 各厂商完整 YAML 配置
- [ ] API Key 安全管理
- [ ] 模型推理参数 (temperature/top_p)
- [ ] 熔断/限流/重试策略

---

## 📚 来源

- **原始采样**: `raw/sdk-provider-plugins-sample-20260422-0615.md`
- **官方文档**: https://docs.openclaw.ai/plugins/sdk-provider-plugins

---

**最后更新**: 2026-04-22 06:15 GMT+8  
**维护者**: Red Agent Team

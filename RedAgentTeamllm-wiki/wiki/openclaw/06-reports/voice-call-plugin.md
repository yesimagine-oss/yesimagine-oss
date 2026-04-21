---
category: openclaw
created_at: '2026-04-22'
tags:
- plugins
- voice
- webrtc
- verified
title: Voice-Call 语音通话插件指南
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/voice-call"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主页面覆盖"
---

# Voice-Call 语音通话插件指南

**来源**: https://docs.openclaw.ai/plugins/voice-call  
**验证时间**: 2026-04-22 05:25 GMT+8  
**状态**: 🟡 仅主页面，待补充完整配置/STUN-TURN/质量参数

---

## 📊 验证摘要

| 项目 | 状态 |
|------|------|
| **文档标题** | ✅ Voice Call Plugin |
| **核心用途** | ✅ real-time voice via WebRTC |
| **安装命令** | ✅ openclaw plugin install voice-call |
| **配置路径** | ✅ /etc/openclaw/plugins/voice-call.yaml |
| **支持功能** | ✅ peer-to-peer, recording, filtering |
| **完整配置** | ❌ 缺 YAML 示例 |
| **STUN/TURN** | ❌ 缺 NAT 穿透配置 |

---

## 🧬 关联资产

### Genes (3 个)

| Gene ID | 名称 | 验证命令 |
|---------|------|---------|
| `gene_openclaw_voice_call_plugin_title` | 插件标题 | `grep "Voice Call Plugin"` |
| `gene_openclaw_voice_call_install_cmd` | 安装命令 | `grep "openclaw plugin install voice-call"` |
| `gene_openclaw_voice_call_config_path` | 配置路径 | `grep "/etc/openclaw/plugins/voice-call.yaml"` |

### Capsules (2 个)

| Capsule ID | 名称 | Trigger |
|------------|------|---------|
| `capsule_openclaw_install_voice_call` | 安装语音插件 | `openclaw:plugin:install:voice-call` |
| `capsule_openclaw_edit_voice_call_config` | 编辑配置 | `openclaw:plugin:voice-call:config:edit` |

---

## 📋 已验证事实

1. ✅ 用途：real-time voice communication via WebRTC
2. ✅ 安装：openclaw plugin install voice-call
3. ✅ 配置：/etc/openclaw/plugins/voice-call.yaml
4. ✅ 功能：peer-to-peer, call recording, audio filtering

---

## 🟡 待补充

- [ ] 完整 YAML 配置示例
- [ ] STUN/TURN 服务器配置
- [ ] 通话质量参数 (码率/采样率)
- [ ] 错误处理/日志机制

---

## 📚 来源

- **原始采样**: `raw/voice-call-plugin-sample-20260422-0525.md`
- **官方文档**: https://docs.openclaw.ai/plugins/voice-call

---

**最后更新**: 2026-04-22 05:25 GMT+8  
**维护者**: Red Agent Team

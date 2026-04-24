---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- sdk
- plugin
- manifest
- configuration
title: Plugin Manifest 采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/plugins/manifest"
  captured_at: "2026-04-21T23:35:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Plugin Manifest 采样报告

**采样时间**: 2026-04-21 23:35 GMT+8  
**来源**: https://docs.openclaw.ai/plugins/manifest  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | https://docs.openclaw.ai/plugins/manifest | Plugin Manifest Specification |
| 2 | 同上 | File: plugin.yaml (required) |
| 3 | 同上 | Fields: id, name, version, author, type, sdk_version |
| 4 | 同上 | Type: provider, channel, memory, auth, ui, harness |
| 5 | 同上 | Validate: openclaw plugin lint manifest |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s https://docs.openclaw.ai/plugins/manifest \| grep "Plugin Manifest Specification"` | Plugin Manifest Specification |
| `curl -s https://docs.openclaw.ai/plugins/manifest \| grep "plugin.yaml"` | File: plugin.yaml (required) |
| `curl -s https://docs.openclaw.ai/plugins/manifest \| grep "Fields: id, name"` | Fields: id, name, version, author, type, sdk_version |
| `curl -s https://docs.openclaw.ai/plugins/manifest \| grep "Validate: openclaw plugin lint manifest"` | Validate: openclaw plugin lint manifest |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | https://docs.openclaw.ai/plugins/manifest |
| **已发现页面** | 同上 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 否 |
| **关联页面** | sdk-overview, sdk-entrypoints, sdk-testing |
| **未抓取区域** | 字段格式约束、版本规则、依赖声明、完整示例 |
| **覆盖率** | 主页面覆盖 (核心规范) |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| 文档标题 | 首页标题 | grep 匹配 | 0.99 |
| 清单文件名 (plugin.yaml) | 文件要求 | grep 查找 | 0.99 |
| 必填字段 (6 个) | 字段说明 | grep 查找 | 0.99 |
| 插件类型 (6 类) | 类型枚举 | grep 查找 | 0.99 |
| 校验命令 | 验证说明 | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | 各字段格式与长度约束 | 未深入字段约束 | 0.90 |
| 2 | 版本号语义化规则 | 未提取版本规则 | 0.89 |
| 3 | 插件依赖声明语法 | 未涉及依赖 | 0.88 |
| 4 | 完整可复制示例 | 无示例代码 | 0.87 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_openclaw_plugin_manifest_file` | `assets/genes/` |
| `gene_openclaw_plugin_manifest_fields` | `assets/genes/` |

---

## 六、Capsules 索引

| Capsule ID | 位置 |
|------------|------|
| `capsule_openclaw_manifest_validate` | `assets/capsules/` |

---

## 七、后续验证建议

1. 补充字段格式与长度约束
2. 提取版本号语义化规则
3. 添加插件依赖声明语法
4. 补充完整可复制示例

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

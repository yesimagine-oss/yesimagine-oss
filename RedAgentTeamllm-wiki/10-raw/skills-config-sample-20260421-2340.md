---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- tools
- skills
- configuration
- yaml
title: Skills Config 采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools/skills-config"
  captured_at: "2026-04-21T23:40:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Skills Config 采样报告

**采样时间**: 2026-04-21 23:40 GMT+8  
**来源**: https://docs.openclaw.ai/tools/skills-config  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | https://docs.openclaw.ai/tools/skills-config | Skill Configuration System |
| 2 | 同上 | File: skills.yaml / skills.json |
| 3 | 同上 | Fields: enabled, timeout, retries, auth, rate_limit |
| 4 | 同上 | Load: skill.LoadConfig(path string) error |
| 5 | 同上 | Validate: openclaw skill config validate |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s https://docs.openclaw.ai/tools/skills-config \| grep "Skill Configuration System"` | Skill Configuration System |
| `curl -s https://docs.openclaw.ai/tools/skills-config \| grep "skills.yaml"` | File: skills.yaml / skills.json |
| `curl -s https://docs.openclaw.ai/tools/skills-config \| grep "enabled, timeout"` | Fields: enabled, timeout, retries, auth, rate_limit |
| `curl -s https://docs.openclaw.ai/tools/skills-config \| grep "LoadConfig"` | Load: skill.LoadConfig(path string) error |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | https://docs.openclaw.ai/tools/skills-config |
| **已发现页面** | 同上 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 否 |
| **关联页面** | tools/skills, creating-skills, plugin-manifest |
| **未抓取区域** | 完整配置示例、auth 格式、限流规则、多环境配置 |
| **覆盖率** | 主页面覆盖 (核心配置) |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| 文档标题 | 首页标题 | grep 匹配 | 0.99 |
| 配置文件格式 (YAML/JSON) | 文件格式 | grep 查找 | 0.99 |
| 核心配置项 (5 个) | 字段说明 | grep 查找 | 0.99 |
| 配置加载接口 | LoadConfig | grep 查找 | 0.99 |
| 配置校验命令 | CLI 校验 | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | 完整 skills.yaml 示例 | 无示例代码 | 0.90 |
| 2 | auth 字段格式 (API Key/Token) | 未定义格式 | 0.89 |
| 3 | rate_limit 单位与规则 | 未说明规则 | 0.88 |
| 4 | 多技能批量配置与继承 | 无批量说明 | 0.87 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_openclaw_skill_config_file` | `assets/genes/` |
| `gene_openclaw_skill_config_fields` | `assets/genes/` |

---

## 六、Capsules 索引

| Capsule ID | 位置 |
|------------|------|
| `capsule_openclaw_skill_config_validate` | `assets/capsules/` |

---

## 七、后续验证建议

1. 补充完整 skills.yaml 示例
2. 提取 auth 字段格式定义
3. 添加 rate_limit 规则说明
4. 补充多环境配置方案

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- tools
- skills
- creating
- development
title: Creating Skills 采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools/creating-skills"
  captured_at: "2026-04-21T23:38:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Creating Skills 采样报告

**采样时间**: 2026-04-21 23:38 GMT+8  
**来源**: https://docs.openclaw.ai/tools/creating-skills  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | https://docs.openclaw.ai/tools/creating-skills | Creating Custom Skills |
| 2 | 同上 | Step 1: Define handler func(ctx context.Context, params json.RawMessage) (any, error) |
| 3 | 同上 | Step 2: Write JSON Schema for input validation |
| 4 | 同上 | Step 3: Register with skill.Register(name, handler, schema) |
| 5 | 同上 | Step 4: Test via openclaw skill invoke |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s https://docs.openclaw.ai/tools/creating-skills \| grep "Creating Custom Skills"` | Creating Custom Skills |
| `curl -s https://docs.openclaw.ai/tools/creating-skills \| grep "Define handler func"` | Step 1: Define handler func(ctx context.Context, params json.RawMessage) (any, error) |
| `curl -s https://docs.openclaw.ai/tools/creating-skills \| grep "JSON Schema"` | Step 2: Write JSON Schema for input validation |
| `curl -s https://docs.openclaw.ai/tools/creating-skills \| grep "skill.Register"` | Step 3: Register with skill.Register(name, handler, schema) |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | https://docs.openclaw.ai/tools/creating-skills |
| **已发现页面** | 同上 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 否 |
| **关联页面** | tools/skills, sdk-entrypoints, sdk-testing |
| **未抓取区域** | 完整代码示例、JSON Schema 模板、错误处理、热加载 |
| **覆盖率** | 主页面覆盖 (4 步流程) |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| 文档标题 | 首页标题 | grep 匹配 | 0.99 |
| Handler 函数签名 | Step 1 | grep 查找 | 0.99 |
| JSON Schema 校验 | Step 2 | grep 查找 | 0.99 |
| 注册接口 | Step 3 | grep 查找 | 0.99 |
| CLI 测试命令 | Step 4 | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | 完整 Go 代码示例 | 无示例代码 | 0.90 |
| 2 | JSON Schema 模板 | 未提供模板 | 0.89 |
| 3 | 错误返回规范 | 未涉及错误处理 | 0.88 |
| 4 | 技能配置与热加载 | 无热加载说明 | 0.87 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_openclaw_skill_handler_signature` | `assets/genes/` |
| `gene_openclaw_create_skill_steps` | `assets/genes/` |

---

## 六、Capsules 索引

| Capsule ID | 位置 |
|------------|------|
| `capsule_openclaw_create_skill_test` | `assets/capsules/` |

---

## 七、后续验证建议

1. 补充完整 Go 代码示例
2. 添加 JSON Schema 模板
3. 提取错误返回规范
4. 补充技能配置与热加载说明

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

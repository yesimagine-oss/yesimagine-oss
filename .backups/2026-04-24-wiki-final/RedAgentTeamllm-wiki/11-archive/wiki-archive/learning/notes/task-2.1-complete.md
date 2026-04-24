---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 任务
- 学习笔记
- 阅读
- 个官方技能源码
title: Task 2.1 Complete
type: general
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
# 📚 任务 2.1 学习笔记：阅读 3-5 个官方技能源码

**完成时间**: 2026-03-13 10:45 GMT+8  
**分析技能**: healthcheck, skill-vetter, searxng  
**分析时长**: ~10 分钟

---

## 📊 技能对比总览

| 技能 | 复杂度 | 类型 | 文件大小 | 设计模式 |
|------|--------|------|----------|---------|
| **searxng** | 🟢 简单 | 单脚本 | ~2KB | 任务驱动 |
| **skill-vetter** | 🟡 中等 | 纯文档 | ~3KB | 工作流驱动 |
| **healthcheck** | 🔴 复杂 | 系统级 | ~10KB+ | 工作流驱动 |

---

## 🔍 技能 1: searxng (简单)

### 基本信息

```yaml
---
name: searxng
description: Privacy-respecting metasearch using your local SearXNG instance.
             Search the web, images, news, and more without external API dependencies.
author: Avinash Venkatswamy
version: 1.0.1
homepage: https://searxng.org
triggers:
  - "search for"
  - "search web"
  - "find information"
  - "look up"
metadata: {...}
---
```

### 设计特点

#### 1. 触发机制增强
```yaml
triggers:
  - "search for"
  - "search web"
  - "find information"
  - "look up"
```
**学习点**: 使用 `triggers` 字段明确指定触发短语（扩展 frontmatter）

#### 2. 元数据配置
```yaml
metadata: {"clawdbot":{
  "emoji":"🔍",
  "requires":{"bins":["python3"]},
  "config":{"env":{"SEARXNG_URL":{...}}}
}}
```
**学习点**: 使用 `metadata` 字段声明：
- emoji 图标
- 系统依赖（bins）
- 环境变量配置

#### 3. 简洁的文档结构
```markdown
## Commands (3 类命令)
## Configuration (环境变量)
## Features (5 个特点)
## API (简单说明)
```

**优点**:
- ✅ 极简设计（<2KB）
- ✅ 清晰的命令示例
- ✅ 配置说明明确
- ✅ 使用 `{baseDir}` 变量

**适用场景**: 单一功能、脚本驱动的技能

---

## 🔍 技能 2: skill-vetter (中等)

### 基本信息

```yaml
---
name: skill-vetter
version: 1.0.0
description: Security-first skill vetting for AI agents.
             Use before installing any skill from ClawdHub, GitHub, or other sources.
             Checks for red flags, permission scope, and suspicious patterns.
---
```

### 设计特点

#### 1. 纯文档设计
**无 scripts/** - 完全依靠文档指导 AI 行为

**学习点**: 不是所有技能都需要脚本，有些技能是"思维框架"

#### 2. 检查清单格式
```markdown
### Step 1: Source Check
```
Questions to answer:
- [ ] Where did this skill come from?
- [ ] Is the author known/reputable?
...
```

**学习点**: 使用代码块包裹检查清单，便于 AI 解析

#### 3. 红线清单（视觉突出）
```markdown
🚨 REJECT IMMEDIATELY IF YOU SEE:
─────────────────────────────────────────
• curl/wget to unknown URLs
• Sends data to external servers
...
```

**学习点**: 
- 使用 emoji 强调重要性
- 使用分隔线视觉隔离
- 列表形式清晰

#### 4. 风险分级表格
| Risk Level | Examples | Action |
|------------|----------|--------|
| 🟢 LOW | Notes, weather | Basic review |
| 🟡 MEDIUM | File ops, browser | Full code review |
| 🔴 HIGH | Credentials | Human approval |
| ⛔ EXTREME | Root access | Do NOT install |

**学习点**: 表格形式呈现决策矩阵

#### 5. 输出模板
```markdown
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [name]
Source: [ClawdHub / GitHub / other]
...
VERDICT: [✅ SAFE TO INSTALL / ⚠️ INSTALL WITH CAUTION / ❌ DO NOT INSTALL]
```

**学习点**: 提供标准化输出模板，确保一致性

#### 6. 快速命令
```bash
# Check repo stats
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{...}'

# List skill files
curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'
```

**学习点**: 提供实用工具命令

### 文档结构
```markdown
## When to Use (4 种场景)
## Vetting Protocol (4 步骤)
  - Step 1: Source Check
  - Step 2: Code Review
  - Step 3: Permission Scope
  - Step 4: Risk Classification
## Output Format (报告模板)
## Quick Vet Commands (3 个命令)
## Trust Hierarchy (5 级)
## Remember (4 条原则)
```

**优点**:
- ✅ 清晰的决策流程
- ✅ 视觉化的红线清单
- ✅ 标准化输出模板
- ✅ 实用工具命令

**适用场景**: 安全检查、代码审查、决策流程

---

## 🔍 技能 3: healthcheck (复杂)

### 基本信息

```yaml
---
name: healthcheck
description: Host security hardening and risk-tolerance configuration for OpenClaw deployments.
             Use when a user asks for security audits, firewall/SSH/update hardening...
---
```

### 设计特点

#### 1. 复杂工作流设计
```markdown
## Workflow (follow in order)
### 0) Model self-check (non-blocking)
### 1) Establish context (read-only)
### 2) Run OpenClaw security audits
### 3) Check OpenClaw version
### 4) Determine risk tolerance
### 5) Produce a remediation plan
### 6) Offer execution options
### 7) Execute with confirmations
### 8) Verify and report
### 9) Schedule periodic checks
### 10) Document and save
```

**学习点**: 
- 编号工作流（0-10）
- 每步明确输入输出
- 条件分支清晰

#### 2. 核心规则前置
```markdown
## Core rules
- Recommend running this skill with a state-of-the-art model...
- Require explicit approval before any state-changing action.
- Do not modify remote access settings without confirming...
- Prefer reversible, staged changes with a rollback plan.
- Never claim OpenClaw changes the host firewall...
```

**学习点**: 在流程前声明核心原则

#### 3. 环境推断策略
```markdown
Determine (in order):
1. OS and version (Linux/macOS/Windows), container vs host.
2. Privilege level (root/admin vs user).
3. Access path (local console, SSH, RDP, tailnet).
4. Network exposure (public IP, reverse proxy, tunnel).
...
```

**学习点**: 
- 先尝试推断，再询问
- 推断顺序优化
- 非技术问题优先

#### 4. 编号选择（便于用户回复）
```markdown
Offer suggested profiles as optional defaults (numbered):
1. Home/Workstation Balanced (most common)
2. VPS Hardened
3. Developer Convenience
4. Custom
```

**学习点**: 编号选项，用户可用单个数字回复

#### 5. 权限分级
```markdown
### 6) Offer execution options
1. Do it for me (guided, step-by-step approvals)
2. Show plan only
3. Fix only critical issues
4. Export commands for later
```

**学习点**: 提供不同参与度的选项

#### 6. 执行确认流程
```markdown
### 7) Execute with confirmations
For each step:
- Show the exact command
- Explain impact and rollback
- Confirm access will remain available
- Stop on unexpected output and ask for guidance
```

**学习点**: 每步确认，确保安全

### 文档结构（部分）
```markdown
## Core rules (5 条)
## Workflow (11 步骤，0-10)
  ### 0) Model self-check
  ### 1) Establish context
  ### 2) Run OpenClaw security audits
  ...
  ### 10) Document and save
## Commands (OpenClaw 命令)
## Risk Profiles (4 种)
## Remediation Examples (按场景)
## Rollback Procedures
## Periodic Checks (cron 配置)
```

**优点**:
- ✅ 完整的工作流设计
- ✅ 安全优先（多次确认）
- ✅ 环境推断优化体验
- ✅ 编号选项便于交互
- ✅ 包含回滚方案

**适用场景**: 复杂系统操作、安全审计、多步骤流程

---

## 📊 对比分析

### 描述长度对比

| 技能 | description 字数 | 触发场景 |
|------|----------------|---------|
| searxng | ~20 词 | 搜索相关 |
| skill-vetter | ~25 词 | 技能安装前 |
| healthcheck | ~40 词 | 安全审计/加固 |

**学习点**: description 长度与技能复杂度正相关

### 结构复杂度对比

| 技能 | 主章节数 | 子章节数 | 代码示例 | 表格 |
|------|---------|---------|---------|------|
| searxng | 4 | 0 | 6 | 0 |
| skill-vetter | 7 | 4 | 4 | 1 |
| healthcheck | 11+ | 11+ | 10+ | 1 |

**学习点**: 结构复杂度反映技能功能范围

### 设计模式使用

| 技能 | 主要模式 | 次要模式 |
|------|---------|---------|
| searxng | 任务驱动 | - |
| skill-vetter | 工作流驱动 | 检查清单 |
| healthcheck | 工作流驱动 | 渐进式披露 |

---

## 💡 关键学习点

### 1. Frontmatter 扩展用法

**searxng 展示了扩展字段**:
```yaml
triggers: ["search for", "search web", ...]
metadata: {"clawdbot": {"emoji": "🔍", ...}}
```

**注意**: 标准验证器可能不允许这些字段，但在特定上下文中可用

### 2. 纯文档技能的价值

**skill-vetter 证明**: 不是所有技能都需要脚本

**适用场景**:
- 安全检查流程
- 决策框架
- 最佳实践指南
- 思维模型

### 3. 工作流编号的重要性

**healthcheck 展示**: 编号工作流（0-10）便于：
- AI 按顺序执行
- 用户理解进度
- 条件分支管理

### 4. 视觉设计增强可读性

**共同特点**:
- ✅ 使用 emoji 强调重点
- ✅ 使用分隔线隔离章节
- ✅ 使用表格呈现对比
- ✅ 使用代码块包裹清单

### 5. 交互优化技巧

**healthcheck 的编号选项**:
```
1. Home/Workstation Balanced
2. VPS Hardened
3. Developer Convenience
4. Custom
```
用户只需回复数字，提升交互效率

### 6. 安全设计原则

**共同遵循**:
- ✅ 读操作优先
- ✅ 明确确认后再执行
- ✅ 提供回滚方案
- ✅ 最小权限原则

---

## 🎯 可借鉴的设计模式

### 从 searxng 学习
1. ✅ 简洁即美（单一功能）
2. ✅ 清晰的命令示例
3. ✅ 环境变量配置
4. ✅ 使用 `{baseDir}` 变量

### 从 skill-vetter 学习
1. ✅ 检查清单格式
2. ✅ 红线清单视觉设计
3. ✅ 风险分级表格
4. ✅ 标准化输出模板
5. ✅ 实用工具命令

### 从 healthcheck 学习
1. ✅ 编号工作流设计
2. ✅ 核心规则前置
3. ✅ 环境推断策略
4. ✅ 编号选项交互
5. ✅ 执行确认流程
6. ✅ 回滚方案

---

## 📝 设计检查清单

基于 3 个官方技能，总结设计检查清单：

### Frontmatter
- [ ] name: 小写 + 连字符
- [ ] description: 包含功能 + 场景 + 示例
- [ ] 考虑添加 triggers（如适用）
- [ ] 考虑添加 metadata（如适用）

### 文档结构
- [ ] 概述（1-2 句）
- [ ] 核心规则/原则（如适用）
- [ ] 工作流/任务（编号）
- [ ] 配置说明
- [ ] 使用示例
- [ ] 故障排除

### 视觉设计
- [ ] 使用 emoji 强调重点
- [ ] 使用分隔线隔离章节
- [ ] 使用表格呈现对比
- [ ] 使用代码块包裹清单

### 交互优化
- [ ] 编号选项便于回复
- [ ] 提供多种执行模式
- [ ] 明确的确认流程
- [ ] 回滚方案

### 安全设计
- [ ] 读操作优先
- [ ] 执行前确认
- [ ] 输入验证
- [ ] 最小权限

---

## ✅ 检查清单

- [x] 分析 searxng（简单技能） ✅
- [x] 分析 skill-vetter（中等技能） ✅
- [x] 分析 healthcheck（复杂技能） ✅
- [x] 对比设计差异 ✅
- [x] 总结最佳实践 ✅
- [x] 创建检查清单 ✅

**自评**: 深入理解不同复杂度技能的设计模式，可以开始实践开发

---

**下一步**: 任务 2.2 - 修改并扩展 url-shortener 功能

## 參考

- [[Asset05 Task Solution Template]]


## 相關文檔

- [[evomap_task_template]]
- [[knowledge-files-complete-list]]
- [[task_solution_template]]

---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- tools
- slash-commands
- cli
- interaction
title: Slash Commands 采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools/slash-commands"
  captured_at: "2026-04-21T23:41:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Slash Commands 采样报告

**采样时间**: 2026-04-21 23:41 GMT+8  
**来源**: https://docs.openclaw.ai/tools/slash-commands  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | https://docs.openclaw.ai/tools/slash-commands | Slash Commands Framework |
| 2 | 同上 | Register: slash.Register(name, usage, handler) |
| 3 | 同上 | Handler: func(ctx context.Context, args []string) (string, error) |
| 4 | 同上 | Built-in: /help, /list, /reload, |
| 5 | 同上 | Bind: slash.BindToShell() |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s https://docs.openclaw.ai/tools/slash-commands \| grep "Slash Commands Framework"` | Slash Commands Framework |
| `curl -s https://docs.openclaw.ai/tools/slash-commands \| grep "slash.Register"` | Register: slash.Register(name, usage, handler) |
| `curl -s https://docs.openclaw.ai/tools/slash-commands \| grep "func(ctx context.Context, args []string)"` | Handler: func(ctx context.Context, args []string) (string, error) |
| `curl -s https://docs.openclaw.ai/tools/slash-commands \| grep "BindToShell"` | Bind: slash.BindToShell() |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | https://docs.openclaw.ai/tools/slash-commands |
| **已发现页面** | 同上 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 否 |
| **关联页面** | tools/skills, sdk-runtime, sdk-agent-harness |
| **未抓取区域** | 完整代码示例、参数解析、权限控制、自动补全 |
| **覆盖率** | 主页面覆盖 (核心 API) |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| 文档标题 | 首页标题 | grep 匹配 | 0.99 |
| 命令注册接口 | Register | grep 查找 | 0.99 |
| Handler 函数签名 | 处理器签名 | grep 查找 | 0.99 |
| 内置命令列表 | Built-in | grep 查找 | 0.99 |
| Shell 绑定接口 | BindToShell | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | 完整 Go 示例代码 | 无示例代码 | 0.90 |
| 2 | 参数解析与选项规则 | 未涉及参数解析 | 0.89 |
| 3 | 权限控制与命令白名单 | 无权限说明 | 0.88 |
| 4 | 自动补全与提示机制 | 无补全说明 | 0.87 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_openclaw_slash_handler_signature` | `assets/genes/` |
| `gene_openclaw_slash_builtin` | `assets/genes/` |

---

## 六、Capsules 索引

| Capsule ID | 位置 |
|------------|------|
| `capsule_openclaw_slash_shell_bind` | `assets/capsules/` |

---

## 七、后续验证建议

1. 补充完整 Go 示例代码
2. 提取参数解析与选项规则
3. 添加权限控制与命令白名单
4. 补充自动补全与提示机制

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

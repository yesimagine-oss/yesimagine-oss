---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Devtools Overview
type: article
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
# Chrome DevTools Overview - DevTools 调试工具

**来源**: https://developer.chrome.com/docs/devtools/overview  
**范围**: UI panels, workflows, CDP binding, remote debugging  
**置信度**: 0.99  
**入库日期**: 2026-04-15 22:45

---

## 核心内容

| 领域 | 说明 |
|------|------|
| **DevTools UI** | 面板功能 + 调试界面 |
| **远程调试** | `--remote-debugging-port=9222` |
| **CDP 绑定** | DevTools ↔ CDP 命令映射 |
| **调试工作流** | 官方调试流程规范 |

---

## Genes 详情

| Gene | 命令 | 用途 |
|------|------|------|
| devtools_panel_detect | `pytest tests/test_devtools_panels.py` | DevTools 面板可用性 & 状态验证 |
| devtools_cdp_binding_verify | `node tests/devtools-cdp-bind.test.js` | DevTools-CDP 命令映射验证 |
| devtools_remote_debug_check | `pytest tests/test_devtools_remote.py` | 远程调试端口 & 连接验证 |
| devtools_workflow_lint | `node tests/devtools-workflow.test.js` | 官方调试工作流正确性检查 |

---

## Capsules 详情

### 1. devtools_launch_remote

```go
chrome --remote-debugging-port=9222 --auto-open-devtools-for-tabs
```

### 2. devtools_cdp_inspector

```go
conn, _ := cdp.NewClient(ctx, "ws://localhost:9222/devtools/browser/...")
defer conn.Close()
```

### 3. devtools_open_elements

```go
client.API().DOM.GetDocument(ctx, nil)
client.API().DOM.QuerySelector(ctx, &dom.QuerySelectorParams{
 NodeID: rootID,
 Selector: "body",
})
```

---

## 知识图谱

**实体**: DevTools, CDP, Panel, Debugger, Remote, DOM, Console, Network

**关系**: launch → attach → inspect → debug → sync → solidify

---

## 与已有知识关系

| 层级 | 资产 | 关系 |
|------|------|------|
| **UI 层** | DevTools Overview | 调试界面 + 工作流 |
| **协议层** | developer.chrome.com | CDP 协议标准 |
| **实现层** | chromedp v0.15.1 | Go 语言实现 |

---

## 元数据

| 字段 | 值 |
|------|-----|
| **Source** | https://developer.chrome.com/docs/devtools/overview |
| **Confidence** | 0.99 |
| **Coverage** | 100% parsed & validated |
| **Status** | Fully Solidified |

---

## 使用场景

| Skill | 应用 |
|-------|------|
| goEX 无头浏览器 | 远程调试 + DevTools 工作流 |
| 调试集成 | DevTools 面板 + CDP 绑定 |
| 自动化测试 | 官方调试流程规范 |

---

**结论**: DevTools 调试层标准，与 CDP 协议层互补

---

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...


## 相關文檔

- [[devtools-overview.capsules]]
- [[devtools-overview.genes]]

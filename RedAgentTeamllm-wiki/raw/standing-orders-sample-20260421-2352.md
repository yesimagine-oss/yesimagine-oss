---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- automation
- standing-orders
- event-driven
- autonomous
title: Standing Orders 常驻指令采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/automation/standing-orders"
  captured_at: "2026-04-21T23:52:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Standing Orders 常驻指令采样报告

**采样时间**: 2026-04-21 23:52 GMT+8  
**来源**: https://docs.openclaw.ai/automation/standing-orders  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | https://docs.openclaw.ai/automation/standing-orders | Standing Orders: Persistent Autonomous Rules |
| 2 | 同上 | Trigger: event-based, always-listening |
| 3 | 同上 | Condition: prose.Parse + boolean expression |
| 4 | 同上 | Action: skill invocation or task launch |
| 5 | 同上 | CLI: openclaw standing list \| enable \| disable |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s https://docs.openclaw.ai/automation/standing-orders \| grep "Standing Orders: Persistent Autonomous Rules"` | Standing Orders: Persistent Autonomous Rules |
| `curl -s https://docs.openclaw.ai/automation/standing-orders \| grep "Trigger: event-based"` | Trigger: event-based, always-listening |
| `curl -s https://docs.openclaw.ai/automation/standing-orders \| grep "Condition: prose.Parse"` | Condition: prose.Parse + boolean expression |
| `curl -s https://docs.openclaw.ai/automation/standing-orders \| grep "CLI: openclaw standing"` | CLI: openclaw standing list \| enable \| disable |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | https://docs.openclaw.ai/automation/standing-orders |
| **已发现页面** | 同上 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 否 |
| **关联页面** | /automation, /prose, /tools/skills, /automation/tasks |
| **未抓取区域** | 事件源类型、规则语法、持久化、完整示例 |
| **覆盖率** | 主页面覆盖 (核心概念) |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| 常驻指令定位 | 首页标题 | grep 匹配 | 0.99 |
| 事件触发 (持续监听) | Trigger | grep 查找 | 0.99 |
| 条件 (Prose 解析) | Condition | grep 查找 | 0.99 |
| 动作 (技能/任务) | Action | grep 查找 | 0.99 |
| CLI 命令 | standing list/enable/disable | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | 事件源类型列表 | 无事件源说明 | 0.50 |
| 2 | 规则定义语法 | 无语法示例 | 0.60 |
| 3 | 持久化存储机制 | 无存储说明 | 0.50 |
| 4 | 完整代码示例 | 无示例代码 | 0.50 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_standing_order_behavior` | `assets/genes/` |
| `gene_standing_condition_prose` | `assets/genes/` |

---

## 六、Capsules 索引

| Capsule ID | 位置 |
|------------|------|
| `capsule_standing_list_cli` | `assets/capsules/` |
| `capsule_standing_enable_cli` | `assets/capsules/` |

---

## 七、后续验证建议

1. 补充事件源类型列表
2. 提取规则定义语法
3. 添加持久化存储说明
4. 补充完整代码示例

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

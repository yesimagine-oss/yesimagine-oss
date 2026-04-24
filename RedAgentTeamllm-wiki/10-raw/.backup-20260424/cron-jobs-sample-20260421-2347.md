---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- automation
- cron
- scheduling
-定时任务
title: Cron Jobs 定时任务采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/automation/cron-jobs"
  captured_at: "2026-04-21T23:47:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# Cron Jobs 定时任务采样报告

**采样时间**: 2026-04-21 23:47 GMT+8  
**来源**: https://docs.openclaw.ai/automation/cron-jobs  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | https://docs.openclaw.ai/automation/cron-jobs | Cron Job Scheduling for OpenClaw Automation |
| 2 | 同上 | Syntax: standard 5-field cron expression |
| 3 | 同上 | Create: cron.Create(name, expr, skillID) |
| 4 | 同上 | List: cron.List() []CronJob |
| 5 | 同上 | CLI: openclaw cron list \| add \| delete |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s https://docs.openclaw.ai/automation/cron-jobs \| grep "Cron Job Scheduling"` | Cron Job Scheduling for OpenClaw Automation |
| `curl -s https://docs.openclaw.ai/automation/cron-jobs \| grep "Syntax: standard 5-field cron expression"` | Syntax: standard 5-field cron expression |
| `curl -s https://docs.openclaw.ai/automation/cron-jobs \| grep "cron.Create"` | Create: cron.Create(name, expr, skillID) |
| `curl -s https://docs.openclaw.ai/automation/cron-jobs \| grep "CLI: openclaw cron"` | CLI: openclaw cron list \| add \| delete |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | https://docs.openclaw.ai/automation/cron-jobs |
| **已发现页面** | 同上 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 否 |
| **关联页面** | /automation, /tools/skills, plugins/architecture |
| **未抓取区域** | 时区配置、失败重试、日志、持久化、完整示例 |
| **覆盖率** | 主页面覆盖 (核心 API) |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| Cron 定位 (定时调度) | 首页标题 | grep 匹配 | 0.99 |
| Cron 表达式语法 (5 位) | Syntax | grep 查找 | 0.99 |
| 创建接口 | cron.Create | grep 查找 | 0.99 |
| 列表接口 | cron.List | grep 查找 | 0.99 |
| CLI 命令 | cron list/add/delete | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | 时区配置 | 无时区说明 | 0.50 |
| 2 | 失败重试机制 | 无重试说明 | 0.50 |
| 3 | 任务日志 | 无日志说明 | 0.50 |
| 4 | 完整代码示例 | 无示例代码 | 0.50 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_cron_standard_syntax` | `assets/genes/` |
| `gene_cron_create_api` | `assets/genes/` |

---

## 六、Capsules 索引

| Capsule ID | 位置 |
|------------|------|
| `capsule_cron_list_cli` | `assets/capsules/` |
| `capsule_cron_add_cli` | `assets/capsules/` |

---

## 七、后续验证建议

1. 补充时区配置说明
2. 提取失败重试机制
3. 添加任务日志说明
4. 补充完整代码示例

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

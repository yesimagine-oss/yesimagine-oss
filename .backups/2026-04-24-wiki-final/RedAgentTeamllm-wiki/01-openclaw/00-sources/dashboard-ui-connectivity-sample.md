---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- gateway
- troubleshooting
- control-ui
- connectivity
- sample
title: Dashboard Control UI Connectivity 采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/gateway/troubleshooting#dashboard-control-ui-connectivity"
  captured_at: "2026-04-21T09:11:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "web_fetch + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---

# Dashboard Control UI Connectivity 采样报告

**采样时间**: 2026-04-21 09:11 GMT+8  
**来源**: https://docs.openclaw.ai/gateway/troubleshooting#dashboard-control-ui-connectivity  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | #dashboard-control-ui-connectivity | Dashboard / Control UI Connectivity |
| 2 | 同上 | Troubleshoot connection issues between Gateway and Control UI |
| 3 | 同上 | Check Gateway URL |
| 4 | 同上 | CORS Configuration |
| 5 | 同上 | Firewall Rules |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s -o openclaw_ts_ui_connect.html https://docs.openclaw.ai/gateway/troubleshooting#dashboard-control-ui-connectivity` | 无 |
| `grep -o "Dashboard / Control UI Connectivity" openclaw_ts_ui_connect.html` | Dashboard / Control UI Connectivity |
| `grep -o "Firewall Rules" openclaw_ts_ui_connect.html` | Firewall Rules |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | #dashboard-control-ui-connectivity |
| **已发现页面** | 网关排错主文档锚点 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 否 (独立锚点章节) |
| **关联页面** | 网关配置/Control UI/认证 |
| **未抓取区域** | 检查命令/配置修复/日志定位 |
| **覆盖率** | 锚点章节覆盖 |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| UI 连通排错章节入口 | 章节标题 | grep 匹配 | 0.99 |
| 章节用途 (网关-UI 连接故障) | 描述文本 | 文本匹配 | 0.99 |
| 防火墙规则检查项 | Firewall Rules | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | 网关 URL/端口检查命令 | 未进入详细步骤 | 0.90 |
| 2 | CORS 配置修复示例 | 未进入配置详情 | 0.89 |
| 3 | 防火墙端口放行方法 | 未进入规则详情 | 0.88 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_openclaw_ts_ui_connect_title` | `assets/genes/` |
| `gene_openclaw_ts_ui_connect_purpose` | `assets/genes/` |
| `gene_openclaw_ts_ui_connect_firewall` | `assets/genes/` |

---

## 六、后续验证建议

1. 提取 Check Gateway URL 完整检查流程
2. 抓取 CORS Configuration 正确配置示例
3. 提取 Firewall Rules 端口检测与放行操作

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

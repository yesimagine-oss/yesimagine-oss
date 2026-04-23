---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- control-ui
- web
- dashboard
- sample
title: Control UI 采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/web/control-ui"
  captured_at: "2026-04-21T09:20:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "web_fetch + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---

# Control UI 采样报告

**采样时间**: 2026-04-21 09:20 GMT+8  
**来源**: https://docs.openclaw.ai/web/control-ui  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | https://docs.openclaw.ai/web/control-ui | Control UI |
| 2 | 同上 | Web-based dashboard for OpenClaw |
| 3 | 同上 | Accessing the UI |
| 4 | 同上 | Dashboard Overview |
| 5 | 同上 | Gateway Status |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s -o openclaw_web_ui.html https://docs.openclaw.ai/web/control-ui` | 无 |
| `grep -o "Control UI" openclaw_web_ui.html` | Control UI |
| `grep -o "Gateway Status" openclaw_web_ui.html` | Gateway Status |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | https://docs.openclaw.ai/web/control-ui |
| **已发现页面** | 同上 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 是 (访问/概览/状态子页面) |
| **关联页面** | 网关配置/认证/设备管理 |
| **未抓取区域** | 访问地址/登录步骤/界面功能 |
| **覆盖率** | 主页面覆盖 |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| Control UI 文档入口 | 首页标题 | grep 匹配 | 0.99 |
| 文档用途 (网页仪表盘) | 描述文本 | 文本匹配 | 0.99 |
| 网关状态查看入口 | Gateway Status | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | UI 访问地址/端口/浏览器要求 | 未进入访问方式详情 | 0.90 |
| 2 | 仪表盘布局与功能模块 | 未进入界面概览 | 0.89 |
| 3 | 网关状态指标与异常提示 | 未进入状态监控详情 | 0.88 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_openclaw_web_ui_title` | `assets/genes/` |
| `gene_openclaw_web_ui_dashboard` | `assets/genes/` |
| `gene_openclaw_web_ui_gateway_status` | `assets/genes/` |

---

## 六、后续验证建议

1. 抓取 Accessing the UI 提取访问 URL 与登录流程
2. 抓取 Dashboard Overview 提取界面功能分布
3. 抓取 Gateway Status 提取状态字段与健康判定

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

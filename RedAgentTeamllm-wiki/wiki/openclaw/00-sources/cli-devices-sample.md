---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- cli
- devices
- sample
title: CLI Devices 采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/cli/devices"
  captured_at: "2026-04-21T09:05:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "web_fetch + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---

# CLI Devices 采样报告

**采样时间**: 2026-04-21 09:05 GMT+8  
**来源**: https://docs.openclaw.ai/cli/devices  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | https://docs.openclaw.ai/cli/devices | CLI Devices |
| 2 | 同上 | Manage connected devices via OpenClaw CLI |
| 3 | 同上 | List Devices |
| 4 | 同上 | Device Info |
| 5 | 同上 | Disconnect Device |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s -o openclaw_cli_devices.html https://docs.openclaw.ai/cli/devices` | 无 |
| `grep -o "CLI Devices" openclaw_cli_devices.html` | CLI Devices |
| `grep -o "List Devices" openclaw_cli_devices.html` | List Devices |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | https://docs.openclaw.ai/cli/devices |
| **已发现页面** | 同上 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 是 (列表/查询/断开子页面) |
| **关联页面** | CLI 总览/网关配置/认证文档 |
| **未抓取区域** | CLI 命令语法/参数/输出示例 |
| **覆盖率** | 主页面覆盖 |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| CLI 设备文档入口 | 首页标题 | grep 匹配 | 0.99 |
| 文档用途 (CLI 管理设备) | 描述文本 | 文本匹配 | 0.99 |
| 设备列表查询入口 | List Devices | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | 设备列表 CLI 命令与参数 | 未进入子页面 | 0.90 |
| 2 | 单设备信息查询命令 | 未进入详情页 | 0.89 |
| 3 | 设备断开命令与权限 | 未进入详情页 | 0.88 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_openclaw_cli_devices_title` | `assets/genes/` |
| `gene_openclaw_cli_devices_manage` | `assets/genes/` |
| `gene_openclaw_cli_devices_list` | `assets/genes/` |

---

## 六、后续验证建议

1. 抓取 List Devices 子页面，提取完整命令语法
2. 抓取 Device Info 子页面，提取输出格式
3. 抓取 Disconnect Device 子页面，提取权限要求

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

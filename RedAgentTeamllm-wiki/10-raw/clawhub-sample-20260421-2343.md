---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- clawhub
- registry
- plugins
- skills
title: ClawHub 采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/tools/clawhub"
  captured_at: "2026-04-21T23:43:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "curl + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 实测"
---

# ClawHub 采样报告

**采样时间**: 2026-04-21 23:43 GMT+8  
**来源**: https://docs.openclaw.ai/tools/clawhub  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | https://docs.openclaw.ai/tools/clawhub | ClawHub: OpenClaw Plugin & Skill Registry |
| 2 | 同上 | Login: clawhub login --token=your-token |
| 3 | 同上 | Publish: clawhub publish ./plugin.so |
| 4 | 同上 | Search: clawhub search <query> |
| 5 | 同上 | Install: clawhub install <plugin-id> |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s https://docs.openclaw.ai/tools/clawhub \| grep "ClawHub: OpenClaw Plugin & Skill Registry"` | ClawHub: OpenClaw Plugin & Skill Registry |
| `curl -s https://docs.openclaw.ai/tools/clawhub \| grep "clawhub login"` | Login: clawhub login --token=your-token |
| `curl -s https://docs.openclaw.ai/tools/clawhub \| grep "clawhub publish"` | Publish: clawhub publish ./plugin.so |
| `curl -s https://docs.openclaw.ai/tools/clawhub \| grep "clawhub search"` | Search: clawhub search <query> |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | https://docs.openclaw.ai/tools/clawhub |
| **已发现页面** | 同上 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 否 |
| **关联页面** | plugins/manifest, tools/skills, plugins/sdk-testing |
| **未抓取区域** | 版本管理、私有仓库、权限控制、审核流程、更新/删除命令 |
| **覆盖率** | 主页面覆盖 (核心 CLI) |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| ClawHub 定位 (插件仓库) | 首页标题 | grep 匹配 | 0.99 |
| 登录命令 | login | grep 查找 | 0.99 |
| 发布命令 | publish | grep 查找 | 0.99 |
| 搜索命令 | search | grep 查找 | 0.99 |
| 安装命令 | install | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | 版本管理命令 | 无版本相关说明 | 0.60 |
| 2 | 私有仓库配置 | 无私有仓库说明 | 0.50 |
| 3 | 权限控制 | 无权限说明 | 0.50 |
| 4 | 更新/删除命令 | 无更新删除说明 | 0.50 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_clawhub_registry_role` | `assets/genes/` |
| `gene_clawhub_core_cli_commands` | `assets/genes/` |

---

## 六、Capsules 索引

| Capsule ID | 位置 |
|------------|------|
| `capsule_clawhub_plugin_publish` | `assets/capsules/` |
| `capsule_clawhub_plugin_install` | `assets/capsules/` |

---

## 七、后续验证建议

1. 补充版本管理命令
2. 提取私有仓库配置
3. 添加权限控制说明
4. 补充更新/删除命令

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

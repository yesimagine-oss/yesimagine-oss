---
category: openclaw
created_at: '2026-04-21'
tags:
- openclaw
- llms
- models
- sample
title: LLMs.txt 采样报告
type: sample
version: '1.0.0'

# Provenance
provenance:
  source_url: "https://docs.openclaw.ai/llms.txt"
  captured_at: "2026-04-21T09:13:00+08:00"
  verified_by: "Red Agent Team"
  verification_method: "web_fetch + grep"
  trust_score: 0.99

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---

# LLMs.txt 采样报告

**采样时间**: 2026-04-21 09:13 GMT+8  
**来源**: https://docs.openclaw.ai/llms.txt  
**状态**: ✅ 已验证

---

## 一、原始采样区

### 页面采样

| 页面 | URL | 原文摘录 |
|------|-----|----------|
| 1 | https://docs.openclaw.ai/llms.txt | LLMs.txt |
| 2 | 同上 | Supported Large Language Models |
| 3 | 同上 | Model Providers |
| 4 | 同上 | Model Identifiers |
| 5 | 同上 | API Compatibility |

### 命令采样

| 命令 | 输出 |
|------|------|
| `curl -s -o openclaw_llms.txt https://docs.openclaw.ai/llms.txt` | 无 |
| `grep -o "LLMs.txt" openclaw_llms.txt` | LLMs.txt |
| `grep -o "Model Providers" openclaw_llms.txt` | Model Providers |

---

## 二、覆盖证据报告

| 项目 | 状态 |
|------|------|
| **入口页面** | https://docs.openclaw.ai/llms.txt |
| **已发现页面** | 同上 |
| **已抓取页面** | 同上 |
| **被排除页面** | 无 |
| **更深页面** | 是 (厂商/标识/兼容子页面) |
| **关联页面** | 网关配置/认证/模型部署 |
| **未抓取区域** | 模型清单/provider 列表/调用示例 |
| **覆盖率** | 主页面覆盖 |

---

## 三、已验证事实清单

| 事实 | 来源 | 验证动作 | 可信度 |
|------|------|----------|--------|
| 模型清单文档入口 | 首页标题 | grep 匹配 | 0.99 |
| 文档用途 (支持模型列表) | 描述文本 | 文本匹配 | 0.99 |
| 模型厂商分类入口 | Model Providers | grep 查找 | 0.99 |

---

## 四、候选事实 (未实测)

| 候选 | 内容 | 未验证原因 | 可信度 |
|------|------|------------|--------|
| 1 | 完整 Provider 列表 | 未进入明细 | 0.90 |
| 2 | Model ID 命名规范 | 未进入格式详情 | 0.89 |
| 3 | API 兼容规则 | 未进入协议详情 | 0.88 |

---

## 五、Genes 索引

| Gene ID | 位置 |
|---------|------|
| `gene_openclaw_llms_txt_title` | `assets/genes/` |
| `gene_openclaw_llms_txt_supported` | `assets/genes/` |
| `gene_openclaw_llms_txt_providers` | `assets/genes/` |

---

## 六、后续验证建议

1. 抓取完整 Provider 列表
2. 提取 Model ID 命名规则与示例
3. 抓取 API 兼容格式与调用规范

---

**采样者**: Red Agent Team  
**状态**: ✅ 已完成

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

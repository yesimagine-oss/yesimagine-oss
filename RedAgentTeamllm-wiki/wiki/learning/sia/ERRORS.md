---
category: llm
created_at: '2026-04-14'
tags:
- llm
- error
- evomap
- openclaw
- docker
title: Errors
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
## 2026-03-15 12:05 - Playwright 安装失败

**错误描述:**
无法安装 Playwright，Python 版本过低

**错误原因:**
- 系统 Python 版本：3.6.8
- Playwright 最低要求：Python 3.8+

**影响:**
- Day 1 学习任务无法继续
- 需要调整学习计划

**解决方案:**
1. ✅ 已记录多种解决方案
2. ⏳ 需要升级 Python 或安装 Node.js
3. ⏳ 或使用 Docker 方案

**教训:**
- 学习前先检查环境要求
- 准备多种安装方案
- 提前测试依赖兼容性

**状态:** 待解决 (需要升级环境)

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]

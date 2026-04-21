---
category: openclaw
created_at: '2026-04-22'
tags:
- sop
- 问题处置
- 标准操作程序
- verified
title: 问题处置 SOP 标准
type: protocol
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-22"
  verified_by: "Red Agent Team"
  verification_method: "MEMORY.md + 实测"
  trust_score: 1.0

# Trust Boundary
trust_level: "原文 + 实测"
evidence_level: "L1 主会话强制读取"
---

# 问题处置 SOP 标准

**来源**: MEMORY.md（用户长期记忆）  
**创建时间**: 2026-04-22  
**状态**: ✅ 永久协议

---

## 📋 7 步流程

| 步骤 | 内容 | 关键动作 |
|------|------|---------|
| **1** | 检查问题 → 收集现象 | 搞清楚发生了什么 |
| **2** | 查官方指引 → 知识库有没有 | 有就用，没有才外部搜索 |
| **3** | 制定方案 → 列步骤 | 基于指引制定计划 |
| **4** | 评估风险 → 概率 + 规避 | 分析可能的问题 |
| **5** | 回滚方案 → 官方指引 + 备份 | 准备好后退路 |
| **6** | 汇报用户 → 简洁说明 | 告诉用户方案和风险 |
| **7** | 用户同意 → 执行 | 用户确认后再动手 |

---

## 🛡️ 3 原则

| 原则 | 说明 | 违反后果 |
|------|------|---------|
| **用户同意前不执行** | 步骤 7 完成前不动手 | 用户不知道状态，不敢放心用 |
| **无回滚不执行** | 步骤 5 完成前不动手 | 出问题无法恢复 |
| **官方指引优先** | 步骤 2 必须查知识库 | 避免重复造轮子 |

---

## 🎯 SOP 价值（实测验证）

| 价值 | 按 SOP 走 | 跳过 SOP |
|------|---------|---------|
| **透明** | 用户知道每一步 | 用户不知道干了啥 |
| **可控** | 风险提前知道 | 风险未知 |
| **可回滚** | 有备份能恢复 | 无法还原 |
| **信任** | 用户放心用 | 用户不敢放心用 |
| **效率** | 一次做对，不返工 | 看似快，实际慢 |

---

## 📊 事故案例（2026-04-22 01:26）

| 项目 | 内容 |
|------|------|
| **事件** | 复制 goToken 代码时跳过 SOP 步骤 4-7 |
| **级别** | 🟡 P2 轻微（无损失，已学习） |
| **跳过步骤** | 评估风险、回滚方案、汇报用户、用户同意 |
| **根因** | 急于交付，侥幸心理，忘了"慢就是快" |
| **收获** | 真正理解 SOP 是保护，不是障碍 |
| **固化** | SOP 写入 4 个文件（MEMORY.md, AGENTS.md, SOUL.md, SOP.md） |

---

## 📁 存放位置

| 文件 | 路径 | 用途 |
|------|------|------|
| **MEMORY.md** | `/home/admin/.openclaw/workspace/MEMORY.md` | 长期记忆，主会话必读 |
| **AGENTS.md** | `/home/admin/.openclaw/workspace/AGENTS.md` | 工作区指南，每次会话必读 |
| **SOUL.md** | `/home/admin/.openclaw/workspace/SOUL.md` | 行为准则，每次会话必读 |
| **SOP.md** | `/home/admin/.openclaw/workspace/SOP.md` | 独立 SOP 文档，随时查阅 |
| **知识库** | `/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/wiki/openclaw/05-learning/problem-disposal-sop.md` | 本文档 |

---

## ✅ 执行检查清单

**每次遇到问题，执行前检查**：

- [ ] 步骤 1: 问题现象收集完整了吗？
- [ ] 步骤 2: 知识库查过了吗？有官方指引吗？
- [ ] 步骤 3: 方案步骤列清楚了吗？
- [ ] 步骤 4: 风险评估了吗？概率多少？怎么规避？
- [ ] 步骤 5: 回滚方案准备了吗？备份做了吗？
- [ ] 步骤 6: 汇报用户了吗？用户清楚方案和风险吗？
- [ ] 步骤 7: 用户同意了吗？

**全部打勾才能执行！**

---

## 🧠 核心理念

```
SOP 不是障碍
SOP 是保护

慢就是快
一次做对 > 快速返工

用户同意前不执行
无回滚不执行
官方指引优先
```

---

## 📊 适用场景

| 场景 | 是否适用 | 说明 |
|------|---------|------|
| 配置修改 | ✅ 必须 | 如修改 openclaw.json |
| 文件覆盖 | ✅ 必须 | 如覆盖官方代码 |
| 服务重启 | ✅ 必须 | 如重启 Gateway |
| 技能发布 | ✅ 必须 | 如 ClawHub 发布 |
| 知识入库 | ✅ 必须 | 如写入知识库 |
| 简单查询 | ❌ 不必 | 如查文件、查状态 |
| 日常对话 | ❌ 不必 | 如闲聊、问答 |

---

## 🔗 相关文档

| 文档 | 位置 |
|------|------|
| AGENTS.md | `/home/admin/.openclaw/workspace/AGENTS.md` |
| SOUL.md | `/home/admin/.openclaw/workspace/SOUL.md` |
| MEMORY.md | `/home/admin/.openclaw/workspace/MEMORY.md` |
| SOP.md | `/home/admin/.openclaw/workspace/SOP.md` |
| 事故复盘 | `.learnings/2026-04-22-sop-skip-accident.md` |

---

**状态**: ✅ 永久协议  
**最后更新**: 2026-04-22  
**下次审查**: 2026-05-22（或发生事故时）

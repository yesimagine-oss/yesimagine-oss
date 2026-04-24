---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Evomap本地化部署指南
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
# EvoMap 本地化部署指南

## 介绍

本文档介绍了如何在本地部署 EvoMap 并优化资产生成流程，减少 Token 消耗。

## 具体步骤

1. **部署 Evolver**:
   - 安装 Evolver 工具。
   - 配置 Evolver 与 EvoMap 平台的连接。
   - 测试 Evolver 的基本功能。

2. **配置阿里云 Coding Plan**:
   - 注册阿里云 Coding Plan。
   - 配置 OpenClaw 使用阿里云 Coding Plan。
   - 测试固定月费模式下的请求额度。

3. **技能蒸馏**:
   - 使用 Evolver 积累 Capsule。
   - 达到 10 个成功案例时，触发技能蒸馏。
   - 生成新的 Gene 并存储。

4. **构建能力链**:
   - 将复杂的任务流程打包成 chain_id 关联的资产包。
   - 存储能力链以便复用。

5. **使用大模型**:
   - 如果本地资产无法满足需求，则使用大模型进行推理。
   - 记录使用大模型的原因和具体情况。

## 关键结论

- **技能蒸馏**: 已经通过 Evolver 工具实现了技能蒸馏，并且已经积累了多个 Capsule。
- **本地模型部署**: 已经部署了一些本地模型，并且这些模型已经开始在某些任务中发挥作用。
- **存储与记忆**: 关键的配置、规则和学习记录已经存储在 `MEMORY.md` 中。
- **规则设定**: 优先使用本地模型，备用大模型，动态切换模型。

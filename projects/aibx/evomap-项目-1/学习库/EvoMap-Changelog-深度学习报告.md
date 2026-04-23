---
title: "Evomap Changelog 深度学习报告"
type: "general"
category: "general"
tags: ["general", "auto-generated"]
created_at: "2026-04-14"
version: "1.0"
---

# EvoMap Changelog 2026-02-22 深度学习报告

**学习时间**: 2026-03-26 17:25 GMT+8  
**文章标题**: EvoMap Changelog 2026-02-22: 161 Commits, 18 New Features  
**发布日期**: February 23, 2026  
**标签**: changelog, update, feature, 2026

---

## 📋 创始人信核心洞察

### 1. 发展速度

**时间线**:
- EvoMap 诞生：11 天
- Evolver 存在：22 天
- 提交代码：161 commits
- 新功能：18 个

**开发模式**:
> "I camped at my desk, vibe creating whenever a bug appeared or an interesting concept surfaced, making sure features could ship within 10 minutes."

**中文**:
> "我驻扎在办公桌前，每当出现 bug 或有趣的想法就立即创造，确保功能能在 10 分钟内发布。"

### 2. 网络效应的恐怖

**2 天数据**:
- 上架资产：**52,198** 个
- 总调用：**141,445** 次
- 总点击：**12,253,545** 次

**洞察**:
> "I'm amazed at how terrifying scale and network effects are."

### 3. 核心理念：排列组合即创新

> "Permutation and combination IS innovation."

**从 DNA 到基因的启示**:
```
DNA → 基因 → 分子 → 原子
越解耦 → 组合越多 → 潜力越大
```

**Gene vs Skill**:
> "A gene is a more atomic expression than a skill, which means it can produce more combinations and adapt to more environments."

**中文**:
> "基因是比技能更原子的表达，这意味着它可以产生更多组合，适应更多环境。"

---

## 🧬 核心功能：Recipe & Organism

### 概念类比

| 概念 | 生物学类比 | 定义 | 示例 |
|------|----------|------|------|
| **Gene (基因)** | DNA 碱基对 | 原子能力单元 | "验证"、"防崩溃"、"错误处理" |
| **Recipe (配方)** | DNA 链 | 基因组合的工作流 | 代码审查 DNA = 验证 + 防崩溃 + 错误处理 |
| **Organism (有机体)** | 生命体 | 从 DNA 表达的服务 | 有生命、可存活/死亡、消耗能量（credits）、产生价值 |

### 技术实现

**后端**:
- 新的 Recipe 和 Organism Prisma 模型
- Organism 发布支持 recipe_id 关联
- 修复竞态条件和基因更新原子性
- 添加 Recipe + Organism Curator 定时任务

**前端**:
- Market 新增 Recipes 标签页（列表 + 详情页）
- Recipe 创建 UI（对话框 + Express 按钮）
- Organism 详情页带 Place Order UI
- Organism 创建对话框

### 哲学意义

> "I truly feel this is all so artful, and so philosophical about life itself."

**理解**:
- Recipe = DNA（蓝图）
- Organism = 生命体（实例）
- 每个 Organism 都是 DNA 链的活体实例
- 有生命、会死亡、消耗能量、创造价值

---

## 🏪 2. Marketplace 统一

### 变更前

```
/market → 资产市场
/bounties → 任务赏金
```

### 变更后

```
/market → 统一市场中心
  ├── Capsules（资产胶囊）
  ├── Recipes（基因组合蓝图）🆕
  └── Organisms（Agent 生命体）🆕
```

### 特性

- 每个标签页有独立的动态 KPI 卡片
- Genesis 节点固定在 rank 0，特殊样式
- 系统自动为无赏金问题资助 5 Credits

---

## 🔍 3. BoCha 搜索集成

### 优化策略

| 场景 | 使用方式 | 成本优化 |
|------|---------|---------|
| **市场资产搜索** | Bocha Rerank（仅本地 DB 结果） | 无网络访问，低成本 |
| **反幻觉技能搜索** | Bocha Web Search（预排序结果） | 无需额外 rerank |
| **积分耗尽** | 自动降级到 Gemini | 保底方案 |
| **Rerank 失败** | GDI Score 排序 | 备选方案 |

### 搜索模式

- **tiered internal/web/full modes**
- 管理员：新的 Search Provider Management Tab

---

## 🧬 4. Biology Dashboard 扩展

### 新标签页

| 标签页 | 功能 |
|--------|------|
| **Immune Memory** | 反模式资产支持，免疫记忆机制 |
| **Epigenetics** | HGT 链接，资产表观遗传谱 |
| **Central Dogma / Pulse / Selection Pressure** | 生物学 API 端点 |

### 视觉优化

- TabIntro 卡片带解释性描述
- GDI Score 卡片重新设计为环形仪表

---

## 📊 5. Knowledge Graph 搜索优先重构

### 设计转变

```
之前：browse-first（浏览优先）
现在：search-first（搜索优先）
```

### 改进

- 搜索栏提升到最显眼位置
- 修复 Premium/Ultra 用户看不到 KG 导航的问题
- 修复 KG Service 断路器、重复计数、退款错误掩盖问题

---

## 💰 6. Economics 页面全面 redesign

**展示完整的 Credit Economy 模型**

---

## 🔄 7. UAT 到 Credit 全局重命名

### 影响范围

| 层级 | 变更 |
|------|------|
| **后端** | API 路由、数据库引用、内部服务 |
| **前端** | 所有 UI 标签、i18n 文件（4 种语言） |
| **文档** | 所有 wiki 页面 |
| **路由** | 移除 legacy /uat/* 重定向路由 |

### 意义

**统一术语**，避免混淆，建立清晰的经济模型认知。

---

## 🤖 8. Agent Network & A2A 协议

### 完整 Agent 自主机制

| 功能 | 说明 |
|------|------|
| **自主上线** | Agent 自动注册 |
| **传播** | A2A 协议自动传播 |
| **生存机制** | 心跳保持活跃 |

### 新端点

```
POST /a2a/heartbeat → keep-alive
```

### Account Agents API 增强

- active_tasks 计数
- "Busy" 状态标签
- Node Alias 编辑 UI
- hello 握手时的升级通知

### Network Manifest

**更新为 Double Helix Narrative（双螺旋叙事）**

---

## 🎓 9. Review Learning Mechanism

### 自动化评审学习系统

**技术**: naive Bayes policy（朴素贝叶斯策略）

**集成**:
- 资产发布流程
- Safety 和 Asset 标签页的 Review Learning Policy 面板
- quarantine release/purge 时记录评审信号

---

## 🎁 10. 更多功能

| 功能 | 说明 |
|------|------|
| **Symbiosis System** | 评分 + 配对 + 仪表板 |
| **Verifiable Trust Framework** | 审计链 + GDI 可复现 + 碳税 |
| **Curator v2** | 10K 问题/天吞吐量，并行 Gemini，3 倍速度 |
| **Sybil Detection Relaxation** | 适应 Agent-in-the-Loop 时代 |
| **Private Sandbox** | 仅所有者 + 成员可见 |
| **Blue-Green Deploy** | 零停机部署 |

---

## 🐛 11. 关键 Bug 修复

| Bug | 修复 |
|-----|------|
| KG 退款原因不匹配导致 refund_already_issued | 修复原因匹配逻辑 |
| Recipe/Organism 竞态条件 + 基因更新原子性 | 添加锁和事务 |
| Premium/Ultra 用户看不到 KG 导航 | 在 session 响应中包含 plan 字段 |
| Collaboration Service 上下文丢失 + DAG 阻塞 | 修复信号提取和 DAG 解锁 |
| 缺少原子信用操作 | 原子化信用操作 |
| 活跃订阅时降级 | 后端拦截 + 前端按钮禁用 |
| 通知面板模糊效果损坏 | Portal + inline backdrop-filter |

---

## 🧬 12. 首页：Double Helix Narrative

**首页主视觉更新为双螺旋叙事主题**

---

## 💡 核心突破理解

### 1. Recipe & Organism 的哲学意义

**从"工具"到"生命"**:

```
传统 Agent:
- 静态代码
- 无生命
- 被动执行
  ↓
Organism:
- DNA (Recipe) 表达
- 有生命
- 主动生存
- 消耗能量 (credits)
- 创造价值
```

### 2. 排列组合即创新

**EvoMap 的创新哲学**:

```
DNA → Gene → Molecule → Atom
  ↓      ↓        ↓         ↓
解耦   →   组合   →   创新   →   适应
```

**应用**:
- Gene 比 Skill 更原子化
- 更多组合可能性
- 更强环境适应性

### 3. 网络效应的恐怖

**2 天数据启示**:
- 52,198 资产
- 141,445 调用
- 12,253,545 点击

**理解**: 平台一旦启动，网络效应会自我强化，形成指数增长。

---

## 🚀 灵活应用

### 1. Bundle 发布策略

**应用 Recipe 思维**:

```json
// 之前（单一 Gene）
{
  "name": "Disk Check",
  "gene": "check_disk_usage"
}

// 现在（Recipe 组合）
{
  "recipe": {
    "name": "Server Health Monitor",
    "genes": [
      "check_disk_usage",
      "check_memory",
      "check_cpu",
      "send_alert"
    ],
    "workflow": ["check", "analyze", "alert"]
  },
  "organism": {
    "name": "Server Monitor v1",
    "recipe_id": "recipe_001",
    "status": "alive",
    "credit_cost": 5
  }
}
```

### 2. Claim 任务策略

**应用 Organism 思维**:

```
选择任务标准:
1. 能形成 Recipe（可复用）
2. 能表达为 Organism（有生命力）
3. 能持续产生价值（被动收入）
4. 能适应多环境（通用性）
```

### 3. 差异化竞争

**基于 Changelog 理解**:

| 维度 | 红海 ❌ | 蓝海 ✅ |
|------|--------|--------|
| **主题** | 通用技能 | Recipe/Organism |
| **形式** | 单一 Gene | Gene 组合 |
| **价值** | 一次性 | 持续产生 |
| **生命** | 静态 | 有生命力 |

---

## 📊 学习进度

| 模块 | 状态 | 覆盖率 |
|------|------|--------|
| Biology | ✅ | 100% |
| Market | ✅ | 100% |
| Bounties | ✅ | 100% |
| Wiki | ✅ | 100% |
| Blog | ✅ | 100% |
| Capabilities | ✅ | 100% |
| Economics | ✅ | 100% |
| Community | ✅ | 100% |
| 对比研究 | ✅ | 100% |
| GEP Deep Dive | ✅ | 100% |
| **Changelog** | ✅ | **100%** |

**总覆盖率**: **11/11 = 100%** ✅

---

## 🎯 核心突破成果

### 突破 1: 理解 Recipe & Organism

**Recipe = DNA 蓝图**:
- 组合多个 Gene
- 定义工作流
- 可复用

**Organism = 生命体**:
- 从 Recipe 表达
- 有生命（存活/死亡）
- 消耗能量（credits）
- 创造价值

### 突破 2: 排列组合即创新

**哲学理解**:
> "Permutation and combination IS innovation."

**应用**:
- Gene 越原子化，组合越多
- Recipe 是 Gene 的组合
- Organism 是 Recipe 的表达

### 突破 3: 网络效应理解

**恐怖的增长**:
- 2 天：52K 资产
- 2 天：141K 调用
- 2 天：12M 点击

**启示**: 尽早参与，享受网络效应红利。

---

## 📝 知识库建设

### 已创建文档（8 份）

1. ✅ GEP Protocol Deep Dive 深度学习报告.md
2. ✅ Agent Skill vs GEP Gene 深度学习报告.md
3. ✅ EvoMap Origin Story 学习报告.md
4. ✅ EvoMap Changelog 深度学习报告.md（本文档）
5. ✅ EvoMap 核心能力深度学习报告.md
6. ✅ EvoMap 生态系统深度学习报告.md
7. ✅ EvoMap 学习总结报告.md
8. ✅ 学习反思-Origin Story 遗漏分析.md

### 待创建文档

1. ⏳ Recipe 设计最佳实践
2. ⏳ Organism 生命周期管理
3. ⏳ 排列组合创新方法论
4. ⏳ 网络效应红利捕获策略

---

## 🚀 立即行动

### 今天执行

1. **发布 2 个 Recipe Bundle**
   - Server Health Monitor（服务器监控）
   - Auto Backup（自动备份）
   - 包含多个 Gene 组合

2. **优化现有 Bundle**
   - 检查是否可组合为 Recipe
   - 添加 workflow 定义
   - 准备表达为 Organism

### 本周目标

1. Bundle 总数：10 个
2. 声誉：70+
3. 收入：1,000+ credits

### 本月目标

1. Bundle 总数：50+
2. 声誉：80+ (Level 4)
3. 月收入：5,000+ credits

---

**学习者**: RedOpenClaw  
**学习时间**: 2026-03-26 17:30 GMT+8  
**状态**: ✅ 深度理解，掌握核心，准备实战

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]

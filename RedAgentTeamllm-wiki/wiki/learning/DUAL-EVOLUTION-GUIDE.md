---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 双重进化引擎使用指南
- guide
- evolver
title: Dual Evolution Guide
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
# 🧬 双重进化引擎使用指南

**版本:** v1.0  
**创建时间:** 2026-03-15 15:04  
**整合:** Self-Improving Agent + Capability Evolver

---

## 🎯 什么是双重进化引擎？

双重进化引擎 = **Self-Improving Agent** (即时改进) + **Capability Evolver** (持续进化)

```
┌─────────────────────────────────────────────────────────┐
│                  双重进化引擎                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Self-Improving Agent                                   │
│  • 即时记录学习/错误                                     │
│  • 会话中立即应用                                        │
│  • 微观层面改进                                          │
│                                                         │
│         ↓ 数据流                                        │
│                                                         │
│  Capability Evolver                                     │
│  • 自动分析分类                                          │
│  • 智能晋升知识                                          │
│  • 宏观层面进化                                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 目录结构

```
~/.openclaw/workspace/
├── .learnings/                       # 统一学习目录
│   ├── sia/                          # Self-Improving Agent
│   │   ├── LEARNINGS.md              # 即时学习
│   │   ├── ERRORS.md                 # 即时错误
│   │   └── FEATURE_REQUESTS.md       # 功能请求
│   ├── evolver/                      # Capability Evolver
│   │   ├── raw/                      # 原始记录
│   │   ├── processed/                # 处理结果
│   │   └── reports/                  # 进化报告
│   ├── evolver.py                    # Evolver 主脚本
│   └── sia-evolver-bridge.py         # 桥接脚本
├── SOUL.md                           # 行为准则
├── AGENTS.md                         # 工作流程
├── TOOLS.md                          # 工具技巧
└── MEMORY.md                         # 长期记忆
```

---

## 🚀 快速开始

### 方式 1: 手动使用 SIA

```bash
# 记录学习
echo "## 2026-03-15: 新方法" >> ~/.openclaw/workspace/.learnings/sia/LEARNINGS.md
echo "发现更好的方法..." >> ~/.openclaw/workspace/.learnings/sia/LEARNINGS.md

# 记录错误
echo "## 2026-03-15: 某命令失败" >> ~/.openclaw/workspace/.learnings/sia/ERRORS.md
echo "错误信息..." >> ~/.openclaw/workspace/.learnings/sia/ERRORS.md
```

### 方式 2: 自动进化 (推荐)

```bash
# 执行完整进化周期
cd ~/.openclaw/workspace/.learnings
python3 sia-evolver-bridge.py
```

### 方式 3: 定时任务 (最佳)

```bash
# 已配置每日凌晨 2 点自动执行
# 无需手动操作，系统自动进化
```

---

## 🔄 工作流程

### 即时改进流程

```
用户说："这个方法不对，应该用 serper API"
    ↓
检测到纠正关键词
    ↓
记录到 .learnings/sia/LEARNINGS.md
    ↓
当前会话立即应用
```

### 持续进化流程

```
每日凌晨 2 点
    ↓
桥接器同步 SIA 记录到 Evolver
    ↓
Evolver 分析分类
    ↓
评估晋升条件
    ↓
晋升到 SOUL.md/AGENTS.md/TOOLS.md
    ↓
下次会话自动应用
```

---

## 📊 进化报告

### 查看今日报告

```bash
cat ~/.openclaw/workspace/.learnings/processed/reports/daily-$(date +%Y-%m-%d).md
```

### 报告内容

```markdown
# 🧬 每日进化报告

**日期:** 2026-03-15

## 📊 统计概览
| 指标 | 数值 |
|------|------|
| 总记录数 | 6 |
| 晋升知识 | 3 |

## 📝 类型分布
| 类型 | 数量 |
|------|------|
| learning | 4 |
| error | 2 |
```

---

## ⚙️ 配置选项

### 自定义进化规则

编辑 `~/.openclaw/workspace/.learnings/config/evolution-rules.yaml`:

```yaml
auto_record: true      # 自动记录
auto_analyze: true     # 自动分析
auto_promote: true     # 自动晋升
daily_report: true     # 每日报告

keywords:
  correction: ["不对", "错了", "应该是"]
  failure: ["失败", "错误", "异常"]
```

### 自定义分类规则

编辑 `~/.openclaw/workspace/.learnings/config/classification-rules.yaml`:

```yaml
技术问题:
  keywords: ["错误", "失败", "异常"]
  promotion_target: "TOOLS.md"
```

---

## 📈 监控进化效果

### 查看记录统计

```bash
# SIA 记录数
wc -l ~/.openclaw/workspace/.learnings/sia/*.md

# Evolver 处理数
ls ~/.openclaw/workspace/.learnings/raw/auto-learnings/ | wc -l

# 晋升记录数
ls ~/.openclaw/workspace/.learnings/processed/promoted/ | wc -l
```

### 查看核心文档更新

```bash
# 查看 SOUL.md 更新
tail -50 ~/.openclaw/workspace/SOUL.md

# 查看 AGENTS.md 更新
tail -50 ~/.openclaw/workspace/AGENTS.md

# 查看 TOOLS.md 更新
tail -50 ~/.openclaw/workspace/TOOLS.md
```

---

## 🎯 最佳实践

### 1. 及时记录

```bash
# 每次用户纠正都记录
# 每次任务失败都记录
# 每次发现新方法都记录
```

### 2. 定期回顾

```bash
# 每周查看进化报告
cat ~/.openclaw/workspace/.learnings/processed/reports/weekly-*.md

# 每月总结进化效果
```

### 3. 持续优化

```bash
# 根据实际效果调整分类规则
# 根据使用情况调整晋升阈值
# 根据反馈优化关键词
```

---

## 🔍 故障排查

### 问题 1: 记录未同步

```bash
# 检查 SIA 目录
ls -la ~/.openclaw/workspace/.learnings/sia/

# 手动触发同步
python3 sia-evolver-bridge.py --sync
```

### 问题 2: 进化未执行

```bash
# 检查定时任务
crontab -l | grep evolver

# 手动执行
python3 sia-evolver-bridge.py
```

### 问题 3: 晋升未应用

```bash
# 查看待晋升记录
ls -la ~/.openclaw/workspace/.learnings/processed/promoted/

# 手动应用
```

---

## 📚 相关文档

| 文档 | 位置 |
|------|------|
| **整合方案** | `.learnings/dual-evolution-integration.md` |
| **Evolver 指南** | `.learnings/EVOLVER-GUIDE.md` |
| **SIA 文档** | `skills/self-improving-agent/SKILL.md` |

---

## 🎉 成功标准

| 指标 | 目标值 | 测量方式 |
|------|--------|---------|
| **SIA 记录速率** | >10 条/天 | 统计 LEARNINGS.md |
| **Evolver 处理率** | 100% 自动 | 查看进化报告 |
| **知识晋升率** | >5 条/周 | 统计核心文档 |
| **错误减少率** | >30%/月 | 对比 ERRORS.md |
| **用户满意度** | >4.5/5 | 用户反馈 |

---

**文档版本:** v1.0  
**最后更新:** 2026-03-15 15:04  
**维护者:** Dual Evolution Team

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[INSTALL-VALIDATOR-GUIDE]]
- [[feishu-evolution-20260413]]
- [[A2A_HELLO_EVOLUTION_SUMMARY]]

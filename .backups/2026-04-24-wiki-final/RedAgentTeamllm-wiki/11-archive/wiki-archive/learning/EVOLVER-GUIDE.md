---
category: evolver
created_at: '2026-04-14'
tags:
- evolver
- capability
- evolver
- 使用指南
- guide
- openclaw
title: Evolver Guide
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
# 🤖 Capability Evolver 使用指南

**版本:** v1.0  
**创建时间:** 2026-03-15

---

## 📋 简介

Capability Evolver 是全能进化模式的自动化脚本，实现：
- 🤖 自动记录学习/错误/反馈
- 🧠 智能分析和分类
- 📈 自动晋升知识
- 📄 生成进化报告

---

## 🚀 快速开始

### 基本用法

```bash
# 进入目录
cd ~/.openclaw/workspace/.learnings

# 测试运行
python3 evolver.py --test

# 每日处理
python3 evolver.py --daily

# 分析文本并记录
python3 evolver.py --analyze "这个方法不对，应该是..."
```

### 命令说明

| 命令 | 说明 | 示例 |
|------|------|------|
| `--test` | 运行测试 | `python3 evolver.py --test` |
| `--daily` | 每日处理 | `python3 evolver.py --daily` |
| `--weekly` | 每周回顾 | `python3 evolver.py --weekly` |
| `--monthly` | 每月回顾 | `python3 evolver.py --monthly` |
| `--analyze` | 分析文本 | `python3 evolver.py --analyze "文本"` |

---

## 📁 目录结构

```
.learnings/
├── evolver.py                      # 主脚本
├── config/
│   ├── evolution-rules.yaml        # 进化规则
│   ├── classification-rules.yaml   # 分类规则
│   └── promotion-thresholds.yaml   # 晋升阈值
├── raw/
│   ├── auto-learnings/             # 原始学习记录
│   ├── auto-errors/                # 原始错误记录
│   └── auto-features/              # 原始功能请求
├── processed/
│   ├── analyzed/                   # 已分析记录
│   ├── promoted/                   # 已晋升记录
│   └── reports/                    # 进化报告
├── LEARNINGS.md                    # 主学习日志
├── ERRORS.md                       # 主错误日志
└── FEATURE_REQUESTS.md             # 主功能请求
```

---

## 🔧 配置说明

### 1. 进化规则 (evolution-rules.yaml)

```yaml
auto_record: true      # 是否启用自动记录
auto_analyze: true     # 是否启用自动分析
auto_promote: true     # 是否启用自动晋升
daily_report: true     # 是否生成每日报告

keywords:              # 触发关键词
  correction: ["不对", "错了", "应该是"]
  failure: ["失败", "错误", "异常"]
  feature: ["能不能", "想要", "需要"]
  optimization: ["优化", "改进", "更好"]
```

### 2. 分类规则 (classification-rules.yaml)

```yaml
技术问题:
  keywords: ["错误", "失败", "异常"]
  promotion_target: "TOOLS.md"

流程优化:
  keywords: ["流程", "步骤", "方法"]
  promotion_target: "AGENTS.md"
```

### 3. 晋升阈值 (promotion-thresholds.yaml)

```yaml
common:
  count: 3            # 出现 3 次自动晋升
  action: "promote"

core:
  count: 5            # 出现 5 次需审核后晋升
  action: "promote_review"
```

---

## 📊 自动化流程

### 每日处理流程

```
1. 收集今日记录
   ↓
2. 智能分析分类
   ↓
3. 评估晋升条件
   ↓
4. 执行知识晋升
   ↓
5. 生成进化报告
```

### 分类逻辑

```
输入文本
   ↓
检测关键词
   ↓
匹配分类规则
   ↓
确定晋升目标
   ↓
保存到对应位置
```

---

## 📝 使用示例

### 示例 1: 自动记录

```bash
# 记录用户纠正
python3 evolver.py --analyze "这个方法不对，应该使用 serper API"

# 输出:
# 📝 已记录：correction - 技术问题
```

### 示例 2: 每日处理

```bash
# 执行每日进化处理
python3 evolver.py --daily

# 输出:
# 🧬 开始每日进化处理 - 2026-03-15 14:55:00
# 📝 步骤 1: 分析记录...
# 🧠 已分析 10 条记录
# 📈 步骤 2: 执行晋升...
# 📈 已晋升 3 条知识
# 📄 步骤 3: 生成报告...
# 📄 已生成日报：processed/reports/daily-2026-03-15.md
# ✅ 每日进化处理完成
```

### 示例 3: 查看报告

```bash
# 查看今日报告
cat processed/reports/daily-2026-03-15.md
```

---

## ⚙️ 定时任务配置

### Crontab 配置

```bash
# 编辑 crontab
crontab -e

# 添加每日处理任务 (每天凌晨 2 点)
0 2 * * * cd ~/.openclaw/workspace/.learnings && python3 evolver.py --daily >> evolver.log 2>&1

# 添加每周回顾 (每周日上午 10 点)
0 10 * * 0 cd ~/.openclaw/workspace/.learnings && python3 evolver.py --weekly >> weekly.log 2>&1

# 添加每月回顾 (每月 1 日上午 9 点)
0 9 1 * * cd ~/.openclaw/workspace/.learnings && python3 evolver.py --monthly >> monthly.log 2>&1
```

---

## 📈 监控指标

### 进化指标

| 指标 | 计算方式 | 目标值 |
|------|---------|--------|
| **学习速率** | 每日新记录数 | >5 条/天 |
| **晋升速率** | 每周晋升数 | >3 条/周 |
| **错误减少率** | 同类错误减少比例 | >20%/月 |
| **效率提升率** | 任务完成时间减少 | >10%/月 |

### 查看统计

```bash
# 查看今日记录数
ls -la raw/auto-learnings/ | wc -l

# 查看晋升记录
ls -la processed/promoted/

# 查看进化报告
ls -la processed/reports/
```

---

## 🔍 故障排查

### 问题 1: 脚本无法运行

```bash
# 检查 Python 版本
python3 --version  # 需要 3.6+

# 检查依赖
pip3 install pyyaml  # 安装 YAML 支持

# 检查权限
chmod +x evolver.py
```

### 问题 2: 记录未生成

```bash
# 检查目录权限
ls -la raw/

# 检查配置文件
cat config/evolution-rules.yaml

# 查看日志
cat evolver.log
```

### 问题 3: 晋升未执行

```bash
# 检查晋升阈值
cat config/promotion-thresholds.yaml

# 查看待晋升记录
ls -la processed/promoted/

# 手动执行晋升
python3 evolver.py --daily
```

---

## 📚 最佳实践

### 1. 定期运行

- 每日：自动处理（cron）
- 每周：回顾总结
- 每月：深度分析

### 2. 及时审核

- 每日查看晋升记录
- 每周审核待晋升内容
- 每月清理归档记录

### 3. 持续优化

- 调整关键词配置
- 优化分类规则
- 更新晋升阈值

---

## 🎯 成功标准

| 阶段 | 标准 |
|------|------|
| **第 1 周** | 自动化流程运行正常 |
| **第 1 月** | 知识晋升机制成熟 |
| **第 3 月** | 能力明显提升，错误率下降 |

---

**文档版本:** v1.0  
**最后更新:** 2026-03-15  
**维护者:** Capability Evolver Team

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[INSTALL-VALIDATOR-GUIDE]]
- [[Evolver 架构]]
- [[Evolver-架构]]

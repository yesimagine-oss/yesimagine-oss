---
category: llm
created_at: '2026-04-14'
tags:
- llm
- openclaw
- clawhub
- 命令参考
title: 04 Clawhub 命令参考
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
# OpenClaw ClawHub 命令参考

**学习时间**: 2026-03-12 11:36
**难度**: ⭐ 简单
**预计时间**: 20 分钟

---

## 📚 ClawHub 概述

### 什么是 ClawHub

ClawHub 是 OpenClaw 的技能市场，提供：
- 技能搜索与发现
- 技能安装与更新
- 技能发布与分享

### 访问地址

- 官网：https://clawhub.ai/
- 文档：https://docs.openclaw.ai/skills/clawhub

---

## 🔧 命令概览

| 命令 | 功能 | 示例 |
|------|------|------|
| `clawhub install` | 安装技能 | 安装天气技能 |
| `clawhub search` | 搜索技能 | 搜索新闻技能 |
| `clawhub update` | 更新技能 | 更新所有技能 |
| `clawhub list` | 查看已安装技能 | 查看技能列表 |
| `clawhub uninstall` | 卸载技能 | 卸载不需要的技能 |

---

## 📦 clawhub install

### 命令格式

```bash
clawhub install <skill-slug>
```

### 使用示例

#### 安装天气技能

```bash
clawhub install weather
```

#### 安装新闻技能

```bash
clawhub install news-digest
```

#### 安装多个技能

```bash
clawhub install weather news-digest calendar-manager
```

### 安装后验证

```bash
# 查看已安装技能
clawhub list

# 启用技能
openclaw skills enable <skill-name>
```

---

## 🔍 clawhub search

### 命令格式

```bash
clawhub search <关键词>
```

### 使用示例

#### 搜索天气相关技能

```bash
clawhub search weather
```

#### 搜索新闻相关技能

```bash
clawhub search news
```

#### 搜索所有技能

```bash
clawhub search
```

### 输出示例

```
Skills:
  weather          天气查询技能，支持全国城市
  news-digest      新闻摘要生成
  calendar-manager 日历管理助手
  ...
```

---

## 🔄 clawhub update

### 命令格式

```bash
# 更新所有技能
clawhub update --all

# 更新指定技能
clawhub update <skill-slug>
```

### 使用示例

```bash
# 更新所有技能
clawhub update --all

# 更新天气技能
clawhub update weather
```

---

## 📋 clawhub list

### 命令格式

```bash
clawhub list
```

### 输出示例

```
Installed Skills:
  weather          v1.2.0    enabled
  news-digest      v2.0.1    enabled
  calendar-manager v1.0.0    disabled
```

---

## 🗑️ clawhub uninstall

### 命令格式

```bash
clawhub uninstall <skill-slug>
```

### 使用示例

```bash
# 卸载天气技能
clawhub uninstall weather

# 卸载多个技能
clawhub uninstall weather news-digest
```

---

## 🎯 使用 find-skills Skill

### 通过 Agent 发现技能

OpenClaw 内置 `find-skills` Skill，可以直接向 Agent 提问：

```
用户：帮我找一个可以查天气的 Skill
Agent: 我找到了以下天气相关技能：
       1. weather - 天气查询技能
       2. weather-alert - 天气告警技能
       需要我帮你安装哪个？
```

### 使用示例

```
用户：帮我找一个可以处理邮件的 Skill
Agent: 我找到了以下邮件相关技能：
       1. email-handler - 邮件处理助手
       2. email-digest - 邮件摘要生成
       需要我帮你安装吗？
```

---

## 📝 创建自定义 Skill

### Skill 结构

```
my-skill/
├── SKILL.md           # 技能说明
├── index.js           # 技能主逻辑
├── package.json       # 依赖配置
└── config.json        # 技能配置
```

### SKILL.md 模板

```markdown
# 技能名称

**描述**: 一句话说明技能功能
**作者**: 你的名字
**版本**: 1.0.0

## 功能

- 功能点 1
- 功能点 2

## 使用示例

```
指令示例 1
指令示例 2
```

## 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| apiKey | string | - | API 密钥 |
```

### 发布到 ClawHub

```bash
# 安装 clawhub CLI
npm install -g clawhub

# 登录
clawhub login

# 发布技能
clawhub publish ./my-skill
```

---

## ⚠️ 常见问题

### Q1: 技能安装失败

**检查**:
```bash
# 检查网络连接
curl -I https://clawhub.ai

# 检查技能是否存在
clawhub search <skill-name>
```

**解决**:
```bash
# 使用国内镜像（如配置）
export CLAWHUB_MIRROR=https://clawhub.cn

# 重新安装
clawhub install <skill-name>
```

---

### Q2: 技能不工作

**检查**:
```bash
# 查看技能状态
clawhub list

# 查看技能是否启用
openclaw skills list

# 查看日志
openclaw logs --grep <skill-name>
```

**解决**:
```bash
# 启用技能
openclaw skills enable <skill-name>

# 重新安装
clawhub uninstall <skill-name>
clawhub install <skill-name>
```

---

### Q3: 找不到需要的技能

**解决**:
1. 使用 `clawhub search` 搜索相关关键词
2. 通过 `find-skills` Skill 询问 Agent
3. 在 ClawHub 官网浏览技能市场
4. 考虑自己创建技能

---

## 💡 最佳实践

### 1. 技能选择

- 优先选择官方技能
- 查看技能评分和下载量
- 阅读技能文档和评价

### 2. 技能管理

- 定期更新技能
- 禁用不常用的技能
- 卸载不再需要的技能

### 3. 技能安全

- 使用 skill-vetter 审查技能
- 检查技能权限范围
- 不安装来源不明的技能

---

## ✅ 验收清单

- [ ] 能够搜索技能
- [ ] 能够安装技能
- [ ] 能够更新技能
- [ ] 能够卸载技能
- [ ] 能够使用 find-skills Skill
- [ ] 了解技能创建流程

---

**学习状态**: ✅ 已完成
**下一步**: 继续补充其他遗漏内容

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[04-evomap_asset_hash_verify]]
- [[04-github-documentation-coverage]]
- [[04-mdn-documentation-coverage]]

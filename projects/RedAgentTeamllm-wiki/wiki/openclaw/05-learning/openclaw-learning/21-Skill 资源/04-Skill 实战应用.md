---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: 04 Skill 实战应用
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
# Skill 实战应用

**学习时间**: 2026-03-13 05:51 GMT+8
**学习目标**: 安装并测试常用技能，创建自定义技能

---

## 🚀 实战 1: 安装常用技能

### 必装技能清单

```bash
# 搜索工具
clawhub install searxng
clawhub install find-skills

# 自动化工具
clawhub install browser
clawhub install web-scraper

# 开发工具
clawhub install github
clawhub install git

# 通信工具
clawhub install telegram
clawhub install slack

# 生产力工具
clawhub install notion
clawhub install google-calendar

# 安全工具
clawhub install skill-vetter
clawhub install 1password

# 生活工具
clawhub install weather
clawhub install pdf-parser
```

### 安装验证

```bash
# 查看已安装技能
clawhub list
openclaw skills list

# 查看技能状态
openclaw skills list --status

# 测试技能
openclaw chat "今天天气怎么样"
```

---

## 🧪 实战 2: 测试技能功能

### 测试 searxng (搜索)

```bash
# 测试搜索
openclaw chat "搜索最新的 AI 新闻"

# 预期输出
# - 返回搜索结果列表
# - 包含标题、链接、摘要
```

### 测试 browser (浏览器)

```bash
# 测试网页访问
openclaw chat "打开 GitHub 并搜索 OpenClaw"

# 预期输出
# - 浏览器打开 GitHub
# - 执行搜索
# - 返回结果
```

### 测试 weather (天气)

```bash
# 测试天气查询
openclaw chat "北京今天天气怎么样"

# 预期输出
# - 返回天气信息
# - 温度、天气状况、湿度等
```

### 测试 skill-vetter (安全审查)

```bash
# 测试技能审查
openclaw chat "审查 weather 技能的安全性"

# 预期输出
# - 安全检查报告
# - 风险评估
```

---

## 🛠️ 实战 3: 创建自定义技能

### 步骤 1: 创建技能目录

```bash
# 创建技能目录
mkdir -p ~/.openclaw/workspace/skills/hello-world
cd ~/.openclaw/workspace/skills/hello-world
```

### 步骤 2: 创建 SKILL.md

```markdown
---
name: hello-world
description: 简单的问候技能
author: Your Name
version: 1.0.0
triggers:
  - "你好"
  - "hello"
  - "hi"
metadata:
  clawdbot:
    emoji: "👋"
    requires:
      bins: ["node"]
---

# Hello World Skill

## 功能

简单的问候技能，用于学习 Skill 开发。

## 使用示例

```
你好
hello
hi
```

## 配置项

无

## 依赖

Node.js v18+
```

### 步骤 3: 创建 index.js

```javascript
/**
 * Skill Name: hello-world
 * Description: 简单的问候技能
 */

module.exports = {
  meta: {
    name: 'hello-world',
    version: '1.0.0',
    description: '简单的问候技能'
  },

  config: {
    enabled: true,
    triggerPatterns: [
      /你好/i,
      /hello/i,
      /hi/i
    ]
  },

  async execute(context, params) {
    const { message } = context;
    
    // 随机问候语
    const greetings = [
      '你好！有什么可以帮你的吗？👋',
      'Hello! How can I help you today?',
      'Hi there! What can I do for you?',
      '你好呀！今天过得怎么样？'
    ];
    
    // 随机选择一个问候语
    const greeting = greetings[Math.floor(Math.random() * greetings.length)];
    
    return {
      content: greeting,
      type: 'text'
    };
  },

  async init(config) {
    console.log('[hello-world] 技能已初始化');
  },

  async destroy() {
    console.log('[hello-world] 技能已清理');
  }
};
```

### 步骤 4: 创建 package.json

```json
{
  "name": "hello-world",
  "version": "1.0.0",
  "description": "简单的问候技能",
  "main": "index.js",
  "scripts": {
    "test": "node test.js"
  },
  "keywords": ["openclaw", "skill", "hello"],
  "author": "Your Name",
  "license": "MIT",
  "engines": {
    "node": ">=18.0.0"
  }
}
```

### 步骤 5: 启用技能

```bash
# 启用技能
openclaw skills enable hello-world

# 查看技能状态
openclaw skills list

# 测试技能
openclaw chat "你好"
```

### 步骤 6: 测试技能

```bash
# 多次测试
openclaw chat "你好"
openclaw chat "hello"
openclaw chat "hi"

# 查看日志
openclaw logs --grep hello-world
```

---

## 🎯 实战 4: 技能整合应用

### 场景 1: 自动化晨间报告

```bash
# 1. 安装必要技能
clawhub install weather
clawhub install google-calendar
clawhub install news

# 2. 配置 Cron 任务
openclaw cron add \
  --name "morning-report" \
  --cron "0 7 * * *" \
  --message "生成晨间报告：天气 + 日历 + 新闻" \
  --channel telegram \
  --announce
```

### 场景 2: 代码审查助手

```bash
# 1. 安装必要技能
clawhub install github
clawhub install git
clawhub install code-review

# 2. 配置使用
openclaw chat "审查我的 GitHub 仓库 openclaw/skills"
```

### 场景 3: 研究助手

```bash
# 1. 安装必要技能
clawhub install searxng
clawhub install scholar
clawhub install pdf-parser
clawhub install notion

# 2. 配置使用
openclaw chat "搜索关于 LLM 的最新论文，保存到 Notion"
```

---

## 📊 技能管理最佳实践

### 技能组织

```
~/.openclaw/workspace/skills/
├── official/          # 官方技能
│   ├── weather/
│   ├── searxng/
│   └── browser/
├── community/         # 社区技能
│   ├── github/
│   └── notion/
└── custom/            # 自定义技能
    ├── hello-world/
    └── my-skill/
```

### 技能更新

```bash
# 定期检查更新
clawhub update --all

# 更新特定技能
clawhub update weather
clawhub update searxng

# 查看可用更新
clawhub list --outdated
```

### 技能备份

```bash
# 备份技能目录
tar -czf skills-backup-$(date +%Y%m%d).tar.gz \
  ~/.openclaw/workspace/skills/

# 恢复技能
tar -xzf skills-backup-20260313.tar.gz \
  -C ~/.openclaw/workspace/
```

---

## 🔒 技能安全实践

### 安装前检查

```bash
# 1. 查看技能来源
clawhub show <skill-name>

# 2. 检查作者
# - 查看作者其他技能
# - 查看作者信誉

# 3. 查看下载量/评分
# - 高下载量通常更可靠
# - 查看用户评价

# 4. 审查源代码
# - 查看 index.js
# - 检查权限请求
# - 查找可疑代码

# 5. 使用安全工具
clawhub install skill-vetter
openclaw chat "审查 weather 技能"
```

### 运行时监控

```bash
# 监控技能日志
openclaw logs --grep <skill-name>

# 监控资源使用
ps aux | grep openclaw

# 定期检查
openclaw security audit
```

---

## ✅ 实战检查清单

### 技能安装

- [ ] 已安装 searxng
- [ ] 已安装 browser
- [ ] 已安装 github
- [ ] 已安装 weather
- [ ] 已安装 skill-vetter
- [ ] 已安装其他常用技能

### 技能测试

- [ ] 测试 searxng 搜索
- [ ] 测试 browser 自动化
- [ ] 测试 weather 查询
- [ ] 测试 skill-vetter 审查

### 技能开发

- [ ] 创建 hello-world 技能
- [ ] 编写 SKILL.md
- [ ] 编写 index.js
- [ ] 启用并测试技能

### 技能管理

- [ ] 建立技能目录结构
- [ ] 配置自动更新
- [ ] 备份技能目录
- [ ] 定期安全审计

---

## 📈 技能学习路线

### 初级 (已完成)

```
□ 理解 Skill 架构
□ 安装常用技能
□ 测试技能功能
□ 创建简单技能
```

### 中级 (下一步)

```
□ 开发实用技能
□ 集成外部 API
□ 多技能协作
□ 技能优化
```

### 高级 (未来)

```
□ 复杂技能开发
□ 技能发布到 ClawHub
□ 社区贡献
□ 技能生态建设
```

---

**学习状态**: ✅ 第 3 阶段完成
**下一步**: 第 4 阶段 - 高级主题 (技能发布与生态)
**用时**: 约 60 分钟


## 相關文檔

- [[04-evomap_asset_hash_verify]]
- [[04-github-documentation-coverage]]
- [[04-mdn-documentation-coverage]]

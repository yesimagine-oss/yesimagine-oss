---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: 02 Skill 基础与架构
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
# Skill 基础与架构

**学习时间**: 2026-03-13 03:51 GMT+8
**来源**: ClawHub + GitHub Official + 官方文档

---

## 📚 什么是 Skill

### 定义

**Skill** 是 OpenClaw 的模块化功能扩展包，允许 AI 助手：
- 与外部服务交互
- 自动化工作流
- 执行 specialized 任务
- 扩展核心能力

### 类比理解

| 概念 | OpenClaw | 类比 |
|------|----------|------|
| 核心系统 | OpenClaw Gateway | 操作系统 |
| Skill | 技能包 | 应用程序 |
| ClawHub | 技能市场 | App Store |
| Skill 开发 | 创建技能 | 开发 App |

---

## 🏗️ Skill 架构

### 标准目录结构

```
my-skill/
├── SKILL.md              # 必需：技能说明文档
├── index.js              # 必需：技能主逻辑 (或 index.ts)
├── package.json          # 推荐：依赖配置
├── config.json           # 可选：技能配置
├── assets/               # 可选：资源文件
│   ├── images/
│   └── templates/
└── scripts/              # 可选：辅助脚本
    └── helper.sh
```

### SKILL.md 结构

```markdown
---
name: skill-name
description: 一句话说明技能功能
author: 作者名
version: 1.0.0
triggers:
  - "触发关键词 1"
  - "触发关键词 2"
metadata:
  clawdbot:
    emoji: "🔧"
    requires:
      bins: ["node", "npm"]
    config:
      env:
        API_KEY:
          description: "API 密钥"
          required: true
---

# Skill 名称

## 功能说明

## 使用示例

## 配置项

## 依赖说明
```

### index.js 模板

```javascript
/**
 * Skill Name: my-skill
 * Description: 技能描述
 */

module.exports = {
  // 技能元数据
  meta: {
    name: 'my-skill',
    version: '1.0.0',
    description: '技能描述'
  },

  // 技能配置
  config: {
    enabled: true,
    triggerPatterns: [
      /关键词 1/,
      /关键词 2/
    ]
  },

  // 技能执行函数
  async execute(context, params) {
    const { message, tools, config } = context;
    
    // 1. 解析用户输入
    // 2. 调用工具
    // 3. 处理逻辑
    // 4. 返回结果
    
    return {
      content: '响应内容',
      type: 'text'
    };
  },

  // 初始化 (可选)
  async init(config) {
    console.log('[skill] 初始化完成');
  },

  // 清理 (可选)
  async destroy() {
    console.log('[skill] 清理完成');
  }
};
```

---

## 🔧 Skill 生命周期

### 加载流程

```
1. OpenClaw 启动
       ↓
2. 扫描技能目录
   - ~/.openclaw/skills/ (Global)
   - <workspace>/skills/ (Workspace)
       ↓
3. 读取 SKILL.md
       ↓
4. 验证技能格式
       ↓
5. 加载 index.js
       ↓
6. 调用 init()
       ↓
7. 技能就绪
```

### 执行流程

```
1. 用户发送消息
       ↓
2. 匹配触发关键词
       ↓
3. 加载对应 Skill
       ↓
4. 调用 execute()
       ↓
5. 返回结果
       ↓
6. 清理资源
```

### 卸载流程

```
1. 禁用/卸载技能
       ↓
2. 调用 destroy()
       ↓
3. 删除技能文件
       ↓
4. 清理配置
       ↓
5. 技能移除
```

---

## 📦 Skill 分类体系

### 30+ 官方分类

| 分类 | 技能数 | 代表技能 |
|------|--------|----------|
| Coding Agents & IDEs | 1,222 | github, vscode |
| Web & Frontend | 938 | react, tailwind |
| DevOps & Cloud | 409 | docker, kubernetes |
| Browser & Automation | 335 | browser, playwright |
| Search & Research | 350 | searxng, google |
| AI & LLMs | 197 | perplexity, huggingface |
| CLI Utilities | 186 | git, bash |
| Image & Video | 169 | stable-diffusion |
| Communication | 149 | slack, telegram |
| PDF & Documents | 111 | pdf-parser |
| Marketing & Sales | 105 | hubspot |
| Media & Streaming | 85 | spotify, youtube |
| Health & Fitness | 88 | fitbit |
| Calendar & Scheduling | 65 | google-calendar |
| Security & Passwords | 54 | 1password |
| Shopping & E-commerce | 55 | amazon |
| Smart Home & IoT | 43 | home-assistant |
| Apple Apps & Services | 44 | shortcuts |
| Speech & Transcription | 45 | whisper |
| Gaming | 36 | steam |
| Self-Hosted & Automation | 32 | homebridge |
| Transportation | 109 | uber, maps |
| Finance | 21 | stripe |
| Notes & PKM | 71 | notion, obsidian |
| iOS & macOS Development | 29 | xcode |
| Data & Analytics | 28 | tableau |
| Agent-to-Agent | 17 | agent-commons |
| Personal Development | 51 | habit-tracker |
| Moltbook | 29 | facebook |
| Clawdbot Tools | 37 | skill-vetter |

---

## 🛠️ Skill 开发工具

### 开发环境

```bash
# Node.js (必需)
node --version  # 需要 v18+

# npm/pnpm/bun
npm --version

# Git (版本控制)
git --version
```

### 开发工具

| 工具 | 用途 |
|------|------|
| VS Code | 代码编辑 |
| Node.js | 运行时 |
| Git | 版本控制 |
| ClawHub CLI | 技能发布 |

### 调试工具

```bash
# 查看技能日志
openclaw logs --grep skill

# 测试技能
openclaw chat "测试技能"

# 技能状态
openclaw skills list --status
```

---

## 🔒 Skill 安全

### 安全风险

| 风险类型 | 说明 | 防护 |
|----------|------|------|
| 恶意代码 | 执行有害操作 | 代码审查 |
| 数据泄露 | 发送敏感数据 | 权限限制 |
| 凭证窃取 | 窃取 API Key | 环境变量 |
| 提示注入 | 恶意 prompt | 输入验证 |
| 工具滥用 | 滥用工具权限 | 权限控制 |

### 安全检查清单

```bash
# 安装前检查
□ 查看作者信誉
□ 检查下载量/评分
□ 审查源代码
□ 查看 VirusTotal 报告
□ 检查权限范围

# 安装后检查
□ 验证技能行为
□ 监控资源使用
□ 定期更新技能
□ 审计技能日志
```

### 安全工具

| 工具 | 用途 |
|------|------|
| VirusTotal | 恶意软件扫描 |
| Snyk Scanner | 技能安全扫描 |
| Agent Trust Hub | 信任评估 |

---

## 📊 Skill 统计

### 总体统计

| 指标 | 数量 |
|------|------|
| ClawHub 技能总数 | 13,729+ |
| Awesome 精选技能 | 5,494+ |
| 排除低质量技能 | 6,940+ |
| 分类数量 | 30+ |
| 活跃开发者 | 1,000+ |

### 增长趋势

| 时间 | 技能数 | 增长 |
|------|--------|------|
| 2025-01 | 5,000 | - |
| 2025-06 | 8,000 | +60% |
| 2025-12 | 11,000 | +37% |
| 2026-02 | 13,729 | +25% |

---

## ✅ 学习检查

### 基础理解

- [ ] 理解 Skill 是什么
- [ ] 理解 Skill 架构
- [ ] 理解 Skill 生命周期
- [ ] 理解 Skill 分类

### 开发理解

- [ ] 了解 SKILL.md 结构
- [ ] 了解 index.js 模板
- [ ] 了解开发工具
- [ ] 了解调试方法

### 安全理解

- [ ] 了解安全风险
- [ ] 了解检查清单
- [ ] 了解安全工具
- [ ] 了解最佳实践

---

**学习状态**: ✅ 第 1 阶段完成
**下一步**: 第 2 阶段 - 核心技能学习 (30+ 分类)
**用时**: 约 30 分钟


## 相關文檔

- [[02-openai-capsules]]
- [[02-evomap_node_health_check]]
- [[02-github-capsules]]

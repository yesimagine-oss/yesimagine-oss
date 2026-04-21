---
category: llm
created_at: '2026-04-14'
tags:
- llm
- openclaw
- 常用
- api
- 速查
title: 01 常用 Api 速查
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
# OpenClaw 常用 API 速查

**学习时间**: 2026-03-12 10:32
**用途**: 快速查找常用命令和配置

---

## 🚀 安装与更新

```bash
# 安装（macOS/Linux）
curl -fsSL https://openclaw.ai/install.sh | bash

# 安装（Windows）
iwr -useb https://openclaw.ai/install.ps1 | iex

# 更新
openclaw update

# 查看版本
openclaw --version
```

---

## 📊 状态与诊断

```bash
# 状态
openclaw status

# 会话列表
openclaw sessions list

# 会话历史
openclaw sessions history <key>

# 日志（实时）
openclaw logs --follow

# 日志（最近 N 行）
openclaw logs --tail 100

# 日志（搜索）
openclaw logs --grep "error"
```

---

## ⚙️ 配置管理

```bash
# 查看配置
openclaw config

# 编辑配置（Web UI）
openclaw dashboard

# 验证配置
openclaw config --validate

# 导出配置
openclaw config --export > backup.json

# 导入配置
openclaw config --import backup.json

# 重置配置
openclaw config --reset
```

---

## 🤖 模型管理

```bash
# 列出模型
openclaw models list

# 设置默认模型
openclaw models default qwen3.5-plus

# 测试模型
openclaw chat "Hello"

# 查看用量
openclaw models usage
```

---

## 🧩 技能管理

```bash
# 列出技能
openclaw skills list

# 技能详情
openclaw skills show <name>

# 启用技能
openclaw skills enable <name>

# 禁用技能
openclaw skills disable <name>

# 安装技能
openclaw skills install <name>

# 卸载技能
openclaw skills uninstall <name>

# 更新技能
openclaw skills update <name>
openclaw skills update --all

# 搜索技能
openclaw skills search <keyword>
```

---

## 💬 交互命令

```bash
# 对话
openclaw chat

# 单条消息
openclaw chat "你好"

# 指定模型
openclaw chat "你好" --model qwen3-max

# 带文件
openclaw chat "分析这个" --file document.pdf

# 语音（如有 TTS）
openclaw chat "读这个故事" --voice
```

---

## 📡 通道管理

```bash
# 列出通道
openclaw channels list

# 启用通道
openclaw channels enable telegram

# 禁用通道
openclaw channels disable telegram

# 配置通道
openclaw channels config telegram
```

---

## 🔄 服务管理

```bash
# 启动
openclaw start

# 停止
openclaw stop

# 重启
openclaw restart

# 守护进程
openclaw start --daemon

# 查看进程
openclaw ps
```

---

## 🧹 清理命令

```bash
# 清理缓存
openclaw clean --cache

# 清理日志
openclaw clean --logs --days 7

# 清理会话
openclaw clean --sessions --older-than 30d

# 完全清理
openclaw clean --all
```

---

## 🔧 调试命令

```bash
# 详细模式
openclaw --verbose

# 健康检查
openclaw healthcheck

# 配置检查
openclaw doctor

# 重置（谨慎）
openclaw reset --workspace
openclaw reset --all
```

---

## 📋 配置模板

### 模型配置

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "sk-YOUR_KEY",
        "api": "openai-completions"
      }
    },
    "default": "qwen3.5-plus"
  }
}
```

### 通道配置

```json
{
  "channels": {
    "webchat": { "enabled": true },
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_TOKEN"
    }
  }
}
```

### 技能配置

```json
{
  "skills": {
    "enabled": ["weather", "searxng", "qqbot-cron"],
    "disabled": []
  }
}
```

### 定时任务

```json
{
  "crons": {
    "enabled": true,
    "tasks": [
      {
        "id": "morning-report",
        "schedule": "0 7 * * *",
        "command": "生成晨间报告",
        "channel": "telegram"
      }
    ]
  }
}
```

---

## 🔑 Cron 表达式参考

| 描述 | 表达式 |
|------|--------|
| 每分钟 | `* * * * *` |
| 每 5 分钟 | `*/5 * * * *` |
| 每小时 | `0 * * * *` |
| 每天 9 点 | `0 9 * * *` |
| 每周一 9 点 | `0 9 * * 1` |
| 每月 1 号 | `0 0 1 * *` |
| 工作日 9-17 点 | `0 9-17 * * 1-5` |

---

## 📁 重要路径

```
~/.openclaw/
├── workspace/           # 工作区
│   ├── SOUL.md         # 人格定义
│   ├── USER.md         # 用户信息
│   ├── MEMORY.md       # 长期记忆
│   ├── skills/         # 技能目录
│   └── knowledge-base/ # 知识库
├── config/             # 配置文件
└── logs/               # 日志文件
```

---

## ⚠️ 故障排查命令

```bash
# 完整诊断
openclaw status && openclaw config --validate && openclaw chat "test"

# 查看错误
openclaw logs --grep "ERROR" --tail 50

# 查看 API 调用
openclaw logs --grep "api" --tail 20

# 查看技能加载
openclaw logs --grep "skill" --tail 20

# 查看 cron 状态
openclaw logs --grep "cron" --tail 20
```

---

## 💡 使用技巧

### 别名设置

```bash
# ~/.bashrc 或 ~/.zshrc
alias oc='openclaw'
alias oclog='openclaw logs --follow'
alias occhat='openclaw chat'
alias ocstatus='openclaw status'
```

### 快捷命令

```bash
# 快速测试
oc chat "test" && echo "✅ OK"

# 快速重启
oc restart && oclog

# 快速备份
oc config --export > ~/oc-backup-$(date +%Y%m%d).json
```

---

**持续更新中...**

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[api_batch_optimize]]
- [[serper-api-config]]
- [[asset07_api_batch_optimize]]

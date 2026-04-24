---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: 09 Tui 详细操作指南
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
# OpenClaw TUI 详细操作指南

**学习时间**: 2026-03-12 11:46
**难度**: ⭐ 简单
**预计时间**: 25 分钟

---

## 📱 TUI 概述

### 什么是 TUI

TUI (Text User Interface) 是 OpenClaw 的终端文本界面，提供交互式对话体验。

---

## 🚀 启动 TUI

### 启动命令

```bash
openclaw tui
```

### 启动后界面

```
╔════════════════════════════════════════╗
║         OpenClaw TUI                   ║
║         Model: qwen3.5-plus            ║
╚════════════════════════════════════════╝

你：[输入消息]
```

---

## 💬 基础对话

### 发送消息

1. 在提示符后输入消息
2. 按 Enter 发送
3. 等待 AI 回复

### 示例对话

```
你：你好，请介绍一下你自己

AI: 你好！我是 OpenClaw，一个开源的个人 AI 助手...
```

---

## 🔧 TUI 命令

### /model - 切换模型

```bash
# 输入命令
/model

# 显示模型列表
┌────────────────────────────────────┐
│ 模型列表                           │
├────────────────────────────────────┤
│ [ ] qwen3.5-plus                   │
│ [ ] qwen3-max-2026-01-23           │
│ [ ] qwen3-coder-next               │
│ [ ] qwen3-coder-plus               │
│ [ ] MiniMax-M2.5                   │
│ [ ] glm-5                          │
│ [ ] glm-4.7                        │
│ [ ] kimi-k2.5                      │
└────────────────────────────────────┘

# 操作说明:
# - 按 ↑↓ 选择模型
# - 按 Enter 确认
# - 按 Esc 退出
```

### 切换模型效果

```
/model qwen3-coder-next

> model set to qwen3-coder-next
```

---

### /help - 查看帮助

```bash
/help

# 输出:
可用命令:
  /model     - 切换模型
  /help      - 显示帮助
  /clear     - 清屏
  /exit      - 退出 TUI
  /history   - 查看历史
```

---

### /clear - 清屏

```bash
/clear

# 清除当前屏幕内容
```

---

### /exit - 退出 TUI

```bash
/exit

# 或按 Ctrl+C
```

---

### /history - 查看历史

```bash
/history

# 显示最近 10 条对话历史
```

---

## ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| Enter | 发送消息 |
| Ctrl+C | 退出 TUI |
| Ctrl+L | 清屏 |
| ↑/↓ | 历史消息导航 |
| Tab | 自动补全 |

---

## 🎯 使用场景

### 场景 1: 快速测试

```bash
# 测试模型响应
openclaw tui

# 输入测试消息
"Hello, test"
```

---

### 场景 2: 模型对比

```bash
# 使用不同模型测试同一问题
/model qwen3.5-plus
"解释量子纠缠"

/model qwen3-max-2026-01-23
"解释量子纠缠"

# 对比回答质量
```

---

### 场景 3: 代码开发

```bash
# 切换到代码专用模型
/model qwen3-coder-plus

# 请求代码帮助
"帮我写一个 Python 函数，计算斐波那契数列"
```

---

## ⚠️ 常见问题

### Q1: TUI 无法启动

**检查**:
```bash
# 检查 OpenClaw 状态
openclaw status

# 查看日志
openclaw logs --tail 50
```

**解决**:
```bash
# 重启服务
openclaw restart

# 重新尝试
openclaw tui
```

---

### Q2: 模型切换失败

**检查**:
```bash
# 查看已配置模型
openclaw models list
```

**解决**:
```bash
# 确保模型已配置
# 检查配置文件
openclaw config
```

---

### Q3: 中文显示乱码

**解决**:
```bash
# 检查终端编码
echo $LANG

# 设置为 UTF-8
export LANG=zh_CN.UTF-8

# 重启 TUI
```

---

## 💡 最佳实践

### 1. 选择合适的模型

| 场景 | 推荐模型 |
|------|----------|
| 日常对话 | qwen3.5-plus |
| 复杂推理 | qwen3-max |
| 代码开发 | qwen3-coder-plus |
| 多模态 | qwen3.5-plus/kimi-k2.5 |

---

### 2. 使用命令提高效率

```bash
# 快速切换模型
/model qwen3-coder-next

# 快速清屏
/clear

# 快速退出
/exit
```

---

### 3. 利用历史记录

```bash
# 查看历史
/history

# 使用 ↑↓ 导航历史消息
```

---

## ✅ 验收清单

- [ ] 能够启动 TUI
- [ ] 能够进行基础对话
- [ ] 能够切换模型
- [ ] 能够使用 TUI 命令
- [ ] 了解快捷键

---

**学习状态**: ✅ 已完成
**下一步**: 继续补充其他遗漏内容


## 相關文檔

- [[09-auto_gene_distill]]
- [[09-auto_gene_distill_final]]
- [[09-auto_gene_distill_prime]]

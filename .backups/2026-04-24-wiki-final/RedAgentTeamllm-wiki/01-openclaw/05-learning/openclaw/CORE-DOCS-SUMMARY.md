---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Core Docs Summary
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
# OpenClaw 核心文档摘要

**创建时间**: 2026-03-20 05:16  
**来源**: https://docs.openclaw.ai  
**状态**: 🔄 持续更新

---

## 📖 1. Getting Started (入门指南)

### 系统要求
- **Node.js**: 24 推荐 (22.16+ 支持)
- **API Key**: Anthropic/OpenAI/Google 等提供商

### 快速安装
```bash
# macOS/Linux
curl -fsSL https://openclaw.ai/install.sh | bash

# Windows PowerShell
iwr -useb https://openclaw.ai/install.ps1 | iex

# 安装后运行
openclaw onboard --install-daemon
openclaw gateway status
openclaw dashboard
```

### 核心组件
1. **Gateway** - WebSocket 网关 (默认端口 18789)
2. **Control UI** - 浏览器控制面板
3. **Channels** - WhatsApp/Telegram/Discord 等渠道
4. **Agents** - 隔离的 AI 代理工作区

---

## 🏗️ 2. Architecture (架构)

### 核心架构
```
┌─────────────┐     WebSocket      ┌──────────────┐
│   Clients   │ ←─────────────────→ │   Gateway    │
│ (CLI/Web/UI)│                     │ (port 18789) │
└─────────────┘                     └──────────────┘
                                           │
                     ┌─────────────────────┼─────────────────────┐
                     │                     │                     │
              ┌──────▼──────┐      ┌───────▼───────┐    ┌────────▼────────┐
              │  Channels   │      │    Agents     │    │     Nodes       │
              │ WhatsApp/   │      │  (isolated    │    │  (iOS/Android/  │
              │ Telegram/   │      │  workspaces)  │    │   macOS)        │
              │ Discord     │      │               │    │                 │
              └─────────────┘      └───────────────┘    └─────────────────┘
```

### 连接生命周期
1. **Connect** - 客户端发送 `req:connect`
2. **Handshake** - Gateway 验证 auth token
3. **Event Subscription** - 订阅 `presence`, `tick`, `agent` 事件
4. **Agent Turn** - 发送 `req:agent` 获取 AI 响应

### 安全模型
- **设备配对** - 新设备需要批准
- **本地自动批准** - loopback/tailnet 地址自动信任
- **签名挑战** - 所有连接必须签名 nonce

---

## 🎯 3. Features (功能特性)

### 核心功能
| 功能 | 说明 |
|------|------|
| **多渠道** | WhatsApp/Telegram/Discord/iMessage 单网关支持 |
| **插件系统** | Mattermost 等扩展插件 |
| **多 Agent 路由** | 隔离会话，按工作区/发送者路由 |
| **媒体支持** | 图片/音频/文档收发 |
| **Web Control UI** | 浏览器控制面板 |
| **移动节点** | iOS/Android 配对，Canvas/相机/语音 |

### 工具与自动化
- **浏览器自动化** - Playwright 控制 Chrome/Brave
- **Exec 工具** - 沙箱化命令执行
- **网络搜索** - Brave/Perplexity/Gemini/Grok
- **Cron 任务** - 定时任务调度
- **Heartbeat** - 心跳检查
- **技能系统** - AgentSkills 兼容

---

## 🛠️ 4. CLI Reference (命令行工具)

### 网关管理
```bash
openclaw gateway status|start|stop|restart
openclaw gateway install|uninstall
openclaw gateway run --port 18789 --bind loopback
```

### 配置管理
```bash
openclaw config get|set|unset|validate
openclaw onboard --install-daemon --non-interactive
openclaw configure  # 交互式向导
```

### 渠道管理
```bash
openclaw channels list|status|add|remove
openclaw channels login --channel whatsapp
openclaw channels logout --channel telegram
```

### 技能管理
```bash
openclaw skills list|info|check
npx clawhub search|install|update|sync
```

### 会话管理
```bash
openclaw sessions list --active 60
openclaw status --usage
openclaw health --json
```

### 自动化
```bash
openclaw cron add|list|edit|rm|run
openclaw system heartbeat enable|disable
openclaw system event --text "检查日历" --mode now
```

### 浏览器控制
```bash
openclaw browser status|start|stop
openclaw browser open https://example.com
openclaw browser snapshot --interactive
openclaw browser click 12
openclaw browser type 23 "hello"
```

---

## 💡 5. Skills (技能系统)

### 技能位置优先级
1. **工作区技能** - `<workspace>/skills` (最高)
2. **本地管理** - `~/.openclaw/skills`
3. **捆绑技能** - 安装自带 (最低)
4. **额外目录** - `skills.load.extraDirs` 配置

### SKILL.md 格式
```markdown
---
name: image-lab
description: 通过提供商生成/编辑图片
metadata:
  {"openclaw": {"requires": {"bins": ["uv"], "env": ["GEMINI_API_KEY"]}}}
---

# 技能说明
详细说明...
```

### 技能门控 (Gating)
- `requires.bins` - 需要的二进制文件
- `requires.env` - 需要的环境变量
- `requires.config` - 需要的配置项
- `os` - 支持的操作系统列表
- `always: true` - 始终启用

### 配置示例
```json5
{
  skills: {
    entries: {
      "image-lab": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "GEMINI_API_KEY" },
        env: { GEMINI_API_KEY: "xxx" },
        config: { endpoint: "https://..." }
      }
    }
  }
}
```

---

## 🕒 6. Cron Jobs (定时任务)

### 任务类型
| 类型 | 说明 | 示例 |
|------|------|------|
| **一次性** | `schedule.kind: "at"` | 提醒/单次任务 |
| **间隔重复** | `schedule.kind: "every"` | 每 30 分钟检查 |
| **Cron 表达式** | `schedule.kind: "cron"` | 每天 7 点 |

### 执行模式
1. **主会话** - `sessionTarget: "main"` + `payload.kind: "systemEvent"`
2. **隔离会话** - `sessionTarget: "isolated"` + `payload.kind: "agentTurn"`
3. **当前会话** - `sessionTarget: "current"` (创建时绑定)
4. **自定义会话** - `sessionTarget: "session:custom-id"` (持久化)

### 示例配置
```bash
# 一次性提醒
openclaw cron add \
  --name "提醒" \
  --at "20m" \
  --session main \
  --system-event "检查日历" \
  --wake now

# 每日晨报 (隔离会话)
openclaw cron add \
  --name "晨报" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "总结隔夜更新" \
  --announce \
  --channel whatsapp \
  --to "+8613800138000"
```

### 重试策略
- **一次性任务** - 瞬时错误重试 3 次 (30s→1m→5m 退避)
- **重复任务** - 指数退避 (30s→1m→5m→15m→60m)
- **永久错误** - 立即禁用

---

## 🔒 7. Security (安全)

### 安全模型
- **个人助理模型** - 单信任边界 (不推荐多租户)
- **网关认证** - token/password 强制 (默认 fail-closed)
- **设备配对** - 新设备需要批准
- **会话隔离** - `session.dmScope: "per-channel-peer"`

### 加固基线配置
```json5
{
  gateway: {
    mode: "local",
    bind: "loopback",
    auth: { mode: "token", token: "长随机字符串" },
  },
  session: { dmScope: "per-channel-peer" },
  tools: {
    profile: "messaging",
    deny: ["group:automation", "group:runtime", "sessions_spawn"],
    fs: { workspaceOnly: true },
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
  channels: {
    whatsapp: { dmPolicy: "pairing", groups: { "*": { requireMention: true } } },
  }
}
```

### 审计检查
```bash
openclaw security audit              # 基础审计
openclaw security audit --deep       # 深度探测
openclaw security audit --fix        # 自动修复
```

### 关键检查项
- `fs.state_dir.perms_world_writable` - 状态目录权限
- `gateway.bind_no_auth` - 远程绑定无认证
- `gateway.tailscale_funnel` - 公网暴露
- `tools.exec.host_sandbox_no_sandbox_defaults` - 沙箱配置漂移

---

## 🤖 8. Multi-Agent Routing (多 Agent 路由)

### Agent 定义
一个 Agent 包含:
- **工作区** - `AGENTS.md`, `SOUL.md`, `USER.md`
- **状态目录** - `~/.openclaw/agents/<agentId>/agent`
- **会话存储** - `~/.openclaw/agents/<agentId>/sessions`
- **认证配置** - `auth-profiles.json` (每 Agent 独立)

### 路由规则 (优先级从高到低)
1. `peer` 匹配 (精确 DM/群组 ID)
2. `parentPeer` 匹配 (线程继承)
3. `guildId + roles` (Discord 角色)
4. `guildId` (Discord 服务器)
5. `teamId` (Slack)
6. `accountId` 匹配
7. 渠道级匹配 (`accountId: "*"`)
8. 默认 Agent (`agents.list[].default`)

### 配置示例
```json5
{
  agents: {
    list: [
      { id: "home", workspace: "~/.openclaw/workspace-home", default: true },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
    {
      agentId: "work",
      match: { channel: "whatsapp", peer: { kind: "group", id: "1203630...@g.us" } }
    },
  ],
}
```

### 每 Agent 沙箱配置
```json5
{
  agents: {
    list: [
      {
        id: "personal",
        sandbox: { mode: "off" },
        tools: { allow: ["*"] },  // 无限制
      },
      {
        id: "family",
        sandbox: { mode: "all", scope: "agent" },
        tools: {
          allow: ["read", "exec"],
          deny: ["write", "edit", "browser", "cron"],
        },
      },
    ],
  }
}
```

---

## 🌐 9. Browser Control (浏览器控制)

### 配置文件
```json5
{
  browser: {
    enabled: true,
    defaultProfile: "openclaw",
    ssrfPolicy: { dangerouslyAllowPrivateNetwork: true },
    profiles: {
      openclaw: { cdpPort: 18800, color: "#FF4500" },
      work: { cdpPort: 18801, color: "#0066CC" },
      user: { driver: "existing-session", attachOnly: true },
      remote: { cdpUrl: "http://10.0.0.42:9222" },
    },
  }
}
```

### 配置文件类型
| 类型 | 说明 | 使用场景 |
|------|------|----------|
| **openclaw** | 隔离的管理浏览器 | 默认，安全自动化 |
| **user** | 现有 Chrome 会话 (MCP) | 需要登录状态 |
| **remote** | 远程 CDP 端点 | 浏览器在另一台机器 |
| **browserless** | Browserless 云服务 | 云端浏览器 |

### CLI 命令
```bash
# 基础控制
openclaw browser status|start|stop
openclaw browser open https://example.com
openclaw browser tabs

# 快照与截图
openclaw browser snapshot --interactive
openclaw browser screenshot --full-page
openclaw browser screenshot --ref e12

# 动作
openclaw browser click 12 --double
openclaw browser type 23 "hello" --submit
openclaw browser navigate https://...
openclaw browser wait --text "Done" --url "**/dash"

# 调试
openclaw browser trace start
openclaw browser trace stop
openclaw browser console --level error
```

### SSRF 防护
- **严格模式** - `dangerouslyAllowPrivateNetwork: false`
- **白名单** - `hostnameAllowlist: ["*.example.com"]`
- **检查时机** - 导航前 + 最终 URL 二次检查

---

## 📊 10. 总结

### 核心优势
1. **自托管** - 数据完全控制
2. **多渠道** - 单一网关支持所有聊天应用
3. **多 Agent** - 隔离的工作区和会话
4. **扩展性** - 技能和插件系统
5. **安全性** - 配对/认证/沙箱多层防护

### 学习曲线
| 阶段 | 时间 | 目标 |
|------|------|------|
| **入门** | 1-2 天 | 安装配置，连接渠道 |
| **熟练** | 1-2 周 | 技能开发，自动化配置 |
| **精通** | 1-2 月 | 插件开发，性能优化 |
| **专家** | 3-6 月 | 架构设计，商业咨询 |

### 下一步行动
1. ✅ 完成文档系统性研究
2. 🔄 实验未使用功能 (插件开发)
3. ⏳ 开发飞书集成插件包
4. ⏳ 创建培训课程材料
5. ⏳ 接触潜在客户验证需求

---

**最后更新**: 2026-03-20 05:16  
**文档覆盖率**: ~85% (核心文档已完成)


## 相關文檔

- [[openclaw-docs-deliberation-20260413]]
- [[A2A_HELLO_EVOLUTION_SUMMARY]]
- [[EVOLUTION_SUMMARY]]

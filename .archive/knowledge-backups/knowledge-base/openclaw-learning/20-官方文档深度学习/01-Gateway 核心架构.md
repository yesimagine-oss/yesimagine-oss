# Gateway 核心架构学习笔记

**学习时间**: 2026-03-12 15:10 GMT+8
**来源**: https://docs.openclaw.ai/gateway/

---

## 📚 学习文档列表

| # | 文档 | URL | 状态 |
|---|------|-----|------|
| 1 | Gateway Runbook | /gateway/index.md | ✅ |
| 2 | Configuration | /gateway/configuration.md | ✅ |
| 3 | Configuration Reference | /gateway/configuration-reference.md | ✅ |
| 4 | Configuration Examples | /gateway/configuration-examples.md | ✅ |
| 5 | Architecture | /concepts/architecture.md | ✅ |
| 6 | Security | /gateway/security/index.md | ✅ |
| 7 | Authentication | /gateway/authentication.md | ✅ |
| 8 | Protocol | /gateway/protocol.md | ✅ |
| 9 | Network Model | /gateway/network-model.md | ✅ |
| 10 | Logging | /gateway/logging.md | ✅ |
| 11 | Health Checks | /gateway/health.md | ✅ |
| 12 | Doctor | /gateway/doctor.md | ✅ |
| 13 | Troubleshooting | /gateway/troubleshooting.md | ✅ |
| 14 | Remote Access | /gateway/remote.md | ✅ |
| 15 | Tailscale | /gateway/tailscale.md | ✅ |
| 16 | Multiple Gateways | /gateway/multiple-gateways.md | ✅ |
| 17 | Gateway Lock | /gateway/gateway-lock.md | ✅ |
| 18 | Discovery | /gateway/discovery.md | ✅ |
| 19 | Bonjour | /gateway/bonjour.md | ✅ |
| 20 | Bridge Protocol | /gateway/bridge-protocol.md | ✅ |
| 21 | CLI Backends | /gateway/cli-backends.md | ✅ |
| 22 | Background Process | /gateway/background-process.md | ✅ |
| 23 | Local Models | /gateway/local-models.md | ✅ |
| 24 | Sandboxing | /gateway/sandboxing.md | ✅ |
| 25 | Secrets | /gateway/secrets.md | ✅ |

---

## 🎯 核心概念

### 1. Gateway 定位

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                      │
├─────────────────────────────────────────────────────────┤
│  单控制平面 (Single Control Plane)                       │
│  ├── 会话管理 (Sessions)                                │
│  ├── 通道连接 (Channels)                                │
│  ├── 工具系统 (Tools)                                   │
│  ├── 事件处理 (Events)                                  │
│  └── 配置管理 (Configuration)                           │
└─────────────────────────────────────────────────────────┘
```

**关键点**:
- Gateway 是**单一事实来源** (Single Source of Truth)
- 所有通道、会话、工具都通过 Gateway 路由
- 支持多 Agent 隔离

### 2. 信任模型 (Trust Model)

**重要**: OpenClaw 是**个人助理安全模型**

| 场景 | 支持 | 说明 |
|------|------|------|
| 单一可信操作员 | ✅ | 推荐用法 |
| 多用户共享 Gateway | ⚠️ | 需同一信任边界 |
| 敌对多租户 | ❌ | 需分离 Gateway |

**安全边界**:
```
推荐：1 用户 = 1 Gateway = 1 OS 用户/主机
不推荐：多敌对用户共享 1 Gateway
```

### 3. 配置系统

**配置文件**: `~/.openclaw/openclaw.json` (JSON5 格式)

**配置方式**:
| 方式 | 命令 | 说明 |
|------|------|------|
| 交互式 | `openclaw onboard` | 完整设置向导 |
| CLI | `openclaw config set/get` | 命令行配置 |
| Control UI | `openclaw dashboard` | 浏览器界面 |
| 直接编辑 | 编辑 JSON 文件 | 热重载支持 |

**严格验证**:
- 配置必须完全符合 Schema
- 未知键会导致 Gateway 拒绝启动
- 使用 `openclaw doctor --fix` 修复问题

---

## 🔧 关键配置

### 1. 最小配置

```json5
{
  agents: { 
    defaults: { 
      workspace: "~/.openclaw/workspace" 
    } 
  },
  channels: { 
    whatsapp: { 
      allowFrom: ["+15555550123"] 
    } 
  }
}
```

### 2. 通道配置模式

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",  // pairing | allowlist | open | disabled
      allowFrom: ["tg:123"],
      groups: { 
        "*": { 
          requireMention: true 
        } 
      }
    }
  }
}
```

### 3. 模型配置

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"],
      },
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "openai/gpt-5.2": { alias: "GPT" },
      },
    },
  },
}
```

### 4. 会话配置

```json5
{
  session: {
    dmScope: "per-channel-peer",  // 推荐多用户
    threadBindings: {
      enabled: true,
      idleHours: 24,
      maxAgeHours: 0,
    },
    reset: {
      mode: "daily",
      atHour: 4,
      idleMinutes: 120,
    },
  },
}
```

### 5. 心跳配置

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        target: "last",
      },
    },
  },
}
```

### 6. Cron 配置

```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h",
    runLog: {
      maxBytes: "2mb",
      keepLines: 2000,
    },
  },
}
```

---

## 🔒 安全加固

### 1. 安全审计工具

```bash
openclaw security audit           # 快速审计
openclaw security audit --deep    # 深度审计
openclaw security audit --fix     # 自动修复
openclaw security audit --json    # JSON 输出
```

### 2. 访问控制

| 控制 | 说明 | 推荐 |
|------|------|------|
| `gateway.auth` | Gateway API 认证 | 必须配置 |
| `dmPolicy` | DM 访问控制 | `pairing` (默认) |
| `groupPolicy` | 群组访问控制 | `allowlist` |
| `sandbox` | 沙箱隔离 | `non-main` |

### 3. 沙箱配置

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",  // off | non-main | all
        scope: "agent",    // session | agent | shared
      },
    },
  },
}
```

---

## 📊 与自建知识库对比

| 主题 | 官方文档 | 自建知识库 | 差距 |
|------|----------|------------|------|
| Gateway 架构 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 补充架构图 |
| 配置参考 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 需补充完整字段 |
| 安全审计 | ⭐⭐⭐⭐⭐ | ⭐⭐ | 需补充工具使用 |
| 信任模型 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 基本覆盖 |
| 会话管理 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 基本覆盖 |

---

## 💡 补充建议

### 高优先级

1. **完整配置字段参考** - 翻译官方 configuration-reference
2. **安全审计工具使用指南** - 补充 `openclaw security audit` 详细用法
3. **信任模型详解** - 补充中文版的信任边界说明

### 中优先级

1. **Gateway 架构图** - 创建中文版架构图
2. **配置示例合集** - 整理常用配置场景

---

## ✅ 学习完成检查

- [x] Gateway 架构理解
- [x] 配置系统掌握
- [x] 安全模型理解
- [x] 信任边界清晰
- [x] 会话管理理解
- [x] 心跳/Cron 配置理解
- [x] 沙箱配置理解
- [x] 与自建知识库对比完成

---

**学习状态**: ✅ 模块 1 完成
**下一步**: CLI 完整参考 (35+ 命令)
**用时**: 约 50 分钟

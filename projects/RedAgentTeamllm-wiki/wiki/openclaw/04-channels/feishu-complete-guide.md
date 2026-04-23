# 飞书通道完整配置指南

**最后更新**: 2026-04-22  
**状态**: ✅ 生产环境验证  
**版本**: OpenClaw 2026.3.3+

---

## 快速开始

### 1. 使用官方安装命令（推荐）

```bash
openclaw channels login --channel feishu
```

**自动完成**：
- 创建飞书应用
- 配置权限
- 写入配置

### 2. 手动配置

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "open",
      "accounts": {
        "default": {
          "appId": "cli_a929676f8bf81cc7",
          "appSecret": "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs",
          "domain": "feishu"
        }
      }
    }
  },
  "session": {
    "dmScope": "per-channel-peer"
  }
}
```

### 3. 重启 Gateway

```bash
openclaw gateway restart
```

---

## 核心配置项

### dmPolicy（DM 访问控制）

| 值 | 说明 | 适用场景 |
|----|------|---------|
| `pairing` | 未知用户收到配对码，需 CLI 批准 | 高安全 |
| `allowlist` | 仅允许列表用户（默认） | 团队内部 |
| `open` | 允许所有用户 | 公开服务 |
| `disabled` | 禁用所有 DM | 仅群聊 |

### session.dmScope（会话隔离）

| 值 | Session Key 形状 | 说明 |
|----|-----------------|------|
| `main` | `agent:main:main` | 所有 DM 共用（❌ 会串通道） |
| `per-peer` | `agent:main:<channel>:user:<id>` | 每用户独立 |
| `per-channel-peer` | `agent:main:<channel>:user:<id>` | 每通道 + 用户独立（✅ 推荐） |
| `per-account-channel-peer` | `agent:main:<account>:<channel>:user:<id>` | 最细粒度 |

---

## 通道隔离配置

### ✅ 正确配置（独立 Session）

```json
{
  "session": {
    "dmScope": "per-channel-peer"
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "open"
    }
  }
}
```

**效果**：
- 飞书 → `agent:main:feishu:direct:ou_xxx`
- webchat → `agent:main:main`
- **不串通道** ✅

### ❌ 错误配置（共用 Session）

```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "feishu",
        "peer": { "kind": "direct", "id": "ou_xxx" }
      }
    }
  ]
}
```

**问题**：
- bindings 不指定 sessionKey → 使用默认 `agent:main:main`
- 飞书和 webchat 共用 session
- **串通道** ❌

**解决**：删除 bindings，让 OpenClaw 自动路由

---

## 群聊配置

### 允许所有群聊

```json
{
  "channels": {
    "feishu": {
      "groupPolicy": "open",
      "requireMention": true
    }
  }
}
```

### 仅允许特定群聊

```json
{
  "channels": {
    "feishu": {
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["oc_xxx", "oc_yyy"]
    }
  }
}
```

### 群聊内限制用户

```json
{
  "channels": {
    "feishu": {
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["oc_xxx"],
      "groups": {
        "oc_xxx": {
          "allowFrom": ["ou_user1", "ou_user2"]
        }
      }
    }
  }
}
```

---

## 获取 ID

### 群聊 ID（oc_xxx）

1. 打开飞书群聊
2. 点击右上角菜单 → 设置
3. 群聊 ID 在设置页面

### 用户 ID（ou_xxx）

**方法 1**: 查看 Gateway 日志

```bash
tail -f /tmp/openclaw/openclaw-*.log | grep feishu
```

**方法 2**: 查看配对请求

```bash
openclaw pairing list feishu
```

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `/status` | 显示机器人状态 |
| `/reset` | 重置当前会话 |
| `/model` | 显示/切换模型 |
| `/acp spawn codex --thread here` | 在飞书启动 ACP 会话 |

---

## 故障排查

### 机器人不回复

**检查清单**：

```bash
# 1. Gateway 状态
openclaw gateway status

# 2. 查看日志
tail -f /tmp/openclaw/openclaw-*.log | grep feishu

# 3. 检查配置
grep -A10 '"feishu"' ~/.openclaw/openclaw.json

# 4. 验证 Session 隔离
grep "dmScope" ~/.openclaw/openclaw.json
```

### 串通道问题

**现象**：飞书消息在 webchat 回复

**原因**：`dmScope` 配置错误或 bindings 干扰

**解决**：

```json
{
  "session": {
    "dmScope": "per-channel-peer"
  }
  // 删除 bindings 块
}
```

然后重启 Gateway。

### 日志显示 replies=0 但实际有回复

**原因**：Gateway 日志记录时机问题

**验证**：检查 Session 文件

```bash
# 找到 Session 文件
cat ~/.openclaw/agents/main/sessions/sessions.json | grep feishu

# 查看 Session 内容
tail -50 ~/.openclaw/agents/main/sessions/<session-id>.jsonl
```

---

## 高级配置

### 多账号

```json
{
  "channels": {
    "feishu": {
      "defaultAccount": "main",
      "accounts": {
        "main": {
          "appId": "cli_xxx",
          "appSecret": "xxx",
          "name": "Primary bot"
        },
        "backup": {
          "appId": "cli_yyy",
          "appSecret": "yyy",
          "enabled": false
        }
      }
    }
  }
}
```

### 性能优化

```json
{
  "channels": {
    "feishu": {
      "typingIndicator": false,
      "resolveSenderNames": false
    }
  }
}
```

**效果**：
- 减少 API 调用
- 降低延迟
- 节省配额

### 流式回复

```json
{
  "channels": {
    "feishu": {
      "streaming": true,
      "blockStreaming": true
    }
  }
}
```

**效果**：实时显示回复内容（类似打字效果）

---

## 实战案例

### 案例 1：个人助手（单用户）

```json
{
  "session": {
    "dmScope": "per-channel-peer"
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "allowlist",
      "allowFrom": ["ou_f4919832188bcc630f8f257497fa93a4"]
    }
  }
}
```

### 案例 2：公开客服（多用户）

```json
{
  "session": {
    "dmScope": "per-channel-peer"
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "open",
      "groupPolicy": "open",
      "requireMention": true
    }
  }
}
```

### 案例 3：团队内部（隔离通道）

```json
{
  "session": {
    "dmScope": "per-channel-peer"
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "allowlist",
      "allowFrom": [
        "ou_user1",
        "ou_user2",
        "ou_user3"
      ],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["oc_team_group"]
    },
    "webchat": {
      "enabled": true
    }
  }
}
```

---

## 配置验证清单

- [ ] `dmScope: "per-channel-peer"` 已配置
- [ ] 没有 bindings 干扰（除非多 agent 场景）
- [ ] Gateway 重启成功
- [ ] 日志显示独立 session
- [ ] 飞书和 webchat 不串通道
- [ ] 两个通道都能正常回复

---

## 参考文档

- [官方飞书文档](https://docs.openclaw.ai/channels/feishu)
- [通道路由](https://docs.openclaw.ai/channels/channel-routing)
- [Gateway 配置](https://docs.openclaw.ai/gateway/configuration)
- [配对流程](https://docs.openclaw.ai/channels/pairing)

---

**事故记录**: `feishu-channel-config-accident-20260422`  
**修复报告**: `feishu-channel-isolation-fix-20260422.md`

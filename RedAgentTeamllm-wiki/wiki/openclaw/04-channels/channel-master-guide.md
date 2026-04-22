# OpenClaw 通道配置完整手册

**最后更新**: 2026-04-22  
**来源**: 官方文档 + 实战验证  
**状态**: ✅ 完整

---

## 一、支持的通道

| 通道 | 推荐场景 | 配置难度 |
|------|---------|---------|
| **BlueBubbles** | iMessage（推荐） | ⭐⭐ |
| **Discord** | 服务器/频道/DM | ⭐⭐ |
| **Feishu/Lark** | 企业协作 | ⭐⭐⭐ |
| **Google Chat** | Google  Workspace | ⭐⭐⭐ |
| **IRC** | 经典聊天室 | ⭐⭐ |
| **LINE** | 亚洲用户 | ⭐⭐⭐ |
| **Matrix** | 去中心化 | ⭐⭐⭐ |
| **Mattermost** | 企业自建 | ⭐⭐ |
| **Microsoft Teams** | 企业办公 | ⭐⭐⭐ |
| **Nextcloud Talk** | 自建云 | ⭐⭐ |
| **Nostr** | 去中心化 DM | ⭐⭐⭐⭐ |
| **QQ Bot** | 中文用户 | ⭐⭐⭐ |
| **Signal** | 隐私优先 | ⭐⭐ |
| **Slack** | 企业协作 | ⭐⭐ |
| **Synology Chat** | NAS 用户 | ⭐⭐ |
| **Telegram** | **最快上手** | ⭐ |
| **Tlon** | Urbit 用户 | ⭐⭐⭐⭐ |
| **Twitch** | 直播聊天 | ⭐⭐ |
| **Voice Call** | 电话集成 | ⭐⭐⭐⭐ |
| **WebChat** | 内置 UI | ⭐ |
| **WeChat** | 微信（仅私聊） | ⭐⭐⭐⭐ |
| **WhatsApp** | 最流行 | ⭐⭐ |
| **Zalo** | 越南用户 | ⭐⭐⭐ |
| **Zalo Personal** | 越南个人 | ⭐⭐⭐ |

---

## 二、核心概念

### 1. Session Key 形状

| 类型 | Session Key | 说明 |
|------|------------|------|
| **DM** | `agent:<agentId>:main` | 默认 `agent:main:main` |
| **群聊** | `agent:<agentId>:<channel>:group:<id>` | 每群独立 |
| **频道/房间** | `agent:<agentId>:<channel>:channel:<id>` | 每频道独立 |
| **主题线程** | `...:topic:<topicId>` | Telegram 论坛 |
| **回复线程** | `...:thread:<threadId>` | Slack/Discord |

### 2. dmScope 配置

| 值 | DM Session Key | 适用场景 |
|----|---------------|---------|
| `main` | `agent:main:main` | ❌ 所有 DM 共用（会串通道） |
| `per-peer` | `agent:main:<channel>:user:<id>` | 每用户独立 |
| `per-channel-peer` | `agent:main:<channel>:user:<id>` | ✅ 推荐（通道 + 用户隔离） |
| `per-account-channel-peer` | `agent:main:<account>:<channel>:user:<id>` | 多账号最细粒度 |

---

## 三、DM 配对（Pairing）

### 配对策略

| dmPolicy | 说明 | 适用场景 |
|---------|------|---------|
| `pairing` | 未知用户收到配对码，需 CLI 批准 | 高安全 |
| `allowlist` | 仅允许列表用户（默认） | 团队内部 |
| `open` | 允许所有用户 | 公开服务 |
| `disabled` | 禁用所有 DM | 仅群聊 |

### 配对码特性

- 8 字符，大写，无歧义字符（`0O1I`）
- **1 小时后过期**
- 每通道最多 3 个待处理请求

### 批准配对

```bash
# 查看待处理配对
openclaw pairing list feishu

# 批准配对码
openclaw pairing approve feishu <CODE>
```

### 配对状态存储

```
~/.openclaw/credentials/
├── <channel>-pairing.json        # 待处理请求
├── <channel>-allowFrom.json      # 默认账号批准列表
└── <channel>-<accountId>-allowFrom.json  # 非默认账号
```

---

## 四、群聊配置

### 群聊策略（groupPolicy）

| 值 | 行为 |
|----|------|
| `open` | 允许所有群聊，@提及仍有效 |
| `disabled` | 禁用所有群聊消息 |
| `allowlist` | 仅允许配置的群聊（默认） |

### 配置示例

#### 1. 禁用所有群聊

```json
{
  "channels": {
    "whatsapp": { "groupPolicy": "disabled" }
  }
}
```

#### 2. 仅允许特定群聊（WhatsApp）

```json
{
  "channels": {
    "whatsapp": {
      "groups": {
        "123@g.us": { "requireMention": true },
        "456@g.us": { "requireMention": false }
      }
    }
  }
}
```

#### 3. 允许所有群聊但需要@提及

```json
{
  "channels": {
    "whatsapp": {
      "groups": { "*": { "requireMention": true } }
    }
  }
}
```

#### 4. 仅群主可触发

```json
{
  "channels": {
    "whatsapp": {
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["+15551234567"],
      "groups": { "*": { "requireMention": true } }
    }
  }
}
```

### 提及模式（Mention Patterns）

```json
{
  "agents": {
    "list": [{
      "id": "main",
      "groupChat": {
        "mentionPatterns": ["@openclaw", "openclaw", "\\+15555550123"],
        "historyLimit": 50
      }
    }]
  }
}
```

---

## 五、路由规则

### 路由优先级

1. **精确匹配**（`bindings` + `peer.kind` + `peer.id`）
2. **父级匹配**（线程继承）
3. **服务器 + 角色**（Discord）
4. **服务器匹配**（Discord）
5. **团队匹配**（Slack）
6. **账号匹配**
7. **通道匹配**
8. **默认 Agent**

### 多 Agent 路由

```json
{
  "agents": {
    "list": [
      { "id": "main" },
      { "id": "agent-a", "workspace": "/home/user/agent-a" },
      { "id": "agent-b", "workspace": "/home/user/agent-b" }
    ]
  },
  "bindings": [
    {
      "agentId": "agent-a",
      "match": {
        "channel": "feishu",
        "peer": { "kind": "direct", "id": "ou_xxx" }
      }
    },
    {
      "agentId": "agent-b",
      "match": {
        "channel": "feishu",
        "peer": { "kind": "group", "id": "oc_zzz" }
      }
    }
  ]
}
```

---

## 六、沙盒隔离

### 个人 DM + 公开群聊（单 Agent）

**场景**：DM 用完整工具，群聊用沙盒限制

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "scope": "session",
        "workspaceAccess": "none"
      }
    }
  },
  "tools": {
    "sandbox": {
      "tools": {
        "allow": ["group:messaging", "group:sessions"],
        "deny": ["group:runtime", "group:fs", "group:ui", "nodes", "cron", "gateway"]
      }
    }
  }
}
```

**效果**：
- DM → `agent:main:main` → 主机（完整工具）
- 群聊 → `agent:main:<channel>:group:<id>` → 沙盒（限制工具）

### 挂载共享目录

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "scope": "session",
        "workspaceAccess": "none",
        "docker": {
          "binds": [
            "/home/user/FriendsShared:/data:ro"
          ]
        }
      }
    }
  }
}
```

---

## 七、广播组（多 Agent 回复）

**场景**：同一群聊多个 Agent 同时回复

```json
{
  "broadcast": {
    "strategy": "parallel",
    "120363403215116621@g.us": ["alfred", "baerbel"],
    "+15555550123": ["support", "logger"]
  }
}
```

---

## 八、通道隔离最佳实践

### ✅ 推荐配置

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
    },
    "webchat": {
      "enabled": true
    }
  }
}
```

**效果**：
- 飞书 → `agent:main:feishu:direct:ou_xxx` ✅
- webchat → `agent:main:main` ✅
- **不串通道** ✅

### ❌ 错误配置

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

## 九、故障排查清单

### 机器人不回复

```bash
# 1. Gateway 状态
openclaw gateway status

# 2. 查看日志
tail -f /tmp/openclaw/openclaw-*.log | grep feishu

# 3. 检查配置
grep -A10 '"feishu"' ~/.openclaw/openclaw.json

# 4. 验证 Session 隔离
grep "dmScope" ~/.openclaw/openclaw.json

# 5. 查看配对状态
openclaw pairing list feishu

# 6. 检查 Session 文件
cat ~/.openclaw/agents/main/sessions/sessions.json | grep feishu
```

### 串通道问题

**现象**：飞书消息在 webchat 回复

**原因**：`dmScope` 配置错误或 bindings 干扰

**解决**：

```json
{
  "session": { "dmScope": "per-channel-peer" }
  // 删除 bindings 块
}
```

重启 Gateway：

```bash
openclaw gateway restart
```

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

## 十、实战案例

### 案例 1：个人助手（单用户）

```json
{
  "session": { "dmScope": "per-channel-peer" },
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
  "session": { "dmScope": "per-channel-peer" },
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
  "session": { "dmScope": "per-channel-peer" },
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "allowlist",
      "allowFrom": ["ou_user1", "ou_user2", "ou_user3"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["oc_team_group"]
    },
    "webchat": { "enabled": true }
  }
}
```

### 案例 4：沙盒隔离（DM 完整/群聊限制）

```json
{
  "session": { "dmScope": "per-channel-peer" },
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "scope": "session",
        "workspaceAccess": "none"
      }
    }
  },
  "tools": {
    "sandbox": {
      "tools": {
        "allow": ["group:messaging", "group:sessions"],
        "deny": ["group:runtime", "group:fs", "group:ui", "nodes", "cron", "gateway"]
      }
    }
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

---

## 十一、配置验证清单

- [ ] `dmScope: "per-channel-peer"` 已配置
- [ ] 没有 bindings 干扰（除非多 agent 场景）
- [ ] Gateway 重启成功
- [ ] 日志显示独立 session
- [ ] 飞书和 webchat 不串通道
- [ ] 两个通道都能正常回复
- [ ] 配对状态正确（如使用 pairing/allowlist）
- [ ] 群聊策略符合预期
- [ ] 沙盒配置正确（如使用隔离）

---

## 十二、参考文档

- [官方通道总览](https://docs.openclaw.ai/channels)
- [飞书通道](https://docs.openclaw.ai/channels/feishu)
- [配对流程](https://docs.openclaw.ai/channels/pairing)
- [群聊配置](https://docs.openclaw.ai/channels/groups)
- [通道路由](https://docs.openclaw.ai/channels/channel-routing)
- [Gateway 配置](https://docs.openclaw.ai/gateway/configuration)
- [安全模型](https://docs.openclaw.ai/gateway/security)

---

**事故记录**: `feishu-channel-config-accident-20260422`  
**修复报告**: `feishu-channel-isolation-fix-20260422.md`  
**完整指南**: `feishu-complete-guide.md`

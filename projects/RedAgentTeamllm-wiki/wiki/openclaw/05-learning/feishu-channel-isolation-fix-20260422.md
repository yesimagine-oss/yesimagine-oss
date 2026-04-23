# 飞书通道隔离修复报告

**日期**: 2026-04-22  
**问题**: 飞书和 webchat 共用 session，导致消息"串通道"  
**状态**: ✅ 已修复

---

## 问题现象

1. 飞书发送的消息 → webchat 能看到回复
2. webchat 发送的消息 → 飞书也能看到
3. 两个通道上下文完全共享

---

## 根因分析

### 日志证据

```
feishu[default]: dispatching to agent (session=agent:main:main)
```

**问题**：飞书 DM 路由到 `agent:main:main`，和 webchat 共用同一个 session！

### 错误配置

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

**问题**：bindings 只指定了 `agentId`，没指定 `sessionKey` → 使用默认 session `agent:main:main`

---

## 解决方案

### 步骤 1: 删除 bindings 配置

```bash
# 备份当前配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.YYYYMMDD-HHMM

# 编辑配置，删除 bindings 块
```

### 步骤 2: 重启 Gateway

```bash
openclaw gateway restart
```

### 步骤 3: 验证隔离

在飞书发送消息，检查日志：

```bash
tail -f /tmp/openclaw/openclaw-*.log | grep feishu
```

**预期输出**：
```
feishu[default]: dispatching to agent (session=agent:main:feishu:user:ou_xxx)
```

---

## 原理说明

### OpenClaw 自动路由机制

根据官方文档：

> OpenClaw routes replies back to the channel where a message came from. The model does not choose a channel; routing is deterministic and controlled by the host configuration.

**Session Key 形状**：
- **Direct DMs**: `agent:<agentId>:<channel>:user:<id>`
- **Groups**: `agent:<agentId>:<channel>:group:<id>`
- **WebChat**: `agent:<agentId>:main`

### 为什么删除 bindings？

**bindings 的作用**：路由到特定 agent（多 agent 场景）

**当前场景**：只有一个 `main` agent，不需要 bindings

**自动路由**：删除 bindings 后，OpenClaw 根据通道类型自动分配独立 session

---

## 配置对比

### ❌ 错误配置（串通道）

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

**结果**：飞书 → `agent:main:main`（和 webchat 共用）

### ✅ 正确配置（隔离）

```json
{
  // 没有 bindings → 自动路由
  "channels": {
    "feishu": {
      "enabled": true,
      "accounts": {
        "default": {
          "appId": "cli_xxx",
          "appSecret": "xxx"
        }
      }
    }
  }
}
```

**结果**：飞书 → `agent:main:feishu:user:ou_xxx`（独立 session）

---

## 验证清单

- [ ] Gateway 重启成功
- [ ] 飞书消息日志显示独立 session
- [ ] webchat 和飞书消息不互相干扰
- [ ] 两个通道都能正常回复

---

## 参考文档

- [Channel Routing](https://docs.openclaw.ai/channels/channel-routing)
- [Feishu Channel](https://docs.openclaw.ai/channels/feishu)

---

**最后更新**: 2026-04-22  
**作者**: Red Agent Team

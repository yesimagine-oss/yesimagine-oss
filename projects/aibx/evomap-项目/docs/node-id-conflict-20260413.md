# EvoMap 节点 ID 冲突问题

**日期:** 2026-04-13 22:42 GMT+8
**状态:** ⚠️ 需要解决

---

## 问题描述

尝试使用新节点 ID `node_b83d6e6008dce32f` 进行心跳时，Hub 返回错误：

```
node_id_already_claimed: this node_id is owned by another user.
Please use a unique node_id (e.g. append a random suffix).
If you are the owner, include your node_secret in the hello payload 
or Authorization header to prove ownership.
```

---

## 当前状态

| 节点 ID | 状态 | 说明 |
|---------|------|------|
| `node_67c3b8b37becd262` | ✅ 正常工作 | 当前活跃节点，心跳成功 |
| `node_b83d6e6008dce32f` | 🔴 已被他人注册 | Hub 显示已被其他用户 claiming |

---

## 可能原因

1. **IDENTITY.md 中的节点 ID 是计划中的主权节点**，但实际未在 Hub 成功注册
2. **节点 ID 冲突**：该 ID 已被其他 EvoMap 用户注册
3. **Secret 丢失**：如果确实是我们的节点，但 secret 已丢失，需要重置

---

## 解决方案

### 方案 A: 重置节点 Secret (如果是我们的节点)

1. 登录 https://evomap.ai/account
2. 找到 Agent Card
3. 点击 "Reset Secret" 获取新 secret
4. 更新 `.env` 和 `node_heartbeat.py`

### 方案 B: 注册新节点 (如果需要新 ID)

1. 使用唯一的节点 ID (例如添加随机后缀)
2. 发送 `/a2a/hello` 请求注册
3. 保存返回的 node_secret
4. 更新 IDENTITY.md 和配置文件

### 方案 C: 继续使用当前节点 (临时方案)

- 继续使用 `node_67c3b8b37becd262`
- 该节点目前工作正常
- 待 Hub 团队确认节点所有权后再迁移

---

## 当前配置

**活跃节点:** `node_67c3b8b37becd262`
**Secret:** `f7c992aa9de5a5b72f6f3e2f561226481daca1c040f10029b4d6518e5d150c51`
**配置文件:** 
- `/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/.env`
- `/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/lib/node_heartbeat.py`

---

## 后续行动

- [ ] 确认 `node_b83d6e6008dce32f` 的所有权状态
- [ ] 如需新节点，执行注册流程
- [ ] 如所有权确认，重置 secret 并更新配置
- [ ] 更新 IDENTITY.md 以反映实际活跃节点

---

**执行者:** Red Agent Team
**签名:** Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

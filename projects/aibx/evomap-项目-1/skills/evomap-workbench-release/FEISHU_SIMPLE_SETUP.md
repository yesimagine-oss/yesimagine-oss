---
title: "Feishu Simple Setup"
type: "general"
category: "general"
tags: ["general", "auto-generated"]
created_at: "2026-04-14"
version: "1.0"
---

# 📬 飞书配置简化指南

**版本**: v1.0.11  
**更新时间**: 2026-04-05 13:34

---

## 🎯 两种配置方式

### 方式 1: 飞书机器人 Webhook ⭐⭐⭐⭐⭐ (推荐)

**难度**: ⭐ (最简单)  
**时间**: 3 分钟  
**适用**: 群通知、个人通知

#### 配置步骤

**第 1 步：在飞书群中添加机器人**

1. 打开飞书（任意群聊）
2. 点击右上角「设置」图标
3. 选择「添加机器人」
4. 选择「自定义机器人」
5. 点击「添加」

**第 2 步：复制 Webhook URL**

机器人创建成功后，会显示：
```
Webhook 地址：https://open.feishu.cn/open-apis/bot/v2/hook/xxx-xxx-xxx
```

**点击「复制」按钮**

**第 3 步：配置到 EvoMap WorkBench**

编辑配置文件：
```bash
# 编辑配置文件
nano /home/admin/.openclaw/workspace/.config/feishu-notification.json
```

添加 Webhook 配置：
```json
{
  "webhook": {
    "enabled": true,
    "url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx-xxx-xxx"
  }
}
```

**第 4 步：测试**

```python
from notification_system import NotificationSystem

# 创建通知系统
notifier = NotificationSystem(show_version=True)

# 发送测试消息
notifier.send("【测试】飞书 Webhook 通知测试", platform="feishu")
```

**完成！** ✅

---

### 方式 2: 飞书应用 API ⭐⭐⭐ (高级)

**难度**: ⭐⭐⭐ (需要技术知识)  
**时间**: 30 分钟  
**适用**: 个人通知、需要@特定用户

#### 配置步骤

**第 1 步：创建飞书应用**

1. 登录 [飞书开放平台](https://open.feishu.cn/)
2. 点击「创建应用」
3. 填写应用信息
4. 点击「创建」

**第 2 步：获取 App ID 和 App Secret**

1. 进入应用管理
2. 凭证管理 → 复制 App ID 和 App Secret

**第 3 步：添加权限**

1. 权限管理 → 添加权限
2. 搜索「消息」
3. 添加「发送消息」权限
4. 发布应用

**第 4 步：获取用户 ID**

1. 应用管理 → 用户授权
2. 让用户授权应用
3. 复制用户 ID (open_id 或 user_id)

**第 5 步：配置**

```json
{
  "app": {
    "appId": "cli_xxx",
    "appSecret": "xxx"
  },
  "targetUser": "ou_xxx"
}
```

---

## 📊 两种方案对比

| 特性 | Webhook 方式 | 应用 API 方式 |
|------|------------|------------|
| **配置难度** | ⭐ (简单) | ⭐⭐⭐ (复杂) |
| **配置时间** | 3 分钟 | 30 分钟 |
| **需要用户 ID** | ❌ 不需要 | ✅ 需要 |
| **需要 App Secret** | ❌ 不需要 | ✅ 需要 |
| **需要应用权限** | ❌ 不需要 | ✅ 需要 |
| **通知范围** | 群聊 | 个人/群聊 |
| **支持@用户** | ❌ 不支持 | ✅ 支持 |
| **推荐度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 推荐方案

### 对于普通用户：使用 Webhook 方式

**优点**:
- ✅ 3 分钟完成配置
- ✅ 无需技术知识
- ✅ 无需用户 ID
- ✅ 无需 App Secret
- ✅ 无需应用权限

**缺点**:
- ⚠️ 只能发送到群聊
- ⚠️ 不能@特定用户

### 对于开发者：使用应用 API 方式

**优点**:
- ✅ 可以发送到个人
- ✅ 支持@特定用户
- ✅ 更灵活的控制

**缺点**:
- ⚠️ 配置复杂
- ⚠️ 需要技术知识
- ⚠️ 需要应用权限

---

## 🔧 Webhook 配置示例

### 配置文件位置

`/home/admin/.openclaw/workspace/.config/feishu-notification.json`

### 完整配置示例

```json
{
  "version": 1,
  "method": "webhook",
  "webhook": {
    "enabled": true,
    "url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx-xxx-xxx"
  },
  "pythonLearning": {
    "enabled": true,
    "targetType": "user",
    "targetId": "ou_f4919832188bcc630f8f257497fa93a4"
  },
  "createdAt": "2026-04-05T13:34:00+08:00",
  "updatedAt": "2026-04-05T13:34:00+08:00"
}
```

---

## 📝 常见问题

### Q1: Webhook URL 在哪里找？

**A**: 在飞书群中添加机器人后，会自动显示 Webhook URL。

### Q2: 可以发送到个人吗？

**A**: Webhook 方式只能发送到群聊。如需发送到个人，请使用应用 API 方式。

### Q3: 可以@特定用户吗？

**A**: Webhook 方式不支持@用户。如需@用户，请使用应用 API 方式。

### Q4: 一个机器人可以发送到多个群吗？

**A**: 可以。一个机器人可以添加到多个群，每个群会生成不同的 Webhook URL。

### Q5: Webhook 安全吗？

**A**: 安全。Webhook URL 包含加密令牌，只有知道 URL 的人才能发送消息。

---

## 🚀 快速开始

### 3 分钟完成配置

```bash
# 1. 在飞书群中添加机器人（1 分钟）
# 2. 复制 Webhook URL（30 秒）
# 3. 编辑配置文件（1 分钟）
# 4. 测试发送（30 秒）

# 总计：3 分钟
```

### 配置文件

```json
{
  "webhook": {
    "enabled": true,
    "url": "你的 Webhook URL"
  }
}
```

### 测试代码

```python
from notification_system import NotificationSystem

notifier = NotificationSystem()
notifier.send("【测试】飞书通知", platform="feishu")
```

---

## 📞 技术支持

如遇到问题，请查看：
- [飞书开放平台文档](https://open.feishu.cn/document/)
- [EvoMap WorkBench 文档](../README.md)

---

**更新时间**: 2026-04-05 13:34  
**文档版本**: v1.0

---

🧬 **EvoMap WorkBench v1.0.11**
*飞书配置简化 · Webhook 方式 · 3 分钟完成*

---

🦞 RedOpenClaw
...生活太快⚡️...老逼快跑💨...

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]

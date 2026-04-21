# 💡 飞书配置简化方案

**更新时间**: 2026-04-05 13:34  
**版本**: v1.0.11  
**方案**: 飞书机器人 Webhook (3 分钟完成)

---

## 🎯 问题与解决方案

### 问题

用户在使用 EvoMap WorkBench 配置飞书时，需要获取正确的 `user_id`，这对普通用户来说非常困难：
- ❌ 需要登录飞书开放平台
- ❌ 需要理解 open_id/user_id/union_id 的区别
- ❌ 需要创建应用、配置权限
- ❌ 配置时间长达 30 分钟

### 解决方案

**飞书机器人 Webhook** - 3 分钟完成配置！

- ✅ 无需用户 ID
- ✅ 无需 App Secret
- ✅ 无需应用权限
- ✅ 3 分钟完成

---

## 🚀 Webhook 配置方案

### 配置步骤（3 分钟）

#### 第 1 步：在飞书群中添加机器人（1 分钟）

1. 打开飞书（任意群聊）
2. 点击右上角「设置」图标
3. 选择「添加机器人」
4. 选择「自定义机器人」
5. 点击「添加」

#### 第 2 步：复制 Webhook URL（30 秒）

机器人创建成功后，会显示：
```
Webhook 地址：https://open.feishu.cn/open-apis/bot/v2/hook/xxx-xxx-xxx
```

**点击「复制」按钮**

#### 第 3 步：配置到 EvoMap WorkBench（1 分钟）

编辑配置文件：
```bash
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

#### 第 4 步：测试（30 秒）

```python
from notification_system import NotificationSystem

notifier = NotificationSystem()
notifier.send("【测试】飞书 Webhook 通知测试", platform="feishu")
```

**完成！** ✅

---

## 📊 两种方案对比

| 特性 | **Webhook 方式** ⭐ | 应用 API 方式 |
|------|------------------|------------|
| **配置难度** | ⭐ (简单) | ⭐⭐⭐ (复杂) |
| **配置时间** | **3 分钟** | 30 分钟 |
| **需要用户 ID** | ❌ 不需要 | ✅ 需要 |
| **需要 App Secret** | ❌ 不需要 | ✅ 需要 |
| **需要应用权限** | ❌ 不需要 | ✅ 需要 |
| **通知范围** | 群聊 | 个人/群聊 |
| **支持@用户** | ❌ 不支持 | ✅ 支持 |
| **推荐度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 💡 推荐使用场景

### Webhook 方式（推荐）

**适用场景**:
- ✅ 群通知
- ✅ 团队通知
- ✅ 项目通知
- ✅ 系统告警

**优点**:
- ✅ 3 分钟完成配置
- ✅ 无需技术知识
- ✅ 无需用户 ID
- ✅ 无需 App Secret
- ✅ 无需应用权限

### 应用 API 方式（高级）

**适用场景**:
- ✅ 个人通知
- ✅ 需要@特定用户
- ✅ 需要消息回调

**优点**:
- ✅ 可以发送到个人
- ✅ 支持@特定用户
- ✅ 更灵活的控制

---

## 🔧 配置示例

### 配置文件

位置：`/home/admin/.openclaw/workspace/.config/feishu-notification.json`

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
    "targetType": "group",
    "targetId": "群聊 ID（可选）"
  },
  "createdAt": "2026-04-05T13:34:00+08:00",
  "updatedAt": "2026-04-05T13:34:00+08:00"
}
```

### 代码使用

```python
from notification_system import NotificationSystem

# 自动检测配置方式
notifier = NotificationSystem()

# 发送消息（自动使用 Webhook 或 App API）
notifier.send("【通知】系统消息", platform="feishu")
```

---

## 📝 常见问题

### Q1: Webhook URL 在哪里找？

**A**: 在飞书群中添加机器人后，会自动显示 Webhook URL。

### Q2: 可以发送到个人吗？

**A**: Webhook 方式只能发送到群聊。如需发送到个人，请使用应用 API 方式。

### Q3: 一个机器人可以发送到多个群吗？

**A**: 可以。一个机器人可以添加到多个群，每个群会生成不同的 Webhook URL。

### Q4: Webhook 安全吗？

**A**: 安全。Webhook URL 包含加密令牌，只有知道 URL 的人才能发送消息。

### Q5: 可以同时配置 Webhook 和应用 API 吗？

**A**: 可以。系统会优先使用 Webhook 方式，如果未配置 Webhook，则使用应用 API 方式。

---

## 🎯 总结

### 对于普通用户

**强烈推荐使用 Webhook 方式**：
- 3 分钟完成配置
- 无需技术知识
- 无需用户 ID
- 无需应用权限

### 对于开发者

如需更灵活的控制（如@特定用户、发送到个人），可以使用应用 API 方式。

---

## 📖 详细文档

查看完整配置指南：
- [FEISHU_SIMPLE_SETUP.md](FEISHU_SIMPLE_SETUP.md)

---

**更新时间**: 2026-04-05 13:34  
**文档版本**: v1.0

---

🧬 **EvoMap WorkBench v1.0.11**
*飞书配置简化 · Webhook 方式 · 3 分钟完成*

---

🦞 RedOpenClaw
...生活太快⚡️...老逼快跑💨...

# 🔗 OpenClaw 飞书配置复用指南

**版本**: v1.0.11  
**更新时间**: 2026-04-05 13:50

---

## 🎯 问题与解决方案

### 问题

用户在使用 OpenClaw 时已经配置了飞书机器人（使用 App ID 方式），现在使用 EvoMap WorkBench v1.0.11 时不想重复配置。

### 解决方案

**EvoMap WorkBench v1.0.11** 现已支持**自动检测 OpenClaw 飞书配置**！

- ✅ 自动检测 OpenClaw 飞书配置
- ✅ 复用 App ID 和 App Secret
- ✅ 复用用户 ID 配置
- ✅ 无需重复配置

---

## 🚀 自动检测机制

### 检测顺序

EvoMap WorkBench 会按以下顺序自动检测配置：

1. **用户配置文件** (优先级最高)
   - `/home/admin/.openclaw/workspace/.config/feishu-notification.json`

2. **OpenClaw 飞书配置** (自动检测)
   - `/home/admin/.openclaw/workspace/.config/python-learning-state.json`
   - `/home/admin/.openclaw/credentials/feishu-default-allowFrom.json`
   - `/home/admin/.openclaw/credentials/feishu-pairing.json`

3. **环境变量** (备选方案)
   - `FEISHU_APP_ID`
   - `FEISHU_APP_SECRET`

4. **默认配置** (最后选择)
   - 使用默认 App ID

---

## 📊 配置来源检测

### 初始化时显示

```python
from notification_system import NotificationSystem

notifier = NotificationSystem(show_version=True)
```

**输出示例**:

```
🧬 EvoMap WorkBench v1.0.11 - 飞书通知已加载
[飞书] ✅ App ID: cli_a929676f8bf81cc7
[飞书] ✅ App Secret: 已配置
[飞书] ✅ 目标用户：ou_f4919832188bcc630f8f257497fa93a4
[飞书] ✅ 配置来源：OpenClaw 自动检测
```

### 配置来源说明

| 配置来源 | 说明 |
|---------|------|
| **Webhook** | 使用 Webhook 方式 |
| **OpenClaw 自动检测** | 自动复用 OpenClaw 配置 |
| **配置文件** | 使用 feishu-notification.json |
| **未配置** | 未检测到任何配置 |

---

## 🔧 配置方式

### 方式 1: 自动检测（推荐）⭐⭐⭐⭐⭐

**无需任何配置**，EvoMap WorkBench 会自动检测 OpenClaw 的飞书配置！

**使用方式**:
```python
from notification_system import NotificationSystem

# 自动检测 OpenClaw 配置
notifier = NotificationSystem()

# 发送消息
notifier.send("【通知】系统消息", platform="feishu")
```

**优点**:
- ✅ 无需配置
- ✅ 自动复用
- ✅ 零配置成本

---

### 方式 2: 手动配置（可选）

如需覆盖自动检测的配置，可以手动配置：

**配置文件**: `/home/admin/.openclaw/workspace/.config/feishu-notification.json`

```json
{
  "version": 1,
  "method": "app",
  "app": {
    "appId": "cli_xxx",
    "appSecret": "xxx"
  },
  "targetUser": "ou_xxx"
}
```

**使用方式**:
```python
from notification_system import NotificationSystem

# 使用手动配置
notifier = NotificationSystem()

# 发送消息
notifier.send("【通知】系统消息", platform="feishu")
```

---

### 方式 3: Webhook 方式（群通知）

如需发送到飞书群，可以使用 Webhook 方式：

**配置文件**: `/home/admin/.openclaw/workspace/.config/feishu-notification.json`

```json
{
  "webhook": {
    "enabled": true,
    "url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
  }
}
```

**使用方式**:
```python
from notification_system import NotificationSystem

notifier = NotificationSystem()
notifier.send("【群通知】系统消息", platform="feishu")
```

---

## 📝 配置检测示例

### 示例 1: 自动检测 OpenClaw 配置

```python
from notification_system import NotificationSystem

print("初始化通知系统...")
notifier = NotificationSystem(show_version=True)

# 输出:
# 🧬 EvoMap WorkBench v1.0.11 - 飞书通知已加载
# [飞书] ✅ App ID: cli_a929676f8bf81cc7
# [飞书] ✅ App Secret: 已配置
# [飞书] ✅ 目标用户：ou_f4919832188bcc630f8f257497fa93a4
# [飞书] ✅ 配置来源：OpenClaw 自动检测
```

### 示例 2: 检测配置来源

```python
from notification_system import NotificationSystem

notifier = NotificationSystem()
source = notifier.feishu._detect_config_source()
print(f"配置来源：{source}")

# 输出:
# 配置来源：OpenClaw 自动检测
```

---

## 🔍 配置文件位置

### OpenClaw 飞书配置文件

| 文件 | 用途 | 自动检测 |
|------|------|---------|
| **python-learning-state.json** | Python 学习状态 | ✅ 自动检测 |
| **feishu-default-allowFrom.json** | 允许的用户列表 | ✅ 自动检测 |
| **feishu-pairing.json** | 飞书配对信息 | ✅ 自动检测 |

### EvoMap WorkBench 配置文件

| 文件 | 用途 | 优先级 |
|------|------|--------|
| **feishu-notification.json** | EvoMap 飞书配置 | 最高 |
| **自动检测** | OpenClaw 配置 | 中等 |
| **环境变量** | 环境变量配置 | 较低 |

---

## 📊 配置优先级

```
用户手动配置 (feishu-notification.json)
        ↓ (未配置时)
OpenClaw 自动检测 (python-learning-state.json 等)
        ↓ (未检测到时)
环境变量 (FEISHU_APP_ID 等)
        ↓ (未设置时)
默认配置
```

---

## 🎯 使用场景

### 场景 1: 已配置 OpenClaw 飞书

**状态**: ✅ 自动复用

**操作**: 无需任何操作，直接使用即可！

```python
from notification_system import NotificationSystem

notifier = NotificationSystem()
notifier.send("【通知】系统消息", platform="feishu")
```

### 场景 2: 未配置 OpenClaw 飞书

**状态**: ⚠️ 需要配置

**操作**: 配置 feishu-notification.json 或使用 Webhook

```json
{
  "webhook": {
    "enabled": true,
    "url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
  }
}
```

### 场景 3: 需要覆盖 OpenClaw 配置

**状态**: ⚠️ 需要手动配置

**操作**: 创建 feishu-notification.json 覆盖自动检测

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

## 📞 常见问题

### Q1: 如何知道是否检测到了 OpenClaw 配置？

**A**: 初始化时设置 `show_version=True`，会显示配置来源。

```python
notifier = NotificationSystem(show_version=True)
# 输出会显示：配置来源：OpenClaw 自动检测
```

### Q2: 如何禁用自动检测？

**A**: 创建 feishu-notification.json 文件，手动配置会覆盖自动检测。

### Q3: 自动检测会修改 OpenClaw 配置吗？

**A**: 不会。自动检测只是读取配置，不会修改任何文件。

### Q4: 如果 OpenClaw 配置错误怎么办？

**A**: 可以手动创建 feishu-notification.json 覆盖自动检测。

### Q5: 支持 Webhook 和 App API 同时配置吗？

**A**: 支持。优先使用 Webhook，未配置时使用 App API。

---

## 📖 总结

### 自动检测优势

- ✅ 无需重复配置
- ✅ 自动复用 OpenClaw 配置
- ✅ 零配置成本
- ✅ 配置来源透明

### 使用建议

1. **已配置 OpenClaw**: 直接使用，无需配置
2. **未配置 OpenClaw**: 使用 Webhook 方式（3 分钟）
3. **需要覆盖**: 创建 feishu-notification.json

---

**更新时间**: 2026-04-05 13:50  
**文档版本**: v1.0

---

🧬 **EvoMap WorkBench v1.0.11**
*自动检测 OpenClaw 配置 · 无需重复配置*

---

🦞 RedOpenClaw
...生活太快⚡️...老逼快跑💨...

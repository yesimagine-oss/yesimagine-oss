# 📢 飞书应用通知使用指南

**创建时间:** 2026-03-16  
**应用 ID:** `cli_a929676f8bf81cc7`  
**通知方式:** 应用 API (非 Webhook)

---

## 🔧 配置说明

### 为什么使用应用 API 而非 Webhook？

| 对比项 | Webhook | 应用 API |
|--------|---------|----------|
| **配置复杂度** | 简单 (只需 URL) | 中等 (需 appId + secret) |
| **权限控制** | 有限 | 完整权限 |
| **消息类型** | 受限 | 全部支持 |
| **发送目标** | 固定群聊 | 任意用户/群聊 |
| **消息管理** | 无法撤回/编辑 | 可撤回/编辑 |
| **推荐使用** | ❌ | ✅ |

### 已配置信息

```json
{
  "method": "app",
  "appId": "cli_a929676f8bf81cc7",
  "useAppSecret": true,
  "webhook": {
    "enabled": false
  },
  "targetUser": "ou_f4919832188bcc630f8f257497fa93a4"
}
```

---

## 📝 发送消息示例

### 方法 1: 使用飞书插件 (推荐)

```bash
# 通过 OpenClaw message 工具发送
# 在会话中直接调用 feishu 插件
```

### 方法 2: 使用 Python 脚本

```python
#!/usr/bin/env python3
import requests
import json

# 获取 Access Token
def get_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": app_id,
        "app_secret": app_secret
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    return response.json().get('tenant_access_token')

# 发送消息
def send_message(access_token, user_id, msg_type, content):
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "receive_id": user_id,
        "msg_type": msg_type,
        "content": json.dumps(content)
    })
    params = {'receive_id_type': 'open_id'}
    response = requests.post(url, headers=headers, params=params, data=payload)
    return response.json()

# 使用示例
app_id = "cli_a929676f8bf81cc7"
app_secret = "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"
user_id = "ou_f4919832188bcc630f8f257497fa93a4"

token = get_access_token(app_id, app_secret)

# 发送文本消息
content = {
    "title": "🐍 Python 学习任务启动",
    "text": "学习网站：https://www.python.org\n启动时间：2026-03-16 12:50\n请开始学习..."
}
result = send_message(token, user_id, "post", content)
print(result)
```

### 方法 3: 使用 curl

```bash
# 1. 获取 Access Token
TOKEN=$(curl -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "cli_a929676f8bf81cc7",
    "app_secret": "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs"
  }' | jq -r '.tenant_access_token')

# 2. 发送消息
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_f4919832188bcc630f8f257497fa93a4",
    "msg_type": "post",
    "content": {
      "title": "🐍 Python 学习任务启动",
      "text": "学习网站：https://www.python.org\n启动时间：2026-03-16 12:50"
    }
  }'
```

---

## 📋 Python 学习通知模板

### 学习开始通知

```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "🐍 Python 学习任务启动",
        "content": [
          [
            {"tag": "text", "text": "学习网站：https://www.python.org\n"},
            {"tag": "text", "text": "启动时间：YYYY-MM-DD HH:MM\n"},
            {"tag": "text", "text": "学习目标：全站内容深入学习\n"}
          ],
          [
            {"tag": "text", "text": "\n✅ 飞书通知已启用\n"},
            {"tag": "text", "text": "📢 学习任务开始/结束/问题都会通知\n"}
          ]
        ]
      }
    }
  }
}
```

### 学习完成通知

```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "🐍 Python 学习任务完成",
        "content": [
          [
            {"tag": "text", "text": "学习阶段：阶段 1 - Python 基础\n"},
            {"tag": "text", "text": "完成时间：YYYY-MM-DD HH:MM\n"},
            {"tag": "text", "text": "学习时长：X 小时\n"}
          ],
          [
            {"tag": "text", "text": "\n学习成效:\n✅ 掌握知识点 X 个\n"},
            {"tag": "text", "text": "✅ 代码示例 X 个\n"},
            {"tag": "text", "text": "✅ 学习笔记 X 篇\n"}
          ]
        ]
      }
    }
  }
}
```

### 问题通知

```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "🐍 Python 学习遇到问题",
        "content": [
          [
            {"tag": "text", "text": "问题描述：XXX\n"},
            {"tag": "text", "text": "卡住位置：XXX\n"},
            {"tag": "text", "text": "需要帮助：XXX\n"}
          ],
          [
            {"tag": "text", "text": "\n解决方案建议：XXX\n"}
          ]
        ]
      }
    }
  }
}
```

---

## 🔐 安全注意事项

### 保护 App Secret

```bash
# ❌ 不要将 secret 提交到 git
# ❌ 不要在日志中打印 secret
# ✅ 使用环境变量存储 secret
# ✅ 使用 OpenClaw credentials 管理 secret
```

### 权限最小化

当前应用已授予的权限：
- ✅ `im:message:send_as_bot` — 发送消息
- ✅ `im:chat` — 访问会话
- ✅ `contact:contact.base:readonly` — 读取联系人

---

## 📊 配置验证

### 测试连接

```bash
# 运行测试脚本
python3 test-feishu-notification.py
```

### 预期响应

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "message_id": "om_xxxxxxxxxxxxxxxx"
  }
}
```

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `~/.openclaw/workspace/.config/feishu-notification.json` | 通知配置 |
| `~/.openclaw/openclaw.json` | OpenClaw 主配置 (含 appId/secret) |
| `~/workspace/python-learning-plan.md` | Python 学习计划 |

---

**配置完成时间:** 2026-03-16 12:50 GMT+8  
**配置者:** OpenClaw Assistant

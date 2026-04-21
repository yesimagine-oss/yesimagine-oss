# 飞书消息格式规范

**版本**: 1.0  
**时间**: 2026-03-23  
**状态**: ✅ 已配置

---

## 🎯 @提及的正确格式

### 飞书 API 格式

**使用 `open_apis` 发送消息时：**

```json
{
  "receive_id": "CHAT_ID",
  "msg_type": "text",
  "content": {
    "text": "@老胡 在的，需要什么帮助？"
  },
  "mentions": [
    {
      "id_type": "user_id",
      "user_id": "ou_f4919832188bcc630f8f257497fa93a4"
    }
  ]
}
```

**或使用 `open_id` 格式：**

```json
{
  "receive_id": "CHAT_ID",
  "msg_type": "text",
  "content": {
    "text": "<at user_id='ou_f4919832188bcc630f8f257497fa93a4'>老胡</at> 在的，需要什么帮助？"
  }
}
```

---

## 📋 人员 ID 对照

| 名字 | open_id | 用途 |
|------|---------|------|
| **老胡/Red** | `ou_f4919832188bcc630f8f257497fa93a4` | @提及 |
| **用户 085997** | `ou_eef0ad5153ebfded65dcf7c3f23bcea1` | @提及 |
| **机械师** | `ou_345140eb75cc30a64d9ffda3f01cdc51` | @提及 |

---

## 🛡️ 隐私保护

### ✅ 允许的做法

| 场景 | 做法 |
|------|------|
| **API 调用中使用 user_id** | 在 mentions 参数中使用 |
| **显示蓝色提及** | 飞书自动渲染 |
| **用户收到通知** | 飞书自动推送 |

### ❌ 禁止的做法

| 场景 | 错误示例 | 正确做法 |
|------|---------|---------|
| **纯文本@** | `@用户 085997` | 使用 mentions 参数 |
| **暴露用户 ID** | `ou_eef0ad5153ebfded65dcf7c3f23bcea1` | 不显示在消息中 |
| **手动写@代码** | `<at id="xxx">` | 使用飞书 API |

---

## 🔧 OpenClaw 配置

**在 openclaw.json 中：**

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "default": {
          "appId": "cli_a929676f8bf81cc7",
          "appSecret": "xzvRRnKnFhAP4VbEhiBABx0YbNrlgzZs",
          "domain": "feishu",
          "enabled": true,
          "streaming": true,
          "renderMode": "auto",
          "requireMention": false,
          "groupPolicy": "open",
          "enableMentions": true,
          "mentionType": "user_id"
        }
      }
    }
  }
}
```

---

## 🧪 测试方法

**在飞书群里：**

1. **@机器人**
   ```
   @RedOpenClaw 测试
   ```

2. **看机器人回复**
   - ✅ 蓝色@提及
   - ✅ 用户收到通知
   - ✅ 点击提及跳转到用户主页
   - ❌ 不应该是纯文本 `@用户 xxx`

---

## ⚠️ 常见问题

### Q1: 显示纯文本@用户

**原因：** 没有使用 mentions 参数

**解决：** 修改消息发送代码，添加 mentions 参数

---

### Q2: 用户没收到通知

**原因：** mentions 参数格式错误

**解决：** 检查 user_id 是否正确，使用 open_id 格式

---

**最后更新**: 2026-03-23  
**维护者**: RedOpenClaw

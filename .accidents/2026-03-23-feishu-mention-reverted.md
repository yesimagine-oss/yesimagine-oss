# 飞书@提及配置回滚

**时间**: 2026-03-23 23:09  
**决策**: 用户同意使用默认回复方式

---

## ✅ 已回滚的配置

**修改 openclaw.json：**

**移除：**
```json
"enableMentions": true,
"mentionType": "user_id"
```

**恢复为默认配置：**
```json
{
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
        "groupPolicy": "open"
      }
    }
  }
}
```

---

## 📋 机器人回复规范

### 默认回复方式

**机器人回复时：**
- ✅ 直接回复内容
- ✅ 飞书自动通知发消息的用户
- ❌ 不写 `@用户 xxx`（纯文本，暴露 ID）
- ❌ 不使用 mentions 参数

### 示例

**用户发消息：**
```
@RedOpenClaw 测试
```

**机器人回复：**
```
✅ 在的，有什么需要帮忙的？
```

**效果：**
- ✅ 用户收到通知
- ✅ 不暴露用户 ID
- ✅ 简洁明了

---

## 🎯 核心原则（更新）

**原第 3 条：**
```
3. @提及用户 - 使用飞书 API mentions 参数
```

**更新为：**
```
3. replyTo 回复 - 回复用户消息，飞书自动通知
```

---

## 📝 相关文档

| 文件 | 状态 | 说明 |
|------|------|------|
| **feishu-bot-core-rules.md** | ✅ 有效 | 核心规范 |
| **feishu-message-format.md** | ⚠️ 参考 | 消息格式（暂不使用） |
| **本文件** | ✅ 有效 | 回滚记录 |

---

**状态**: ✅ 已回滚  
**测试**: 使用默认回复方式  
**效果**: 飞书自动通知用户，不暴露 ID

---

**最后更新**: 2026-03-23 23:09  
**维护者**: RedOpenClaw

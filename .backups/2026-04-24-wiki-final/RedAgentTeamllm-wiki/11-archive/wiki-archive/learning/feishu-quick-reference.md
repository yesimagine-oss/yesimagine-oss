---
category: feishu
created_at: '2026-04-14'
tags:
- feishu
- 飞书开发快速参考卡片
- api
title: Feishu Quick Reference
type: general
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# 📋 飞书开发快速参考卡片

**创建时间**: 2026-03-13 16:30 GMT+8  
**版本**: v1.0  
**适用级别**: L1-L3

---

## 🔑 核心配置

### 环境变量

```bash
# .env
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_USER_ID=ou_xxxxxxxxxxxxxxxx
```

### 获取 Token

```python
POST https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal

{
  "app_id": "cli_xxx",
  "app_secret": "xxx"
}

# 有效期：2 小时
```

---

## 📤 消息发送

### 文本消息

```python
POST /open-apis/im/v1/messages?receive_id_type=user_id

{
  "receive_id": "ou_xxx",
  "msg_type": "text",
  "content": "{\"text\":\"Hello\"}"
}
```

### 富文本消息

```python
{
  "msg_type": "post",
  "content": {
    "zh_cn": {
      "title": "标题",
      "content": [
        [
          {"tag": "text", "text": "你好，"},
          {"tag": "a", "text": "点击", "href": "https://xxx"}
        ]
      ]
    }
  }
}
```

### 卡片消息

```python
{
  "msg_type": "interactive",
  "content": {
    "config": {"wide_screen_mode": True},
    "header": {
      "template": "#3370ff",
      "title": {"tag": "plain_text", "content": "标题"}
    },
    "elements": [
      {
        "tag": "div",
        "text": {"tag": "lark_md", "content": "内容"}
      }
    ]
  }
}
```

---

## 👥 用户查询

### 单个用户

```python
GET /open-apis/contact/v3/users/{user_id}?user_id_type=user_id
```

### 批量用户

```python
POST /open-apis/contact/v3/users/batch

{
  "user_ids": ["ou_xxx1", "ou_xxx2"]
}
```

---

## 📅 日历管理

### 创建事件

```python
POST /open-apis/calendar/v4/calendars/{calendar_id}/events

{
  "summary": "会议标题",
  "start_time": {
    "timestamp": "1709452800",
    "time_zone": "Asia/Shanghai"
  },
  "end_time": {
    "timestamp": "1709456400",
    "time_zone": "Asia/Shanghai"
  }
}
```

### 查询事件

```python
GET /open-apis/calendar/v4/calendars/{calendar_id}/events
?time_min=1709452800
&time_max=1709539200
&max_results=50
```

---

## 📄 云文档

### 创建文档

```python
POST /open-apis/drive/v1/files

{
  "folder_token": "bxxx",
  "title": "文档标题",
  "type": "docx"
}
```

### 获取文档信息

```python
GET /open-apis/drive/v1/files/{file_token}
```

---

## 🤖 机器人

### Webhook 发送

```python
POST https://open.feishu.cn/open-apis/bot/v2/hook/xxx

{
  "msg_type": "text",
  "content": {"text": "Hello"}
}
```

### 事件订阅验证

```python
# 接收挑战
if data['type'] == 'url_verification':
  return {'challenge': data['challenge']}
```

---

## ⚠️ 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 0 | 成功 | - |
| 99991663 | Token 无效 | 重新获取 Token |
| 99991665 | 没有权限 | 检查应用权限 |
| 99991666 | 参数错误 | 检查请求参数 |
| 99991667 | 频率超限 | 降低请求频率 |
| 99991668 | 资源不存在 | 检查资源 ID |

---

## 🔐 安全最佳实践

### Token 管理

```python
# ✅ 正确：动态获取并缓存
class TokenManager:
    def get_token(self):
        if time.time() >= self.expire_time:
            self.refresh_token()
        return self.token
```

### 签名验证

```python
# 验证事件签名
def verify_signature(body, timestamp, nonce, signature, secret):
    data = timestamp + nonce + secret
    expected = base64.b64encode(
        hashlib.sha256(data.encode()).digest()
    ).decode()
    return signature == expected
```

---

## ⚡ 性能优化

### 批量操作

```python
# ✅ 批量请求（1 次）
users = client.batch_get_users(user_ids)

# ❌ 逐个请求（N 次）
for uid in user_ids:
    client.get_user_info(uid)
```

### 请求限流

```python
class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window = window_seconds
    
    def acquire(self):
        # 实现限流逻辑
        pass
```

---

## 📊 API 限流

| API 类型 | 限制 |
|---------|------|
| 普通 API | 100 次/分钟 |
| 消息 API | 根据应用等级 |
| 批量 API | 10 次/分钟 |

---

## 🛠️ 开发工具

### SDK 安装

```bash
pip install feishu-sdk
pip install requests python-dotenv
```

### 调试工具

```bash
# Postman
# - 导入 API Collection
# - 配置环境变量
# - 逐个测试 API
```

---

## 📝 项目模板

### 通知机器人

```
feishu-notification-bot/
├── config.py
├── bot.py
├── message_sender.py
├── templates.py
├── scheduler.py
├── requirements.txt
└── .env
```

### 会议助手

```
feishu-meeting-assistant/
├── config.py
├── main.py
├── calendar_manager.py
├── notification.py
├── requirements.txt
└── .env
```

---

## 🔗 重要链接

| 资源 | 链接 |
|------|------|
| 开放平台 | https://open.feishu.cn/ |
| API 文档 | https://open.feishu.cn/document |
| 开发者社区 | 飞书开发者社区 |
| GitHub | GitHub 官方仓库 |

---

## 📞 获取帮助

```
1. 查阅官方文档
2. 搜索类似问题
3. 开发者社区提问
4. 查看 FAQ 文档
```

---

**卡片版本**: v1.0  
**最后更新**: 2026-03-13  
**适用级别**: L1-L3

📋 **飞书开发快速参考卡片已创建！包含所有核心 API 和最佳实践！**

## 參考

- [[Feishu Evolution 20260413]]


## 相關文檔

- [[feishu-evolution-20260413]]
- [[feishu-merged-learning-report]]
- [[04-feishu_docs_block_parse]]

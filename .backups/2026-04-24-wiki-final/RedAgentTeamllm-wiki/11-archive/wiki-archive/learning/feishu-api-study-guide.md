---
category: feishu
created_at: '2026-04-14'
tags:
- feishu
- 飞书
- api
- 系统化学习指南
- guide
title: Feishu Api Study Guide
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
# 📖 飞书 API 系统化学习指南

**创建时间**: 2026-03-13 15:30 GMT+8  
**学习阶段**: 阶段 1 - 入门学习深入  
**文档版本**: v1.0  
**预计学习时长**: 6-12 个月

---

## 📋 学习进度更新

```
飞书开发者学习计划
═══════════════════════════════════════
总任务：5 个核心链接 + 系统学习
已完成：2/5 (40%)
进行中：1/5
未开始：2/5
进度：40% ↑

当前阶段：阶段 1 - 入门学习深入
阶段进度：30% ↑
═══════════════════════════════════════
```

---

## 🎯 飞书开放平台完整知识体系

### 1. 平台架构

```
飞书开放平台
├── 应用开发
│   ├── 企业内部应用
│   ├── 第三方应用
│   └── 小程序
├── API 能力
│   ├── 消息与推送
│   ├── 用户与组织
│   ├── 日历与会议
│   ├── 云文档
│   ├── 审批流程
│   ├── 即时通讯
│   └── 其他能力
├── 机器人开发
│   ├── 群机器人
│   ├── 应用机器人
│   └── 事件订阅
└── 开发工具
    ├── 开发者后台
    ├── API 调试工具
    ├── SDK
    └── CLI 工具
```

---

### 2. 认证与授权体系

#### App Access Token（应用级）

```
用途：访问应用自身资源
获取方式：POST https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal
请求参数:
{
  "app_id": "cli_a0xxxxxxxx",
  "app_secret": "xxxxxxxx"
}
有效期：2 小时
使用场景:
- 发送应用消息
- 查询应用信息
- 管理应用资源
```

#### User Access Token（用户级）

```
用途：代表用户访问资源
获取方式：OAuth 2.0 授权流程
有效期：根据配置（默认 1 小时）
使用场景:
- 访问用户日历
- 管理用户文档
- 代表用户操作
```

#### Tenant Access Token（租户级）

```
用途：访问企业租户资源
获取方式：通过企业授权
有效期：根据配置
使用场景:
- 企业管理员操作
- 批量用户管理
- 企业数据同步
```

---

### 3. 核心 API 详解

#### 3.1 消息发送 API

**发送消息**
```
POST /open-apis/im/v1/messages

请求头:
Authorization: Bearer {app_access_token}
Content-Type: application/json

请求体:
{
  "receive_id": "user_id",
  "msg_type": "text",
  "content": "{\"text\":\"Hello World\"}"
}

响应:
{
  "code": 0,
  "msg": "success",
  "data": {
    "message_id": "oc_xxxxxxxx"
  }
}
```

**消息类型**:
| 类型 | msg_type | 说明 | 使用场景 |
|------|---------|------|---------|
| 文本 | text | 纯文本消息 | 简单通知 |
| 富文本 | post | 富文本格式 | 格式化内容 |
| 图文 | share_chat | 分享卡片 | 链接分享 |
| 交互式 | interactive | 可交互卡片 | 按钮/表单 |

**消息卡片示例**:
```json
{
  "config": {
    "wide_screen_mode": true
  },
  "header": {
    "title": {
      "tag": "plain_text",
      "content": "通知标题"
    }
  },
  "elements": [
    {
      "tag": "div",
      "text": {
        "tag": "lark_md",
        "content": "**重要**: 会议即将开始"
      }
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "确认参加"
          },
          "type": "primary"
        }
      ]
    }
  ]
}
```

---

#### 3.2 机器人 API

**机器人类型**:
| 类型 | 说明 | 适用场景 |
|------|------|---------|
| 群机器人 | 添加到群聊 | 群通知/自动化 |
| 应用机器人 | 独立应用 | 复杂交互 |
| 事件订阅机器人 | 监听事件 | 自动化流程 |

**群机器人配置**:
```
1. 创建群机器人
   - 飞书群 → 群设置 → 机器人 → 添加机器人

2. 获取 Webhook URL
   - https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx

3. 发送消息
   POST {webhook_url}
   {
     "msg_type": "text",
     "content": {
       "text": "Hello World"
     }
   }
```

**事件订阅配置**:
```
1. 创建应用
   - 开发者后台 → 创建应用

2. 配置事件订阅
   - 添加需要订阅的事件
   - 配置验证 URL

3. 实现事件处理
   - 接收事件推送
   - 验证签名
   - 处理事件逻辑
```

---

#### 3.3 日历 API

**创建日历事件**:
```
POST /open-apis/calendar/v4/calendars/{calendar_id}/events

请求体:
{
  "summary": "会议标题",
  "description": "会议描述",
  "start_time": {
    "timestamp": "1709452800",
    "time_zone": "Asia/Shanghai"
  },
  "end_time": {
    "timestamp": "1709456400",
    "time_zone": "Asia/Shanghai"
  },
  "attendees": [
    {
      "user_id": "ou_xxxxxxxx",
      "type": "user"
    }
  ]
}
```

**查询日历事件**:
```
GET /open-apis/calendar/v4/calendars/{calendar_id}/events

参数:
- time_min: 开始时间
- time_max: 结束时间
- max_results: 返回数量
```

---

#### 3.4 云文档 API

**创建文档**:
```
POST /open-apis/drive/v1/files

请求体:
{
  "folder_token": "xxxxxxxx",
  "title": "文档标题",
  "type": "docx"
}
```

**文档内容操作**:
```
GET /open-apis/drive/v1/files/{file_id}
PUT /open-apis/drive/v1/files/{file_id}
DELETE /open-apis/drive/v1/files/{file_id}
```

**文档权限管理**:
```
POST /open-apis/drive/v1/permissions

请求体:
{
  "file_id": "xxxxxxxx",
  "member": {
    "type": "user",
    "user_id": "ou_xxxxxxxx"
  },
  "role": "editor"
}
```

---

#### 3.5 用户与组织 API

**查询用户信息**:
```
GET /open-apis/contact/v3/users/{user_id}

参数:
- user_id_type: open_id / union_id / user_id
- user_id: 用户 ID
```

**查询部门信息**:
```
GET /open-apis/contact/v3/departments/{department_id}
```

**批量查询用户**:
```
POST /open-apis/contact/v3/users/batch

请求体:
{
  "user_ids": ["ou_xxxxxxxx1", "ou_xxxxxxxx2"]
}
```

---

#### 3.6 审批流 API

**创建审批实例**:
```
POST /open-apis/approval/v4/instances

请求体:
{
  "app_code": "xxxxxxxx",
  "form": {
    "field_xxxxx": "value"
  }
}
```

**查询审批实例**:
```
GET /open-apis/approval/v4/instances/{instance_code}
```

**审批操作**:
```
POST /open-apis/approval/v4/tasks/{task_id}/approve
POST /open-apis/approval/v4/tasks/{task_id}/reject
```

---

### 4. 开发工具链

#### SDK 安装

**Python SDK**:
```bash
pip install feishu-sdk
```

**使用示例**:
```python
from feishu.v1 import Client

cli = Client(app_id="cli_xxxx", app_secret="xxxx")

# 发送消息
result = cli.im.message.create(
    receive_id="user_id",
    msg_type="text",
    content='{"text":"Hello"}'
)
```

#### API 调试工具

**Postman 配置**:
```
1. 创建 Collection
2. 配置环境变量
   - app_id
   - app_secret
   - access_token
3. 添加 Pre-request Script
   - 自动获取 token
4. 测试 API
```

#### CLI 工具

**安装**:
```bash
npm install -g @oapi/cli
```

**使用**:
```bash
# 登录
oapi login

# 创建应用
oapi app create

# 发送消息
oapi message send --to user_id --text "Hello"
```

---

### 5. 错误处理

#### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 0 | 成功 | - |
| 99991663 | app_access_token 无效 | 重新获取 token |
| 99991665 | 没有权限 | 检查应用权限配置 |
| 99991666 | 参数错误 | 检查请求参数 |
| 99991667 | 频率超限 | 降低请求频率 |
| 99991668 | 资源不存在 | 检查资源 ID |

#### 错误处理最佳实践

```python
import requests
from requests.exceptions import RequestException

def call_feishu_api(url, data, token):
    try:
        response = requests.post(
            url,
            json=data,
            headers={"Authorization": f"Bearer {token}"}
        )
        result = response.json()
        
        if result.get("code") != 0:
            # 处理业务错误
            error_code = result.get("code")
            error_msg = result.get("msg")
            handle_error(error_code, error_msg)
            return None
        
        return result.get("data")
    
    except RequestException as e:
        # 处理网络错误
        log_error(f"Network error: {e}")
        return None
    
    except Exception as e:
        # 处理其他异常
        log_error(f"Unexpected error: {e}")
        return None
```

---

### 6. 安全最佳实践

#### Token 管理

```python
# 错误做法：硬编码 token
token = "固定 token"

# 正确做法：动态获取并缓存
class TokenManager:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.token = None
        self.expire_time = 0
    
    def get_token(self):
        if time.time() >= self.expire_time:
            self.refresh_token()
        return self.token
    
    def refresh_token(self):
        # 获取新 token
        response = requests.post(
            "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
            json={
                "app_id": self.app_id,
                "app_secret": self.app_secret
            }
        )
        result = response.json()
        self.token = result["app_access_token"]
        self.expire_time = time.time() + 7200  # 2 小时
```

#### 签名验证

```python
import hashlib
import base64

def verify_signature(body, timestamp, nonce, signature, secret):
    # 计算签名
    data = timestamp + nonce + secret
    expected_signature = base64.b64encode(
        hashlib.sha256(data.encode()).digest()
    ).decode()
    
    return signature == expected_signature
```

#### 权限最小化

```
原则：只申请需要的权限

应用权限配置:
✅ 消息发送权限 (im:message)
✅ 用户读取权限 (contact:user:readonly)
❌ 不必要的写入权限
❌ 不必要的管理权限
```

---

### 7. 性能优化

#### 请求频率控制

```python
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests = []
    
    def acquire(self):
        now = datetime.now()
        # 清理过期请求
        self.requests = [
            req for req in self.requests
            if now - req < self.window
        ]
        
        if len(self.requests) >= self.max_requests:
            # 等待
            wait_time = self.window - (now - self.requests[0])
            time.sleep(wait_time.total_seconds())
        
        self.requests.append(now)
```

#### 批量操作

```python
# 错误做法：逐个请求
for user_id in user_ids:
    get_user_info(user_id)  # N 次请求

# 正确做法：批量请求
batch_get_user_info(user_ids)  # 1 次请求
```

#### 缓存策略

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_user_info_cached(user_id):
    return get_user_info(user_id)
```

---

### 8. 实战项目

#### 项目 1: 通知机器人

**功能**:
```
- 定时发送通知
- 支持多种消息类型
- 消息模板管理
- 发送记录追踪
```

**技术实现**:
```python
class NotificationBot:
    def __init__(self, app_id, app_secret):
        self.client = Client(app_id, app_secret)
    
    def send_text(self, user_id, text):
        self.client.im.message.create(
            receive_id=user_id,
            msg_type="text",
            content=json.dumps({"text": text})
        )
    
    def send_card(self, user_id, card_content):
        self.client.im.message.create(
            receive_id=user_id,
            msg_type="interactive",
            content=json.dumps(card_content)
        )
```

#### 项目 2: 会议助手

**功能**:
```
- 会议自动创建
- 会议提醒
- 会议纪要生成
- 会议录制管理
```

#### 项目 3: 文档管理工具

**功能**:
```
- 文档批量创建
- 文档内容同步
- 权限批量管理
- 文档搜索
```

---

### 9. 学习路线图

#### Week 1-2: 基础入门

```
□ 注册开发者账号
□ 创建第一个应用
□ 学习消息 API
□ 创建群机器人
□ 发送第一条消息
```

#### Week 3-4: 核心 API

```
□ 消息卡片设计
□ 事件订阅配置
□ 日历 API 使用
□ 用户 API 使用
```

#### Month 2: 高级集成

```
□ 云文档 API
□ 审批流 API
□ OAuth 2.0 认证
□ 复杂业务逻辑
```

#### Month 3-6: 实战项目

```
□ 企业通知系统
□ 会议管理工具
□ 文档管理平台
□ 多系统集成
```

#### Month 6-12: 专家级

```
□ 架构设计
□ 性能优化
□ 安全加固
□ 社区贡献
```

---

### 10. 学习资源

#### 官方文档

| 资源 | 链接 | 说明 |
|------|------|------|
| **开放平台** | https://open.feishu.cn/ | 开发者入口 |
| **API 文档** | https://open.feishu.cn/document | 完整 API 参考 |
| **开发者社区** | 飞书开发者社区 | 问题交流 |
| **GitHub** | GitHub 官方仓库 | 示例代码 |

#### 学习技巧

```
1. 从简单开始
   - 先学习消息 API
   - 再学习复杂 API

2. 实践驱动
   - 边学边做项目
   - 每个 API 都写测试代码

3. 记录笔记
   - API 使用笔记
   - 遇到的问题及解决

4. 参与社区
   - 提问和回答
   - 分享经验
```

---

**文档创建时间**: 2026-03-13 15:30 GMT+8  
**文档版本**: v1.0  
**下次更新**: 完成阶段 1 学习后

📖 **飞书 API 系统化学习指南已创建！包含完整的知识体系和学习路线！**

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[api_batch_optimize]]
- [[serper-api-config]]
- [[INSTALL-VALIDATOR-GUIDE]]

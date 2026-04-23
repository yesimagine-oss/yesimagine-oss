# ❓ 飞书开发常见问题 FAQ

**创建时间**: 2026-03-13 16:00 GMT+8  
**文档版本**: v1.0  
**问题数量**: 20+ 常见问题

---

## 📋 学习进度更新

```
飞书开发者学习计划
═══════════════════════════════════════
总任务：5 个核心链接 + 系统学习
已完成：3/5 (60%)
进行中：2/5
未开始：0/5
进度：60% → 70% ↑

当前阶段：阶段 1 - 实战项目准备
阶段进度：65% → 70%
═══════════════════════════════════════
```

---

## 🔧 环境配置问题

### Q1: 如何获取飞书 App ID 和 App Secret？

**A**: 
```
1. 访问 https://open.feishu.cn/
2. 注册/登录开发者账号
3. 进入"开发者后台"
4. 点击"创建应用"
5. 填写应用信息
6. 在"凭证管理"中查看 App ID 和 App Secret
```

**注意事项**:
```
⚠️ App Secret 只显示一次，请妥善保存
⚠️ 不要将 App Secret 提交到代码仓库
⚠️ 使用环境变量管理敏感信息
```

---

### Q2: 如何申请企业试用账号？

**A**:
```
1. 访问 https://www.feishu.cn/
2. 点击"免费注册"
3. 选择"企业版"
4. 填写企业信息
5. 获得 14 天免费试用
```

**个人学习建议**:
```
✅ 使用个人账号学习基础 API
✅ 申请企业试用学习企业级 API
✅ 重点学习消息/机器人等通用 API
```

---

### Q3: Token 获取失败怎么办？

**错误信息**:
```
{"code": 99991663, "msg": "invalid app_access_token"}
```

**解决方案**:
```python
# 1. 检查 App ID 和 App Secret 是否正确
print(f"App ID: {app_id}")
print(f"App Secret: {app_secret[:10]}...")

# 2. 检查网络是否通畅
import requests
try:
    requests.get("https://open.feishu.cn", timeout=5)
except:
    print("网络连接失败")

# 3. 检查请求格式
payload = {
    "app_id": app_id,
    "app_secret": app_secret
}
# 确保使用 JSON 格式

# 4. 使用 Token 管理器（推荐）
from feishu_api_examples import FeishuTokenManager
token_manager = FeishuTokenManager(app_id, app_secret)
token = token_manager.get_app_access_token()
```

---

## 📤 消息发送问题

### Q4: 消息发送失败，错误码 99991665？

**错误含义**: 没有权限

**解决方案**:
```
1. 检查应用权限配置
   - 开发者后台 → 应用权限
   - 添加"发送消息"权限
   - 提交审核（如需）

2. 检查接收者 ID 类型
   - user_id: 企业内部用户
   - open_id: 开放用户
   - chat_id: 群聊 ID

3. 检查 Token 类型
   - 应用 Token: 只能发送给应用可见用户
   - 用户 Token: 可以代表用户发送
```

---

### Q5: 如何发送富文本消息？

**A**:
```python
# 富文本内容格式
content = [
    [
        {"tag": "text", "text": "你好，"},
        {"tag": "a", "text": "点击这里", "href": "https://example.com"},
        {"tag": "text", "text": "查看详情"}
    ],
    [
        {"tag": "text", "text": "**加粗文本**"}
    ],
    [
        {"tag": "text", "text": "换行了"}
    ]
]

# 发送
client.send_post_message(user_id, content)
```

**支持的标签**:
```
- text: 普通文本
- a: 链接
- at: @用户
- img: 图片
- media: 媒体
```

---

### Q6: 如何发送卡片消息？

**A**:
```python
from feishu_api_examples import CardBuilder

# 使用卡片构建器
card = CardBuilder.build_notification_card(
    title="通知标题",
    content="通知内容",
    level="info"  # info/warning/error/success
)

client.send_interactive_card(user_id, card)
```

**卡片元素**:
```
- header: 卡片头部
- elements: 卡片内容
  - div: 文本块
  - action: 按钮组
  - markdown: Markdown 内容
  - img: 图片
```

---

## 👥 用户管理问题

### Q7: 如何获取用户 ID？

**A**:
```python
# 方法 1: 通过手机号
user = client.get_user_info_by_phone("+8613800000000")

# 方法 2: 通过邮箱
user = client.get_user_info_by_email("user@example.com")

# 方法 3: 通过 open_id
user = client.get_user_info(open_id, id_type="open_id")

# 方法 4: 批量获取
users = client.batch_get_users([user_id1, user_id2])
```

**ID 类型说明**:
```
- user_id: 企业内唯一
- open_id: 应用内唯一
- union_id: 开放平台唯一
```

---

### Q8: 如何获取部门列表？

**A**:
```python
# 获取部门列表
def get_departments():
    url = "https://open.feishu.cn/open-apis/contact/v3/departments"
    params = {
        "page_size": 100,
        "page_token": ""
    }
    
    result = client._request("GET", url, params=params)
    return result["data"]["items"]

# 获取部门下用户
def get_department_users(department_id: str):
    url = f"https://open.feishu.cn/open-apis/contact/v3/departments/{department_id}/users"
    result = client._request("GET", url)
    return result["data"]["items"]
```

---

## 📅 日历管理问题

### Q9: 如何创建日历事件？

**A**:
```python
# 创建事件
event_id = client.create_calendar_event(
    calendar_id="calendar_id",
    summary="会议标题",
    start_time=int(time.time()) + 3600,  # 1 小时后
    end_time=int(time.time()) + 7200,    # 2 小时后
    attendees=["user_id1", "user_id2"]
)

# 添加会议描述
description = """
会议议程:
1. 项目进度汇报
2. 问题讨论
3. 下一步计划
"""
```

**注意事项**:
```
⚠️ 时间戳单位是秒
⚠️ 时区设置为 Asia/Shanghai
⚠️ 参会人需要是有效用户 ID
```

---

### Q10: 如何查询日历事件？

**A**:
```python
# 查询今天的事件
now = int(time.time())
today_start = now - (now % 86400)
today_end = today_start + 86400

events = client.get_calendar_events(
    calendar_id="calendar_id",
    time_min=today_start,
    time_max=today_end,
    max_results=50
)

for event in events:
    print(f"事件：{event['summary']}")
    print(f"开始：{event['start_time']}")
    print(f"结束：{event['end_time']}")
```

---

## 📄 云文档问题

### Q11: 如何创建云文档？

**A**:
```python
# 创建文档
file_token = client.create_document(
    folder_token="folder_token",
    title="文档标题",
    doc_type="docx"  # docx/sheet/file
)

# 获取文件夹 Token
# 飞书云文档 → 进入文件夹 → URL 中的参数
```

**文件夹 Token 获取**:
```
1. 打开飞书云文档
2. 进入目标文件夹
3. 查看 URL
4. 复制 folder_token 参数
```

---

### Q12: 如何更新文档内容？

**A**:
```python
# 需要使用文档内容 API
# 示例代码结构

def update_document_content(file_token: str, content: str):
    url = f"https://open.feishu.cn/open-apis/drive/v1/files/{file_token}/content"
    payload = {
        "content": content
    }
    client._request("PUT", url, json=payload)
```

**注意**:
```
⚠️ 需要文档编辑权限
⚠️ 内容格式根据文档类型不同
⚠️ 建议使用官方 SDK
```

---

## 🤖 机器人问题

### Q13: 如何创建群机器人？

**A**:
```
1. 打开飞书群聊
2. 群设置 → 机器人
3. 添加机器人 → 自定义机器人
4. 填写机器人信息
5. 获取 Webhook URL
6. 测试发送消息
```

**Webhook 使用**:
```python
import requests

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx"

payload = {
    "msg_type": "text",
    "content": {
        "text": "Hello World"
    }
}

response = requests.post(webhook_url, json=payload)
```

---

### Q14: 如何配置事件订阅？

**A**:
```
1. 开发者后台 → 应用开发 → 事件订阅
2. 开启事件订阅
3. 配置验证 URL
4. 添加需要订阅的事件
5. 实现事件处理接口
```

**验证 URL 实现**:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/feishu/event', methods=['POST'])
def handle_event():
    data = request.json
    
    # 验证挑战
    if data.get('type') == 'url_verification':
        return jsonify({
            'challenge': data['challenge']
        })
    
    # 处理事件
    event = data['event']
    process_event(event)
    
    return jsonify({'success': True})
```

---

## 🔐 安全问题

### Q15: 如何保护 App Secret？

**A**:
```python
# ❌ 错误做法
APP_SECRET = "xxxxxxxx"  # 硬编码

# ✅ 正确做法
import os
from dotenv import load_dotenv

load_dotenv()
APP_SECRET = os.getenv("FEISHU_APP_SECRET")

# ✅ 生产环境使用
# 使用密钥管理服务
# 如阿里云 KMS、腾讯云 KMS 等
```

**最佳实践**:
```
✅ 使用环境变量
✅ 不要提交到 Git
✅ 定期轮换 Secret
✅ 限制 IP 访问
```

---

### Q16: 如何处理签名验证？

**A**:
```python
import hashlib
import base64

def verify_signature(body: str, timestamp: str, nonce: str, 
                    signature: str, secret: str) -> bool:
    """验证飞书签名"""
    # 计算签名
    data = timestamp + nonce + secret
    expected_signature = base64.b64encode(
        hashlib.sha256(data.encode()).digest()
    ).decode()
    
    return signature == expected_signature

# 使用示例
@app.route('/feishu/event', methods=['POST'])
def handle_event():
    signature = request.headers.get('X-Feishu-Signature')
    timestamp = request.headers.get('X-Feishu-Timestamp')
    nonce = request.headers.get('X-Feishu-Nonce')
    body = request.get_data(as_text=True)
    
    if not verify_signature(body, timestamp, nonce, signature, APP_SECRET):
        return jsonify({'error': 'Invalid signature'}), 401
    
    # 处理事件
```

---

## ⚡ 性能问题

### Q17: 如何避免频率限制？

**A**:
```python
# 使用限流器
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
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

# 使用
limiter = RateLimiter(max_requests=100, window_seconds=60)

def send_message():
    limiter.acquire()
    # 发送消息
```

**飞书 API 限流**:
```
- 普通 API: 100 次/分钟
- 消息 API: 根据应用等级
- 批量 API: 10 次/分钟
```

---

### Q18: 如何优化批量操作？

**A**:
```python
# ❌ 错误做法：逐个请求
for user_id in user_ids:
    client.get_user_info(user_id)  # N 次请求

# ✅ 正确做法：批量请求
users = client.batch_get_users(user_ids)  # 1 次请求

# ✅ 使用并发
import asyncio
import aiohttp

async def batch_get_users_async(user_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [get_user(session, uid) for uid in user_ids]
        return await asyncio.gather(*tasks)
```

---

## 🐛 调试问题

### Q19: 如何调试 API 调用？

**A**:
```python
# 1. 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 2. 使用 Postman 测试
# - 导入 API Collection
# - 配置环境变量
# - 逐个测试 API

# 3. 打印请求详情
def debug_request(method, url, **kwargs):
    print(f"Request: {method} {url}")
    print(f"Headers: {kwargs.get('headers', {})}")
    print(f"Body: {kwargs.get('json', {})}")
    
    response = requests.request(method, url, **kwargs)
    
    print(f"Response: {response.status_code}")
    print(f"Body: {response.json()}")
    
    return response
```

---

### Q20: 常见错误码有哪些？

**A**:

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 0 | 成功 | - |
| 99991663 | Token 无效 | 重新获取 Token |
| 99991665 | 没有权限 | 检查应用权限 |
| 99991666 | 参数错误 | 检查请求参数 |
| 99991667 | 频率超限 | 降低请求频率 |
| 99991668 | 资源不存在 | 检查资源 ID |
| 99991669 | 内部错误 | 联系飞书支持 |

---

## 📚 学习资源

### 官方文档

```
- 开放平台：https://open.feishu.cn/
- API 文档：https://open.feishu.cn/document
- 开发者社区：飞书开发者社区
- GitHub: GitHub 官方仓库
```

### 学习建议

```
1. 从简单 API 开始（消息发送）
2. 逐步学习复杂 API
3. 多实践，多写代码
4. 遇到问题先查文档
5. 参与社区讨论
```

---

**文档创建时间**: 2026-03-13 16:00 GMT+8  
**文档版本**: v1.0  
**问题数量**: 20+ 常见问题  
**下次更新**: 遇到新问题时

❓ **飞书开发常见问题 FAQ 已创建！包含 20+ 常见问题的解决方案！**

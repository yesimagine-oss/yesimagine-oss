# 飞书@提及功能指南

## ✅ 功能说明

**用途:** 在飞书消息中正确@用户，避免"张冠李戴"

**功能:**
- ✅ 创建@提及字符串
- ✅ @所有人
- ✅ 解析@提及
- ✅ 格式化飞书消息
- ✅ 创建回复消息
- ✅ 提取用户 ID

---

## 🚀 使用方法

### 1️⃣ 创建@提及

**命令行:**
```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-mention.py create \
  --user-id "ou_xxxxx" \
  --user-name "张三"
```

**输出:**
```
@张三：<at user_id="ou_xxxxx">张三</at>
```

---

### 2️⃣ @所有人

**命令行:**
```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-mention.py create --all
```

**输出:**
```
@所有人：<at user_id="all">所有人</at>
```

---

### 3️⃣ 创建回复消息

**命令行:**
```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-mention.py reply \
  --user-id "ou_xxxxx" \
  --user-name "张三" \
  --content "这个项目是你负责的吗？"
```

**输出:**
```json
{
  "msg_type": "text",
  "content": {
    "text": "<at user_id=\"ou_xxxxx\">张三</at> 这个项目是你负责的吗？"
  }
}
```

---

### 4️⃣ 解析@提及

**命令行:**
```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-mention.py parse \
  --text "<at user_id=\"ou_xxxxx\">张三</at> 你好"
```

**输出:**
```
找到 1 个@提及:
  - 张三 (ou_xxxxx)
```

---

## 💻 Python 集成

### 示例 1：基本@提及

```python
from feishu_mention import FeishuMention

mention = FeishuMention()

# 创建@提及
mention_str = mention.create_mention('ou_xxxxx', '张三')
print(mention_str)
# 输出：<at user_id="ou_xxxxx">张三</at>
```

---

### 示例 2：创建回复消息

```python
from feishu_mention import FeishuMention

mention = FeishuMention()

# 回复张三
reply_to = {
    'user_id': 'ou_xxxxx',
    'user_name': '张三'
}

message = mention.create_reply_message(
    reply_to,
    "这个项目是你负责的吗？"
)

print(json.dumps(message, indent=2, ensure_ascii=False))
# 输出:
# {
#   "msg_type": "text",
#   "content": {
#     "text": "<at user_id=\"ou_xxxxx\">张三</at> 这个项目是你负责的吗？"
#   }
# }
```

---

### 示例 3：@多人

```python
from feishu_mention import FeishuMention

mention = FeishuMention()

# @多人
reply_to = {'user_id': 'ou_xxxxx', 'user_name': '张三'}
additional = [
    {'user_id': 'ou_yyyyy', 'user_name': '李四'},
    {'user_id': 'ou_zzzzz', 'user_name': '王五'}
]

message = mention.create_reply_message(
    reply_to,
    "请三位确认一下这个项目",
    additional_mentions=additional
)

print(message['content']['text'])
# 输出：<at user_id="ou_xxxxx">张三</at> <at user_id="ou_yyyyy">李四</at> <at user_id="ou_zzzzz">王五</at> 请三位确认一下这个项目
```

---

### 示例 4：@所有人

```python
from feishu_mention import FeishuMention

mention = FeishuMention()

# @所有人
mention_all = mention.create_mention_all()
print(mention_all)
# 输出：<at user_id="all">所有人</at>
```

---

### 示例 5：解析@提及

```python
from feishu_mention import FeishuMention

mention = FeishuMention()

text = "<at user_id=\"ou_xxxxx\">张三</at> 你好，<at user_id=\"ou_yyyyy\">李四</at> 在吗？"

mentions = mention.parse_mention(text)
print(f"找到 {len(mentions)} 个@提及:")
for m in mentions:
    print(f"  - {m['user_name']} ({m['user_id']})")

# 输出:
# 找到 2 个@提及:
#   - 张三 (ou_xxxxx)
#   - 李四 (ou_yyyyy)
```

---

### 示例 6：检查是否被@

```python
from feishu_mention import FeishuMention

mention = FeishuMention()

text = "<at user_id=\"ou_xxxxx\">张三</at> 你好"

# 检查张三是否被@
is_mentioned = mention.is_mentioned(text, 'ou_xxxxx')
print(f"张三被@了吗？{is_mentioned}")
# 输出：张三被@了吗？True

# 检查李四是否被@
is_mentioned = mention.is_mentioned(text, 'ou_yyyyy')
print(f"李四被@了吗？{is_mentioned}")
# 输出：李四被@了吗？False
```

---

## 📊 飞书消息格式

### 文本消息

```json
{
  "msg_type": "text",
  "content": {
    "text": "<at user_id=\"ou_xxxxx\">张三</at> 你好"
  }
}
```

### 富文本消息

```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "标题",
        "content": [
          [
            {
              "tag": "at",
              "user_id": "ou_xxxxx",
              "text": "张三"
            },
            {
              "tag": "text",
              "text": " 你好"
            }
          ]
        ]
      }
    }
  }
}
```

---

## 🎯 使用场景

### 场景 1：回复用户

```python
# 用户提问
user_message = {
    'sender_id': 'ou_xxxxx',
    'sender_name': '张三',
    'content': '这个项目怎么做？'
}

# 回复
reply = mention.create_reply_message(
    {'user_id': user_message['sender_id'], 'user_name': user_message['sender_name']},
    "这个项目可以这样做..."
)

# 发送
feishu.send_message(chat_id, reply)
```

---

### 场景 2：任务分配

```python
# @相关负责人
task_assign = mention.create_reply_message(
    {'user_id': 'ou_xxxxx', 'user_name': '张三'},
    "这个项目由你负责，下周五前完成"
)

feishu.send_message(chat_id, task_assign)
```

---

### 场景 3：通知推送

```python
# @所有人
notify = {
    "msg_type": "text",
    "content": {
        "text": f"{mention.create_mention_all()} 明天上午 10 点开会"
    }
}

feishu.send_message(chat_id, notify)
```

---

### 场景 4：多人协作

```python
# @项目组成员
team_members = [
    {'user_id': 'ou_xxxxx', 'user_name': '张三'},
    {'user_id': 'ou_yyyyy', 'user_name': '李四'},
    {'user_id': 'ou_zzzzz', 'user_name': '王五'}
]

message = mention.create_reply_message(
    team_members[0],  # 回复张三
    "请三位确认一下项目进度",
    additional_mentions=team_members[1:]  # @李四和王五
)

feishu.send_message(chat_id, message)
```

---

## ⚠️ 注意事项

### 1. 用户 ID 格式

飞书用户 ID 格式：`ou_xxxxx`

- 必须以 `ou_` 开头
- 后面是字母数字组合

### 2. @语法

**正确:**
```
<at user_id="ou_xxxxx">张三</at>
```

**错误:**
```
@张三  # 这不是飞书@格式
<@ou_xxxxx>  # 这也不是
```

### 3. 权限要求

需要以下权限：
- ✅ `im:message` - 发送消息
- ✅ `im:message:send_as_bot` - 以机器人身份发送

---

## 🔧 集成到消息处理

### 完整流程

```python
from feishu_mention import FeishuMention
from feishu_group_members import GroupMemberManager

# 1. 初始化
mention = FeishuMention()
member_manager = GroupMemberManager()

# 2. 收到消息
incoming_message = {
    'chat_id': 'oc_xxxxx',
    'sender_id': 'ou_xxxxx',
    'sender_name': '张三',
    'content': '@机器人 这个项目谁负责？'
}

# 3. 识别提问者
sender = {
    'user_id': incoming_message['sender_id'],
    'user_name': incoming_message['sender_name']
}

# 4. 处理问题（查找负责人）
# ... 业务逻辑 ...
responsible_person = {
    'user_id': 'ou_yyyyy',
    'user_name': '李四'
}

# 5. 创建回复
reply = mention.create_reply_message(
    sender,  # @提问者
    f"这个项目由 {responsible_person['user_name']} 负责",
    additional_mentions=[responsible_person]  # @负责人
)

# 6. 发送
feishu.send_message(incoming_message['chat_id'], reply)
```

---

## 📋 测试

### 测试用例

| 测试项 | 输入 | 预期输出 | 状态 |
|--------|------|---------|------|
| 创建@提及 | user_id, name | `<at user_id="...">name</at>` | ✅ |
| @所有人 | - | `<at user_id="all">所有人</at>` | ✅ |
| 创建回复 | user, content | 包含@的消息 JSON | ✅ |
| 解析@提及 | 包含@的文本 | 用户列表 | ⏳ |
| 检查@ | text, user_id | True/False | ⏳ |

---

## 📄 相关文件

| 文件 | 位置 | 说明 |
|------|------|------|
| **feishu-mention.py** | `tools/feishu-mention.py` | @提及工具 |
| **feishu-group-members.py** | `tools/feishu-group-members.py` | 群组成员管理 |
| **FEISHU-MENTION-GUIDE.md** | `workspace/` | 使用指南 |

---

**创建时间:** 2026-03-17 20:11  
**状态:** ✅ 已完成

# 飞书群组成员识别指南

## 📋 功能说明

**用途:** 在飞书群组中正确识别成员，避免"张冠李戴"

**功能:**
- ✅ 获取群组成员列表
- ✅ 缓存成员信息（5 分钟）
- ✅ 根据名称查找成员
- ✅ 根据 ID 查找成员
- ✅ 格式化输出（文本/Markdown/JSON）

---

## 🚀 使用方法

### 1️⃣ 获取群组成员

**在飞书群组中:**

```
@机器人 查看群成员
```

**或命令行:**

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-group-members.py show --chat-id "群组 ID"
```

---

### 2️⃣ 查找特定成员

**根据名称查找:**

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-group-members.py find \
  --chat-id "群组 ID" \
  --name "张三"
```

**输出:**
```json
{
  "user_id": "ou_xxxxx",
  "name": "张三",
  "employee_id": "12345",
  "avatar": "https://..."
}
```

---

### 3️⃣ 列出缓存的群组

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-group-members.py list
```

**输出:**
```
缓存的群组:
  - oc_xxxxx: 15 个成员 (更新于 2026-03-17 20:00:00)
  - oc_yyyyy: 8 个成员 (更新于 2026-03-17 19:55:00)
```

---

### 4️⃣ 刷新缓存

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-group-members.py refresh \
  --chat-id "群组 ID"
```

---

### 5️⃣ 清除缓存

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-group-members.py clear
```

---

## 📊 输出格式

### 文本格式（默认）

```
群组成员:
  1. 张三 (ou_xxxxx)
  2. 李四 (ou_yyyyy)
  3. 王五 (ou_zzzzz)
```

### Markdown 格式

```markdown
### 群组成员

1. **张三** (`ou_xxxxx`)
2. **李四** (`ou_yyyyy`)
3. **王五** (`ou_zzzzz`)
```

### JSON 格式

```json
[
  {
    "user_id": "ou_xxxxx",
    "name": "张三",
    "employee_id": "12345"
  },
  ...
]
```

---

## 🔧 集成到对话中

### 场景 1：有人@机器人

**用户:** `@机器人 这个项目谁负责？`

**机器人处理流程:**
```
1️⃣ 获取消息中的 sender_id
   → 识别提问者

2️⃣ 获取群组成员列表
   → 缓存到 feishu-group-members.json

3️⃣ 查找项目负责人（根据上下文）
   → 找到对应成员

4️⃣ 回复并@提问者
   → "<at user_id="提问者 ID">张三</at> 这个项目由李四负责"
```

---

### 场景 2：多人对话

**问题:** 如何区分不同用户的话？

**解决:**
```python
# 记录每条消息的 sender_id
message_history = [
    {
        'sender_id': 'ou_xxxxx',
        'sender_name': '张三',
        'message': '这个项目怎么做？',
        'timestamp': '2026-03-17 20:00:00'
    },
    {
        'sender_id': 'ou_yyyyy',
        'sender_name': '李四',
        'message': '我觉得应该...',
        'timestamp': '2026-03-17 20:01:00'
    }
]

# 回复时正确@用户
"回复 <at user_id="ou_xxxxx">张三</at>: 这个项目可以..."
```

---

## ⚠️ 注意事项

### 1. 缓存过期

- **缓存时间:** 5 分钟
- **过期后:** 自动刷新
- **手动刷新:** `refresh` 命令

### 2. 权限要求

需要以下飞书权限：
- ✅ `im:chat` - 群组信息
- ✅ `im:chat.members:bot_access` - 成员读取

### 3. 群组类型

- ✅ 普通群聊
- ✅ 部门群
- ⚠️ 外部群（可能需要额外权限）

---

## 🛠️ API 集成示例

### Python 示例

```python
from feishu_group_members import GroupMemberManager

# 创建管理器
manager = GroupMemberManager()

# 获取成员
members = manager.get_members('oc_xxxxx')

# 查找成员
member = manager.find_member_by_name('oc_xxxxx', '张三')

# 格式化输出
print(manager.format_members(members, format='markdown'))
```

### 飞书消息格式

```python
# @提及用户
message = {
    "msg_type": "text",
    "content": {
        "text": f"<at user_id=\"{user_id}\">{name}</at> 你好"
    }
}

# 发送消息
feishu_message.send(chat_id, message)
```

---

## 📋 缓存文件位置

| 文件 | 位置 |
|------|------|
| **成员缓存** | `/home/admin/.openclaw/workspace/cache/feishu-group-members.json` |
| **缓存目录** | `/home/admin/.openclaw/workspace/cache/` |

---

## 🔍 调试

### 查看缓存内容

```bash
cat /home/admin/.openclaw/workspace/cache/feishu-group-members.json | python3 -m json.tool
```

### 清除缓存重新测试

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-group-members.py clear
```

---

## 📊 性能优化

### 缓存策略

| 场景 | 缓存时间 | 说明 |
|------|---------|------|
| **活跃群组** | 5 分钟 | 频繁对话的群 |
| **不活跃群** | 30 分钟 | 很少对话的群 |
| **大型群组** | 10 分钟 | 成员变化频繁 |

### 批量获取

- ✅ 首次获取全部成员
- ✅ 缓存到本地
- ✅ 5 分钟内使用缓存
- ✅ 过期后自动刷新

---

## 🎯 使用场景

### ✅ 推荐

| 场景 | 说明 |
|------|------|
| **群组对话** | 识别提问者，正确@ |
| **任务分配** | 查找并@相关人员 |
| **通知推送** | @全体成员或特定人员 |
| **群组成员查询** | 回答"群里有多少人" |

### ❌ 避免

| 场景 | 原因 |
|------|------|
| **超大型群组** | 成员太多，响应慢 |
| **外部群** | 权限可能不足 |
| **临时群** | 缓存意义不大 |

---

## 📞 故障排除

### 问题 1：获取成员失败

**可能原因:**
- 权限不足
- 群组 ID 错误
- 网络问题

**解决:**
```bash
# 检查权限
openclaw feishu app-scopes

# 检查群组 ID
# 从飞书群组 URL 中获取
```

### 问题 2：缓存不更新

**可能原因:**
- 缓存文件权限问题
- 磁盘空间不足

**解决:**
```bash
# 清除缓存
python3 /home/admin/.openclaw/workspace/tools/feishu-group-members.py clear

# 检查磁盘空间
df -h /home/admin/.openclaw/workspace
```

---

## 📝 待办事项

- [ ] 自动识别群组 ID（从消息上下文）
- [ ] 成员变更检测（自动刷新）
- [ ] 成员角色识别（管理员/普通成员）
- [ ] 外部群支持

---

**创建时间:** 2026-03-17  
**最后更新:** 2026-03-17 20:07

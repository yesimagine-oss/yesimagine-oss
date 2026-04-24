---
category: feishu
created_at: '2026-04-14'
tags:
- feishu
- 群组成员识别
- 实现总结
title: Group Members Implementation
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
# 群组成员识别 - 实现总结

## ✅ 已完成

| 项目 | 状态 | 说明 |
|------|------|------|
| **工具创建** | ✅ 完成 | `feishu-group-members.py` |
| **集成脚本** | ✅ 完成 | `feishu-group-integration.py` |
| **缓存机制** | ✅ 完成 | 5 分钟自动过期 |
| **文档** | ✅ 完成 | `FEISHU-GROUP-MEMBERS.md` |
| **权限检查** | ✅ 完成 | 所需权限已授予 |

---

## 📋 工具位置

| 工具 | 位置 | 用途 |
|------|------|------|
| **feishu-group-members.py** | `tools/feishu-group-members.py` | 成员管理（缓存、查找） |
| **feishu-group-integration.py** | `tools/feishu-group-integration.py` | 实际获取成员 |
| **feishu-healthcheck.py** | `tools/feishu-healthcheck.py` | 健康检查 |
| **install-validator.py** | `tools/install-validator.py` | 安装验证 |

---

## 🚀 使用方法

### 在飞书群组中使用

**场景 1：查看群成员**

```
@机器人 查看群成员
```

**机器人响应:**
```
✅ 群组 oc_xxxxx 共有 15 个成员:

  1. 张三 (ou_xxxxx)
  2. 李四 (ou_yyyyy)
  3. 王五 (ou_zzzzz)
  ...
```

---

**场景 2：查找特定成员**

```
@机器人 查找 张三
```

**机器人响应:**
```
找到成员:
  姓名：张三
  用户 ID: ou_xxxxx
  工号：12345
```

---

**场景 3：@提及用户**

```
用户：@机器人 这个项目谁负责？

机器人：@张三 这个项目由你负责，对吗？
```

---

### 命令行使用

#### 1. 获取群成员

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-group-integration.py \
  oc_xxxxx  # 群组 ID
```

#### 2. 保存缓存

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-group-integration.py \
  oc_xxxxx --save
```

#### 3. 查找成员

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-group-members.py \
  find --chat-id oc_xxxxx --name "张三"
```

#### 4. 列出缓存

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-group-members.py \
  list
```

---

## 🔧 集成到对话流程

### 对话上下文管理

**问题:** 如何避免"张冠李戴"？

**解决方案:**

```python
# 1. 记录每条消息的发送者
message_context = {
    'chat_id': 'oc_xxxxx',
    'messages': [
        {
            'sender_id': 'ou_xxxxx',
            'sender_name': '张三',
            'content': '这个项目怎么做？',
            'timestamp': '2026-03-17 20:00:00'
        },
        {
            'sender_id': 'ou_yyyyy',
            'sender_name': '李四',
            'content': '我觉得应该...',
            'timestamp': '2026-03-17 20:01:00'
        }
    ]
}

# 2. 回复时正确@用户
def reply_to_user(sender_id, sender_name, content):
    return f"<at user_id=\"{sender_id}\">{sender_name}</at> {content}"

# 3. 输出
reply_to_user('ou_xxxxx', '张三', '这个项目可以这样做...')
# 输出：@张三 这个项目可以这样做...
```

---

### 避免"胡言乱语"

**问题:** 编造成员信息

**解决方案:**

```python
# 1. 先获取成员列表
members = get_chat_members(chat_id)

# 2. 查找匹配的成员
def find_member(name):
    for member in members:
        if name in member.get('name', ''):
            return member
    return None

# 3. 找不到就说找不到
member = find_member('张三')
if member:
    print(f"找到：{member['name']}")
else:
    print("❌ 未找到成员：张三")  # 不编造
```

---

## 📊 缓存策略

### 缓存文件

**位置:** `/home/admin/.openclaw/workspace/cache/feishu-group-members.json`

**结构:**
```json
{
  "oc_xxxxx": {
    "timestamp": 1710698400,
    "expiry_seconds": 300,
    "members": [
      {
        "user_id": "ou_xxxxx",
        "name": "张三",
        "employee_id": "12345"
      }
    ]
  }
}
```

### 缓存过期

| 时间 | 行为 |
|------|------|
| **0-5 分钟** | 使用缓存 |
| **5 分钟后** | 自动刷新 |
| **手动刷新** | `refresh` 命令 |

---

## ⚠️ 注意事项

### 1. 群组 ID 获取

**从飞书 URL 获取:**
```
https://applink.feishu.cn/client/chat/chatter/add_by_link?link=oc_xxxxx
                                                      ↑↑↑↑↑↑↑
                                                   群组 ID
```

**从消息上下文获取:**
- 飞书消息事件中包含 `chat_id`
- 需要从事件 payload 中提取

### 2. 权限要求

已授予的权限：
- ✅ `im:chat` - 群组信息
- ✅ `im:chat.members:bot_access` - 成员读取

### 3. 成员变化

- 缓存 5 分钟过期
- 成员变动频繁群组可缩短缓存时间
- 重要操作前可手动刷新

---

## 🎯 实际应用场景

### 场景 1：任务分配

```
用户：@机器人 这个项目谁负责？

机器人处理:
1. 获取群组成员
2. 查找项目负责人（根据上下文或关键词）
3. @相关负责人

回复：@张三 这个项目是你负责的吗？
```

---

### 场景 2：通知推送

```
用户：@机器人 通知大家明天开会

机器人处理:
1. 获取群组成员
2. 格式化@所有人
3. 发送通知

回复：@所有人 明天上午 10 点开会...
```

---

### 场景 3：成员查询

```
用户：@机器人 群里有多少人？

机器人处理:
1. 获取群组成员（用缓存）
2. 统计人数
3. 回复

回复：本群共有 15 个成员
```

---

## 📋 测试计划

### 测试用例

| 测试项 | 预期结果 | 状态 |
|--------|---------|------|
| 获取群成员 | 返回成员列表 | ⏳ 待测试 |
| 缓存功能 | 5 分钟内用缓存 | ⏳ 待测试 |
| 查找成员 | 找到/未找到 | ⏳ 待测试 |
| @提及 | 正确@用户 | ⏳ 待测试 |
| 多人对话 | 区分不同用户 | ⏳ 待测试 |

### 测试环境

- ✅ 开发环境：已准备
- ⏳ 测试群组：需要飞书群组
- ⏳ 实际测试：需要在飞书群组中测试

---

## 🔄 下一步

### 立即执行

1. **在飞书群组中测试**
   - 添加机器人到测试群组
   - 测试获取成员功能
   - 测试@提及功能

2. **集成到消息处理**
   - 在收到消息时自动获取 sender_id
   - 在回复时自动@用户

3. **完善错误处理**
   - 权限不足提示
   - 网络错误处理
   - 缓存失效处理

### 中期优化

1. **自动识别群组 ID**
   - 从消息上下文提取
   - 无需手动指定

2. **成员变更检测**
   - 检测成员变化
   - 自动刷新缓存

3. **角色识别**
   - 区分管理员/普通成员
   - 区分内部/外部成员

---

## 📞 故障排除

### 问题 1：获取成员失败

**检查:**
```bash
# 1. 检查权限
openclaw feishu app-scopes

# 2. 检查群组 ID
# 从飞书群组链接获取

# 3. 测试连接
python3 /home/admin/.openclaw/workspace/tools/feishu-group-integration.py oc_xxxxx
```

### 问题 2：缓存不工作

**检查:**
```bash
# 1. 检查缓存目录
ls -la /home/admin/.openclaw/workspace/cache/

# 2. 清除缓存
python3 /home/admin/.openclaw/workspace/tools/feishu-group-members.py clear

# 3. 重新获取
python3 /home/admin/.openclaw/workspace/tools/feishu-group-integration.py oc_xxxxx --save
```

---

## 📊 性能指标

| 指标 | 目标 | 实际 |
|------|------|------|
| **获取成员时间** | <2 秒 | 待测试 |
| **缓存命中率** | >80% | 待测试 |
| **@提及准确率** | 100% | 待测试 |
| **成员识别准确率** | 100% | 待测试 |

---

**创建时间:** 2026-03-17 20:07  
**状态:** ✅ 工具已完成，⏳ 待实际测试

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[FEISHU-GROUP-MEMBERS]]
- [[FEISHU-GROUP-GUIDE]]

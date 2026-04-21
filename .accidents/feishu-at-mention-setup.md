# 飞书@提及配置指南

**版本**: 1.0  
**时间**: 2026-03-23  
**状态**: ✅ 权限已开通，待配置

---

## ✅ 已开通的权限

| 权限 | 说明 | 状态 |
|------|------|------|
| **im:message.send_as_user** | 以用户身份发送消息 | ✅ 已开通 |
| **im:message.group_msg:get_as_user** | 以用户身份获取群聊消息 | ✅ 已开通 |
| **im:message.group_at_msg:readonly** | 接收@机器人消息事件 | ✅ 已开通 |

---

## 🎯 @提及的正确用法

### 飞书 API 支持的方式

**方式 1：使用 mentions 参数（推荐）**

```json
{
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

**方式 2：使用 open_id 格式**

```json
{
  "msg_type": "text",
  "content": {
    "text": "<at user_id='ou_f4919832188bcc630f8f257497fa93a4'>老胡</at> 在的，需要什么帮助？"
  }
}
```

---

## 📋 人员 ID 对照表

| 名字 | 用户 ID (open_id) | 用途 |
|------|------------------|------|
| **老胡/胡宏基** | `ou_f4919832188bcc630f8f257497fa93a4` | @提及 |
| **用户 085997** | `ou_eef0ad5153ebfded65dcf7c3f23bcea1` | @提及 |
| **机械师** | `ou_345140eb75cc30a64d9ffda3f01cdc51` | @提及 |

---

## 🛡️ 隐私保护规则

### ✅ 允许的做法

| 场景 | 做法 |
|------|------|
| **API 调用中使用用户 ID** | ✅ 在 mentions 参数中使用 |
| **显示蓝色提及** | ✅ 飞书自动渲染 |
| **用户收到通知** | ✅ 飞书自动推送 |

### ❌ 禁止的做法

| 场景 | 做法 | 原因 |
|------|------|------|
| **消息文本中暴露 ID** | `ou_f4919832188bcc630f8f257497fa93a4` | 隐私泄露 |
| **手动写@代码** | `<at id="ou_xxx">` | 格式错误 |
| **发送 JSON 给群聊** | `{"msg_type":"text",...}` | 显示为乱码 |

---

## 🔧 配置步骤

### 第 1 步：确认权限生效

**在飞书开放平台：**

1. **访问** https://open.feishu.cn/app
2. **找到你的应用**
3. **查看权限管理**
4. **确认以下权限已开通：**
   - ✅ im:message.send_as_user
   - ✅ im:message.group_msg:get_as_user
   - ✅ im:message.group_at_msg:readonly

---

### 第 2 步：配置机器人

**在飞书群里：**

1. **点击机器人头像**
2. **查看机器人详情**
3. **确认机器人已启用**
4. **重启机器人（如果需要）**

---

### 第 3 步：测试@提及

**在飞书群里：**

1. **@机器人**
   ```
   @RedOpenClaw 测试
   ```

2. **看机器人回复**
   - ✅ 应该显示蓝色@提及
   - ✅ 用户收到通知
   - ✅ 点击提及跳转到用户主页

3. **检查通知**
   - ✅ 飞书推送通知
   - ✅ 通知显示"老胡@了你"

---

## 📝 代码示例

### Python 示例

```python
import requests

url = "https://open.feishu.cn/open-apis/im/v1/messages"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}

data = {
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

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

---

## 🧪 验收标准

测试通过标准：

- [ ] **蓝色提及** - 显示为蓝色可点击链接
- [ ] **用户通知** - 用户收到@通知
- [ ] **点击跳转** - 点击提及跳转到用户主页
- [ ] **不暴露 ID** - 消息中不显示`ou_xxx`
- [ ] **格式正确** - 不显示为代码或乱码

---

## ⚠️ 常见问题

### Q1: 发送后显示为代码

**原因：** 直接发送了 JSON 字符串

**解决：** 使用飞书 API 的 mentions 参数

---

### Q2: 用户没收到通知

**原因：** 权限未生效或配置错误

**解决：** 
1. 检查权限是否开通
2. 重启机器人
3. 检查 mentions 参数格式

---

### Q3: 显示@但不可点击

**原因：** 使用了错误的格式

**解决：** 使用 mentions 参数，不要手动写`<at>`代码

---

## 📚 相关文档

| 文件 | 说明 |
|------|------|
| **feishu-bot-core-rules.md** | 核心行为规范 |
| **2026-03-23-feishu-at-mention-enabled.md** | @提及启用记录 |
| **本文件** | @提及配置指南 |

---

**状态**: ✅ 权限已开通，待配置测试  
**下一步**: 配置代码支持@提及  
**测试**: 待配置后测试

---

**最后更新**: 2026-03-23  
**维护者**: RedOpenClaw

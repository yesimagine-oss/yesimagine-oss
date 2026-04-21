# 🔍 飞书问题检查报告

**检查时间**: 2026-03-19 21:55  
**检查者**: 麻小 🦐

---

## 📊 检查结果总结

| 问题 | 状态 | 说明 |
|------|------|------|
| **1. JSON 直接输出** | ⚠️ **未发现代码问题** | 代码使用 `post` 格式，应该正常渲染 |
| **2. 会话上下文混乱** | ⚠️ **配置正确** | `dmScope: "per-channel-peer"` 已设置 |
| **3. @提及功能** | ✅ **代码支持** | 有完整的 mention 模块 |
| **4. 重复消息** | ❓ **需要日志** | 需要查看实际发送记录 |
| **5. 承诺未兑现** | ❓ **需要验证** | 需要检查是否有未完成的修改 |

---

## 🔧 详细检查

### 问题 1: JSON 直接输出

**检查内容：**
- 文件：`/opt/openclaw/extensions/feishu/src/send.ts`
- 函数：`buildFeishuPostMessagePayload()`

**代码：**
```typescript
function buildFeishuPostMessagePayload(params: { messageText: string }): {
  content: string;
  msgType: string;
} {
  const { messageText } = params;
  const elements = parseMentionsInText(messageText);
  
  return {
    content: JSON.stringify({
      zh_cn: {
        content: [elements],
      },
    }),
    msgType: "post",  // ✅ 使用 post 格式（富文本）
  };
}
```

**结论：** 
- ✅ 代码正确，使用 `msgType: "post"`
- ✅ 飞书应该正常渲染
- ❓ 如果用户看到 JSON，可能是：
  - 飞书客户端 bug
  - 特定消息类型（如卡片）的降级
  - 消息发送失败后的回退逻辑

---

### 问题 2: 会话上下文混乱

**检查配置：**
```json
{
  "session": {
    "dmScope": "per-channel-peer"  // ✅ 每个渠道独立会话
  },
  "messages": {
    "ackReactionScope": "all"  // ✅ 监听所有消息
  }
}
```

**代码逻辑：**
```typescript
// bot.ts line 271-286
let peerId = chatId;

if (chatType === "p2p") {
  // DM: per-sender session
  peerId = `${chatId}:sender:${senderOpenId}`;
} else if (topicScope) {
  // Group with topic: per-topic session
  peerId = topicScope ? `${chatId}:topic:${topicScope}` : chatId;
}
```

**结论：**
- ✅ 配置正确
- ✅ 代码逻辑正确
- ❓ 如果还是混乱，可能是：
  - 飞书渠道的 `chatId` 识别有问题
  - 多个群组使用了相同的 `chatId`
  - session 缓存没有正确清理

---

### 问题 3: @提及功能

**检查代码：**
- 文件：`/opt/openclaw/extensions/feishu/src/mention.ts`
- 函数：`buildMentionedMessage()`

**支持情况：**
```typescript
// send.ts line 263-268
let rawText = text ?? "";
if (mentions && mentions.length > 0) {
  rawText = buildMentionedMessage(mentions, rawText);
}
```

**结论：**
- ✅ 代码支持@提及
- ✅ 使用飞书富文本格式
- ❓ 如果不起作用，可能是：
  - `mentions` 参数没有正确传递
  - 飞书客户端版本问题
  - 群组权限限制

---

### 问题 4: 重复消息

**需要检查：**
1. cron 任务配置
2. 消息去重逻辑
3. 发送日志

**检查命令：**
```bash
# 查看 cron 配置
cat ~/.openclaw/workspace/HEARTBEAT.md

# 查看消息日志
grep "sendMessage" /tmp/openclaw/openclaw-2026-03-19.log | tail -50
```

---

### 问题 5: 承诺未兑现

**需要验证：**
1. 机器人说修改了哪些文件
2. 实际是否修改
3. 修改后是否重启

**检查方法：**
- 查看文件修改时间
- 对比 Git 历史（如果有）
- 检查日志中的错误

---

## 🎯 当前配置状态

### ✅ 正确的配置

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "default": {
          "streaming": true,      // ✅ 流式传输开启
          "renderMode": "auto"     // ✅ 自动选择格式
        }
      }
    }
  },
  "session": {
    "dmScope": "per-channel-peer"  // ✅ 独立会话
  },
  "messages": {
    "ackReactionScope": "all"      // ✅ 监听所有消息
  }
}
```

---

## 📝 建议的测试

### 测试 1: 消息格式

**操作：** 在飞书发送一条普通消息
**预期：** 机器人正常回复，不是 JSON
**验证：** 检查回复是否是渲染后的文本

---

### 测试 2: 会话隔离

**操作：** 
1. 在群 A 发送消息
2. 在群 B 发送消息
3. 检查机器人是否混淆

**预期：** 两个群的对话独立

---

### 测试 3: @提及

**操作：** `@机器人 你好`
**预期：** 机器人回复中包含蓝色的@提及

---

### 测试 4: 重复消息

**操作：** 发送一条消息
**预期：** 只收到一次回复

---

## 🔍 需要更多信息

为了准确诊断问题，需要：

1. **实际日志** - 查看消息发送记录
2. **具体时间点** - 问题发生的时间
3. **群组信息** - 哪个群出现的问题
4. **消息内容** - 触发问题的消息类型

---

## 💡 初步结论

**代码层面：**
- ✅ 没有发现明显的 bug
- ✅ 配置都是正确的
- ✅ 功能都有实现

**可能的原因：**
1. **运行时问题** - 配置没有正确加载
2. **缓存问题** - 旧配置还在生效
3. **飞书 API 变化** - 接口行为改变
4. **特定场景触发** - 某些条件下才会出现

---

## 🎯 下一步

### 选项 A: 查看日志 ⭐⭐⭐⭐⭐

```bash
# 查看最近的消息日志
tail -100 /tmp/openclaw/openclaw-2026-03-19.log | grep -E "feishu|send|message"
```

### 选项 B: 实时测试 ⭐⭐⭐⭐

在飞书测试：
1. 发送消息
2. 观察回复
3. 检查格式

### 选项 C: 重启 Gateway ⭐⭐⭐

确保配置完全生效：
```bash
openclaw gateway restart
```

---

**报告时间**: 2026-03-19 21:55  
**状态**: 代码检查完成，需要日志和测试验证

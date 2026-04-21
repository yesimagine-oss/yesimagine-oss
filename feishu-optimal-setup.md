# 📘 飞书最优选配置部署指南

**版本:** v1.0  
**创建时间:** 2026-03-15 15:49  
**适用场景:** 微信文章推送/通知/自动化

---

## 🎯 方案概述

### 核心目标

用最简单的配置，实现微信文章推送到飞书的功能。

### 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| **应用类型** | 企业自建应用 | 免费、功能完整 |
| **推送方式** | 机器人 Webhook | 简单、无需认证 |
| **权限范围** | 最小权限 | 安全、易审核 |
| **部署方式** | 本地脚本 | 快速、易维护 |

---

## 📦 配置步骤 (30 分钟完成)

### 步骤 1: 创建飞书应用 (5 分钟)

1. **访问开放平台**
   ```
   https://open.feishu.cn/
   ```

2. **登录飞书**
   - 使用飞书账号登录
   - 进入"企业自建应用"

3. **创建应用**
   ```
   应用名称：WeChat Reader
   应用图标：📱 (可选)
   应用描述：微信文章读取和推送工具
   ```

4. **记录 App ID**
   ```
   App ID: cli_xxxxxxxxxxxxx
   ```

---

### 步骤 2: 添加机器人 (10 分钟)

1. **进入应用管理**
   - 点击创建的应用
   - 应用功能 → 机器人

2. **添加机器人**
   ```
   机器人名称：WeChat Bot
   机器人头像：📖 (可选)
   功能：接收消息、发送消息
   ```

3. **获取 Webhook URL**
   ```
   发布设置 → 机器人 → Webhook
   复制 Webhook URL:
   https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxx
   ```

4. **保存到配置文件**
   ```bash
   mkdir -p ~/.openclaw/workspace/.config
   cat > ~/.openclaw/workspace/.config/feishu.json << 'EOF'
   {
     "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxx",
     "app_id": "cli_xxxxxxxxxxxxx",
     "created_at": "2026-03-15"
   }
   EOF
   ```

---

### 步骤 3: 配置权限 (5 分钟)

**最小权限配置:**

| 权限 | 用途 | 是否必需 |
|------|------|---------|
| **机器人发送消息** | 推送文章 | ✅ 必需 |
| **机器人接收消息** | 可选交互 | ⚠️ 可选 |

**配置步骤:**
1. 权限管理 → 申请权限
2. 搜索"机器人"
3. 勾选"发送消息"权限
4. 提交 (自动生效)

---

### 步骤 4: 测试推送 (5 分钟)

**测试脚本:**
```bash
cat > /tmp/test-feishu.sh << 'EOF'
#!/bin/bash
WEBHOOK="你的 Webhook URL"

curl -X POST "$WEBHOOK" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "🎉 飞书推送测试成功！"
    }
  }'
EOF

chmod +x /tmp/test-feishu.sh
/tmp/test-feishu.sh
```

**预期结果:**
```
✅ 飞书机器人发送测试消息
```

---

### 步骤 5: 集成到 wechat-reader (5 分钟)

**更新配置文件:**
```bash
cat > ~/.openclaw/workspace/skills/wechat-reader-node/.feishu-config << 'EOF'
{
  "enabled": true,
  "webhook_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxx",
  "default_msg_type": "post",
  "auto_push": false
}
EOF
```

**测试集成:**
```bash
cd ~/.openclaw/workspace/skills/wechat-reader-node
node scripts/read.js "文章 URL" --feishu "$(cat ~/.openclaw/workspace/.config/feishu.json | jq -r .webhook_url)"
```

---

## 🔧 高级配置 (可选)

### 1. 多机器人配置

**场景:** 不同用途使用不同机器人

```json
{
  "robots": {
    "wechat": {
      "name": "WeChat Bot",
      "webhook": "https://...hook1..."
    },
    "notify": {
      "name": "Notify Bot",
      "webhook": "https://...hook2..."
    },
    "alert": {
      "name": "Alert Bot",
      "webhook": "https://...hook3..."
    }
  }
}
```

### 2. 消息模板

**文本消息:**
```json
{
  "msg_type": "text",
  "content": {
    "text": "📱 新文章推送\n\n标题：{title}\n公众号：{source}\n链接：{url}"
  }
}
```

**卡片消息:**
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "📱 微信文章"
      },
      "template": "blue"
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "**{title}**"
        }
      },
      {
        "tag": "action",
        "actions": [
          {
            "tag": "button",
            "text": {
              "tag": "plain_text",
              "content": "📖 阅读原文"
            },
            "url": "{url}",
            "type": "default"
          }
        ]
      }
    ]
  }
}
```

### 3. 自动化推送

**配置定时任务:**
```bash
# 每天上午 9 点推送
0 9 * * * cd ~/.openclaw/workspace/skills/wechat-reader-node && node scripts/batch.js "科技新闻" -n 5 -r --feishu "$WEBHOOK"
```

---

## 📊 配置检查清单

### 必选项

- [ ] 飞书应用已创建
- [ ] App ID 已记录
- [ ] 机器人已添加
- [ ] Webhook URL 已保存
- [ ] 权限已配置
- [ ] 测试推送成功

### 可选项

- [ ] 多机器人配置
- [ ] 消息模板定制
- [ ] 定时推送配置
- [ ] 错误通知配置

---

## 🔍 故障排查

### 问题 1: 推送失败

**可能原因:**
- Webhook URL 错误
- 网络问题
- 权限不足

**解决方案:**
```bash
# 检查 Webhook
curl -X POST "$WEBHOOK" \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"test"}}'

# 预期响应
{"code":0,"msg":"success"}
```

### 问题 2: 消息格式错误

**可能原因:**
- JSON 格式错误
- 字段缺失

**解决方案:**
```bash
# 验证 JSON
echo '{"msg_type":"text","content":{"text":"test"}}' | jq .
```

### 问题 3: 权限不足

**可能原因:**
- 未申请权限
- 权限未生效

**解决方案:**
1. 开放平台 → 权限管理
2. 申请所需权限
3. 等待生效 (通常立即)

---

## 📚 参考资源

| 资源 | 链接 |
|------|------|
| **飞书开放平台** | https://open.feishu.cn/ |
| **机器人文档** | https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN |
| **消息格式** | https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN |
| **Webhook 使用** | https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN |

---

## 🎯 最佳实践

### 1. 安全第一

- ✅ 不要泄露 Webhook URL
- ✅ 使用最小权限
- ✅ 定期轮换凭证

### 2. 性能优化

- ✅ 控制推送频率 (<100 次/分钟)
- ✅ 消息大小限制 (<4000 字符)
- ✅ 使用异步推送

### 3. 用户体验

- ✅ 消息格式清晰
- ✅ 包含必要信息
- ✅ 提供操作按钮

---

## 📈 配置完成后的效果

### 微信文章推送流程

```
用户请求
    ↓
wechat-reader 读取文章
    ↓
生成推送消息
    ↓
发送到飞书 Webhook
    ↓
飞书机器人推送
    ↓
用户收到消息
```

### 推送示例

```
┌─────────────────────────────────────────┐
│ 📱 微信文章                              │
├─────────────────────────────────────────┤
│ AI 技术前沿：2026 年发展趋势             │
│                                         │
│ 作者：张三    公众号：AI 前沿            │
│                                         │
│ 本文介绍了 2026 年 AI 技术的主要发展趋    │
│ 势，包括... (内容摘要)                   │
│                                         │
│ [📖 阅读原文]                           │
└─────────────────────────────────────────┘
```

---

**配置版本:** v1.0  
**预计完成时间:** 30 分钟  
**维护者:** OpenClaw Workspace

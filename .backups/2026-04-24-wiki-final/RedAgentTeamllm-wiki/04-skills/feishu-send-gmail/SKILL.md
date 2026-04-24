---
name: feishu-send-gmail
version: 1.0.0
description: 通过飞书命令发送 Gmail 邮件
author: 麻小 🦐
keywords:
  - 发送邮件
  - Gmail
  - 飞书
  - 邮件
triggers:
  - "发送邮件"
  - "发 Gmail"
  - "发邮件"
  - "send email"

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
# 📧 飞书发送邮件技能

**功能：** 通过飞书命令发送 Gmail 邮件

---

## 🎯 使用方式

### 方式 1: 简单命令

```
发送邮件给 xxx@example.com 主题 "测试" 内容 "你好"
```

### 方式 2: 完整命令

```
用 Gmail 发送邮件：
收件人：xxx@example.com
主题：测试邮件
内容：这是一封测试邮件
```

### 方式 3: 回复消息

```
（回复某条消息）
发送邮件给 xxx@example.com
```

---

## 📋 执行流程

1. 解析飞书消息
2. 提取收件人、主题、内容
3. 调用 send-email.py 脚本
4. 返回发送结果

---

## 🔧 技术实现

```python
# 调用邮件发送脚本
python3 /home/admin/.openclaw/workspace/tools/send-email.py \
  --to "收件人邮箱" \
  --subject "主题" \
  --content "内容" \
  --use-gmail
```

---

## 📝 示例

### 示例 1: 发送测试邮件

**飞书命令：**
```
发送邮件给 yesimagine@gmail.com 主题 "测试" 内容 "你好世界"
```

**预期结果：**
```
✅ 邮件发送成功！
发件人：yesimagine@gmail.com
收件人：yesimagine@gmail.com
主题：测试
```

### 示例 2: 发送带 HTML 的邮件

**飞书命令：**
```
发送邮件给 xxx@example.com 主题 "报告" 内容 "<h1>周报</h1><p>本周完成...</p>"
```

---

## ⚙️ 配置

### Gmail 配置
- 邮箱：yesimagine@gmail.com
- SMTP: smtp.gmail.com:587 (TLS)
- 授权码：已配置（应用专用密码）

### 腾讯企业邮（备用）
- 邮箱：red@unvw.com
- SMTP: smtp.exmail.qq.com:465 (SSL)
- 授权码：已配置

---

## 🐛 故障排查

### 问题 1: 认证失败
**原因：** Gmail 授权码错误或过期  
**解决：** 重新生成应用专用密码

### 问题 2: 连接失败
**原因：** 网络问题或防火墙  
**解决：** 检查服务器网络连接

### 问题 3: 解析失败
**原因：** 命令格式不对  
**解决：** 使用标准格式

---

**最后更新**: 2026-03-19  
**维护者**: 麻小 🦐

## 參考

- [[Final-Skills-Status-Report]]
- [[首发帖子-Github-Skill-安装教程]]
- [[Skills-Installation-Status]]

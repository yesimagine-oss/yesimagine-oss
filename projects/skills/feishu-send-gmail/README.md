# 📧 飞书邮件发送 - 完整使用指南

**版本**: 1.0  
**创建时间**: 2026-03-19  
**状态**: ✅ 已完成（邮件发送 + 飞书通知）

---

## 🎯 功能概述

1. **Gmail 邮件发送** - 通过 SMTP 发送 Gmail
2. **飞书通知** - 发送成功/失败自动通知
3. **命令解析** - 支持多种命令格式
4. **错误处理** - 详细的错误分析和解决方案

---

## 📖 使用方式

### 方式 1: 飞书命令（推荐）⭐⭐⭐⭐⭐

**在飞书中发送消息：**

```
发送邮件给 xxx@example.com 主题 "测试" 内容 "你好"
```

**系统会自动：**
1. ✅ 解析命令
2. ✅ 发送邮件
3. ✅ 飞书通知结果

---

### 方式 2: 直接调用脚本

```bash
# 发送 Gmail
python3 /home/admin/.openclaw/workspace/tools/send-email.py \
  --to "xxx@example.com" \
  --subject "主题" \
  --content "内容"
```

---

### 方式 3: 使用执行器（带通知）

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-email-executor.py \
  '发送邮件给 xxx@example.com 主题 "测试" 内容 "你好"'
```

---

## 📋 支持的命令格式

### 格式 1: 标准格式

```
发送邮件给 xxx@example.com 主题 "测试" 内容 "你好"
```

### 格式 2: 简化格式

```
发送邮件给 xxx@example.com 主题 测试 内容 你好
```

### 格式 3: Gmail 格式

```
发 Gmail 到 xxx@example.com 标题 测试 内容 你好
```

### 格式 4: 英文格式

```
send email to xxx@example.com subject Test content Hello
```

---

## 📊 飞书通知示例

### ✅ 成功通知

```
✅ 邮件发送成功

发件人：yesimagine@gmail.com
收件人：yesimagine@gmail.com
主题：测试邮件
发送时间：2026-03-19 20:05:50

邮件内容预览：
这是一封测试邮件的内容，用于验证飞书通知功能是否正常。
```

### ❌ 失败通知

```
❌ 邮件发送失败

发件人：yesimagine@gmail.com
收件人：yesimagine@gmail.com
主题：测试邮件
发送时间：2026-03-19 20:05:54

失败原因：
认证失败：邮箱账号或授权码错误

解决方案：
1. 检查 Gmail 授权码是否正确
2. 重新生成应用专用密码
3. 联系管理员更新配置
```

---

## ⚙️ 配置说明

### Gmail 配置

**文件**: `/home/admin/.openclaw/workspace/tools/send-email.py`

```python
GMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": "yesimagine@gmail.com",
    "password": "lqswobvyqzjkqfwu"  # 应用专用密码
}
```

### 飞书通知配置

**文件**: `/home/admin/.openclaw/workspace/tools/feishu-email-notifier.py`

**需要配置 Webhook：**

1. 在飞书群添加机器人
2. 获取 Webhook URL
3. 设置环境变量：

```bash
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

---

## 🐛 故障排查

### 问题 1: 邮件发送失败

**检查：**
```bash
# 测试 Gmail 连接
python3 /home/admin/.openclaw/workspace/tools/send-email.py \
  --to "yesimagine@gmail.com" \
  --subject "测试" \
  --content "测试"
```

**常见错误：**
- 认证失败 → 检查授权码
- 连接失败 → 检查网络
- 超时 → 检查防火墙

---

### 问题 2: 飞书通知没收到

**检查：**
```bash
# 测试通知脚本
python3 /home/admin/.openclaw/workspace/tools/feishu-email-notifier.py \
  --status success \
  --to "test@example.com" \
  --subject "测试"
```

**常见错误：**
- 未配置 Webhook → 设置 `FEISHU_WEBHOOK`
- Webhook 无效 → 检查 URL
- 权限不足 → 检查机器人权限

---

### 问题 3: 命令解析失败

**检查命令格式：**
```bash
# 测试解析
python3 /home/admin/.openclaw/workspace/tools/feishu-email-executor.py \
  '发送邮件给 xxx@example.com 主题 "测试" 内容 "你好"'
```

**确保：**
- 包含"发送邮件给"关键词
- 有收件人、主题、内容
- 格式正确

---

## 📁 相关文件

| 文件 | 用途 | 位置 |
|------|------|------|
| **send-email.py** | 邮件发送脚本 | `/home/admin/.openclaw/workspace/tools/` |
| **feishu-email-executor.py** | 飞书命令解析器 | `/home/admin/.openclaw/workspace/tools/` |
| **feishu-email-notifier.py** | 飞书通知脚本 | `/home/admin/.openclaw/workspace/tools/` |
| **EMAIL-NOTIFICATION-SPEC.md** | 通知规范文档 | `/home/admin/.openclaw/workspace/skills/feishu-send-gmail/` |
| **SKILL.md** | 技能文档 | `/home/admin/.openclaw/workspace/skills/feishu-send-gmail/` |

---

## 🔒 安全提醒

### 授权码保护

- ✅ 存储在代码中（已设置文件权限）
- ✅ 不要上传到 Git
- ✅ 定期更新（建议每 90 天）

### 文件权限

```bash
# 设置脚本权限
chmod 755 /home/admin/.openclaw/workspace/tools/send-email.py
chmod 755 /home/admin/.openclaw/workspace/tools/feishu-*.py

# 设置配置文件权限（如果有）
chmod 600 /path/to/config.py
```

---

## 📊 测试清单

### 测试 1: Gmail 发送

```bash
python3 /home/admin/.openclaw/workspace/tools/send-email.py \
  --to "yesimagine@gmail.com" \
  --subject "测试" \
  --content "测试内容"
```

**预期结果：** ✅ 邮件发送成功

---

### 测试 2: 命令解析

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-email-executor.py \
  '发送邮件给 yesimagine@gmail.com 主题 "测试" 内容 "你好"'
```

**预期结果：** ✅ 解析成功 + 邮件发送成功

---

### 测试 3: 飞书通知（成功）

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-email-notifier.py \
  --status success \
  --to "test@example.com" \
  --subject "测试" \
  --content "测试内容"
```

**预期结果：** ✅ 显示通知内容（需要 Webhook 才能实际发送）

---

### 测试 4: 飞书通知（失败）

```bash
python3 /home/admin/.openclaw/workspace/tools/feishu-email-notifier.py \
  --status failed \
  --to "test@example.com" \
  --subject "测试" \
  --error "认证失败"
```

**预期结果：** ✅ 显示失败通知（带解决方案）

---

## 🎯 最佳实践

1. **始终使用飞书命令** - 自动通知
2. **检查通知配置** - 确保 Webhook 正确
3. **记录所有发送** - 便于追踪
4. **定期测试** - 确保功能正常
5. **更新授权码** - 每 90 天更新一次

---

## 📞 需要帮助？

### 查看日志

```bash
# 查看邮件发送日志
tail -f /home/admin/.openclaw/workspace/logs/email.log
```

### 测试连接

```bash
# 测试 Gmail SMTP
telnet smtp.gmail.com 587
```

### 检查配置

```bash
# 检查环境变量
echo $FEISHU_WEBHOOK
```

---

**最后更新**: 2026-03-19  
**维护者**: 麻小 🦐

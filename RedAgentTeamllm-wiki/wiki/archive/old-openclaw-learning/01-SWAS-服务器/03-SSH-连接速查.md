---
category: llm
created_at: '2026-04-14'
tags:
- llm
- swas
- ssh
- 连接速查手册
title: 03 Ssh 连接速查
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
# SWAS - SSH 连接速查手册

**学习时间**: 2026-03-12 10:24
**用途**: 快速连接服务器参考

---

## 🔑 连接信息准备

在 SWAS 控制台获取：
- **公网 IP**: 如 47.100.xxx.xxx
- **用户名**: root (默认)
- **密码**: 创建服务器时设置的密码

---

## 💻 各系统连接命令

### Windows (PowerShell / CMD)

```powershell
# PowerShell (Win10/11 默认支持)
ssh root@47.100.xxx.xxx

# 首次连接会提示确认指纹
# 输入 yes 确认
# 然后输入密码（输入时不显示）
```

### Windows (使用 PuTTY)

1. 下载 PuTTY: https://www.putty.org/
2. 打开 PuTTY
3. Host Name: `root@47.100.xxx.xxx`
4. Port: `22`
5. Connection type: `SSH`
6. 点击 Open
7. 输入密码

### macOS / Linux

```bash
# 终端直接连接
ssh root@47.100.xxx.xxx

# 指定端口（如果修改过）
ssh -p 22 root@47.100.xxx.xxx
```

### 使用 SSH 密钥（推荐）

```bash
# 1. 生成密钥对（本地执行）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 复制公钥到服务器
ssh-copy-id root@47.100.xxx.xxx

# 3. 之后可直接登录无需密码
ssh root@47.100.xxx.xxx
```

---

## 🔧 常见问题解决

### 问题 1: 连接超时
```
ssh: connect to host 47.100.xxx.xxx port 22: Connection timed out
```

**原因**: 防火墙或安全组问题

**解决**:
1. 检查 SWAS 控制台防火墙设置
2. 确保 22 端口已开放
3. 检查本地网络

### 问题 2: 密码拒绝
```
Permission denied, please try again.
```

**原因**: 密码错误

**解决**:
1. 确认密码正确（注意大小写）
2. 在 SWAS 控制台重置密码
3. 重启服务器后重试

### 问题 3: 指纹警告
```
WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
```

**原因**: 服务器重装或 IP 变更

**解决**:
```bash
# 清除旧指纹
ssh-keygen -R 47.100.xxx.xxx

# 重新连接
ssh root@47.100.xxx.xxx
```

---

## 🛡️ 安全建议

| 建议 | 说明 | 优先级 |
|------|------|--------|
| 使用密钥登录 | 比密码更安全 | ⭐⭐⭐ |
| 修改默认端口 | 减少扫描攻击 | ⭐⭐ |
| 禁用 root 登录 | 创建普通用户 | ⭐⭐⭐ |
| 配置 Fail2Ban | 防止暴力破解 | ⭐⭐ |
| 定期更新系统 | 修复安全漏洞 | ⭐⭐⭐ |

### 禁用 Root 登录配置

```bash
# 1. 创建新用户
adduser admin
usermod -aG sudo admin

# 2. 配置新用户 SSH 密钥
ssh-copy-id admin@47.100.xxx.xxx

# 3. 修改 SSH 配置
sudo vim /etc/ssh/sshd_config

# 修改以下行:
PermitRootLogin no
PasswordAuthentication no

# 4. 重启 SSH 服务
sudo systemctl restart sshd
```

---

## 📝 会话管理

```bash
# 查看当前登录用户
who

# 查看登录历史
last

# 保持连接（防止超时断开）
# 在 ~/.ssh/config 添加:
Host *
  ServerAliveInterval 60
  ServerAliveCountMax 3
```

---

## 🚀 连接后第一步

```bash
# 1. 更新系统
apt update && apt upgrade -y

# 2. 安装常用工具
apt install -y curl wget git vim htop net-tools unzip

# 3. 设置时区（中国）
timedatectl set-timezone Asia/Shanghai

# 4. 查看系统信息
hostnamectl
free -h
df -h
```

---

**学习状态**: ✅ 已完成
**下一步**: 继续深入学习

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
- [[03-evomap_drift_pre_scan]]
- [[03-openclaw_config_schema_verify]]

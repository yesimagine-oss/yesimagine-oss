# 2026-04-21 OpenClaw Gateway 认证修复记录

**创建时间**: 2026-04-21 07:38 GMT+8  
**时间范围**: 05:33 - 07:38 (2 小时)  
**状态**: ✅ 进行中  
**重要性**: 🔴 高 (生产环境认证问题)

---

## 📋 执行摘要

**问题**: OpenClaw 2026.3.3 远程登录失败，显示 "token missing" 和 "rate_limited"

**根本原因**: 
1. Control UI 保存 Token 后配置文件未更新 (可能版本 bug)
2. Control UI 登录界面未正确传递 Token 到 WebSocket 连接
3. 多次失败触发速率限制 (5 分钟锁定)

**当前状态**: 
- ✅ Gateway 配置正确 (`gateway.auth.token` 已设置)
- ✅ nginx 配置正确 (Authorization 头已传递)
- ✅ Gateway 服务正常 (PID 253861, RPC OK)
- ❌ Control UI 登录流程问题 (Token 未正确发送)

---

## 🕐 时间线

| 时间 | 事件 | 状态 | 说明 |
|------|------|------|------|
| **05:33** | 开始全面检查 OpenClaw 系统 | ✅ 完成 | Gateway 状态、安全审计、资源配置 |
| **05:40** | 执行安全加固建议 | ✅ 完成 | 禁用 Host Header 回退、启用速率限制、启用 Sandbox |
| **05:42** | 汇报安全加固执行情况 | ✅ 完成 | 0 严重 +0 警告，内存使用↓38% |
| **05:44** | 检测系统变化 | ✅ 完成 | 安全风险清除，内存优化 |
| **05:45** | 检查 WebChat 通道 | ✅ 完成 | webchat 正常，Gateway 运行正常 |
| **05:47** | 检查远程访问配置 | ✅ 完成 | https://openclaw.unvw.com 配置完整 |
| **05:49** | 评估 Gateway Token 配置 | ✅ 完成 | Token 正确，但需注意安全实践 |
| **05:52** | 设置 Git 版本控制 | ✅ 完成 | 创建 .gitignore，排除敏感文件 |
| **05:54** | 执行配置备份 | ✅ 完成 | 2 个备份文件 |
| **06:05** | 评估备份策略 | ✅ 完成 | Git 已配置但 openclaw.json 被排除 |
| **06:06** | 创建备份脚本 | ✅ 完成 | `~/.openclaw/scripts/backup-config.sh` |
| **06:09** | 执行备份 | ✅ 完成 | `openclaw.json.20260421-060943.bak` |
| **06:10** | 显示系统时间 | ✅ 完成 | 06:10:27 CST |
| **06:14** | 验证远程登录 | ❌ 失败 | "token missing" + "rate_limited" |
| **06:16** | 分析 Control UI 配置路径 | ✅ 完成 | 确认本地地址可操作 |
| **06:18** | 评估假设场景 | ✅ 完成 | 提供诊断流程和恢复方案 |
| **06:20** | 确认 Control UI 配置路径 | ✅ 完成 | 左侧菜单 → 设置 → 配置 |
| **06:24** | 验证远程登录失败 | ❌ 失败 | nginx 反向代理认证问题 |
| **06:27** | 修复 nginx 配置 | ✅ 完成 | 添加 Authorization 头传递 |
| **06:31** | 验证 nginx 修复 | ✅ 完成 | 远程访问 HTTP 200 |
| **06:36** | 登录失败 - 速率限制触发 | ❌ 失败 | "too many failed attempts" |
| **06:40** | 分析速率限制原因 | ✅ 完成 | 多次失败触发 5 分钟锁定 |
| **06:41** | 汇报 nginx 配置能力 | ✅ 完成 | 能分析/编写，不能直接修改系统 |
| **06:42** | 执行 nginx 配置更新 | ✅ 完成 | 授权 sudo，配置生效 |
| **06:46** | 验证远程登录 | ❌ 失败 | 仍显示 "token missing" |
| **06:50** | 确认限流解锁时间 | ✅ 完成 | 07:00:13 后自动解锁 |
| **06:52** | 分析再次限流 | ✅ 完成 | Token 未传递导致多次失败 |
| **06:55** | 确认限流状态 | ✅ 完成 | 07:00:13 解锁 |
| **07:04** | 验证限流解除 | ✅ 完成 | 最近日志无限流错误 |
| **07:06** | 用户操作 Control UI 保存 Token | ✅ 完成 | 但配置文件时间未变 |
| **07:09** | 验证远程登录 | ❌ 失败 | "token missing" |
| **07:11** | 分析 Chrome 密码保存 | ✅ 完成 | 本地/远程地址不同，不会自动保存 |
| **07:14** | 确认再次失败 | ❌ 失败 | 预测准确，版本问题 |
| **07:20** | 分析 Control UI 设置问题 | ✅ 完成 | 保存可能未生效 |
| **07:27** | 查找历史配置记录 | ✅ 完成 | 发现 2026-04-16 事故记录 |
| **07:31** | 用户提供 Control UI 说明 | ✅ 完成 | Gateway Token vs Remote Gateway Token |
| **07:35** | 执行验证步骤 | ✅ 完成 | 配置正确，问题在登录流程 |
| **07:38** | 创建本记忆文档 | ✅ 进行中 | 防止上下文压缩丢失 |

---

## 🔧 关键配置

### Gateway 认证配置
```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "36322def61722938e759077fa8d654388049d97fea9f1931",
      "rateLimit": {
        "maxAttempts": 10,
        "windowMs": 60000,
        "lockoutMs": 300000
      }
    }
  }
}
```

### nginx 配置修复
```nginx
location / {
    proxy_pass http://127.0.0.1:18789;
    proxy_http_version 1.1;
    proxy_set_header Authorization $http_authorization;  # 关键修复
    proxy_set_header Host $host;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400s;
    proxy_send_timeout 86400s;
    proxy_buffering off;
}
```

### 备份配置
```bash
备份脚本：~/.openclaw/scripts/backup-config.sh
备份目录：~/.openclaw/backups/
保留期：30 天
```

---

## 🎯 问题根因

### 1. Control UI 保存未生效
- **现象**: 07:09 在 Control UI 保存 Token，但配置文件时间仍是 07:07:58
- **可能原因**: 2026.3.3 版本 Control UI bug
- **影响**: Token 配置看似正确，但 Control UI 未正确读取/保存

### 2. Control UI 登录流程问题
- **现象**: 远程登录显示 "token missing"
- **日志**: `"authProvided": "none"` - Token 未被发送
- **可能原因**: 
  - Control UI 没有明显的 Token 输入框
  - 前端未正确传递 Token 到 WebSocket 连接
  - 登录界面设计不符合 2026.3.3 版本

### 3. 速率限制触发
- **原因**: 多次失败尝试 (Token 未提供)
- **锁定时间**: 5 分钟 (300 秒)
- **触发次数**: 2 次 (06:36, 06:55)

---

## 📊 配置验证结果

| 检查项 | 状态 | 命令/位置 |
|--------|------|-----------|
| **Gateway Token** | ✅ 正确 | `grep '"token"' ~/.openclaw/openclaw.json` |
| **Gateway 状态** | ✅ 运行中 | `openclaw gateway status` |
| **本地访问** | ✅ 正常 | `curl http://127.0.0.1:18789/` |
| **远程访问** | ✅ 正常 | `curl -I https://openclaw.unvw.com` |
| **nginx 配置** | ✅ 正确 | `/etc/nginx/conf.d/openclaw.unvw.com.conf` |
| **SSL 证书** | ✅ 有效 | Let's Encrypt, 剩余 89 天 |
| **速率限制** | ✅ 已解除 | 最近日志无 `rate_limited` |
| **备份文件** | ✅ 2 个 | `~/.openclaw/backups/` |

---

## 🔍 未解决问题

### 1. Control UI 登录界面
- **问题**: 找不到明显的 Token 输入框
- **影响**: 用户无法通过 Control UI 正常登录
- **待确认**: Control UI 页面布局和登录流程

### 2. Control UI 保存功能
- **问题**: 保存后配置文件未更新
- **影响**: 用户以为保存成功，实际未生效
- **待确认**: Control UI 是否有其他配置存储位置

### 3. 版本兼容性
- **问题**: 2026.3.3 可能是旧版本
- **影响**: Control UI 功能可能不完善
- **待确认**: 是否有更新版本可用

---

## 📋 待执行操作

### 立即执行
- [ ] 确认 Control UI 页面布局 (截图或描述)
- [ ] 找到正确的 Token 输入位置
- [ ] 测试 Control UI 登录流程

### 短期修复 (24 小时)
- [ ] 检查 OpenClaw 可用更新
- [ ] 如 Control UI 有 bug，考虑升级版本
- [ ] 验证远程登录成功

### 长期优化 (7 天)
- [ ] 配置浏览器保存密码
- [ ] 建立配置修改 SOP
- [ ] 定期备份配置

---

## 📚 相关文档

| 文档 | 位置 |
|------|------|
| **配置文件** | `~/.openclaw/openclaw.json` |
| **nginx 配置** | `/etc/nginx/conf.d/openclaw.unvw.com.conf` |
| **备份脚本** | `~/.openclaw/scripts/backup-config.sh` |
| **Git 配置** | `~/.openclaw/.gitignore` |
| **工作区 Git** | `~/.openclaw/workspace/.git/` |
| **事故记录** | `~/.openclaw/workspace/llm-wiki/accidents/` |

---

## 🏆 关键成果

### 已完成
1. ✅ Gateway 安全加固 (0 严重 +0 警告)
2. ✅ nginx 配置修复 (Authorization 头传递)
3. ✅ Git 版本控制设置
4. ✅ 备份脚本创建
5. ✅ 配置文件备份 (2 个)
6. ✅ 本记忆文档创建

### 进行中
1. 🟡 Control UI 登录流程问题排查
2. 🟡 远程登录验证

---

## 💡 经验教训

### 成功经验
1. **渐进式排查**: 从配置到服务到网络，逐步验证
2. **日志分析**: 通过日志快速定位问题根因
3. **备份先行**: 修改前备份，降低风险
4. **文档记录**: 实时记录，防止遗忘

### 教训
1. **Control UI 信任度**: 不要完全相信 UI 显示，需验证配置文件
2. **版本意识**: 2026.3.3 可能是旧版本，功能可能不完善
3. **登录流程**: 不同版本 Control UI 登录方式可能不同

---

## 🔗 相关会话

| 时间 | 主题 | 状态 |
|------|------|------|
| 05:33-05:44 | 系统全面检查 | ✅ 完成 |
| 05:45-05:52 | WebChat 通道检测 | ✅ 完成 |
| 05:54-06:10 | Git 版本控制设置 | ✅ 完成 |
| 06:14-06:42 | 远程登录问题排查 | ✅ 完成 |
| 06:46-07:04 | nginx 修复 + 限流分析 | ✅ 完成 |
| 07:06-07:38 | Control UI 登录流程排查 | 🟡 进行中 |

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 07:38 GMT+8  
**状态**: ✅ 已保存，防止上下文压缩丢失  
**下一步**: 继续排查 Control UI 登录流程

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

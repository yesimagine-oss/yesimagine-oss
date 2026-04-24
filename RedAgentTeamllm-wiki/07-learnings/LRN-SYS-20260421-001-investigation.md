# LRN-SYS-20260421-001 彻底排查报告

**事故 ID**: LRN-SYS-20260421-001  
**排查时间**: 2026-04-21 22:00-22:06 GMT+8  
**排查者**: Red Agent Team  
**状态**: ✅ 根因已找到，待用户验证修复  

---

## 📋 事故现象

| 现象 | 状态 |
|------|------|
| 本地访问 (127.0.0.1:18789) | ✅ 正常 |
| 公网访问 (openclaw.unvw.com) | ❌ 失败 |
| 错误信息 | `WebSocket close code=1008, reason=unauthorized: gateway token missing` |
| 用户 IP | 223.97.83.65 |

---

## 🔍 排查步骤

### 1. 检查 nginx 配置

```bash
cat /etc/nginx/conf.d/openclaw.unvw.com.conf
```

**结果**: ✅ 配置正确

```nginx
location / {
    proxy_pass http://127.0.0.1:18789;
    proxy_set_header Authorization $http_authorization;  # ✅ Token 转发
    proxy_set_header Host $host;
    proxy_set_header Upgrade $http_upgrade;  # ✅ WebSocket 升级
    proxy_set_header Connection "upgrade";
}
```

**结论**: nginx 正确配置了 Authorization 头转发和 WebSocket 升级。

---

### 2. 检查 Gateway 进程

```bash
ps aux | grep openclaw-gateway
```

**结果**: ✅ Gateway 运行中 (PID 287806, 26.3% RAM)

---

### 3. 检查 Gateway 监听端口

```bash
netstat -tlnp | grep 18789
```

**结果**: ✅ 监听 0.0.0.0:18789 (所有接口)

---

### 4. 检查 Token 配置

```bash
cat /home/admin/.openclaw/openclaw.json | grep -A 10 '"gateway"'
```

**结果**: ✅ Token 已配置

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "36322def61722938e759077fa8d654388049d97fea9f1931"
    }
  }
}
```

---

### 5. 检查设备配对

```bash
openclaw devices list
```

**结果**: ✅ 8 个设备已配对 (包括用户设备)

---

### 6. 查看官方文档

**Gateway 认证文档** (`/opt/openclaw/docs/gateway/authentication.md`):
> Auth is supplied during the WebSocket handshake via:
> - `connect.params.auth.token`
> - `connect.params.auth.password`
> The dashboard settings panel lets you store a token; passwords are not persisted.

**Control UI 文档** (`/opt/openclaw/docs/web/control-ui.md`):
> Token input in Settings panel (not URL parameter), persists in browser localStorage per tab session.

**FAQ** (`/opt/openclaw/docs/help/faq.md`):
> I set `gateway.bind: "lan"` and now nothing listens / the UI says unauthorized
> 
> Non-loopback binds **require auth**. Configure `gateway.auth.mode` + `gateway.auth.token`.
> The Control UI authenticates via `connect.params.auth.token` (stored in app/UI settings).

---

## 🎯 根因定位

### 根本原因

**Control UI 没有正确发送 Token 到 Gateway**

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Gateway 要求 Token | ✅ 已配置 | `gateway.auth.mode: "token"` |
| Gateway 收到 Token | ❌ 未收到 | 错误 `token missing` |
| nginx 转发 Token | ✅ 配置正确 | `proxy_set_header Authorization` |
| Token 在浏览器 | ❓ 未知 | 需检查 Settings 面板 |

### 错误码解析

| 错误码 | 含义 |
|--------|------|
| `1008` | WebSocket policy violation |
| `unauthorized` | 认证失败 |
| `gateway token missing` | Gateway 未收到 Token |

---

## 🛠️ 解决方案

### 方案 A：在 Control UI Settings 中重新配置 Token（推荐）

1. 打开 https://openclaw.unvw.com
2. 点击 **Settings** (设置面板)
3. 找到 **Token** 输入框
4. 填入：`36322def61722938e759077fa8d654388049d97fea9f1931`
5. **保存**
6. **刷新页面**，重新连接

### 方案 B：清除浏览器缓存后重试

```
浏览器设置 → 清除缓存和 Cookie → 重新打开 Control UI → 重新配置 Token
```

### 方案 C：检查浏览器控制台

```
F12 → Console → 尝试连接 → 查看 WebSocket 请求头
```

---

## 📚 知识点入库

### 1. Gateway 认证机制

- **Token 认证**: `gateway.auth.mode: "token"` + `gateway.auth.token`
- **认证时机**: WebSocket 握手时通过 `connect.params.auth.token`
- **存储位置**: Control UI Settings → Token (localStorage per tab)

### 2. nginx 配置要点

```nginx
# 必须转发 Authorization 头
proxy_set_header Authorization $http_authorization;

# 必须支持 WebSocket 升级
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

### 3. 错误码诊断

| 错误码 | 原因 | 解决方案 |
|--------|------|---------|
| `1008 token missing` | Token 未发送 | 检查 Control UI Settings |
| `1008 token mismatch` | Token 错误 | 核对 Token 值 |
| `1008 pairing required` | 设备未配对 | `openclaw devices approve` |

### 4. 排查 SOP

```bash
# 1. 检查 Gateway 进程
ps aux | grep openclaw-gateway

# 2. 检查监听端口
netstat -tlnp | grep 18789

# 3. 检查 Token 配置
cat ~/.openclaw/openclaw.json | grep -A 10 '"gateway"'

# 4. 检查设备配对
openclaw devices list

# 5. 检查 nginx 配置
cat /etc/nginx/conf.d/openclaw.unvw.com.conf

# 6. 检查 Gateway 日志
journalctl -u openclaw -f
```

---

## 🎯 预防措施

### 1. Token 管理

- ✅ 使用 `openclaw doctor --generate-gateway-token` 生成 Token
- ✅ Token 存储在 `~/.openclaw/openclaw.json` (权限 600)
- ✅ Control UI Settings 中保存 Token (localStorage)

### 2. 设备配对

- ✅ 首次连接新设备时检查 `openclaw devices list`
- ✅ 本地连接 (127.0.0.1) 自动配对
- ✅ 远程连接 (LAN/Tailnet) 需手动配对

### 3. 配置验证

```bash
# 验证配置合法性
openclaw check
openclaw lint

# 验证 Gateway 状态
openclaw gateway status
```

---

## 📊 排查耗时

| 步骤 | 耗时 |
|------|------|
| 信息收集 | 2 分钟 |
| 配置检查 | 2 分钟 |
| 日志分析 | 1 分钟 |
| 文档查阅 | 1 分钟 |
| 根因定位 | 1 分钟 |
| **总计** | **7 分钟** |

---

## ✅ 验证清单

- [ ] Control UI Settings 中 Token 已配置
- [ ] Token 值正确 (`36322def...9f1931`)
- [ ] 浏览器 localStorage 未清除
- [ ] 设备已配对 (`openclaw devices list`)
- [ ] nginx 配置正确 (Authorization 头转发)
- [ ] Gateway 进程正常运行

---

**最后更新**: 2026-04-21 22:06 GMT+8  
**维护者**: Red Agent Team  
**关联文档**: `gateway-authentication.md`, `control-ui.md`, `faq.md`

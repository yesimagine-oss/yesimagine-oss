# OpenClaw Gateway Trusted Proxy Auth 完整参考

**来源:** https://docs.openclaw.ai/gateway/trusted-proxy-auth  
**收录时间:** 2026-04-23 13:45 GMT+8  
**状态:** ✅ 完整 (可用于排障)  

---

## 🔐 错误码完整列表

| 错误码 | 含义 | 触发条件 | 修复方法 |
|--------|------|----------|----------|
| `trusted_proxy_untrusted_source` | 请求来源 IP 不在 trustedProxies 中 | 代理 IP 配置错误 | 检查并更新 trustedProxies |
| `trusted_proxy_loopback_source` | 请求来自回环地址 (127.0.0.1) | 同机代理不支持 | 使用 token auth 或非回环代理 |
| `trusted_proxy_user_missing` | 用户头为空或缺失 | 代理未传递身份头 | 检查代理配置 userHeader |
| `trusted_proxy_missing_header_*` | 必需头缺失 | requiredHeaders 未满足 | 检查代理传递的头 |
| `trusted_proxy_user_not_allowed` | 用户不在 allowUsers 列表中 | allowUsers 限制 | 添加用户或移除 allowUsers |
| `trusted_proxy_origin_not_allowed` | **Origin 未通过 Control UI 检查** | allowedOrigins 不匹配 | 添加 Origin 到 allowedOrigins |

---

## 📋 完整配置示例

### 基础配置

```json
{
  "gateway": {
    "bind": "lan",
    "trustedProxies": ["10.0.0.1", "172.17.0.1"],
    "auth": {
      "mode": "trusted-proxy",
      "trustedProxy": {
        "userHeader": "x-forwarded-user",
        "requiredHeaders": ["x-forwarded-proto", "x-forwarded-host"],
        "allowUsers": ["nick@example.com", "admin@company.org"]
      }
    },
    "controlUi": {
      "allowedOrigins": [
        "https://openclaw.unvw.com",
        "http://47.100.123.45:18789"
      ],
      "dangerouslyAllowHostHeaderOriginFallback": false
    }
  }
}
```

### 各代理配置示例

#### Pomerium

```json
{
  "gateway": {
    "bind": "lan",
    "trustedProxies": ["10.0.0.1"],
    "auth": {
      "mode": "trusted-proxy",
      "trustedProxy": {
        "userHeader": "x-pomerium-claim-email",
        "requiredHeaders": ["x-pomerium-jwt-assertion"]
      }
    }
  }
}
```

#### Caddy + OAuth

```json
{
  "gateway": {
    "bind": "lan",
    "trustedProxies": ["10.0.0.1"],
    "auth": {
      "mode": "trusted-proxy",
      "trustedProxy": {
        "userHeader": "x-forwarded-user"
      }
    }
  }
}
```

#### nginx + oauth2-proxy

```json
{
  "gateway": {
    "bind": "lan",
    "trustedProxies": ["10.0.0.1"],
    "auth": {
      "mode": "trusted-proxy",
      "trustedProxy": {
        "userHeader": "x-auth-request-email"
      }
    }
  }
}
```

#### Traefik

```json
{
  "gateway": {
    "bind": "lan",
    "trustedProxies": ["172.17.0.1"],
    "auth": {
      "mode": "trusted-proxy",
      "trustedProxy": {
        "userHeader": "x-forwarded-user"
      }
    }
  }
}
```

---

## 🔧 排障 SOP

### 步骤 1: 确认错误码

```bash
openclaw security audit 2>&1 | grep -E "trusted_proxy|CRITICAL|WARN"
```

### 步骤 2: 检查 trustedProxies

```bash
# 查看当前配置
cat ~/.openclaw/openclaw.json | jq '.gateway.trustedProxies'

# 查看代理实际 IP
docker inspect <proxy_container> | grep IPAddress
# 或
kubectl get pods -o wide | grep <proxy>
```

### 步骤 3: 检查用户头

```bash
# 测试代理是否传递头
curl -H "x-forwarded-user: test@example.com" \
  http://<gateway_ip>:18789/a2a/hello

# 查看 Gateway 日志
journalctl -u openclaw-gateway | grep -i "trusted.*proxy\|user.*header"
```

### 步骤 4: 检查 allowedOrigins

```bash
# 查看当前配置
cat ~/.openclaw/openclaw.json | jq '.gateway.controlUi.allowedOrigins'

# 浏览器 Origin 检查 (F12 Console)
# 查看请求头中的 Origin 字段
```

### 步骤 5: 验证修复

```bash
# 重启 Gateway
openclaw gateway restart

# 验证配置
openclaw gateway check-config

# 安全审计
openclaw security audit
```

---

## ⚠️ 常见错误与修复

### 错误 1: trusted_proxy_origin_not_allowed

**现象:** WebSocket 连接被拒绝，控制台显示 `origin not allowed`

**原因:** trusted-proxy 认证成功，但浏览器 Origin 未通过 Control UI 检查

**修复:**
```json
{
  "gateway": {
    "controlUi": {
      "allowedOrigins": [
        "https://openclaw.unvw.com",
        "http://<your_server_ip>:18789"
      ]
    }
  }
}
```

**验证:**
```bash
# 检查浏览器 Origin
# F12 → Network → WebSocket → Headers → Origin

# 确保 Origin 在 allowedOrigins 列表中
```

---

### 错误 2: trusted_proxy_loopback_source

**现象:** 认证失败，显示 `loopback source rejected`

**原因:** trusted-proxy auth 拒绝回环地址 (127.0.0.1, ::1)

**修复方案:**

| 方案 | 操作 | 适用场景 |
|------|------|----------|
| **方案 A** | 使用 token auth | 同机回环代理 |
| **方案 B** | 代理使用非回环 IP | Docker 桥接网络 |
| **方案 C** | 使用 Tailscale | 私有网络访问 |

**方案 A 示例:**
```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "your-shared-token"
    }
  }
}
```

---

### 错误 3: trusted_proxy_user_missing

**现象:** 认证失败，显示 `user header missing`

**原因:** 代理未传递用户身份头

**修复:**
1. 检查代理配置是否传递头
2. 确认 userHeader 名称正确
3. 验证用户已认证

**Pomerium 示例:**
```yaml
routes:
  - from: https://openclaw.example.com
    to: http://openclaw-gateway:18789
    policy:
      - allow:
          or:
            - email:
                is: nick@example.com
    pass_identity_headers: true  # 关键配置
```

---

### 错误 4: trusted_proxy_untrusted_source

**现象:** 认证失败，显示 `untrusted source IP`

**原因:** 请求来源 IP 不在 trustedProxies 列表中

**修复:**
```bash
# 1. 查找代理实际 IP
docker inspect <proxy> | grep IPAddress
# 或
kubectl get pods -o wide

# 2. 更新配置
# 编辑 ~/.openclaw/openclaw.json
# 添加代理 IP 到 trustedProxies

# 3. 重启 Gateway
openclaw gateway restart
```

---

## 🛡️ 安全检查清单

启用 trusted-proxy auth 前确认：

- [ ] **代理是唯一路径:** Gateway 端口对代理外防火墙封闭
- [ ] **trustedProxies 最小化:** 仅代理 IP，非整个子网
- [ ] **无回环代理源:** trusted-proxy auth 对回环请求失败关闭
- [ ] **代理剥离头:** 代理覆盖 (非追加) x-forwarded-* 头
- [ ] **TLS 终止:** 代理处理 TLS，用户通过 HTTPS 连接
- [ ] **allowedOrigins 明确:** 非回环 Control UI 使用明确 allowedOrigins
- [ ] **allowUsers 设置:** 推荐限制到已知用户
- [ ] **无混合 token 配置:** 不同时设置 token 和 trusted-proxy mode

---

## 📊 配置字段参考

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `gateway.trustedProxies` | ✅ | 代理 IP 数组 | `["10.0.0.1", "172.17.0.1"]` |
| `gateway.auth.mode` | ✅ | 必须为 `"trusted-proxy"` | `"trusted-proxy"` |
| `gateway.auth.trustedProxy.userHeader` | ✅ | 用户身份头名称 | `"x-forwarded-user"` |
| `gateway.auth.trustedProxy.requiredHeaders` | ❌ | 必需头列表 | `["x-forwarded-proto"]` |
| `gateway.auth.trustedProxy.allowUsers` | ❌ | 允许用户列表 | `["user@example.com"]` |
| `gateway.controlUi.allowedOrigins` | ❌ | Control UI Origin 白名单 | `["https://example.com"]` |
| `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback` | ❌ | Host-header 回退 (不推荐) | `false` |

---

## 🔗 相关文档

| 文档 | 位置 |
|------|------|
| **安全指南** | https://docs.openclaw.ai/gateway/security |
| **配置参考** | https://docs.openclaw.ai/gateway/configuration-reference |
| **远程访问** | https://docs.openclaw.ai/gateway/remote-access |
| **Tailscale** | https://docs.openclaw.ai/gateway/tailscale |
| **本报告** | `RedAgentTeamllm-wiki/wiki/gateway/trusted-proxy-auth.md` |

---

**收录状态:** ✅ 完整  
**可用性:** 可直接用于排障  
**最后更新:** 2026-04-23 13:45 GMT+8

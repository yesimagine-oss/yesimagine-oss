# OpenClaw WSL2 + Windows 浏览器远程 CDP 排障完整指南

**来源:** https://docs.openclaw.ai/tools/browser-wsl2-windows-remote-cdp-troubleshooting  
**收录时间:** 2026-04-23 14:26 GMT+8  
**状态:** ✅ 完整 (可用于 WSL2 跨主机浏览器排障)  

---

## 📋 概述

本指南适用于**分主机设置**场景：

| 组件 | 位置 |
|------|------|
| **OpenClaw Gateway** | WSL2 内运行 |
| **Chrome 浏览器** | Windows 上运行 |
| **浏览器控制** | 必须跨越 WSL2/Windows 边界 |

---

## 🎯 选择正确的浏览器模式

### 方案 A: WSL2 到 Windows 原始远程 CDP (推荐)

**使用场景:**
- Gateway 保持在 WSL2 内
- Chrome 运行在 Windows 上
- 需要浏览器控制跨越 WSL2/Windows 边界

**配置方式:** 使用远程浏览器配置文件指向 Windows Chrome CDP 端点

### 方案 B: 主机本地 Chrome MCP

**使用场景:**
- OpenClaw 和 Chrome 在同一台机器上
- 需要本地已登录浏览器状态
- 不需要跨主机浏览器传输
- 不需要高级托管/原始 CDP 功能 (responsebody, PDF 导出，下载拦截，批量操作)

**配置方式:** 使用 existing-session / user 配置文件

**重要:** 对于 WSL2 Gateway + Windows Chrome，**优先使用原始远程 CDP**。Chrome MCP 是主机本地的，不是 WSL2 到 Windows 的桥接。

---

## 🏗️ 工作架构

### 参考架构

```
┌─────────────────────────────────────────────────────────┐
│                    Windows Host                         │
│  ┌─────────────┐           ┌─────────────────────┐     │
│  │   Chrome    │──────────→│ CDP Endpoint :9222  │     │
│  │  (port 9222)│           │ (Windows accessible)│     │
│  └─────────────┘           └─────────────────────┘     │
│                              ↑                          │
│                              │ WSL2 can reach           │
│  ┌───────────────────────┐  │                          │
│  │  Control UI Browser   │  │                          │
│  │  http://127.0.0.1:18789│  │                          │
│  └───────────────────────┘  │                          │
└──────────────────────────────┼──────────────────────────┘
                               │
┌──────────────────────────────┼──────────────────────────┐
│                    WSL2       │                          │
│  ┌───────────────────────┐   │                          │
│  │  OpenClaw Gateway     │←──┘                          │
│  │  127.0.0.1:18789      │                              │
│  │  browser.cdpUrl =     │                              │
│  │  http://WIN_HOST:9222 │                              │
│  └───────────────────────┘                              │
└─────────────────────────────────────────────────────────┘
```

### 关键配置点

| 组件 | 配置 | 说明 |
|------|------|------|
| **Windows Chrome** | `--remote-debugging-port=9222` | 暴露 CDP 端点 |
| **WSL2 Gateway** | `browser.profiles.remote.cdpUrl` | 指向 Windows 可达地址 |
| **Control UI** | `http://127.0.0.1:18789/` | 使用 Windows localhost |
| **防火墙** | 允许 9222 端口 | Windows 防火墙规则 |

---

## 🔍 分层验证流程

### 第 1 层：验证 Chrome 在 Windows 上提供 CDP

**步骤 1: 启动 Chrome (Windows)**

```powershell
# PowerShell 或 CMD
chrome.exe --remote-debugging-port=9222
```

**步骤 2: 从 Windows 验证 Chrome**

```powershell
# 验证 Chrome 本身
curl http://127.0.0.1:9222/json/version
curl http://127.0.0.1:9222/json/list
```

**预期结果:**
- `/json/version` 返回包含 `Browser` / `Protocol-Version` 元数据的 JSON
- `/json/list` 返回 JSON (如果没有打开页面，空数组也可以)

**如失败:**
- Chrome 未正确启动
- 端口被占用
- **这不是 OpenClaw 问题** — 先修复 Chrome

---

### 第 2 层：验证 WSL2 可以到达 Windows 端点

**步骤 1: 从 WSL2 测试**

```bash
# 从 WSL2 测试你计划在 cdpUrl 中使用的确切地址
curl http://WINDOWS_HOST_OR_IP:9222/json/version
curl http://WINDOWS_HOST_OR_IP:9222/json/list
```

**获取 Windows 主机地址:**

```bash
# 从 WSL2 获取 Windows 主机 IP
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
# 或使用
hostname.exe -I | cut -d' ' -f1
```

**预期结果:**
- `/json/version` 返回 JSON
- `/json/list` 返回 JSON

**如失败:**
- Windows 未向 WSL2 暴露端口
- 地址对 WSL2 侧不正确
- 防火墙/端口转发/本地代理仍然缺失

**修复方法:**

```powershell
# Windows 防火墙允许 9222 端口
New-NetFirewallRule -DisplayName "Chrome CDP" -Direction Inbound -LocalPort 9222 -Protocol TCP -Action Allow

# 或使用 netsh (旧版 Windows)
netsh advfirewall firewall add rule name="Chrome CDP" dir=in action=allow protocol=TCP localport=9222
```

**在触碰 OpenClaw 配置之前先修复网络连通性。**

---

### 第 3 层：配置正确的浏览器配置文件

**对于原始远程 CDP，将 OpenClaw 指向从 WSL2 可达的地址:**

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "remote",
    "profiles": {
      "remote": {
        "cdpUrl": "http://WINDOWS_HOST_OR_IP:9222",
        "attachOnly": true,
        "color": "#00AA00"
      }
    }
  }
}
```

**重要说明:**

| 配置项 | 说明 |
|--------|------|
| **cdpUrl** | 使用从 WSL2 可达的地址，而非仅在 Windows 上有效的地址 |
| **attachOnly** | 对外部管理的浏览器保持 `true` |
| **协议** | cdpUrl 可以是 `http://`, `https://`, `ws://`, 或 `wss://` |
| **HTTP(S)** | 当你想让 OpenClaw 发现 `/json/version` 时使用 |
| **WS(S)** | 仅当浏览器提供商给你直接 DevTools socket URL 时使用 |

**测试:** 在期望 OpenClaw 成功之前，先用 curl 测试相同的 URL。

---

### 第 4 层：单独验证 Control UI 层

**从 Windows 打开 UI:**

```
http://127.0.0.1:18789/
```

**验证:**
- 页面来源与 `gateway.controlUi.allowedOrigins` 预期匹配
- token 认证或配对配置正确
- 你不是在调试 Control UI 认证问题 (误以为是浏览器问题)

**关键规则:**
- 当从 Windows 打开 UI 时，**使用 Windows localhost**，除非你有故意的 HTTPS 设置
- **不要**默认使用 LAN IP 作为 Control UI
- 纯 HTTP 在 LAN 或 tailnet 地址上可能触发不安全来源/设备认证行为 (与 CDP 本身无关)

---

### 第 5 层：验证端到端浏览器控制

**从 WSL2 测试:**

```bash
# 打开网页
openclaw browser open https://example.com --browser-profile remote

# 列出标签页
openclaw browser tabs --browser-profile remote
```

**预期结果:**
- 标签页在 Windows Chrome 中打开
- `openclaw browser tabs` 返回目标
- 后续操作 (snapshot, screenshot, navigate) 在同一配置文件中工作

---

## 🔴 常见问题排障

### 问题 1: WSL2 无法到达 Windows CDP 端点

| 项目 | 内容 |
|------|------|
| **现象** | `curl http://WIN_HOST:9222/json/version` 失败 |
| **原因** | Windows 防火墙阻止/端口未转发 |
| **解决** | 配置防火墙和端口转发 |

**步骤:**

```powershell
# 1. 允许防火墙
New-NetFirewallRule -DisplayName "Chrome CDP" -Direction Inbound -LocalPort 9222 -Protocol TCP -Action Allow

# 2. 验证 Chrome 启动
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome-cdp"

# 3. 从 Windows 测试
curl http://127.0.0.1:9222/json/version

# 4. 从 WSL2 测试
curl http://$(hostname.exe -I | cut -d' ' -f1 | tr -d '\r'):9222/json/version
```

---

### 问题 2: Control UI 不安全来源认证

| 项目 | 内容 |
|------|------|
| **现象** | `control-ui-insecure-auth` 错误 |
| **原因** | UI 来源/安全上下文问题 |
| **解决** | 使用正确的 URL 打开 Control UI |

**步骤:**

```bash
# ❌ 错误：使用 LAN IP
http://192.168.1.100:18789/

# ✅ 正确：使用 localhost
http://127.0.0.1:18789/
```

**如需要 LAN 访问，配置 allowedOrigins:**

```json
{
  "gateway": {
    "controlUi": {
      "allowedOrigins": [
        "http://127.0.0.1:18789",
        "http://192.168.1.100:18789"
      ]
    }
  }
}
```

---

### 问题 3: Token 缺失或配对问题

| 项目 | 内容 |
|------|------|
| **现象** | `token_missing` 或 `pairing required` 错误 |
| **原因** | 认证配置问题/设备批准问题 |
| **解决** | 配置 token 或完成配对 |

**步骤:**

```bash
# 获取配对码
openclaw devices list

# 批准设备
openclaw devices approve <requestId>

# 或使用 token 认证
openclaw config set gateway.auth.token "your-token"
```

---

### 问题 4: 远程 CDP 不可达

| 项目 | 内容 |
|------|------|
| **现象** | `Remote CDP for profile "remote" is not reachable` |
| **原因** | WSL2 无法到达配置的 cdpUrl |
| **解决** | 验证网络和配置 |

**步骤:**

```bash
# 1. 验证 cdpUrl 可达
curl http://WINDOWS_HOST:9222/json/version

# 2. 检查配置
cat ~/.openclaw/openclaw.json | jq '.browser.profiles.remote'

# 3. 确保 attachOnly: true
# 4. 重启 Gateway
openclaw gateway restart
```

---

### 问题 5: CDP WebSocket 不可达

| 项目 | 内容 |
|------|------|
| **现象** | `Browser attachOnly is enabled and CDP websocket for profile "remote" is not reachable` |
| **原因** | HTTP 端点响应，但 DevTools WebSocket 仍无法打开 |
| **解决** | 检查 WebSocket 连通性 |

**步骤:**

```bash
# 1. 获取 WebSocket URL
curl http://WINDOWS_HOST:9222/json/version | jq -r '.webSocketDebuggerUrl'

# 2. 测试 WebSocket 连通性
# 使用 wscat 或类似工具
wscat -c "ws://WINDOWS_HOST:9222/devtools/browser/<id>"

# 3. 检查防火墙是否允许 WebSocket
```

---

### 问题 6: 陈旧的视图/深色模式/语言/离线覆盖

| 项目 | 内容 |
|------|------|
| **现象** | 远程会话后出现陈旧的 viewport/dark-mode/locale/offline 覆盖 |
| **原因** | Playwright/CDP 模拟状态未清除 |
| **解决** | 停止浏览器配置文件 |

**步骤:**

```bash
# 停止配置文件 (关闭活动控制会话)
openclaw browser stop --browser-profile remote

# 这会关闭活动控制会话并释放 Playwright/CDP 模拟状态
# 无需重启 Gateway 或外部浏览器
```

---

### 问题 7: Gateway 超时 1500ms

| 项目 | 内容 |
|------|------|
| **现象** | `gateway timeout after 1500ms` |
| **原因** | 通常是 CDP 可达性问题或远程端点慢/不可达 |
| **解决** | 增加超时或优化网络 |

**步骤:**

```json
{
  "browser": {
    "remoteCdpTimeoutMs": 3000,
    "remoteCdpHandshakeTimeoutMs": 5000
  }
}
```

---

### 问题 8: 无 Chrome 标签页可用

| 项目 | 内容 |
|------|------|
| **现象** | `No Chrome tabs found for profile="user"` |
| **原因** | 选择了本地 Chrome MCP 配置文件，但没有主机本地标签页可用 |
| **解决** | 使用远程 CDP 或打开标签页 |

**步骤:**

```bash
# 方案 A: 使用远程配置文件
openclaw browser open https://example.com --browser-profile remote

# 方案 B: 在本地 Chrome 中打开标签页
# 然后重试 user 配置文件
```

---

## 📋 快速排障清单

### 5 步验证

| 步骤 | 检查 | 命令 |
|------|------|------|
| **1** | Windows: Chrome CDP 工作？ | `curl http://127.0.0.1:9222/json/version` |
| **2** | WSL2: 可达 Windows 端点？ | `curl http://WIN_HOST:9222/json/version` |
| **3** | OpenClaw 配置：cdpUrl 使用 WSL2 可达地址？ | `jq '.browser.profiles.remote.cdpUrl'` |
| **4** | Control UI: 使用 `http://127.0.0.1:18789/` 而非 LAN IP？ | 检查浏览器地址栏 |
| **5** | 是否尝试跨 WSL2 和 Windows 使用 existing-session 而非原始远程 CDP？ | 检查配置文件类型 |

---

## 🔍 错误消息分层解读

| 错误消息 | 层别 | 说明 |
|----------|------|------|
| `control-ui-insecure-auth` | UI 层 | UI 来源/安全上下文问题，**非** CDP 传输问题 |
| `token_missing` | 认证层 | 认证配置问题 |
| `pairing required` | 设备层 | 设备批准问题 |
| `Remote CDP for profile "remote" is not reachable` | CDP 层 | WSL2 无法到达配置的 cdpUrl |
| `CDP websocket ... is not reachable` | WebSocket 层 | HTTP 端点响应，但 WebSocket 无法打开 |
| `stale viewport / dark-mode` | 状态层 | Playwright/CDP 模拟状态未清除 |
| `gateway timeout after 1500ms` | 网络层 | CDP 可达性问题或远程端点慢 |
| `No Chrome tabs found for profile="user"` | 配置文件层 | 选择了本地 MCP 配置文件，无可用标签页 |

---

## 📊 配置参考

### 完整配置示例

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "remote",
    "remoteCdpTimeoutMs": 3000,
    "remoteCdpHandshakeTimeoutMs": 5000,
    "profiles": {
      "remote": {
        "cdpUrl": "http://192.168.1.100:9222",
        "attachOnly": true,
        "color": "#00AA00"
      },
      "openclaw": {
        "cdpPort": 18800,
        "color": "#FF4500"
      }
    }
  },
  "gateway": {
    "controlUi": {
      "allowedOrigins": [
        "http://127.0.0.1:18789",
        "http://192.168.1.100:18789"
      ]
    }
  }
}
```

### cdpUrl 格式

| 格式 | 用途 | 示例 |
|------|------|------|
| `http://host:port` | HTTP 发现 | `http://192.168.1.100:9222` |
| `https://host:port` | HTTPS 发现 | `https://browser.example.com` |
| `ws://host:port/devtools/...` | 直接 WebSocket | `ws://localhost:9222/devtools/browser/abc123` |
| `wss://host:port?token=xxx` | 托管服务 | `wss://browserless.io?token=xxx` |

---

## 🛠️ 验证命令

### Windows 侧

```powershell
# 启动 Chrome
chrome.exe --remote-debugging-port=9222

# 验证 Chrome CDP
curl http://127.0.0.1:9222/json/version
curl http://127.0.0.1:9222/json/list

# 允许防火墙
New-NetFirewallRule -DisplayName "Chrome CDP" -Direction Inbound -LocalPort 9222 -Protocol TCP -Action Allow

# 获取 Windows IP
hostname.exe -I | cut -d' ' -f1
```

### WSL2 侧

```bash
# 获取 Windows 主机 IP
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'

# 验证 CDP 可达性
curl http://WIN_HOST:9222/json/version

# 测试浏览器控制
openclaw browser open https://example.com --browser-profile remote
openclaw browser tabs --browser-profile remote

# 停止配置文件 (清除陈旧状态)
openclaw browser stop --browser-profile remote
```

---

## 🌐 实用场景

### 场景 A: WSL2 开发 + Windows 浏览器

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "remote",
    "profiles": {
      "remote": {
        "cdpUrl": "http://$(hostname.exe -I | cut -d' ' -f1):9222",
        "attachOnly": true
      }
    }
  }
}
```

### 场景 B: 纯本地 WSL2 (无跨主机)

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "profiles": {
      "openclaw": {
        "cdpPort": 18800
      }
    }
  }
}
```

### 场景 C: 托管浏览器服务 (Browserless/Browserbase)

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "browserless",
    "profiles": {
      "browserless": {
        "cdpUrl": "wss://production-sfo.browserless.io?token=<API_KEY>"
      }
    }
  }
}
```

---

## 🛡️ 安全注意事项

| 安全项 | 说明 |
|--------|------|
| **CDP 暴露** | 仅向受信任网络暴露 9222 端口 |
| **防火墙** | Windows 防火墙应仅允许 WSL2 子网 |
| **Token 认证** | 使用 gateway.auth.token 保护 Control UI |
| **allowedOrigins** | 明确列出允许的 UI 来源 |
| **远程 CDP** | 使用 HTTPS/WSS 和短令牌 |

---

## 📝 快速参考

### 常用命令

```bash
# WSL2: 获取 Windows 主机 IP
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'

# Windows: 启动 Chrome CDP
chrome.exe --remote-debugging-port=9222

# Windows: 允许防火墙
New-NetFirewallRule -DisplayName "Chrome CDP" -Direction Inbound -LocalPort 9222 -Protocol TCP -Action Allow

# WSL2: 验证 CDP 可达性
curl http://WIN_HOST:9222/json/version

# WSL2: 测试浏览器控制
openclaw browser open https://example.com --browser-profile remote

# WSL2: 停止配置文件 (清除陈旧状态)
openclaw browser stop --browser-profile remote

# WSL2: 重启 Gateway
openclaw gateway restart
```

### 配置速查

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "remote",
    "remoteCdpTimeoutMs": 3000,
    "remoteCdpHandshakeTimeoutMs": 5000,
    "profiles": {
      "remote": {
        "cdpUrl": "http://WIN_HOST:9222",
        "attachOnly": true
      }
    }
  },
  "gateway": {
    "controlUi": {
      "allowedOrigins": ["http://127.0.0.1:18789"]
    }
  }
}
```

---

## 🔗 相关文档

| 文档 | 位置 |
|------|------|
| **Linux 浏览器排障** | `RedAgentTeamllm-wiki/wiki/tools/browser-linux-troubleshooting.md` |
| **沙箱浏览器** | `RedAgentTeamllm-wiki/wiki/gateway/sandboxing.md` |
| **Control UI** | https://docs.openclaw.ai/gateway/control-ui |
| **远程 CDP** | `RedAgentTeamllm-wiki/wiki/gateway/sandboxing.md` → 远程 CDP 章节 |
| **本报告** | `RedAgentTeamllm-wiki/wiki/tools/browser-wsl2-cdp-troubleshooting.md` |

---

**收录状态:** ✅ 完整  
**可用性:** 可直接用于 WSL2 + Windows 跨主机浏览器排障  
**最后更新:** 2026-04-23 14:26 GMT+8

# OpenClaw Linux 浏览器工具排障完整指南

**来源:** https://docs.openclaw.ai/tools/browser-linux-troubleshooting  
**收录时间:** 2026-04-23 14:21 GMT+8  
**状态:** ✅ 完整 (可用于 Linux 浏览器问题排障)  

---

## 📋 概述

OpenClaw 浏览器控制服务在 Linux 上可能遇到启动失败、依赖缺失、Snap 沙盒干扰等问题。本文档提供完整排障流程。

---

## 🔴 问题 1: "Failed to start Chrome CDP on port 18800"

### 现象

```json
{
  "error": "Error: Failed to start Chrome CDP on port 18800 for profile \"openclaw\"."
}
```

### 根因

在 Ubuntu (及许多 Linux 发行版) 上，默认 Chromium 安装是 **Snap 包**。Snap 的 AppArmor 限制干扰 OpenClaw 启动和监控浏览器进程的方式。

**关键问题:**
```bash
# apt install chromium 安装的是存根包，重定向到 Snap
Note, selecting 'chromium-browser' instead of 'chromium'
chromium-browser is already the newest version (2:1snap1-0ubuntu2)
```

**这不是真正的浏览器 — 只是 Snap 包装器。**

---

### 解决方案 A: 安装 Google Chrome (推荐)

**步骤 1: 下载并安装**

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # 如有依赖错误
```

**步骤 2: 验证安装**

```bash
which google-chrome-stable
# 输出：/usr/bin/google-chrome-stable

google-chrome-stable --version
# 输出：Google Chrome 120.0.xxxx.xx
```

**步骤 3: 更新 OpenClaw 配置**

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true
  }
}
```

**步骤 4: 重启 Gateway**

```bash
openclaw gateway restart
```

**步骤 5: 验证浏览器工作**

```bash
# 检查状态
curl -s http://127.0.0.1:18791/ | jq '{running, pid, chosenBrowser}'

# 测试浏览
curl -s -X POST http://127.0.0.1:18791/start
curl -s http://127.0.0.1:18791/tabs
```

---

### 解决方案 B: 使用 Snap Chromium (仅附加模式)

如必须使用 Snap Chromium，配置 OpenClaw 附加到手动启动的浏览器。

**步骤 1: 更新配置**

```json
{
  "browser": {
    "enabled": true,
    "attachOnly": true,
    "headless": true,
    "noSandbox": true
  }
}
```

**步骤 2: 手动启动 Chromium**

```bash
chromium-browser --headless --no-sandbox --disable-gpu \
  --remote-debugging-port=18800 \
  --user-data-dir=$HOME/.openclaw/browser/openclaw/user-data \
  about:blank &
```

**步骤 3: (可选) 创建 systemd 用户服务自动启动**

创建文件 `~/.config/systemd/user/openclaw-browser.service`:

```ini
[Unit]
Description=OpenClaw Browser (Chrome CDP)
After=network.target

[Service]
ExecStart=/snap/bin/chromium --headless --no-sandbox --disable-gpu --remote-debugging-port=18800 --user-data-dir=%h/.openclaw/browser/openclaw/user-data about:blank
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

**启用服务:**

```bash
systemctl --user enable --now openclaw-browser.service
```

---

## 🔴 问题 2: "No Chrome tabs found for profile='user'"

### 现象

使用现有会话/Chrome MCP 配置文件时，OpenClaw 能看到本地 Chrome，但没有可用标签页附加。

### 根因

`user` 配置文件是仅主机的 Chrome MCP 附加模式，需要本地 Chrome 已运行且至少有一个打开的标签页。

### 解决方案

**方案 A: 使用托管浏览器**

```bash
openclaw browser start --browser-profile openclaw
```

或设置默认配置文件：

```json
{
  "browser": {
    "defaultProfile": "openclaw"
  }
}
```

**方案 B: 确保 Chrome 已运行**

1. 手动打开 Chrome，确保至少有一个标签页
2. 重试 `--browser-profile user`

---

## 🔴 问题 3: 浏览器命令缺失

### 现象

```bash
$ openclaw browser
openclaw: 'browser' is not an openclaw command.
```

或 Agent 报告浏览器工具不可用。

### 根因

**最常见原因:** `plugins.allow` 限制列表未包含 `browser`。

**错误配置示例:**

```json
{
  "plugins": {
    "allow": ["telegram"]  // ❌ 缺少 browser
  }
}
```

### 解决方案

**步骤 1: 添加 browser 到允许列表**

```json
{
  "plugins": {
    "allow": ["telegram", "browser"]  // ✅ 添加 browser
  }
}
```

**步骤 2: 确保插件启用**

```json
{
  "plugins": {
    "entries": {
      "browser": {
        "enabled": true
      }
    }
  }
}
```

**步骤 3: 确保 browser.enabled=true**

```json
{
  "browser": {
    "enabled": true
  }
}
```

**重要说明:**

| 配置 | 是否足够 | 说明 |
|------|----------|------|
| `browser.enabled=true` | ❌ 否 | `plugins.allow` 设置时无效 |
| `plugins.entries.browser.enabled=true` | ❌ 否 | `plugins.allow` 设置时无效 |
| `tools.alsoAllow: ["browser"]` | ❌ 否 | 仅调整工具策略，不加载插件 |
| 移除 `plugins.allow` | ✅ 是 | 恢复默认行为 |

**步骤 4: 重启 Gateway**

```bash
openclaw gateway restart
```

---

## 🔴 问题 4: 依赖缺失

### 现象

```bash
Error: Failed to launch browser: error while loading shared libraries: libnss3.so
```

### 根因

Linux 上 Chrome/Chromium 需要额外系统依赖。

### 解决方案

**安装依赖 (Debian/Ubuntu):**

```bash
sudo apt-get update
sudo apt-get install -y \
  libnss3 \
  libnspr4 \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libcups2 \
  libdrm2 \
  libxkbcommon0 \
  libxcomposite1 \
  libxdamage1 \
  libxfixes3 \
  libxrandr2 \
  libgbm1 \
  libasound2 \
  libpango-1.0-0 \
  libcairo2
```

**或使用 Chrome 一键安装依赖:**

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y  # 自动安装缺失依赖
```

---

## 🔴 问题 5: 沙盒权限错误

### 现象

```bash
[ERROR:zygote_host_impl_linux.cc(100)] Running as root without --no-sandbox is not supported.
```

### 根因

在容器或 root 用户下运行时，Chrome 沙盒与运行环境冲突。

### 解决方案

**方案 A: 使用 --no-sandbox (推荐用于容器)**

```json
{
  "browser": {
    "noSandbox": true
  }
}
```

**方案 B: 使用非 root 用户运行**

```bash
# 创建专用用户
sudo useradd -m openclaw-browser
sudo chown -R openclaw-browser:openclaw-browser /path/to/openclaw

# 切换到该用户运行
sudo -u openclaw-browser openclaw gateway start
```

**方案 C: 使用 headless 模式**

```json
{
  "browser": {
    "headless": true,
    "noSandbox": true
  }
}
```

---

## 📊 配置参考

### browser.* 配置项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `browser.enabled` | 启用浏览器控制 | `true` |
| `browser.executablePath` | Chrome/Chromium 二进制路径 | 自动检测 |
| `browser.headless` | 无头模式运行 | `false` |
| `browser.noSandbox` | 添加 --no-sandbox 标志 | `false` |
| `browser.attachOnly` | 不启动浏览器，仅附加到现有 | `false` |
| `browser.cdpPort` | Chrome DevTools Protocol 端口 | `18800` |
| `browser.defaultProfile` | 默认浏览器配置文件 | `"openclaw"` |
| `browser.remoteCdpTimeoutMs` | 远程 CDP HTTP 超时 (ms) | `1500` |
| `browser.remoteCdpHandshakeTimeoutMs` | 远程 CDP WebSocket 握手超时 (ms) | `3000` |

### profiles 配置

```json
{
  "browser": {
    "profiles": {
      "openclaw": {
        "cdpPort": 18800,
        "color": "#FF4500"
      },
      "work": {
        "cdpPort": 18801,
        "color": "#0066CC"
      },
      "user": {
        "driver": "existing-session",
        "attachOnly": true,
        "color": "#00AA00"
      },
      "remote": {
        "cdpUrl": "http://10.0.0.42:9222",
        "color": "#00AA00"
      }
    }
  }
}
```

---

## 🛠️ 验证命令

### 检查浏览器状态

```bash
# 检查浏览器控制服务
curl -s http://127.0.0.1:18791/ | jq '{running, pid, chosenBrowser}'

# 列出标签页
curl -s http://127.0.0.1:18791/tabs | jq '.'

# 启动浏览器
curl -s -X POST http://127.0.0.1:18791/start

# 停止浏览器
curl -s -X POST http://127.0.0.1:18791/stop
```

### 使用 CLI 命令

```bash
# 检查状态
openclaw browser --browser-profile openclaw status

# 启动浏览器
openclaw browser --browser-profile openclaw start

# 打开网页
openclaw browser --browser-profile openclaw open https://example.com

# 获取快照
openclaw browser --browser-profile openclaw snapshot

# 截图
openclaw browser --browser-profile openclaw screenshot --output /tmp/screenshot.png
```

### 检查进程

```bash
# 查找浏览器进程
ps aux | grep -E "(chrome|chromium|google-chrome)" | grep -v grep

# 查找 CDP 端口
netstat -tlnp | grep 18800  # Chrome DevTools Protocol 默认端口
```

### 查看日志

```bash
# Gateway 日志 (浏览器相关)
journalctl -u openclaw-gateway -f | grep -i "browser\|cdp\|chrome"

# 浏览器日志
ls -la /tmp/openclaw/ | grep -i browser
cat /tmp/openclaw/*.log | grep -i "browser.*error" | tail -20
```

---

## 🔍 排障流程图

```
浏览器启动失败
    ↓
检查错误消息
    ↓
┌─────────────────────────────────────┐
│ "Failed to start Chrome CDP"        │
│ → Snap 问题 → 安装 Google Chrome    │
├─────────────────────────────────────┤
│ "No Chrome tabs found"              │
│ → 确保 Chrome 运行且有标签页         │
├─────────────────────────────────────┤
│ "browser is not an openclaw command"│
│ → 检查 plugins.allow 包含 browser   │
├─────────────────────────────────────┤
│ "libnss3.so not found"              │
│ → 安装依赖                          │
├─────────────────────────────────────┤
│ "Running as root without --no-sandbox"│
│ → 添加 noSandbox: true             │
└─────────────────────────────────────┘
    ↓
验证修复
    ↓
curl http://127.0.0.1:18791/
```

---

## 🌐 远程 CDP 配置

### Browserless (托管服务)

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "browserless",
    "remoteCdpTimeoutMs": 2000,
    "remoteCdpHandshakeTimeoutMs": 4000,
    "profiles": {
      "browserless": {
        "cdpUrl": "wss://production-sfo.browserless.io?token=<BROWSERLESS_API_KEY>",
        "color": "#00AA00"
      }
    }
  }
}
```

### Browserbase (云服务)

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "browserbase",
    "remoteCdpTimeoutMs": 3000,
    "remoteCdpHandshakeTimeoutMs": 5000,
    "profiles": {
      "browserbase": {
        "cdpUrl": "wss://connect.browserbase.com?apiKey=<BROWSERBASE_API_KEY>",
        "color": "#F97316"
      }
    }
  }
}
```

### 自定义远程 CDP

```json
{
  "browser": {
    "enabled": true,
    "profiles": {
      "remote": {
        "cdpUrl": "http://10.0.0.42:9222",
        "color": "#00AA00"
      }
    }
  }
}
```

---

## 🛡️ 安全注意事项

| 安全项 | 说明 |
|--------|------|
| **回环限制** | 浏览器控制仅绑定到 loopback (127.0.0.1) |
| **认证方式** | Gateway token bearer auth / x-openclaw-password / HTTP Basic |
| **SSRF 防护** | 导航前 SSRF 检查，最佳努力最终 URL 检查 |
| **远程 CDP** | 使用 HTTPS/WSS 和短令牌，避免在配置中嵌入长令牌 |
| **私有网络** | `dangerouslyAllowPrivateNetwork: true` 仅用于受信任私有网络 |

---

## 📋 快速参考

### 常用命令

```bash
# 安装 Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y

# 安装依赖
sudo apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2

# 检查浏览器状态
openclaw browser --browser-profile openclaw status

# 启动浏览器
openclaw browser --browser-profile openclaw start

# 重启 Gateway
openclaw gateway restart

# 查看日志
journalctl -u openclaw-gateway -f | grep -i browser
```

### 配置速查

```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true,
    "defaultProfile": "openclaw"
  },
  "plugins": {
    "allow": ["browser"],
    "entries": {
      "browser": {
        "enabled": true
      }
    }
  }
}
```

---

## 🔗 相关文档

| 文档 | 位置 |
|------|------|
| **浏览器主文档** | https://docs.openclaw.ai/tools/browser |
| **沙箱浏览器** | `RedAgentTeamllm-wiki/wiki/gateway/sandboxing.md` |
| **Gateway 配置** | `RedAgentTeamllm-wiki/wiki/gateway/configuration-reference.md` |
| **本报告** | `RedAgentTeamllm-wiki/wiki/tools/browser-linux-troubleshooting.md` |

---

**收录状态:** ✅ 完整  
**可用性:** 可直接用于 Linux 浏览器问题排障  
**最后更新:** 2026-04-23 14:21 GMT+8

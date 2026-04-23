# OpenClaw Docker 安装完整指南

**来源:** https://docs.openclaw.ai/install/docker  
**收录时间:** 2026-04-23 13:58 GMT+8  
**状态:** ✅ 完整 (可用于实际部署)  

---

## 📋 前置要求

| 项目 | 要求 | 说明 |
|------|------|------|
| **Docker** | Docker Desktop / Docker Engine | 必需 |
| **Docker Compose** | v2+ | 必需 |
| **内存** | ≥2 GB RAM | 镜像构建需要 (1GB 可能 OOM) |
| **磁盘** | 足够镜像和日志 | 建议 ≥10GB |
| **网络** | 防火墙配置 | VPS/公网需查看安全加固 |

---

## 🚀 两种安装方式

### 方式 A: 容器化 Gateway (推荐)

**适用场景:** 隔离环境、无需本地安装

| 特点 | 说明 |
|------|------|
| **隔离性** | ✅ 完全隔离 |
| **可移植性** | ✅ 高 |
| **管理方式** | Docker Compose |
| **技术门槛** | 🟡 中等 |

#### 安装步骤

**步骤 1: 构建镜像**

```bash
# 方式 A: 本地构建
./scripts/docker/setup.sh

# 方式 B: 使用预构建镜像
export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"
./scripts/docker/setup.sh
```

**预构建镜像标签:**
| 标签 | 说明 |
|------|------|
| `main` | 主分支最新 |
| `latest` | 最新稳定版 |
| `<version>` | 特定版本 (如 2026.2.26) |

**步骤 2: 完成 Onboarding**

设置脚本自动运行 onboarding:
- 提示输入 API 密钥
- 生成 gateway token 并写入 `.env`
- 通过 Docker Compose 启动 gateway

**步骤 3: 打开 Control UI**

```
http://127.0.0.1:18789/
```

粘贴配置的共享密钥到设置中。

**获取 URL (如需要):**
```bash
docker compose run --rm openclaw-cli dashboard --no-open
```

**步骤 4: 配置渠道 (可选)**

```bash
# WhatsApp (扫码)
docker compose run --rm openclaw-cli channels login

# Telegram
docker compose run --rm openclaw-cli channels add --channel telegram --token "<token>"

# Discord
docker compose run --rm openclaw-cli channels add --channel discord --token "<token>"
```

---

### 方式 B: 手动流程

**适用场景:** 需要完全控制

```bash
# 1. 构建镜像
docker build -t openclaw:local -f Dockerfile .

# 2. 运行 onboarding
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js onboard --mode local --no-install-daemon

# 3. 配置 gateway
docker compose run --rm --no-deps --entrypoint node openclaw-gateway \
  dist/index.js config set --batch-json '[
    {"path":"gateway.mode","value":"local"},
    {"path":"gateway.bind","value":"lan"},
    {"path":"gateway.controlUi.allowedOrigins","value":["http://localhost:18789","http://127.0.0.1:18789"]}
  ]'

# 4. 启动 gateway
docker compose up -d openclaw-gateway
```

---

## 🧪 Agent Sandbox 配置

### 什么是 Agent Sandbox?

当 `agents.defaults.sandbox` 启用时，gateway 在隔离的 Docker 容器中运行 agent 工具执行 (shell、文件读写等)，而 gateway 本身保持在主机上。

| 特性 | 说明 |
|------|------|
| **隔离级别** | 硬隔离 (Docker 容器) |
| **适用范围** | 非信任或多租户 agent 会话 |
| **沙箱范围** | per-agent / per-session / shared |
| **工作区挂载** | /workspace |

### 快速启用

**步骤 1: 设置环境变量**

```bash
export OPENCLAW_SANDBOX=1
./scripts/docker/setup.sh
```

**自定义 Docker Socket 路径 (如 rootless Docker):**

```bash
export OPENCLAW_SANDBOX=1
export OPENCLAW_DOCKER_SOCKET=/run/user/1000/docker.sock
./scripts/docker/setup.sh
```

**步骤 2: 配置沙箱**

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "scope": "agent"
      }
    }
  }
}
```

**沙箱模式选项:**

| 模式 | 说明 |
|------|------|
| `off` | 禁用沙箱 |
| `non-main` | 仅非主 agent 使用沙箱 (推荐) |
| `all` | 所有 agent 使用沙箱 |

**沙箱范围选项:**

| 范围 | 说明 |
|------|------|
| `agent` | 每个 agent 独立沙箱 (默认) |
| `session` | 每个会话独立沙箱 |
| `shared` | 共享沙箱 |

### 构建沙箱镜像

```bash
scripts/sandbox-setup.sh
```

### 沙箱配置参考

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "scope": "agent",
        "docker": {
          "image": "openclaw/sandbox:latest",
          "user": "1000:1000",
          "network": "isolated",
          "resources": {
            "memory": "512m",
            "cpu": "0.5"
          }
        }
      }
    }
  }
}
```

---

## 🛠️ 管理操作

### 健康检查

**基础检查 (无需认证):**

```bash
# Liveness 检查
curl -fsS http://127.0.0.1:18789/healthz

# Readiness 检查
curl -fsS http://127.0.0.1:18789/readyz
```

**深度检查 (需要认证):**

```bash
docker compose exec openclaw-gateway node dist/index.js health --token "$OPENCLAW_GATEWAY_TOKEN"
```

### 启动/停止

```bash
# 启动
docker compose up -d

# 停止
docker compose down

# 重启
docker compose restart
```

### 查看日志

```bash
# 实时日志
docker compose logs -f openclaw-gateway

# 最近 100 行
docker compose logs --tail=100 openclaw-gateway
```

### 更新

```bash
# 拉取最新镜像
docker compose pull

# 重新构建
docker compose build

# 重启容器
docker compose up -d
```

---

## 📊 环境变量参考

| 变量 | 用途 | 示例 |
|------|------|------|
| `OPENCLAW_IMAGE` | 使用远程镜像 | `ghcr.io/openclaw/openclaw:latest` |
| `OPENCLAW_DOCKER_APT_PACKAGES` | 安装额外 apt 包 | `git curl jq` |
| `OPENCLAW_EXTENSIONS` | 预安装扩展 | `extension1 extension2` |
| `OPENCLAW_EXTRA_MOUNTS` | 额外主机挂载 | `/host/path:/container/path` |
| `OPENCLAW_HOME_VOLUME` | 持久化 /home/node | `openclaw_home` |
| `OPENCLAW_SANDBOX` | 启用沙箱 | `1` / `true` |
| `OPENCLAW_DOCKER_SOCKET` | Docker socket 路径 | `/run/user/1000/docker.sock` |

---

## 🌐 LAN vs Loopback

**bind 模式选项:**

| 模式 | 说明 |
|------|------|
| `lan` (默认) | 主机浏览器和 CLI 可访问 |
| `loopback` | 仅容器内可访问 |
| `custom` | 自定义绑定 |
| `tailnet` | Tailscale 网络 |
| `auto` | 自动检测 |

**配置示例:**

```json
{
  "gateway": {
    "bind": "lan"
  }
}
```

<Note>
使用 `lan` / `loopback` 等模式值，而非 `0.0.0.0` 或 `127.0.0.1`。
</Note>

---

## 📦 存储与持久化

### 挂载目录

| 主机目录 | 容器目录 | 用途 |
|----------|----------|------|
| `OPENCLAW_CONFIG_DIR` | `/home/node/.openclaw` | 配置目录 |
| `OPENCLAW_WORKSPACE_DIR` | `/home/node/.openclaw/workspace` | 工作区 |

### 持久化数据

| 文件/目录 | 用途 |
|-----------|------|
| `openclaw.json` | 行为配置 |
| `agents/<agentId>/auth-profiles.json` | 提供商认证 |
| `.env` | 运行时密钥 (如 `OPENCLAW_GATEWAY_TOKEN`) |

### 磁盘增长热点

监控以下目录：

| 目录 | 说明 |
|------|------|
| `media/` | 媒体文件 |
| `session JSONL` | 会话日志 |
| `cron/runs/*.jsonl` | 定时任务日志 |
| `/tmp/openclaw/` | 滚动日志 |

---

## 🔧 Shell 助手 (可选)

### 安装 ClawDock

```bash
mkdir -p ~/.clawdock
curl -sL https://raw.githubusercontent.com/openclaw/openclaw/main/scripts/clawdock/clawdock-helpers.sh \
  -o ~/.clawdock/clawdock-helpers.sh
echo 'source ~/.clawdock/clawdock-helpers.sh' >> ~/.zshrc
source ~/.zshrc
```

### 常用命令

| 命令 | 说明 |
|------|------|
| `clawdock-start` | 启动 OpenClaw |
| `clawdock-stop` | 停止 OpenClaw |
| `clawdock-dashboard` | 打开仪表盘 |
| `clawdock-logs` | 查看日志 |
| `clawdock-help` | 显示帮助 |

---

## 🔍 常见问题排障

### 问题 1: 镜像缺失或沙箱容器未启动

| 项目 | 内容 |
|------|------|
| **现象** | 沙箱容器无法启动 |
| **原因** | 沙箱镜像未构建 |
| **解决** | 构建沙箱镜像 |

**步骤:**
```bash
scripts/sandbox-setup.sh
```

或设置自定义镜像：
```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "image": "your-custom-image:latest"
        }
      }
    }
  }
}
```

---

### 问题 2: 沙箱权限错误

| 项目 | 内容 |
|------|------|
| **现象** | 沙箱内权限错误 (EACCES) |
| **原因** | UID/GID 不匹配 |
| **解决** | 调整 docker.user 或 chown |

**步骤:**
```bash
# 方案 A: 设置 docker.user
# 编辑 ~/.openclaw/openclaw.json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "user": "1000:1000"
        }
      }
    }
  }
}

# 方案 B: 修改工作区所有权
sudo chown -R 1000:1000 /path/to/openclaw-workspace
```

---

### 问题 3: 自定义工具在沙箱中未找到

| 项目 | 内容 |
|------|------|
| **现象** | 自定义工具命令未找到 |
| **原因** | PATH 被重置 |
| **解决** | 设置 PATH 环境变量 |

**步骤:**
```bash
# 方案 A: 设置 docker.env.PATH
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "env": {
            "PATH": "/custom/path:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
          }
        }
      }
    }
  }
}

# 方案 B: 在 Dockerfile 中添加脚本
# /etc/profile.d/custom-tools.sh
export PATH="/custom/path:$PATH"
```

---

### 问题 4: 镜像构建时 OOM (exit 137)

| 项目 | 内容 |
|------|------|
| **现象** | pnpm install 被杀死，exit 137 |
| **原因** | 内存不足 (需要 ≥2GB) |
| **解决** | 增加 VM 内存 |

**步骤:**
```bash
# 检查当前内存
free -h

# 升级 VPS 内存配置
# 或使用 swap (临时方案)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

### 问题 5: Control UI 显示 Unauthorized 或 Pairing Required

| 项目 | 内容 |
|------|------|
| **现象** | 仪表盘显示需要配对 |
| **原因** | 设备未认证 |
| **解决** | 获取仪表盘链接并批准设备 |

**步骤:**
```bash
# 1. 获取仪表盘链接
docker compose run --rm openclaw-cli dashboard --no-open

# 2. 列出设备请求
docker compose run --rm openclaw-cli devices list

# 3. 批准设备
docker compose run --rm openclaw-cli devices approve <requestId>
```

---

### 问题 6: Gateway target 显示 ws://172.x.x.x 或配对错误

| 项目 | 内容 |
|------|------|
| **现象** | WebSocket 地址错误或配对失败 |
| **原因** | gateway mode/bind 配置错误 |
| **解决** | 重置 gateway 配置 |

**步骤:**
```bash
# 重置 gateway 配置
docker compose run --rm openclaw-cli config set --batch-json '[
  {"path":"gateway.mode","value":"local"},
  {"path":"gateway.bind","value":"lan"}
]'

# 使用正确 URL 列出设备
docker compose run --rm openclaw-cli devices list --url ws://127.0.0.1:18789
```

---

## 🛡️ 安全注意事项

### 共享网络安全

`openclaw-cli` 使用 `network_mode: "service:openclaw-gateway"`，CLI 命令可通过 127.0.0.1 访问 gateway。

**安全措施:**
- Compose 配置已丢弃 `NET_RAW`/`NET_ADMIN` 能力
- 启用 `no-new-privileges`
- 视为共享信任边界

### 权限问题 (EACCES)

镜像以 `node` (uid 1000) 运行。如遇到权限错误：

```bash
sudo chown -R 1000:1000 /path/to/openclaw-config /path/to/openclaw-workspace
```

---

## 📊 配置对比

### Docker vs 本地安装

| 特性 | Docker | 本地安装 |
|------|--------|----------|
| **隔离性** | ✅ 完全隔离 | ❌ 无隔离 |
| **可移植性** | ✅ 高 | ❌ 低 |
| **性能** | 🟡 略低 (5-10%) | ✅ 原生 |
| **管理复杂度** | 🟡 中等 | 🟢 低 |
| **推荐场景** | 生产/多租户 | 开发/个人使用 |

### 沙箱模式对比

| 模式 | 隔离性 | 性能 | 推荐场景 |
|------|--------|------|----------|
| `off` | ❌ 无 | ✅ 100% | 开发/信任环境 |
| `non-main` | ✅ 中等 | 🟡 90% | 生产 (推荐) |
| `all` | ✅ 完全 | 🟡 80% | 多租户/高安全 |

---

## 🔗 相关文档

| 文档 | 位置 |
|------|------|
| **沙箱完整参考** | `RedAgentTeamllm-wiki/wiki/sandbox/` (待创建) |
| **OpenShell** | `RedAgentTeamllm-wiki/wiki/shell/` (待创建) |
| **多 Agent 沙箱** | `RedAgentTeamllm-wiki/wiki/agents/multi-agent.md` (待创建) |
| **Podman 替代** | https://docs.openclaw.ai/install/podman |
| **ClawDock** | https://docs.openclaw.ai/install/clawdock |
| **更新指南** | https://docs.openclaw.ai/install/updating |
| **本报告** | `RedAgentTeamllm-wiki/wiki/install/docker.md` |

---

## 📝 快速参考

### 常用命令

```bash
# 启动
docker compose up -d

# 停止
docker compose down

# 查看日志
docker compose logs -f

# 健康检查
curl http://127.0.0.1:18789/healthz

# 进入容器
docker compose exec openclaw-gateway bash

# 重建镜像
docker compose build

# 更新
docker compose pull && docker compose up -d
```

### 环境变量速查

```bash
# 使用预构建镜像
export OPENCLAW_IMAGE="ghcr.io/openclaw/openclaw:latest"

# 启用沙箱
export OPENCLAW_SANDBOX=1

# 自定义 Docker socket
export OPENCLAW_DOCKER_SOCKET=/run/user/1000/docker.sock

# 安装额外包
export OPENCLAW_DOCKER_APT_PACKAGES="git curl jq"

# 持久化 /home/node
export OPENCLAW_HOME_VOLUME="openclaw_home"
```

---

**收录状态:** ✅ 完整  
**可用性:** 可直接用于 Docker 环境部署和沙箱配置  
**最后更新:** 2026-04-23 13:58 GMT+8

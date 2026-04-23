# OpenClaw Gateway Sandboxing 完整参考

**来源:** https://docs.openclaw.ai/gateway/sandboxing  
**收录时间:** 2026-04-23 14:07 GMT+8  
**状态:** ✅ 完整 (可用于沙箱配置和安全隔离)  

---

## 📋 概述

OpenClaw 可以在**沙箱后端内运行工具**以减少爆炸半径。

| 特性 | 说明 |
|------|------|
| **可选性** | ✅ 可选功能，通过配置控制 |
| **隔离范围** | 工具执行 (exec, read, write, edit, apply_patch 等) |
| **沙箱浏览器** | ✅ 可选 (agents.defaults.sandbox.browser) |
| **Gateway 进程** | ❌ 不沙箱化 (保持在主机) |
| **安全边界** | ⚠️ 非完美，但实质限制文件和进程访问 |

---

## 🎯 沙箱模式

### agents.defaults.sandbox.mode

控制**何时**使用沙箱：

| 模式 | 说明 | 推荐场景 |
|------|------|----------|
| `off` | 无沙箱 | 开发/信任环境 |
| `non-main` (默认) | 仅非主会话沙箱 | 生产环境 (推荐) |
| `all` | 所有会话沙箱 | 高安全/多租户 |

<Note>
`non-main` 基于 session.mainKey (默认 "main")，而非 agent id。
组/渠道会话使用自己的键，因此算作 non-main 并会被沙箱化。
</Note>

---

## 🔬 沙箱范围

### agents.defaults.sandbox.scope

控制**创建多少容器**：

| 范围 | 说明 | 容器数量 |
|------|------|----------|
| `agent` (默认) | 每个 agent 一个容器 | 多容器 |
| `session` | 每个会话一个容器 | 中等 |
| `shared` | 所有沙箱会话共享一个容器 | 单容器 |

---

## 🖥️ 沙箱后端

### agents.defaults.sandbox.backend

控制**哪个运行时**提供沙箱：

| 后端 | 说明 | 推荐场景 |
|------|------|----------|
| `docker` (默认) | 本地 Docker 后端 | 本地开发/完全隔离 |
| `ssh` | SSH 远程后端 | 远程机器卸载 |
| `openshell` | OpenShell 管理后端 | 托管远程沙箱 |

---

## 📊 后端对比

| 特性 | Docker | SSH | OpenShell |
|------|--------|-----|-----------|
| **运行位置** | 本地容器 | 任意 SSH 主机 | OpenShell 管理 |
| **设置** | scripts/sandbox-setup.sh | SSH 密钥 + 目标主机 | OpenShell 插件启用 |
| **工作区模型** | 绑定挂载或复制 | 远程规范 (种子一次) | mirror 或 remote |
| **网络控制** | docker.network | 取决于远程主机 | 取决于 OpenShell |
| **浏览器沙箱** | ✅ 支持 | ❌ 不支持 | ❌ 暂不支持 |
| **绑定挂载** | docker.binds | N/A | N/A |
| **最佳场景** | 本地开发/完全隔离 | 远程机器卸载 | 托管远程沙箱 |

---

## 🐳 Docker 后端

### 工作原理

沙箱默认关闭。如启用沙箱且未选择后端，OpenClaw 使用 Docker 后端。

**执行方式:** 通过 Docker daemon socket (`/var/run/docker.sock`) 本地执行工具和沙箱浏览器。

**隔离级别:** 由 Docker 命名空间决定。

### Docker-out-of-Docker (DooD) 约束

如将 OpenClaw Gateway 本身部署为 Docker 容器：

| 约束 | 说明 |
|------|------|
| **配置需要主机路径** | openclaw.json 中的工作区配置**必须**包含主机绝对路径 (如 `/home/user/.openclaw/workspaces`) |
| **FS 桥接对等** | Gateway 容器必须有相同卷映射 (`-v /home/user/.openclaw:/home/user/.openclaw`) |
| **路径不一致后果** | OpenClaw 会抛出 EACCES 权限错误 |

### 配置示例

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "backend": "docker",
        "scope": "agent",
        "workspaceAccess": "none",
        "docker": {
          "image": "openclaw-sandbox:bookworm-slim",
          "network": "none",
          "user": "1000:1000",
          "binds": ["/home/user/source:/source:ro"],
          "env": {
            "API_KEY": "your-api-key"
          }
        }
      }
    }
  }
}
```

### 环境变量

| 变量 | 用途 | 示例 |
|------|------|------|
| `OPENCLAW_SANDBOX` | 启用沙箱 | `1` / `true` |
| `OPENCLAW_DOCKER_SOCKET` | Docker socket 路径 | `/run/user/1000/docker.sock` |
| `OPENCLAW_DOCKER_APT_PACKAGES` | 安装额外 apt 包 | `git curl jq` |
| `OPENCLAW_HOME_VOLUME` | 持久化 /home/node | `openclaw_home` |

---

## 🔐 SSH 后端

### 工作原理

使用 `backend: "ssh"` 时，OpenClaw 在任意 SSH 可访问机器上沙箱化 exec、文件工具和媒体读取。

### 配置示例

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all",
        "backend": "ssh",
        "scope": "session",
        "workspaceAccess": "rw",
        "ssh": {
          "target": "user@gateway-host:22",
          "workspaceRoot": "/tmp/openclaw-sandboxes",
          "strictHostKeyChecking": true,
          "updateHostKeys": true,
          "identityFile": "~/.ssh/id_ed25519",
          "certificateFile": "~/.ssh/id_ed25519-cert.pub",
          "knownHostsFile": "~/.ssh/known_hosts"
        }
      }
    }
  }
}
```

### 认证材料

| 选项 | 说明 |
|------|------|
| `*File` | 使用现有本地文件 (如 `identityFile`) |
| `*Data` | 使用内联字符串或 SecretRefs |
| **优先级** | `*Data` 优先于 `*File` |

### 重要后果

- **远程规范模型:** 远程 SSH 工作区在初始种子后成为真实沙箱状态
- **主机本地编辑:** 种子步骤后在 OpenClaw 外的编辑不可见，直到重新创建沙箱
- **浏览器沙箱:** ❌ 不支持
- **重新创建:** `openclaw sandbox recreate` 删除每范围远程根并重新种子

---

## 🐚 OpenShell 后端

### 工作原理

OpenShell 是 OpenClaw 的托管沙箱后端。OpenClaw 将沙箱生命周期委托给 openshell CLI，后者配置基于 SSH 的远程环境。

### 快速启动

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all",
        "backend": "openshell",
        "scope": "session",
        "workspaceAccess": "rw"
      }
    }
  },
  "plugins": {
    "entries": {
      "openshell": {
        "enabled": true,
        "config": {
          "from": "openclaw",
          "mode": "remote"
        }
      }
    }
  }
}
```

### 工作区模式

| 模式 | 规范工作区 | 同步方向 | 每转开销 | 本地编辑可见 | 最佳场景 |
|------|-----------|----------|----------|-------------|----------|
| **mirror** | 本地主机 | 双向 (每次 exec) | 高 | ✅ 是 | 开发工作流 |
| **remote** | 远程 OpenShell | 一次种子 | 低 | ❌ 否 | 长运行 agent/CI |

### 配置参考

| 键 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `mode` | "mirror" 或 "remote" | "mirror" | 工作区同步模式 |
| `command` | string | "openshell" | openshell CLI 路径或名称 |
| `from` | string | "openclaw" | 首次创建的沙箱源 |
| `gateway` | string | — | OpenShell gateway 名称 |
| `gatewayEndpoint` | string | — | OpenShell gateway 端点 URL |
| `policy` | string | — | 沙箱创建的 OpenShell 策略 ID |
| `providers` | string[] | [] | 创建时附加的提供商名称 |
| `gpu` | boolean | false | 请求 GPU 资源 |
| `autoProviders` | boolean | true | 沙箱创建时传递 --auto-providers |
| `remoteWorkspaceDir` | string | "/sandbox" | 沙箱内主可写工作区 |
| `remoteAgentWorkspaceDir` | string | "/agent" | Agent 工作区挂载路径 |
| `timeoutSeconds` | number | 120 | openshell CLI 操作超时 |

### 示例配置

**最小远程设置:**
```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all",
        "backend": "openshell"
      }
    }
  },
  "plugins": {
    "entries": {
      "openshell": {
        "enabled": true,
        "config": {
          "from": "openclaw",
          "mode": "remote"
        }
      }
    }
  }
}
```

**mirror 模式 + GPU:**
```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "all",
        "backend": "openshell",
        "scope": "agent",
        "workspaceAccess": "rw"
      }
    }
  },
  "plugins": {
    "entries": {
      "openshell": {
        "enabled": true,
        "config": {
          "from": "openclaw",
          "mode": "mirror",
          "gpu": true,
          "providers": ["openai"],
          "timeoutSeconds": 180
        }
      }
    }
  }
}
```

---

## 📂 工作区访问

### agents.defaults.sandbox.workspaceAccess

控制**沙箱能看到什么**：

| 模式 | 说明 | 推荐场景 |
|------|------|----------|
| `none` (默认) | 工具看到沙箱工作区 (~/.openclaw/sandboxes) | 高安全 |
| `ro` | 只读挂载 agent 工作区到 /agent | 只读访问 |
| `rw` | 读写挂载 agent 工作区到 /workspace | 完全访问 |

**注意:**
- 入站媒体复制到沙箱工作区 (`media/inbound/*`)
- `read` 工具是沙箱根定的
- `workspaceAccess: "none"` 时，OpenClaw 镜像合格技能到沙箱工作区

---

## 🔗 自定义绑定挂载

### agents.defaults.sandbox.docker.binds

挂载额外主机目录到容器。

**格式:** `host:container:mode` (如 `"/home/user/source:/source:ro"`)

### 配置示例

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "binds": [
            "/home/user/source:/source:ro",
            "/var/data/myapp:/data:ro"
          ]
        }
      }
    },
    "list": [
      {
        "id": "build",
        "sandbox": {
          "docker": {
            "binds": ["/mnt/cache:/cache:rw"]
          }
        }
      }
    ]
  }
}
```

### 安全说明

| 规则 | 说明 |
|------|------|
| **绕过沙箱** | 绑定挂载暴露主机路径，按设置模式 (:ro 或 :rw) |
| **阻止危险源** | docker.sock, /etc, /proc, /sys, /dev, 父挂载 |
| **阻止凭证根** | ~/.aws, ~/.cargo, ~/.config, ~/.docker, ~/.gnupg, ~/.netrc, ~/.npm, ~/.ssh |
| **路径验证** | 规范化源路径，通过最深现有祖先解析后重新检查 |
| **敏感挂载** | 除非绝对需要，否则使用 :ro |

---

## 🖼️ 镜像 + 设置

### 默认 Docker 镜像

| 镜像 | 用途 | 构建命令 |
|------|------|----------|
| `openclaw-sandbox:bookworm-slim` | 默认沙箱镜像 | `scripts/sandbox-setup.sh` |
| `openclaw-sandbox-common:bookworm-slim` | 功能更全 (含 curl/jq/nodejs/python3/git) | `scripts/sandbox-common-setup.sh` |
| `openclaw-sandbox-browser` | 沙箱浏览器镜像 | `scripts/sandbox-browser-setup.sh` |

### setupCommand (一次性容器设置)

**运行时机:** 容器创建后运行一次 (非每次运行)

**执行方式:** 通过 `sh -lc` 在容器内执行

**常见陷阱:**

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 包安装失败 | 默认 `docker.network: "none"` (无出口) | 设置 `docker.network` |
| 命名空间加入风险 | `network: "container:<id>"` | 需 `dangerouslyAllowContainerNamespaceJoin: true` |
| 写入被阻止 | `readOnlyRoot: true` | 设置 `false` 或自定义镜像 |
| 包安装需要 root | 用户非 root | 省略 user 或设置 `user: "0:0"` |
| 环境变量不继承 | 沙箱 exec 不继承 host process.env | 使用 `sandbox.docker.env` |

---

## 🌐 沙箱浏览器

### 配置选项

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "browser": {
          "autoStart": true,
          "autoStartTimeoutMs": 30000,
          "network": "openclaw-sandbox-browser",
          "cdpSourceRange": "172.21.0.1/32",
          "allowHostControl": false,
          "binds": ["/home/user/downloads:/downloads:rw"]
        }
      }
    }
  }
}
```

### 安全默认值

| 设置 | 默认值 | 说明 |
|------|--------|------|
| `network: "host"` | ❌ 阻止 | 防止主机网络访问 |
| `network: "container:<id>"` | ❌ 阻止 | 命名空间加入绕过风险 |
| **noVNC 访问** | ✅ 密码保护 | 短令牌 URL，密码在 URL 片段中 |

### Chromium 启动标志

| 标志 | 默认 | 环境变量控制 |
|------|------|-------------|
| `--disable-3d-apis` | ✅ 启用 | `OPENCLAW_BROWSER_DISABLE_GRAPHICS_FLAGS=0` 禁用 |
| `--disable-gpu` | ✅ 启用 | 同上 |
| `--disable-extensions` | ✅ 启用 | `OPENCLAW_BROWSER_DISABLE_EXTENSIONS=0` 禁用 |
| `--renderer-process-limit` | 2 | `OPENCLAW_BROWSER_RENDERER_PROCESS_LIMIT=<N>` |

---

## 🛠️ 工具策略 + 逃逸舱

### 工具允许/拒绝策略

工具允许/拒绝策略在沙箱规则之前应用。如工具全局或每 agent 被拒绝，沙箱化不会恢复它。

### tools.elevated

**明确的逃逸舱**，在沙箱外运行 exec (默认 gateway，或 exec 目标为 node 时)。

**注意:**
- `/exec` 指令仅适用于授权发送者
- 每会话持久化
- 如要硬禁用 exec，使用工具策略拒绝

### 调试命令

```bash
# 检查有效沙箱模式、工具策略和修复配置键
openclaw sandbox explain

# 查看所有沙箱运行时
openclaw sandbox list

# 重新创建沙箱
openclaw sandbox recreate --all
```

---

## 🔄 生命周期管理

### 沙箱命令

| 命令 | 说明 |
|------|------|
| `openclaw sandbox list` | 列出所有沙箱运行时 (Docker + OpenShell) |
| `openclaw sandbox explain` | 检查有效策略 |
| `openclaw sandbox recreate --all` | 重新创建 (删除远程工作区，下次使用时重新种子) |

### 何时重新创建

更改以下配置后重新创建：

| 配置项 | 说明 |
|--------|------|
| `agents.defaults.sandbox.backend` | 后端切换 |
| `plugins.entries.openshell.config.from` | OpenShell 源更改 |
| `plugins.entries.openshell.config.mode` | 工作区模式切换 |
| `plugins.entries.openshell.config.policy` | 策略更改 |

---

## 🔍 常见问题排障

### 问题 1: 沙箱容器未启动

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

### 问题 2: 权限错误 (EACCES)

| 项目 | 内容 |
|------|------|
| **现象** | 沙箱内权限错误 |
| **原因** | UID/GID 不匹配或路径不一致 |
| **解决** | 调整 docker.user 或 chown |

**步骤:**
```bash
# 方案 A: 设置 docker.user
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

# 方案 C: Docker Gateway 部署确保路径对等
# 主机路径：/home/user/.openclaw
# 容器卷映射：-v /home/user/.openclaw:/home/user/.openclaw
```

---

### 问题 3: 包安装失败 (exit 137)

| 项目 | 内容 |
|------|------|
| **现象** | setupCommand 中包安装失败 |
| **原因** | 网络禁用或内存不足 |
| **解决** | 启用网络或增加内存 |

**步骤:**
```bash
# 方案 A: 启用网络
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "network": "bridge"
        }
      }
    }
  }
}

# 方案 B: 增加 VM 内存
# 至少 2GB RAM

# 方案 C: 使用自定义镜像预装包
scripts/sandbox-common-setup.sh
```

---

### 问题 4: 自定义工具未找到

| 项目 | 内容 |
|------|------|
| **现象** | 沙箱中自定义工具命令未找到 |
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

### 问题 5: SSH 后端连接失败

| 项目 | 内容 |
|------|------|
| **现象** | SSH 连接被拒绝或认证失败 |
| **原因** | SSH 密钥配置错误 |
| **解决** | 检查 SSH 配置 |

**步骤:**
```bash
# 1. 验证 SSH 连接
ssh -i ~/.ssh/id_ed25519 user@gateway-host

# 2. 检查 known_hosts
ssh-keyscan gateway-host >> ~/.ssh/known_hosts

# 3. 更新配置
{
  "agents": {
    "defaults": {
      "sandbox": {
        "ssh": {
          "strictHostKeyChecking": false,
          "identityFile": "~/.ssh/id_ed25519"
        }
      }
    }
  }
}
```

---

### 问题 6: OpenShell 工作区不同步

| 项目 | 内容 |
|------|------|
| **现象** | 本地编辑在远程沙箱不可见 |
| **原因** | 使用 remote 模式，本地编辑不自动同步 |
| **解决** | 切换到 mirror 模式或重新创建 |

**步骤:**
```bash
# 方案 A: 切换到 mirror 模式
{
  "plugins": {
    "entries": {
      "openshell": {
        "config": {
          "mode": "mirror"
        }
      }
    }
  }
}

# 方案 B: 重新创建沙箱
openclaw sandbox recreate --all
```

---

## 📊 最小启用示例

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "scope": "session",
        "workspaceAccess": "none"
      }
    }
  }
}
```

**说明:**
- `mode: "non-main"` — 仅非主会话沙箱 (推荐)
- `scope: "session"` — 每会话一个容器
- `workspaceAccess: "none"` — 沙箱工作区独立，不访问主机工作区

---

## 🛡️ 安全最佳实践

| 实践 | 说明 |
|------|------|
| **最小权限** | 使用 `workspaceAccess: "none"` 或 `"ro"` |
| **绑定挂载只读** | 敏感挂载使用 `:ro` |
| **阻止危险路径** | OpenClaw 自动阻止 docker.sock, /etc, ~/.ssh 等 |
| **网络隔离** | 默认 `docker.network: "none"`，按需启用 |
| **工具策略** | 结合工具策略 deny 硬禁用 exec |
| **定期重新创建** | `openclaw sandbox recreate --all` 重置环境 |

---

## 🔗 相关文档

| 文档 | 位置 |
|------|------|
| **OpenShell** | `RedAgentTeamllm-wiki/wiki/gateway/openshell.md` (待创建) |
| **Sandbox CLI** | `openclaw sandbox` 命令 |
| **多 Agent 沙箱** | `RedAgentTeamllm-wiki/wiki/agents/multi-agent.md` (待创建) |
| **工具策略** | `RedAgentTeamllm-wiki/wiki/gateway/tool-policy.md` (待创建) |
| **Elevated Mode** | `RedAgentTeamllm-wiki/wiki/gateway/elevated.md` (待创建) |
| **安全加固** | `RedAgentTeamllm-wiki/wiki/gateway/security.md` (待创建) |
| **本报告** | `RedAgentTeamllm-wiki/wiki/gateway/sandboxing.md` |

---

## 📝 快速参考

### 常用命令

```bash
# 构建沙箱镜像
scripts/sandbox-setup.sh

# 构建功能更全的镜像
scripts/sandbox-common-setup.sh

# 构建沙箱浏览器镜像
scripts/sandbox-browser-setup.sh

# 列出沙箱运行时
openclaw sandbox list

# 检查有效策略
openclaw sandbox explain

# 重新创建沙箱
openclaw sandbox recreate --all

# 启用沙箱 (Docker Gateway)
export OPENCLAW_SANDBOX=1
./scripts/docker/setup.sh
```

### 配置速查

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "backend": "docker",
        "scope": "agent",
        "workspaceAccess": "none",
        "docker": {
          "image": "openclaw-sandbox:bookworm-slim",
          "network": "none",
          "user": "1000:1000",
          "binds": ["/source:/source:ro"],
          "env": {"API_KEY": "key"}
        }
      }
    }
  }
}
```

---

**收录状态:** ✅ 完整  
**可用性:** 可直接用于沙箱配置和安全隔离部署  
**最后更新:** 2026-04-23 14:07 GMT+8

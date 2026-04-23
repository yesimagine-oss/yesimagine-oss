---
category: docker
created_at: '2026-04-14'
tags:
- docker
- docker
- 基礎概念
title: Docker 核心概念
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
# Docker 基礎概念

**創建時間**: 2026-03-19  
**難度**: ⭐ 入門  
**參考文檔**: https://docs.docker.com/get-started/overview/

---

## 📚 核心概念

### 1. 什麼是 Docker？

Docker 是一個開源平台，用於將應用程序及其依賴打包到輕量級容器中，實現：
- **一次構建，隨處運行**
- **環境一致性**
- **快速部署**
- **資源隔離**

### 2. 三大核心組件

```
┌─────────────────────────────────────────┐
│              Docker 架構                 │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │  鏡像    │→ │  容器    │←│ 倉庫   ││
│  │ (Image)  │  │(Container)│  │(Registry)│
│  └──────────┘  └──────────┘  └────────┘│
│                                         │
└─────────────────────────────────────────┘
```

#### 鏡像 (Image)
- **定義**: 只讀模板，包含應用程序和運行環境
- **特點**: 分層存儲、不可變、可共享
- **示例**: `ubuntu:24.04`, `node:22-bookworm`

#### 容器 (Container)
- **定義**: 鏡像的運行實例
- **特點**: 可啟動/停止、有獨立文件系統、網絡隔離
- **生命周期**: 創建 → 運行 → 暫停 → 停止 → 刪除

#### 倉庫 (Registry)
- **定義**: 存儲和分發鏡像的服務
- **公共倉庫**: Docker Hub (hub.docker.com)
- **私有倉庫**: Harbor, GitLab Registry, AWS ECR

---

## 🏗️ Docker 架構

```
┌─────────────────────────────────────────────────┐
│                    Docker 架構                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┐                               │
│  │   Client    │  docker CLI                   │
│  └──────┬──────┘                               │
│         │ REST API                             │
│  ┌──────▼──────┐                               │
│  │   Daemon    │  dockerd                      │
│  └──────┬──────┘                               │
│         │                                      │
│  ┌──────▼──────────────────────────┐           │
│  │         容器運行時               │           │
│  │  ┌────────┐ ┌────────┐ ┌─────┐ │           │
│  │  │容器 1  │ │容器 2  │ │...  │ │           │
│  │  └────────┘ └────────┘ └─────┘ │           │
│  └────────────────────────────────┘           │
│                                               │
│  ┌──────────────────────────────────┐         │
│  │     鏡像倉庫 (Registry)          │         │
│  └──────────────────────────────────┘         │
│                                               │
└─────────────────────────────────────────────────┘
```

### Docker Daemon (dockerd)
- 後台服務，管理容器、鏡像、網絡、卷
- 監聽 API 請求
- 與容器運行時交互

### Docker Client
- 命令行工具 (`docker` 命令)
- 通過 REST API 與 Daemon 通信
- 可與遠程 Daemon 通信

### Container Runtime
- 實際運行容器的組件
- 默認：runc
- 其他：containerd, CRI-O

---

## 📦 鏡像分層原理

```
┌─────────────────────────────┐
│     可寫容器層 (Container)   │ ← 運行時創建
├─────────────────────────────┤
│     應用層 (Application)     │ ← 你的代碼
├─────────────────────────────┤
│     依賴層 (Dependencies)    │ ← pip/npm install
├─────────────────────────────┤
│     運行時層 (Runtime)       │ ← Python/Node.js
├─────────────────────────────┤
│     基礎鏡像層 (Base Image)  │ ← ubuntu/debian
└─────────────────────────────┘
```

### 特點
- **共享**: 多個鏡像可共享相同層
- **只讀**: 除最上層外，其他層都是只讀的
- **增量**: 修改只影響變更的層
- **緩存**: 構建時緩存未變化的層

---

## 🔄 容器生命周期

```
┌─────────┐    create    ┌─────────┐
│  不存在  │────────────→│ Created │
└─────────┘              └────┬────┘
                              │ start
                              ▼
┌─────────┐   timeout   ┌─────────┐
│  Removed│←───────────│ Running │
└────┬────┘             └────┬────┘
     │                       │ pause
     │ remove                ▼
     │                ┌─────────┐
     └────────────────│ Paused  │
         stop         └────┬────┘
                           │ unpause
                           ▼
                     ┌─────────┐
                     │ Running │
                     └─────────┘
```

### 狀態說明

| 狀態 | 說明 | 命令 |
|------|------|------|
| Created | 已創建未啟動 | `docker create` |
| Running | 運行中 | `docker start` |
| Paused | 已暫停 | `docker pause` |
| Stopped | 已停止 | `docker stop` |
| Removed | 已刪除 | `docker rm` |

---

## 🌐 網絡模式

### 1. Bridge (橋接)
```
┌──────────┐     ┌──────────┐
│  容器 1   │────→│  docker0 │←────┌──────────┐
│ 172.17.0.2│     │ 網橋     │     │  容器 2   │
└──────────┘     └──────────┘     │ 172.17.0.3│
                                  └──────────┘
```
- **默認模式**
- 容器通過網橋通信
- 可通過端口映射訪問外部

### 2. Host (主機)
```
┌──────────┐
│  容器     │←─── 直接使用主機網絡
│ 無隔離    │
└──────────┘
```
- 容器共享主機網絡命名空間
- 無網絡隔離
- 性能最好

### 3. None (無網絡)
```
┌──────────┐
│  容器     │←─── 無網絡接口
│  隔離     │
└──────────┘
```
- 完全網絡隔離
- 只有 loopback 接口

### 4. Container (共享)
```
┌──────────┐     ┌──────────┐
│  容器 1   │←───→│  容器 2   │
│ (主容器) │     │共享網絡  │
└──────────┘     └──────────┘
```
- 多個容器共享網絡命名空間
- 使用 `--network container:<name>`

---

## 💾 存儲驅動

### Overlay2 (推薦)

```
┌─────────────────────────────┐
│     容器可寫層               │
├─────────────────────────────┤
│     鏡像上層 (upperdir)     │
├─────────────────────────────┤
│     鏡像下層 (lowerdir)     │
├─────────────────────────────┤
│     基礎鏡像                │
└─────────────────────────────┘
```

### 其他驅動

| 驅動 | 說明 | 狀態 |
|------|------|------|
| overlay2 | 推薦，性能好 | ✅ 默認 |
| aufs | 老舊，已棄用 | ❌ 不推薦 |
| devicemapper | 塊存儲 | ⚠️ 特殊場景 |
| btrfs | 文件系統級 | ⚠️ 需要支持 |
| zfs | 文件系統級 | ⚠️ 需要支持 |

---

## 🔒 安全模型

### 1. 命名空間隔離 (Namespaces)

| 類型 | 隔離內容 | 命令 |
|------|---------|------|
| PID | 進程 ID | `--pid` |
| NET | 網絡接口 | `--network` |
| IPC | 進程間通信 | `--ipc` |
| MNT | 文件系統掛載 | - |
| UTS | 主機名 | `--hostname` |
| USER | 用戶 ID | `--userns` |

### 2. 控制組 (Cgroups)

```
┌─────────────────────────────┐
│       系統資源              │
├─────────────────────────────┤
│  ┌─────────┐ ┌─────────┐   │
│  │ 容器 1   │ │ 容器 2   │   │
│  │ 50% CPU │ │ 30% CPU │   │
│  │ 512MB   │ │ 256MB   │   │
│  └─────────┘ └─────────┘   │
└─────────────────────────────┘
```

### 3. 能力控制 (Capabilities)

```bash
# 刪除所有能力，只添加需要的
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE ...

# 常見能力
NET_BIND_SERVICE  # 綁定低端口 (<1024)
SYS_ADMIN         # 管理員權限 (危險)
SYS_PTRACE        # 調試進程
```

### 4. Seccomp (系統調用過濾)

```bash
# 使用默認配置文件
docker run --security-opt seccomp=default ...

# 使用自定義配置文件
docker run --security-opt seccomp=/path/to/profile.json ...
```

---

## 📊 資源限制

```bash
# CPU 限制
docker run --cpus="1.5" ...      # 1.5 個 CPU 核心
docker run --cpu-shares="512" ... # CPU 權重

# 內存限制
docker run --memory="512m" ...   # 512MB 內存
docker run --memory-swap="1g" ... # 內存 + 交換空間

# 磁盤限制 (需要配額)
docker run --device-read-bps="/dev/sda:1mb" ...
```

---

## 🎯 最佳實踐

### 鏡像構建

```dockerfile
# ✅ 使用具體版本標籤
FROM node:22-bookworm-slim

# ✅ 多階段構建
FROM node:22 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

# ✅ 合併 RUN 指令
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    package1 \
    package2 && \
    rm -rf /var/lib/apt/lists/*

# ❌ 避免
FROM node:latest  # 不確定性
RUN apt-get update
RUN apt-get install -y package1  # 多層
RUN apt-get install -y package2
```

### 容器運行

```bash
# ✅ 推薦
docker run -d \
  --name myapp \
  --restart unless-stopped \
  --memory 512m \
  --cpus 1 \
  --read-only \
  --tmpfs /tmp \
  --security-opt no-new-privileges:true \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  myapp:latest

# ❌ 避免
docker run myapp:latest  # 無任何限制
docker run --privileged myapp:latest  # 特權模式 (危險)
```

---

## 📖 參考資源

- **官方文檔**: https://docs.docker.com/
- **Docker Hub**: https://hub.docker.com/
- **最佳實踐**: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- **安全指南**: https://docs.docker.com/engine/security/

---

**最後更新**: 2026-03-19

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[docker_layer_cache]]
- [[Node.js 核心概念]]
- [[Node.js-核心概念]]

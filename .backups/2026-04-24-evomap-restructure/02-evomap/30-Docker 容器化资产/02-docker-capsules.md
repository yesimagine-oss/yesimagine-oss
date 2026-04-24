---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 02 Docker Capsules
type: article
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
# Docker Capsules - 功能封装

**来源:** Docker Official Docs (92 页完整覆盖)
**置信度:** 0.98
**入库日期:** 2026-04-15

---

## Capsule 列表

| # | Capsule ID | 触发条件 | 功能 |
|---|------------|----------|------|
| 1 | `docker_container_start` | 启动已验证容器 | docker pull + docker run |
| 2 | `docker_compose_deploy` | 部署多容器应用 | docker-compose up -d |
| 3 | `docker_daemon_restart` | Docker 守护进程故障 | systemctl restart docker |

---

## Capsule 详细实现

### 1. docker_container_start

**触发:** 需要启动新容器

**代码:**
```bash
# 1. 拉取镜像
docker pull {image}

# 2. 运行容器
docker run -d \
  -p {host_port}:{container_port} \
  -v {volume} \
  --name {container_name} \
  {image}
```

**参数:**
- `image`: 镜像名称 (如 nginx:latest)
- `host_port`: 主机端口
- `container_port`: 容器端口
- `volume`: 卷挂载 (可选)

---

### 2. docker_compose_deploy

**触发:** 部署多容器应用

**代码:**
```bash
# 1. 验证配置
docker-compose config -q

# 2. 启动服务
docker-compose up -d

# 3. 检查状态
docker-compose ps
```

**适用场景:**
- 微服务部署
- 数据库 + 应用栈
- 开发环境一键部署

---

### 3. docker_daemon_restart

**触发:** Docker 守护进程故障

**代码:**
```bash
# 1. 重启守护进程
systemctl restart docker

# 2. 设置开机自启
systemctl enable docker

# 3. 验证状态
systemctl status docker
```

**注意:** 重启会中断所有运行中的容器

---

**状态:** ✅ 已验证可复用
**适用场景:** 容器自动化 Skill 开发


## 相關文檔

- [[docker_layer_cache]]
- [[asset01_docker_layer_cache]]
- [[02-openai-capsules]]

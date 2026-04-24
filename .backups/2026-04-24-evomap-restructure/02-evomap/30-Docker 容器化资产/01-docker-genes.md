---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 01 Docker Genes
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
# Docker Genes - 验证核心

**来源:** Docker Official Docs (92 页完整覆盖)
**置信度:** 0.98
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `docker_daemon_health_check` | Docker 守护进程运行状态验证 | `pytest tests/test_docker_daemon.py` |
| 2 | `docker_image_pull_validate` | 镜像拉取和 Digest 验证 | `node tests/docker-image-validate.test.js` |
| 3 | `docker_container_port_check` | 容器端口映射和可用性检查 | `pytest tests/test_docker_port.py` |
| 4 | `docker_compose_validate` | docker-compose.yml 语法验证 | `node tests/docker-compose-validate.test.js` |
| 5 | `docker_api_auth_verify` | Docker Hub/Registry 认证验证 | `pytest tests/test_docker_auth.py` |

---

## Gene 详细说明

### 1. docker_daemon_health_check

**用途:** 验证 Docker 守护进程状态

**关键检查点:**
- 守护进程是否运行
- Socket 连接可用性
- 系统资源状态
- 日志健康检查

**命令:**
```bash
systemctl status docker
docker info
docker system df
```

---

### 2. docker_image_pull_validate

**用途:** 验证镜像拉取完整性

**检查项:**
- 镜像 Digest 校验
- 层完整性验证
- 签名验证 (Docker Content Trust)
- 来源仓库验证

---

### 3. docker_container_port_check

**用途:** 验证容器端口映射

**检查项:**
- 端口映射配置
- 端口可用性测试
- 防火墙规则检查
- 网络连通性验证

---

### 4. docker_compose_validate

**用途:** 验证 Compose 文件语法

**检查项:**
- YAML 语法正确性
- 服务依赖关系
- 卷挂载配置
- 网络配置验证

---

### 5. docker_api_auth_verify

**用途:** 验证 Registry 认证

**检查项:**
- Docker Hub 登录状态
- 私有 Registry 认证
- Token 有效期验证
- 凭证存储安全

---

**状态:** ✅ 已验证可复用
**适用场景:** Docker 容器化 Skill 开发


## 相關文檔

- [[docker_layer_cache]]
- [[asset01_docker_layer_cache]]
- [[01-openai-genes]]

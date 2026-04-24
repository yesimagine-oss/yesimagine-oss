# 软件安装验证模板大全

## 📋 支持的软件

| 软件 | 命令 | 验证内容 |
|------|------|---------|
| **Clash/Mihomo** | `clash` | 命令、版本、进程、端口 (7890, 9090) |
| **Git** | `git` | 命令、版本、用户名配置、邮箱配置 |
| **Docker** | `docker` | 命令、版本、进程、服务、docker-compose |
| **Nginx** | `nginx` | 命令、版本、配置测试、进程、端口 (80, 443) |
| **MySQL** | `mysql` | 命令、版本、进程、端口 (3306) |
| **Redis** | `redis-server` | 命令、版本、进程、端口 (6379) |
| **Node.js** | `node` | node、npm、npx、版本 |
| **Python** | `python3` | 命令、版本、pip3、requests 包 |
| **Java** | `java` | java、javac、版本、JAVA_HOME |
| **Go** | `go` | 命令、版本、GOPATH |
| **Rust** | `rustc` | rustc、cargo、版本 |
| **pnpm** | `pnpm` | 命令、版本 |
| **Yarn** | `yarn` | 命令、版本 |
| **PM2** | `pm2` | 命令、版本、进程列表 |

---

## 🚀 使用方法

### 1. 列出所有支持的软件

```bash
python3 /home/admin/.openclaw/workspace/tools/install-validator.py --list
```

**输出:**
```
支持的软件验证模板:
  - clash
  - mihomo
  - git
  - docker
  - nginx
  - mysql
  - redis
  - nodejs
  - node
  - python
  - java
  - go
  - rust
  - pnpm
  - yarn
  - pm2

特殊选项:
  --python <包名>  - 验证 Python 包
  --node <包名>    - 验证 Node.js 包
```

---

### 2. 验证软件安装

#### 验证 Clash
```bash
python3 /home/admin/.openclaw/workspace/tools/install-validator.py clash
```

**输出:**
```
✅ 命令检查：clash
   路径：/home/admin/bin/clash
✅ 版本检查
   Mihomo Meta v1.19.21 linux amd64
✅ 进程检查：clash
   PID: 107147
✅ 端口检查：7890
   端口 7890 正在监听
✅ 端口检查：9090
   端口 9090 正在监听

✅ Clash/Mihomo 安装验证通过 (5/5)
```

---

#### 验证 Git
```bash
python3 /home/admin/.openclaw/workspace/tools/install-validator.py git
```

**输出:**
```
✅ 命令检查：git
   路径：/usr/bin/git
✅ 版本检查
   git version 2.43.7
❌ Git 用户名配置
   错误：测试失败
❌ Git 邮箱配置
   错误：测试失败

⚠️ Git 安装验证部分通过 (2/4)
```

---

#### 验证 Docker
```bash
python3 /home/admin/.openclaw/workspace/tools/install-validator.py docker
```

**输出:**
```
✅ 命令检查：docker
   路径：/usr/bin/docker
✅ 版本检查
   Docker version 26.1.3
✅ 进程检查：dockerd
   PID: 962
✅ Docker 服务状态
   Client: Docker Engine - Community...
❌ 命令检查：docker-compose
   错误：命令未找到

⚠️ Docker 安装验证部分通过 (4/5)
```

---

#### 验证 Node.js
```bash
python3 /home/admin/.openclaw/workspace/tools/install-validator.py nodejs
```

**输出:**
```
✅ 命令检查：node
   路径：/usr/bin/node
✅ 版本检查
   v24.14.0
✅ 命令检查：npm
   路径：/usr/bin/npm
✅ 版本检查
   11.9.0
✅ 命令检查：npx
   路径：/usr/bin/npx

✅ Node.js 安装验证通过 (5/5)
```

---

### 3. 验证 Python 包

```bash
python3 /home/admin/.openclaw/workspace/tools/install-validator.py --python requests
```

**输出:**
```
✅ 包导入测试：requests
   2.31.0

✅ Python 包：requests 安装验证通过 (1/1)
```

---

### 4. 验证 Node.js 包

```bash
python3 /home/admin/.openclaw/workspace/tools/install-validator.py --node pm2
```

**输出:**
```
✅ 全局包检查：pm2
   pm2@5.3.0

✅ Node.js 包：pm2 安装验证通过 (1/1)
```

---

## 📊 验证结果说明

### 结果类型

| 符号 | 说明 |
|------|------|
| ✅ | 验证通过 |
| ⚠️ | 部分通过 |
| ❌ | 验证失败 |

### 评分标准

| 通过率 | 状态 | 说明 |
|--------|------|------|
| **100%** | ✅ 通过 | 所有检查项通过 |
| **≥70%** | ⚠️ 部分通过 | 核心功能正常，部分可选功能缺失 |
| **<70%** | ❌ 失败 | 核心功能缺失，需要修复 |

---

## 🔧 添加自定义验证模板

### 示例：验证 Redis

```python
def validate_redis():
    """验证 Redis 安装"""
    v = InstallValidator("Redis")
    
    # 1. 检查命令
    v.check_command_exists('redis-server')
    v.check_command_exists('redis-cli')
    
    # 2. 检查版本
    v.check_version('redis-server', ['--version'])
    
    # 3. 检查进程
    v.check_process('redis-server')
    
    # 4. 检查端口
    v.check_port(6379, use_netstat=True)
    
    return v.finalize()
```

---

### 示例：验证 Nginx

```python
def validate_nginx():
    """验证 Nginx 安装"""
    v = InstallValidator("Nginx")
    
    # 1. 检查命令
    v.check_command_exists('nginx')
    
    # 2. 检查版本
    v.check_version('nginx', ['-v'])
    
    # 3. 检查配置
    v.test_function('nginx -t', 'Nginx 配置测试')
    
    # 4. 检查进程
    v.check_process('nginx')
    
    # 5. 检查端口
    v.check_port(80, use_netstat=True)
    v.check_port(443, use_netstat=True)
    
    return v.finalize()
```

---

## 📋 集成到安装流程

### 标准安装流程

```bash
# 1. 安装软件
yum install -y git

# 2. 验证安装
python3 /home/admin/.openclaw/workspace/tools/install-validator.py git

# 3. 根据结果决定下一步
# ✅ 通过 → 继续
# ⚠️ 部分通过 → 检查警告
# ❌ 失败 → 重新安装或排查问题
```

---

### 在脚本中使用

```bash
#!/bin/bash

# 安装 Git
echo "🔧 安装 Git..."
yum install -y git

# 验证安装
echo "✅ 验证 Git 安装..."
python3 /home/admin/.openclaw/workspace/tools/install-validator.py git

# 检查结果
if [ $? -eq 0 ]; then
    echo "✅ Git 安装成功"
else
    echo "❌ Git 安装失败"
    exit 1
fi
```

---

## 🎯 实际应用场景

### 场景 1：服务器初始化

```bash
# 验证基础软件
python3 /home/admin/.openclaw/workspace/tools/install-validator.py git
python3 /home/admin/.openclaw/workspace/tools/install-validator.py python
python3 /home/admin/.openclaw/workspace/tools/install-validator.py nodejs
python3 /home/admin/.openclaw/workspace/tools/install-validator.py docker
```

---

### 场景 2：部署前检查

```bash
# 检查所有依赖
python3 /home/admin/.openclaw/workspace/tools/install-validator.py nginx
python3 /home/admin/.openclaw/workspace/tools/install-validator.py mysql
python3 /home/admin/.openclaw/workspace/tools/install-validator.py redis
python3 /home/admin/.openclaw/workspace/tools/install-validator.py --python flask
python3 /home/admin/.openclaw/workspace/tools/install-validator.py --node pm2
```

---

### 场景 3：故障排查

```bash
# Docker 不工作？
python3 /home/admin/.openclaw/workspace/tools/install-validator.py docker

# 输出会显示具体哪个检查失败：
# ❌ 进程检查：dockerd - 进程未运行
# → 解决：systemctl start docker
```

---

## 📄 相关文件

| 文件 | 位置 | 说明 |
|------|------|------|
| **install-validator.py** | `tools/` | 验证工具主程序 |
| **INSTALL-VALIDATOR-GUIDE.md** | `workspace/` | 使用指南 |
| **MEMORY.md** | `workspace/` | 安装验证规范 |

---

## 📊 验证模板统计

| 类别 | 数量 | 软件 |
|------|------|------|
| **代理工具** | 1 | Clash/Mihomo |
| **版本控制** | 1 | Git |
| **容器化** | 1 | Docker |
| **Web 服务器** | 1 | Nginx |
| **数据库** | 2 | MySQL, Redis |
| **运行时** | 5 | Node.js, Python, Java, Go, Rust |
| **包管理器** | 3 | npm, pnpm, Yarn |
| **进程管理** | 1 | PM2 |

**总计:** 15+ 个验证模板

---

**创建时间:** 2026-03-17  
**最后更新:** 2026-03-17 20:15

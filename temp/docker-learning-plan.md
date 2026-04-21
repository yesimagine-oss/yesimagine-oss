# 🐳 Docker 学习计划

**创建时间:** 2026-03-15 12:55  
**目标:** 掌握 Docker 基础 + Playwright 容器化

---

## 📅 3 天学习计划

### Day 1: Docker 基础

#### 上午 (2 小时)
- [ ] **核心概念**
  - 镜像 (Image): 只读模板
  - 容器 (Container): 运行中的镜像
  - Dockerfile: 构建镜像的脚本
  - Docker Compose: 多容器管理

- [ ] **安装 Docker**
  ```bash
  # CentOS/RHEL
  sudo yum install -y docker
  sudo systemctl start docker
  sudo systemctl enable docker
  
  # 验证安装
  docker --version
  docker run hello-world
  ```

#### 下午 (2 小时)
- [ ] **基本命令**
  ```bash
  # 拉取镜像
  docker pull python:3.10
  
  # 运行容器
  docker run -it python:3.10 bash
  
  # 查看容器
  docker ps
  docker ps -a
  
  # 停止/删除容器
  docker stop <container_id>
  docker rm <container_id>
  ```

- [ ] **镜像管理**
  ```bash
  # 查看镜像
  docker images
  
  # 删除镜像
  docker rmi <image_id>
  
  # 构建镜像
  docker build -t myimage .
  ```

#### 晚上 (1 小时)
- [ ] **练习:** Docker 命令练习
- [ ] **总结:** 核心概念理解

---

### Day 2: Dockerfile 与容器化

#### 上午 (2 小时)
- [ ] **Dockerfile 基础**
  ```dockerfile
  # 基础镜像
  FROM python:3.10
  
  # 工作目录
  WORKDIR /app
  
  # 复制文件
  COPY . /app
  
  # 安装依赖
  RUN pip install -r requirements.txt
  
  # 暴露端口
  EXPOSE 8080
  
  # 启动命令
  CMD ["python", "app.py"]
  ```

- [ ] **构建和运行**
  ```bash
  # 构建镜像
  docker build -t myapp:1.0 .
  
  # 运行容器
  docker run -p 8080:8080 myapp:1.0
  ```

#### 下午 (2 小时)
- [ ] **数据卷 (Volumes)**
  ```bash
  # 挂载本地目录
  docker run -v $(pwd):/app myapp
  
  # 命名卷
  docker volume create mydata
  docker run -v mydata:/data myapp
  ```

- [ ] **网络**
  ```bash
  # 创建网络
  docker network create mynet
  
  # 连接到网络
  docker run --network=mynet myapp
  ```

#### 晚上 (1 小时)
- [ ] **练习:** 容器化简单应用
- [ ] **总结:** Dockerfile 最佳实践

---

### Day 3: Playwright 容器化

#### 上午 (2 小时)
- [ ] **Playwright 官方镜像**
  ```bash
  # 拉取镜像
  docker pull mcr.microsoft.com/playwright/python
  
  # 运行容器
  docker run -it mcr.microsoft.com/playwright/python bash
  ```

- [ ] **运行脚本**
  ```bash
  # 挂载代码并运行
  docker run -v $(pwd):/app -w /app \
    mcr.microsoft.com/playwright/python \
    python script.py
  ```

#### 下午 (2 小时)
- [ ] **创建自定义镜像**
  ```dockerfile
  FROM mcr.microsoft.com/playwright/python
  
  WORKDIR /app
  COPY . /app
  
  CMD ["python", "read_wechat.py"]
  ```

- [ ] **Docker Compose**
  ```yaml
  version: '3'
  services:
    playwright:
      build: .
      volumes:
        - .:/app
      environment:
        - DISPLAY=:99
  ```

#### 晚上 (1 小时)
- [ ] **练习:** Playwright 容器化项目
- [ ] **总结:** 容器化优势
- [ ] **规划:** 下一步学习

---

## 📖 推荐资源

### 官方文档
- [Docker 官方](https://docs.docker.com/)
- [Playwright Docker](https://playwright.dev/docs/docker)

### 中文教程
- [Docker 从入门到实践](https://yeasy.gitbook.io/docker_practice/) ⭐⭐⭐⭐⭐
- [菜鸟教程 Docker](https://www.runoob.com/docker/docker-tutorial.html) ⭐⭐⭐⭐

### 互动平台
- [Play with Docker](https://labs.play-with-docker.com/)
- [Katacoda Docker](https://www.katacoda.com/courses/docker)

### 视频教程
- B 站搜索 "Docker 教程"
- YouTube "Docker Tutorial"

---

## 🔧 Playwright Docker 实战

### 基础示例

```dockerfile
# Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.40.0

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "read_article.py"]
```

### 运行命令

```bash
# 构建镜像
docker build -t wechat-reader .

# 运行
docker run --rm \
  -v $(pwd):/app \
  -e ARTICLE_URL="https://mp.weixin.qq.com/s/xxx" \
  wechat-reader
```

### Docker Compose

```yaml
version: '3.8'

services:
  reader:
    build: .
    volumes:
      - .:/app
      - output:/app/output
    environment:
      - ARTICLE_URL=${ARTICLE_URL}

volumes:
  output:
```

---

## 📝 每日记录模板

```markdown
## Day X - YYYY-MM-DD

### 学习内容
- 

### Docker 命令
```bash

```

### Dockerfile
```dockerfile

```

### 遇到的问题
1. 

### 解决方案
1. 

### 明日计划
- 

```

---

## 🎯 学习检查清单

### Day 1 检查
- [ ] 理解镜像和容器的区别
- [ ] 能运行基本容器
- [ ] 掌握常用 Docker 命令

### Day 2 检查
- [ ] 能编写 Dockerfile
- [ ] 能构建和运行镜像
- [ ] 理解数据卷和网络

### Day 3 检查
- [ ] 能使用 Playwright 镜像
- [ ] 能容器化 Python 项目
- [ ] 理解 Docker Compose

---

**预计完成时间:** 2026-03-18  
**总学习时间:** 15 小时

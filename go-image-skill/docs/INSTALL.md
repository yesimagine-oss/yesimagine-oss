# Go Image Skill 安装指南

---

## 方式一：从源码编译

### 前置要求

- Go 1.21+
- Git
- Make (可选)

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/openclaw/go-image-skill.git
cd go-image-skill

# 安装依赖
go mod download

# 构建
make build

# 验证安装
./image-skill version
```

---

## 方式二：下载预编译二进制

### Linux

```bash
# 下载
wget https://github.com/openclaw/go-image-skill/releases/latest/download/image-skill-linux-amd64

# 添加执行权限
chmod +x image-skill-linux-amd64

# 移动到 PATH
sudo mv image-skill-linux-amd64 /usr/local/bin/image-skill

# 验证
image-skill version
```

### macOS

```bash
# 下载
wget https://github.com/openclaw/go-image-skill/releases/latest/download/image-skill-darwin-amd64

# 添加执行权限
chmod +x image-skill-darwin-amd64

# 移动到 PATH
sudo mv image-skill-darwin-amd64 /usr/local/bin/image-skill

# 验证
image-skill version
```

### Windows

```powershell
# 下载
Invoke-WebRequest -Uri "https://github.com/openclaw/go-image-skill/releases/latest/download/image-skill-windows-amd64.exe" -OutFile "image-skill.exe"

# 移动到 PATH
Move-Item "image-skill.exe" "C:\Windows\System32\"

# 验证
image-skill version
```

---

## 方式三：Docker

```bash
# 拉取镜像
docker pull go-image-skill:latest

# 运行 CLI
docker run --rm -v $(pwd):/data go-image-skill analyze /data/photo.jpg

# 运行 HTTP 服务
docker run -d -p 8080:8080 -v $(pwd)/data:/app/data go-image-skill serve
```

---

## 方式四：OpenClaw Skill

```bash
# 安装 Skill
cd go-image-skill
openclaw skill install .

# 验证
openclaw skill list
```

---

## 配置

### 默认配置

配置文件位于 `configs/config.yaml`

### 自定义配置

```bash
# 复制配置文件
cp configs/config.yaml configs/config.local.yaml

# 编辑配置
vim configs/config.local.yaml

# 使用自定义配置启动
./image-skill serve --config configs/config.local.yaml
```

---

## 验证安装

### CLI 测试

```bash
# 显示帮助
image-skill help

# 显示版本
image-skill version

# 分析测试图片
image-skill analyze test.jpg
```

### HTTP API 测试

```bash
# 启动服务
image-skill serve --port 8080

# 健康检查
curl http://localhost:8080/health

# 分析图片
curl -X POST http://localhost:8080/analyze \
  -F "file=@test.jpg"
```

---

## 故障排除

### 问题：找不到命令

**解决：** 确保二进制文件在 PATH 中

```bash
export PATH=$PATH:/usr/local/bin
```

### 问题：权限不足

**解决：** 添加执行权限

```bash
chmod +x image-skill
```

### 问题：端口被占用

**解决：** 使用其他端口

```bash
image-skill serve --port 8081
```

### 问题：内存不足

**解决：** 限制并发数

```yaml
# config.yaml
queue:
  workers: 2  # 减少工作协程数
```

---

## 下一步

- 阅读 [使用文档](USAGE.md)
- 查看 [API 文档](API.md)
- 了解 [配置选项](CONFIG.md)

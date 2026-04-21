# Go Image Skill - 全能型图像分析工具

**版本:** 1.0.0  
**语言:** Go 1.21+  
**部署:** OpenClaw Skill / HTTP API / CLI / Docker  
**状态:** 开发中

---

## 功能清单 (30 项)

### 基础功能 (12 项)

| # | 功能 | 状态 |
|---|------|------|
| 1 | 上传与下载 | ⏳ |
| 2 | 本地保存图片 | ⏳ |
| 3 | 本地搜索图片 | ⏳ |
| 4 | 通过飞书发送 | ⏳ |
| 5 | 多格式加载 | ⏳ |
| 6 | 颜色分析 | ⏳ |
| 7 | 结构特征 | ⏳ |
| 8 | 文字识别 OCR | ⏳ |
| 9 | 物体检测 | ⏳ |
| 10 | 场景识别 | ⏳ |
| 11 | 图像比对 | ⏳ |
| 12 | EXIF 元数据 | ⏳ |

### 高级功能 (10 项)

| # | 功能 | 状态 |
|---|------|------|
| 13 | 重复图片检测 | ⏳ |
| 14 | 图像分类整理 | ⏳ |
| 15 | 图像压缩优化 | ⏳ |
| 16 | 批量重命名 | ⏳ |
| 17 | 图像搜索索引 | ⏳ |
| 18 | 隐私信息模糊 | ⏳ |
| 19 | 图像时间线分析 | ⏳ |
| 20 | 图像问答 | ⏳ |
| 21 | 搜索查询 | ⏳ |
| 22 | 对比描述 | ⏳ |

### Agent 专属功能 (8 项)

| # | 功能 | 状态 |
|---|------|------|
| 23 | 多轮对话上下文 | ⏳ |
| 24 | 图片引用链 | ⏳ |
| 25 | 批量分析队列 | ⏳ |
| 26 | 分析结果缓存 | ⏳ |
| 27 | 模糊查询处理 | ⏳ |
| 28 | 多模态输出 | ⏳ |
| 29 | 置信度报告 | ⏳ |
| 30 | 意图识别 | ⏳ |

---

## 快速开始

### CLI 使用

```bash
# 安装
go build -o image-skill cmd/main.go

# 分析单张图片
./image-skill analyze photo.jpg

# 批量分析
./image-skill batch ./photos/

# 自然语言查询
./image-skill query "照片里有几个人？" photo.jpg
```

### HTTP API

```bash
# 启动服务
./image-skill serve --port 8080

# 调用 API
curl -X POST http://localhost:8080/analyze \
  -F "file=@photo.jpg" \
  -F "query=有几个人？"
```

### OpenClaw Skill

```bash
# 安装 Skill
openclaw skill install ./go-image-skill

# 飞书使用
发送图片 + "/analyze 这张图里有什么？"
```

### Docker

```bash
# 构建镜像
docker build -t go-image-skill:latest .

# 运行
docker run -p 8080:8080 -v ./data:/data go-image-skill serve
```

---

## 项目结构

```
go-image-skill/
├── cmd/                    # 命令行入口
│   └── main.go
├── internal/               # 内部包
│   ├── image/              # 图像处理核心
│   ├── api/                # HTTP API
│   ├── cli/                # CLI 命令
│   ├── nlp/                # 自然语言处理
│   ├── cache/              # 结果缓存
│   └── queue/              # 批量队列
├── pkg/                    # 公共包
│   ├── models/             # 数据模型
│   └── utils/              # 工具函数
├── configs/                # 配置文件
├── tests/                  # 测试用例
├── docs/                   # 文档
└── images/                 # 示例图片
```

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Go 1.21+ |
| 图像处理 | imaging/resize/gosseract |
| OCR | Tesseract (gosseract) |
| HTTP 服务 | net/http |
| 缓存 | 内存 + SQLite |
| 队列 | Channel + Goroutine |

---

## 许可证

MIT License

---

**开发团队:** Red AgentTeam  
**最后更新:** 2026-04-15

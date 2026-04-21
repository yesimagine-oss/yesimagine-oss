# Go Image Skill Dockerfile

# 构建阶段
FROM golang:1.21-alpine AS builder

WORKDIR /app

# 安装依赖
RUN apk add --no-cache git

# 复制 go.mod 和 go.sum
COPY go.mod go.sum ./
RUN go mod download

# 复制源代码
COPY . .

# 构建
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o image-skill cmd/main.go

# 运行阶段
FROM alpine:latest

WORKDIR /app

# 安装运行时依赖
RUN apk add --no-cache ca-certificates

# 从构建阶段复制二进制文件
COPY --from=builder /app/image-skill .
COPY --from=builder /app/configs ./configs

# 创建数据目录
RUN mkdir -p /app/data /app/logs

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD ./image-skill health || exit 1

# 启动命令
ENTRYPOINT ["./image-skill"]
CMD ["serve", "--port", "8080"]

# Go Image Skill Makefile

.PHONY: all build test clean run serve docker docker-push lint fmt vet

# 变量
BINARY_NAME=image-skill
VERSION=1.0.0
BUILD_TIME=$(shell date -u +'%Y-%m-%dT%H:%M:%SZ')
GIT_COMMIT=$(shell git rev-parse HEAD)

# 默认目标
all: build

# 构建
build:
	@echo "构建 ${BINARY_NAME} v${VERSION}..."
	go build -ldflags "-X main.Version=${VERSION} -X main.BuildTime=${BUILD_TIME} -X main.GitCommit=${GIT_COMMIT}" \
		-o ${BINARY_NAME} cmd/main.go

# 测试
test:
	@echo "运行测试..."
	go test ./... -v -cover

# 测试覆盖率
coverage:
	@echo "生成测试覆盖率报告..."
	go test ./... -coverprofile=coverage.out
	go tool cover -html=coverage.out -o coverage.html

# 清理
clean:
	@echo "清理构建文件..."
	rm -f ${BINARY_NAME}
	rm -rf data/ logs/ cache/
	go clean

# 运行 CLI
run: build
	./${BINARY_NAME} help

# 启动 HTTP 服务
serve: build
	./${BINARY_NAME} serve --port 8080

# Docker 构建
docker:
	@echo "构建 Docker 镜像..."
	docker build -t go-image-skill:${VERSION} .
	docker tag go-image-skill:${VERSION} go-image-skill:latest

# Docker 推送
docker-push: docker
	@echo "推送 Docker 镜像..."
	docker push go-image-skill:${VERSION}
	docker push go-image-skill:latest

# 代码检查
lint:
	@echo "运行 linter..."
	golangci-lint run

# 格式化代码
fmt:
	@echo "格式化代码..."
	go fmt ./...

# 代码检查
vet:
	@echo "运行 vet..."
	go vet ./...

# 安装依赖
deps:
	@echo "安装依赖..."
	go mod download
	go mod tidy

# 生成文档
docs:
	@echo "生成文档..."
	godoc -http=:6060 &

# 开发环境
dev: deps fmt vet build test

# 生产环境
prod: lint vet build test docker

# 帮助
help:
	@echo "Go Image Skill Makefile"
	@echo ""
	@echo "目标:"
	@echo "  all        - 构建项目 (默认)"
	@echo "  build      - 构建二进制文件"
	@echo "  test       - 运行测试"
	@echo "  coverage   - 生成测试覆盖率报告"
	@echo "  clean      - 清理构建文件"
	@echo "  run        - 运行 CLI"
	@echo "  serve      - 启动 HTTP 服务"
	@echo "  docker     - 构建 Docker 镜像"
	@echo "  docker-push- 推送 Docker 镜像"
	@echo "  lint       - 代码检查"
	@echo "  fmt        - 格式化代码"
	@echo "  vet        - 代码检查"
	@echo "  deps       - 安装依赖"
	@echo "  docs       - 生成文档"
	@echo "  dev        - 开发环境设置"
	@echo "  prod       - 生产环境构建"
	@echo "  help       - 显示帮助"

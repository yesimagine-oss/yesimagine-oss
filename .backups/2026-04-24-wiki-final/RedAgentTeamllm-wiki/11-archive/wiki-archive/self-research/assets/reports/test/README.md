# goEX - Go Headless Browser Automation

**版本**: v0.1.0  
**Go**: 1.26+  
**状态**: Phase 1 开发中

---

## 功能

- ✅ 导航/定位/点击/截图
- ✅ HTML 解析/JS 执行
- ✅ Cookie/多标签页管理
- ✅ 网页爬取
- ✅ 飞书推送
- ✅ 自然语言解析（关键字匹配）
- ✅ HTTP API（Gin）
- ✅ 插件系统（Go plugin）
- ✅ 快捷方式配置

---

## 快速开始

```bash
# 安装依赖
go mod tidy

# 运行
go run cmd/main.go

# 构建
go build -o goex cmd/main.go
```

---

## 目录结构

```
~/.goex/
├── cmd/              # 主程序入口
├── internal/         # 内部包
├── plugins/          # 插件目录
├── sessions/         # 会话数据
├── config.yaml       # 配置文件
└── README.md
```

---

## API 示例

```bash
# 导航
curl -X POST http://localhost:8080/navigate \
  -d '{"url": "https://mp.weixin.qq.com"}'

# 截图
curl -X GET http://localhost:8080/screenshot -o shot.png

# 点击
curl -X POST http://localhost:8080/click \
  -d '{"selector": "#login"}'
```

---

**开发中** | 2026-04-16

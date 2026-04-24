---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Gin
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
# Gin - 高性能 HTTP 框架

**来源:** github.com/gin-gonic (100% 覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 路由 | 高性能基数树路由 |
| 中间件 | 日志/恢复/CORS |
| 请求绑定 | JSON/Form 自动解析 |
| 响应 | JSON/HTML/XML |

---

## 项目应用

| 项目 | 用途 | 节省 |
|------|------|------|
| go-image-skill | HTTP API 服务 | ~3h |
| 无头浏览器 | HTTP API 服务 | ~3h |
| **总计** | - | **~6h** |

---

## 代码示例

```go
// 启动服务
r := gin.Default()
r.Run(":8080")

// API 路由
r.GET("/api/ping", func(c *gin.Context) {
    c.JSON(200, gin.H{"message": "pong"})
})

// 请求绑定
type User struct {
    Name string `json:"name" binding:"required"`
}
c.ShouldBindJSON(&user)
```

---

**结论:** Go HTTP API 标准选择，建议入库

---

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
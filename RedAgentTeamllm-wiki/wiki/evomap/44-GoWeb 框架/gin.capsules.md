---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Gin.Capsules
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
# Capsule: gin_quickstart_default

**Trigger**: Official minimal working example

**Code**:
```go
package main
import "github.com/gin-gonic/gin"
func main() {
 r := gin.Default()
 r.GET("/ping", func(c *gin.Context) {
 c.JSON(200, gin.H{"message": "pong"})
 })
 r.Run(":8080")
}
```

---

# Capsule: gin_json_post

**Trigger**: JSON body bind + response

**Code**:
```go
type User struct {
 Name string `json:"name" binding:"required"`
}
r.POST("/user", func(c *gin.Context) {
 var u User
 if err := c.ShouldBindJSON(&u); err != nil {
 c.JSON(400, gin.H{"err": err.Error()})
 return
 }
 c.JSON(200, u)
})
```

---

# Capsule: gin_release_mode

**Trigger**: Production mode setup

**Code**:
```go
gin.SetMode(gin.ReleaseMode)
r := gin.Default()
```

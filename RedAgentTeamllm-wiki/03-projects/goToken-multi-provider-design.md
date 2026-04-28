# goToken 多模型多方案优化设计方案

**创建时间：** 2026-04-26 15:29 GMT+8  
**状态：** 待执行  
**维护者：** Red Agent Team

---

## 📋 背景

### 现有问题
- goToken 仅支持百炼（DashScope）单 Provider
- 当前主模型已切换为 MiniMax Token Plan
- goToken 与 MiniMax 未连通，无法服务新主模型

### 目标
让 goToken 同时支持百炼 + MiniMax Token Plan，自动路由，用户无论用什么模型都能节省 token

---

## 💡 核心创新点

| 创新点 | 描述 |
|--------|------|
| **多Provider动态路由** | 自动选择可用 Provider |
| **统一缓存层** | 一个缓存服务所有 Provider |
| **Provider-agnostic Key** | 避免答案混淆 |
| **Token Plan 感知** | 优先使用 MiniMax Token Plan |
| **Fallback机制** | Provider 不可用自动切换 |

---

## 📊 架构设计

```
OpenClaw Gateway
    ↓
goToken Skill (多Provider缓存层)
    ├── Bailian Provider (百炼)
    └── MiniMax Provider (Token Plan)
            ↓
    统一缓存管理层 (TTL 2h)
```

---

## 🔧 核心代码模块

### 1. Provider配置 (providers.go)
```go
type ProviderConfig struct {
    Name       string // "bailian", "minimax"
    BaseURL   string
    APIKey    string
    Model     string
    APIVersion string // "openai" | "anthropic" | "dashscope"
    Priority  int    // 数字越小越高
    Enabled   bool
}

func getEnabledProviders() []*ProviderConfig {
    // 从环境变量读取所有Provider配置
}
```

### 2. 统一API调用 (api_call.go)
```go
func (gt *goToken) callProvider(provider *ProviderConfig, prompt string) (string, error) {
    switch provider.APIVersion {
    case "anthropic":  return gt.callAnthropic(provider, prompt)
    case "dashscope":   return gt.callDashScope(provider, prompt)
    case "openai":     return gt.callOpenAI(provider, prompt)
    }
}
```

### 3. 智能路由 (router.go)
```go
func (gt *goToken) routeRequest(prompt string) (*ProviderConfig, error) {
    providers := getEnabledProviders()
    sort.Slice(providers, func(i, j int) bool {
        return providers[i].Priority < providers[j].Priority
    })
    for _, p := range providers {
        if p.Enabled && gt.testProvider(p) {
            return p, nil
        }
    }
}
```

### 4. Provider-agnostic缓存Key
```go
func (gt *goToken) generateCacheKey(provider, model, prompt string) string {
    combined := fmt.Sprintf("%s:%s:%s", provider, model, prompt)
    return hash(combined)
}
```

---

## ⚙️ 环境变量配置

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | 百炼 API Key |
| `BAILIAN_MODEL` | 百炼模型，默认 qwen3.5-plus |
| `ANTHROPIC_API_KEY` | MiniMax API Key |
| `MINIMAX_MODEL` | MiniMax 模型，默认 MiniMax-M2.7 |

---

## 📁 待修改文件

| 文件 | 位置 | 操作 |
|------|------|------|
| `providers.go` | `/opt/openclaw/gateway/skills/goToken/` | 新增 |
| `api_call.go` | `/opt/openclaw/gateway/skills/goToken/` | 改造 |
| `router.go` | `/opt/openclaw/gateway/skills/goToken/` | 新增 |
| `main.go` | `/opt/openclaw/gateway/skills/goToken/` | 改造 |

---

## ⚠️ 待确认事项

1. **编译环境**：Go 1.x 编译环境是否可用？
2. **API Key配置**：百炼和MiniMax的Key是否都已在环境变量中？
3. **优先级策略**：百炼和MiniMax的优先级如何设定？
4. **测试计划**：如何在不影响生产的情况下测试？

---

## 📈 预期效果

| 指标 | 当前 | 优化后 |
|------|------|---------|
| Provider支持 | 1 (百炼) | 2+ |
| Token节省率 | 75% | 75%+ |
| 缓存命中率 | 75% | 80%+ |
| 可用性 | 单点故障 | 自动切换 |

---

**记录时间：** 2026-04-26 15:29 GMT+8  
**下次审查：** 待定

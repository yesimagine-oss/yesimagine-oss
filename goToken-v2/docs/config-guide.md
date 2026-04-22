# goToken-v2 配置指南

**版本**: v2.0.0  
**创建时间**: 2026-04-22

---

## 📁 配置文件位置

```
/opt/openclaw/gateway/skills/goToken/config/config.yaml
```

---

## 🔧 配置项说明

### 缓存设置

| 配置项 | 默认值 | 说明 | 建议 |
|--------|--------|------|------|
| `cache.ttl_hours` | 2 | 缓存有效期（小时） | 2-4 小时 |
| `cache.max_tokens` | 300 | 最大 Token 数 | 300-500 |

**示例**：
```yaml
cache:
  ttl_hours: 4      # 缓存 4 小时
  max_tokens: 500   # 允许 500 Token
```

---

### 模型设置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `model.name` | qwen-coding-lite | 使用的模型 |
| `model.api_base` | (自动) | API 地址（一般不改） |

**可选模型**：
- `qwen-coding-lite` → 省 Token（推荐）
- `qwen3.5-plus` → 质量好，费 Token
- `qwen-max` → 最好，最贵

---

### 监控设置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `monitoring.enabled` | true | 是否启用监控 |
| `monitoring.log_path` | (自动) | 监控日志路径 |
| `monitoring.stats_interval` | 60 | 统计间隔（秒） |

---

### 限流设置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `rate_limit.max_concurrent` | 2 | 最大并发请求 |
| `rate_limit.enabled` | true | 是否启用限流 |

---

## 📝 修改配置步骤

### 步骤 1: 编辑配置文件

```bash
nano /opt/openclaw/gateway/skills/goToken/config/config.yaml
```

### 步骤 2: 保存并重启 Gateway

```bash
openclaw gateway restart
```

### 步骤 3: 验证配置生效

```bash
# 查看 Gateway 日志
tail /tmp/openclaw/openclaw-2026-04-22.log | grep "配置文件已加载"
```

**看到类似输出**：
```
✅ 配置文件已加载：/opt/openclaw/gateway/skills/goToken/config/config.yaml
   缓存 TTL: 4 小时
   最大 Token: 500
   模型：qwen-coding-lite
```

---

## 🎯 常见配置场景

### 场景 1: 提高命中率（延长缓存）

```yaml
cache:
  ttl_hours: 4  # 从 2 小时→4 小时
```

**效果**：缓存时间更长，命中率更高  
**代价**：答案可能过时

---

### 场景 2: 提高质量（用更好的模型）

```yaml
model:
  name: qwen3.5-plus  # 从 lite→plus
```

**效果**：答案质量更好  
**代价**：Token 消耗更多

---

### 场景 3: 节省 Token（限制长度）

```yaml
cache:
  max_tokens: 200  # 从 300→200
```

**效果**：每次调用更省 Token  
**代价**：长答案可能被截断

---

### 场景 4: 关闭监控（极致性能）

```yaml
monitoring:
  enabled: false  # 关闭监控
```

**效果**：减少日志写入开销  
**代价**：无法查看统计数据

---

## ⚠️ 注意事项

1. **修改配置后必须重启 Gateway**
2. **配置文件格式是 YAML，注意缩进**
3. **不要删除注释，方便以后参考**
4. **改之前备份**：
   ```bash
   cp config.yaml config.yaml.backup
   ```

---

## 📊 配置优化建议

| 使用场景 | TTL | Max Tokens | 模型 |
|---------|-----|------------|------|
| **日常问答** | 2h | 300 | qwen-coding-lite |
| **代码生成** | 4h | 500 | qwen3.5-plus |
| **文档生成** | 4h | 800 | qwen3.5-plus |
| **实时数据** | 0.5h | 300 | qwen-coding-lite |

---

**最后更新**: 2026-04-22  
**状态**: ✅ 配置分离完成

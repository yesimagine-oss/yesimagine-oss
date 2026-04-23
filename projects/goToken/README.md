# goToken - 穷逼专用 Token 优化器

> **用 75% 更少 Token，做 100% 相同的事**

---

## 🎯 这是什么？

goToken 是一个**智能 Token 缓存优化器**，专为 OpenClaw 设计。

**核心功能**：
- ✅ 智能缓存：相同问题不重复调用 API
- ✅ 语义匹配：相似问题自动复用答案
- ✅ 限流保护：防止 API 额度超限
- ✅ 自动清理：定期删除过期缓存

**适用场景**：
- ✅ 重复问答（常见问题）
- ✅ 模板化内容（固定格式）
- ✅ API 额度紧张（省钱！）

**不适用**：
- ❌ 实时数据（天气/股价）
- ❌ 个性化对话
- ❌ 长文本生成

---

## 📊 性能指标

| 指标 | 实测值 | 说明 |
|------|--------|------|
| **缓存命中率** | 75% | 20 题真实场景测试 |
| **Token 节省** | 75% | 相比无缓存 |
| **响应速度** | <10ms | 缓存命中时 |
| **API 错误率** | 0% | 完整错误处理 |

---

## 🚀 快速开始

### 安装

```bash
# 使用 ClawHub CLI
clawhub install gotoken
```

### 配置

**环境变量**（可选）：

```bash
# 缓存有效期（小时），默认 2 小时
export CACHE_TTL_HOURS=2

# 最大 Token 数，默认 300
export MAX_TOKENS=300

# 使用的模型，默认 qwen-coding-lite
export LLM_MODEL=qwen-coding-lite

# DashScope API Key（必需）
export DASHSCOPE_API_KEY=your_api_key
```

### 使用

**自动生效**，无需额外操作！

goToken 会自动拦截你的请求，检查缓存：
- 缓存命中 → 直接返回（<10ms，0 Token）
- 缓存未命中 → 调用 API → 缓存答案

---

## 📝 示例

### 场景 1: 重复问题

```
第 1 次：什么是 OpenClaw？
→ API 调用（消耗 Token）

第 2 次：什么是 OpenClaw？
→ 缓存命中（0 Token，<10ms）

第 3 次：OpenClaw 是什么？
→ 语义匹配命中（0 Token，<10ms）
```

### 场景 2: 额度保护

```
并发请求超过 2 个 → 自动限流
API 错误 → 友好提示："本周额度已达上限，将在周一重置"
```

---

## 🔧 高级配置

### 调整缓存策略

```yaml
# 延长缓存时间（适合固定知识）
CACHE_TTL_HOURS=24

# 缩短缓存时间（适合变化内容）
CACHE_TTL_HOURS=0.5
```

### 查看缓存统计

```bash
# 查看命中率
goToken stats
```

---

## ⚠️ 注意事项

1. **API Key 安全**：DASHSCOPE_API_KEY 仅存储在本地
2. **缓存隐私**：缓存内容存储在本地，不会上传
3. **实时数据**：天气/股价等实时数据建议关闭缓存

---

## 📦 技术栈

- **语言**: Go 1.21+
- **API**: DashScope (阿里百炼)
- **模型**: qwen-coding-lite
- **缓存**: 内存 Map + RWMutex
- **相似度**: 余弦相似度 + 编辑距离 + 关键词匹配

---

## 📊 版本历史

### v1.0.2 (当前)
- ✅ 语义相似度缓存（75% 命中率）
- ✅ 并发限流（最多 2 个同时请求）
- ✅ 完整错误处理
- ✅ 定期缓存清理

### v1.0.1
- ✅ 基础缓存功能
- ✅ Prompt 压缩

### v1.0.0
- ✅ 初始版本

---

## 🤝 贡献

**问题反馈**: https://github.com/yesimagine-oss/goToken/issues

**代码贡献**: 欢迎 PR！

---

## 📄 许可证

MIT-0（完全免费，随便用）

---

## 🦞 开发者

**Red Agent Team**  
**GitHub**: https://github.com/yesimagine-oss

---

**Slogan**: 穷逼专用，Token 省 75%！

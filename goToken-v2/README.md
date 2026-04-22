# goToken-v2 Token 缓存优化器

**版本**: v2.0.0  
**创建时间**: 2026-04-22  
**状态**: 🧪 开发测试中

---

## 🎯 功能

- ✅ 智能缓存（相同问题不重复调用 API）
- ✅ 配置分离（YAML 配置文件）
- ✅ 测试套件（6 个自动化测试）
- ✅ 报告导出（JSON+CSV）
- ✅ 透明模式（用户可查看可关闭）

---

## 🚀 快速开始

### 1. 测试配置

```bash
cd /home/admin/.openclaw/workspace/goToken-v2
cat config/config.yaml
```

### 2. 运行测试

```bash
cd test
bash run_tests.sh
```

### 3. 查看初始数据

```bash
cat logs/metrics.json
```

---

## 📁 目录结构

```
goToken-v2/
├── src/              # 源代码
│   ├── main.go       # 主程序
│   ├── config.go     # 配置读取
│   ├── report.go     # 报告生成
│   └── ...
├── config/           # 配置文件
│   └── config.yaml   # 配置（可修改）
├── test/             # 测试
│   ├── test_suite.go
│   └── run_tests.sh
├── logs/             # 日志和数据
│   └── metrics.json  # 监控数据
└── docs/             # 文档
    ├── config-guide.md
    ├── test-guide.md
    └── report-guide.md
```

---

## 📊 当前状态

| 模块 | 状态 |
|------|------|
| **配置分离** | ✅ 完成 |
| **测试套件** | ✅ 完成（6 个测试） |
| **报告导出** | ✅ 完成 |
| **数据录入** | ✅ 初始化完成 |
| **语义匹配** | ⏳ 待开发 |
| **Web 看板** | ⏳ 待开发 |

---

## 🧪 测试运行

```bash
cd /home/admin/.openclaw/workspace/goToken-v2/test
go run test_suite.go
```

**预期输出**：
```
🧪 goToken-v2 测试套件
================================
✅ 缓存命中测试 (0.01s)
✅ 缓存未命中测试 (0.00s)
✅ TTL 过期测试 (1.02s)
✅ 限流保护测试 (0.05s)
✅ 空查询处理测试 (0.00s)
✅ 配置加载测试 (0.01s)

================================
📊 测试完成：6 通过，0 失败，6 总计
⏱️  总耗时：1.09s
================================
```

---

## 📝 下一步

1. **运行测试** → 验证所有功能
2. **积累数据** → 运行 7 天收集真实数据
3. **P2 开发** → 语义匹配 + Web 看板

---

**开发日志**: `docs/dev-log-20260422.md`

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

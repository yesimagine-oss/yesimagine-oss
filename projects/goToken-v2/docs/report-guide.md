# goToken-v2 报告指南

**版本**: v2.0.0  
**创建时间**: 2026-04-22

---

## 📊 报告类型

| 报告 | 格式 | 说明 |
|------|------|------|
| **统计报告** | JSON | 详细统计数据 |
| **CSV 报告** | CSV | Excel 可打开 |
| **控制台摘要** | 文本 | 快速查看 |

---

## 🚀 生成报告

### 方法 1: 命令行生成

```bash
cd /home/admin/.openclaw/workspace/goToken-v2
go run src/report.go
```

### 方法 2: 自动定期生成

**配置**：
```yaml
# config/config.yaml
monitoring:
  enabled: true
  report_interval: 86400  # 每天生成一次报告（秒）
```

---

## 📁 报告位置

```
goToken-v2/logs/
├── metrics.json          # 原始监控数据
├── token_report.json     # JSON 报告
└── token_report.csv      # CSV 报告
```

---

## 📈 报告内容

### JSON 报告示例

```json
{
  "period": "自启动至今",
  "total_requests": 1000,
  "cache_hits": 750,
  "cache_misses": 250,
  "hit_rate": 75.0,
  "tokens_saved": 600000,
  "cost_saved": 1.20,
  "timestamp": "2026-04-22T13:20:00+08:00"
}
```

### CSV 报告示例

```csv
指标，数值，说明
总请求数，1000，统计周期内总请求
缓存命中，750，从缓存返回的请求
缓存未命中，250，调用 API 的请求
命中率，75.0%,命中/总请求
节省 Token,600000，缓存命中节省的 Token
节省金额，¥1.20，按¥1=50 万 Token 计算
```

---

## 💰 费用计算说明

**定价参考**（百炼 Coding Plan）：

| 套餐 | Token/月 | 价格 | 单价 |
|------|---------|------|------|
| 免费版 | 200 万 | ¥0 | - |
| 基础版 | 1000 万 | ¥99 | ¥0.0099/万 |
| 专业版 | 5000 万 | ¥399 | ¥0.00798/万 |

**goToken 计算**：
- 假设每次 API 调用 800 Token
- 按 ¥1 = 50 万 Token 估算
- 实际价格以官方为准

---

## 🎯 报告使用场景

### 场景 1: 评估 goToken 效果

```bash
# 查看节省了多少 Token
cat logs/token_report.json | jq .tokens_saved
```

### 场景 2: 选择套餐

```bash
# 查看每月用量预估
# 总请求 → 去重后实际 API 调用 → 选套餐
```

### 场景 3: 向老板汇报

```bash
# 打印报告摘要
go run src/report.go

# 输出：
# 节省金额：¥XX.XX
# 命中率：XX%
```

---

## 📝 最佳实践

### 1. 定期查看报告

```bash
# 每天查看
cat logs/token_report.json

# 或每周汇总
```

### 2. 根据报告优化配置

| 命中率 | 建议 |
|--------|------|
| <50% | 增加 TTL 时间 |
| 50-70% | 正常 |
| >70% | 优秀，保持 |

### 3. 存档报告

```bash
# 每月归档
cp logs/token_report.json logs/token_report-2026-04.json
```

---

**最后更新**: 2026-04-22  
**状态**: ✅ 报告功能完成

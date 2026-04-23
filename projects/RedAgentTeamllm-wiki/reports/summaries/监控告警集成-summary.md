# Serper API 监控告警集成指南

**创建日期:** 2026-03-15  
**版本:** v1.0  
**状态:** ✅ 完成

---

## 📊 监控指标

### 核心指标

| 指标 | 类型 | 说明 | 告警阈值 |
|------|------|------|---------|
| `serper_requests_total` | Counter | 总请求数 | - |
| `serper_requests_failed` | Counter | 失败请求数 | > 1% |
| `serper_request_duration` | Histogram | 请求延迟 | P95 > 5s |
| `serper_credits_remaining` | Gauge | 剩余额度 | < 1000 |
| `serper_rate_limit_hits` | Counter | 限流次数 | > 0 |


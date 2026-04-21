# Serper API 错误处理大全

**创建日期:** 2026-03-15  
**版本:** v1.0  
**状态:** ✅ 完成

---

## 📋 错误代码总览

| 错误码 | 名称 | 说明 | 解决方案 |
|--------|------|------|---------|
| 400 | Bad Request | 请求参数错误 | 检查参数格式 |
| 401 | Unauthorized | API Key 无效 | 检查 API Key |
| 402 | Payment Required | 信用点数不足 | 充值或等待重置 |
| 429 | Too Many Requests | 请求频率过高 | 降低请求频率 |
| 500 | Internal Server Error | 服务器错误 | 稍后重试 |
| 503 | Service Unavailable | 服务不可用 | 稍后重试 |

---

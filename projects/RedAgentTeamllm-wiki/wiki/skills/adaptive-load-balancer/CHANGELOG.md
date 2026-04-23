---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 更新日志
- api
title: Changelog
type: general
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
# 更新日志

## [2.0.0] - 2026-03-27

### 🎉 新增功能
- ✅ QPS 追踪和速率限制
- ✅ 错误率滑动窗口（60 秒）
- ✅ 自动熔断机制（可配置阈值）
- ✅ 请求优先级队列（4 级优先级）
- ✅ Prometheus 指标导出（11 种指标）
- ✅ 自定义权重因子支持

### 🚀 性能改进
- 故障切换时间从 <1s 优化到 <0.5s
- 新增半开状态支持熔断器自动恢复
- 优化权重计算算法

### 📊 监控增强
- 新增 P99 延迟指标
- 新增 QPS 实时追踪
- 新增峰值 QPS 记录
- 新增熔断器状态监控

### 🐛 Bug 修复
- 修复空 Agent 列表时的异常
- 修复并发请求时的竞态条件

### 📚 文档
- 完整的 API 参考文档
- 4 个使用示例
- 故障排查指南
- Prometheus/Grafana 集成指南

## [1.0.0] - 2026-03-27

### 🎉 初始版本
- ✅ 动态权重计算（健康/容量/负载/响应时间）
- ✅ 一致性哈希路由（150 虚拟节点）
- ✅ 健康检查（主动 + 被动）
- ✅ 弹性伸缩建议
- ✅ 基础监控指标

### 📊 性能
- 吞吐量：74,608 req/s
- P99 延迟：<1ms
- 测试覆盖：21/21 单元测试

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]

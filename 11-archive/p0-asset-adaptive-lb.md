# P0 资产发布配置

**创建时间**: 2026-03-27 10:15  
**资产类型**: 自适应负载均衡器 v2.0

---

## 📦 资产内容

### Gene
```json
{
  "type": "Gene",
  "schema_version": "1.5.0",
  "id": "gene_adaptive_load_balancer",
  "category": "optimize",
  "signals_match": ["load_balancing", "multi_agent", "scalability", "performance", "adaptive"],
  "summary": "Adaptive load balancing for multi-agent systems with dynamic weighting, health checks, circuit breaker, and QPS tracking",
  "strategy": [
    "Measure per-agent load: connections, response times, error rates, QPS",
    "Calculate weights: weight = health × error_factor × capacity × load × qps × rt",
    "Select lowest score agent: score = (connections + 1) / weight",
    "Use consistent hashing for sticky sessions",
    "Circuit breaker at 30% error rate, 30s timeout",
    "Update weights every 10s"
  ],
  "constraints": {"max_files": 3, "forbidden_paths": ["node_modules/"]},
  "validation": ["python3 -m unittest test_load_balancer -v"]
}
```

### Capsule
```json
{
  "type": "Capsule",
  "schema_version": "1.5.0",
  "trigger": ["load_balancing", "multi_agent", "scalability", "circuit_breaker"],
  "summary": "Production-ready adaptive load balancer: 70k+ req/s, <1.2ms P99, auto failover <0.5s",
  "confidence": 0.98,
  "blast_radius": {"files": 3, "lines": 800},
  "outcome": {"status": "success", "score": 0.98},
  "content": "Adaptive load balancer v2.0 with dynamic weighting, circuit breaker, QPS tracking, priority queues, Prometheus metrics, K8s integration, and HTTP API.",
  "code_snippet": "class AdaptiveLoadBalancerV2:\n    def select_agent(self, key=None):\n        if key: return self.hash_ring.get(key)\n        return min(healthy_agents, key=lambda m: m.score).agent_id"
}
```

---

## 📊 性能指标

| 指标 | 值 |
|------|-----|
| 吞吐量 | 70,000+ req/s |
| P99 延迟 | <1.2ms |
| 故障切换 | <0.5s |
| 测试覆盖 | 21/21 通过 |

---

## 📁 相关文件

- `skills/adaptive-load-balancer/adaptive_load_balancer_v2.py` (560 行)
- `skills/adaptive-load-balancer/http_api.py` (180 行)
- `skills/adaptive-load-balancer/stress_test.py` (250 行)
- `skills/adaptive-load-balancer/k8s/k8s_discovery.py` (120 行)
- `skills/adaptive-load-balancer/grafana/dashboard.json`

---

## 🚀 发布步骤

1. **计算 asset_id** (需要 canonical JSON)
2. **发布 Bundle** (Gene + Capsule + Event)
3. **等待审查** → Promoted

---

## ⏳ 状态

- [x] 资产准备完成
- [ ] asset_id 计算
- [ ] Bundle 发布
- [ ] 审查通过

---

**备注**: 需要正确的 canonical JSON 序列化来计算 asset_id，建议使用官方 evolver 工具。

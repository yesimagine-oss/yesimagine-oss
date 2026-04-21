# Adaptive Load Balancer Skill

多 Agent 系统自适应负载均衡技能 - 智能请求分发、动态权重计算、自动熔断。

## 安装

```bash
clawhub install adaptive-load-balancer
```

## 使用

```python
from skills.adaptive_load_balancer import load_balancer

lb = load_balancer.get_instance()
agent = lb.select_agent()
lb.record_request(agent, success=True, response_time=100)
```

## 功能

- 动态权重计算（健康/容量/负载/QPS/响应时间）
- 自动熔断器（错误率触发，自动恢复）
- 请求优先级队列（4 级优先级）
- Prometheus 指标导出（11 种指标）
- 弹性伸缩建议
- 一致性哈希（粘性会话）

## 性能

- 吞吐量：>70,000 req/s
- P99 延迟：<1.2ms
- 故障切换：<0.5s

## 文档

完整文档：https://github.com/your-repo/adaptive-load-balancer-skill

## License

MIT

# 自适应负载均衡器 (Adaptive Load Balancer)

多 Agent 系统智能请求分发解决方案，实现动态权重分配、健康检查和弹性伸缩建议。

## 🚀 快速开始

### 安装

```python
# 无需依赖，使用 Python 标准库
from adaptive_load_balancer import AdaptiveLoadBalancer
```

### 基础用法

```python
from adaptive_load_balancer import AdaptiveLoadBalancer

# 创建负载均衡器
lb = AdaptiveLoadBalancer()

# 添加 Agent
lb.add_agent("agent_1", "http://localhost:8001")
lb.add_agent("agent_2", "http://localhost:8002")
lb.add_agent("agent_3", "http://localhost:8003")

# 选择最佳 Agent
agent_id = lb.select_agent()

# 转发请求（伪代码）
response = forward_to_agent(agent_id, request)

# 记录结果
lb.record_request(
    agent_id,
    success=(response.status == 200),
    response_time=response.time_ms
)
```

### 带一致性哈希的用法

```python
# 使用用户 ID 作为 key，保证同一用户的请求路由到同一 Agent
agent_id = lb.select_agent(key=user_id)
```

## 📊 核心特性

### 1. 动态权重计算

权重基于多维度指标：
- **健康得分**: 基于错误率和最近活跃时间
- **容量因子**: CPU 和内存使用情况
- **负载因子**: 当前活跃连接数
- **响应时间因子**: EWMA 平均响应时间

```python
weight = health_score × capacity_factor × load_factor × rt_factor
```

### 2. 智能健康检查

- **主动探测**: 后台线程定期检查 Agent 状态
- **被动监控**: 根据请求结果自动调整
- **故障切换**: 连续 3 次失败标记为不健康，自动排除

### 3. 一致性哈希路由

- 150 个虚拟节点，减少重新平衡影响
- 支持粘性会话（同一 key 路由到同一 Agent）
- 节点增减时最小化迁移成本

### 4. 弹性伸缩建议

```python
recommendation = lb.get_scaling_recommendation()
print(recommendation)
# {'action': 'scale_up', 'reason': '高负载', 'suggested_count': 4}
```

## 🔧 高级配置

```python
lb = AdaptiveLoadBalancer(
    health_check_interval=5.0,    # 健康检查间隔（秒）
    weight_update_interval=10.0   # 权重更新间隔（秒）
)
```

## 📈 监控指标

```python
stats = lb.get_stats()
print(stats)
# {
#   "total_agents": 3,
#   "healthy_agents": 3,
#   "degraded_agents": 0,
#   "unhealthy_agents": 0,
#   "agents": {
#     "agent_1": {
#       "status": "healthy",
#       "active_connections": 15,
#       "avg_response_time": "125.50ms",
#       "health_score": "0.98",
#       "weight": "0.85",
#       "error_rate": "2.1%"
#     }
#   }
# }
```

## 🧪 运行测试

```bash
python3 -m unittest test_load_balancer -v
```

### 测试覆盖

- ✅ 基础功能测试（添加/移除 Agent）
- ✅ 健康检查测试
- ✅ 权重计算测试
- ✅ 一致性哈希测试
- ✅ 并发请求测试（50 线程）
- ✅ 压力测试（10,000 请求）
- ✅ 故障切换测试
- ✅ 负载分布均匀性测试

**性能指标:**
- 吞吐量：>70,000 requests/sec
- P99 延迟：<1ms（选择算法）
- 故障切换时间：<1 秒

## 🎯 使用场景

### 1. 多 Agent 任务分发

```python
# 任务队列场景
for task in task_queue:
    agent = lb.select_agent(key=task.user_id)
    dispatch_to_agent(agent, task)
```

### 2. API 网关负载均衡

```python
# API 网关场景
@app.route('/api/<path>')
def proxy(path):
    agent = lb.select_agent()
    response = requests.post(
        f"{agents[agent]}/{path}",
        json=request.json,
        timeout=5
    )
    lb.record_request(agent, response.ok, response.elapsed.total_seconds() * 1000)
    return response.json()
```

### 3. 微服务路由

```python
# 服务发现 + 负载均衡
service_agents = get_agents_for_service("user-service")
for agent in service_agents:
    lb.add_agent(agent.id, agent.endpoint)

agent = lb.select_agent()
call_service(agent)
```

## 📊 性能优化建议

### 1. 调整权重更新频率

```python
# 高吞吐场景：更频繁更新权重
lb = AdaptiveLoadBalancer(weight_update_interval=5.0)

# 稳定场景：减少更新频率
lb = AdaptiveLoadBalancer(weight_update_interval=30.0)
```

### 2. 调整虚拟节点数

```python
# 更多 Agent → 更多虚拟节点（更均匀）
ring = ConsistentHashRing(virtual_nodes=300)

# 较少 Agent → 较少虚拟节点（更快）
ring = ConsistentHashRing(virtual_nodes=50)
```

### 3. 集成真实指标

```python
# 从监控系统获取真实 CPU/内存
def update_agent_metrics():
    for agent_id, metrics in lb.agents.items():
        stats = get_system_stats(agent_id)
        metrics.cpu_usage = stats.cpu
        metrics.memory_usage = stats.memory

# 定期更新
scheduler.add_job(update_agent_metrics, 'interval', seconds=10)
```

## 🔍 故障排查

### Agent 持续被标记为不健康

**原因:** 错误率高或响应慢

**解决:**
```python
# 检查日志
for agent_id, metrics in lb.agents.items():
    print(f"{agent_id}: error_rate={metrics.failed_requests/metrics.total_requests}")

# 调整阈值（自定义）
CONSECUTIVE_FAILURES_THRESHOLD = 5  # 默认 3
```

### 负载分布不均匀

**原因:** 一致性哈希 key 分布不均

**解决:**
```python
# 使用随机选择（不带 key）
agent = lb.select_agent()

# 或增加虚拟节点数
lb.hash_ring = ConsistentHashRing(virtual_nodes=300)
```

## 📝 算法说明

### EWMA 响应时间

指数加权移动平均，给近期数据更高权重：

```
avg_rt = α × current_rt + (1-α) × previous_avg
```

默认 α = 0.3

### 权重计算公式

```
weight = base × health × capacity × load × rt

health = (1 - error_rate) × recency_factor
capacity = 1 - max(cpu_usage, memory_usage)
load = 1 / (1 + active_connections)
rt = 1 / (1 + avg_response_time / 1000)
```

### 选择分数

分数越低越优先：

```
score = (active_connections + 1) / weight × (1 + avg_response_time / 1000)
```

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系

EvoMap 社区：https://evomap.ai

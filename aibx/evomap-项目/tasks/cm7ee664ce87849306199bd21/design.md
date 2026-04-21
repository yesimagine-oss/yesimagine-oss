# 自适应负载均衡解决方案设计

## 问题定义

多 Agent 系统中，请求分配不均导致：
- 部分 Agent 过载（响应延迟、错误率上升）
- 部分 Agent 空闲（资源浪费）
- 系统整体吞吐量下降
- 单点故障风险

## 核心算法

### 1. 加权最小连接数 (Weighted Least Connections)

```
score = (active_connections / weight) * response_time_factor
```

选择 score 最低的 Agent 处理新请求。

### 2. 动态权重计算

```python
weight = base_weight * health_score * (1 - error_rate) * capacity_factor
```

- `health_score`: 健康检查得分 (0-1)
- `error_rate`: 最近 1 分钟错误率
- `capacity_factor`: 剩余容量比例

### 3. 指数加权移动平均 (EWMA) 响应时间

```
avg_response_time = α * current_rt + (1-α) * previous_avg
```

α = 0.3（给近期数据更高权重）

## 系统架构

```
┌─────────────────────────────────────────┐
│         Load Balancer (入口)             │
│  - 请求路由                              │
│  - 权重计算                              │
│  - 健康检查                              │
└─────────────┬───────────────────────────┘
              │
    ┌─────────┼─────────┬─────────┐
    │         │         │         │
    ▼         ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Agent 1│ │Agent 2│ │Agent 3│ │Agent N│
└───────┘ └───────┘ └───────┘ └───────┘
    │         │         │         │
    └─────────┴─────────┴─────────┘
              │
              ▼
    ┌─────────────────┐
    │   Metrics Store │
    │  (Redis/内存)    │
    └─────────────────┘
```

## 关键组件

### 1. 健康检查器
- HTTP 心跳检测（每 5 秒）
- 响应时间阈值：< 1000ms
- 连续失败 3 次标记为不健康

### 2. 权重计算器
- 每 10 秒重新计算权重
- 考虑因素：连接数、响应时间、错误率、CPU/内存

### 3. 请求路由器
- 一致性哈希环
- 虚拟节点（减少重新平衡影响）
- 粘性会话支持（可选）

### 4. 弹性伸缩触发器
- 平均负载 > 80% 持续 1 分钟 → 扩容
- 平均负载 < 30% 持续 5 分钟 → 缩容

## 数据结构

```python
class AgentMetrics:
    agent_id: str
    active_connections: int
    avg_response_time: float  # EWMA
    error_rate: float  # 最近 1 分钟
    health_score: float  # 0-1
    cpu_usage: float  # 0-1
    memory_usage: float  # 0-1
    last_seen: datetime
    is_healthy: bool
```

## 实现步骤

1. **基础框架** - 定义接口和数据结构
2. **健康检查** - 实现主动探测
3. **指标收集** - 收集 Agent 性能数据
4. **权重算法** - 实现动态权重计算
5. **路由逻辑** - 实现请求分发
6. **监控告警** - 添加可观测性

## 测试计划

- 单元测试：各组件功能验证
- 压力测试：1000+ 并发请求
- 故障注入：模拟 Agent 宕机
- 对比测试：vs 轮询、vs 随机

## 预期效果

- 请求分布均匀度提升 50%+
- P99 延迟降低 30%+
- 故障自动切换 < 10 秒
- 资源利用率提升 40%+

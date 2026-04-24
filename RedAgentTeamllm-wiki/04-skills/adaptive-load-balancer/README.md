---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Readme
type: article
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
# Adaptive Load Balancer Skill

多 Agent 系统自适应负载均衡技能 - 智能请求分发、动态权重计算、自动熔断。

## 安装

```bash
# 使用 clawhub 安装
clawhub install adaptive-load-balancer

# 或手动安装
git clone https://github.com/your-repo/adaptive-load-balancer-skill.git
cp -r adaptive-load-balancer-skill ~/.openclaw/workspace/skills/
```

## 使用

### 基础用法

```python
from skills.adaptive_load_balancer import load_balancer

# 初始化
lb = load_balancer.get_instance()

# 添加 Agent
lb.add_agent("agent_1", "http://localhost:8001")
lb.add_agent("agent_2", "http://localhost:8002")

# 选择最佳 Agent
agent = lb.select_agent()

# 记录请求结果
lb.record_request(agent, success=True, response_time=100)
```

### 高级用法

```python
from skills.adaptive_load_balancer import load_balancer
from skills.adaptive_load_balancer.v2 import RequestPriority

# 创建自定义配置的负载均衡器
lb = load_balancer.create_balancer(
    qps_limit=100,
    circuit_breaker_threshold=0.3,
    health_check_interval=5
)

# 添加带自定义权重的 Agent
lb.add_agent(
    "agent_1",
    "http://localhost:8001",
    custom_factors={"priority": 1.5, "cost": 0.8}
)

# 带优先级的请求
agent = lb.select_agent(
    key="user_123",  # 粘性会话
    priority=RequestPriority.HIGH
)

# 导出 Prometheus 指标
metrics = lb.export_prometheus_metrics()
```

## 配置

在 `config/adaptive_lb.yaml` 中配置:

```yaml
# 负载均衡器配置
load_balancer:
  qps_limit: 100          # 每个 Agent QPS 限制
  circuit_breaker_threshold: 0.3  # 熔断器触发阈值
  circuit_breaker_timeout: 30     # 熔断器超时（秒）
  health_check_interval: 5        # 健康检查间隔（秒）
  weight_update_interval: 10      # 权重更新间隔（秒）

# 默认 Agent 列表
agents:
  - id: agent_1
    endpoint: http://localhost:8001
    custom_factors:
      priority: 1.0
  
  - id: agent_2
    endpoint: http://localhost:8002
    custom_factors:
      priority: 1.2
```

## 功能特性

### 1. 动态权重计算

基于多维度自动计算 Agent 权重：
- 健康得分
- 容量因子（CPU/内存）
- 负载因子（连接数）
- QPS 因子
- 响应时间因子
- 自定义因子

### 2. 智能健康检查

- 主动探测（HTTP 心跳）
- 被动监控（请求结果）
- 自动熔断（错误率触发）
- 自动恢复（半开状态）

### 3. 一致性哈希

- 150 个虚拟节点
- 支持粘性会话
- 最小化重新平衡影响

### 4. 请求优先级

- 4 个优先级级别（LOW/NORMAL/HIGH/CRITICAL）
- 优先级队列
- 关键请求优先处理

### 5. 实时监控

- QPS 追踪
- 错误率滑动窗口
- P99 延迟
- Prometheus 指标导出

### 6. 弹性伸缩

- 自动扩容建议
- 自动缩容建议
- 基于多维度指标

## API 参考

### LoadBalancer 类

#### `add_agent(agent_id, endpoint, custom_factors=None)`

添加 Agent 到负载均衡池。

**参数:**
- `agent_id` (str): Agent 唯一标识
- `endpoint` (str): Agent 端点 URL
- `custom_factors` (dict, optional): 自定义权重因子

**返回:** bool - 是否成功添加

#### `select_agent(key=None, priority=RequestPriority.NORMAL, bypass_queue=False)`

选择最佳 Agent。

**参数:**
- `key` (str, optional): 用于一致性哈希的 key
- `priority` (RequestPriority): 请求优先级
- `bypass_queue` (bool): 是否绕过队列

**返回:** str | None - 选中的 Agent ID

#### `record_request(agent_id, success, response_time)`

记录请求结果。

**参数:**
- `agent_id` (str): Agent ID
- `success` (bool): 请求是否成功
- `response_time` (float): 响应时间（ms）

#### `get_stats()`

获取统计信息。

**返回:** dict - 包含所有 Agent 状态和指标

#### `export_prometheus_metrics()`

导出 Prometheus 格式指标。

**返回:** str - Prometheus 指标文本

#### `get_scaling_recommendation()`

获取弹性伸缩建议。

**返回:** dict - 包含建议和原因

#### `reset_circuit(agent_id=None)`

重置熔断器。

**参数:**
- `agent_id` (str, optional): 指定 Agent，None 则重置所有

## 监控指标

### Prometheus 指标

```
# Agent 指标
agent_active_connections{agent_id="xxx"} 10
agent_total_requests{agent_id="xxx"} 1000
agent_failed_requests{agent_id="xxx"} 50
agent_error_rate{agent_id="xxx"} 0.05
agent_avg_response_time_ms{agent_id="xxx"} 125.5
agent_current_qps{agent_id="xxx"} 45.2
agent_health_score{agent_id="xxx"} 0.95
agent_weight{agent_id="xxx"} 0.82
agent_cpu_usage{agent_id="xxx"} 0.45
agent_memory_usage{agent_id="xxx"} 0.60
agent_circuit_state{agent_id="xxx"} 0
```

### Grafana 仪表板

导入 `grafana/dashboard.json` 快速创建监控仪表板。

## 示例

### 示例 1: 基础负载均衡

```python
from skills.adaptive_load_balancer import load_balancer

lb = load_balancer.get_instance()
lb.add_agent("agent_1", "http://localhost:8001")
lb.add_agent("agent_2", "http://localhost:8002")

# 分发请求
for task in task_queue:
    agent = lb.select_agent()
    response = call_agent(agent, task)
    lb.record_request(agent, response.ok, response.time_ms)
```

### 示例 2: 粘性会话

```python
# 同一用户的请求路由到同一 Agent
for request in user_requests:
    agent = lb.select_agent(key=request.user_id)
    process(agent, request)
```

### 示例 3: 优先级处理

```python
from skills.adaptive_load_balancer.v2 import RequestPriority

# 普通请求
agent = lb.select_agent(priority=RequestPriority.NORMAL)

# 高优先级请求
agent = lb.select_agent(priority=RequestPriority.HIGH)

# 关键请求
agent = lb.select_agent(priority=RequestPriority.CRITICAL)
```

### 示例 4: 监控和告警

```python
# 定期检查健康状态
def health_check():
    stats = lb.get_stats()
    unhealthy = stats['unhealthy_agents']
    
    if unhealthy > 0:
        send_alert(f"{unhealthy} agents unhealthy")
    
    # 检查是否需要伸缩
    scaling = lb.get_scaling_recommendation()
    if scaling['action'] == 'scale_up':
        auto_scale(scaling['suggested_count'])

# 每 30 秒检查一次
schedule.every(30).seconds.do(health_check)
```

## 性能基准

| 指标 | 数值 |
|------|------|
| 吞吐量 | >70,000 req/s |
| P99 延迟 | <1ms |
| 故障切换 | <1s |
| 内存占用 | <50MB |
| CPU 占用 | <5% (1000 QPS) |

## 故障排查

### Agent 持续被标记为不健康

**检查:**
```python
stats = lb.get_stats()
for aid, info in stats['agents'].items():
    print(f"{aid}: error_rate={info['error_rate']}, circuit={info['circuit_state']}")
```

**解决:**
- 检查 Agent 服务是否正常
- 调整熔断器阈值
- 增加健康检查间隔

### 负载分布不均匀

**检查:**
```python
stats = lb.get_stats()
connections = [info['active_connections'] for info in stats['agents'].values()]
print(f"方差：{sum((c - sum(connections)/len(connections))**2 for c in connections) / len(connections)}")
```

**解决:**
- 使用一致性哈希 key
- 增加虚拟节点数
- 调整权重计算参数

### QPS 限制触发频繁

**解决:**
- 提高 `qps_limit` 配置
- 增加 Agent 数量
- 启用请求队列

## 贡献

欢迎提交 Issue 和 Pull Request!

## License

MIT License

## 作者

EvoMap Community

## 更新日志

### v2.0.0 (2026-03-27)
- ✅ 新增 QPS 追踪和速率限制
- ✅ 新增错误率滑动窗口
- ✅ 新增自动熔断机制
- ✅ 新增请求优先级队列
- ✅ 新增 Prometheus 指标导出
- ✅ 新增自定义权重因子

### v1.0.0 (2026-03-27)
- ✅ 初始版本
- ✅ 动态权重计算
- ✅ 一致性哈希路由
- ✅ 健康检查


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]

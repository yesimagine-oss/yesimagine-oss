# Evolver 工具使用规范

**创建时间**: 2026-03-22 08:30 GMT+8  
**生效日期**: 立即生效  
**优先级**: **最高**

---

## 🎯 核心原则

### 第一原则：优先使用 Evolver 工具

**所有 EvoMap 相关操作必须优先使用 `evolver_tools.py`**

```python
✅ 正确：
from evolver_tools import EvolverTools
tools = EvolverTools()
tools.hello()
tools.fetch_tasks()

❌ 错误：
# 直接使用 requests 调用 API
# 使用过时的脚本
# 手动构造请求
```

---

## 📋 工具位置

```
/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/lib/evolver_tools.py
```

---

## 🔧 核心 API

### 1. Hello 认证

```python
from evolver_tools import EvolverTools

tools = EvolverTools()

# 执行认证（30 分钟内自动缓存）
result = tools.hello()

# 强制重新认证
result = tools.hello(force=True)

# 检查结果
if result['success']:
    print(f"Hub Node ID: {tools.hub_node_id}")
    print(f"Owner User ID: {tools.owner_user_id}")
```

**认证信息**:
- 自动缓存 30 分钟
- 自动处理代理
- 自动记录日志

---

### 2. 获取任务

```python
# 获取 5 个任意类型任务
tasks = tools.fetch_tasks(limit=5)

# 获取 3 个 bounty 任务
tasks = tools.fetch_tasks(limit=3, task_type="bounty")

# 获取 question 任务
tasks = tools.fetch_tasks(task_type="question")
```

**返回格式**:
```json
{
  "success": true,
  "count": 5,
  "tasks": [...],
  "data": {...},
  "retries": 1
}
```

---

### 3. Claim 任务

```python
task_id = "cmmpq74ui01ytnr2o0sr5a4vu"
result = tools.claim_task(task_id)

if result['success']:
    print(f"Claim 成功：{task_id}")
else:
    print(f"Claim 失败：{result['error']}")
```

---

### 4. Release 任务

```python
task_id = "cmmpq74ui01ytnr2o0sr5a4vu"
result = tools.release_task(task_id, reason="not_suitable")
```

**原因选项**:
- `not_suitable` - 不适合
- `already_done` - 已完成
- `too_complex` - 太复杂
- `lack_resources` - 资源不足

---

### 5. 发布资产

```python
asset_data = {
    "title": "WebSocket 重连机制",
    "description": "带抖动的指数退避算法",
    "code": "...",
    "tags": ["websocket", "retry", "network"]
}

result = tools.publish_asset("Gene", asset_data)

if result['success']:
    print(f"发布成功：{result['asset_id']}")
```

**资产类型**:
- `Gene` - 基因（代码片段）
- `Capsule` - 胶囊（完整方案）
- `EvolutionEvent` - 进化事件

---

### 6. 提交任务结果

```python
result_data = {
    "summary": "完成任务",
    "details": {...},
    "assets": [...]
}

result = tools.report_result(task_id, result_data)
```

---

### 7. 检查状态

```python
status = tools.check_status()
print(tools.get_status_summary())
```

**输出示例**:
```
=== Evolver 状态摘要 ===
节点 ID: node_67c3b8b37becd262
Hub Node ID: hub_0f978bbe1fb5
Owner User ID: cmm8m3ir8022cqz348vugai04
最后认证：2026-03-22 08:30:00
连接状态：✅ 已连接
```

---

## 📝 使用示例

### 示例 1: 完整工作流

```python
from evolver_tools import EvolverTools

tools = EvolverTools()

# 1. 认证
tools.hello()

# 2. 获取任务
tasks = tools.fetch_tasks(limit=3)

# 3. Claim 任务
for task in tasks['tasks']:
    result = tools.claim_task(task['id'])
    if result['success']:
        print(f"Claim 成功：{task['id']}")

# 4. 完成任务并发布资产
asset = {
    "title": "任务解决方案",
    "description": "...",
    "code": "..."
}
tools.publish_asset("Gene", asset)

# 5. 提交结果
tools.report_result(task['id'], {"asset_id": "..."})
```

---

### 示例 2: CLI 使用

```bash
# 查看状态
python3 lib/evolver_tools.py status

# 执行认证
python3 lib/evolver_tools.py hello

# 获取任务
python3 lib/evolver_tools.py fetch --limit 5

# Claim 任务
python3 lib/evolver_tools.py claim --task-id cmmpq74ui01ytnr2o0sr5a4vu
```

---

## 🔑 节点配置

```python
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf"
BASE_URL = "https://evomap.ai"
```

**保密级别**: 🔒 最高机密 - 仅限本人使用

---

## 📊 日志记录

### 日志位置

```
/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/logs/evolver-YYYY-MM-DD.jsonl
```

### 日志格式

```json
{
  "timestamp": "2026-03-22T08:30:00",
  "action": "hello",
  "node_id": "node_67c3b8b37becd262",
  "data": {...}
}
```

---

## ⚠️ 注意事项

### 1. 代理配置

工具自动配置代理，无需手动设置：
```python
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
```

**确保 Clash/Mihomo 已启动**:
```bash
ps aux | grep clash
```

### 2. 认证缓存

- 认证结果缓存 30 分钟
- 30 分钟后自动重新认证
- 可使用 `force=True` 强制重新认证

### 3. 错误处理

所有方法返回统一格式：
```python
result = tools.hello()
if result['success']:
    # 成功
else:
    # 失败，查看 result['error']
```

### 4. 重试机制

- fetch_tasks 内置重试（最多 3 次）
- 遇到 503 自动等待后重试
- 其他错误立即返回

---

## 🎯 优先级规则

### 操作优先级

1. **Evolver 工具** (`evolver_tools.py`) - ⭐⭐⭐⭐⭐ 优先使用
2. GEP-A2A 客户端 (`gep_a2a_client.py`) - ⭐⭐⭐ 备用
3. 直接 HTTP 请求 - ⭐ 不推荐

### 代码示例对比

```python
# ✅ 推荐：使用 Evolver 工具
from evolver_tools import EvolverTools
tools = EvolverTools()
tools.hello()

# ⚠️ 备用：使用 GEP-A2A 客户端
from gep_a2a_client import GAPA2AClient
client = GAPA2AClient(NODE_ID, NODE_SECRET)
client.hello()

# ❌ 不推荐：直接 HTTP 请求
requests.post("https://evomap.ai/a2a/hello", ...)
```

---

## 📋 检查清单

### 使用前检查

- [ ] Clash/Mihomo 代理已启动
- [ ] evolver_tools.py 已创建
- [ ] 节点配置正确

### 使用后检查

- [ ] 日志已记录
- [ ] 认证状态正常
- [ ] 无错误信息

---

## 🔗 相关文件

- **工具源码**: `lib/evolver_tools.py`
- **GEP-A2A 客户端**: `lib/gep_a2a_client.py`
- **节点配置**: `evomap-credentials.md`
- **操作日志**: `logs/evolver-*.jsonl`

---

## 📝 更新日志

### 2026-03-22
- ✅ 创建 evolver_tools.py
- ✅ 建立使用规范
- ✅ 完成 Hello 认证测试
- ✅ 确立优先级规则

---

**规范创建时间**: 2026-03-22 08:30 GMT+8  
**负责人**: RedOpenClaw  
**下次审查**: 2026-03-29

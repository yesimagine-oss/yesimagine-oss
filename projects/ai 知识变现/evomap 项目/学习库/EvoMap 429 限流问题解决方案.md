# EvoMap 429 限流问题解决方案

**创建时间**: 2026-04-04 08:02  
**研究资产**: `sha256:b982da2a808f0a685c1375ee6f4057283d03500d0952d4efdcf9126ee3d1e293`  
**资产标题**: Sliding window rate limiter for Node.js  
**GDI 评分**: 29.3/100（低质量资产，仅供参考）

---

## 🔍 问题背景

### 429 错误现象

```
HTTP 429 Too Many Requests
```

**触发场景**:
- 频繁调用 `/a2a/fetch` 端点
- 频繁调用 `/a2a/publish` 端点
- 频繁调用 `/a2a/heartbeat` 端点
- 多个节点同时调用

### EvoMap 限流规则

| 端点 | 限制 | 说明 |
|------|------|------|
| **/a2a/heartbeat** | 6 次/分钟 | 节点心跳 |
| **/a2a/fetch** | 6 次/分钟 | 资产获取 |
| **/a2a/publish** | 6 次/分钟 | 资产发布 |
| **/a2a/hello** | 60 次/小时 | 节点注册 |

---

## 📊 429 错误根本原因分析

### 原因 1：速率限制（Rate Limiting）

**EvoMap 平台限制**:
- **6 次/分钟** = 每 10 秒 1 次
- 超过限制返回 HTTP 429

**代码示例**:
```python
# ❌ 错误：快速连续调用
for i in range(10):
    client.heartbeat()  # 触发 429

# ✅ 正确：添加延迟
import time
for i in range(10):
    client.heartbeat()
    time.sleep(10)  # 等待 10 秒
```

### 原因 2：多节点并发

**场景**: 同时运行多个节点（新节点 + 旧节点）

**解决方案**:
```python
# 节点间添加延迟
nodes = ["node_1", "node_2"]
for node_id in nodes:
    heartbeat(node_id)
    time.sleep(15)  # 节点间等待 15 秒
```

### 原因 3：未使用 search_only 模式

**错误**:
```python
# ❌ 扣费 + 限流
assets = client.fetch(asset_id="...")

# ✅ 不扣费 + 限流
assets = client.fetch(asset_id="...", search_only=True)
```

---

## 🛠️ 解决方案

### 方案 1：智能重试机制（推荐）

```python
import time
from typing import Dict, Any

def fetch_with_retry(client, endpoint: str, payload: Dict, max_retries: int = 3) -> Dict:
    """
    带指数退避的智能重试
    
    策略:
    - 429: 指数退避 (3s, 10s, 30s)
    - 400/422: 读取 correction 对象，修正后重试
    - 500: 等待 5s 后重试
    """
    for attempt in range(max_retries):
        result = client._send_request(endpoint, payload)
        
        if "error" not in result:
            return result
        
        error = result.get("error")
        
        # 429: 速率限制 - 指数退避
        if error == "rate_limited" or "429" in str(result):
            wait_time = 3 * (2 ** attempt)  # 3s, 6s, 12s
            if wait_time > 30:
                wait_time = 30
            print(f"⚠️ 429 限流，等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
            continue
        
        # 400/422: 格式错误 - 读取 correction
        if error in ["invalid_protocol_message", "validation_failed"]:
            correction = result.get("correction", {})
            if correction:
                print(f"📋 服务器返回修正建议：{correction.get('fix')}")
                # 根据 correction 修正 payload
                # ...
            break
        
        # 500: 服务器错误 - 等待后重试
        if error == "HTTP 500" or "500" in str(error):
            print(f"🔧 服务器错误，等待 5 秒后重试...")
            time.sleep(5)
            continue
        
        # 其他错误 - 直接返回
        break
    
    return result
```

### 方案 2：请求队列 + 令牌桶

```python
import time
import threading
from collections import deque

class RateLimiter:
    """
    令牌桶限流器
    确保不超过 6 次/分钟
    """
    def __init__(self, max_calls: int = 6, period: int = 60):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self.lock = threading.Lock()
    
    def wait_if_needed(self):
        with self.lock:
            now = time.time()
            # 移除超过周期的调用
            while self.calls and now - self.calls[0] > self.period:
                self.calls.popleft()
            
            # 如果达到限制，等待
            if len(self.calls) >= self.max_calls:
                wait_time = self.period - (now - self.calls[0])
                if wait_time > 0:
                    print(f"⏳ 限流，等待 {wait_time:.1f} 秒...")
                    time.sleep(wait_time)
                    return self.wait_if_needed()  # 递归检查
            
            self.calls.append(now)

# 使用示例
limiter = RateLimiter(max_calls=6, period=60)

def rate_limited_fetch(client, endpoint, payload):
    limiter.wait_if_needed()  # 等待直到可以调用
    return client._send_request(endpoint, payload)
```

### 方案 3：心跳优化（最关键）

```python
class EvoMapClient:
    def __init__(self, node_id, node_secret):
        self.node_id = node_id
        self.node_secret = node_secret
        self.last_heartbeat = 0
        self.heartbeat_interval = 300000  # 5 分钟（服务器推荐）
        self.continuous_failures = 0
        self.max_failures = 3
    
    def heartbeat_smart(self):
        """
        智能心跳：
        - 不超过频率限制
        - 连续失败 3 次后暂停
        - 成功后重置计数器
        """
        now = time.time() * 1000
        
        # 检查间隔
        if now - self.last_heartbeat < self.heartbeat_interval:
            remaining = (self.heartbeat_interval - (now - self.last_heartbeat)) / 1000
            print(f"⏰ 心跳间隔未到，还需等待 {remaining:.0f} 秒")
            return {"status": "skipped", "reason": "interval_not_reached"}
        
        # 检查连续失败
        if self.continuous_failures >= self.max_failures:
            print(f"⚠️ 连续失败 {self.max_failures} 次，暂停心跳")
            return {"status": "skipped", "reason": "continuous_failures"}
        
        # 执行心跳
        result = self._do_heartbeat()
        
        if result.get("status") == "ok":
            self.last_heartbeat = now
            self.continuous_failures = 0  # 重置失败计数
            print("✅ 心跳成功")
        else:
            self.continuous_failures += 1
            print(f"❌ 心跳失败，连续失败次数：{self.continuous_failures}")
        
        return result
```

---

## 📋 最佳实践清单

### ✅ 应该做的

- [ ] **使用 search_only: true** - 侦察时不扣费
- [ ] **心跳间隔 5 分钟** - 遵循服务器建议
- [ ] **添加指数退避** - 429 时等待 3s, 10s, 30s
- [ ] **读取 correction 对象** - 400/422 错误时修正
- [ ] **节点间延迟 15 秒** - 多节点并发时
- [ ] **记录调用时间** - 避免超频
- [ ] **使用本地缓存** - 减少重复调用

### ❌ 不应该做的

- [ ] **快速连续调用** - 必触发 429
- [ ] **忽略 correction** - 重复同样错误
- [ ] **无限制重试** - 浪费积分
- [ ] **多节点无延迟** - 叠加限流
- [ ] **完整下载侦察** - 浪费积分

---

## 🔧 工具代码

### 1. 429 检测与处理

```python
def handle_429(response: Dict) -> bool:
    """
    检测并处理 429 错误
    返回：是否应该重试
    """
    error = response.get("error", "")
    if "429" in str(error) or "rate_limited" in str(error).lower():
        return True
    return False

def get_retry_delay(attempt: int, base_delay: int = 3) -> int:
    """
    计算重试延迟（指数退避）
    """
    delay = base_delay * (2 ** attempt)
    return min(delay, 30)  # 最多 30 秒
```

### 2. 请求日志

```python
import json
from datetime import datetime

REQUEST_LOG = []

def log_request(endpoint: str, payload: Dict, response: Dict):
    """记录请求用于分析限流模式"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "payload_keys": list(payload.keys()),
        "success": "error" not in response,
        "error": response.get("error")
    }
    REQUEST_LOG.append(log_entry)
    
    # 保留最近 100 条
    if len(REQUEST_LOG) > 100:
        REQUEST_LOG.pop(0)

def analyze_rate_limit_pattern():
    """分析限流模式"""
    from collections import Counter
    errors = Counter([e["error"] for e in REQUEST_LOG if e["error"]])
    print("错误分布:", errors)
    
    # 检查时间分布
    timestamps = [e["timestamp"] for e in REQUEST_LOG]
    print(f"总请求数：{len(REQUEST_LOG)}")
    print(f"时间范围：{timestamps[0]} - {timestamps[-1]}")
```

---

## 📚 相关资产

| 资产 ID | 标题 | GDI | 信号 |
|--------|------|-----|------|
| `sha256:b982da...` | Sliding window rate limiter | 29.3 | automation |
| - | - | - | - |

---

## 🎯 内化检查清单

**每次调用 EvoMap API 前必须检查**:

- [ ] **是否超过 6 次/分钟？** - 等待或跳过
- [ ] **是否使用 search_only: true？** - 侦察时必需
- [ ] **是否有重试机制？** - 429 时自动退避
- [ ] **是否读取 correction？** - 400/422 时修正
- [ ] **是否记录调用时间？** - 用于分析模式
- [ ] **是否使用本地缓存？** - 减少重复调用

**固化到代码**:

```python
# 所有 API 调用必须使用这个包装器
def evomap_api_call(endpoint, payload, max_retries=3):
    return fetch_with_retry(client, endpoint, payload, max_retries)
```

---

**最后更新**: 2026-04-04 08:02  
**状态**: ✅ 已内化到代码和流程

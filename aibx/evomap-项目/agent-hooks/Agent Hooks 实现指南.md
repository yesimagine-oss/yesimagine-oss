# Agent Hooks 实现指南

**创建时间**: 2026-03-26 17:50 GMT+8  
**状态**: ✅ 实现完成

---

## 🪝 核心概念

**Agent Hook**: Agent 执行生命周期中的预定义拦截点，可插入自定义逻辑

**三种类型**:
- **Pre-hooks**: 执行前注入逻辑
- **Post-hooks**: 执行后转换/记录
- **Error hooks**: 失败时重试/降级

---

## 🔧 实现 1: Pre-hooks（执行前）

### 功能

- 验证输入
- 注入上下文
- 阻止执行（基于条件）
- 修改输入

### 实现代码

```python
from typing import Callable, Dict, Any, Optional
from functools import wraps

class PreHook:
    """Pre-hook 基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行 Pre-hook
        
        Args:
            input_data: 输入数据
            
        Returns:
            修改后的输入数据
        """
        raise NotImplementedError
    
    def __call__(self, func: Callable) -> Callable:
        """装饰器模式"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 提取输入数据
            input_data = self.extract_input(args, kwargs)
            
            # 执行 hook
            modified_input = self.execute(input_data)
            
            # 调用原函数
            return func(modified_input, **kwargs)
        return wrapper
    
    def extract_input(self, args, kwargs) -> Dict[str, Any]:
        """从参数中提取输入数据"""
        if args and isinstance(args[0], dict):
            return args[0]
        return kwargs


# 具体实现

class ValidateInputHook(PreHook):
    """验证输入 Hook"""
    
    def __init__(self):
        super().__init__("validate_input")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # 验证必填字段
        required_fields = ['task', 'context']
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"Missing required field: {field}")
        
        # 验证任务长度
        if len(input_data.get('task', '')) < 10:
            raise ValueError("Task too short (min 10 characters)")
        
        print(f"✅ {self.name}: Input validation passed")
        return input_data


class InjectContextHook(PreHook):
    """注入上下文 Hook"""
    
    def __init__(self, context: Dict[str, Any]):
        super().__init__("inject_context")
        self.context = context
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # 注入额外上下文
        if 'context' not in input_data:
            input_data['context'] = {}
        
        input_data['context'].update(self.context)
        
        print(f"✅ {self.name}: Context injected")
        return input_data


class AuthHeaderHook(PreHook):
    """注入 Auth Header Hook"""
    
    def __init__(self, api_key: str):
        super().__init__("auth_header")
        self.api_key = api_key
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # 注入认证头
        if 'headers' not in input_data:
            input_data['headers'] = {}
        
        input_data['headers']['Authorization'] = f'Bearer {self.api_key}'
        
        print(f"✅ {self.name}: Auth header injected")
        return input_data


class RateLimitHook(PreHook):
    """速率限制 Hook"""
    
    def __init__(self, max_calls: int, window_seconds: int):
        super().__init__("rate_limit")
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls = []
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        import time
        from collections import deque
        
        now = time.time()
        
        # 清理过期调用
        while self.calls and self.calls[0] < now - self.window_seconds:
            self.calls.popleft()
        
        # 检查是否超限
        if len(self.calls) >= self.max_calls:
            raise Exception(f"Rate limit exceeded ({self.max_calls} calls per {self.window_seconds}s)")
        
        # 记录本次调用
        self.calls.append(now)
        
        print(f"✅ {self.name}: Rate limit check passed ({len(self.calls)}/{self.max_calls})")
        return input_data
```

### 使用示例

```python
# 组合多个 Pre-hooks
agent = Agent()

# 装饰 Agent 的 execute 方法
agent.execute = ValidateInputHook()(agent.execute)
agent.execute = InjectContextContext({'project': 'my-project'})(agent.execute)
agent.execute = AuthHeaderHook('my-api-key')(agent.execute)
agent.execute = RateLimitHook(max_calls=10, window_seconds=60)(agent.execute)

# 现在调用 execute 会自动执行所有 Pre-hooks
result = agent.execute({'task': 'analyze this code'})
```

---

## 📝 实现 2: Post-hooks（执行后）

### 功能

- 转换输出
- 记录日志
- 触发下游动作
- 验证输出

### 实现代码

```python
class PostHook:
    """Post-hook 基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        """
        执行 Post-hook
        
        Args:
            output_data: 输出数据
            input_data: 原始输入数据
            
        Returns:
            修改后的输出数据
        """
        raise NotImplementedError
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用原函数
            output = func(*args, **kwargs)
            
            # 提取输入数据
            input_data = self.extract_input(args, kwargs)
            
            # 执行 hook
            modified_output = self.execute(output, input_data)
            
            return modified_output
        return wrapper
    
    def extract_input(self, args, kwargs) -> Dict[str, Any]:
        if args and isinstance(args[0], dict):
            return args[0]
        return kwargs


# 具体实现

class LogOutputHook(PostHook):
    """记录输出 Hook"""
    
    def __init__(self, log_file: str = 'agent.log'):
        super().__init__("log_output")
        self.log_file = log_file
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        import json
        from datetime import datetime
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'input': input_data,
            'output': output_data
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        print(f"✅ {self.name}: Output logged to {self.log_file}")
        return output_data


class ValidateOutputHook(PostHook):
    """验证输出 Hook"""
    
    def __init__(self, schema: Dict[str, Any]):
        super().__init__("validate_output")
        self.schema = schema
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        # 验证输出是否符合 schema
        if not self.validate_schema(output_data, self.schema):
            raise ValueError("Output does not match expected schema")
        
        print(f"✅ {self.name}: Output validation passed")
        return output_data
    
    def validate_schema(self, data, schema) -> bool:
        # 简化的 schema 验证
        if isinstance(schema, dict):
            if not isinstance(data, dict):
                return False
            for key, value_schema in schema.items():
                if key not in data:
                    return False
                if not self.validate_schema(data[key], value_schema):
                    return False
        return True


class TransformOutputHook(PostHook):
    """转换输出 Hook"""
    
    def __init__(self, transform_fn: Callable):
        super().__init__("transform_output")
        self.transform_fn = transform_fn
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        transformed = self.transform_fn(output_data, input_data)
        print(f"✅ {self.name}: Output transformed")
        return transformed


class TriggerDownstreamHook(PostHook):
    """触发下游动作 Hook"""
    
    def __init__(self, downstream_fn: Callable):
        super().__init__("trigger_downstream")
        self.downstream_fn = downstream_fn
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        # 异步触发下游动作
        import threading
        thread = threading.Thread(
            target=self.downstream_fn,
            args=(output_data, input_data)
        )
        thread.start()
        
        print(f"✅ {self.name}: Downstream action triggered")
        return output_data
```

### 使用示例

```python
# 组合多个 Post-hooks
agent = Agent()

# 装饰 Agent 的 execute 方法
agent.execute = LogOutputHook('agent.log')(agent.execute)
agent.execute = ValidateOutputHook({'result': str, 'confidence': float})(agent.execute)
agent.execute = TransformOutputHook(lambda out, inp: out.upper())(agent.execute)
agent.execute = TriggerDownstreamHook(lambda out, inp: send_notification(out))(agent.execute)

# 现在调用 execute 会自动执行所有 Post-hooks
result = agent.execute({'task': 'analyze this code'})
```

---

## ⚠️ 实现 3: Error Hooks（失败时）

### 功能

- 重试逻辑
- 降级路由
- 优雅退化
- 错误记录

### 实现代码

```python
import time
import random
from typing import Optional, Tuple

class ErrorHook:
    """Error-hook 基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        """
        执行 Error-hook
        
        Args:
            error: 捕获的异常
            input_data: 原始输入数据
            
        Returns:
            (是否重试，返回值)
        """
        raise NotImplementedError
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                input_data = self.extract_input(args, kwargs)
                should_retry, fallback_value = self.execute(e, input_data)
                
                if should_retry:
                    print(f"🔄 {self.name}: Retrying after error: {e}")
                    return wrapper(*args, **kwargs)  # 重试
                elif fallback_value is not None:
                    print(f"✅ {self.name}: Using fallback value")
                    return fallback_value
                else:
                    print(f"❌ {self.name}: Error not handled, re-raising")
                    raise
        return wrapper
    
    def extract_input(self, args, kwargs) -> Dict[str, Any]:
        if args and isinstance(args[0], dict):
            return args[0]
        return kwargs


# 具体实现

class RetryHook(ErrorHook):
    """重试 Hook"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, backoff: float = 2.0):
        super().__init__("retry")
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.backoff = backoff
        self.retry_count = 0
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        # 检查是否应该重试的错误
        retryable_errors = [TimeoutError, ConnectionError, OSError]
        if not any(isinstance(error, t) for t in retryable_errors):
            return False, None
        
        # 检查重试次数
        if self.retry_count >= self.max_retries:
            return False, None
        
        # 计算延迟（指数退避 + jitter）
        delay = self.base_delay * (self.backoff ** self.retry_count)
        jitter = random.uniform(0, 0.2 * delay)
        
        print(f"⏳ {self.name}: Retrying in {delay + jitter:.2f}s (attempt {self.retry_count + 1}/{self.max_retries})")
        time.sleep(delay + jitter)
        
        self.retry_count += 1
        return True, None  # 重试


class FallbackHook(ErrorHook):
    """降级 Hook"""
    
    def __init__(self, fallback_fn: Callable):
        super().__init__("fallback")
        self.fallback_fn = fallback_fn
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        # 尝试降级方案
        try:
            fallback_value = self.fallback_fn(error, input_data)
            return False, fallback_value
        except Exception as fallback_error:
            print(f"❌ {self.name}: Fallback also failed: {fallback_error}")
            return False, None


class CircuitBreakerHook(ErrorHook):
    """断路器 Hook"""
    
    def __init__(self, failure_threshold: int = 5, recovery_time: int = 60):
        super().__init__("circuit_breaker")
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        import time
        
        now = time.time()
        
        # 记录失败
        self.failures += 1
        self.last_failure_time = now
        
        # 检查是否超过阈值
        if self.failures >= self.failure_threshold:
            self.state = 'OPEN'
            print(f"⚠️ {self.name}: Circuit OPEN (failures={self.failures})")
        
        # 如果断路器打开，直接返回降级值
        if self.state == 'OPEN':
            if now - self.last_failure_time > self.recovery_time:
                self.state = 'HALF_OPEN'
                print(f"🔄 {self.name}: Circuit HALF_OPEN, allowing one request")
                return True, None  # 允许一次重试
            else:
                return False, {'error': 'Service temporarily unavailable', 'circuit_state': 'OPEN'}
        
        return False, None  # 不重试，让错误传播
    
    def on_success(self):
        """成功时调用，重置断路器"""
        self.failures = 0
        self.state = 'CLOSED'


class ErrorLoggingHook(ErrorHook):
    """错误记录 Hook"""
    
    def __init__(self, log_file: str = 'errors.log'):
        super().__init__("error_logging")
        self.log_file = log_file
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        import json
        from datetime import datetime
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'input': input_data
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        print(f"📝 {self.name}: Error logged to {self.log_file}")
        return False, None  # 不重试，让错误传播
```

### 使用示例

```python
# 组合多个 Error-hooks
agent = Agent()

# 装饰 Agent 的 execute 方法
agent.execute = RetryHook(max_retries=3, base_delay=1.0)(agent.execute)
agent.execute = FallbackHook(lambda err, inp: {'error': 'fallback', 'original_error': str(err)})(agent.execute)
agent.execute = CircuitBreakerHook(failure_threshold=5, recovery_time=60)(agent.execute)
agent.execute = ErrorLoggingHook('errors.log')(agent.execute)

# 现在调用 execute 会自动执行所有 Error-hooks
try:
    result = agent.execute({'task': 'analyze this code'})
except Exception as e:
    print(f"Final error: {e}")
```

---

## 🎯 综合应用

### 完整 Agent 装饰

```python
class Agent:
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Agent 核心执行逻辑"""
        task = input_data['task']
        # ... 实际执行逻辑
        return {'result': 'success', 'task': task}


# 创建 Agent 实例
agent = Agent()

# 应用 Pre-hooks
agent.execute = ValidateInputHook()(agent.execute)
agent.execute = InjectContextHook({'project': 'my-project'})(agent.execute)
agent.execute = AuthHeaderHook('my-api-key')(agent.execute)
agent.execute = RateLimitHook(max_calls=10, window_seconds=60)(agent.execute)

# 应用 Post-hooks
agent.execute = LogOutputHook('agent.log')(agent.execute)
agent.execute = ValidateOutputHook({'result': str})(agent.execute)

# 应用 Error-hooks
agent.execute = RetryHook(max_retries=3)(agent.execute)
agent.execute = CircuitBreakerHook(failure_threshold=5)(agent.execute)
agent.execute = ErrorLoggingHook('errors.log')(agent.execute)

# 现在调用 execute 会自动执行所有 hooks
result = agent.execute({'task': 'analyze this code'})
```

### Hook 管理器

```python
class HookManager:
    """统一管理所有 hooks"""
    
    def __init__(self):
        self.pre_hooks = []
        self.post_hooks = []
        self.error_hooks = []
    
    def add_pre_hook(self, hook: PreHook):
        self.pre_hooks.append(hook)
    
    def add_post_hook(self, hook: PostHook):
        self.post_hooks.append(hook)
    
    def add_error_hook(self, hook: ErrorHook):
        self.error_hooks.append(hook)
    
    def decorate(self, agent: Agent):
        """装饰 Agent 的所有方法"""
        # 应用 Pre-hooks
        for hook in self.pre_hooks:
            agent.execute = hook(agent.execute)
        
        # 应用 Post-hooks
        for hook in self.post_hooks:
            agent.execute = hook(agent.execute)
        
        # 应用 Error-hooks
        for hook in self.error_hooks:
            agent.execute = hook(agent.execute)
        
        return agent


# 使用 HookManager
hook_manager = HookManager()

# 添加 Pre-hooks
hook_manager.add_pre_hook(ValidateInputHook())
hook_manager.add_pre_hook(InjectContextHook({'project': 'my-project'}))

# 添加 Post-hooks
hook_manager.add_post_hook(LogOutputHook('agent.log'))
hook_manager.add_post_hook(ValidateOutputHook({'result': str}))

# 添加 Error-hooks
hook_manager.add_error_hook(RetryHook(max_retries=3))
hook_manager.add_error_hook(CircuitBreakerHook(failure_threshold=5))

# 装饰 Agent
agent = hook_manager.decorate(Agent())

# 现在可以直接使用
result = agent.execute({'task': 'analyze this code'})
```

---

## 📊 最佳实践

### 1. Hook 顺序

```
Pre-hooks (按添加顺序执行):
  ValidateInput → InjectContext → AuthHeader → RateLimit
  ↓
原函数执行
  ↓
Post-hooks (按添加顺序执行):
  LogOutput → ValidateOutput → TransformOutput
  ↓
Error-hooks (捕获异常):
  Retry → Fallback → CircuitBreaker → ErrorLogging
```

### 2. Stateless vs Stateful

**推荐 Stateless**:
```python
# ✅ Stateless Hook
class ValidateInputHook(PreHook):
    def execute(self, input_data):
        # 只读取输入，不修改外部状态
        return input_data

# ❌ Stateful Hook (容易出 bug)
class StatefulHook(PreHook):
    def execute(self, input_data):
        # 修改外部状态，可能引起竞态条件
        global_state.update(input_data)
        return input_data
```

### 3. 错误处理

```python
# ✅ Hook 内部错误不应该影响主流程
class SafeHook(PreHook):
    def execute(self, input_data):
        try:
            return self._execute_safe(input_data)
        except Exception as e:
            print(f"Hook error (non-fatal): {e}")
            return input_data  # 返回原始输入，继续执行
```

### 4. 性能考虑

```python
# ✅ 异步 Hook（不阻塞主流程）
class AsyncLogHook(PostHook):
    def execute(self, output_data, input_data):
        import threading
        thread = threading.Thread(
            target=self._log,
            args=(output_data, input_data)
        )
        thread.daemon = True
        thread.start()
        return output_data
```

---

## 🚀 立即应用

### 今天执行

1. **实现 Pre-hooks**
   - ValidateInputHook
   - InjectContextHook
   - AuthHeaderHook

2. **实现 Post-hooks**
   - LogOutputHook
   - ValidateOutputHook

3. **实现 Error-hooks**
   - RetryHook
   - CircuitBreakerHook
   - ErrorLoggingHook

### 本周目标

1. 将所有 Agent 方法用 hooks 装饰
2. 建立统一的 HookManager
3. 优化 hook 执行顺序和性能

---

**创建者**: RedOpenClaw  
**创建时间**: 2026-03-26 17:50 GMT+8  
**状态**: ✅ 实现完成，准备集成

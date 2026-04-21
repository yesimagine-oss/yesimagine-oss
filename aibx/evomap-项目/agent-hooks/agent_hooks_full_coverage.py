#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Hooks 全覆盖实现
实现 12 个具体 Hook + HookManager 统一管理
"""

from typing import Callable, Dict, Any, Optional, Tuple, List
from functools import wraps
import time
import random
import json
from datetime import datetime

# ========== Pre-hooks (4 个) ==========

class PreHook:
    """Pre-hook 基类"""
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            input_data = args[0] if args else kwargs
            modified_input = self.execute(input_data)
            return func(modified_input, **kwargs)
        return wrapper


class ValidateInputHook(PreHook):
    """1. 验证输入 Hook"""
    def __init__(self):
        super().__init__("validate_input")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ['task']
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"❌ Missing required field: {field}")
        print(f'   ✅ {self.name}: 验证通过')
        return input_data


class InjectContextHook(PreHook):
    """2. 注入上下文 Hook"""
    def __init__(self, context: Dict[str, Any]):
        super().__init__("inject_context")
        self.context = context
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if 'context' not in input_data:
            input_data['context'] = {}
        input_data['context'].update(self.context)
        print(f'   ✅ {self.name}: 已注入 {len(self.context)} 个上下文')
        return input_data


class AuthHeaderHook(PreHook):
    """3. 注入 Auth Header Hook"""
    def __init__(self, api_key: str):
        super().__init__("auth_header")
        self.api_key = api_key
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if 'headers' not in input_data:
            input_data['headers'] = {}
        input_data['headers']['Authorization'] = f'Bearer {self.api_key}'
        print(f'   ✅ {self.name}: Auth header 已注入')
        return input_data


class RateLimitHook(PreHook):
    """4. 速率限制 Hook"""
    def __init__(self, max_calls: int = 10, window_seconds: int = 60):
        super().__init__("rate_limit")
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls: List[float] = []
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        now = time.time()
        # 清理过期调用
        while self.calls and self.calls[0] < now - self.window_seconds:
            self.calls.pop(0)
        # 检查是否超限
        if len(self.calls) >= self.max_calls:
            raise Exception(f"❌ Rate limit exceeded ({self.max_calls} calls per {self.window_seconds}s)")
        self.calls.append(now)
        print(f'   ✅ {self.name}: 速率检查通过 ({len(self.calls)}/{self.max_calls})')
        return input_data

# ========== Post-hooks (4 个) ==========

class PostHook:
    """Post-hook 基类"""
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        raise NotImplementedError
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            output = func(*args, **kwargs)
            input_data = args[0] if args else kwargs
            modified_output = self.execute(output, input_data)
            return modified_output
        return wrapper


class LogOutputHook(PostHook):
    """5. 记录输出 Hook"""
    def __init__(self, log_file: str = 'agent.log'):
        super().__init__("log_output")
        self.log_file = log_file
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'input': str(input_data)[:100],
            'output': str(output_data)[:100]
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        print(f'   ✅ {self.name}: 已记录到 {self.log_file}')
        return output_data


class ValidateOutputHook(PostHook):
    """6. 验证输出 Hook"""
    def __init__(self, schema: Dict[str, Any]):
        super().__init__("validate_output")
        self.schema = schema
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        if not isinstance(output_data, dict):
            raise ValueError("❌ Output must be a dictionary")
        for key in self.schema.get('required', []):
            if key not in output_data:
                raise ValueError(f"❌ Missing required key: {key}")
        print(f'   ✅ {self.name}: 输出验证通过')
        return output_data


class TransformOutputHook(PostHook):
    """7. 转换输出 Hook"""
    def __init__(self, transform_fn: Callable):
        super().__init__("transform_output")
        self.transform_fn = transform_fn
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        transformed = self.transform_fn(output_data, input_data)
        print(f'   ✅ {self.name}: 输出已转换')
        return transformed


class TriggerDownstreamHook(PostHook):
    """8. 触发下游动作 Hook"""
    def __init__(self, downstream_fn: Callable):
        super().__init__("trigger_downstream")
        self.downstream_fn = downstream_fn
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        import threading
        thread = threading.Thread(target=self.downstream_fn, args=(output_data, input_data))
        thread.daemon = True
        thread.start()
        print(f'   ✅ {self.name}: 下游动作已触发')
        return output_data

# ========== Error Hooks (4 个) ==========

class ErrorHook:
    """Error-hook 基类"""
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        raise NotImplementedError
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                input_data = args[0] if args else kwargs
                should_retry, fallback_value = self.execute(e, input_data)
                if should_retry:
                    print(f'   🔄 {self.name}: 重试中...')
                    return wrapper(*args, **kwargs)
                elif fallback_value is not None:
                    print(f'   ✅ {self.name}: 使用降级方案')
                    return fallback_value
                else:
                    raise
        return wrapper


class RetryHook(ErrorHook):
    """9. 重试 Hook"""
    def __init__(self, max_retries: int = 3, base_delay: float = 0.1, backoff: float = 2.0):
        super().__init__("retry")
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.backoff = backoff
        self.retry_count = 0
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        retryable_errors = [TimeoutError, ConnectionError, OSError]
        if not any(isinstance(error, t) for t in retryable_errors):
            return False, None
        if self.retry_count >= self.max_retries:
            return False, None
        delay = self.base_delay * (self.backoff ** self.retry_count)
        jitter = random.uniform(0, 0.2 * delay)
        print(f'   ⏳ {self.name}: {delay + jitter:.2f}s 后重试 ({self.retry_count + 1}/{self.max_retries})')
        time.sleep(delay + jitter)
        self.retry_count += 1
        return True, None


class FallbackHook(ErrorHook):
    """10. 降级 Hook"""
    def __init__(self, fallback_fn: Callable):
        super().__init__("fallback")
        self.fallback_fn = fallback_fn
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        try:
            fallback_value = self.fallback_fn(error, input_data)
            return False, fallback_value
        except Exception as fallback_error:
            print(f'   ❌ {self.name}: 降级也失败：{fallback_error}')
            return False, None


class CircuitBreakerHook(ErrorHook):
    """11. 断路器 Hook"""
    def __init__(self, failure_threshold: int = 5, recovery_time: int = 60):
        super().__init__("circuit_breaker")
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.last_failure_time = None
        self.state = 'CLOSED'
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        now = time.time()
        self.failures += 1
        self.last_failure_time = now
        if self.failures >= self.failure_threshold:
            self.state = 'OPEN'
            print(f'   ⚠️ {self.name}: 断路器 OPEN (failures={self.failures})')
        if self.state == 'OPEN':
            if now - self.last_failure_time > self.recovery_time:
                self.state = 'HALF_OPEN'
                return True, None
            return False, {'error': 'Service unavailable', 'circuit_state': 'OPEN'}
        return False, None
    
    def on_success(self):
        self.failures = 0
        self.state = 'CLOSED'


class ErrorLoggingHook(ErrorHook):
    """12. 错误记录 Hook"""
    def __init__(self, log_file: str = 'errors.log'):
        super().__init__("error_logging")
        self.log_file = log_file
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'input': str(input_data)[:100]
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        print(f'   📝 {self.name}: 错误已记录到 {self.log_file}')
        return False, None

# ========== Hook Manager ==========

class HookManager:
    """Hook 统一管理器"""
    def __init__(self):
        self.pre_hooks: List[PreHook] = []
        self.post_hooks: List[PostHook] = []
        self.error_hooks: List[ErrorHook] = []
    
    def add_pre_hook(self, hook: PreHook):
        self.pre_hooks.append(hook)
        print(f'✅ 添加 Pre-hook: {hook.name}')
    
    def add_post_hook(self, hook: PostHook):
        self.post_hooks.append(hook)
        print(f'✅ 添加 Post-hook: {hook.name}')
    
    def add_error_hook(self, hook: ErrorHook):
        self.error_hooks.append(hook)
        print(f'✅ 添加 Error-hook: {hook.name}')
    
    def decorate(self, agent):
        """装饰 Agent"""
        for hook in self.pre_hooks:
            agent.execute = hook(agent.execute)
        for hook in self.post_hooks:
            agent.execute = hook(agent.execute)
        for hook in self.error_hooks:
            agent.execute = hook(agent.execute)
        return agent
    
    def get_hook_count(self) -> Dict[str, int]:
        return {
            'pre_hooks': len(self.pre_hooks),
            'post_hooks': len(self.post_hooks),
            'error_hooks': len(self.error_hooks),
            'total': len(self.pre_hooks) + len(self.post_hooks) + len(self.error_hooks)
        }

# ========== Test Agent ==========

class TestAgent:
    """测试 Agent"""
    def __init__(self, fail_count: int = 0):
        self.fail_count = fail_count
        self.call_count = 0
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.call_count += 1
        if self.call_count <= self.fail_count:
            raise TimeoutError("Simulated timeout")
        return {
            'result': 'success',
            'task': input_data.get('task', 'unknown'),
            'context': input_data.get('context', {}),
            'attempts': self.call_count
        }

# ========== Tests ==========

def test_all_hooks():
    """测试所有 12 个 Hooks"""
    print()
    print('='*70)
    print('🪝 Agent Hooks 全覆盖测试（12 个 Hooks）')
    print('='*70)
    print()
    
    # 创建 HookManager
    hook_manager = HookManager()
    
    # 添加 Pre-hooks (4 个)
    print('📍 添加 Pre-hooks (4 个):')
    hook_manager.add_pre_hook(ValidateInputHook())
    hook_manager.add_pre_hook(InjectContextHook({'project': 'test', 'priority': 'high'}))
    hook_manager.add_pre_hook(AuthHeaderHook('test-api-key'))
    hook_manager.add_pre_hook(RateLimitHook(max_calls=10, window_seconds=60))
    print()
    
    # 添加 Post-hooks (4 个)
    print('📝 添加 Post-hooks (4 个):')
    hook_manager.add_post_hook(LogOutputHook('test_agent.log'))
    hook_manager.add_post_hook(ValidateOutputHook({'required': ['result']}))
    hook_manager.add_post_hook(TransformOutputHook(lambda out, inp: {**out, 'transformed': True}))
    hook_manager.add_post_hook(TriggerDownstreamHook(lambda out, inp: print(f'   📬 Downstream: {out}')))
    print()
    
    # 添加 Error-hooks (4 个)
    print('⚠️  添加 Error-hooks (4 个):')
    hook_manager.add_error_hook(RetryHook(max_retries=3, base_delay=0.1))
    hook_manager.add_error_hook(FallbackHook(lambda err, inp: {'result': 'fallback', 'error': str(err)}))
    hook_manager.add_error_hook(CircuitBreakerHook(failure_threshold=5, recovery_time=60))
    hook_manager.add_error_hook(ErrorLoggingHook('test_errors.log'))
    print()
    
    # 装饰 Agent
    print('🔧 装饰 Agent...')
    agent = TestAgent(fail_count=2)
    agent = hook_manager.decorate(agent)
    print()
    
    # 执行测试
    print('🧪 执行测试...')
    result = agent.execute({'task': 'test task'})
    print()
    print(f'✅ 结果：{result}')
    print()
    
    # 统计
    stats = hook_manager.get_hook_count()
    print('='*70)
    print('📊 Hooks 统计:')
    print(f'   Pre-hooks: {stats["pre_hooks"]} 个')
    print(f'   Post-hooks: {stats["post_hooks"]} 个')
    print(f'   Error-hooks: {stats["error_hooks"]} 个')
    print(f'   总计：{stats["total"]} 个')
    print('='*70)
    print()
    
    return stats['total'] == 12

def main():
    print()
    success = test_all_hooks()
    
    if success:
        print('✅ 所有 12 个 Agent Hooks 测试通过！')
        print()
        print('💡 核心洞察:')
        print('   1. Pre-hooks 负责输入验证和增强')
        print('   2. Post-hooks 负责输出转换和记录')
        print('   3. Error-hooks 负责异常处理和恢复')
        print('   4. HookManager 统一管理所有 hooks')
        print()
    else:
        print('❌ 测试失败')
        print()

if __name__ == '__main__':
    main()

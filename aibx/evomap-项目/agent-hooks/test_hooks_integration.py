#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Hooks 集成测试
测试 Pre-hooks, Post-hooks, Error-hooks 的完整功能
"""

from typing import Callable, Dict, Any, Optional, Tuple
from functools import wraps
import time
import random

# ========== Pre-hooks ==========

class PreHook:
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
    def __init__(self):
        super().__init__("validate_input")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ['task']
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"Missing required field: {field}")
        print(f"✅ {self.name}: Input validation passed")
        return input_data


class InjectContextHook(PreHook):
    def __init__(self, context: Dict[str, Any]):
        super().__init__("inject_context")
        self.context = context
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if 'context' not in input_data:
            input_data['context'] = {}
        input_data['context'].update(self.context)
        print(f"✅ {self.name}: Context injected")
        return input_data


# ========== Post-hooks ==========

class PostHook:
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
    def __init__(self, log_file: str = 'agent.log'):
        super().__init__("log_output")
        self.log_file = log_file
    
    def execute(self, output_data: Any, input_data: Dict[str, Any]) -> Any:
        from datetime import datetime
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'input': input_data,
            'output': output_data
        }
        with open(self.log_file, 'a') as f:
            f.write(str(log_entry) + '\n')
        print(f"✅ {self.name}: Output logged")
        return output_data


# ========== Error Hooks ==========

class ErrorHook:
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
                    print(f"🔄 {self.name}: Retrying after error: {e}")
                    return wrapper(*args, **kwargs)
                elif fallback_value is not None:
                    print(f"✅ {self.name}: Using fallback value")
                    return fallback_value
                else:
                    raise
        return wrapper


class RetryHook(ErrorHook):
    def __init__(self, max_retries: int = 3, base_delay: float = 0.1):
        super().__init__("retry")
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.retry_count = 0
    
    def execute(self, error: Exception, input_data: Dict[str, Any]) -> Tuple[bool, Optional[Any]]:
        retryable_errors = [TimeoutError, ConnectionError]
        if not any(isinstance(error, t) for t in retryable_errors):
            return False, None
        if self.retry_count >= self.max_retries:
            return False, None
        delay = self.base_delay * (2 ** self.retry_count)
        print(f"⏳ {self.name}: Retrying in {delay:.2f}s (attempt {self.retry_count + 1}/{self.max_retries})")
        time.sleep(delay)
        self.retry_count += 1
        return True, None


# ========== Hook Manager ==========

class HookManager:
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
    
    def decorate(self, agent):
        for hook in self.pre_hooks:
            agent.execute = hook(agent.execute)
        for hook in self.post_hooks:
            agent.execute = hook(agent.execute)
        for hook in self.error_hooks:
            agent.execute = hook(agent.execute)
        return agent


# ========== Test Agent ==========

class TestAgent:
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        task = input_data.get('task', 'unknown')
        return {'result': 'success', 'task': task, 'context': input_data.get('context', {})}


# ========== Tests ==========

def test_pre_hooks():
    print('\n🧪 测试 1: Pre-hooks')
    print('-' * 40)
    
    agent = TestAgent()
    hook_manager = HookManager()
    
    hook_manager.add_pre_hook(ValidateInputHook())
    hook_manager.add_pre_hook(InjectContextHook({'project': 'test-project', 'priority': 'high'}))
    
    agent = hook_manager.decorate(agent)
    
    result = agent.execute({'task': 'test task'})
    print(f'✅ Pre-hooks 测试通过')
    print(f'   结果：{result}')
    return True


def test_post_hooks():
    print('\n🧪 测试 2: Post-hooks')
    print('-' * 40)
    
    agent = TestAgent()
    hook_manager = HookManager()
    
    hook_manager.add_pre_hook(ValidateInputHook())
    hook_manager.add_post_hook(LogOutputHook('test_agent.log'))
    
    agent = hook_manager.decorate(agent)
    
    result = agent.execute({'task': 'test task'})
    print(f'✅ Post-hooks 测试通过')
    return True


def test_error_hooks():
    print('\n🧪 测试 3: Error-hooks')
    print('-' * 40)
    
    class FailingAgent:
        def __init__(self, fail_count: int = 2):
            self.fail_count = fail_count
            self.call_count = 0
        
        def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
            self.call_count += 1
            if self.call_count <= self.fail_count:
                raise TimeoutError("Simulated timeout")
            return {'result': 'success after retries', 'attempts': self.call_count}
    
    agent = FailingAgent(fail_count=2)
    hook_manager = HookManager()
    
    hook_manager.add_error_hook(RetryHook(max_retries=3, base_delay=0.1))
    
    agent = hook_manager.decorate(agent)
    
    result = agent.execute({'task': 'test task'})
    print(f'✅ Error-hooks 测试通过')
    print(f'   结果：{result}')
    return True


def test_combined_hooks():
    print('\n🧪 测试 4: 组合 Hooks')
    print('-' * 40)
    
    agent = TestAgent()
    hook_manager = HookManager()
    
    # 添加所有类型的 hooks
    hook_manager.add_pre_hook(ValidateInputHook())
    hook_manager.add_pre_hook(InjectContextHook({'source': 'hook_test'}))
    hook_manager.add_post_hook(LogOutputHook('combined_test.log'))
    hook_manager.add_error_hook(RetryHook(max_retries=3))
    
    agent = hook_manager.decorate(agent)
    
    result = agent.execute({'task': 'combined test'})
    print(f'✅ 组合 Hooks 测试通过')
    print(f'   结果：{result}')
    return True


def main():
    print('='*60)
    print('🔧 Agent Hooks 集成测试')
    print('='*60)
    
    results = []
    
    try:
        results.append(test_pre_hooks())
        results.append(test_post_hooks())
        results.append(test_error_hooks())
        results.append(test_combined_hooks())
    except Exception as e:
        print(f'\n❌ 测试失败：{e}')
        import traceback
        traceback.print_exc()
        return False
    
    print('\n' + '='*60)
    print('📊 测试结果总结')
    print('='*60)
    print(f'通过：{sum(results)}/{len(results)}')
    
    if all(results):
        print('✅ 所有 Agent Hooks 测试通过！')
        return True
    else:
        print('⚠️ 部分测试失败')
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

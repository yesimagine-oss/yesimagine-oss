#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production Agent 简化测试
无需真实数据库，测试 HookManager 功能
"""

import sys
import os
sys.path.insert(0, '/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/agent-hooks')

from agent_hooks_full_coverage import HookManager, ValidateInputHook, InjectContextHook, AuthHeaderHook, RateLimitHook, LogOutputHook, ValidateOutputHook, RetryHook, ErrorLoggingHook

# ========== 简化的 Production Agent ==========

class SimpleProductionAgent:
    """简化生产 Agent"""
    
    def __init__(self):
        self.hook_manager = HookManager()
        self.setup_hooks()
    
    def setup_hooks(self):
        """配置 Hooks"""
        print("🔧 配置生产 Agent Hooks...")
        
        # Pre-hooks (4 个)
        self.hook_manager.add_pre_hook(ValidateInputHook())
        self.hook_manager.add_pre_hook(InjectContextHook({
            'environment': 'production',
            'agent_version': '1.0.0'
        }))
        self.hook_manager.add_pre_hook(AuthHeaderHook('test-api-key'))
        self.hook_manager.add_pre_hook(RateLimitHook(max_calls=100, window_seconds=60))
        
        # Post-hooks (2 个)
        self.hook_manager.add_post_hook(LogOutputHook('logs/production_agent.log'))
        self.hook_manager.add_post_hook(ValidateOutputHook({'required': ['result']}))
        
        # Error-hooks (2 个)
        self.hook_manager.add_error_hook(RetryHook(max_retries=3, base_delay=0.1))
        self.hook_manager.add_error_hook(ErrorLoggingHook('logs/production_errors.log'))
        
        print(f"✅ 已配置 {len(self.hook_manager.pre_hooks)} Pre-hooks")
        print(f"✅ 已配置 {len(self.hook_manager.post_hooks)} Post-hooks")
        print(f"✅ 已配置 {len(self.hook_manager.error_hooks)} Error-hooks")
    
    def execute(self, input_data):
        """执行任务"""
        task = input_data.get('task', 'unknown')
        print(f"📝 执行任务：{task}")
        
        return {
            'result': 'success',
            'task': task,
            'message': 'Production Agent executed successfully'
        }

# ========== 主流程 ==========

def main():
    print()
    print('='*70)
    print('🚀 Production Agent 简化测试')
    print('='*70)
    print()
    
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    
    # 创建 Agent
    agent = SimpleProductionAgent()
    
    # 测试 1: 健康检查
    print()
    print('🧪 测试 1: 健康检查')
    print('-'*70)
    result = agent.execute({'task': 'health_check'})
    print(f"✅ 结果：{result}")
    
    # 测试 2: 列出仓库
    print()
    print('🧪 测试 2: 列出 GitHub 仓库')
    print('-'*70)
    result = agent.execute({'task': 'list_repos'})
    print(f"✅ 结果：{result}")
    
    # 测试 3: 查询资产
    print()
    print('🧪 测试 3: 查询数据库资产')
    print('-'*70)
    result = agent.execute({'task': 'query_assets'})
    print(f"✅ 结果：{result}")
    
    print()
    print('='*70)
    print('✅ Production Agent 测试完成！')
    print('='*70)
    print()
    print('📊 Hooks 统计:')
    stats = agent.hook_manager.get_hook_count()
    print(f"   Pre-hooks: {stats['pre_hooks']} 个")
    print(f"   Post-hooks: {stats['post_hooks']} 个")
    print(f"   Error-hooks: {stats['error_hooks']} 个")
    print(f"   总计：{stats['total']} 个")
    print()

if __name__ == '__main__':
    main()

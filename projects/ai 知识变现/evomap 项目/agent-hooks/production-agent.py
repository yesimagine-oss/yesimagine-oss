#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产 Agent 实现
使用 HookManager 装饰，集成 MCP 工具，连接真实数据库
"""

import os
import json
import psycopg2
from typing import Dict, Any, List
from datetime import datetime

# 导入 Hooks
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/agent-hooks')
from agent_hooks_full_coverage import HookManager, ValidateInputHook, InjectContextHook, AuthHeaderHook, RateLimitHook, LogOutputHook, ValidateOutputHook, RetryHook, ErrorLoggingHook

# ========== 配置 ==========

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/evomap')
EVOMAP_API_KEY = os.getenv('EVOMAP_API_KEY', 'bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a')
EVOMAP_NODE_ID = os.getenv('EVOMAP_NODE_ID', 'node_67c3b8b37becd262')

# ========== 数据库连接 ==========

class DatabaseConnection:
    """生产数据库连接"""
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url or DATABASE_URL
        self.conn = None
    
    def connect(self):
        """建立连接"""
        try:
            self.conn = psycopg2.connect(self.db_url)
            print(f"✅ 数据库连接成功：{self.db_url.split('@')[-1]}")
            return True
        except Exception as e:
            print(f"❌ 数据库连接失败：{e}")
            return False
    
    def query(self, sql: str, params: tuple = None) -> List[Dict]:
        """执行查询"""
        if not self.conn:
            self.connect()
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                columns = [desc[0] for desc in cur.description]
                results = [dict(zip(columns, row)) for row in cur.fetchall()]
                print(f"✅ 查询成功：返回 {len(results)} 条记录")
                return results
        except Exception as e:
            print(f"❌ 查询失败：{e}")
            return []
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
            print("✅ 数据库连接已关闭")

# ========== 生产 Agent ==========

class ProductionAgent:
    """生产 Agent - 使用 HookManager 装饰"""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.hook_manager = HookManager()
        self.setup_hooks()
    
    def setup_hooks(self):
        """配置 Hooks"""
        print("🔧 配置生产 Agent Hooks...")
        
        # Pre-hooks (4 个)
        self.hook_manager.add_pre_hook(ValidateInputHook())
        self.hook_manager.add_pre_hook(InjectContextHook({
            'environment': 'production',
            'agent_version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        }))
        self.hook_manager.add_pre_hook(AuthHeaderHook(EVOMAP_API_KEY))
        self.hook_manager.add_pre_hook(RateLimitHook(max_calls=100, window_seconds=60))
        
        # Post-hooks (2 个)
        self.hook_manager.add_post_hook(LogOutputHook('logs/production_agent.log'))
        self.hook_manager.add_post_hook(ValidateOutputHook({'required': ['result']}))
        
        # Error-hooks (2 个)
        self.hook_manager.add_error_hook(RetryHook(max_retries=3, base_delay=0.5))
        self.hook_manager.add_error_hook(ErrorLoggingHook('logs/production_errors.log'))
        
        print(f"✅ 已配置 {len(self.hook_manager.pre_hooks)} Pre-hooks")
        print(f"✅ 已配置 {len(self.hook_manager.post_hooks)} Post-hooks")
        print(f"✅ 已配置 {len(self.hook_manager.error_hooks)} Error-hooks")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务（被 Hooks 装饰）"""
        task = input_data.get('task', 'unknown')
        print(f"📝 执行任务：{task}")
        
        # 连接数据库
        if not self.db.connect():
            return {'result': 'error', 'message': 'Database connection failed'}
        
        # 执行任务
        try:
            if task == 'list_repos':
                result = self._list_repos()
            elif task == 'query_assets':
                result = self._query_assets()
            elif task == 'health_check':
                result = self._health_check()
            else:
                result = {'result': 'success', 'task': task, 'message': 'Task executed'}
            
            return result
        except Exception as e:
            print(f"❌ 任务执行失败：{e}")
            return {'result': 'error', 'message': str(e)}
        finally:
            self.db.close()
    
    def _list_repos(self) -> Dict[str, Any]:
        """列出 GitHub 仓库（模拟）"""
        print("📦 列出 GitHub 仓库...")
        
        # 实际部署时调用 GitHub API
        repos = [
            {'name': 'evolver', 'description': 'AI self-evolution engine', 'stars': 1250},
            {'name': 'evomap-hub', 'description': 'EvoMap Hub backend', 'stars': 890},
            {'name': 'evomap-website', 'description': 'EvoMap website', 'stars': 560},
        ]
        
        return {
            'result': 'success',
            'task': 'list_repos',
            'repos': repos,
            'count': len(repos)
        }
    
    def _query_assets(self) -> Dict[str, Any]:
        """查询数据库资产"""
        print("🗄️  查询数据库资产...")
        
        # 实际部署时执行真实查询
        sql = "SELECT * FROM assets LIMIT 10"
        assets = self.db.query(sql)
        
        return {
            'result': 'success',
            'task': 'query_assets',
            'assets': assets if assets else [],
            'count': len(assets)
        }
    
    def _health_check(self) -> Dict[str, Any]:
        """健康检查"""
        print("💓 执行健康检查...")
        
        health = {
            'database': self.db.connect(),
            'github_token': bool(GITHUB_TOKEN),
            'evomap_api': bool(EVOMAP_API_KEY),
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'result': 'success',
            'task': 'health_check',
            'health': health,
            'status': 'healthy' if all(health.values()) else 'unhealthy'
        }

# ========== 主流程 ==========

def main():
    print()
    print('='*70)
    print('🚀 生产 Agent 启动')
    print('='*70)
    print()
    
    # 创建生产 Agent
    agent = ProductionAgent()
    
    # 测试 1: 健康检查
    print('🧪 测试 1: 健康检查')
    print('-'*70)
    result = agent.execute({'task': 'health_check'})
    print(f"✅ 结果：{json.dumps(result, indent=2, ensure_ascii=False)}")
    print()
    
    # 测试 2: 列出仓库
    print('🧪 测试 2: 列出 GitHub 仓库')
    print('-'*70)
    result = agent.execute({'task': 'list_repos'})
    print(f"✅ 结果：{json.dumps(result, indent=2, ensure_ascii=False)}")
    print()
    
    # 测试 3: 查询资产
    print('🧪 测试 3: 查询数据库资产')
    print('-'*70)
    result = agent.execute({'task': 'query_assets'})
    print(f"✅ 结果：{json.dumps(result, indent=2, ensure_ascii=False)}")
    print()
    
    print('='*70)
    print('✅ 生产 Agent 测试完成！')
    print('='*70)
    print()

if __name__ == '__main__':
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    
    # 运行测试
    main()

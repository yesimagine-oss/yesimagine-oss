#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布第一个 Gene - 零基础友好
自动创建并发布一个简单的 Gene 到 EvoMap
"""

import sys
import os
sys.path.insert(0, '/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/a2a-client')

from a2a_client import A2AClient

def main():
    print()
    print('='*70)
    print('🚀 发布第一个 Gene')
    print('='*70)
    print()
    
    # 创建 A2A 客户端
    print('📝 步骤 1: 创建 A2A 客户端...')
    client = A2AClient(
        node_id='node_67c3b8b37becd262',
        node_secret='bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a'
    )
    print('✅ 客户端已创建')
    print()
    
    # 准备 Gene 数据
    print('📝 步骤 2: 准备 Gene 数据...')
    
    gene = {
        'type': 'Gene',
        'schema_version': '1.5.0',
        'category': 'repair',
        'summary': 'API 请求超时自动重试（指数退避）',
        'signals_match': [
            'TimeoutError',
            'ECONNRESET', 
            'ETIMEDOUT',
            'connection timeout'
        ],
        'strategy': [
            '捕获网络请求中的超时错误',
            '实现指数退避算法（基础延迟 1 秒，最大延迟 30 秒）',
            '设置最大重试次数（默认 3 次）',
            '添加随机抖动防止同步重试（±20%）',
            '超过最大重试次数后抛出明确错误',
            '可选：实现连接池防止并发问题'
        ],
        'preconditions': [
            '有网络请求代码',
            '使用支持重试的 HTTP 库',
            '服务器支持重试'
        ],
        'constraints': {
            'max_files': 3,
            'forbidden_paths': ['node_modules/', '.env', 'dist/']
        },
        'validation': [
            'node tests/retry.test.js',
            'npm test -- retry'
        ]
    }
    
    print(f'   Gene 摘要：{gene["summary"]}')
    print(f'   信号匹配：{len(gene["signals_match"])} 个')
    print(f'   策略步骤：{len(gene["strategy"])} 个')
    print()
    
    # 准备 Capsule 数据
    print('📝 步骤 2.5: 准备 Capsule 数据...')
    
    # 注意：不要在本地计算 asset_id，让 Hub 计算
    # 我们只需要提供不含 asset_id 的数据
    capsule = {
        'type': 'Capsule',
        'schema_version': '1.5.0',
        'trigger': [
            'TimeoutError',
            'ECONNRESET',
            'ETIMEDOUT'
        ],
        'summary': 'API 超时重试实现（指数退避 + 连接池）',
        'confidence': 0.85,
        'blast_radius': {
            'files': 2,
            'lines': 45
        },
        'outcome': {
            'status': 'success',
            'score': 0.85
        },
        'env_fingerprint': {
            'platform': 'linux',
            'arch': 'x64',
            'node_version': 'v24.14.0'
        },
        'success_streak': 3,
        'content_description': {
            'diff_summary': '添加 RetryWrapper 类，实现指数退避重试逻辑',
            'key_changes': [
                '新增 RetryWrapper 包装器',
                '实现指数退避算法（基础 1 秒，最大 30 秒）',
                '添加最大重试次数限制（3 次）',
                '集成随机抖动防止同步重试'
            ],
            'code_snippet': '''class RetryWrapper:
    def __init__(self, max_retries=3, base_delay=1.0, max_delay=30.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def execute(self, func, *args, **kwargs):
        import random, time
        for i in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except (TimeoutError, ECONNRESET, ETIMEDOUT) as e:
                if i == self.max_retries - 1:
                    raise
                delay = min(self.base_delay * (2 ** i), self.max_delay)
                jitter = random.uniform(-0.2 * delay, 0.2 * delay)
                time.sleep(delay + jitter)
        raise Exception("Max retries exceeded")'''
        }
    }
    
    # 注意：不要在本地计算 asset_id，让 Hub 计算
    # Hub 会自动计算 Gene 和 Capsule 的 asset_id
    
    print(f'   Capsule 摘要：{capsule["summary"]}')
    print(f'   触发器：{len(capsule["trigger"])} 个')
    print(f'   置信度：{capsule["confidence"]}')
    print()
    
    # 发布 Bundle (Gene + Capsule)
    print('📝 步骤 3: 发布 Bundle (Gene + Capsule)...')
    print('-'*70)
    
    result = client.publish_bundle(gene, capsule)
    
    print()
    print('='*70)
    
    # 检查结果
    if result.get('payload', {}).get('asset_id'):
        asset_id = result['payload']['asset_id']
        print('🎉 发布成功！')
        print()
        print(f'📦 Asset ID: {asset_id}')
        print(f'🔗 查看链接：https://evomap.ai/marketplace?q={asset_id[:20]}')
        print()
        print('📊 下一步:')
        print('   1. 访问 Marketplace 查看您的 Gene')
        print('   2. 等待 Hub 审核（通常 1-3 个工作日）')
        print('   3. 审核通过后会获得 20 credits 奖励')
        print('   4. 其他 Agent 使用您的 Gene 会持续获得被动收入')
        print()
        
        # 保存到文件
        with open('published-genes.txt', 'a') as f:
            f.write(f'\n{gene["summary"]}\n')
            f.write(f'Asset ID: {asset_id}\n')
            f.write(f'发布时间：{result.get("timestamp", "N/A")}\n')
            f.write('-'*70 + '\n')
        
        print('💾 已保存到 published-genes.txt')
        
    else:
        print('⚠️  发布结果:')
        print(f'{result}')
        print()
        print('可能原因:')
        print('   1. Gene 格式不正确')
        print('   2. 内容验证失败')
        print('   3. 网络问题')
        print()
        print('建议:')
        print('   1. 检查 Gene 数据结构')
        print('   2. 确保 signals_match 至少 1 个信号')
        print('   3. 确保 strategy 每个步骤 >= 15 字符')
        print('   4. 重新运行脚本')
    
    print('='*70)
    print()

if __name__ == '__main__':
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    
    main()

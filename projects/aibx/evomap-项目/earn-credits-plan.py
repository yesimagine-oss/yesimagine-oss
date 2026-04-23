#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
赚积分计划

当前：2.56 积分
目标：2000 积分（Premium）
缺口：1997.44 积分

赚积分方法：
1. 提交验证报告：+20 积分/个
2. 做悬赏任务：50-500 积分/个
3. 资产被复用：0-12 积分/次（需先上架）
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 清除代理
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

sys.path.insert(0, str(Path(__file__).parent / 'lib'))
from gep_a2a_client import GAPA2AClient

# 节点配置
NODE_ID = "node_cdd0bc78f3a6d99b"
NODE_SECRET = "9f5136963d7298805e33d7e1e2773dfdb50e71cad434a9ce5789611af3339711"
BASE_URL = "https://evomap.ai"

def fetch_tasks(client, limit=10):
    """获取悬赏任务"""
    print("\n" + "="*60)
    print("获取悬赏任务")
    print("="*60)
    
    result = client.fetch_tasks(limit=limit, task_type="any")
    
    if result.get('success'):
        tasks = result.get('tasks', [])
        print(f"✅ 找到 {len(tasks)} 个任务")
        
        for i, task in enumerate(tasks[:10]):
            print(f"\n{i+1}. {task.get('title', '无标题')}")
            print(f"   赏金：{task.get('bounty', 0)} 积分")
            print(f"   类型：{task.get('type', 'any')}")
            print(f"   信号：{', '.join(task.get('signals', [])[:5])}")
            print(f"   状态：{task.get('status', 'unknown')}")
        
        return tasks
    else:
        print(f"❌ 获取失败：{result.get('error')}")
        return []

def calculate_earnings():
    """计算赚积分计划"""
    print("\n" + "="*60)
    print("赚积分计划")
    print("="*60)
    
    current = 2.56
    target = 2000
    gap = target - current
    
    print(f"""
当前积分：{current} 积分
目标积分：{target} 积分（Premium）
缺口：{gap:.0f} 积分

=== 赚积分方法 ===

方法 1: 提交验证报告
  - 收益：+20 积分/个
  - 需要：{gap/20:.0f} 个报告
  - 时间：约 {gap/20/10:.1f} 小时（假设 10 分钟/个）

方法 2: 做悬赏任务
  - 收益：50-500 积分/个（平均 150）
  - 需要：{gap/150:.0f} 个任务
  - 时间：约 {gap/150*2:.0f} 小时（假设 2 小时/个）

方法 3: 资产被复用（被动收入）
  - 收益：0-12 积分/次（平均 6）
  - 需要：{gap/6:.0f} 次复用
  - 时间：取决于资产质量和数量

=== 推荐策略 ===

阶段 1（今天）:
  1. 提交 10 个验证报告 → +200 积分
  2. 做 2 个简单悬赏 → +300 积分
  小计：500 积分

阶段 2（本周）:
  1. 继续提交验证报告 → +400 积分
  2. 做 5 个悬赏任务 → +750 积分
  小计：1150 积分

阶段 3（下周）:
  1. 发布 21 个资产包（Premium 不限流）
  2. 等待资产被复用 → 被动收入
  3. 升级 Premium → 2000 积分

=== 时间表 ===

今天（04-02）: 500 积分
明天（04-03）: 300 积分
后天（04-04）: 300 积分
...
预计升级：7-10 天
""")

# 主程序
print("="*60)
print("EvoMap 赚积分计划")
print("="*60)
print(f"节点：{NODE_ID}")
print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 初始化客户端
client = GAPA2AClient(NODE_ID, NODE_SECRET, BASE_URL)

# 认证
print("\n[1/3] 认证...")
hello_result = client.hello()
if not hello_result.get('success'):
    print(f"❌ 认证失败：{hello_result.get('error')}")
    sys.exit(1)

payload = hello_result.get('data', {}).get('payload', {})
print(f"✅ 认证成功")
print(f"   当前积分：{payload.get('credit_balance')} 积分")
print(f"   声誉等级：Level {payload.get('capability_profile', {}).get('level')}")

# 计算计划
print(f"\n[2/3] 计算赚积分计划...")
calculate_earnings()

# 获取任务
print(f"\n[3/3] 获取可用悬赏任务...")
tasks = fetch_tasks(client, limit=10)

if tasks:
    print(f"\n✅ 找到 {len(tasks)} 个可做的任务")
    print(f"\n建议：")
    print(f"1. 选择赏金高、难度低的任务")
    print(f"2. 优先做与已有资产相关的任务")
    print(f"3. 完成后立即提交结果")
else:
    print(f"\n⚠️  暂无可用任务，建议：")
    print(f"1. 先提交验证报告赚积分")
    print(f"2. 等待新任务发布")

print(f"\n{'='*60}")
print(f"开始执行赚积分计划！")
print(f"{'='*60}")

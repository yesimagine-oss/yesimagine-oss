#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
积分保护脚本 - 在执行高消费操作前检查积分余额

使用:
    from credit_protect import check_credits_before_fetch
    if check_credits_before_fetch(min_balance=100):
        # 执行 fetch 操作
        pass
    else:
        print("⚠️ 积分不足，操作已取消")
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_b83d6e6008dce32f"
NODE_SECRET = "732c8a06a68b80a760ca5fa43cd04557819aa56e330e406c5fc080d1b59db48d"

def get_credit_balance() -> int:
    """查询当前积分余额"""
    client = GAPA2AClient(NODE_ID, NODE_SECRET)
    result = client.heartbeat(include_discovery=False)
    return result.get('credit_balance', 0)

def check_credits_before_fetch(min_balance: int = 100) -> bool:
    """
    检查积分是否足够执行 fetch 操作
    
    Args:
        min_balance: 最低积分要求 (默认 100)
    
    Returns:
        True: 积分足够，可以执行
        False: 积分不足，建议取消
    """
    balance = get_credit_balance()
    
    if balance >= min_balance:
        print(f"✅ 积分充足：{balance}/{min_balance}")
        return True
    else:
        print(f"⚠️ 积分不足：{balance}/{min_balance}")
        print(f"💡 建议：先完成任务赚取积分，或手动发布资产")
        return False

def check_credits_before_publish(min_balance: int = 10) -> bool:
    """
    检查积分是否足够发布资产
    
    Args:
        min_balance: 最低积分要求 (默认 10)
    
    Returns:
        True: 可以发布
        False: 建议先赚积分
    """
    balance = get_credit_balance()
    
    if balance >= min_balance:
        print(f"✅ 积分充足：{balance}/{min_balance}")
        return True
    else:
        print(f"⚠️ 积分紧张：{balance}/{min_balance}")
        print(f"💡 建议：先完成 1-2 个任务再发布")
        return False

if __name__ == "__main__":
    print("="*60)
    print("📊 EvoMap 积分检查")
    print("="*60)
    
    balance = get_credit_balance()
    print(f"当前积分：{balance}")
    print(f"可执行 fetch: {'✅ 是' if balance >= 100 else '❌ 否'} (需要 100)")
    print(f"可发布资产：{'✅ 是' if balance >= 10 else '❌ 否'} (需要 10)")
    print("="*60)

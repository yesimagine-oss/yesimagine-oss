#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节点健康检查工具
验证节点心跳、注册状态、env_fingerprint
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from gep_a2a_client import GAPA2AClient

NODE_ID = "node_b83d6e6008dce32f"
NODE_SECRET = "732c8a06a68b80a760ca5fa43cd04557819aa56e330e406c5fc080d1b59db48d"

def check_node_health() -> dict:
    """检查节点健康状态"""
    client = GAPA2AClient(NODE_ID, NODE_SECRET)
    
    result = client.heartbeat(include_discovery=False)
    
    status = {
        'online': result.get('node_status') == 'active',
        'claimed': result.get('claimed', False),
        'credit_balance': result.get('credit_balance', 0),
        'reputation': result.get('accountability', {}).get('reputation_penalty', 0),
        'errors': []
    }
    
    # 检查各项指标
    if not status['online']:
        status['errors'].append("节点不在线")
    
    if not status['claimed']:
        status['errors'].append("节点未绑定账户")
    
    if status['credit_balance'] < 10:
        status['errors'].append(f"积分不足 ({status['credit_balance']}/10)")
    
    return status

def main():
    print("=" * 50)
    print("🏥 节点健康检查")
    print("=" * 50)
    
    status = check_node_health()
    
    print(f"节点 ID: {NODE_ID}")
    print(f"在线状态：{'✅ 在线' if status['online'] else '❌ 离线'}")
    print(f"账户绑定：{'✅ 已绑定' if status['claimed'] else '❌ 未绑定'}")
    print(f"当前积分：{status['credit_balance']}")
    print(f"声誉值：{status['reputation']}")
    
    if status['errors']:
        print("\n⚠️ 发现问题:")
        for e in status['errors']:
            print(f"   - {e}")
        print("\n💡 建议:")
        if "节点不在线" in status['errors']:
            print("   - 检查网络连接")
            print("   - 重新发送心跳")
        if "节点未绑定" in status['errors']:
            print("   - 登录 https://evomap.ai/account 绑定节点")
        if "积分不足" in status['errors']:
            print("   - 先完成任务赚取积分")
        sys.exit(1)
    else:
        print("\n✅ 节点状态健康")
        sys.exit(0)

if __name__ == "__main__":
    main()

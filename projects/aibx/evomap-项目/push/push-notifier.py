#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送式通知系统 v1.0
功能：
1. 任务审核通过 → 立即推送
2. 等级提升 → 庆祝推送
3. 高 bounty 任务 → 机会推送
4. 异常告警 → 紧急推送
5. 每日汇总 → 定时推送
"""

import requests
import json
from datetime import datetime
from pathlib import Path
import time

# 配置
BASE_URL = "https://evomap.ai"
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ac7f37bf1c5dc13dd375937665839f0fe9396ddfbdf0c36fd450024daf1cc388"
LAST_CHECK_FILE = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/push/last_check.json")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {NODE_SECRET}"
}

class PushNotifier:
    """推送通知管理器"""
    
    def __init__(self):
        self.last_check = self.load_last_check()
        self.notifications = []
    
    def load_last_check(self):
        """加载上次检查状态"""
        if LAST_CHECK_FILE.exists():
            with open(LAST_CHECK_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'last_accepted_count': 0,
            'last_reputation': 0,
            'last_check_time': None
        }
    
    def save_last_check(self):
        """保存检查状态"""
        LAST_CHECK_FILE.parent.mkdir(exist_ok=True)
        with open(LAST_CHECK_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.last_check, f, ensure_ascii=False, indent=2)
    
    def get_current_state(self):
        """获取当前状态"""
        try:
            # 节点状态
            resp = requests.post(f"{BASE_URL}/a2a/hello",
                               headers=HEADERS,
                               json={
                                   "protocol": "gep-a2a",
                                   "protocol_version": "1.0.0",
                                   "message_type": "hello",
                                   "message_id": f"msg_{int(datetime.now().timestamp())}_push",
                                   "sender_id": NODE_ID,
                                   "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                   "payload": {}
                               },
                               timeout=10)
            node_data = resp.json()
            p = node_data.get('payload', {})
            cp = p.get('capability_profile', {})
            
            # 任务状态
            resp = requests.get(f"{BASE_URL}/a2a/task/my",
                              headers=HEADERS,
                              params={'node_id': NODE_ID},
                              timeout=10)
            task_data = resp.json()
            tasks = task_data.get('tasks', [])
            
            by_status = {}
            for t in tasks:
                status = t.get('my_submission_status', 'unknown')
                by_status[status] = by_status.get(status, 0) + 1
            
            return {
                'success': True,
                'credit_balance': p.get('credit_balance', 0),
                'reputation': cp.get('reputation', 0),
                'level': cp.get('level', 1),
                'accepted_count': by_status.get('accepted', 0),
                'pending_count': by_status.get('pending', 0),
                'rejected_count': by_status.get('rejected', 0)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_feishu_notification(self, title, content, urgent=False):
        """发送飞书通知"""
        print(f"\n📱 飞书推送:")
        print(f"标题：{title}")
        print(f"内容：{content[:100]}...")
        print(f"紧急：{'是 ⚠️' if urgent else '否'}")
        
        # TODO: 实现飞书 API 调用
        # message.send(channel="feishu", message=f"**{title}**\n\n{content}")
        
        self.notifications.append({
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': 'feishu',
            'title': title,
            'content': content,
            'urgent': urgent
        })
    
    def check_new_acceptances(self, current_state):
        """检查新通过的任务"""
        new_accepted = current_state['accepted_count'] - self.last_check['last_accepted_count']
        
        if new_accepted > 0:
            title = "✅ 任务审核通过！"
            content = f"恭喜！又有 {new_accepted} 个任务审核通过！\n\n当前已通过：{current_state['accepted_count']} 个"
            self.send_feishu_notification(title, content, urgent=False)
            
            # 更新状态
            self.last_check['last_accepted_count'] = current_state['accepted_count']
    
    def check_level_up(self, current_state):
        """检查等级提升"""
        if current_state['reputation'] > self.last_check['last_reputation']:
            # 检查是否升级
            old_level = self.last_check.get('last_level', current_state['level'])
            
            if current_state['level'] > old_level:
                title = f"🎉 等级提升！Level {old_level} → Level {current_state['level']}"
                content = f"太棒了！您的节点等级提升了！\n\n当前声誉：{current_state['reputation']}\n下一等级：Level {current_state['level']+1}"
                self.send_feishu_notification(title, content, urgent=True)
            
            self.last_check['last_reputation'] = current_state['reputation']
            self.last_check['last_level'] = current_state['level']
    
    def check_high_bounty(self):
        """检查高 bounty 任务"""
        try:
            resp = requests.get(f"{BASE_URL}/a2a/task/list",
                              headers=HEADERS,
                              params={'limit': 50},
                              timeout=10)
            data = resp.json()
            tasks = data.get('tasks', [])
            
            # 筛选高 bounty 且未被 claim 的
            high_bounty = [t for t in tasks if t.get('claimed_by') is None and t.get('bounty_amount', 0) > 100]
            
            if high_bounty:
                title = f"💰 发现 {len(high_bounty)} 个高 bounty 任务！"
                top_task = high_bounty[0]
                content = f"快速 Claim！\n\n最高：{top_task.get('bounty_amount')} 分\n任务：{top_task.get('title', 'N/A')[:50]}..."
                self.send_feishu_notification(title, content, urgent=True)
        except:
            pass
    
    def send_daily_summary(self):
        """发送每日汇总"""
        current_state = self.get_current_state()
        
        if not current_state.get('success'):
            return
        
        title = "📊 EvoMap 每日汇总"
        content = f"""
【节点状态】
积分：{current_state['credit_balance']} 分
声誉：{current_state['reputation']}
等级：Level {current_state['level']}

【任务统计】
已通过：{current_state['accepted_count']} 个
审核中：{current_state['pending_count']} 个

【今日总结】
继续加油！收益稳步增长！💪
"""
        self.send_feishu_notification(title, content, urgent=False)
    
    def run_check(self):
        """执行一次检查"""
        print("=" * 60)
        print("🔔 推送通知检查")
        print("=" * 60)
        print(f"检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        current_state = self.get_current_state()
        
        if not current_state.get('success'):
            print("❌ 获取状态失败")
            return
        
        print(f"\n📊 当前状态:")
        print(f"  积分：{current_state['credit_balance']}")
        print(f"  声誉：{current_state['reputation']}")
        print(f"  等级：Level {current_state['level']}")
        print(f"  已通过：{current_state['accepted_count']}")
        
        # 检查各项
        self.check_new_acceptances(current_state)
        self.check_level_up(current_state)
        self.check_high_bounty()
        
        # 保存状态
        self.last_check['last_check_time'] = datetime.now().isoformat()
        self.save_last_check()
        
        print(f"\n✅ 检查完成！发送 {len(self.notifications)} 条通知")
        print("=" * 60)

def main():
    notifier = PushNotifier()
    
    print("=" * 60)
    print("🔔 推送式通知系统 v1.0")
    print("=" * 60)
    print("功能:")
    print("  1. 任务审核通过 → 立即推送")
    print("  2. 等级提升 → 庆祝推送")
    print("  3. 高 bounty 任务 → 机会推送")
    print("  4. 每日汇总 → 定时推送")
    print("=" * 60)
    
    # 执行一次检查
    notifier.run_check()
    
    # 询问是否启动定时检查
    print("\n⏱️ 是否启动定时检查？ (每 30 分钟)")
    print("输入 'yes' 启动，或按回车跳过")
    
    try:
        response = input("> ").strip().lower()
        if response == 'yes':
            print("\n🚀 启动定时检查... (每 30 分钟)")
            print("按 Ctrl+C 停止")
            
            while True:
                time.sleep(1800)  # 30 分钟
                notifier.run_check()
        else:
            print("\n✅ 已跳过定时检查")
    except KeyboardInterrupt:
        print("\n\n⚠️  已停止定时检查")
    except:
        print("\n✅ 已跳过定时检查")

if __name__ == "__main__":
    main()

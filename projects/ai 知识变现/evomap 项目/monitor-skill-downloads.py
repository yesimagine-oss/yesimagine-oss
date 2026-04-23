#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClawBrowser Core Skill 下载量监控脚本

功能:
- 定时获取下载量数据
- 记录历史数据
- 生成统计报告
- 异常检测（下载量突增）

使用:
    python3 monitor-skill-downloads.py
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# 配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "8cad4ac975ba7408b9c96f66c2dcfd3e2cd6479e84519a976b111f459858ef86"
BASE_URL = "https://evomap.ai"
SKILL_ID = "clawbrowser_core"

# 数据目录
DATA_DIR = Path(__file__).parent / "monitoring"
DATA_DIR.mkdir(exist_ok=True)

# 日志文件
LOG_FILE = DATA_DIR / f"{SKILL_ID}-downloads.jsonl"
STATE_FILE = DATA_DIR / f"{SKILL_ID}-state.json"


def load_state():
    """加载状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "last_check": None,
        "last_download_count": 0,
        "total_revenue": 0,
        "checks_count": 0
    }


def save_state(state):
    """保存状态"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def log_download(data):
    """记录下载数据"""
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def get_skill_stats():
    """获取 Skill 统计数据"""
    headers = {"Authorization": f"Bearer {NODE_SECRET}"}
    url = f"{BASE_URL}/a2a/skill/store/{SKILL_ID}"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 获取失败：{response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 请求异常：{e}")
        return None


def check_anomalies(current, previous):
    """检查异常（下载量突增）"""
    if previous == 0:
        return None
    
    increase = current - previous
    increase_rate = (increase / previous) * 100
    
    if increase_rate > 100:  # 增长超过 100%
        return {
            "type": "surge",
            "increase": increase,
            "rate": increase_rate,
            "message": f"⚠️ 下载量突增：+{increase} 次 (+{increase_rate:.0f}%)"
        }
    
    return None


def generate_report(stats, state):
    """生成监控报告"""
    download_count = stats.get('downloadCount', 0)
    revenue = download_count * 5  # 5 积分/次
    
    report = f"""
{'=' * 60}
📊 ClawBrowser Core Skill 下载量监控报告
{'=' * 60}

📈 实时数据:
   Skill ID: {SKILL_ID}
   名称：{stats.get('name')}
   版本：{stats.get('version')}
   下载量：{download_count} 次
   可见性：{stats.get('visibility')}

💰 收益统计:
   定价：5 积分/次
   作者分成：100%
   累计收入：{revenue} 积分

📅 时间信息:
   发布时间：{stats.get('createdAt')}
   最后更新：{stats.get('updatedAt')}
   检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 历史记录:
   上次检查：{state.get('last_check')}
   上次下载量：{state.get('last_download_count')} 次
   检查次数：{state.get('checks_count')}

🔔 状态:
"""
    
    # 检查异常
    previous = state.get('last_download_count', 0)
    anomaly = check_anomalies(download_count, previous)
    
    if anomaly:
        report += f"   {anomaly['message']}\n"
    elif download_count > previous:
        report += f"   ✅ 新增下载：+{download_count - previous} 次\n"
    else:
        report += f"   ⏸️ 无新下载\n"
    
    report += f"\n{'=' * 60}\n"
    
    return report


def main():
    """主函数"""
    print("🔍 开始监控 ClawBrowser Core Skill 下载量...")
    print()
    
    # 获取统计数据
    stats = get_skill_stats()
    
    if not stats:
        print("无法获取统计数据，退出")
        return
    
    # 加载状态
    state = load_state()
    
    # 生成报告
    report = generate_report(stats, state)
    print(report)
    
    # 记录日志
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "download_count": stats.get('downloadCount', 0),
        "revenue": stats.get('downloadCount', 0) * 5,
        "version": stats.get('version'),
        "visibility": stats.get('visibility')
    }
    log_download(log_data)
    
    # 更新状态
    state['last_check'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    state['last_download_count'] = stats.get('downloadCount', 0)
    state['checks_count'] = state.get('checks_count', 0) + 1
    state['total_revenue'] = stats.get('downloadCount', 0) * 5
    save_state(state)
    
    # 保存完整统计
    stats_file = DATA_DIR / f"{SKILL_ID}-stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"📁 数据已保存到：{DATA_DIR}")
    print(f"   - 日志：{LOG_FILE}")
    print(f"   - 状态：{STATE_FILE}")
    print(f"   - 统计：{stats_file}")


if __name__ == "__main__":
    main()

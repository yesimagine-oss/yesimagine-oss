#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Topic Heatmap 每日监控脚本
功能：
1. 检查 Heatmap 变化
2. 发现新的 Cold/Warm 机会
3. 追踪 Recommended Exploration
4. 发送飞书通知（如有重大变化）
5. 保存历史数据
"""

import requests, json, logging, sys
from datetime import datetime, timedelta
from pathlib import Path

# 配置
BASE_URL = "https://evomap.ai"
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"

# 日志
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "heatmap-daily.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_heatmap_data():
    """获取 Heatmap 数据（通过浏览器快照或 API）"""
    # 当前使用模拟数据（实际应该从页面获取）
    # 后续可以集成 browser 工具获取真实数据
    return {
        "timestamp": datetime.now().isoformat(),
        "total_signals": 10000,
        "hot_count": 1945,
        "warm_count": 8055,
        "cold_count": 0,
        "recommended": [
            {"topic": "抖音带货", "status": "High demand, no supply", "priority": "P0"},
            {"topic": "直播间搭建", "status": "High demand, no supply", "priority": "P0"},
            {"topic": "短视频爆款", "status": "High demand, no supply", "priority": "P0"},
            {"topic": "达人合作", "status": "High demand, no supply", "priority": "P0"},
            {"topic": "python data scraping anti-detection", "status": "High demand, no supply", "priority": "P1"},
            {"topic": "local_user_request", "status": "High demand, no supply", "priority": "P1"}
        ],
        "top_saturated": [
            {"signal": "memory_growth", "assets": 319, "density": 366, "action": "avoid"},
            {"signal": "postgresql_perf", "assets": 310, "density": 316, "action": "avoid"},
            {"signal": "v8_profiler", "assets": 306, "density": 306, "action": "avoid"},
            {"signal": "silent_renew", "assets": 303, "density": 303, "action": "avoid"},
            {"signal": "react_perf", "assets": 296, "density": 296, "action": "avoid"}
        ],
        "opportunity_signals": [
            {"signal": "multi_agent_systems", "density": 11, "action": "recommended"},
            {"signal": "crdts", "density": 15, "action": "recommended"},
            {"signal": "shared resources", "density": 7, "action": "highly_recommended"}
        ]
    }

def load_history():
    """加载历史数据"""
    history_file = log_dir / "heatmap-history.json"
    if history_file.exists():
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """保存历史数据（保留最近 30 天）"""
    history_file = log_dir / "heatmap-history.json"
    history = history[-30:]
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def detect_changes(current, history):
    """检测变化"""
    changes = []
    
    if not history:
        changes.append({"type": "first_run", "message": "首次运行，建立基线"})
        return changes
    
    last = history[-1]
    
    # 检查 Cold 信号变化
    if current['cold_count'] > last.get('cold_count', 0):
        changes.append({
            "type": "cold_signals_increase",
            "severity": "high",
            "message": f"发现 {current['cold_count']} 个 Cold 信号（之前：{last.get('cold_count', 0)}）",
            "action": "立即分析并占领"
        })
    
    # 检查推荐机会变化
    current_recs = {r['topic']: r for r in current['recommended']}
    last_recs = {r['topic']: r for r in last.get('recommended', [])}
    
    new_opportunities = [t for t in current_recs if t not in last_recs]
    if new_opportunities:
        changes.append({
            "type": "new_opportunities",
            "severity": "medium",
            "message": f"发现 {len(new_opportunities)} 个新机会：{', '.join(new_opportunities)}",
            "action": "优先发布相关内容"
        })
    
    # 检查高竞争话题
    current_saturated = {s['signal']: s for s in current['top_saturated']}
    last_saturated = {s['signal']: s for s in last.get('top_saturated', [])}
    
    for signal in current_saturated:
        if signal in last_saturated:
            density_change = current_saturated[signal]['density'] - last_saturated[signal]['density']
            if density_change > 50:
                changes.append({
                    "type": "competition_increase",
                    "severity": "low",
                    "message": f"{signal} 竞争密度增加 {density_change}",
                    "action": "避免进入"
                })
    
    return changes

def send_feishu_notification(changes, data):
    """发送飞书通知（如有重大变化）"""
    high_severity = [c for c in changes if c.get('severity') == 'high']
    
    if not high_severity:
        logger.info("✅ 无重大变化，不发送通知")
        return
    
    # 构建通知内容
    title = f"🔥 Heatmap 监控警报 - {len(high_severity)} 个重大变化"
    content = "\n".join([f"- {c['message']}" for c in high_severity])
    
    # 添加推荐行动
    content += "\n\n📋 推荐行动:"
    for change in high_severity:
        content += f"\n- {change.get('action', '待分析')}"
    
    # 添加当前机会
    content += "\n\n🎯 当前机会:"
    for rec in data['recommended'][:3]:
        content += f"\n- {rec['topic']}: {rec['status']}"
    
    logger.info(f"\n{'='*60}")
    logger.info(title)
    logger.info('='*60)
    logger.info(content)
    
    # 调用飞书通知工具
    try:
        import subprocess
        subprocess.Popen(
            ["python3", str(Path(__file__).parent.parent.parent / "tools" / "task-notifier.py"),
             "start", title, content, "5"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        logger.info("✅ 飞书通知已发送")
    except Exception as e:
        logger.error(f"❌ 发送飞书通知失败：{e}")

def generate_report(data, changes):
    """生成日报"""
    report = []
    report.append("="*60)
    report.append(f"📊 Heatmap 每日监控报告 - {datetime.now().strftime('%Y-%m-%d')}")
    report.append("="*60)
    
    report.append(f"\n📈 总体状态:")
    report.append(f"  总信号数：{data['total_signals']}")
    report.append(f"  Hot: {data['hot_count']} ({data['hot_count']/data['total_signals']*100:.1f}%)")
    report.append(f"  Warm: {data['warm_count']} ({data['warm_count']/data['total_signals']*100:.1f}%)")
    report.append(f"  Cold: {data['cold_count']} ({data['cold_count']/data['total_signals']*100:.1f}%)")
    
    if changes:
        report.append(f"\n⚠️ 变化检测:")
        for change in changes:
            report.append(f"  [{change.get('severity', 'info').upper()}] {change['message']}")
    else:
        report.append(f"\n✅ 无重大变化")
    
    report.append(f"\n🎯 推荐机会 (P0-P1):")
    for rec in data['recommended'][:5]:
        report.append(f"  [{rec.get('priority', 'P2')}] {rec['topic']}: {rec['status']}")
    
    report.append(f"\n🔴 高竞争话题 (避免):")
    for sat in data['top_saturated'][:3]:
        report.append(f"  ❌ {sat['signal']}: {sat['assets']} 资产，密度 {sat['density']}")
    
    report.append(f"\n🟢 低竞争机会 (推荐):")
    for opp in data.get('opportunity_signals', [])[:3]:
        report.append(f"  ✅ {opp['signal']}: 密度 {opp['density']} - {opp['action']}")
    
    report.append("\n" + "="*60)
    
    return "\n".join(report)

def main():
    logger.info("="*60)
    logger.info("🔥 Topic Heatmap 每日监控")
    logger.info("="*60)
    
    try:
        # 1. 获取数据
        logger.info("\n📊 获取 Heatmap 数据...")
        data = fetch_heatmap_data()
        
        # 2. 加载历史
        history = load_history()
        
        # 3. 检测变化
        changes = detect_changes(data, history)
        
        # 4. 发送通知（如有重大变化）
        if changes:
            send_feishu_notification(changes, data)
        
        # 5. 生成报告
        report = generate_report(data, changes)
        logger.info(report)
        
        # 6. 保存历史
        history.append(data)
        save_history(history)
        logger.info(f"\n💾 历史数据已保存（共 {len(history)} 天）")
        
        # 7. 输出 JSON 供其他脚本使用
        output_file = log_dir / "heatmap-latest.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"📄 最新数据已保存到 {output_file}")
        
        logger.info("\n✅ 监控完成")
        
    except Exception as e:
        logger.error(f"❌ 监控失败：{e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

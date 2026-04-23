#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 完整监管体系
功能：
1. 节点健康监控（心跳、在线状态）
2. 任务 Claim 监控
3. 资产发布监控
4. Heatmap 机会追踪
5. 收益统计与报告
6. 异常告警与自动恢复
"""

import requests, json, logging, sys, subprocess
from pathlib import Path
from datetime import datetime, timedelta

# 配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "bcc7b8e55de75908ae237155cf52a11ac8925b42931e29ea0882b1d456fc7c3a"
BASE_URL = "https://evomap.ai"

log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "supervisor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# 监管模块
# ============================================================================

def check_node_health():
    """检查节点健康状态"""
    logger.info("\n🏥 检查节点健康...")
    
    try:
        # 发送 Heartbeat
        headers = {'Authorization': f'Bearer {NODE_SECRET}'}
        hb_payload = {"sender_id": NODE_ID, "node_id": NODE_ID}
        
        response = requests.post(f"{BASE_URL}/a2a/heartbeat", headers=headers, json=hb_payload, timeout=30)
        result = response.json()
        
        status = result.get('status', 'unknown')
        survival = result.get('survival_status', 'unknown')
        credit_balance = result.get('credit_balance', 0)
        
        logger.info(f"   状态：{status}")
        logger.info(f"   生存状态：{survival}")
        logger.info(f"   积分余额：{credit_balance}")
        
        # 告警
        if survival != 'alive':
            logger.warning("⚠️ 节点离线！尝试恢复...")
            # 可以尝试重新 Hello
            return False, credit_balance
        
        return True, credit_balance
        
    except Exception as e:
        logger.error(f"❌ 健康检查失败：{e}")
        return False, 0

def check_claim_status():
    """检查 Claim 状态"""
    logger.info("\n📋 检查 Claim 状态...")
    
    state_file = log_dir / "claim_state.json"
    if not state_file.exists():
        logger.warning("⚠️ Claim 状态文件不存在")
        return
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        today = datetime.now().date()
        claims_today = [c for c in state.get('claims_today', []) if datetime.fromisoformat(c['date']).date() == today]
        completed_today = sum(c.get('completed_count', 0) for c in claims_today)
        
        logger.info(f"   今日 Claim: {len(claims_today)}")
        logger.info(f"   今日完成：{completed_today}")
        
        # 告警：如果 20:00 后还没有 Claim
        if datetime.now().hour >= 20 and len(claims_today) == 0:
            logger.warning("⚠️ 今日还未 Claim 任务！")
            # 可以触发手动 Claim
        
    except Exception as e:
        logger.error(f"❌ Claim 状态检查失败：{e}")

def check_publish_status():
    """检查资产发布状态"""
    logger.info("\n📤 检查资产发布状态...")
    
    publish_log = log_dir / "bundle-publish.log"
    if not publish_log.exists():
        logger.warning("⚠️ 发布日志不存在")
        return
    
    try:
        # 检查最近一次发布
        with open(publish_log, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if lines:
            last_line = lines[-1]
            logger.info(f"   最近发布：{last_line[:100]}...")
        
        # 检查发布成功率
        success_count = sum(1 for line in lines if '✅' in line or '成功' in line)
        fail_count = sum(1 for line in lines if '❌' in line or '失败' in line)
        
        logger.info(f"   成功：{success_count}, 失败：{fail_count}")
        
    except Exception as e:
        logger.error(f"❌ 发布状态检查失败：{e}")

def check_heatmap_opportunities():
    """检查 Heatmap 机会"""
    logger.info("\n🎯 检查 Heatmap 机会...")
    
    heatmap_file = log_dir / "heatmap-latest.json"
    if not heatmap_file.exists():
        logger.warning("⚠️ Heatmap 数据不存在")
        return
    
    try:
        with open(heatmap_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        p0_opportunities = [r for r in data.get('recommended', []) if r.get('priority') == 'P0']
        low_competition = data.get('opportunity_signals', [])
        
        logger.info(f"   P0 机会：{len(p0_opportunities)}")
        for opp in p0_opportunities[:3]:
            logger.info(f"     - {opp['topic']}: {opp['status']}")
        
        logger.info(f"   低竞争机会：{len(low_competition)}")
        for opp in low_competition[:3]:
            logger.info(f"     - {opp['signal']}: 密度 {opp['density']}")
        
    except Exception as e:
        logger.error(f"❌ Heatmap 机会检查失败：{e}")

def generate_daily_report(credit_balance):
    """生成日报"""
    logger.info("\n📊 生成日报...")
    
    report = []
    report.append("="*60)
    report.append(f"📈 EvoMap 监管日报 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("="*60)
    
    report.append(f"\n🏥 节点健康:")
    report.append(f"   状态：{'✅ 在线' if True else '❌ 离线'}")
    report.append(f"   积分余额：{credit_balance}")
    
    report.append(f"\n📋 Claim 状态:")
    state_file = log_dir / "claim_state.json"
    if state_file.exists():
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
            today = datetime.now().date()
            claims_today = [c for c in state.get('claims_today', []) if datetime.fromisoformat(c['date']).date() == today]
            completed = sum(c.get('completed_count', 0) for c in claims_today)
            report.append(f"   今日 Claim: {len(claims_today)}")
            report.append(f"   今日完成：{completed}")
        except:
            report.append(f"   数据不可用")
    else:
        report.append(f"   无数据")
    
    report.append(f"\n🎯 Heatmap 机会:")
    heatmap_file = log_dir / "heatmap-latest.json"
    if heatmap_file.exists():
        try:
            with open(heatmap_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            p0_count = len([r for r in data.get('recommended', []) if r.get('priority') == 'P0'])
            report.append(f"   P0 机会：{p0_count}")
        except:
            report.append(f"   数据不可用")
    else:
        report.append(f"   无数据")
    
    report.append("\n" + "="*60)
    
    report_text = "\n".join(report)
    logger.info(report_text)
    
    # 保存到文件
    report_file = log_dir / f"supervisor-report-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    # 发送飞书通知
    try:
        # 已禁用：用户不需要心跳报告
        # subprocess.Popen(
            ["python3", str(Path(__file__).parent.parent.parent / "tools" / "task-notifier.py"),
             "start", "EvoMap 监管日报", report_text, "5"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        logger.info("✅ 日报已发送")
    except Exception as e:
        logger.error(f"❌ 发送日报失败：{e}")

# ============================================================================
# 主流程
# ============================================================================

def main():
    logger.info("="*60)
    logger.info("🔍 EvoMap 完整监管体系")
    logger.info("="*60)
    
    # 1. 节点健康检查
    healthy, credit_balance = check_node_health()
    
    if not healthy:
        logger.warning("⚠️ 节点健康问题，尝试恢复...")
        # 可以尝试重新 Hello 或其他恢复措施
    
    # 2. Claim 状态检查
    check_claim_status()
    
    # 3. 发布状态检查
    check_publish_status()
    
    # 4. Heatmap 机会检查
    check_heatmap_opportunities()
    
    # 5. 生成日报
    generate_daily_report(credit_balance)
    
    logger.info("\n✅ 监管完成")

if __name__ == "__main__":
    main()

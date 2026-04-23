#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志数据分析与策略优化
功能：
1. 分析 Claim 成功率
2. 分析 Heatmap 准确率
3. 分析收益趋势
4. 优化 Claim 策略参数
5. 生成优化建议
"""

import json, logging
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# 分析模块
# ============================================================================

def analyze_claim_success_rate():
    """分析 Claim 成功率"""
    logger.info("\n📊 分析 Claim 成功率...")
    
    log_file = log_dir / "auto-claim-v6.log"
    if not log_file.exists():
        logger.warning("⚠️ Claim 日志不存在")
        return None
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_attempts = sum(1 for line in lines if 'Claim 任务' in line)
        successes = sum(1 for line in lines if '✅ Claim 成功' in line)
        failures_task_full = sum(1 for line in lines if '任务已满' in line)
        failures_already_joined = sum(1 for line in lines if '已加入' in line)
        
        success_rate = (successes / total_attempts * 100) if total_attempts > 0 else 0
        
        logger.info(f"   总尝试：{total_attempts}")
        logger.info(f"   成功：{successes} ({success_rate:.1f}%)")
        logger.info(f"   失败 - 任务已满：{failures_task_full}")
        logger.info(f"   失败 - 已加入：{failures_already_joined}")
        
        # 优化建议
        if success_rate < 50:
            logger.warning("⚠️ 成功率过低，建议调整策略")
            if failures_task_full > failures_already_joined:
                logger.info("   建议：更早 Claim，避免任务被抢完")
            else:
                logger.info("   建议：清理已加入任务列表")
        
        return {
            'total_attempts': total_attempts,
            'successes': successes,
            'success_rate': success_rate,
            'failures_task_full': failures_task_full,
            'failures_already_joined': failures_already_joined
        }
        
    except Exception as e:
        logger.error(f"❌ 分析失败：{e}")
        return None

def analyze_heatmap_accuracy():
    """分析 Heatmap 准确率"""
    logger.info("\n🎯 分析 Heatmap 准确率...")
    
    # 加载历史 Heatmap 数据
    history_file = log_dir / "heatmap-history.json"
    if not history_file.exists():
        logger.warning("⚠️ Heatmap 历史数据不足")
        return None
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        if len(history) < 2:
            logger.warning("⚠️ 历史数据不足")
            return None
        
        # 分析 Cold 信号变化
        cold_predictions = []
        for i, day in enumerate(history[1:], 1):
            prev_cold = history[i-1].get('cold_count', 0)
            curr_cold = day.get('cold_count', 0)
            if curr_cold > prev_cold:
                cold_predictions.append({
                    'date': day.get('timestamp', '')[:10],
                    'predicted': prev_cold,
                    'actual': curr_cold
                })
        
        logger.info(f"   历史天数：{len(history)}")
        logger.info(f"   Cold 信号发现：{len(cold_predictions)} 次")
        
        # 分析推荐机会准确性
        p0_opportunities = []
        for day in history:
            for rec in day.get('recommended', []):
                if rec.get('priority') == 'P0':
                    p0_opportunities.append(rec['topic'])
        
        from collections import Counter
        topic_counts = Counter(p0_opportunities)
        
        logger.info(f"   P0 机会话题：{len(topic_counts)} 个")
        for topic, count in topic_counts.most_common(5):
            logger.info(f"     - {topic}: {count} 次")
        
        return {
            'history_days': len(history),
            'cold_discoveries': len(cold_predictions),
            'p0_topics': dict(topic_counts)
        }
        
    except Exception as e:
        logger.error(f"❌ 分析失败：{e}")
        return None

def analyze_revenue_trend():
    """分析收益趋势"""
    logger.info("\n💰 分析收益趋势...")
    
    # 从 Claim 日志中提取收益数据
    log_file = log_dir / "auto-claim-v6.log"
    if not log_file.exists():
        logger.warning("⚠️ Claim 日志不存在")
        return None
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        daily_revenue = defaultdict(int)
        
        for line in lines:
            if 'Bounty:' in line:
                # 提取 Bounty 金额
                try:
                    bounty = int(line.split('Bounty:')[1].split()[0])
                    date = line.split(' - ')[0][:10]
                    daily_revenue[date] += bounty
                except:
                    pass
        
        if not daily_revenue:
            logger.warning("⚠️ 无收益数据")
            return None
        
        # 计算趋势
        dates = sorted(daily_revenue.keys())
        recent_7d = [daily_revenue[d] for d in dates[-7:]]
        recent_30d = [daily_revenue[d] for d in dates[-30:]] if len(dates) >= 30 else recent_7d
        
        avg_7d = sum(recent_7d) / len(recent_7d) if recent_7d else 0
        avg_30d = sum(recent_30d) / len(recent_30d) if recent_30d else 0
        
        logger.info(f"   有数据天数：{len(dates)}")
        logger.info(f"   最近 7 天平均：{avg_7d:.1f} 积分/天")
        logger.info(f"   最近 30 天平均：{avg_30d:.1f} 积分/天")
        
        trend = "📈 上升" if avg_7d > avg_30d else "📉 下降" if avg_7d < avg_30d else "➡️ 平稳"
        logger.info(f"   趋势：{trend}")
        
        return {
            'days_with_data': len(dates),
            'avg_7d': avg_7d,
            'avg_30d': avg_30d,
            'trend': 'up' if avg_7d > avg_30d else 'down' if avg_7d < avg_30d else 'stable',
            'daily_revenue': dict(daily_revenue)
        }
        
    except Exception as e:
        logger.error(f"❌ 分析失败：{e}")
        return None

def generate_optimization_suggestions(claim_stats, heatmap_stats, revenue_stats):
    """生成优化建议"""
    logger.info("\n💡 生成优化建议...")
    
    suggestions = []
    
    # Claim 成功率优化
    if claim_stats and claim_stats['success_rate'] < 50:
        suggestions.append({
            'category': 'Claim 策略',
            'priority': 'high',
            'issue': f"成功率过低 ({claim_stats['success_rate']:.1f}%)",
            'suggestion': "更早执行 Claim 任务，避免任务被抢完"
        })
    
    # Heatmap 机会优化
    if heatmap_stats and heatmap_stats.get('p0_topics'):
        top_topics = list(heatmap_stats['p0_topics'].keys())[:3]
        suggestions.append({
            'category': 'Heatmap 机会',
            'priority': 'medium',
            'issue': f"发现 {len(heatmap_stats['p0_topics'])} 个 P0 话题",
            'suggestion': f"优先发布内容：{', '.join(top_topics)}"
        })
    
    # 收益趋势优化
    if revenue_stats:
        if revenue_stats['trend'] == 'down':
            suggestions.append({
                'category': '收益趋势',
                'priority': 'high',
                'issue': f"收益下降 (7 天平均:{revenue_stats['avg_7d']:.1f} vs 30 天平均:{revenue_stats['avg_30d']:.1f})",
                'suggestion': "增加 Claim 频率，优化任务选择策略"
            })
        elif revenue_stats['avg_7d'] < 100:
            suggestions.append({
                'category': '收益提升',
                'priority': 'medium',
                'issue': f"收益偏低 ({revenue_stats['avg_7d']:.1f} 积分/天)",
                'suggestion': "关注 Heatmap P0 机会，提高任务完成质量"
            })
    
    # 输出建议
    logger.info(f"\n{'='*60}")
    logger.info(f"💡 优化建议")
    logger.info(f"{'='*60}")
    
    for i, sug in enumerate(suggestions, 1):
        logger.info(f"\n{i}. [{sug['priority'].upper()}] {sug['category']}")
        logger.info(f"   问题：{sug['issue']}")
        logger.info(f"   建议：{sug['suggestion']}")
    
    logger.info(f"\n{'='*60}")
    
    # 保存建议
    suggestions_file = log_dir / "optimization-suggestions.json"
    with open(suggestions_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'suggestions': suggestions
        }, f, ensure_ascii=False, indent=2)
    
    return suggestions

# ============================================================================
# 主流程
# ============================================================================

def main():
    logger.info("="*60)
    logger.info("📈 日志数据分析与策略优化")
    logger.info("="*60)
    
    # 1. Claim 成功率分析
    claim_stats = analyze_claim_success_rate()
    
    # 2. Heatmap 准确率分析
    heatmap_stats = analyze_heatmap_accuracy()
    
    # 3. 收益趋势分析
    revenue_stats = analyze_revenue_trend()
    
    # 4. 生成优化建议
    suggestions = generate_optimization_suggestions(claim_stats, heatmap_stats, revenue_stats)
    
    # 5. 保存分析结果
    analysis_result = {
        'timestamp': datetime.now().isoformat(),
        'claim_stats': claim_stats,
        'heatmap_stats': heatmap_stats,
        'revenue_stats': revenue_stats,
        'suggestions': suggestions
    }
    
    result_file = log_dir / "analysis-result.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n💾 分析结果已保存到 {result_file}")
    logger.info("\n✅ 分析完成")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 统计面板 - 积分/成功率/Claim 历史追踪

功能:
- 积分余额追踪
- Claim 成功率统计
- 历史记录分析
- 趋势可视化（文本）

使用:
    from stats_dashboard import StatsDashboard
    dashboard = StatsDashboard()
    dashboard.update_points(10.5)
    dashboard.record_claim(task_id, success=True, bounty=50)
    dashboard.print_report()
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class StatsDashboard:
    """EvoMap 统计面板"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "stats"
        self.data_dir.mkdir(exist_ok=True)
        
        # 数据文件
        self.points_file = self.data_dir / "points_history.jsonl"
        self.claims_file = self.data_dir / "claims_history.jsonl"
        self.summary_file = self.data_dir / "summary.json"
        
        # 加载现有数据
        self.summary = self._load_summary()
    
    def _load_summary(self) -> Dict:
        """加载汇总数据"""
        if self.summary_file.exists():
            with open(self.summary_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            'current_points': 10.5,  # 初始值
            'total_claims': 0,
            'successful_claims': 0,
            'failed_claims': 0,
            'total_bounty_earned': 0,
            'first_claim_date': None,
            'last_claim_date': None
        }
    
    def update_points(self, points: float, source: str = 'manual'):
        """
        更新积分余额
        
        Args:
            points: 当前积分
            source: 来源 (manual/api/claim等)
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'points': points,
            'source': source
        }
        
        # 记录到历史
        with open(self.points_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        # 更新汇总
        self.summary['current_points'] = points
        self._save_summary()
        
        print(f"✅ 积分更新：{points} (来源：{source})")
    
    def record_claim(self, task_id: str, success: bool, bounty: int = 0, 
                     error: str = None, task_type: str = 'unknown'):
        """
        记录 Claim 操作
        
        Args:
            task_id: 任务 ID
            success: 是否成功
            bounty: 积分奖励
            error: 错误信息
            task_type: 任务类型
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'task_id': task_id,
            'success': success,
            'bounty': bounty,
            'error': error,
            'task_type': task_type
        }
        
        # 记录到历史
        with open(self.claims_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        # 更新汇总
        self.summary['total_claims'] += 1
        if success:
            self.summary['successful_claims'] += 1
            self.summary['total_bounty_earned'] += bounty
        else:
            self.summary['failed_claims'] += 1
        
        if not self.summary['first_claim_date']:
            self.summary['first_claim_date'] = entry['timestamp']
        self.summary['last_claim_date'] = entry['timestamp']
        
        self._save_summary()
        
        status = '✅' if success else '❌'
        print(f"{status} Claim 记录：{'成功' if success else '失败'} (+{bounty}积分)")
    
    def _save_summary(self):
        """保存汇总数据"""
        with open(self.summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.summary, f, ensure_ascii=False, indent=2)
    
    def get_success_rate(self) -> float:
        """获取成功率"""
        total = self.summary['total_claims']
        if total == 0:
            return 0.0
        return self.summary['successful_claims'] / total * 100
    
    def get_points_trend(self, days: int = 7) -> List[Dict]:
        """
        获取积分趋势
        
        Args:
            days: 天数
        
        Returns:
            趋势数据列表
        """
        trend = []
        
        if not self.points_file.exists():
            return trend
        
        with open(self.points_file, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line.strip())
                trend.append(entry)
        
        # 只保留最近 N 天（Python 3.6 兼容）
        cutoff = datetime.now().timestamp() - (days * 24 * 3600)
        filtered = []
        for e in trend:
            try:
                ts = datetime.strptime(e['timestamp'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
                if ts.timestamp() > cutoff:
                    filtered.append(e)
            except:
                filtered.append(e)  # 解析失败保留
        
        return filtered[-10:]  # 最多返回 10 个点
    
    def get_claim_history(self, limit: int = 10) -> List[Dict]:
        """
        获取 Claim 历史
        
        Args:
            limit: 记录数量
        
        Returns:
            历史记录列表
        """
        history = []
        
        if not self.claims_file.exists():
            return history
        
        with open(self.claims_file, 'r', encoding='utf-8') as f:
            for line in f:
                history.append(json.loads(line.strip()))
        
        # 倒序（最新的在前）
        history.reverse()
        return history[:limit]
    
    def print_report(self):
        """打印统计报告"""
        print("\n" + "=" * 70)
        print("📊 EvoMap 统计面板")
        print("=" * 70)
        
        # 核心指标
        print("\n💎 核心指标:")
        print(f"   当前积分：{self.summary['current_points']:.1f}")
        print(f"   总 Claim 数：{self.summary['total_claims']}")
        print(f"   成功率：{self.get_success_rate():.1f}%")
        print(f"   累计获得：{self.summary['total_bounty_earned']}积分")
        
        # 成功/失败对比
        print(f"\n   ✅ 成功：{self.summary['successful_claims']}")
        print(f"   ❌ 失败：{self.summary['failed_claims']}")
        
        # 时间信息
        if self.summary['first_claim_date']:
            # Python 3.6 兼容：用 strptime 代替 fromisoformat
            first_str = self.summary['first_claim_date'].replace('Z', '+0000').split('.')[0]
            last_str = self.summary['last_claim_date'].replace('Z', '+0000').split('.')[0]
            try:
                first = datetime.strptime(first_str, '%Y-%m-%dT%H:%M:%S')
                last = datetime.strptime(last_str, '%Y-%m-%dT%H:%M:%S')
            except:
                first = last = datetime.now()
            print(f"\n📅 时间跨度:")
            print(f"   首次 Claim: {first.strftime('%Y-%m-%d %H:%M')}")
            print(f"   最近 Claim: {last.strftime('%Y-%m-%d %H:%M')}")
        
        # 最近 Claim 历史
        print("\n📋 最近 Claim 历史:")
        history = self.get_claim_history(limit=5)
        if history:
            for entry in history:
                status = '✅' if entry['success'] else '❌'
                bounty = f"+{entry['bounty']}" if entry['success'] else ''
                print(f"   {status} {entry['task_id'][:20]}... {bounty}")
                if entry.get('error'):
                    print(f"      错误：{entry['error'][:50]}")
        else:
            print("   暂无记录")
        
        # 积分趋势
        print("\n📈 积分趋势:")
        trend = self.get_points_trend(days=7)
        if trend:
            for entry in trend[-5:]:
                try:
                    ts = datetime.strptime(entry['timestamp'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
                except:
                    ts = datetime.now()
                print(f"   {ts.strftime('%m-%d %H:%M')}: {entry['points']:.1f} ({entry['source']})")
        else:
            print("   暂无趋势数据")
        
        # 健康度评估
        print("\n🏥 健康度评估:")
        points = self.summary['current_points']
        if points >= 100:
            print("   ✅ 优秀 - 积分充足")
        elif points >= 50:
            print("   ⚠️  良好 - 积分健康")
        elif points >= 20:
            print("   ⚠️  警戒 - 积分偏低")
        else:
            print("   🔴 危险 - 积分不足，需尽快赚积分")
        
        print("\n" + "=" * 70)
    
    def export_report(self) -> str:
        """
        导出完整报告
        
        Returns:
            报告文件路径
        """
        report = {
            'summary': self.summary,
            'success_rate': self.get_success_rate(),
            'points_trend': self.get_points_trend(days=30),
            'recent_claims': self.get_claim_history(limit=20),
            'exported_at': datetime.now().isoformat()
        }
        
        output_file = self.data_dir / f"report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return str(output_file)


def main():
    """主函数 - 测试统计面板"""
    dashboard = StatsDashboard()
    
    # 打印报告
    dashboard.print_report()
    
    # 导出报告
    report_file = dashboard.export_report()
    print(f"\n💾 完整报告已导出：{report_file}")


if __name__ == "__main__":
    main()

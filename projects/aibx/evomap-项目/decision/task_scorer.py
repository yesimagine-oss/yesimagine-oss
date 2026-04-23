#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 決策引擎 v2.0 - 智能任務評分模型

功能:
- 4 維度評分（Bounty 40% + Success 30% + Competition 20% + Freshness 10%）
- 批量評分和排名
- 智能任務推薦
- 自動 Claim（可選）

使用:
    python3 task_scorer.py --test
    python3 task_scorer.py --score --tasks task1,task2,task3

作者：RedOpenClaw
版本：v2.0
創建：2026-03-23
"""

import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from pathlib import Path

# 導入 Evolver 工具
lib_path = Path(__file__).parent.parent / 'lib'
sys.path.insert(0, str(lib_path))

try:
    from evolver_tools import EvolverTools
except ImportError:
    print("⚠️  警告：evolver_tools 未找到，使用模擬模式")
    EvolverTools = None


@dataclass
class Task:
    """任務數據結構"""
    id: str
    title: str
    bounty: int
    task_type: str
    claimers: int
    published_at: datetime
    signals: List[str] = field(default_factory=list)
    difficulty: str = "medium"  # easy/medium/hard
    deadline: Optional[datetime] = None


@dataclass
class ScoredTask(Task):
    """評分後任務"""
    total_score: float = 0.0
    bounty_score: float = 0.0
    success_score: float = 0.0
    competition_score: float = 0.0
    freshness_score: float = 0.0
    rank: int = 0


class TaskScorer:
    """任務評分器"""
    
    def __init__(self, config: Dict = None):
        """
        初始化評分器
        
        Args:
            config: 配置字典
        """
        self.config = config or self._default_config()
        self.tools = EvolverTools() if EvolverTools else None
        self.history = self._load_history()
    
    def _default_config(self) -> Dict:
        """默認配置"""
        return {
            'weights': {
                'bounty': 0.4,
                'success_rate': 0.3,
                'competition': 0.2,
                'freshness': 0.1
            },
            'thresholds': {
                'min_bounty': 50,
                'max_bounty': 2000,
                'min_score': 60,
                'auto_claim_score': 80
            },
            'preferences': {
                'preferred_types': ['technical', 'bounty', 'research'],
                'preferred_signals': ['python', 'api', 'automation', 'data_analysis'],
                'avoid_signals': ['design', 'writing']
            },
            'bonuses': {
                'signal_match': 0.05,
                'urgent_deadline': 0.1,
                'hard_difficulty': 0.1,
                'early_claim': 0.2
            }
        }
    
    def score_task(self, task: Task) -> ScoredTask:
        """
        對單一任務評分
        
        Args:
            task: 任務對象
        
        Returns:
            評分後任務對象
        """
        # 1. Bounty 評分
        bounty_score = self._score_bounty(task.bounty)
        
        # 2. Success Rate 評分
        success_score = self._score_success_rate(task.task_type)
        
        # 3. Competition 評分
        competition_score = self._score_competition(task.claimers)
        
        # 4. Freshness 評分
        freshness_score = self._score_freshness(task.published_at)
        
        # 5. 加權總分
        weights = self.config['weights']
        total_score = (
            bounty_score * weights['bounty'] +
            success_score * weights['success_rate'] +
            competition_score * weights['competition'] +
            freshness_score * weights['freshness']
        )
        
        # 6. 應用額外加成
        total_score = self._apply_bonuses(total_score, task)
        
        # 創建評分後任務
        scored_task = ScoredTask(
            id=task.id,
            title=task.title,
            bounty=task.bounty,
            task_type=task.task_type,
            claimers=task.claimers,
            published_at=task.published_at,
            signals=task.signals,
            difficulty=task.difficulty,
            deadline=task.deadline,
            total_score=total_score,
            bounty_score=bounty_score,
            success_score=success_score,
            competition_score=competition_score,
            freshness_score=freshness_score
        )
        
        return scored_task
    
    def _score_bounty(self, bounty: int) -> float:
        """Bounty 評分（0-100）"""
        min_bounty = self.config['thresholds']['min_bounty']
        max_bounty = self.config['thresholds']['max_bounty']
        
        if bounty < min_bounty:
            return 0
        
        # 線性歸一化
        normalized = min(100, (bounty - min_bounty) / (max_bounty - min_bounty) * 100)
        
        # 高 bounty 加成
        if bounty >= 1000:
            normalized *= 1.1
        
        return min(100, normalized)
    
    def _score_success_rate(self, task_type: str) -> float:
        """成功率評分（0-100）"""
        # 從歷史數據獲取個人成功率
        personal_rate = self.history.get('overall_success_rate', 0.95)
        
        # 基礎分
        base_score = personal_rate * 100
        
        # 類型加成
        if task_type in self.config['preferences']['preferred_types']:
            base_score *= 1.1
        
        return min(100, base_score)
    
    def _score_competition(self, claimers: int) -> float:
        """競爭程度評分（0-100，反向）"""
        max_claimers = 20
        
        if claimers == 0:
            return 100
        
        # 反向線性評分
        score = max(0, 100 - (claimers / max_claimers * 100))
        
        # 早期加成
        if claimers <= 3:
            score *= 1.2
        
        return min(100, score)
    
    def _score_freshness(self, published_at: datetime) -> float:
        """新鮮度評分（0-100）"""
        now = datetime.now()
        age_hours = (now - published_at).total_seconds() / 3600
        
        if age_hours < 1:
            return 100
        elif age_hours < 6:
            return 90
        elif age_hours < 24:
            return 70
        elif age_hours < 72:
            return 50
        else:
            return max(0, 100 - age_hours)
    
    def _apply_bonuses(self, base_score: float, task: Task) -> float:
        """應用額外加成"""
        multiplier = 1.0
        bonuses = self.config['bonuses']
        
        # 信號匹配加成
        for signal in task.signals:
            if signal in self.config['preferences']['preferred_signals']:
                multiplier += bonuses['signal_match']
        
        # 截止日期加成
        if task.deadline:
            hours_left = (task.deadline - datetime.now()).total_seconds() / 3600
            if hours_left < 24:
                multiplier += bonuses['urgent_deadline']
        
        # 難度加成
        if task.difficulty == 'hard':
            multiplier += bonuses['hard_difficulty']
        
        return min(100, base_score * multiplier)
    
    def score_and_rank(self, tasks: List[Task]) -> List[ScoredTask]:
        """
        批量評分並排名
        
        Args:
            tasks: 任務列表
        
        Returns:
            評分後任務列表（已排序）
        """
        scored_tasks = [self.score_task(task) for task in tasks]
        
        # 按總分排序
        scored_tasks.sort(key=lambda t: t.total_score, reverse=True)
        
        # 設置排名
        for i, task in enumerate(scored_tasks):
            task.rank = i + 1
        
        return scored_tasks
    
    def get_top_tasks(self, tasks: List[Task], top_n: int = 5) -> List[ScoredTask]:
        """獲取前 N 個推薦任務"""
        scored_tasks = self.score_and_rank(tasks)
        return scored_tasks[:top_n]
    
    def _load_history(self) -> Dict:
        """加載歷史數據"""
        # 從日誌文件加載
        log_dir = Path(__file__).parent.parent / 'logs'
        history = {
            'overall_success_rate': 0.95,
            'total_tasks': 400,
            'successful_tasks': 380
        }
        
        # 可以從實際日誌中計算
        # 此處使用默認值
        
        return history
    
    def fetch_and_score(self, limit: int = 10) -> List[ScoredTask]:
        """
        獲取任務並評分
        
        Args:
            limit: 任務數量
        
        Returns:
            評分後任務列表
        """
        # 從 API 獲取任務
        result = self.tools.fetch_tasks(limit=limit * 2)
        
        if not result.get('success'):
            print(f"❌ 獲取任務失敗：{result.get('error')}")
            return []
        
        # 轉換為 Task 對象
        tasks = []
        for task_data in result.get('tasks', []):
            task = Task(
                id=task_data.get('id'),
                title=task_data.get('title', 'Unknown'),
                bounty=task_data.get('bounty', 0),
                task_type=task_data.get('type', 'any'),
                claimers=task_data.get('claimers', 0),
                published_at=datetime.now(),  # 實際應從 API 獲取
                signals=task_data.get('signals', []),
                difficulty=task_data.get('difficulty', 'medium')
            )
            tasks.append(task)
        
        # 評分並排名
        scored_tasks = self.score_and_rank(tasks)
        
        return scored_tasks
    
    def print_recommendations(self, scored_tasks: List[ScoredTask]):
        """打印推薦任務"""
        if not scored_tasks:
            print("❌ 沒有推薦任務")
            return
        
        print("\n🎯 推薦任務 TOP 5:\n")
        print("=" * 80)
        
        for task in scored_tasks[:5]:
            print(f"#{task.rank} {task.title}")
            print(f"   Bounty: {task.bounty}分 | 評分：{task.total_score:.1f}")
            print(f"   競爭：{task.claimers}人 | 類型：{task.task_type}")
            print(f"   信號：{', '.join(task.signals[:3]) if task.signals else 'N/A'}")
            print(f"   細項：Bounty={task.bounty_score:.1f}, 成功率={task.success_score:.1f}, "
                  f"競爭={task.competition_score:.1f}, 新鮮度={task.freshness_score:.1f}")
            print()
        
        print("=" * 80)


def test_scorer():
    """測試評分器"""
    print("🧪 測試 AI 決策引擎 v2.0\n")
    
    scorer = TaskScorer()
    
    # 創建測試任務
    test_tasks = [
        Task(
            id="task_001",
            title="Python API 自動化腳本",
            bounty=500,
            task_type="technical",
            claimers=2,
            published_at=datetime.now() - timedelta(hours=2),
            signals=["python", "api", "automation"],
            difficulty="medium"
        ),
        Task(
            id="task_002",
            title="數據分析儀表板",
            bounty=800,
            task_type="research",
            claimers=5,
            published_at=datetime.now() - timedelta(hours=6),
            signals=["data_analysis", "python", "visualization"],
            difficulty="hard"
        ),
        Task(
            id="task_003",
            title="簡單的網頁設計",
            bounty=100,
            task_type="design",
            claimers=15,
            published_at=datetime.now() - timedelta(days=2),
            signals=["design", "css", "html"],
            difficulty="easy"
        ),
    ]
    
    # 評分
    scored_tasks = scorer.score_and_rank(test_tasks)
    
    # 打印結果
    scorer.print_recommendations(scored_tasks)
    
    # 驗證評分邏輯
    print("\n✅ 評分邏輯驗證:")
    best_task = scored_tasks[0]
    print(f"   最佳任務：{best_task.title}")
    print(f"   總分：{best_task.total_score:.1f}")
    print(f"   Bounty 評分：{best_task.bounty_score:.1f}")
    print(f"   成功率評分：{best_task.success_score:.1f}")
    print(f"   競爭評分：{best_task.competition_score:.1f}")
    print(f"   新鮮度評分：{best_task.freshness_score:.1f}")
    
    print("\n✅ 測試完成")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 決策引擎 v2.0")
    parser.add_argument('--test', action='store_true', help='運行測試')
    parser.add_argument('--fetch', type=int, help='獲取並評分任務')
    parser.add_argument('--auto-claim', action='store_true', help='自動 Claim 最佳任務')
    
    args = parser.parse_args()
    
    if args.test:
        test_scorer()
    
    elif args.fetch:
        scorer = TaskScorer()
        scored_tasks = scorer.fetch_and_score(limit=args.fetch)
        scorer.print_recommendations(scored_tasks)
        
        if args.auto_claim and scored_tasks:
            best_task = scored_tasks[0]
            if best_task.total_score >= scorer.config['thresholds']['auto_claim_score']:
                print(f"\n🚀 自動 Claim: {best_task.title}")
                result = scorer.tools.claim_task(best_task.id)
                if result['success']:
                    print(f"✅ Claim 成功！")
                else:
                    print(f"❌ Claim 失敗：{result.get('error')}")
    
    else:
        parser.print_help()

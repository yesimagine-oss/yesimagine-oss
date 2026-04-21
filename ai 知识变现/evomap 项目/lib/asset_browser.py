#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 资产浏览器 - 定期 fetch 热门 Gene/Capsule

功能:
- 获取热门/推荐资产列表
- 分析资产模式（category/strategy 等）
- 记录到本地知识库
- 提学习建议

使用:
    from asset_browser import AssetBrowser
    browser = AssetBrowser()
    browser.fetch_promoted_assets(limit=20)
    browser.analyze_patterns()
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, str(Path(__file__).parent))
from evolver_tools import EvolverTools


class AssetBrowser:
    """EvoMap 资产浏览器"""
    
    def __init__(self):
        self.tools = EvolverTools()
        self.log_dir = Path(__file__).parent / "logs" / "assets"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 分析结果存储
        self.analysis_file = self.log_dir / "asset_analysis.jsonl"
        self.patterns_file = self.log_dir / "patterns.json"
    
    def fetch_promoted_assets(self, limit: int = 20) -> Dict:
        """
        获取热门/推荐资产
        
        Args:
            limit: 资产数量
        
        Returns:
            资产列表 + 分析结果
        """
        print(f'📚 获取热门资产 (limit={limit})...')
        
        # 确保已认证
        hello = self.tools.hello()
        if not hello.get('success'):
            return {'success': False, 'error': 'Authentication failed'}
        
        # 使用 fetch 获取推荐资产
        # 注意：当前 API 可能不直接支持获取 promoted assets
        # 这里用 fetch_tasks 间接获取活跃资产信息
        
        result = self.tools.fetch_tasks(limit=limit)
        
        if not result.get('success'):
            print(f'⚠️ 获取失败：{result}')
            return result
        
        assets = result.get('tasks', [])
        print(f'✅ 获取到 {len(assets)} 个资产')
        
        # 记录到日志
        self._log_assets(assets)
        
        # 分析模式
        patterns = self._analyze_patterns(assets)
        
        return {
            'success': True,
            'count': len(assets),
            'assets': assets,
            'patterns': patterns,
            'timestamp': datetime.now().isoformat()
        }
    
    def _log_assets(self, assets: List[Dict]):
        """记录资产到日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'count': len(assets),
            'assets': assets
        }
        
        log_file = self.log_dir / f"assets-{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, ensure_ascii=False, indent=2)
    
    def _analyze_patterns(self, assets: List[Dict]) -> Dict:
        """
        分析资产模式
        
        分析维度:
        - category 分布
        - strategy 长度/模式
        - signals_match 关键词
        - bounty 分布
        """
        if not assets:
            return {}
        
        patterns = {
            'categories': {},
            'avg_bounty': 0,
            'common_signals': {},
            'strategy_lengths': []
        }
        
        total_bounty = 0
        
        for asset in assets:
            # Category 统计
            category = asset.get('category', 'unknown')
            patterns['categories'][category] = patterns['categories'].get(category, 0) + 1
            
            # Bounty 统计
            bounty = asset.get('bounty', 0)
            total_bounty += bounty
            
            # Signals 统计
            signals = asset.get('signals', [])
            for signal in signals:
                patterns['common_signals'][signal] = patterns['common_signals'].get(signal, 0) + 1
            
            # Strategy 长度
            strategy = asset.get('strategy', [])
            patterns['strategy_lengths'].append(len(strategy))
        
        # 计算平均值
        patterns['avg_bounty'] = total_bounty / len(assets) if assets else 0
        patterns['avg_strategy_length'] = (
            sum(patterns['strategy_lengths']) / len(patterns['strategy_lengths'])
            if patterns['strategy_lengths'] else 0
        )
        
        # 排序热门 signals
        sorted_signals = sorted(
            patterns['common_signals'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        patterns['top_signals'] = dict(sorted_signals)
        
        # 保存模式
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, ensure_ascii=False, indent=2)
        
        return patterns
    
    def get_learning_suggestions(self, patterns: Dict) -> List[str]:
        """
        根据模式分析给出学习建议
        
        Returns:
            建议列表
        """
        suggestions = []
        
        # 基于 category 分布
        categories = patterns.get('categories', {})
        if categories:
            top_category = max(categories.items(), key=lambda x: x[1])
            suggestions.append(
                f"📊 热门领域：{top_category[0]} ({top_category[1]}个资产)\n"
                f"   建议：关注此领域的 Gene 设计模式"
            )
        
        # 基于热门 signals
        top_signals = patterns.get('top_signals', {})
        if top_signals:
            signals_list = list(top_signals.keys())[:5]
            suggestions.append(
                f"🎯 热门信号：{', '.join(signals_list)}\n"
                f"   建议：在 Gene 中使用这些 signals_match"
            )
        
        # 基于平均 strategy 长度
        avg_length = patterns.get('avg_strategy_length', 0)
        if avg_length > 0:
            suggestions.append(
                f"📝 平均 strategy 步骤：{avg_length:.1f}步\n"
                f"   建议：Gene.strategy 保持{int(avg_length)}±2 个步骤"
            )
        
        return suggestions
    
    def print_report(self, result: Dict):
        """打印资产分析报告"""
        if not result.get('success'):
            print(f"❌ 获取失败：{result.get('error')}")
            return
        
        print("\n" + "=" * 70)
        print("📊 EvoMap 资产分析报告")
        print("=" * 70)
        
        patterns = result.get('patterns', {})
        
        # Category 分布
        print("\n📁 Category 分布:")
        for cat, count in sorted(patterns.get('categories', {}).items(), 
                                  key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {cat}: {count}个")
        
        # 热门 Signals
        print("\n🎯 热门 Signals:")
        for signal, count in list(patterns.get('top_signals', {}).items())[:5]:
            print(f"   {signal}: {count}次")
        
        # 统计数据
        print("\n📈 统计数据:")
        print(f"   平均 Bounty: {patterns.get('avg_bounty', 0):.1f}")
        print(f"   平均 Strategy 步骤：{patterns.get('avg_strategy_length', 0):.1f}")
        
        # 学习建议
        print("\n💡 学习建议:")
        suggestions = self.get_learning_suggestions(patterns)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n   {i}. {suggestion}")
        
        print("\n" + "=" * 70)


def main():
    """主函数 - 测试资产浏览器"""
    browser = AssetBrowser()
    
    # 获取并分析资产
    result = browser.fetch_promoted_assets(limit=20)
    
    # 打印报告
    browser.print_report(result)
    
    # 保存结果
    output_file = browser.log_dir / f"report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 报告已保存：{output_file}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 学习循环 - 分析失败→学习→改进→验证

功能:
- 分析 Claim 失败原因
- 提取教训
- 生成改进建议
- 验证改进效果
- 记录到知识库

使用:
    from learning_loop import LearningLoop
    loop = LearningLoop()
    loop.analyze_failure(task_id, error='server_busy')
    loop.generate_improvements()
    loop.verify_improvement('claim_with_retry')
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from stats_dashboard import StatsDashboard


class LearningLoop:
    """EvoMap 学习循环"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "learnings"
        self.data_dir.mkdir(exist_ok=True)
        
        # 数据文件
        self.failures_file = self.data_dir / "failures.jsonl"
        self.improvements_file = self.data_dir / "improvements.jsonl"
        self.lessons_file = self.data_dir / "lessons_learned.json"
        
        # 统计面板
        self.stats = StatsDashboard()
        
        # 加载已学教训
        self.lessons = self._load_lessons()
    
    def _load_lessons(self) -> Dict:
        """加载已学教训"""
        if self.lessons_file.exists():
            with open(self.lessons_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            'failures_analyzed': 0,
            'improvements_made': 0,
            'lessons': []
        }
    
    def analyze_failure(self, task_id: str, error: str, 
                       context: Dict = None) -> Dict:
        """
        分析失败原因
        
        Args:
            task_id: 任务 ID
            error: 错误信息
            context: 上下文信息（时间/任务类型等）
        
        Returns:
            分析结果
        """
        print(f"🔍 分析失败：{task_id[:20]}...")
        
        # 错误分类
        error_type = self._classify_error(error)
        
        # 根因分析
        root_cause = self._analyze_root_cause(error_type, context)
        
        # 生成教训
        lesson = self._generate_lesson(error_type, root_cause)
        
        # 记录失败
        failure_entry = {
            'timestamp': datetime.now().isoformat(),
            'task_id': task_id,
            'error': error,
            'error_type': error_type,
            'root_cause': root_cause,
            'lesson': lesson,
            'context': context or {}
        }
        
        with open(self.failures_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(failure_entry, ensure_ascii=False) + '\n')
        
        # 更新教训
        self.lessons['failures_analyzed'] += 1
        self.lessons['lessons'].append({
            'date': datetime.now().isoformat(),
            'error_type': error_type,
            'lesson': lesson
        })
        self._save_lessons()
        
        print(f"✅ 分析完成：{error_type}")
        print(f"   根因：{root_cause}")
        print(f"   教训：{lesson}")
        
        return failure_entry
    
    def _classify_error(self, error: str) -> str:
        """
        错误分类
        
        分类体系:
        - network_error: 网络问题（503/timeout）
        - validation_error: 验证失败（schema 不匹配）
        - auth_error: 认证失败
        - resource_error: 资源不足（积分不够）
        - logic_error: 逻辑错误（任务已 Claim 等）
        - unknown: 未知错误
        """
        error_lower = error.lower()
        
        if '503' in error_lower or 'timeout' in error_lower or 'busy' in error_lower:
            return 'network_error'
        elif 'validation' in error_lower or 'schema' in error_lower:
            return 'validation_error'
        elif 'auth' in error_lower or 'unauthorized' in error_lower or '401' in error_lower:
            return 'auth_error'
        elif 'points' in error_lower or 'credits' in error_lower or 'balance' in error_lower:
            return 'resource_error'
        elif 'already' in error_lower or 'not found' in error_lower or '404' in error_lower:
            return 'logic_error'
        else:
            return 'unknown'
    
    def _analyze_root_cause(self, error_type: str, context: Dict = None) -> str:
        """分析根因"""
        root_causes = {
            'network_error': (
                '服务器繁忙或网络不稳定\n'
                '可能原因：免费层级限流/高峰期拥堵/代理问题'
            ),
            'validation_error': (
                '数据格式不符合 API 要求\n'
                '可能原因：schema 版本不匹配/字段缺失/格式错误'
            ),
            'auth_error': (
                '认证失败\n'
                '可能原因：node_secret 错误/认证过期/节点被封'
            ),
            'resource_error': (
                '资源不足\n'
                '可能原因：积分余额不足/碳税过高/配额用尽'
            ),
            'logic_error': (
                '业务逻辑错误\n'
                '可能原因：任务已被 Claim/任务已过期/权限不足'
            ),
            'unknown': (
                '未知错误\n'
                '需要进一步调查错误详情'
            )
        }
        
        return root_causes.get(error_type, root_causes['unknown'])
    
    def _generate_lesson(self, error_type: str, root_cause: str) -> str:
        """生成教训"""
        lessons = {
            'network_error': (
                '1. 实现重试机制（指数退避）\n'
                '2. 错峰操作（避开高峰期）\n'
                '3. 监控服务器状态\n'
                '4. 考虑升级付费层级'
            ),
            'validation_error': (
                '1. 严格遵循官方 schema\n'
                '2. 发布前本地验证\n'
                '3. 参考成功案例格式\n'
                '4. 记录验证错误日志'
            ),
            'auth_error': (
                '1. 定期刷新认证（30 分钟）\n'
                '2. 安全存储 node_secret\n'
                '3. 监控认证状态\n'
                '4. 准备备用节点'
            ),
            'resource_error': (
                '1. 监控积分余额（<50 预警）\n'
                '2. 优先高价值任务\n'
                '3. 发布资产赚积分\n'
                '4. 优化碳税策略'
            ),
            'logic_error': (
                '1. Claim 前检查任务状态\n'
                '2. 实现任务去重\n'
                '3. 及时处理已 Claim 任务\n'
                '4. 记录任务生命周期'
            ),
            'unknown': (
                '1. 记录完整错误信息\n'
                '2. 查阅官方文档\n'
                '3. 参考社区案例\n'
                '4. 提交问题反馈'
            )
        }
        
        return lessons.get(error_type, lessons['unknown'])
    
    def generate_improvements(self) -> List[Dict]:
        """
        生成改进建议
        
        Returns:
            改进建议列表
        """
        improvements = []
        
        # 分析失败模式
        failure_patterns = self._analyze_failure_patterns()
        
        for error_type, count in failure_patterns.items():
            if count >= 1:  # 至少发生 1 次就建议改进
                improvement = {
                    'error_type': error_type,
                    'occurrences': count,
                    'priority': 'high' if count >= 3 else 'medium',
                    'suggestions': self._get_improvement_suggestions(error_type)
                }
                improvements.append(improvement)
        
        # 保存改进建议
        for imp in improvements:
            with open(self.improvements_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(imp, ensure_ascii=False) + '\n')
        
        self.lessons['improvements_made'] += len(improvements)
        self._save_lessons()
        
        return improvements
    
    def _analyze_failure_patterns(self) -> Dict[str, int]:
        """分析失败模式"""
        patterns = {}
        
        if not self.failures_file.exists():
            return patterns
        
        with open(self.failures_file, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line.strip())
                error_type = entry.get('error_type', 'unknown')
                patterns[error_type] = patterns.get(error_type, 0) + 1
        
        return patterns
    
    def _get_improvement_suggestions(self, error_type: str) -> List[str]:
        """获取改进建议"""
        suggestions_map = {
            'network_error': [
                '实现 claim_with_retry() 函数（指数退避）',
                '添加服务器状态监控',
                '配置错峰检查时间（凌晨/清晨）',
                '研究付费层级优势'
            ],
            'validation_error': [
                '创建 schema 验证工具',
                '收集官方成功案例模板',
                '实现发布前自动验证',
                '建立验证错误知识库'
            ],
            'auth_error': [
                '实现自动认证刷新（30 分钟）',
                '添加认证状态监控',
                '安全存储 node_secret',
                '准备备用认证方案'
            ],
            'resource_error': [
                '实现积分预警（<50 通知）',
                '优化任务选择策略（高 Bounty）',
                '准备资产发布方案',
                '研究碳税优化策略'
            ],
            'logic_error': [
                '实现任务状态检查',
                '添加 Claim 去重逻辑',
                '建立任务生命周期追踪',
                '优化任务筛选条件'
            ]
        }
        
        return suggestions_map.get(error_type, ['调查错误原因', '查阅文档', '参考案例'])
    
    def verify_improvement(self, improvement_name: str, 
                          success: bool, metrics: Dict = None) -> Dict:
        """
        验证改进效果
        
        Args:
            improvement_name: 改进名称
            success: 是否成功
            metrics: 指标数据
        
        Returns:
            验证结果
        """
        result = {
            'timestamp': datetime.now().isoformat(),
            'improvement': improvement_name,
            'success': success,
            'metrics': metrics or {}
        }
        
        # 记录验证结果
        improvements_log = self.data_dir / "improvements_verified.jsonl"
        with open(improvements_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
        
        status = '✅' if success else '❌'
        print(f"{status} 改进验证：{improvement_name} - {'成功' if success else '失败'}")
        
        return result
    
    def print_learning_report(self):
        """打印学习报告"""
        print("\n" + "=" * 70)
        print("🧠 EvoMap 学习循环报告")
        print("=" * 70)
        
        # 总体统计
        print(f"\n📊 总体统计:")
        print(f"   失败分析：{self.lessons['failures_analyzed']}次")
        print(f"   改进建议：{self.lessons['improvements_made']}条")
        print(f"   已学教训：{len(self.lessons['lessons'])}条")
        
        # 失败模式
        print(f"\n🔍 失败模式分析:")
        patterns = self._analyze_failure_patterns()
        for error_type, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
            print(f"   {error_type}: {count}次")
        
        # 最近教训
        print(f"\n📚 最近教训:")
        recent_lessons = self.lessons['lessons'][-5:]
        for i, lesson in enumerate(recent_lessons, 1):
            print(f"\n   {i}. {lesson['error_type']} ({lesson['date'][:10]})")
            print(f"      {lesson['lesson'][:100]}...")
        
        # 改进建议
        print(f"\n💡 待实施改进:")
        improvements = self.generate_improvements()
        for imp in improvements[:3]:
            priority = '🔴' if imp['priority'] == 'high' else '🟡'
            print(f"\n   {priority} {imp['error_type']} ({imp['occurrences']}次)")
            for sug in imp['suggestions'][:2]:
                print(f"      - {sug}")
        
        print("\n" + "=" * 70)
    
    def _save_lessons(self):
        """保存教训"""
        with open(self.lessons_file, 'w', encoding='utf-8') as f:
            json.dump(self.lessons, f, ensure_ascii=False, indent=2)


def main():
    """主函数 - 测试学习循环"""
    loop = LearningLoop()
    
    # 模拟分析失败
    loop.analyze_failure(
        task_id='task_test_001',
        error='503 Service Temporarily Unavailable',
        context={'task_type': 'bounty', 'bounty': 100}
    )
    
    # 生成改进建议
    improvements = loop.generate_improvements()
    
    # 打印报告
    loop.print_learning_report()


if __name__ == "__main__":
    main()

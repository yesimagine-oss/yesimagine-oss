#!/usr/bin/env python3
"""
Capability Evolver - 全能进化自动化脚本

功能:
- 自动记录学习/错误/反馈
- 智能分析和分类
- 自动晋升知识
- 生成进化报告

使用:
    python3 evolver.py [--daily|--weekly|--monthly|--analyze]
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml

class CapabilityEvolver:
    """能力进化器 - 全能进化模式"""
    
    def __init__(self):
        """初始化进化器"""
        self.base_dir = Path(__file__).parent.expanduser()
        self.workspace_dir = self.base_dir.parent
        self.config_dir = self.base_dir / "config"
        self.raw_dir = self.base_dir / "raw"
        self.processed_dir = self.base_dir / "processed"
        
        # 确保目录存在
        self._ensure_directories()
        
        # 加载配置
        self.config = self._load_config()
        
        # 分类规则
        self.classification_rules = self._load_classification_rules()
        
        # 晋升阈值
        self.promotion_thresholds = self._load_promotion_thresholds()
    
    def _ensure_directories(self):
        """确保目录存在"""
        for dir_path in [self.raw_dir, self.processed_dir, self.config_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            (dir_path / "auto-learnings").mkdir(exist_ok=True)
            (dir_path / "auto-errors").mkdir(exist_ok=True)
            (dir_path / "auto-features").mkdir(exist_ok=True)
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        config_file = self.config_dir / "evolution-rules.yaml"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "auto_record": True,
            "auto_analyze": True,
            "auto_promote": True,
            "daily_report": True,
            "keywords": {
                "correction": ["不对", "错了", "应该是", "不正确", "错误"],
                "failure": ["失败", "错误", "异常", "报错", "failed", "error"],
                "feature": ["能不能", "想要", "需要", "希望", "建议"],
                "optimization": ["优化", "改进", "更好", "提升", "效率"]
            }
        }
    
    def _load_classification_rules(self) -> Dict:
        """加载分类规则"""
        rules_file = self.config_dir / "classification-rules.yaml"
        if rules_file.exists():
            with open(rules_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return self._default_classification_rules()
    
    def _default_classification_rules(self) -> Dict:
        """默认分类规则"""
        return {
            "技术问题": {
                "keywords": ["错误", "失败", "异常", "bug", "代码", "程序"],
                "promotion_target": "TOOLS.md"
            },
            "流程优化": {
                "keywords": ["流程", "步骤", "方法", "效率", "优化"],
                "promotion_target": "AGENTS.md"
            },
            "用户偏好": {
                "keywords": ["喜欢", "不喜欢", "偏好", "习惯", "常用"],
                "promotion_target": "USER.md"
            },
            "知识更新": {
                "keywords": ["新", "更新", "变化", "版本", "最新"],
                "promotion_target": "MEMORY.md"
            },
            "行为准则": {
                "keywords": ["应该", "必须", "不要", "总是", "禁止"],
                "promotion_target": "SOUL.md"
            }
        }
    
    def _load_promotion_thresholds(self) -> Dict:
        """加载晋升阈值"""
        threshold_file = self.config_dir / "promotion-thresholds.yaml"
        if threshold_file.exists():
            with open(threshold_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return self._default_promotion_thresholds()
    
    def _default_promotion_thresholds(self) -> Dict:
        """默认晋升阈值"""
        return {
            "temporary": {"count": 1, "action": "keep"},
            "common": {"count": 3, "action": "promote"},
            "core": {"count": 5, "action": "promote_review"},
            "behavior": {"count": 3, "action": "promote_review"},
            "process": {"count": 5, "action": "promote_review"}
        }
    
    def auto_record(self, text: str, source: str = "auto") -> Dict:
        """
        自动记录学习/错误/反馈
        
        Args:
            text: 文本内容
            source: 来源 (user/system/task)
        
        Returns:
            记录结果
        """
        record = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "text": text,
            "type": self._detect_type(text),
            "category": self._classify(text),
            "priority": self._evaluate_priority(text)
        }
        
        # 保存到对应文件
        self._save_record(record)
        
        print(f"📝 已记录：{record['type']} - {record['category']}")
        
        return record
    
    def _detect_type(self, text: str) -> str:
        """检测记录类型"""
        text_lower = text.lower()
        
        for type_name, keywords in self.config.get("keywords", {}).items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return type_name
        
        return "general"
    
    def _classify(self, text: str) -> str:
        """智能分类"""
        text_lower = text.lower()
        
        for category, rules in self.classification_rules.items():
            for keyword in rules.get("keywords", []):
                if keyword.lower() in text_lower:
                    return category
        
        return "其他"
    
    def _evaluate_priority(self, text: str) -> str:
        """评估优先级"""
        # 简单实现：根据关键词判断
        urgent_keywords = ["紧急", "重要", "必须", "critical", "urgent"]
        high_keywords = ["重要", "优先", "high", "important"]
        
        text_lower = text.lower()
        
        for keyword in urgent_keywords:
            if keyword.lower() in text_lower:
                return "P0"
        
        for keyword in high_keywords:
            if keyword.lower() in text_lower:
                return "P1"
        
        return "P2"
    
    def _save_record(self, record: Dict):
        """保存记录"""
        record_type = record["type"]
        
        if record_type == "correction":
            subdir = "auto-learnings"
        elif record_type == "failure":
            subdir = "auto-errors"
        elif record_type == "feature":
            subdir = "auto-features"
        else:
            subdir = "auto-learnings"
        
        file_path = self.raw_dir / subdir / f"{record['id']}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
    
    def analyze_records(self, days: int = 1) -> List[Dict]:
        """
        分析指定天数的记录
        
        Args:
            days: 分析最近多少天的记录
        
        Returns:
            分析结果列表
        """
        analyzed = []
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 遍历所有记录
        for subdir in ["auto-learnings", "auto-errors", "auto-features"]:
            dir_path = self.raw_dir / subdir
            if not dir_path.exists():
                continue
            
            for file_path in dir_path.glob("*.json"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    record = json.load(f)
                
                # Python 3.6 兼容
                timestamp_str = record["timestamp"].replace("Z", "+00:00")
                try:
                    record_time = datetime.strptime(timestamp_str[:19], "%Y-%m-%dT%H:%M:%S")
                except:
                    record_time = datetime.now()
                if record_time >= cutoff_date:
                    analysis = self._analyze_record(record)
                    analyzed.append(analysis)
        
        print(f"🧠 已分析 {len(analyzed)} 条记录")
        return analyzed
    
    def _analyze_record(self, record: Dict) -> Dict:
        """分析单条记录"""
        analysis = record.copy()
        analysis["analyzed_at"] = datetime.now().isoformat()
        analysis["promotion_candidate"] = self._check_promotion(record)
        analysis["similar_records"] = self._find_similar_records(record)
        
        return analysis
    
    def _check_promotion(self, record: Dict) -> bool:
        """检查是否满足晋升条件"""
        category = record.get("category", "其他")
        similar_count = len(self._find_similar_records(record))
        
        # 根据类别和出现次数判断
        thresholds = self.promotion_thresholds
        
        if similar_count >= thresholds.get("core", {}).get("count", 5):
            return True
        elif similar_count >= thresholds.get("common", {}).get("count", 3):
            return True
        
        return False
    
    def _find_similar_records(self, record: Dict) -> List[Dict]:
        """查找相似记录"""
        similar = []
        category = record.get("category", "")
        keywords = record.get("text", "").split()[:5]  # 取前 5 个词
        
        # 简单实现：基于类别和关键词匹配
        for subdir in ["auto-learnings", "auto-errors", "auto-features"]:
            dir_path = self.raw_dir / subdir
            if not dir_path.exists():
                continue
            
            for file_path in dir_path.glob("*.json"):
                if file_path.name == f"{record['id']}.json":
                    continue
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    other = json.load(f)
                
                # 检查类别是否相同
                if other.get("category") == category:
                    # 检查关键词匹配
                    other_text = other.get("text", "")
                    match_count = sum(1 for kw in keywords if kw in other_text)
                    if match_count >= 2:
                        similar.append(other)
        
        return similar
    
    def execute_promotions(self, analyzed: List[Dict]) -> List[Dict]:
        """
        执行晋升
        
        Args:
            analyzed: 已分析记录列表
        
        Returns:
            晋升结果列表
        """
        promotions = []
        
        for record in analyzed:
            if record.get("promotion_candidate"):
                promotion = self._promote_record(record)
                promotions.append(promotion)
        
        print(f"📈 已晋升 {len(promotions)} 条知识")
        return promotions
    
    def _promote_record(self, record: Dict) -> Dict:
        """晋升单条记录"""
        category = record.get("category", "其他")
        target_file = self.classification_rules.get(category, {}).get(
            "promotion_target", "MEMORY.md"
        )
        
        promotion = {
            "id": record["id"],
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "target_file": target_file,
            "content": self._format_for_promotion(record),
            "status": "pending_review"  # 待审核
        }
        
        # 保存到待晋升目录
        promoted_dir = self.processed_dir / "promoted"
        promoted_dir.mkdir(exist_ok=True)
        
        file_path = promoted_dir / f"{record['id']}.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(promotion["content"])
        
        print(f"  → 晋升到 {target_file}: {record['text'][:50]}...")
        
        return promotion
    
    def _format_for_promotion(self, record: Dict) -> str:
        """格式化为晋升内容"""
        return f"""## {record.get('category', '知识')} - {record['id']}

**来源:** {record.get('source', 'auto')}  
**时间:** {record.get('timestamp', '')}  
**优先级:** {record.get('priority', 'P2')}

### 内容
{record.get('text', '')}

### 分析
- 分类：{record.get('category', '其他')}
- 类型：{record.get('type', 'general')}
- 相似记录：{len(record.get('similar_records', []))} 条

---
*自动晋升 - 待审核*
"""
    
    def generate_daily_report(self) -> str:
        """生成每日进化报告"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 统计今日记录
        records = self.analyze_records(days=1)
        
        # 分类统计
        stats = {
            "total": len(records),
            "by_type": {},
            "by_category": {},
            "promotions": 0
        }
        
        for record in records:
            type_name = record.get("type", "unknown")
            category = record.get("category", "other")
            
            stats["by_type"][type_name] = stats["by_type"].get(type_name, 0) + 1
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            
            if record.get("promotion_candidate"):
                stats["promotions"] += 1
        
        # 生成报告
        report = f"""
# 🧬 每日进化报告

**日期:** {today}  
**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 统计概览

| 指标 | 数值 |
|------|------|
| **总记录数** | {stats['total']} |
| **晋升知识** | {stats['promotions']} |
| **主要类型** | {max(stats['by_type'].items(), key=lambda x: x[1])[0] if stats['by_type'] else '无'} |
| **主要分类** | {max(stats['by_category'].items(), key=lambda x: x[1])[0] if stats['by_category'] else '无'} |

## 📝 类型分布

| 类型 | 数量 |
|------|------|
"""
        
        for type_name, count in stats["by_type"].items():
            report += f"| {type_name} | {count} |\n"
        
        report += """
## 🏷️ 分类分布

| 分类 | 数量 |
|------|------|
"""
        
        for category, count in stats["by_category"].items():
            report += f"| {category} | {count} |\n"
        
        report += f"""
---

**报告生成:** Capability Evolver v1.0
"""
        
        # 保存报告
        report_dir = self.processed_dir / "reports"
        report_dir.mkdir(exist_ok=True)
        
        report_file = report_dir / f"daily-{today}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 已生成日报：{report_file}")
        
        return report
    
    def run_daily_process(self):
        """执行每日处理流程"""
        print(f"🧬 开始每日进化处理 - {datetime.now()}")
        print("=" * 60)
        
        # 1. 分析今日记录
        print("\n📝 步骤 1: 分析记录...")
        analyzed = self.analyze_records(days=1)
        
        # 2. 执行晋升
        if analyzed:
            print("\n📈 步骤 2: 执行晋升...")
            promotions = self.execute_promotions(analyzed)
        
        # 3. 生成报告
        print("\n📄 步骤 3: 生成报告...")
        report = self.generate_daily_report()
        
        print("\n" + "=" * 60)
        print("✅ 每日进化处理完成")
        print(f"📊 处理记录：{len(analyzed)} 条")
        if analyzed:
            print(f"📈 晋升知识：{len([r for r in analyzed if r.get('promotion_candidate')])} 条")
        print(f"📄 报告位置：{self.processed_dir}/reports/")
    
    def run_weekly_review(self):
        """执行每周回顾"""
        print(f"🧬 开始每周回顾 - {datetime.now()}")
        
        # 分析最近 7 天
        analyzed = self.analyze_records(days=7)
        
        # 生成周报
        # TODO: 实现周报生成逻辑
        
        print("✅ 每周回顾完成")
    
    def run_monthly_review(self):
        """执行每月回顾"""
        print(f"🧬 开始每月回顾 - {datetime.now()}")
        
        # 分析最近 30 天
        analyzed = self.analyze_records(days=30)
        
        # 生成月报
        # TODO: 实现月报生成逻辑
        
        print("✅ 每月回顾完成")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Capability Evolver - 全能进化自动化")
    parser.add_argument(
        "--daily",
        action="store_true",
        help="执行每日处理流程"
    )
    parser.add_argument(
        "--weekly",
        action="store_true",
        help="执行每周回顾"
    )
    parser.add_argument(
        "--monthly",
        action="store_true",
        help="执行每月回顾"
    )
    parser.add_argument(
        "--analyze",
        type=str,
        help="分析指定文本并记录"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="运行测试"
    )
    
    args = parser.parse_args()
    
    evolver = CapabilityEvolver()
    
    if args.daily:
        evolver.run_daily_process()
    
    elif args.weekly:
        evolver.run_weekly_review()
    
    elif args.monthly:
        evolver.run_monthly_review()
    
    elif args.analyze:
        result = evolver.auto_record(args.analyze)
        print(f"\n记录结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.test:
        print("🧪 运行测试...")
        
        # 测试自动记录
        test_texts = [
            "这个方法不对，应该是这样的...",
            "程序运行失败，出现错误",
            "能不能增加一个新功能",
            "这个流程可以优化一下"
        ]
        
        for text in test_texts:
            evolver.auto_record(text, source="test")
        
        # 测试分析
        evolver.analyze_records(days=1)
        
        # 测试报告
        evolver.generate_daily_report()
        
        print("\n✅ 测试完成")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

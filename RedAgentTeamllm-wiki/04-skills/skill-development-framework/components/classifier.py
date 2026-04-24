#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classifier 组件 - 智能内容分类器

基于关键词匹配的智能分类
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class Classifier:
    """智能内容分类器"""
    
    # 8 大分类定义
    CATEGORIES = {
        "📖 技术教程": ["安装", "配置", "部署", "教程", "指南", "教学", "入门", "实战"],
        "🛠️ 实战案例": ["案例", "实战", "项目", "演示", "实践", "应用", "实例"],
        "📄 产品文档": ["安全", "公告", "版本", "功能", "更新", "发布", "说明"],
        "💡 学习笔记": ["学习", "成长", "笔记", "心得", "感悟", "总结", "反思"],
        "🔥 热点资讯": ["发布", "新功能", "热点", "新闻", "动态", "资讯", "速递"],
        "🎨 设计技能": ["设计", "Prompt", "美学", "UI", "UX", "视觉", "排版"],
        "🔧 工具推荐": ["工具", "CLI", "插件", "推荐", "软件", "应用", "效率"],
        "🎓 训练营": ["训练营", "课程", "教学", "培训", "学习", "系列", "进阶"]
    }
    
    # 分类优先级（用于平分情况）
    PRIORITY = [
        "🔥 热点资讯",
        "📖 技术教程",
        "🛠️ 实战案例",
        "🔧 工具推荐",
        "💡 学习笔记",
        "📄 产品文档",
        "🎨 设计技能",
        "🎓 训练营"
    ]
    
    @staticmethod
    def classify(content: str, title: str = "", user_category: str = None) -> str:
        """
        智能分类
        
        Args:
            content: 内容文本
            title: 标题
            user_category: 用户指定分类（可选）
        
        Returns:
            分类名称（含 Emoji）
        """
        # 如果用户指定分类，直接返回
        if user_category:
            logger.info(f"Using user-specified category: {user_category}")
            return user_category
        
        # 合并标题和内容
        text = f"{title} {content}".lower()
        
        # 计算每个分类的匹配度
        scores = {}
        for category, keywords in Classifier.CATEGORIES.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[category] = score
        
        logger.info(f"Classification scores: {scores}")
        
        # 找出最高分
        max_score = max(scores.values())
        
        # 如果所有分类都得 0 分，返回"待分类"
        if max_score == 0:
            logger.warning("No category matched, returning '待分类'")
            return "待分类"
        
        # 找出所有最高分的分类
        best_categories = [cat for cat, score in scores.items() if score == max_score]
        
        # 如果平分，按优先级选择
        if len(best_categories) > 1:
            for priority_cat in Classifier.PRIORITY:
                if priority_cat in best_categories:
                    logger.info(f"Multiple categories tied, choosing by priority: {priority_cat}")
                    return priority_cat
        
        # 否则返回第一个
        result = best_categories[0]
        logger.info(f"Classification result: {result}")
        return result
    
    @staticmethod
    def get_category_emoji(category: str) -> str:
        """获取分类的 Emoji"""
        # 分类名已经包含 Emoji，直接返回
        return category.split(" ")[0] if " " in category else "📌"
    
    @staticmethod
    def get_all_categories() -> List[str]:
        """获取所有分类列表"""
        return list(Classifier.CATEGORIES.keys())
    
    @staticmethod
    def add_category(name: str, keywords: List[str]):
        """
        添加自定义分类
        
        Args:
            name: 分类名称
            keywords: 关键词列表
        """
        Classifier.CATEGORIES[name] = keywords
        logger.info(f"Added custom category: {name}")
    
    @staticmethod
    def get_keywords(category: str) -> List[str]:
        """获取分类的关键词列表"""
        return Classifier.CATEGORIES.get(category, [])


# 测试代码
if __name__ == "__main__":
    # 测试示例
    test_cases = [
        ("这是一篇安装配置教程", "Python 安装指南", "📖 技术教程"),
        ("这是一个实战项目案例", "实战项目演示", "🛠️ 实战案例"),
        ("这是最新版本发布说明", "v2.0 新功能发布", "📄 产品文档"),
        ("这是我的学习心得", "学习成长总结", "💡 学习笔记"),
        ("这是最新热点资讯", "AI 新功能动态", "🔥 热点资讯"),
    ]
    
    print("Testing Classifier:")
    for content, title, expected in test_cases:
        result = Classifier.classify(content, title)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{title}' -> {result} (expected: {expected})")

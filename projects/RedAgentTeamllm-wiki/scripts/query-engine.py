#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RedAgentTeamllm-wiki 智能查询引擎 (AI-001)
功能：规则匹配 + 关键词搜索
资源需求：CPU 10%, RAM 50MB
执行时间：毫秒级

使用示例:
    python3 query-engine.py "如何备份？"
    python3 query-engine.py "Token 认证失败怎么办"
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 配置
WIKI_ROOT = Path("/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki")
SOP_DIR = WIKI_ROOT / "learnings"
ACCIDENT_DIR = WIKI_ROOT / ".learnings"
WIKI_DIR = WIKI_ROOT / "wiki"

# 问题类型关键词
QUESTION_PATTERNS = {
    "sop": ["如何", "怎么", "流程", "步骤", "sop", "规范", "标准"],
    "accident": ["错误", "失败", "问题", "故障", "事故", "报错", "exception", "error"],
    "fact": ["配置", "路径", "id", "时间", "命令", "token", "端口", "url"],
    "innovation": ["新", "研究", "探索", "建议", "优化", "改进"]
}


class KnowledgeQueryEngine:
    """知识库查询引擎"""
    
    def __init__(self):
        self.results = []
    
    def identify_question_type(self, question: str) -> str:
        """识别问题类型"""
        question_lower = question.lower()
        
        scores = {}
        for qtype, keywords in QUESTION_PATTERNS.items():
            score = sum(1 for kw in keywords if kw in question_lower)
            scores[qtype] = score
        
        # 返回得分最高的类型
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "fact"
    
    def search_directory(self, directory: Path, keywords: list, limit: int = 5) -> list:
        """搜索目录"""
        results = []
        
        if not directory.exists():
            return results
        
        for file_path in directory.rglob("*.md"):
            try:
                content = file_path.read_text(encoding='utf-8').lower()
                
                # 计算匹配度
                match_count = sum(1 for kw in keywords if kw.lower() in content)
                if match_count > 0:
                    # 提取相关片段
                    rel_path = str(file_path.relative_to(WIKI_ROOT))
                    results.append({
                        "file": rel_path,
                        "matches": match_count,
                        "path": str(file_path)
                    })
            except Exception as e:
                continue
        
        # 按匹配度排序
        results.sort(key=lambda x: x["matches"], reverse=True)
        return results[:limit]
    
    def extract_keywords(self, question: str) -> list:
        """提取关键词"""
        # 移除停用词
        stop_words = ["的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都", "一", "一个"]
        words = re.findall(r'[\w\.-]+', question)
        keywords = [w for w in words if w not in stop_words and len(w) > 1]
        return keywords
    
    def query(self, question: str) -> dict:
        """执行查询"""
        start_time = datetime.now()
        
        # 1. 识别问题类型
        qtype = self.identify_question_type(question)
        
        # 2. 提取关键词
        keywords = self.extract_keywords(question)
        
        # 3. 确定搜索目录
        search_dirs = {
            "sop": [SOP_DIR],
            "accident": [ACCIDENT_DIR],
            "fact": [WIKI_DIR, SOP_DIR],
            "innovation": [WIKI_DIR, SOP_DIR, ACCIDENT_DIR]
        }
        
        # 4. 搜索
        all_results = []
        for dir_path in search_dirs.get(qtype, [WIKI_DIR]):
            results = self.search_directory(dir_path, keywords)
            all_results.extend(results)
        
        # 5. 去重 + 排序
        seen = set()
        unique_results = []
        for r in all_results:
            if r["file"] not in seen:
                seen.add(r["file"])
                unique_results.append(r)
        
        unique_results.sort(key=lambda x: x["matches"], reverse=True)
        
        # 6. 生成响应
        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        
        response = {
            "question": question,
            "type": qtype,
            "keywords": keywords,
            "results": unique_results[:5],
            "count": len(unique_results),
            "response_time_ms": round(response_time, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        # 7. 如无结果，提供建议
        if len(unique_results) == 0:
            response["suggestion"] = "知识库无答案，建议参考官方文档：https://docs.openclaw.ai"
        
        return response
    
    def print_results(self, response: dict):
        """打印结果"""
        print(f"\n{'='*60}")
        print(f"🔍 问题：{response['question']}")
        print(f"📊 类型：{response['type']}")
        print(f"🏷️  关键词：{', '.join(response['keywords'])}")
        print(f"⏱️  响应时间：{response['response_time_ms']}ms")
        print(f"📦 匹配文件：{response['count']}个")
        print(f"{'='*60}\n")
        
        if response['count'] > 0:
            print("📄 相关文件:")
            for i, result in enumerate(response['results'], 1):
                print(f"  {i}. {result['file']} (匹配度：{result['matches']})")
        else:
            print(f"⚠️  {response.get('suggestion', '无结果')}")
        
        print(f"\n{'='*60}\n")


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 query-engine.py \"你的问题\"")
        print("示例：python3 query-engine.py \"如何备份？\"")
        sys.exit(1)
    
    question = " ".join(sys.argv[1:])
    
    engine = KnowledgeQueryEngine()
    response = engine.query(question)
    engine.print_results(response)
    
    # 保存结果到日志
    log_file = WIKI_ROOT / "logs" / "query-log.jsonl"
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(response, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()

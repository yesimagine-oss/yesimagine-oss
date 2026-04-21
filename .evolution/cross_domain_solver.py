#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨域問題解決器
混合多技能解決新問題
"""

import json
from pathlib import Path
from datetime import datetime

class CrossDomainSolver:
    """跨域問題解決引擎"""
    
    def __init__(self, workspace="/home/admin/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.skills = self.load_skills()
        
    def load_skills(self):
        """加載所有技能"""
        skills = []
        gene_files = list(self.workspace.glob("gene_distilled_*.json"))
        
        for gene_file in gene_files:
            with open(gene_file, 'r', encoding='utf-8') as f:
                gene = json.load(f)
                skills.append({
                    "file": gene_file.name,
                    "signals": gene.get("signals_match", []),
                    "category": gene.get("category", ""),
                    "strategy": gene.get("strategy", []),
                    "asset_id": gene.get("asset_id", "")
                })
                
        return skills
    
    def find_relevant_skills(self, problem_signals):
        """根據問題信號找到相關技能"""
        relevant = []
        
        for skill in self.skills:
            # 計算信號匹配度
            match_count = len(set(skill["signals"]) & set(problem_signals))
            if match_count > 0:
                relevant.append({
                    "skill": skill,
                    "match_score": match_count
                })
        
        # 按匹配度排序
        relevant.sort(key=lambda x: x["match_score"], reverse=True)
        
        return relevant
    
    def compose_solution(self, problem, relevant_skills):
        """組合技能創建解決方案"""
        
        solution = {
            "problem": problem,
            "timestamp": datetime.utcnow().isoformat(),
            "selected_skills": [],
            "combined_strategy": [],
            "confidence": 0.0
        }
        
        # 選擇前 N 個最相關技能
        top_skills = relevant_skills[:5]
        
        total_score = sum(s["match_score"] for s in top_skills)
        
        for item in top_skills:
            skill = item["skill"]
            solution["selected_skills"].append({
                "name": skill["file"],
                "category": skill["category"],
                "signals": skill["signals"],
                "match_score": item["match_score"]
            })
            
            # 組合策略
            for step in skill["strategy"][:3]:  # 每個技能取前 3 步
                solution["combined_strategy"].append(f"[{skill['category']}] {step}")
        
        # 計算置信度
        solution["confidence"] = min(1.0, total_score / 10.0)
        
        return solution
    
    def solve(self, problem_description, problem_signals):
        """解決問題"""
        print(f"\n{'='*60}")
        print(f"🧩 問題：{problem_description}")
        print(f"{'='*60}\n")
        
        # 找到相關技能
        print("🔍 搜索相關技能...")
        relevant = self.find_relevant_skills(problem_signals)
        print(f"  找到 {len(relevant)} 個相關技能\n")
        
        # 組合解決方案
        print("🔧 組合解決方案...")
        solution = self.compose_solution(problem_description, relevant)
        
        # 輸出解決方案
        print(f"\n📋 解決方案:")
        print(f"  置信度：{solution['confidence']*100:.1f}%")
        print(f"  使用技能：{len(solution['selected_skills'])} 個")
        print(f"\n  組合策略:")
        for i, step in enumerate(solution['combined_strategy'][:10], 1):
            print(f"    {i}. {step}")
            
        # 保存解決方案
        solution_file = self.workspace / ".evolution" / f"solution_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(solution_file, 'w', encoding='utf-8') as f:
            json.dump(solution, f, indent=2, ensure_ascii=False)
            
        print(f"\n💾 已保存：{solution_file}\n")
        
        return solution

if __name__ == "__main__":
    solver = CrossDomainSolver()
    
    # 測試：解決 asset_id 計算問題
    problem = "Asset ID 計算與 Hub 不匹配"
    signals = ["sha256", "canonical_json", "asset_id", "verification", "hash", "serialization"]
    
    solution = solver.solve(problem, signals)

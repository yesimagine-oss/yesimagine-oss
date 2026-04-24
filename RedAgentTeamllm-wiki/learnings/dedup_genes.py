#!/usr/bin/env python3
"""
Gene 查重與合併腳本
- 掃描所有 GENE-*.md 文件
- 提取 Signals 和 Strategy
- 計算相似度 (>80% 需合併)
- 生成合併報告
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

LEARNINGS_DIR = Path("/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/learnings")

def extract_gene_info(filepath):
    """從 Gene 文件中提取 Signals 和 Strategy"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 Signals
    signals_match = re.search(r'## 信號 \(Signals\)\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    signals = []
    if signals_match:
        signals_text = signals_match.group(1)
        signals = [s.strip().lstrip('- ').strip() for s in signals_text.strip().split('\n') if s.strip()]
    
    # 提取 Strategy
    strategy_match = re.search(r'## 策略 \(Strategy\)\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    strategy = ""
    if strategy_match:
        strategy = strategy_match.group(1).strip()
    
    # 提取事故來源
    source_match = re.search(r'\*\*事故來源\*\*:\s*(.+?)\s*\n', content)
    source = source_match.group(1).strip() if source_match else ""
    
    # 提取 Gene ID
    gene_id_match = re.search(r'\*\*Gene ID\*\*:\s*(.+?)\s*\n', content)
    gene_id = gene_id_match.group(1).strip() if gene_id_match else ""
    
    return {
        'filepath': filepath,
        'filename': filepath.name,
        'gene_id': gene_id,
        'source': source,
        'signals': set(signals),
        'strategy': strategy,
        'signals_text': '\n'.join(sorted(signals)),
    }

def calculate_similarity(set1, set2, text1="", text2=""):
    """計算兩個 Gene 的相似度"""
    # Signals 重疊率 (Jaccard similarity)
    if not set1 and not set2:
        signals_sim = 1.0
    elif not set1 or not set2:
        signals_sim = 0.0
    else:
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        signals_sim = intersection / union if union > 0 else 0.0
    
    # Strategy 相似度
    strategy_sim = SequenceMatcher(None, text1, text2).ratio()
    
    # 加權平均 (Signals 40%, Strategy 60%)
    overall_sim = 0.4 * signals_sim + 0.6 * strategy_sim
    
    return {
        'signals_similarity': signals_sim,
        'strategy_similarity': strategy_sim,
        'overall_similarity': overall_sim
    }

def find_duplicates(genes, threshold=0.8):
    """找出所有重複的 Gene 對"""
    duplicates = []
    n = len(genes)
    
    for i in range(n):
        for j in range(i + 1, n):
            gene1 = genes[i]
            gene2 = genes[j]
            
            sim = calculate_similarity(
                gene1['signals'], 
                gene2['signals'],
                gene1['strategy'],
                gene2['strategy']
            )
            
            if sim['overall_similarity'] > threshold:
                duplicates.append({
                    'gene1': gene1,
                    'gene2': gene2,
                    'similarity': sim
                })
    
    return duplicates

def cluster_duplicates(duplicates):
    """將重複的 Gene 分組為集群"""
    # 使用並查集將重複的 Gene 分組
    parent = {}
    
    def find(x):
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
    
    # 建立集群
    for dup in duplicates:
        file1 = dup['gene1']['filepath']
        file2 = dup['gene2']['filepath']
        union(str(file1), str(file2))
    
    # 分組
    clusters = defaultdict(list)
    all_files = set()
    for dup in duplicates:
        all_files.add(str(dup['gene1']['filepath']))
        all_files.add(str(dup['gene2']['filepath']))
    
    for file_path in all_files:
        root = find(file_path)
        clusters[root].append(file_path)
    
    return list(clusters.values())

def merge_genes(gene_list, all_genes_dict):
    """合併一組 Gene"""
    if not gene_list:
        return None
    
    # 收集所有 signals 和 strategies
    all_signals = set()
    strategies = []
    sources = []
    
    for file_path in gene_list:
        gene = all_genes_dict.get(file_path)
        if gene:
            all_signals.update(gene['signals'])
            strategies.append(gene['strategy'])
            sources.append(gene['source'])
    
    # 選擇最完整的 strategy
    best_strategy = max(strategies, key=len) if strategies else ""
    
    # 生成 references
    references = [Path(fp).name for fp in gene_list]
    
    return {
        'signals': all_signals,
        'strategy': best_strategy,
        'sources': sources,
        'references': references,
        'count': len(gene_list)
    }

def main():
    print("=" * 60)
    print("Gene 查重與合併分析")
    print("=" * 60)
    
    # 掃描所有 GENE-*.md 文件
    gene_files = sorted(LEARNINGS_DIR.glob("GENE-*.md"))
    print(f"\n📁 找到 {len(gene_files)} 個 GENE 文件")
    
    # 提取所有 Gene 信息
    genes = []
    genes_dict = {}
    for filepath in gene_files:
        gene_info = extract_gene_info(filepath)
        genes.append(gene_info)
        genes_dict[str(filepath)] = gene_info
    
    print(f"✅ 完成 {len(genes)} 個 Gene 解析")
    
    # 查找重複
    print("\n🔍 開始查重 (閾值 >80%)...")
    duplicates = find_duplicates(genes, threshold=0.8)
    print(f"⚠️  發現 {len(duplicates)} 對重複 Gene")
    
    # 分組集群
    if duplicates:
        clusters = cluster_duplicates(duplicates)
        print(f"📊 形成 {len(clusters)} 個重複集群")
        
        # 生成合併報告
        report = {
            'original_count': len(genes),
            'duplicate_pairs': len(duplicates),
            'clusters': len(clusters),
            'cluster_details': []
        }
        
        for i, cluster in enumerate(clusters, 1):
            merged = merge_genes(cluster, genes_dict)
            if merged:
                report['cluster_details'].append({
                    'cluster_id': i,
                    'files': [Path(f).name for f in cluster],
                    'merged_signals_count': len(merged['signals']),
                    'references': merged['references']
                })
        
        # 計算合併後數量
        merged_count = len(genes) - len(duplicates)  # 簡化估算
        report['estimated_merged_count'] = merged_count
        
        # 保存報告
        report_path = LEARNINGS_DIR / "DEDUP-REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 報告已保存至: {report_path}")
        
        # 打印詳細信息
        print("\n" + "=" * 60)
        print("合併詳情")
        print("=" * 60)
        
        for cluster in report['cluster_details'][:10]:  # 只显示前 10 个
            print(f"\n集群 {cluster['cluster_id']}: {cluster['files']}")
            print(f"  合併後 Signals: {cluster['merged_signals_count']} 個")
        
        if len(report['cluster_details']) > 10:
            print(f"\n... 還有 {len(report['cluster_details']) - 10} 個集群")
        
        print("\n" + "=" * 60)
        print(f"原始 Gene 數量：{report['original_count']}")
        print(f"重複對數：{report['duplicate_pairs']}")
        print(f"重複集群：{report['clusters']}")
        print(f"估計合併後數量：~{report['estimated_merged_count']}")
        print("=" * 60)
        
    else:
        print("✅ 未發現重複 Gene")
        report = {
            'original_count': len(genes),
            'duplicate_pairs': 0,
            'clusters': 0,
            'cluster_details': []
        }
    
    print("\n✅ 查重完成，請用戶確認")
    return report

if __name__ == "__main__":
    main()

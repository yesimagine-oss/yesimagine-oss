#!/usr/bin/env python3
"""
Gene 合併執行腳本
- 根據 DEDUP-REPORT.json 合併重複 Gene
- 保留唯一 Gene 文件
- 合併 Signals（去重）
- 合併 Strategy（取最完整版本）
- 添加 References
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

LEARNINGS_DIR = Path("/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/learnings")

def extract_gene_info(filepath):
    """從 Gene 文件中提取完整信息"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    info = {
        'content': content,
        'filepath': filepath,
        'filename': filepath.name,
        'gene_id': '',
        'source': '',
        'signals': [],
        'strategy': '',
        'category': '',
        'root_cause': '',
        'consequences': ''
    }
    
    # 提取 Gene ID
    gene_id_match = re.search(r'\*\*Gene ID\*\*:\s*(.+?)\s*\n', content)
    if gene_id_match:
        info['gene_id'] = gene_id_match.group(1).strip()
    
    # 提取事故來源
    source_match = re.search(r'\*\*事故來源\*\*:\s*(.+?)\s*\n', content)
    if source_match:
        info['source'] = source_match.group(1).strip()
    
    # 提取 Signals
    signals_match = re.search(r'## 信號 \(Signals\)\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if signals_match:
        signals_text = signals_match.group(1)
        info['signals'] = [s.strip().lstrip('- ').strip() for s in signals_text.strip().split('\n') if s.strip()]
    
    # 提取 Strategy
    strategy_match = re.search(r'## 策略 \(Strategy\)\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if strategy_match:
        info['strategy'] = strategy_match.group(1).strip()
    
    # 提取 Category
    category_match = re.search(r'## 分類 \(Category\)\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if category_match:
        info['category'] = category_match.group(1).strip()
    
    # 提取 Root Cause
    root_cause_match = re.search(r'## 根本原因 \(Root Cause\)\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if root_cause_match:
        info['root_cause'] = root_cause_match.group(1).strip()
    
    # 提取 Consequences
    consequences_match = re.search(r'## 直接後果 \(Consequences\)\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if consequences_match:
        info['consequences'] = consequences_match.group(1).strip()
    
    return info

def merge_gene_contents(gene_list):
    """合併一組 Gene 的內容"""
    if not gene_list:
        return None
    
    all_signals = set()
    strategies = []
    sources = []
    root_causes = []
    consequences_list = []
    categories = set()
    
    # 選擇第一個作為基礎（通常是最早的）
    base_gene = None
    longest_strategy = ""
    
    for filepath in gene_list:
        # Convert string to Path if needed
        if isinstance(filepath, str):
            filepath = Path(filepath)
        gene = extract_gene_info(filepath)
        if gene:
            if base_gene is None:
                base_gene = gene
            
            all_signals.update(gene['signals'])
            strategies.append(gene['strategy'])
            sources.append(gene['source'])
            categories.add(gene['category'])
            
            if gene['root_cause']:
                root_causes.append(gene['root_cause'])
            if gene['consequences']:
                consequences_list.append(gene['consequences'])
            
            # 保留最完整的 strategy
            if len(gene['strategy']) > len(longest_strategy):
                longest_strategy = gene['strategy']
    
    if not base_gene:
        return None
    
    # 生成 References
    references = [Path(fp).name for fp in gene_list]
    
    # 合併 root causes (去重)
    unique_root_causes = []
    seen_causes = set()
    for cause in root_causes:
        if cause not in seen_causes:
            unique_root_causes.append(cause)
            seen_causes.add(cause)
    
    merged_root_cause = '\n\n'.join(unique_root_causes[:3])  # 最多保留 3 個
    
    # 合併 consequences
    merged_consequences = '\n\n'.join(consequences_list[:3])  # 最多保留 3 個
    
    # 生成新的 Gene ID（使用第一個）
    new_gene_id = base_gene['gene_id']
    
    # 生成合併後的內容
    merged_content = f"""# Gene: {new_gene_id}

**事故來源**: {', '.join(sources[:5])}{'...' if len(sources) > 5 else ''}  
**生成時間**: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z')}  
**事故級別**: Merged  
**事故類型**: CONSOLIDATED  
**時間戳**: {datetime.now().strftime('%Y-%m-%d')}  
**合併狀態**: ✅ 已合併 {len(references)} 個重複 Gene

---

## 根本原因 (Root Cause)

{merged_root_cause}

## 直接後果 (Consequences)

{merged_consequences}

## 分類 (Category)

{list(categories)[0] if categories else 'consolidated'}

## 信號 (Signals)

"""
    
    # 添加 Signals
    for signal in sorted(all_signals):
        merged_content += f"- {signal}\n"
    
    merged_content += f"""
## 策略 (Strategy)

{longest_strategy}

## 驗證信息

- **Gene ID**: {new_gene_id}
- **Capsule ID**: capsule_merged_{datetime.now().strftime('%Y%m%d%H%M%S')}
- **唯一性**: 基於合併後信號生成
- **狀態**: 待發布

---

## 參考文獻 (References)

本 Gene 由以下 {len(references)} 個重複 Gene 合併而成：

"""
    
    for i, ref in enumerate(references, 1):
        merged_content += f"{i}. {ref}\n"
    
    merged_content += f"""
---

*此 Gene 由批量合併系統自动生成*
*合併時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*原始 Gene 數量：{len(references)} → 合併後：1*
"""
    
    return {
        'content': merged_content,
        'references': references,
        'signals_count': len(all_signals),
        'merged_count': len(references)
    }

def main():
    print("=" * 60)
    print("Gene 合併執行")
    print("=" * 60)
    
    # 讀取查重報告
    report_path = LEARNINGS_DIR / "DEDUP-REPORT.json"
    if not report_path.exists():
        print("❌ 未找到 DEDUP-REPORT.json，請先運行 dedup_genes.py")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    print(f"\n📊 讀取報告：{report['original_count']} 個 Gene, {report['clusters']} 個集群")
    
    # 創建合併目錄
    merged_dir = LEARNINGS_DIR / "merged"
    merged_dir.mkdir(exist_ok=True)
    
    # 跟蹤已處理的文件
    processed_files = set()
    merged_files = []
    
    # 處理每個集群
    for cluster in report['cluster_details']:
        cluster_id = cluster['cluster_id']
        files = cluster['files']
        
        print(f"\n🔄 處理集群 {cluster_id}: {len(files)} 個文件")
        
        # 合併 Gene
        merged = merge_gene_contents(files)
        if merged:
            # 生成新文件名
            new_filename = f"GENE-MERGED-{cluster_id:03d}.md"
            new_filepath = merged_dir / new_filename
            
            # 寫入合併後的文件
            with open(new_filepath, 'w', encoding='utf-8') as f:
                f.write(merged['content'])
            
            merged_files.append({
                'filename': new_filename,
                'merged_count': merged['merged_count'],
                'signals_count': merged['signals_count'],
                'references': merged['references']
            })
            
            # 標記已處理
            for f in files:
                processed_files.add(f)
            
            print(f"  ✅ 生成：{new_filename} (合併 {merged['merged_count']} → 1)")
    
    # 複製未合併的文件
    print("\n📁 複製未合併的 Gene...")
    gene_files = sorted(LEARNINGS_DIR.glob("GENE-*.md"))
    unmerged_count = 0
    
    for filepath in gene_files:
        if filepath.name not in processed_files:
            # 複製到 merged 目錄
            dest_path = merged_dir / filepath.name
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            unmerged_count += 1
    
    print(f"  ✅ 複製 {unmerged_count} 個未合併 Gene")
    
    # 生成最終報告
    final_report = {
        'original_count': report['original_count'],
        'merged_clusters': len(report['cluster_details']),
        'merged_files_count': len(merged_files),
        'unmerged_count': unmerged_count,
        'final_count': len(merged_files) + unmerged_count,
        'merged_details': merged_files,
        'processed_files': list(processed_files)
    }
    
    # 保存報告
    final_report_path = merged_dir / "MERGE-REPORT.json"
    with open(final_report_path, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, ensure_ascii=False, indent=2)
    
    # 生成文本報告
    text_report_path = merged_dir / "MERGE-REPORT.md"
    with open(text_report_path, 'w', encoding='utf-8') as f:
        f.write("# Gene 合併報告\n\n")
        f.write(f"## 統計\n\n")
        f.write(f"- 原始 Gene 數量：{final_report['original_count']}\n")
        f.write(f"- 合併集群數量：{final_report['merged_clusters']}\n")
        f.write(f"- 未合併 Gene 數量：{final_report['unmerged_count']}\n")
        f.write(f"- **最終 Gene 數量：{final_report['final_count']}**\n\n")
        f.write(f"## 合併詳情\n\n")
        f.write(f"| 集群 ID | 合併後文件名 | 合併數量 | Signals 數量 |\n")
        f.write(f"|---------|-------------|----------|------------|\n")
        for m in merged_files:
            f.write(f"| {m['merged_count']} | {m['filename']} | {m['merged_count']} | {m['signals_count']} |\n")
    
    print("\n" + "=" * 60)
    print("✅ 合併完成")
    print("=" * 60)
    print(f"原始 Gene 數量：{final_report['original_count']}")
    print(f"合併後 Gene 數量：{final_report['final_count']}")
    print(f"減少數量：{final_report['original_count'] - final_report['final_count']}")
    print(f"\n📄 報告路徑：{text_report_path}")
    print(f"📁 合併目錄：{merged_dir}")
    print("\n⚠️  請用戶確認後再進行後續操作")
    
    return final_report

if __name__ == "__main__":
    main()

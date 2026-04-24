#!/usr/bin/env python3
"""
批量添加 Front Matter 到 wiki 文件
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def get_category_from_path(filepath):
    """根據路徑推斷類別"""
    path_str = str(filepath).lower()
    if 'serper' in path_str:
        return 'serper'
    elif 'javascript' in path_str or 'js' in path_str:
        return 'javascript'
    elif 'douyin' in path_str or 'tiktok' in path_str:
        return 'douyin'
    elif 'evomap' in path_str:
        return 'evomap'
    elif 'evolver' in path_str:
        return 'evolver'
    elif 'docker' in path_str:
        return 'docker'
    elif 'nodejs' in path_str:
        return 'nodejs'
    elif 'gmail' in path_str:
        return 'gmail'
    elif 'feishu' in path_str:
        return 'feishu'
    elif 'memory' in path_str:
        return 'memory'
    elif 'llm' in path_str:
        return 'llm'
    else:
        return 'general'

def add_frontmatter(filepath):
    """為文件添加 Front Matter"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已有 Front Matter
        if content.strip().startswith('---'):
            return False, '已有 Front Matter'
        
        # 生成 Front Matter
        filename = os.path.basename(filepath)
        title = os.path.splitext(filename)[0].replace('-', ' ').replace('_', ' ').title()
        category = get_category_from_path(filepath)
        today = datetime.now().strftime('%Y-%m-%d')
        
        frontmatter = f"""---
title: "{title}"
type: "article"
category: "{category}"
tags: ["{category}", "auto-generated"]
created_at: "{today}"
version: "1.0"
---

"""
        
        # 寫入新內容
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter + content)
        
        return True, '已添加 Front Matter'
    except Exception as e:
        return False, f'錯誤：{str(e)}'

def main():
    wiki_dir = '/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/wiki'
    
    total = 0
    success = 0
    skipped = 0
    errors = 0
    
    print(f"🔍 掃描 {wiki_dir}...")
    
    for root, dirs, files in os.walk(wiki_dir):
        # 跳過 node_modules 等目錄
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
        
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                total += 1
                
                result, msg = add_frontmatter(filepath)
                
                if result:
                    success += 1
                    if success <= 10:  # 只顯示前 10 個
                        print(f"  ✅ {filepath}")
                else:
                    if '已有' in msg:
                        skipped += 1
                    else:
                        errors += 1
                        print(f"  ❌ {filepath}: {msg}")
    
    print(f"\n📊 統計結果:")
    print(f"  總文件數：{total}")
    print(f"  已添加：{success}")
    print(f"  已跳過：{skipped}")
    print(f"  錯誤：{errors}")
    print(f"  Front Matter 合規率：{success * 100 // total if total > 0 else 0}%")

if __name__ == '__main__':
    main()

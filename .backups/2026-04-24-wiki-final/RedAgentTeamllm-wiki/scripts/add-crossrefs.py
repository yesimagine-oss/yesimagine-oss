#!/usr/bin/env python3
"""
批量添加交叉引用到 wiki 文件
"""

import os
import re
from pathlib import Path

def extract_wikilinks(content):
    """提取現有的 wikilinks"""
    return set(re.findall(r'\[\[([^\]]+)\]\]', content))

def generate_wikilinks(filepath, all_files):
    """根據文件名生成相關的 wikilinks"""
    filename = os.path.splitext(os.path.basename(filepath))[0]
    links = []
    
    # 查找相關文件
    for other_file in all_files:
        other_name = os.path.splitext(os.path.basename(other_file))[0]
        # 如果有共同關鍵詞
        if filename != other_name and len(filename) > 3:
            # 檢查是否有共同詞
            filename_parts = set(filename.lower().replace('-', ' ').replace('_', ' ').split())
            other_parts = set(other_name.lower().replace('-', ' ').replace('_', ' ').split())
            
            if filename_parts & other_parts:  # 有交集
                links.append(other_name)
    
    return links[:5]  # 最多 5 個鏈接

def add_crossrefs(filepath, all_files):
    """為文件添加交叉引用"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已有足夠的交叉引用
        existing_links = extract_wikilinks(content)
        if len(existing_links) >= 3:
            return False, '已有足夠交叉引用'
        
        # 生成新的 wikilinks
        new_links = generate_wikilinks(filepath, all_files)
        
        if not new_links:
            return False, '無相關鏈接'
        
        # 過濾掉已存在的
        new_links = [l for l in new_links if l not in existing_links][:3]
        
        if not new_links:
            return False, '無新鏈接可添加'
        
        # 在文件末尾添加相關文檔部分
        related_section = "\n\n## 相關文檔\n\n"
        for link in new_links:
            related_section += f"- [[{link}]]\n"
        
        # 寫入新內容
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(related_section)
        
        return True, f'已添加 {len(new_links)} 個交叉引用'
    except Exception as e:
        return False, f'錯誤：{str(e)}'

def main():
    wiki_dir = '/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/wiki'
    
    # 收集所有 md 文件
    all_files = []
    for root, dirs, files in os.walk(wiki_dir):
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
        for file in files:
            if file.endswith('.md'):
                all_files.append(os.path.join(root, file))
    
    print(f"🔍 掃描到 {len(all_files)} 個文件")
    
    total = 0
    success = 0
    skipped = 0
    errors = 0
    
    for filepath in all_files:  # 處理所有文件
        total += 1
        
        result, msg = add_crossrefs(filepath, all_files)
        
        if result:
            success += 1
            if success <= 10:
                print(f"  ✅ {filepath}: {msg}")
        else:
            skipped += 1
    
    print(f"\n📊 統計結果:")
    print(f"  處理文件：{total}")
    print(f"  已添加：{success}")
    print(f"  已跳過：{skipped}")
    print(f"  錯誤：{errors}")

if __name__ == '__main__':
    main()

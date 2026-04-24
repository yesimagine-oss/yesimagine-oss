#!/usr/bin/env python3
"""
Front Matter 深度優化腳本 v2
- 修復不標準的 Front Matter
- 改進 category 分類
- 生成有價值的 tags
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path

def get_category_from_path(filepath):
    """根據路徑精確推斷類別"""
    path_str = str(filepath).lower()
    
    # 精確匹配
    if 'serper' in path_str:
        if 'api' in path_str:
            return 'serper-api'
        elif 'error' in path_str:
            return 'serper-errors'
        elif 'param' in path_str:
            return 'serper-params'
        else:
            return 'serper'
    elif 'javascript' in path_str or 'js-' in path_str:
        if 'es6' in path_str or 'es20' in path_str:
            return 'javascript-es'
        elif 'async' in path_str or 'promise' in path_str:
            return 'javascript-async'
        else:
            return 'javascript'
    elif 'douyin' in path_str or 'tiktok' in path_str:
        if 'select' in path_str:
            return 'douyin-selection'
        elif 'live' in path_str:
            return 'douyin-live'
        else:
            return 'douyin'
    elif 'evomap' in path_str:
        if 'publish' in path_str:
            return 'evomap-publish'
        elif 'gdi' in path_str:
            return 'evomap-gdi'
        elif 'asset' in path_str:
            return 'evomap-assets'
        else:
            return 'evomap'
    elif 'evolver' in path_str:
        return 'evolver'
    elif 'docker' in path_str:
        if 'layer' in path_str or 'cache' in path_str:
            return 'docker-cache'
        else:
            return 'docker'
    elif 'nodejs' in path_str or 'node-' in path_str:
        return 'nodejs'
    elif 'gmail' in path_str:
        if 'oauth' in path_str:
            return 'gmail-oauth'
        else:
            return 'gmail'
    elif 'feishu' in path_str:
        if 'gep' in path_str:
            return 'feishu-gep'
        else:
            return 'feishu'
    elif 'memory' in path_str:
        return 'memory'
    elif 'llm-wiki' in path_str or 'llm_wiki' in path_str:
        if 'protocol' in path_str:
            return 'llm-protocol'
        elif 'report' in path_str:
            return 'llm-reports'
        else:
            return 'llm'
    elif 'k8s' in path_str or 'kubernetes' in path_str:
        if 'health' in path_str:
            return 'k8s-health'
        elif 'resource' in path_str:
            return 'k8s-resources'
        else:
            return 'k8s'
    elif 'sql' in path_str:
        return 'database-sql'
    elif 'accident' in path_str or 'incident' in path_str:
        return 'accidents'
    elif 'learning' in path_str:
        return 'learning'
    elif 'concept' in path_str:
        return 'concepts'
    elif 'protocol' in path_str:
        return 'protocols'
    elif 'report' in path_str:
        return 'reports'
    elif 'gene' in path_str:
        return 'genes'
    elif 'capsule' in path_str:
        return 'capsules'
    elif 'script' in path_str:
        return 'scripts'
    elif 'schema' in path_str:
        return 'schemas'
    elif 'backup' in path_str:
        return 'backups'
    elif 'log' in path_str:
        return 'logs'
    elif 'task' in path_str:
        return 'tasks'
    elif 'deliberat' in path_str:
        return 'deliberations'
    elif 'brief' in path_str:
        return 'briefings'
    elif 'audit' in path_str:
        return 'audits'
    elif 'monetiz' in path_str:
        return 'monetization'
    elif 'rule' in path_str:
        return 'rules'
    else:
        return 'general'

def extract_keywords_from_content(content, max_keywords=5):
    """從內容提取關鍵詞作為 tags"""
    # 提取標題
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    keywords = []
    
    if title_match:
        title = title_match.group(1)
        # 從標題提取關鍵詞
        words = re.findall(r'[\w\u4e00-\u9fff]+', title)
        keywords.extend([w.lower() for w in words if len(w) > 1])
    
    # 從前 500 字提取關鍵詞
    first_part = content[:500].lower()
    important_words = ['api', 'guide', 'tutorial', 'report', 'analysis', 'protocol', 
                       'error', 'debug', 'optimize', 'deploy', 'setup', 'config',
                       'evomap', 'evolver', 'openclaw', 'serper', 'docker', 'k8s']
    
    for word in important_words:
        if word in first_part and word not in keywords:
            keywords.append(word)
    
    return keywords[:max_keywords]

def optimize_frontmatter(filepath):
    """優化文件的 Front Matter"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否有 Front Matter
        if not content.strip().startswith('---'):
            # 添加新的 Front Matter
            filename = os.path.basename(filepath)
            title = os.path.splitext(filename)[0].replace('-', ' ').replace('_', ' ').title()
            category = get_category_from_path(filepath)
            today = datetime.now().strftime('%Y-%m-%d')
            keywords = extract_keywords_from_content(content)
            
            frontmatter = f"""---
title: "{title}"
type: "article"
category: "{category}"
tags: ["{category}", {', '.join([f'"{kw}"' for kw in keywords])}]
created_at: "{today}"
version: "1.0"
---

"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + content)
            return True, '已添加 Front Matter', category
        else:
            # 已有 Front Matter，嘗試優化
            try:
                # 解析現有 Front Matter
                match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if not match:
                    return False, 'Front Matter 格式錯誤', None
                
                fm_str = match.group(1)
                fm = yaml.safe_load(fm_str)
                
                if not fm:
                    return False, 'Front Matter 為空', None
                
                # 優化 category
                if fm.get('category') == 'general':
                    fm['category'] = get_category_from_path(filepath)
                
                # 優化 tags
                if fm.get('tags') == ['general', 'auto-generated']:
                    keywords = extract_keywords_from_content(content)
                    fm['tags'] = [fm['category']] + keywords
                
                # 重建 Front Matter
                new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False)
                new_content = f"---\n{new_fm}---\n{content[match.end():]}"
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True, '已優化 Front Matter', fm.get('category')
            except Exception as e:
                return False, f'解析失敗：{str(e)}', None
    
    except Exception as e:
        return False, f'錯誤：{str(e)}', None

def main():
    wiki_dir = '/home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/wiki'
    
    total = 0
    success = 0
    skipped = 0
    errors = 0
    categories = {}
    
    print(f"🔍 開始優化 {wiki_dir}...")
    print(f"   這可能需要幾分鐘，請耐心等待\n")
    
    for root, dirs, files in os.walk(wiki_dir):
        # 跳過 node_modules 等目錄
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__']]
        
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                total += 1
                
                result, msg, category = optimize_frontmatter(filepath)
                
                if result:
                    success += 1
                    if category:
                        categories[category] = categories.get(category, 0) + 1
                    if success <= 5:
                        print(f"  ✅ {filepath[:80]}... → {category}")
                else:
                    if '解析失敗' in msg or '錯誤' in msg:
                        errors += 1
                        if errors <= 5:
                            print(f"  ❌ {filepath[:80]}... → {msg}")
                    else:
                        skipped += 1
    
    print(f"\n📊 優化結果:")
    print(f"  總文件數：{total}")
    print(f"  成功優化：{success} ({success * 100 // total if total > 0 else 0}%)")
    print(f"  已跳過：{skipped}")
    print(f"  錯誤：{errors}")
    
    print(f"\n📁 類別分佈 (Top 10):")
    sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]
    for cat, count in sorted_cats:
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    main()

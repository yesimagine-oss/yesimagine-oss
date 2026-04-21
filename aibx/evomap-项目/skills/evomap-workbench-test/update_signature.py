#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修改 Markdown 文件签名格式
将签名调整为右对齐 + 小字体
"""

import os
from pathlib import Path

# 新旧签名格式
OLD_SIGNATURE = """🦞 RedOpenClaw
...生活太快⚡️...老逼快跑💨..."""

NEW_SIGNATURE = """<div align="right"><small>🦞 RedOpenClaw<br>...生活太快⚡️...老逼快跑💨...</small></div>"""

def update_signature(file_path):
    """更新文件签名"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if OLD_SIGNATURE in content:
        content = content.replace(OLD_SIGNATURE, NEW_SIGNATURE)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# 发布包目录
release_dir = Path("/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/skills/evomap-workbench-release")

# 查找所有 Markdown 文件
md_files = list(release_dir.rglob("*.md"))

print(f"=== 批量修改签名格式 ===\n")
print(f"找到 {len(md_files)} 个 Markdown 文件\n")

updated = 0
for md_file in md_files:
    if update_signature(md_file):
        print(f"✅ {md_file.name}")
        updated += 1
    else:
        print(f"⚠️ {md_file.name} (无签名或已更新)")

print(f"\n✅ 完成：{updated}/{len(md_files)} 个文件已更新")

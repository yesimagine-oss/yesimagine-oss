#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
self-improving-agent 每週回顧優化腳本

功能:
- 回顧本週所有學習和錯誤記錄
- 統計數據（新增數量、解決數量、提升數量）
- 識別重複發生的問題
- 建議需要提升到長期記憶的學習
- 生成週報

使用:
    python3 weekly-review.py
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# 配置
LEARNINGS_DIR = Path.home() / ".openclaw" / "workspace" / ".learnings"
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"

def get_week_range() -> Tuple[datetime, datetime]:
    """獲取本週的開始和結束日期"""
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())  # 週一開始
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=7)
    return start_of_week, end_of_week

def parse_entry_date(file_path: Path, entry_content: str) -> datetime:
    """從條目內容中解析日期"""
    import re
    # 查找 **Logged**: 2026-03-20T10:27:00+08:00
    match = re.search(r'\*\*Logged\*\*:\s*(\d{4}-\d{2}-\d{2})', entry_content)
    if match:
        return datetime.strptime(match.group(1), '%Y-%m-%d')
    return None

def read_markdown_entries(file_path: Path) -> List[Dict]:
    """讀取 markdown 文件中的所有條目"""
    if not file_path.exists():
        return []
    
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割條目（## 開頭的標題）
    entry_blocks = content.split('\n## ')[1:]  # 跳過第一個空塊
    
    for block in entry_blocks:
        lines = block.split('\n')
        title = lines[0].strip()
        
        # 提取優先級和狀態
        priority = None
        status = None
        for line in lines[:20]:  # 在前 20 行查找
            if '**Priority**:' in line:
                priority = line.split('**Priority**:')[1].strip()
            if '**Status**:' in line:
                status = line.split('**Status**:')[1].strip()
        
        # 解析日期
        date = parse_entry_date(file_path, block)
        
        entries.append({
            'title': title,
            'priority': priority,
            'status': status,
            'date': date,
            'content': block
        })
    
    return entries

def filter_week_entries(entries: List[Dict], start: datetime, end: datetime) -> List[Dict]:
    """過濾出本週的條目"""
    week_entries = []
    for entry in entries:
        if entry['date'] and start <= entry['date'] < end:
            week_entries.append(entry)
    return week_entries

def generate_weekly_report(learnings: List[Dict], errors: List[Dict], features: List[Dict]) -> str:
    """生成週報"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 統計數據
    total_learnings = len(learnings)
    total_errors = len(errors)
    total_features = len(features)
    
    pending_count = sum(1 for e in learnings + errors if e.get('status') == 'pending')
    resolved_count = sum(1 for e in learnings + errors if e.get('status') == 'resolved')
    promoted_count = sum(1 for e in learnings + errors if e.get('status') == 'promoted')
    
    high_priority = [e for e in learnings + errors if e.get('priority') in ['high', 'critical']]
    
    report = f"""
# self-improving-agent 週報

**生成時間**: {now}
**回顧週期**: {get_week_range()[0].strftime('%Y-%m-%d')} 至 {get_week_range()[1].strftime('%Y-%m-%d')}

---

## 📊 本週統計

| 類別 | 數量 |
|------|------|
| **學習記錄** | {total_learnings} 條 |
| **錯誤記錄** | {total_errors} 條 |
| **功能請求** | {total_features} 條 |
| **總計** | {total_learnings + total_errors + total_features} 條 |

---

## ✅ 處理狀態

| 狀態 | 數量 | 佔比 |
|------|------|------|
| **待解決** | {pending_count} | {pending_count / max(1, total_learnings + total_errors) * 100:.1f}% |
| **已解決** | {resolved_count} | {resolved_count / max(1, total_learnings + total_errors) * 100:.1f}% |
| **已提升** | {promoted_count} | {promoted_count / max(1, total_learnings + total_errors) * 100:.1f}% |

---

## 🔴 高優先級項目

"""
    
    if high_priority:
        for entry in high_priority[:10]:  # 最多顯示 10 個
            report += f"### {entry['title']}\n"
            report += f"- **優先級**: {entry['priority']}\n"
            report += f"- **狀態**: {entry['status']}\n"
            if entry['date']:
                report += f"- **日期**: {entry['date'].strftime('%Y-%m-%d')}\n"
            report += "\n"
    else:
        report += "本週無高優先級項目 ✅\n\n"
    
    # 建議提升的學習
    report += """
---

## 💡 建議提升到長期記憶

以下學習建議提升到 `AGENTS.md` / `TOOLS.md` / `MEMORY.md`：

"""
    
    # 找出待解決的高價值學習
    pending_high_value = [e for e in learnings if e.get('status') == 'pending' and e.get('priority') in ['high', 'critical']]
    
    if pending_high_value:
        for entry in pending_high_value[:5]:  # 最多顯示 5 個
            report += f"### {entry['title']}\n"
            report += f"- **原因**: 高優先級，影響重大\n"
            report += f"- **建議提升到**: `MEMORY.md` 或 `TOOLS.md`\n"
            report += "\n"
    else:
        report += "本週無需要提升的學習 ✅\n\n"
    
    # 重複發生的問題
    report += """
---

## ⚠️ 重複發生的問題

"""
    
    # 簡單的重複檢測（基於標題關鍵詞）
    title_keywords = {}
    for entry in learnings + errors:
        keywords = entry['title'].split('-')[0].strip()
        if keywords not in title_keywords:
            title_keywords[keywords] = 0
        title_keywords[keywords] += 1
    
    recurring = {k: v for k, v in title_keywords.items() if v > 1}
    
    if recurring:
        for keyword, count in recurring.items():
            report += f"- **{keyword}**: 出現 {count} 次\n"
        report += "\n**建議**: 這些問題重複發生，需要系統性解決方案。\n\n"
    else:
        report += "本週無重複發生的問題 ✅\n\n"
    
    # 下週行動建議
    report += """
---

## 📋 下週行動建議

1. **解決待解決項目** - 優先處理高優先級的 {pending_count} 個待解決項目
2. **提升重要學習** - 將高價值學習提升到長期記憶
3. **重複問題分析** - 對重複發生的問題進行系統性分析
4. **清理過時記錄** - 歸檔或刪除過時的學習記錄

---

**生成工具**: `weekly-review.py`
**下次回顧**: 下週一 09:00
"""
    
    return report

def main():
    """主函數"""
    start_week, end_week = get_week_range()
    
    print(f"\n📊 self-improving-agent 每週回顧")
    print(f"回顧週期：{start_week.strftime('%Y-%m-%d')} 至 {end_week.strftime('%Y-%m-%d')}\n")
    
    # 讀取所有記錄
    learnings = read_markdown_entries(LEARNINGS_DIR / "LEARNINGS.md")
    errors = read_markdown_entries(LEARNINGS_DIR / "ERRORS.md")
    features = read_markdown_entries(LEARNINGS_DIR / "FEATURE_REQUESTS.md")
    
    # 過濾本週記錄
    week_learnings = filter_week_entries(learnings, start_week, end_week)
    week_errors = filter_week_entries(errors, start_week, end_week)
    week_features = filter_week_entries(features, start_week, end_week)
    
    # 生成週報
    report = generate_weekly_report(week_learnings, week_errors, week_features)
    
    # 保存到文件
    report_file = WORKSPACE_DIR / f"weekly-review-{start_week.strftime('%Y-%m-%d')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n✅ 週報已保存到：{report_file}")
    
    # 如果有待解決的高優先級項目，發送通知
    pending_high = [e for e in week_learnings + week_errors if e.get('status') == 'pending' and e.get('priority') in ['high', 'critical']]
    
    if pending_high:
        print(f"\n⚠️ 發現 {len(pending_high)} 個待解決的高優先級項目，請儘快處理！")

if __name__ == "__main__":
    main()

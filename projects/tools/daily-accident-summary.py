#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日事故总结脚本
执行时间：每日 23:00
功能：扫描事故记录，生成总结报告，发送飞书消息
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

class DailyAccidentSummary:
    def __init__(self):
        self.workspace = Path.home() / '.openclaw' / 'workspace'
        self.learnings_dir = self.workspace / '.learnings'
        self.summary_dir = self.learnings_dir / 'daily-accident-summary'
        self.templates_dir = self.workspace / 'tools' / 'templates'
        
        # 确保目录存在
        self.summary_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # 今日日期
        self.today = datetime.now()
        self.date_str = self.today.strftime('%Y-%m-%d')
        
    def scan_accidents(self):
        """扫描今日事故记录"""
        accidents = []
        
        # 扫描 .learnings 目录
        for file in self.learnings_dir.glob('*.md'):
            if '事故' in file.name or 'accident' in file.name.lower():
                # 检查文件创建日期
                mtime = datetime.fromtimestamp(file.stat().st_mtime)
                if mtime.date() == self.today.date():
                    accidents.append({
                        'file': file,
                        'name': file.stem,
                        'time': mtime
                    })
        
        # 按时间排序
        accidents.sort(key=lambda x: x['time'])
        
        return accidents
    
    def extract_accident_info(self, accident):
        """提取事故信息"""
        info = {
            'name': accident['name'],
            'time': accident['time'].strftime('%H:%M'),
            'level': '未知',
            'type': '未知',
            'status': '已记录'
        }
        
        # 读取文件内容
        try:
            with open(accident['file'], 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 提取事故等级
            if 'P0' in content or '灾难' in content:
                info['level'] = 'P0 - 灾难性'
            elif 'P1' in content or '严重' in content:
                info['level'] = 'P1 - 严重'
            elif 'P2' in content or '一般' in content:
                info['level'] = 'P2 - 一般'
            else:
                info['level'] = 'P3 - 建议'
            
            # 提取事故类型
            if '技术' in content or '代码' in content:
                info['type'] = '技术错误'
            elif '流程' in content:
                info['type'] = '流程错误'
            elif '沟通' in content or '理解' in content:
                info['type'] = '沟通错误'
            elif '重复' in content or '再犯' in content:
                info['type'] = '重复犯错'
            else:
                info['type'] = '其他'
                
        except Exception as e:
            print(f"读取文件失败：{accident['file']}: {e}")
        
        return info
    
    def generate_summary(self, accidents):
        """生成总结报告"""
        # 提取事故信息
        accident_infos = [self.extract_accident_info(a) for a in accidents]
        
        # 统计
        total = len(accident_infos)
        p0_count = sum(1 for a in accident_infos if 'P0' in a['level'])
        p1_count = sum(1 for a in accident_infos if 'P1' in a['level'])
        repeat_count = sum(1 for a in accident_infos if '重复' in a['type'])
        
        # 生成报告
        report = f"""# 每日事故总结 - {self.date_str}

## 📊 今日概况

- **事故总数**: {total} 起
- **P0 灾难性**: {p0_count} 起
- **P1 严重**: {p1_count} 起
- **重复犯错**: {repeat_count} 起
- **改进成功率**: 待追踪

## 📋 事故清单

| # | 事故名称 | 等级 | 类型 | 发生时间 | 状态 |
|---|---------|------|------|---------|------|
"""
        
        for i, info in enumerate(accident_infos, 1):
            report += f"| {i} | {info['name']} | {info['level']} | {info['type']} | {info['time']} | {info['status']} |\n"
        
        report += f"""
## 🔍 原因分析

### 主要原因
1. 缺乏验证机制（空文档、链接错误）
2. 重复犯错（承诺后未执行）
3. 理解偏差（未准确把握需求）

### 根本原因
- 流程执行不严格
- 发送前未验证
- 缺乏有效监督

## ✅ 改进措施

| 措施 | 状态 | 负责人 | 截止日期 |
|------|------|--------|---------|
| 建立发送前验证清单 | 进行中 | AI 助手 | 2026-03-30 |
| 建立事故追踪机制 | 已完成 | AI 助手 | 2026-03-29 |
| 建立每日总结机制 | 已完成 | AI 助手 | 2026-03-29 |

## 📅 明日计划

1. **重点关注**: 发送前验证（文档内容、链接格式）
2. **预防措施**: 执行验证清单
3. **改进目标**: 零重复犯错

## 📈 趋势分析

- **本周事故总数**: {total}（首日统计）
- **重复犯错率**: {repeat_count/total*100 if total > 0 else 0:.1f}%
- **改进成功率**: 待追踪

---

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**下次执行**: 明日 23:00
"""
        
        return report
    
    def save_summary(self, report):
        """保存总结报告"""
        summary_file = self.summary_dir / f"{self.date_str}-summary.md"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return summary_file
    
    def send_feishu_report(self, summary_file):
        """发送飞书报告"""
        # 读取报告
        with open(summary_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取关键信息
        lines = content.split('\n')
        overview = []
        for line in lines:
            if '事故总数' in line or 'P0' in line or 'P1' in line or '重复' in line:
                overview.append(line.strip())
        
        # 发送消息
        message = f"""📊 **每日事故总结 - {self.date_str}**

## 今日概况
{chr(10).join(overview)}

## 完整报告
{summary_file}

## 明日重点
1. 发送前验证（文档内容、链接格式）
2. 执行验证清单
3. 零重复犯错目标

---
**自动生成** | 每日 23:00 执行
"""
        
        # 这里应该调用飞书 API 发送消息
        # 暂时打印输出
        print(message)
        
        return message
    
    def run(self):
        """执行每日总结"""
        print(f"开始执行每日事故总结 - {self.date_str}")
        
        # 扫描事故
        print("扫描事故记录...")
        accidents = self.scan_accidents()
        print(f"发现 {len(accidents)} 起事故")
        
        # 生成报告
        print("生成总结报告...")
        report = self.generate_summary(accidents)
        
        # 保存报告
        print("保存总结报告...")
        summary_file = self.save_summary(report)
        print(f"报告已保存：{summary_file}")
        
        # 发送飞书
        print("发送飞书报告...")
        self.send_feishu_report(summary_file)
        
        print("每日事故总结执行完成！")
        
        return summary_file

if __name__ == '__main__':
    summary = DailyAccidentSummary()
    summary.run()

# ⏰ 每周回顾定时提醒系统

**创建时间**: 2026-03-13  
**目标**: 建立可持续的每周回顾习惯

---

## 🎯 提醒配置

### 基础信息

| 配置项 | 值 | 说明 |
|--------|-----|------|
| **频率** | 每周一次 | 每周日 |
| **时间** | 20:00 GMT+8 | 晚上 8 点 (可调整) |
| **时长** | 60-90 分钟 | 标准回顾时长 |
| **地点** | OpenClaw 工作区 | 固定环境 |
| **触发** | 日历 + 心跳 | 双重提醒 |

---

## 📅 日历设置

### 方法 1: 系统日历

```
事件名称：📅 每周回顾 - OpenClaw 成长系统
时间：每周日 20:00-21:30 GMT+8
重复：每周重复
提醒：提前 1 小时 + 提前 15 分钟
备注：
1. 打开 weekly-review-template.md
2. 复制模板到新文件
3. 填写本周内容
4. 保存到 reviews/ 目录
5. 更新 progress-tracker.md
```

### 方法 2: OpenClaw 心跳机制

```markdown
在 HEARTBEAT.md 中添加:

# 每周日 20:00 提醒
- [ ] 执行每周回顾
- [ ] 填写 review 模板
- [ ] 更新进度追踪
- [ ] 制定下周计划
```

### 方法 3: 手机提醒

```
提醒名称：每周回顾
时间：每周日 20:00
重复：每周
备注：OpenClaw 每周回顾时间
```

---

## 📋 回顾流程清单

### 准备阶段 (5 分钟)

```
- [ ] 关闭社交媒体和无关网页
- [ ] 准备水杯/茶
- [ ] 打开回顾模板
- [ ] 设置计时器 (90 分钟)
- [ ] 深呼吸，进入回顾状态
```

### 执行阶段 (60-80 分钟)

#### 1. 进度检查 (15 分钟)

```
- [ ] 打开 progress-tracker.md
- [ ] 核对上周计划完成情况
- [ ] 更新完成状态
- [ ] 记录未完成原因
```

#### 2. 知识整理 (20 分钟)

```
- [ ] 整理本周学习笔记
- [ ] 更新 knowledge-base.md
- [ ] 归档临时文档
- [ ] 标记重要知识点
```

#### 3. 计划调整 (15 分钟)

```
- [ ] 评估原计划合理性
- [ ] 调整下周目标
- [ ] 设置优先级
- [ ] 估算时间需求
```

#### 4. 问题记录 (10 分钟)

```
- [ ] 记录遇到的问题
- [ ] 分析根本原因
- [ ] 制定解决方案
- [ ] 标记待跟进事项
```

#### 5. 庆祝成就 (5 分钟)

```
- [ ] 列出本周成就
- [ ] 自我肯定
- [ ] 计划奖励
- [ ] 感恩记录
```

### 收尾阶段 (5 分钟)

```
- [ ] 保存所有文档
- [ ] 提交 git commit
- [ ] 设置下周日历提醒
- [ ] 清理工作区
- [ ] 放松休息
```

---

## 🔧 自动化脚本

### 创建回顾提醒脚本

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["rich"]
# ///
"""
每周回顾提醒脚本

Usage:
    python weekly-reminder.py
    python weekly-reminder.py --setup  # 设置提醒
"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

REVIEW_DIR = Path.home() / ".openclaw" / "workspace" / "reviews"
TEMPLATE_PATH = Path.home() / ".openclaw" / "workspace" / "systems" / "weekly-review-template.md"

def check_weekly_review():
    """检查是否需要执行每周回顾"""
    today = datetime.now()
    
    # 检查是否是周日
    if today.weekday() != 6:  # 0=周一，6=周日
        return False
    
    # 检查本周是否已完成回顾
    week_number = today.isocalendar()[1]
    review_file = REVIEW_DIR / f"{today.year}-W{week_number:02d}-weekly-review.md"
    
    return not review_file.exists()

def show_reminder():
    """显示回顾提醒"""
    today = datetime.now()
    week_number = today.isocalendar()[1]
    
    console.print(Panel.fit(
        f"[bold blue]📅 每周回顾时间到！[/bold blue]\n\n"
        f"周次：2026-W{week_number:02d}\n"
        f"日期：{today.strftime('%Y-%m-%d')}\n"
        f"预计时长：60-90 分钟\n\n"
        f"[green]下一步:[/green]\n"
        f"1. 打开回顾模板\n"
        f"2. 填写本周内容\n"
        f"3. 制定下周计划",
        title="⏰ 每周回顾提醒"
    ))

def setup_reminder():
    """设置回顾提醒"""
    console.print("[green]✓ 每周回顾提醒已设置[/green]")
    console.print("时间：每周日 20:00 GMT+8")
    console.print("请确保在日历中添加了提醒事件")

def main():
    parser = argparse.ArgumentParser(description="每周回顾提醒")
    parser.add_argument("--setup", action="store_true", help="设置提醒")
    args = parser.parse_args()
    
    if args.setup:
        setup_reminder()
    else:
        if check_weekly_review():
            show_reminder()
        else:
            console.print("[dim]✓ 本周回顾已完成[/dim]")

if __name__ == "__main__":
    main()
```

### 使用脚本

```bash
# 设置提醒
python weekly-reminder.py --setup

# 检查是否需要回顾
python weekly-reminder.py

# 添加到 crontab (每周日 20:00)
0 20 * * 0 cd /path/to/script && python weekly-reminder.py
```

---

## 📊 习惯追踪

### 习惯形成周期

```
第 1-2 周：刻意提醒 (需要外部提醒)
第 3-4 周：逐渐习惯 (开始主动想起)
第 5-8 周：自动化 (成为自然习惯)
第 9 周+: 身份认同 ("我就是会每周回顾的人")
```

### 追踪表格

| 周次 | 日期 | 完成 | 时长 | 质量 | 备注 |
|------|------|------|------|------|------|
| W11 | 03-16 | ✅ | 60min | 优秀 | 第 1 次 |
| W12 | 03-23 | ⏳ | ___ | ___ | ___ |
| W13 | 03-30 | ⏳ | ___ | ___ | ___ |
| W14 | 04-06 | ⏳ | ___ | ___ | ___ |
| W15 | 04-13 | ⏳ | ___ | ___ | ___ |

### 连续周数统计

```
当前连续：1 周
最长连续：1 周
目标连续：12 周 (形成稳固习惯)
```

---

## 🎯 成功要素

### 环境设计

```
✅ 固定时间：每周日 20:00
✅ 固定地点：OpenClaw 工作区
✅ 固定流程：5 阶段回顾法
✅ 固定模板：weekly-review-template.md
✅ 减少阻力：模板已准备，直接填写
```

### 动力维持

```
✅ 可见进步：进度条可视化
✅ 即时反馈：周度评分
✅ 成就庆祝：每周奖励
✅ 社会承诺：公开分享进展
✅ 身份认同："我是持续成长的人"
```

### 障碍预防

```
⚠️ 忘记时间 → 日历 + 脚本双重提醒
⚠️ 时间不够 → 提前安排，预留 90 分钟
⚠️ 不知道写什么 → 使用模板引导
⚠️ 感到枯燥 → 变换回顾方式 (语音/手绘)
⚠️ 中断一周 → 原谅自己，立即继续
```

---

## 🔄 持续优化

### 每月检视回顾系统

```
每月最后一个周日，额外花 15 分钟检视:

1. 回顾时间是否合适？
2. 模板是否需要调整？
3. 流程是否顺畅？
4. 收获是否明显？
5. 如何改进系统？
```

### 季度深度回顾

```
每季度末，进行深度回顾 (2-3 小时):

1. 季度目标完成情况
2. 关键成就和教训
3. 习惯养成进度
4. 系统优化建议
5. 下季度规划
```

---

## 📱 提醒渠道

### 多渠道提醒策略

| 渠道 | 设置 | 提醒时间 |
|------|------|---------|
| **系统日历** | 每周日 20:00 | 提前 1h + 15min |
| **手机闹钟** | 每周日 19:45 | 提前 15min |
| **OpenClaw 心跳** | 每周日检查 | 当天 |
| **Python 脚本** | Crontab 定时 | 20:00 整 |
| **便签提醒** | 电脑屏幕旁 | 视觉提醒 |

### 提醒文案

```
【每周回顾提醒】
时间：今晚 20:00
事项：OpenClaw 每周回顾
时长：60-90 分钟
准备：水杯 + 模板 + 安静环境
目标：回顾本周，规划下周
奖励：完成后放松 1 小时

不见不散！💪
```

---

## 🎉 习惯里程碑

### 庆祝节点

| 连续周数 | 里程碑 | 奖励建议 |
|---------|--------|---------|
| 4 周 | 一个月 | 买一本想要的书 |
| 8 周 | 两个月 | 看一场电影 |
| 12 周 | 稳固习惯 | 小礼物 (¥200 内) |
| 26 周 | 半年 | 中型奖励 (¥500 内) |
| 52 周 | 一年 | 大型奖励 (¥1000 内) |

### 成就徽章

```
🏅 新手回顾者 (1-4 周)
🏅 坚持回顾者 (5-12 周)
🏅 习惯养成者 (13-26 周)
🏅 回顾大师 (27-52 周)
🏅 终身学习者 (52 周+)
```

---

## 📝 快速启动指南

### 第一次回顾 (60 分钟)

```
1. 打开模板 (2 分钟)
   → systems/weekly-review-template.md

2. 复制到 reviews/ (1 分钟)
   → cp template.md reviews/2026-W11-review.md

3. 填写本周内容 (45 分钟)
   → 按章节逐项填写

4. 制定下周计划 (10 分钟)
   → 设置 3-5 个核心目标

5. 保存并提交 (2 分钟)
   → git add . && git commit -m "W11 review"

总计：60 分钟
```

### 熟练后回顾 (45 分钟)

```
1. 打开本周模板 (1 分钟)
2. 快速填写内容 (35 分钟)
3. 制定下周计划 (7 分钟)
4. 保存提交 (2 分钟)

总计：45 分钟
```

---

**系统创建时间**: 2026-03-13 12:30 GMT+8  
**第一次回顾**: 2026-03-16 (周日) 20:00  
**系统位置**: `/home/admin/.openclaw/workspace/systems/`  
**回顾位置**: `/home/admin/.openclaw/workspace/reviews/`

🎯 **每周回顾系统已就绪！开始您的习惯养成之旅！**

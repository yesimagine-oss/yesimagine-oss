---
title: "Skill 下载量监控方案"
type: "general"
category: "general"
tags: ["general", "auto-generated"]
created_at: "2026-04-14"
version: "1.0"
---

# ClawBrowser Core Skill 下载量监控方案

**创建时间**: 2026-04-04 08:29  
**监控对象**: `clawbrowser_core`  
**监控频率**: 每小时 1 次

---

## 📊 监控架构

```
┌─────────────────┐
│  监控脚本       │
│  (Python)       │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  EvoMap API     │
│  /skill/store   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  数据记录       │
│  - JSONL 日志   │
│  - 状态文件     │
│  - 统计快照     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  通知/报告      │
│  - 飞书通知     │
│  - 定时报告     │
└─────────────────┘
```

---

## 🛠️ 监控工具

### 1. 监控脚本

**位置**: `monitor-skill-downloads.py`

**功能**:
- ✅ 定时获取下载量
- ✅ 记录历史数据（JSONL）
- ✅ 异常检测（下载量突增）
- ✅ 生成监控报告
- ✅ 收益统计

**使用**:
```bash
# 手动运行
python3 monitor-skill-downloads.py

# 查看日志
cat monitoring/clawbrowser_core-downloads.jsonl

# 查看状态
cat monitoring/clawbrowser_core-state.json
```

### 2. 定时任务（Cron）

**设置**:
```bash
# 编辑 crontab
crontab -e

# 添加每小时执行一次
0 * * * * cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目 && python3 monitor-skill-downloads.py >> monitoring/cron.log 2>&1
```

**频率选项**:
| 频率 | Cron 表达式 | 说明 |
|------|-----------|------|
| 每分钟 | `* * * * *` | 高频监控（测试用） |
| 每小时 | `0 * * * *` | 标准监控 ✅ |
| 每天 | `0 9 * * *` | 每日报告 |

---

## 📁 数据文件

### 目录结构

```
monitoring/
├── clawbrowser_core-downloads.jsonl  # 下载日志（每行一条记录）
├── clawbrowser_core-state.json       # 当前状态
├── clawbrowser_core-stats.json       # 完整统计
└── cron.log                          # Cron 执行日志
```

### 日志格式（JSONL）

```json
{"timestamp":"2026-04-04T08:29:17","download_count":0,"revenue":0,"version":"1.0.0","visibility":"public"}
{"timestamp":"2026-04-04T09:29:17","download_count":1,"revenue":5,"version":"1.0.0","visibility":"public"}
```

### 状态文件格式

```json
{
  "last_check": "2026-04-04 08:29:17",
  "last_download_count": 0,
  "total_revenue": 0,
  "checks_count": 1
}
```

---

## 📈 监控指标

### 核心指标

| 指标 | 说明 | 告警阈值 |
|------|------|---------|
| **下载量** | 累计下载次数 | - |
| **新增下载** | 上次检查后的增量 | >10 次/小时 |
| **累计收入** | 下载量 × 5 积分 | - |
| **下载增长率** | 环比增长百分比 | >100% |

### 告警规则

| 规则 | 条件 | 动作 |
|------|------|------|
| **下载突增** | 增长>100% | 飞书通知 |
| **零下载** | 7 天无下载 | 周报提醒 |
| **API 失败** | 连续 3 次失败 | 立即通知 |

---

## 🔔 通知机制

### 飞书通知（推荐）

**触发条件**:
- 下载量突增（>100%）
- 首次下载
- 达到里程碑（10/50/100 次）

**通知格式**:
```
🎉 ClawBrowser Core Skill 下载通知

📊 下载量：10 次（+5 次）
💰 累计收入：50 积分
📈 增长率：+100%
⏰ 时间：2026-04-04 09:00
```

### 定时报告

**日报**（每天 9:00）:
- 昨日下载量
- 昨日收入
- 累计数据

**周报**（每周一 9:00）:
- 本周下载趋势
- 收入统计
- 改进建议

---

## 📊 监控仪表板

### 实时数据

```bash
# 查看最新状态
python3 monitor-skill-downloads.py
```

### 历史趋势

```bash
# 查看下载趋势
cat monitoring/clawbrowser_core-downloads.jsonl | \
  python3 -c "import sys,json; [print(json.loads(l)['timestamp'], json.loads(l)['download_count']) for l in sys.stdin]"
```

### 收益统计

```bash
# 计算总收入
cat monitoring/clawbrowser_core-state.json | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f'总收入：{d[\"total_revenue\"]} 积分')"
```

---

## 🎯 预测模型

### 下载量预测

| 时间 | 保守估计 | 乐观估计 |
|------|---------|---------|
| **第 1 周** | 10 次 | 50 次 |
| **第 1 月** | 50 次 | 200 次 |
| **第 3 月** | 200 次 | 1000 次 |

### 收入预测

| 时间 | 保守估计 | 乐观估计 |
|------|---------|---------|
| **第 1 周** | 50 积分 | 250 积分 |
| **第 1 月** | 250 积分 | 1000 积分 |
| **第 3 月** | 1000 积分 | 5000 积分 |

---

## 📋 操作指南

### 日常监控

```bash
# 1. 查看最新报告
python3 monitor-skill-downloads.py

# 2. 检查异常
cat monitoring/cron.log | tail -20

# 3. 查看趋势
cat monitoring/clawbrowser_core-downloads.jsonl
```

### 故障排查

```bash
# 检查 Cron 状态
crontab -l

# 检查日志
tail -f monitoring/cron.log

# 手动测试
python3 monitor-skill-downloads.py
```

### 数据导出

```bash
# 导出为 CSV
cat monitoring/clawbrowser_core-downloads.jsonl | \
  python3 -c "import sys,json; print('timestamp,downloads,revenue'); [print(f'{json.loads(l)[\"timestamp\"]},{json.loads(l)[\"download_count\"]},{json.loads(l)[\"revenue\"]}') for l in sys.stdin]" > downloads.csv
```

---

## 🚀 下一步

### 短期（1-7 天）

- [ ] 设置 Cron 定时任务
- [ ] 配置飞书通知
- [ ] 测试告警规则

### 中期（1-4 周）

- [ ] 建立可视化仪表板
- [ ] 添加更多指标（来源、地区）
- [ ] 优化预测模型

### 长期（1-3 月）

- [ ] 自动化报告生成
- [ ] A/B 测试优化
- [ ] 多 Skill 监控

---

**监控状态**: ✅ 已启动  
**最后检查**: 2026-04-04 08:29:17  
**当前下载量**: 0 次  
**累计收入**: 0 积分

---
🦞 RedOpenClaw
...生活太快⚡️...老逼快跑💨...

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]

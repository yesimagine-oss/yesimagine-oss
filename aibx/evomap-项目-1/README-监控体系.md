---
title: "Readme 监控体系"
type: "general"
category: "general"
tags: ["general", "auto-generated"]
created_at: "2026-04-14"
version: "1.0"
---

# EvoMap 监控体系文档

**创建时间:** 2026-03-21 20:45  
**版本:** v1.0  

---

## 📊 监控体系架构

```
┌─────────────────────────────────────────────────────────┐
│                   监控仪表盘                              │
│  (status-dashboard.html - 实时显示所有任务状态)           │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼──────┐  ┌──────▼───────┐  ┌──────▼──────┐
│  主动监控     │  │  执行汇报     │  │  自动补救    │
│  task-monitor │  │  task-reporter│  │  auto-remediation│
└───────┬──────┘  ┌──────┴───────┐  ┌──────┴──────┐
        │         │                │
        │    ┌────▼────────────────▼────┐
        │    │      交叉验证机制          │
        │    │      validator.py        │
        │    └──────────────────────────┘
        │
┌───────▼──────────────────────────────┐
│          API 测试工具                  │
│          api-tester.py               │
└──────────────────────────────────────┘
```

---

## 📁 文件清单

### 监控脚本

| 文件 | 用途 | 执行方式 |
|------|------|---------|
| `scripts/task-monitor.py` | 主动监控（每 5 分钟） | `python3 task-monitor.py` |
| `scripts/task-reporter.py` | 执行汇报 | `python3 task-reporter.py --task xxx --status success` |
| `scripts/auto-remediation.py` | 失败自动补救 | `python3 auto-remediation.py task_name error` |
| `scripts/api-tester.py` | API 测试 | `python3 api-tester.py` |

### 库文件

| 文件 | 用途 |
|------|------|
| `lib/gep_a2a_client.py` | GEP-A2A 协议客户端 |
| `lib/validator.py` | 交叉验证机制 |

### 配置文件

| 文件 | 用途 |
|------|------|
| `scripts/auto-claim-task-v2.py` | 三层混合 Claim 脚本 |
| `crontab` | 定时任务配置 |

---

## 🔧 使用方法

### 1. 启动主动监控

```bash
cd /home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/scripts
python3 task-monitor.py
```

### 2. 汇报任务执行

```bash
# 成功
python3 task-reporter.py --task morning_check --status success --details "执行完成"

# 失败
python3 task-reporter.py --task auto_claim --status failed --details "API 404"

# 生成每日摘要
python3 task-reporter.py --daily-summary
```

### 3. 自动补救

```bash
python3 auto-remediation.py morning_check "脚本执行失败"
```

### 4. API 测试

```bash
# 测试所有端点
python3 api-tester.py

# 测试单个端点
python3 api-tester.py --endpoint "A2A Hello"

# 性能测试
python3 api-tester.py --performance --iterations 20
```

### 5. 交叉验证

```bash
# 验证 cron 状态
python3 lib/validator.py

# 在 Python 中使用
from lib.validator import validate_cron
result = validate_cron()
print(f"状态：{result['status']}, 置信度：{result['confidence']}")
```

---

## 📊 监控仪表盘

**文件:** `status-dashboard.html` (待创建)

**功能:**
- 实时显示所有任务状态
- 显示最近执行记录
- 显示告警信息
- 自动刷新（每 30 秒）

**访问:** `file:///home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/status-dashboard.html`

---

## 🎯 监控指标

### 任务执行指标

| 指标 | 目标 | 告警阈值 |
|------|------|---------|
| 任务执行率 | >95% | <90% |
| 任务成功率 | >90% | <80% |
| 平均执行延迟 | <2 分钟 | >5 分钟 |
| 补救成功率 | >80% | <60% |

### API 指标

| 指标 | 目标 | 告警阈值 |
|------|------|---------|
| API 可用性 | >99% | <95% |
| 平均响应时间 | <500ms | >2000ms |
| 错误率 | <1% | >5% |

### 系统指标

| 指标 | 目标 | 告警阈值 |
|------|------|---------|
| cron 在线率 | 100% | 离线 |
| 节点心跳 | 每 15 分钟 | >20 分钟 |
| 日志文件大小 | <100MB | >500MB |

---

## 🚨 告警流程

```
任务失败
  ↓
主动监控检测（5 分钟内）
  ↓
发送飞书告警
  ↓
自动补救执行
  ↓
补救成功 → 发送成功通知
  ↓
补救失败 → 发送失败通知 + 人工介入
```

---

## 📝 日志文件

| 日志文件 | 用途 | 位置 |
|---------|------|------|
| `task-monitor.log` | 主动监控日志 | `logs/` |
| `task-reporter.log` | 执行汇报日志 | `logs/` |
| `auto-remediation.log` | 自动补救日志 | `logs/` |
| `api-tester.log` | API 测试日志 | `logs/` |
| `execution_history.json` | 执行历史记录 | `logs/` |

---

## 🎓 培训材料

### 新手入门

1. 阅读本文档
2. 运行 `python3 api-tester.py` 测试 API
3. 运行 `python3 lib/validator.py` 测试验证
4. 查看 `logs/execution_history.json` 了解执行记录

### 故障排查

**问题 1: 任务未执行**
```bash
# 1. 检查 cron 状态
python3 lib/validator.py

# 2. 检查日志
tail -20 logs/cron_*.log

# 3. 手动执行
python3 scripts/morning_check.py
```

**问题 2: API 失败**
```bash
# 1. 测试 API
python3 api-tester.py

# 2. 检查节点状态
curl -X POST https://evomap.ai/a2a/hello \
  -H "Content-Type: application/json" \
  -d '{"protocol":"gep-a2a",...}'
```

**问题 3: 监控不工作**
```bash
# 1. 检查监控进程
ps aux | grep task-monitor

# 2. 查看监控日志
tail -50 logs/task-monitor.log

# 3. 重启监控
pkill task-monitor
python3 scripts/task-monitor.py &
```

---

## 📈 持续改进

### 每周检查

- [ ] 审查执行记录
- [ ] 分析失败原因
- [ ] 优化监控阈值
- [ ] 更新文档

### 每月优化

- [ ] 性能测试
- [ ] 代码审查
- [ ] 添加新监控项
- [ ] 培训新人

---

**文档版本:** v1.0  
**最后更新:** 2026-03-21 20:45  
**维护人:** AI 助手

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]

# OpenClaw Cron 命令详解

**学习时间**: 2026-03-12 11:36
**难度**: ⭐⭐ 中等
**预计时间**: 30 分钟

---

## 📋 命令概览

| 命令 | 功能 | 示例 |
|------|------|------|
| `openclaw cron add` | 添加定时任务 | 添加每日新闻推送 |
| `openclaw cron list` | 查看任务列表 | 查看所有任务 |
| `openclaw cron run` | 手动执行任务 | 立即测试任务 |
| `openclaw cron runs` | 查看执行历史 | 查看任务执行结果 |
| `openclaw cron delete` | 删除任务 | 删除不需要的任务 |

---

## 🔧 openclaw cron add

### 命令格式

```bash
openclaw cron add \
  --name "<任务名称>" \
  --cron "<Cron 表达式>" \
  --tz "<时区>" \
  --message "<提示词>" \
  --channel "<推送通道>" \
  --announce \
  --timeout-seconds <超时时间>
```

### 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| --name | ✅ | 任务名称 | `ai-daily-news` |
| --cron | ✅ | Cron 表达式 | `"0 9 * * *"` |
| --tz | ❌ | 时区 | `"Asia/Shanghai"` |
| --message | ✅ | 发送给 Agent 的提示词 | `"访问...获取..."` |
| --channel | ❌ | 推送通道 | `dingtalk`, `telegram` |
| --announce | ❌ | 将结果推送到通道 | - |
| --timeout-seconds | ❌ | 任务超时时间 | `120` |

### Cron 表达式参考

| 描述 | 表达式 |
|------|--------|
| 每分钟 | `* * * * *` |
| 每 5 分钟 | `*/5 * * * *` |
| 每小时 | `0 * * * *` |
| 每天 9 点 | `0 9 * * *` |
| 每周一 9 点 | `0 9 * * 1` |
| 每月 1 号 | `0 0 1 * *` |
| 工作日 9-17 点 | `0 9-17 * * 1-5` |

### 使用示例

#### 每日 AI 新闻推送

```bash
openclaw cron add \
  --name "ai-daily-news" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --message "请访问 https://www.aibase.com/zh/daily 获取今天的 AI 日报，总结前 10 条最重要的 AI 新闻，用简洁的中文列表形式输出，每条包含标题和一句话摘要" \
  --channel dingtalk \
  --announce \
  --timeout-seconds 120
```

#### 每周论文推送

```bash
openclaw cron add \
  --name "paper-digest" \
  --cron "0 9 * * 1" \
  --tz "Asia/Shanghai" \
  --message '请使用 curl 命令执行以下请求获取论文数据：
curl -s "http://export.arxiv.org/api/query?search_query=all:%22llm+as+a+judge%22&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
解析返回的 XML 数据，列出前 5 篇论文，每篇包含：
1. 标题
2. 发布日期
3. 摘要总结（用中文，2-3 句话概括核心贡献）
4. arXiv 链接' \
  --channel dingtalk \
  --announce \
  --timeout-seconds 120
```

#### 每小时健康检查

```bash
openclaw cron add \
  --name "health-check" \
  --cron "0 * * * *" \
  --message "检查系统状态，包括 CPU、内存、磁盘使用情况，如有异常发送告警" \
  --channel telegram \
  --announce \
  --timeout-seconds 60
```

---

## 📋 openclaw cron list

### 命令格式

```bash
openclaw cron list
```

### 输出示例

```json
{
  "crons": [
    {
      "id": "cron-abc123",
      "name": "ai-daily-news",
      "cron": "0 9 * * *",
      "timezone": "Asia/Shanghai",
      "enabled": true,
      "nextRun": "2026-03-13T09:00:00+08:00",
      "lastRun": "2026-03-12T09:00:00+08:00",
      "lastStatus": "ok"
    },
    {
      "id": "cron-def456",
      "name": "paper-digest",
      "cron": "0 9 * * 1",
      "timezone": "Asia/Shanghai",
      "enabled": true,
      "nextRun": "2026-03-16T09:00:00+08:00",
      "lastRun": "2026-03-09T09:00:00+08:00",
      "lastStatus": "ok"
    }
  ]
}
```

---

## ▶️ openclaw cron run

### 命令格式

```bash
openclaw cron run --id <任务 ID> --timeout <超时毫秒>
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| --id | ✅ | 任务 ID（从 list 获取） |
| --timeout | ❌ | 超时时间（毫秒） |

### 使用示例

```bash
# 获取任务 ID
openclaw cron list

# 手动执行任务
openclaw cron run --id cron-abc123 --timeout 120000
```

---

## 📊 openclaw cron runs

### 命令格式

```bash
openclaw cron runs --id <任务 ID>
```

### 输出示例

```json
{
  "runs": [
    {
      "id": "run-xyz789",
      "cronId": "cron-abc123",
      "status": "ok",
      "delivered": true,
      "startTime": "2026-03-12T09:00:00+08:00",
      "endTime": "2026-03-12T09:01:30+08:00",
      "duration": 90,
      "result": "新闻已成功推送到钉钉"
    }
  ]
}
```

---

## 🗑️ openclaw cron delete

### 命令格式

```bash
openclaw cron delete --id <任务 ID>
```

### 使用示例

```bash
# 删除任务
openclaw cron delete --id cron-abc123
```

---

## 🎯 实战案例

### 案例 1: 晨间报告

```bash
openclaw cron add \
  --name "morning-report" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --message "生成晨间报告，包含：1) 北京今天天气 2) 3 条科技新闻摘要 3) 今日日程安排 4) 友好问候语" \
  --channel telegram \
  --announce \
  --timeout-seconds 120
```

---

### 案例 2: 邮件摘要

```bash
openclaw cron add \
  --name "email-digest" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --message "检查最近的 10 封邮件，分析重要性，生成摘要清单，标注需要回复的邮件" \
  --channel telegram \
  --announce \
  --timeout-seconds 180
```

---

### 案例 3: 用量告警

```bash
openclaw cron add \
  --name "api-usage-alert" \
  --cron "0 20 * * *" \
  --tz "Asia/Shanghai" \
  --message "查询今日 API 用量，如超过¥10 发送告警通知" \
  --channel telegram \
  --announce \
  --timeout-seconds 60
```

---

### 案例 4: 备份提醒

```bash
openclaw cron add \
  --name "backup-reminder" \
  --cron "0 10 * * 0" \
  --tz "Asia/Shanghai" \
  --message "提醒进行每周备份，检查备份文件是否完整" \
  --channel telegram \
  --announce \
  --timeout-seconds 60
```

---

## ⚠️ 常见问题

### Q1: 任务不执行

**检查**:
```bash
# 查看任务状态
openclaw cron list

# 查看执行历史
openclaw cron runs --id <任务 ID>

# 查看日志
openclaw logs --grep cron
```

**解决**:
- 确认任务已启用
- 检查 Cron 表达式
- 验证时区设置

---

### Q2: 执行超时

**解决**:
```bash
# 增加超时时间
openclaw cron run --id <任务 ID> --timeout 300000
```

---

### Q3: 推送失败

**检查**:
```bash
# 检查通道状态
openclaw channels list
```

**解决**:
- 确认通道已启用
- 检查通道配置
- 验证网络连接

---

## ✅ 验收清单

- [ ] 理解 Cron 表达式
- [ ] 掌握 add 命令参数
- [ ] 能够查看任务列表
- [ ] 能够手动执行任务
- [ ] 能够查看执行历史
- [ ] 能够删除任务

---

**学习状态**: ✅ 已完成
**下一步**: 继续补充其他遗漏内容

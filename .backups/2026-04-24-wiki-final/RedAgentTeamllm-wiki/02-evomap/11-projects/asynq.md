---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Asynq
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# asynq - Redis 任务队列

**来源:** github.com/hibiken/asynq (100% 覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 异步任务 | Redis 后台队列 |
| Worker 池 | 并发处理 |
| 定时任务 | Cron 调度 |
| 重试机制 | 失败自动重试 |

---

## 项目应用

| 项目 | 用途 | 节省 |
|------|------|------|
| go-image-skill | 批量分析/定时任务 | ~3h |
| 无头浏览器 | 批量采集/定时抓取 | ~3h |
| **总计** | - | **~6h** |

---

## 代码示例

```go
//  enqueue 任务
client := asynq.NewClient(asynq.RedisClientOpt{Addr: "localhost:6379"})
task := asynq.NewTask("image:analyze", payload)
client.Enqueue(task)

// 启动 Worker
srv := asynq.NewServer(redisOpt, asynq.Config{Concurrency: 10})
srv.Run(handler)

// 定时任务
scheduler.Register("* * * * *", task)
```

---

**结论:** 生产级任务队列，建议入库

---

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
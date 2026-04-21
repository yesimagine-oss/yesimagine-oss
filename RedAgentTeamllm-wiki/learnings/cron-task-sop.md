# RedAgentTeamllm-wiki 定时任务 SOP

**版本**: v1.0  
**生效日期**: 2026-04-21  
**状态**: ✅ Active  
**维护者**: Red Agent Team  
**最后更新**: 2026-04-21 12:05 CST

---

## 1️⃣ 定时任务清单 (10 个)

| ID | 频率 | 时间 | 脚本 | 说明 | 优先级 |
|----|------|------|------|------|--------|
| **CRON-001** | `*/30 * * * *` | 每 30 分钟 | `evomap-monitor.py` | EvoMap 服务器限流监控 | P0 |
| **CRON-002** | `0 6:30 * * *` | 每日 06:30 | `monitor-skill-downloads.py` | Skill 下载量统计 | P1 |
| **CRON-003** | `0 3 * * *` | 每日 03:00 | `auto-backup.sh` | 知识库自动备份 (保留 7 天) | P0 |
| **CRON-004** | `0 4 * * *` | 每日 04:00 | `auto-ingest.py` | 知识自动入库 (6 大领域≥18 条) | P0 |
| **CRON-005** | `0 1 * * 0` | 周日 01:00 | `auto-lint.sh` | 健康检查 (孤页/矛盾/过时) | P1 |
| **CRON-006** | `0 6 * * *` | 每日 06:00 | `health-alert.sh` | 健康分告警 (<80 飞书通知) | P1 |
| **CRON-007** | `0 6 * * 0` | 周日 06:00 | `generate-weekly-report.sh` | 周报生成 (更新量/趋势) | P2 |
| **CRON-008** | `0 2 1 * *` | 1 日 02:00 | `auto-audit.sh` | 月度审计 + 归档>3 个月文件 | P1 |
| **CRON-009** | `0 6 1 * *` | 1 日 06:00 | `generate-monthly-report.sh` | 月报生成 (增长率/自动化率) | P2 |
| **CRON-010** | `0 9 21 * *` | 21 日 09:00 | `review-health-sop.sh` | SOP 月度审查 (优化建议) | P1 |

**知识入库领域 (CRON-004)**: llm-wiki-pattern / agent-development / ai-monetization / skill-development / openclaw-framework / llm-technology (6 领域 × 3 条 = 18 条/天)

---

## 2️⃣ 执行状态 (2026-04-21 12:05 更新)

| 任务 | 配置状态 | 执行状态 | 说明 |
|------|----------|----------|------|
| CRON-001 | ✅ 已安装 | ✅ 运行中 | 路径正确 |
| CRON-002 | ✅ 已更新 | ⏳ 待安装 | 时间调整为 06:30 |
| CRON-003 | ✅ 已更新 | ⏳ 待安装 | 时间调整为 03:00 |
| CRON-004 | ✅ 已更新 | ⏳ 待安装 | 时间调整为 04:00 + 6 大领域配置 |
| CRON-005 | ✅ 已更新 | ⏳ 待安装 | 路径修复 |
| CRON-006 | ✅ 已创建 | ⏳ 待安装 | 健康告警 |
| CRON-007 | ❌ 待创建 | ❌ 未执行 | 周报生成 |
| CRON-008 | ❌ 待创建 | ❌ 未执行 | 月度审计 |
| CRON-009 | ❌ 待创建 | ❌ 未执行 | 月报生成 |
| CRON-010 | ❌ 待创建 | ❌ 未执行 | SOP 审查 |

**配置确认**: ✅ 所有配置已更新，待用户执行 `crontab -e` 安装

---

## 3️⃣ 安装流程

### 步骤 1: 备份现有 Crontab

```bash
crontab -l > ~/cron-backup-$(date +%Y%m%d-%H%M%S).txt
```

### 步骤 2: 编辑 Crontab

```bash
crontab -e
```

### 步骤 3: 粘贴配置 (更新时间 2026-04-21 12:05)

```bash
# ============= EvoMap 监控 =============
*/30 * * * * cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目 && python3 scripts/evomap-monitor.py >> logs/evomap-monitor.log 2>&1
0 6:30 * * * cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目 && python3 monitor-skill-downloads.py >> monitoring/cron.log 2>&1

# ============= RedAgentTeamllm-wiki 自动化 =============
0 3 * * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/auto-backup.sh >> /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/backup.log 2>&1
0 4 * * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/auto-ingest.py >> /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/ingest.log 2>&1
0 1 * * 0 /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/auto-lint.sh >> /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/lint.log 2>&1

# ============= 健康监测 =============
0 6 * * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/health-alert.sh >> /tmp/wiki-alert.log 2>&1
0 6 * * 0 /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/generate-weekly-report.sh >> /tmp/wiki-report.log 2>&1
0 2 1 * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/auto-audit.sh >> /tmp/wiki-audit.log 2>&1
0 6 1 * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/generate-monthly-report.sh >> /tmp/wiki-report.log 2>&1
0 9 21 * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/review-health-sop.sh >> /tmp/wiki-sop-review.log 2>&1
```

### 步骤 4: 验证安装

```bash
# 查看已安装的 Crontab
crontab -l | wc -l  # 应显示 10 行

# 检查 Cron 服务状态
systemctl status cron
```

---

## 4️⃣ 监控与验证

### 每日检查 (06:30)

```bash
# 查看健康告警日志
tail -20 /tmp/wiki-alert.log

# 查看 Lint 日志
tail -20 /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/lint.log
```

### 每周检查 (周日 07:00)

```bash
# 查看周报是否生成
ls -lt /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/reports/weekly-*.md | head -1
```

### 每月检查 (1 日 07:00)

```bash
# 查看月报是否生成
ls -lt /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/reports/monthly-*.md | head -1

# 查看备份目录
ls -lt /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/backups/ | head -7
```

---

## 5️⃣ 补充条款与规范

### 5.1 空闲检测机制 (CRON-003/004/005/008)

| 任务 | 空闲检测 | 等待策略 | 超时放弃 |
|------|---------|---------|---------|
| **CRON-003** (备份) | CPU<50% 且 无活跃会话 | 等待 30 分钟 | 03:30 放弃 |
| **CRON-004** (Ingest) | CPU<50% 且 无活跃会话 | 等待 30 分钟 | 04:30 放弃 |
| **CRON-005** (Lint) | 仅周日检测 | 等待 60 分钟 | 02:00 放弃 |
| **CRON-008** (审计) | 仅 1 日检测 | 等待 60 分钟 | 03:00 放弃 |

**空闲条件**: Gateway CPU<50% + 活跃会话<5

---

### 5.2 失败重试机制

| 任务 | 重试次数 | 重试间隔 | 通知条件 |
|------|---------|---------|---------|
| **CRON-003** (备份) | 2 次 | 1 小时 | 连续失败 3 次 |
| **CRON-004** (Ingest) | 2 次 | 1 小时 | 连续失败 3 次 |
| **CRON-005** (Lint) | 1 次 | 2 小时 | 连续失败 2 次 |
| **CRON-006** (告警) | 1 次 | 30 分钟 | 连续失败 2 次 |
| **CRON-008** (审计) | 1 次 | 4 小时 | 连续失败 2 次 |

---

### 5.3 知识入库规范 (CRON-004)

| 项目 | 规范 |
|------|------|
| **6 大领域** | llm-wiki-pattern / agent-development / ai-monetization / skill-development / openclaw-framework / llm-technology |
| **每日目标** | ≥18 条 (6 领域 × 3 条) |
| **来源限制** | 仅限 `raw/` 目录文件 (不主动抓取新闻) |
| **格式要求** | Markdown + Frontmatter 元数据 |
| **查重机制** | 标题 + 内容相似度>80% → 跳过 |
| **不足处理** | 不强制补齐，记录日志即可 |

---

### 5.4 日志管理规范

| 日志 | 位置 | 保留期限 | 清理频率 |
|------|------|---------|---------|
| **备份日志** | `logs/backup.log` | 30 天 | 每月 1 日 |
| **Ingest 日志** | `logs/ingest.log` | 30 天 | 每月 1 日 |
| **Lint 日志** | `logs/lint.log` | 90 天 | 每月 1 日 |
| **告警日志** | `/tmp/wiki-alert.log` | 30 天 | 每月 1 日 |
| **报告日志** | `/tmp/wiki-report.log` | 180 天 | 每月 1 日 |
| **SOP 审查日志** | `/tmp/wiki-sop-review.log` | 365 天 | 每年 1 月 1 日 |

---

### 5.5 异常分级响应

| 级别 | 定义 | 示例 | 响应时间 | 通知方式 |
|------|------|------|---------|---------|
| **P0** | 核心功能失败 | 备份失败>2 天、Ingest 停滞>24h | 立即 | 飞书 + 邮件 |
| **P1** | 重要功能异常 | Lint 失败、健康分<75 | 24 小时 | 飞书 |
| **P2** | 优化类问题 | 周报未生成、单领域<3 条 | 周度 | 日志记录 |

---

### 5.6 变更管理流程

```
用户提出变更 → 评估影响级别 → 更新 SOP → 执行变更 → 验证测试 → Git 提交
```

| 变更类型 | 影响级别 | SOP 更新 | 示例 |
|----------|---------|---------|------|
| 时间调整 | 🟢 小 | 更新任务清单表格 | 03:00→04:00 |
| 脚本优化 | 🟢 小 | 更新脚本说明 | 增加压缩功能 |
| 新增任务 | 🟡 中 | 新增任务行 + 更新统计 | 增加 CRON-011 |
| 删除任务 | 🟡 中 | 标记"已停用" | 停用 CRON-002 |
| 流程变化 | 🟠 大 | 更新对应章节 | 异常响应 24h→1h |
| 架构重构 | 🔴 特大 | SOP v2.0 | Crontab→systemd |

---

## 6️⃣ 异常处理 (快速参考)

### P0 异常 (立即处理)

| 异常 | 现象 | 处理流程 |
|------|------|---------|
| **备份失败** | 备份目录>7 天未更新 | 1. 检查磁盘空间 2. 手动执行备份 3. 检查脚本权限 |
| **Ingest 失败** | raw/有文件未处理 | 1. 检查 Python 依赖 2. 查看 ingest.log 3. 手动执行 |
| **健康分<75** | 收到告警通知 | 1. 查看 Lint 报告 2. 处理孤页/矛盾 3. 补充更新 |

### P1 异常 (24 小时内)

| 异常 | 现象 | 处理流程 |
|------|------|---------|
| **周报未生成** | reports/无最新周报 | 1. 检查脚本存在 2. 查看 cron 日志 3. 手动执行 |
| **Lint 失败** | lint.log 有错误 | 1. 检查索引文件 2. 修复路径 3. 重新执行 |

---

## 7️⃣ 脚本依赖

### 已存在脚本

| 脚本 | 位置 | 状态 |
|------|------|------|
| `auto-backup.sh` | `scripts/` | ✅ 存在 |
| `auto-ingest.py` | `scripts/` | ✅ 存在 (已更新 6 大领域配置) |
| `auto-lint.sh` | `scripts/` | ✅ 存在 (已修复路径) |
| `health-alert.sh` | `scripts/` | ✅ 存在 (新增) |
| `evomap-monitor.py` | `evomap 项目/scripts/` | ✅ 存在 |
| `monitor-skill-downloads.py` | `evomap 项目/` | ✅ 存在 |

### 待创建脚本

| 脚本 | 位置 | 说明 | 优先级 |
|------|------|------|--------|
| `generate-weekly-report.sh` | `scripts/` | 周报生成 | P2 |
| `generate-monthly-report.sh` | `scripts/` | 月报生成 | P2 |
| `auto-audit.sh` | `scripts/` | 月度深度审计 | P1 |
| `review-health-sop.sh` | `scripts/` | SOP 月度审查 | P1 |

---

## 7️⃣ 日志管理

### 日志位置

| 任务 | 日志文件 | 保留期限 |
|------|---------|---------|
| 备份 | `logs/backup.log` | 30 天 |
| Ingest | `logs/ingest.log` | 30 天 |
| Lint | `logs/lint.log` | 90 天 |
| 健康告警 | `/tmp/wiki-alert.log` | 30 天 |
| 周报 | `/tmp/wiki-report.log` | 90 天 |
| 月报 | `/tmp/wiki-report.log` | 180 天 |
| SOP 审查 | `/tmp/wiki-sop-review.log` | 365 天 |

### 日志清理 (每月 1 日)

```bash
# 清理>30 天的日志
find /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs -name "*.log" -mtime +30 -delete
find /tmp -name "wiki-*.log" -mtime +30 -delete
```

---

## 8️⃣ 变更管理

### 修改 Crontab 流程

1. **备份**: `crontab -l > backup.txt`
2. **编辑**: `crontab -e`
3. **验证**: `crontab -l`
4. **测试**: 手动执行脚本确认
5. **记录**: 更新本 SOP 任务清单

### 版本记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-04-21 | 初始版本 (10 个任务 + 空闲检测 + 失败重试 + 知识入库规范) | Red Agent Team |

---

## 📚 相关文档

| 文档 | 路径 |
|------|------|
| 健康监测 SOP | `learnings/health-monitoring-sop.md` |
| Crontab 配置指南 | `scripts/CRONTAB-CONFIG.md` |
| 起草记录 | `learnings/health-monitoring-sop-draft-record.md` |

---

**SOP 状态**: ✅ Active (2026-04-21 12:05 生效)  
**下次审查**: 2026-05-21 (CRON-010 自动提醒)

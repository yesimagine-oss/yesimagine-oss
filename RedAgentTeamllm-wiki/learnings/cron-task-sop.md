# RedAgentTeamllm-wiki 定时任务 SOP

**版本**: v1.0  
**生效日期**: 2026-04-21  
**状态**: 🟡 Draft  
**维护者**: Red Agent Team

---

## 1️⃣ 定时任务清单

### 现有任务 (5 个)

| ID | 频率 | 脚本 | 说明 | 优先级 |
|----|------|------|------|--------|
| **CRON-001** | 每 30 分钟 | `evomap-monitor.py` | EvoMap 资产监控 | P0 |
| **CRON-002** | 每小时 | `monitor-skill-downloads.py` | Skill 下载统计 | P1 |
| **CRON-003** | 每日 02:00 | `auto-backup.sh` | 自动备份 | P0 |
| **CRON-004** | 每日 05:00 | `auto-ingest.py` | 自动 Ingest | P0 |
| **CRON-005** | 每周日 01:00 | `auto-lint.sh` | 完整 Lint 检查 | P1 |

### 新增任务 (5 个)

| ID | 频率 | 脚本 | 说明 | 优先级 |
|----|------|------|------|--------|
| **CRON-006** | 每日 06:00 | `health-alert.sh` | 健康分告警 (<80 通知) | P1 |
| **CRON-007** | 每周日 06:00 | `generate-weekly-report.sh` | 周报生成 | P2 |
| **CRON-008** | 每月 1 日 02:00 | `auto-audit.sh` | 深度审计 + 归档 | P1 |
| **CRON-009** | 每月 1 日 06:00 | `generate-monthly-report.sh` | 月报生成 | P2 |
| **CRON-010** | 每月 21 日 09:00 | `review-health-sop.sh` | SOP 月度审查 | P1 |

---

## 2️⃣ 执行状态

| 任务 | 配置状态 | 执行状态 | 最后检查 |
|------|----------|----------|----------|
| CRON-001 | ✅ 已安装 | ✅ 运行中 | - |
| CRON-002 | ✅ 已安装 | ✅ 运行中 | - |
| CRON-003 | ⚠️ 路径待更新 | ❓ 待验证 | - |
| CRON-004 | ⚠️ 路径待更新 | ❓ 待验证 | - |
| CRON-005 | ⚠️ 路径待更新 | ❓ 待验证 | - |
| CRON-006 | ❌ 未安装 | ❌ 未执行 | - |
| CRON-007 | ❌ 未安装 | ❌ 未执行 | - |
| CRON-008 | ❌ 未安装 | ❌ 未执行 | - |
| CRON-009 | ❌ 未安装 | ❌ 未执行 | - |
| CRON-010 | ❌ 未安装 | ❌ 未执行 | - |

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

### 步骤 3: 粘贴配置

```bash
# ============= EvoMap 监控 =============
*/30 * * * * cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目 && python3 scripts/evomap-monitor.py >> logs/evomap-monitor.log 2>&1
0 * * * * cd /home/admin/.openclaw/workspace/ai\ 知识变现/evomap\ 项目 && python3 monitor-skill-downloads.py >> monitoring/cron.log 2>&1

# ============= RedAgentTeamllm-wiki 自动化 =============
0 2 * * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/auto-backup.sh >> /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/backup.log 2>&1
0 5 * * * /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/scripts/auto-ingest.py >> /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/logs/ingest.log 2>&1
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

## 5️⃣ 异常处理

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

## 6️⃣ 脚本依赖

### 已存在脚本

| 脚本 | 位置 | 状态 |
|------|------|------|
| `auto-backup.sh` | `scripts/` | ✅ 存在 |
| `auto-ingest.py` | `scripts/` | ✅ 存在 |
| `auto-lint.sh` | `scripts/` | ✅ 存在 (已修复路径) |
| `health-alert.sh` | `scripts/` | ✅ 存在 (新增) |

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
| v1.0 | 2026-04-21 | 初始版本 | Red Agent Team |

---

## 📚 相关文档

| 文档 | 路径 |
|------|------|
| 健康监测 SOP | `learnings/health-monitoring-sop.md` |
| Crontab 配置指南 | `scripts/CRONTAB-CONFIG.md` |
| 起草记录 | `learnings/health-monitoring-sop-draft-record.md` |

---

**SOP 状态**: 🟡 Draft → 🔴 Pending → ✅ Active (用户确认后)  
**下次审查**: 2026-05-21 (月度)

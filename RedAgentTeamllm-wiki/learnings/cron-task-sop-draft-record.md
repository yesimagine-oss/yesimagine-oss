# 定时任务 SOP 起草记录

**起草时间**: 2026-04-21 11:25 CST  
**起草者**: Red Agent Team  
**状态**: 🟡 进行中  
**目标**: 创建/更新 `cron-task-sop.md` v1.0 + 安装 Crontab

---

## 📋 需求来源

### 用户要求

| 要求 | 说明 |
|------|------|
| **了解当前任务** | 查询已安装的 Crontab 任务 |
| **建议新任务** | 根据健康监测 SOP 补充缺失任务 |
| **同步记录** | 定制过程全程记录 |
| **知识获取配置** | 6 大领域 × 3 条 = 18 条/天 |

---

## 🧠 知识自动获取配置 (2026-04-21 11:53 更新)

### 6 大领域定位

| 领域 | 标识 | 每日目标 | 说明 |
|------|------|---------|------|
| **LLM-Wiki 模式** | `llm-wiki-pattern` | ≥3 条 | 知识库管理/架构/最佳实践 |
| **Agent 领域** | `agent-development` | ≥3 条 | AI Agent 设计/开发/部署 |
| **AI 知识变现** | `ai-monetization` | ≥3 条 | 商业模式/定价/推广 |
| **Skill 领域** | `skill-development` | ≥3 条 | OpenClaw Skills/工具/插件 |
| **OpenClaw 领域** | `openclaw-framework` | ≥3 条 | 框架更新/功能/案例 |
| **大模型领域** | `llm-technology` | ≥3 条 | 模型技术/应用/趋势 |
| **合计** | - | **≥18 条/天** | 原标准 30 条/天 |

### 配置更新

- **文件**: `scripts/auto-ingest.py`
- **变更**: `DAILY_TARGET = 30` → `18`
- **新增**: `KNOWLEDGE_DOMAINS` (6 大领域)
- **新增**: `DOMAIN_TARGETS` (各领域目标)

---

## 📊 当前定时任务清单 (已安装 5 个)

| ID | 频率 | 脚本 | 路径状态 | 优先级 |
|----|------|------|---------|--------|
| **CRON-001** | */30 * * * * | `evomap-monitor.py` | ✅ 正确 | P0 |
| **CRON-002** | 0 6:30 * * * | `monitor-skill-downloads.py` | ✅ 正确 (已调整) | P1 |
| **CRON-003** | 0 3 * * * | `auto-backup.sh` | ✅ 已修复 | P0 |
| **CRON-004** | 0 4 * * * | `auto-ingest.py` | ✅ 已修复 | P0 |
| **CRON-005** | 0 1 * * 0 | `auto-lint.sh` | ✅ 已修复 | P1 |

**路径修复**: CRON-003/004/005 已从 `AgentTeamllm-wiki` → `RedAgentTeamllm-wiki` ✅

---

## 🎯 定时任务清单 (共 10 个)

### 保留任务 (5 个 - 已修复)

| ID | 频率 | 脚本 | 说明 | 状态 |
|----|------|------|------|------|
| **CRON-001** | */30 * * * * | `evomap-monitor.py` | EvoMap 监控 | ✅ 已修复 |
| **CRON-002** | 0 6:30 * * * | `monitor-skill-downloads.py` | Skill 下载统计 (每日) | ✅ 已修复 |
| **CRON-003** | 0 3 * * * | `auto-backup.sh` | 自动备份 (每日 03:00) | ✅ 已修复 |
| **CRON-004** | 0 4 * * * | `auto-ingest.py` | 自动 Ingest (每日 04:00) | ✅ 已修复 |
| **CRON-005** | 0 1 * * 0 | `auto-lint.sh` | Lint 检查 (周日 01:00) | ✅ 已修复 |

### 新增任务 (5 个 - 健康监测)

| ID | 频率 | 脚本 | 说明 | 状态 |
|----|------|------|------|------|
| **CRON-006** | 0 6 * * * | `health-alert.sh` | 健康分告警 (<80 通知) | ❌ 待安装 |
| **CRON-007** | 0 6 * * 0 | `generate-weekly-report.sh` | 周报生成 (每周) | ❌ 待创建 |
| **CRON-008** | 0 2 1 * * | `auto-audit.sh` | 深度审计 (每月) | ❌ 待创建 |
| **CRON-009** | 0 6 1 * * | `generate-monthly-report.sh` | 月报生成 (每月) | ❌ 待创建 |
| **CRON-010** | 0 9 21 * * | `review-health-sop.sh` | SOP 审查 (每月) | ❌ 待创建 |

---

## 🔄 执行计划

### 阶段 1: 修复现有任务 (P0)

```bash
# 备份当前 Crontab
crontab -l > ~/cron-backup-$(date +%Y%m%d-%H%M%S).txt

# 编辑 Crontab，修复路径
crontab -e
# 将 AgentTeamllm-wiki → RedAgentTeamllm-wiki
```

### 阶段 2: 创建缺失脚本 (P1)

| 脚本 | 预计大小 | 说明 |
|------|---------|------|
| `generate-weekly-report.sh` | ~100 行 | 汇总周报 |
| `generate-monthly-report.sh` | ~150 行 | 汇总月报 |
| `auto-audit.sh` | ~200 行 | 深度审计 |
| `review-health-sop.sh` | ~80 行 | SOP 审查 |

### 阶段 3: 安装新任务 (P1)

```bash
# 添加 CRON-006 ~ CRON-010 到 Crontab
crontab -e
```

### 阶段 4: 验证测试 (P1)

```bash
# 验证任务数量
crontab -l | wc -l  # 应=10

# 手动测试脚本
./scripts/health-alert.sh
```

---

## 📐 SOP 结构预览

```markdown
# RedAgentTeamllm-wiki 定时任务 SOP

1. 定时任务清单 (10 个任务详情)
2. 执行状态追踪 (已安装/待安装)
3. 安装流程 (备份→编辑→验证)
4. 监控验证 (日/周/月检查)
5. 异常处理 (P0/P1 流程)
6. 日志管理 (位置 + 保留期限)
7. 变更管理 (Crontab 修改规范)
```

---

## ⏭️ 下一步

1. ⏳ 修复现有 3 个任务路径
2. ⏳ 创建 4 个缺失脚本
3. ⏳ 安装 5 个新任务
4. ⏳ 验证测试
5. ⏳ Git 提交归档

---

**记录时间**: 2026-04-21 11:25 CST  
**下一步**: 修复现有任务路径
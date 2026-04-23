---
category: knowledge-management
created_at: '2026-04-21'
tags:
- sop
- knowledge-flow
- redagentteamllm-wiki
- openclaw
title: 知识提炼与存放标准流程 (SOP)
type: sop
version: '1.0.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-21"
  verified_by: "Red Agent Team"
  verification_method: "SOP 固化"
  trust_score: 1.0

# Trust Boundary
trust_level: "internal"
evidence_level: "SOP 规范"
---

# 知识提炼与存放标准流程 (SOP)

**版本**: v1.0.0  
**创建**: 2026-04-21  
**维护者**: Red Agent Team  
**状态**: ✅ 生产就绪

---

## 📊 流程图

```
日常记录 → 识别价值 → 提炼格式化 → 资产提取 → 分类存放 → 更新索引
```

---

## 阶段 1: 日常记录 (OpenClaw 工作区)

**位置**:
```
~/.openclaw/workspace/
├── MEMORY.md                    # 长期记忆
├── memory/
│   └── YYYY-MM-DD.md            # 每日记忆
└── .learnings/
    └── LEARNINGS.md             # 学习记录
```

**内容**:
- 对话记录
- 操作步骤
- 错误信息
- 临时学习

**频率**: 实时/自动

---

## 阶段 2: 识别价值

**触发时机**:
- 任务完成后
- 每日结束时
- 发现可复用模式时

**判断标准** (全部满足):

| 标准 | 问题 | 是→继续 |
|------|------|--------|
| **可复用** | 这个知识能否在其他场景使用？ | ✅ |
| **有学习价值** | 对未来任务有帮助吗？ | ✅ |
| **可验证** | 能否通过命令/测试验证？ | ✅ |

**否→丢弃**，仅保留在 daily memory 中

---

## 阶段 3: 提炼格式化

**标准格式**:

```markdown
---
category: <主题>
created_at: 'YYYY-MM-DD'
tags: [tag1, tag2, tag3]
title: <标题>
type: article|sop|reference|report
version: '1.0.0'

# Provenance
provenance:
  source_url: "<来源 URL 或 internal>"
  captured_at: "YYYY-MM-DDTHH:MM:SS+08:00"
  verified_by: "<验证者>"
  verification_method: "<验证方法>"
  trust_score: 0.XX

# Trust Boundary
trust_level: "llm+verified|internal|external"
evidence_level: "原文 + 實測|原文|推论"
---

# 正文内容
```

**必填字段**:
- `category`
- `created_at`
- `title`
- `provenance.source_url`
- `provenance.trust_score`
- `trust_level`
- `evidence_level`

---

## 阶段 4: 资产提取

### Gene 提取

**格式**:
```json
{
  "asset_type": "Gene",
  "asset_id": "gene_<主题>_<功能>",
  "name": "<名称>",
  "description": "<描述>",
  "validate_command": "<验证命令>",
  "confidence": 0.XX,
  "gep_version": "v1.0.0",
  "tags": ["tag1", "tag2"],
  "created_at": "YYYY-MM-DDTHH:MM:SS+08:00",
  "verified_by": "<验证者>",
  "source_url": "<来源>"
}
```

**何时提取**:
- 有明确验证逻辑时
- 可重复验证时
- 可信度 ≥ 0.90

---

### Capsule 提取

**格式**:
```json
{
  "asset_type": "Capsule",
  "asset_id": "capsule_<主题>_<功能>",
  "name": "<名称>",
  "trigger_signal": "<触发信号>",
  "executable_code": "<执行代码>",
  "description": "<描述>",
  "confidence": 0.XX,
  "gep_version": "v1.0.0",
  "tags": ["tag1", "tag2"],
  "prerequisites": ["前置条件 1", "前置条件 2"],
  "expected_output": "<预期输出>",
  "error_handling": "<错误处理>"
}
```

**何时提取**:
- 有可执行代码时
- 有明确触发信号时
- 可自动化执行时

---

## 阶段 5: 分类存放 (RedAgentTeamllm-wiki)

### 存放决策树

```
                    ┌─────────────────┐
                    │ 知识类型？       │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ↓                    ↓                    ↓
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ 重大经验/整合  │   │ 事故报告       │   │ 主题相关学习   │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                    │                    │
        ↓                    ↓                    ↓
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ learnings/    │   │ accidents/    │   │ wiki/<主题>/  │
│               │   │               │   │ 05-learning/  │
└───────────────┘   └───────────────┘   └───────────────┘
```

### 存放位置规范

| 位置 | 存放内容 | 示例 |
|------|----------|------|
| **`learnings/`** | 重大经验、整合任务、跨主题学习 | `2026-04-21-openclaw-knowledge-integration.md` |
| **`accidents/`** | 事故报告、根因分析、修复方案 | `2026-04-07-evomap-heartbeat-failure.md` |
| **`wiki/<主题>/05-learning/`** | 主题相关学习、验证报告、会话总结 | `wiki/openclaw/05-learning/openclawx-feishu-verification.md` |
| **`wiki/<主题>/assets/genes/`** | Genes (验证逻辑) | `gene_openclaw_control_ui_auth_flow.json` |
| **`wiki/<主题>/assets/capsules/`** | Capsules (执行代码) | `capsule_openclaw_gateway_status_check.json` |

---

## 阶段 6: 更新索引

### 主题索引更新

**文件**: `wiki/<主题>/index.md`

**更新内容**:
```markdown
## 📊 统计

| 分类 | 文件数 | Gene 数 | Capsule 数 |
|------|--------|--------|-----------|
| **05-learning** | +1 | - | - |

## 🔄 更新日志

| 日期 | 操作 | 说明 |
|------|------|------|
| YYYY-MM-DD | 新增 | <文件说明> |
```

### 全局索引更新 (如需要)

**文件**: `wiki/index.md`

**何时更新**:
- 新增主题时
- 重大更新时
- 定期汇总时

---

## ✅ 质量检查清单

### 存放前检查

| 检查项 | 标准 | 状态 |
|--------|------|------|
| **格式完整** | Frontmatter + Provenance + Trust Boundary | □ |
| **分类正确** | 符合决策树 | □ |
| **资产提取** | Genes/Capsules 已提取 (如适用) | □ |
| **命名规范** | `YYYY-MM-DD-<主题>-<说明>.md` | □ |
| **无重复** | 查重完成 | □ |

### 存放后检查

| 检查项 | 标准 | 状态 |
|--------|------|------|
| **索引更新** | 统计数字准确 | □ |
| **链接有效** | 相对路径正确 | □ |
| **Git 提交** | 版本控制已更新 | □ |

---

## 📖 示例

### 示例 1: 重大整合任务

**场景**: OpenClaw 知识库整合 (65+ 文件迁移)

**流向**:
```
memory/2026-04-21.md (日常记录)
  ↓
识别价值：可复用 + 有学习价值 + 可验证
  ↓
提炼格式化：添加 Frontmatter + Provenance
  ↓
资产提取：9 Genes + 6 Capsules
  ↓
分类存放：learnings/2026-04-21-openclaw-knowledge-integration.md
  ↓
更新索引：wiki/openclaw/index.md 统计更新
```

---

### 示例 2: 事故报告

**场景**: Gateway 认证失败导致远程登录问题

**流向**:
```
memory/2026-04-21.md (错误记录)
  ↓
识别价值：有学习价值 + 可验证
  ↓
提炼格式化：事故报告格式
  ↓
资产提取：gene_openclaw_auth_error_codes
  ↓
分类存放：accidents/2026-04-21-gateway-auth-failure.md
  ↓
更新索引：wiki/openclaw/index.md + accidents/index.md
```

---

### 示例 3: 主题学习

**场景**: Control UI 认证配置学习

**流向**:
```
memory/2026-04-21.md (学习记录)
  ↓
识别价值：可复用 + 有学习价值
  ↓
提炼格式化：reference 格式
  ↓
资产提取：gene_openclaw_control_ui_auth_flow + capsule_openclaw_control_ui_auth_verify
  ↓
分类存放：wiki/openclaw/02-control-ui/authentication.md
  ↓
更新索引：wiki/openclaw/index.md
```

---

## 🎯 关键原则

| 原则 | 说明 |
|------|------|
| **单一来源** | 每个知识只存一份，避免重复 |
| **可追溯** | Provenance 完整，可追溯来源 |
| **可验证** | Genes 提供验证命令，Capsules 可执行 |
| **分类清晰** | 按决策树存放，便于查找 |
| **索引同步** | 存放后立即更新索引 |

---

## 📊 维护频率

| 任务 | 频率 | 说明 |
|------|------|------|
| **日常记录** | 实时 | OpenClaw 自动记录 |
| **提炼格式化** | 任务完成后 | 或每日结束时 |
| **资产提取** | 提炼时同步 | 有可提取内容时 |
| **索引更新** | 存放后立即 | 保持索引准确 |
| **定期审查** | 每周 | 检查是否有遗漏 |

---

**创建者**: Red Agent Team  
**创建时间**: 2026-04-21 08:33 GMT+8  
**状态**: ✅ 生产就绪  
**下次审查**: 2026-04-28

---

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

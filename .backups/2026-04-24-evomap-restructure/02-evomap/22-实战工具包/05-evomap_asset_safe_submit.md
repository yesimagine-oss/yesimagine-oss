---
category: optimize
created_at: '2026-04-15T08:40:00+08:00'
tags:
- evomap
- safe_submit
- asset_upload
- verify
title: EvoMap 资产安全提交
type: capsule
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
# Capsule: evomap_asset_safe_submit

## 触发条件

资产完成验证，准备上传 EvoMap

## 内容

```bash
# 1. 验证资产结构
evomap-cli asset verify

# 2. 上传资产 (跳过固定签名检查)
evomap-cli asset upload --skip-fixed-signature

# 3. 确认发布状态
evomap-cli asset status --latest
```

## 执行流程

```
1. 运行 4 个 Gene 验证
   ↓
2. 全部通过 → 继续
   ↓
3. 上传资产
   ↓
4. 等待 Hub 决策
   ↓
5. 记录结果 (accept/quarantine/reject)
```

## 成功标准

| 状态 | 说明 | 后续 |
|------|------|------|
| accept | 自动推广 | ✅ 成功 |
| quarantine | 安全审核 | ⏳ 等待 |
| reject | 被拒绝 | ❌ 修复重发 |

## 关联 Gene

- evomap_asset_structure_validate
- evomap_node_health_check
- evomap_drift_pre_scan
- evomap_asset_hash_verify


## 相關文檔

- [[evomap_task_template]]
- [[evomap-asset-publishing]]
- [[EvoMap Capsule 详细信息]]

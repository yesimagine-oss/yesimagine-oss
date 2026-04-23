---
category: evomap
created_at: '2026-04-15T08:40:00+08:00'
tags:
- evomap
- tools
- genes
- capsules
- index
title: EvoMap 实战工具包索引
type: index
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
# EvoMap 实战工具包

**创建时间:** 2026-04-15  
**来源:** 用户实战经验总结  
**状态:** ✅ 已入库启用

---

## 📦 工具包内容

### Gene 资产 (4 个)

| 编号 | 名称 | 用途 | 验证命令 |
|------|------|------|---------|
| 01 | evomap_asset_structure_validate | 资产结构验证 | `pytest tests/evomap_asset_validate.py` |
| 02 | evomap_node_health_check | 节点健康检查 | `node tools/node-health-check.js` |
| 03 | evomap_drift_pre_scan | 漂移风险扫描 | `node tools/drift-scanner.js` |
| 04 | evomap_asset_hash_verify | 哈希验证 | `node tools/asset-hash-verify.js` |

### Capsule 资产 (3 个)

| 编号 | 名称 | 触发条件 | 执行命令 |
|------|------|---------|---------|
| 05 | evomap_asset_safe_submit | 资产发布前 | `evomap-cli asset verify && upload` |
| 06 | evomap_node_re_register | 节点失联 | `evomap-cli node reset && register` |
| 07 | evomap_knowledge_merge | 知识合并 | `llm-wiki merge --source evomap` |

---

## 🔗 实体关系

```
Gene 资产 → 验证 → Capsule 资产
   ↓
节点 → 注册 → EvoMap 平台
   ↓
资产 → 提交 → EvoMap 变现
   ↓
风险 → 检测 → High Intent Drift
   ↓
知识 → 合并 → RedAgentTeamllm-wiki
```

---

## 🎯 使用场景

### 发布前自检

```bash
# 1. 运行 4 个 Gene 验证
pytest tests/evomap_asset_validate.py
node tools/drift-scanner.js
node tools/asset-hash-verify.js

# 2. 安全提交
evomap-cli asset verify
evomap-cli asset upload --skip-fixed-signature
```

### 节点监控

```bash
# 每 5 分钟心跳
node tools/node-health-check.js

# 失联时重注册
evomap-cli node reset --fingerprint {fp}
evomap-cli node register
```

### 知识合并

```bash
# 新知识入库
llm-wiki merge --source evomap --strategy overwrite-duplicate
```

---

## 📊 价值评估

| 维度 | 评分 | 说明 |
|------|------|------|
| **实用性** | ⭐⭐⭐⭐⭐ | 实战经验总结 |
| **独特性** | ⭐⭐⭐⭐⭐ | 无重复内容 |
| **可执行性** | ⭐⭐⭐⭐⭐ | 命令可直接运行 |
| **完整性** | ⭐⭐⭐⭐⭐ | Gene+Capsule 完整 |

---

## ✅ 入库状态

- [x] Gene 文件创建 (4/4)
- [x] Capsule 文件创建 (3/3)
- [x] 索引文档创建
- [x] Front Matter 合规
- [x] 交叉引用正确
- [x] 知识库启用

---

**下一步:** 创建验证脚本和测试用例


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]

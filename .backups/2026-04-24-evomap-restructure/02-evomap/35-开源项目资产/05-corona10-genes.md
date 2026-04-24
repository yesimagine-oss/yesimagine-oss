---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 05 Corona10 Genes
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
# corona10 Genes - 验证核心

**来源:** corona10 GitHub Profile (42 个仓库完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `corona10_repo_metadata_scan` | corona10 仓库元数据扫描 | `pytest tests/test_corona10_repo.py` |
| 2 | `corona10_cgo_env_validate` | CGO + OpenCV 环境验证 | `node tests/corona10-cgo-env.test.js` |
| 3 | `corona10_go_build_test` | Go 项目构建和测试验证 | `pytest tests/test_corona10_build.py` |
| 4 | `corona10_opencv_version_check` | OpenCV >=4.x 兼容性验证 | `node tests/corona10-opencv-version.test.js` |

---

## 与 go-image-skill 关联

| Gene | 应用 | 节省 |
|------|------|------|
| `corona10_cgo_env_validate` | GoCV 环境配置 | 2h → 0.5h |
| `corona10_opencv_version_check` | OpenCV 版本验证 | 1h → 0.5h |

---

**总计节省:** ~3h


## 相關文檔

- [[01-openai-genes]]
- [[05-evomap_asset_safe_submit]]
- [[01-github-genes]]

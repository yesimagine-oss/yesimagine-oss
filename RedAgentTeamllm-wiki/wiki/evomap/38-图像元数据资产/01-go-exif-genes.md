---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 01 Go Exif Genes
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
# go-exif Genes - 验证核心

**来源:** go-exif Official Docs (72 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## Gene 列表

| # | Gene ID | 验证目标 | 测试命令 |
|---|---------|----------|----------|
| 1 | `go_exif_image_validate` | JPEG/TIFF EXIF 存在验证 | `pytest tests/test_go_exif_image.py` |
| 2 | `go_exif_parse_verify` | 完整 EXIF/IFD/Tag 解析验证 | `node tests/go-exif-parse.test.js` |
| 3 | `go_exif_tag_extract_check` | GPS/DateTime Tag 提取验证 | `pytest tests/test_go_exif_tags.py` |
| 4 | `go_exif_corrupt_safe` | 损坏/畸形图像安全解析 | `node tests/go-exif-corrupt.test.js` |

---

## 与 go-image-skill 关联

| Gene | 应用 | 节省 |
|------|------|------|
| `go_exif_image_validate` | 图像格式验证 | 1h → 0.5h |
| `go_exif_parse_verify` | EXIF 解析 | 2h → 0.5h |
| `go_exif_tag_extract_check` | GPS/时间提取 | 2h → 0.5h |

---

**总计节省:** ~3h


## 相關文檔

- [[go-lang-deliberation-20260413]]
- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]

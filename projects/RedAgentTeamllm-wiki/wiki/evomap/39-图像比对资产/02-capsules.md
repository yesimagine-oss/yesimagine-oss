---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 02 Capsules
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
# goimagehash Capsules

**入库日期:** 2026-04-15

| # | Capsule | 用途 | 代码 |
|---|---------|------|------|
| 1 | `goimagehash_phash_generate` | 生成 pHash | `PerceptionHash(img)` |
| 2 | `goimagehash_compare_images` | 比对两张图片 | `hash1.Distance(hash2)` |
| 3 | `goimagehash_decode_safe` | 安全图像解码 | `image.Decode(f)` |

---

## go-image-skill 应用

- **图像比对:** 计算两张图片相似度
- **重复检测:** 找出重复/相似图片
- **搜索索引:** 建立可搜索的图像库


## 相關文檔

- [[02-openai-capsules]]
- [[02-evomap_node_health_check]]
- [[02-github-capsules]]

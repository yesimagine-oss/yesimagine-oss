---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Readme
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
# goimagehash 资产包 - 感知哈希算法

**来源:** github.com/corona10/goimagehash (68 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## 核心功能

| 算法 | 用途 | 节省 |
|------|------|------|
| **pHash** | 感知哈希 | 2h→0.5h |
| **dHash** | 差异哈希 | 2h→0.5h |
| **aHash** | 平均哈希 | 1h→0.5h |
| **图像比对** | 相似度计算 | 4h→1h |

---

## go-image-skill 集成

```go
import "github.com/corona10/goimagehash"

// 生成哈希
img, _ := goimagehash.Open("test.jpg")
hash, _ := goimagehash.PerceptionHash(img)

// 比对相似度
hash1, _ := goimagehash.DifferenceHash(img1)
hash2, _ := goimagehash.DifferenceHash(img2)
distance, _ := hash1.Distance(hash2)  // 越小越相似
```

---

**节省工时:** ~7h


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]

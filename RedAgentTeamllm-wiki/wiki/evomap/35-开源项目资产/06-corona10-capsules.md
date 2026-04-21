---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 06 Corona10 Capsules
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
# corona10 Capsules - 功能封装

**来源:** corona10 GitHub Profile (42 个仓库完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## Capsule 列表

| # | Capsule ID | 触发条件 | 功能 |
|---|------------|----------|------|
| 1 | `corona10_repo_list_scan` | 扫描 corona10 全部仓库 | gh api + jq |
| 2 | `corona10_gocv_build_setup` | GoCV 项目环境配置 | apt + CGO + go build |
| 3 | `corona10_image_process` | 图像处理工具 | GoCV 图像处理 |

---

## go-image-skill 集成

```bash
# GoCV 环境配置
apt install -y libopencv-dev
export CGO_ENABLED=1
go build -tags full github.com/hybridgroup/gocv/...
```

```go
// 图像处理
img := gocv.IMRead("input.jpg", gocv.IMReadColor)
defer img.Close()
gocv.CvtColor(img, &gray, gocv.ColorBGRToGray)
```

---

**总计节省:** ~7h


## 相關文檔

- [[02-openai-capsules]]
- [[06-evomap_node_re_register]]
- [[02-github-capsules]]

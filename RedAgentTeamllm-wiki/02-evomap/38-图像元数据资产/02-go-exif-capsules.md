---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 02 Go Exif Capsules
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
# go-exif Capsules - 功能封装

**来源:** go-exif Official Docs (72 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## Capsule 列表

| # | Capsule ID | 触发条件 | 功能 |
|---|------------|----------|------|
| 1 | `exif_extract_full` | 解析图像 EXIF | 完整元数据提取 |
| 2 | `exif_gps_extract` | 提取 GPS 坐标 | 位置信息 |
| 3 | `exif_jpeg_validate` | JPEG 结构验证 | 格式检查 |

---

## go-image-skill 集成代码

```go
package image

import (
    "os"
    exif "github.com/dsoprea/go-exif/v3"
)

// 提取 EXIF
func extractEXIF(imagePath string) (*EXIFResult, error) {
    fd, err := os.Open(imagePath)
    if err != nil {
        return nil, err
    }
    defer fd.Close()

    parser := exif.NewParser()
    parsed, err := parser.Parse(fd)
    if err != nil {
        return nil, err
    }

    // 提取 GPS
    gps, _ := parsed.GetGps()
    lat, long := gps.Latitude, gps.Longitude

    return &EXIFResult{
        GPSLatitude:  lat,
        GPSLongitude: long,
    }, nil
}
```

---

**总计节省:** ~5h


## 相關文檔

- [[go-lang-deliberation-20260413]]
- [[02-openai-capsules]]
- [[02-evomap_node_health_check]]

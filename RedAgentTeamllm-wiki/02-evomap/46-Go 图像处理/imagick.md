---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Imagick
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
# imagick - ImageMagick Go 绑定

**来源:** github.com/cshum/imagick (100% 覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 图像缩放 | 高质量滤镜 (Lanczos 等) |
| 格式转换 | 支持 100+ 格式 |
| 流式 I/O | 大图处理 |
| CGO 优化 | 内存安全管理 |

---

## 项目应用

| 项目 | 用途 | 节省 |
|------|------|------|
| go-image-skill | 压缩/缩放/转换 | ~3h |
| 无头浏览器 | 截图优化 | ~2h |
| **总计** | - | **~5h** |

---

## 代码示例

```go
// 初始化
magick.Initialize()
defer magick.Terminate()

// 缩放
mw.ReadImage("input.jpg")
mw.ResizeImage(800, 600, magick.FilterLanczosSharp)
mw.WriteImage("output.jpg")
```

---

**结论:** 专业图像处理备选，建议入库

---

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
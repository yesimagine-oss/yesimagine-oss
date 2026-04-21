---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Chromedp.Capsules
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
# Capsule: chromedp_server_init

**Trigger**: 服务器环境（Linux 无头）

**Code**:
```go
opts := append(chromedp.DefaultExecAllocatorOptions[:],
    chromedp.Flag("headless", "new"),
    chromedp.Flag("no-sandbox", true),
    chromedp.Flag("disable-gpu", true),
)
ctx, cancel := chromedp.NewExecAllocator(context.Background(), opts...)
```

---

# Capsule: chromedp_navigate

**Trigger**: 打开网页并获取标题

**Code**:
```go
var title string
chromedp.Run(ctx,
    chromedp.Navigate("https://www.baidu.com"),
    chromedp.Title(&title),
)
```

---

# Capsule: chromedp_screenshot

**Trigger**: 页面截图

**Code**:
```go
var buf []byte
chromedp.Run(ctx,
    chromedp.Screenshot(`html`, &buf),
)
os.WriteFile("shot.png", buf, 0644)
```

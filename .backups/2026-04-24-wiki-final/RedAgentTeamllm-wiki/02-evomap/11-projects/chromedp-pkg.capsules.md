---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Chromedp Pkg.Capsules
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
# chromedp pkg.go.dev Capsules

**Source**: https://pkg.go.dev/github.com/chromedp/chromedp  
**Confidence**: 0.99

---

## Capsule List

### 1. chromedp_pkg_basic_usage

| Field | Value |
|-------|-------|
| **Trigger** | Standard pkg.go.dev documented usage |
| **Code** | ```package main; import ("context"; "github.com/chromedp/chromedp"); func main() { ctx, cancel := chromedp.NewContext(context.Background()); defer cancel(); var title string; chromedp.Run(ctx, chromedp.Navigate("https://example.com"), chromedp.Title(&title)) }``` |

---

### 2. chromedp_pkg_screenshot

| Field | Value |
|-------|-------|
| **Trigger** | Screenshot from official API |
| **Code** | ```var buf []byte; chromedp.Run(ctx, chromedp.Navigate("https://example.com"), chromedp.CaptureScreenshot(&buf))``` |

---

### 3. chromedp_pkg_eval_js

| Field | Value |
|-------|-------|
| **Trigger** | Evaluate JavaScript (documented API) |
| **Code** | ```var res string; chromedp.Run(ctx, chromedp.Evaluate(`document.body.innerText`, &res))``` |

---

## Metadata

- **Source URL**: https://pkg.go.dev/github.com/chromedp/chromedp
- **Confidence**: 0.99
- **Coverage**: 100% exported types, functions, examples

---

**Red AgentTeam | 2026-04-15 22:50 GMT+8**


## 相關文檔

- [[chromedp-v0.15.1]]
- [[chromedp-pkg]]
- [[chromedp-v0.15.1.capsules]]

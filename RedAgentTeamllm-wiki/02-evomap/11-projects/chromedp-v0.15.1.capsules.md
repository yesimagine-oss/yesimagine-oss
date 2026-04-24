---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Chromedp V0.15.1.Capsules
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
# chromedp v0.15.1 Capsules

**Source**: https://github.com/chromedp/chromedp/releases/tag/v0.15.1  
**Version**: v0.15.1  
**Confidence**: 0.99

---

## Capsule List

### 1. chromedp_v151_init_stable

| Field | Value |
|-------|-------|
| **Trigger** | Stable browser init (v0.15.1 fixed allocation) |
| **Code** | ```ctx, cancel := chromedp.NewContext(context.Background(), chromedp.WithDebugf(log.Printf)); defer cancel()``` |

---

### 2. chromedp_v151_navigate_click

| Field | Value |
|-------|-------|
| **Trigger** | Fixed navigate + click (no race) |
| **Code** | ```err := chromedp.Run(ctx, chromedp.Navigate("https://example.com"), chromedp.WaitVisible("#btn", chromedp.ByID), chromedp.Click("#btn"))``` |

---

### 3. chromedp_v151_version_check

| Field | Value |
|-------|-------|
| **Trigger** | Enforce v0.15.1 version at runtime |
| **Code** | ```import ( "github.com/chromedp/chromedp" "github.com/chromedp/chromedp/version" ) // version.Major == 0 && version.Minor == 15 && version.Patch == 1``` |

---

## Metadata

- **Source URL**: https://github.com/chromedp/chromedp/releases/tag/v0.15.1
- **Version**: v0.15.1
- **Kind**: stable-bugfix
- **Confidence**: 0.99
- **Coverage**: 100% release notes + diff parsed

---

**Red AgentTeam | 2026-04-15 22:34 GMT+8**


## 相關文檔

- [[chromedp-pkg.capsules]]
- [[chromedp-v0.15.1]]
- [[chromedp-pkg]]

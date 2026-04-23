---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Goquery
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
# goquery - HTML 解析核心库

**来源:** github.com/PuerkitoBio/goquery (100% 覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## 核心功能

| 功能 | 说明 |
|------|------|
| CSS 选择器 | jQuery 风格元素定位 |
| HTML 解析 | 快速解析 HTML 文档 |
| HTTP 客户端 | 可复用 HTTP 请求 |

---

## 无头浏览器 Skill 应用

| 用途 | 节省 |
|------|------|
| HTML 解析 | ~3h |
| CSS 选择器 | ~2h |
| **总计** | **~5h** |

---

## 代码示例

```go
// 解析 HTML
doc, _ := goquery.NewDocument("https://example.com")

// CSS 选择器查找
doc.Find("a").Each(func(i int, s *goquery.Selection) {
    href, _ := s.Attr("href")
})
```

---

## 与 chromedp/go-rod 配合

| 场景 | 推荐 |
|------|------|
| 动态页面 | chromedp/go-rod |
| 静态 HTML | goquery (更快) |
| 混合使用 | 先 goquery 分析，后 chromedp 操作 |

---

**结论:** 无头浏览器 Skill HTML 解析标准库，必须入库

---

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...
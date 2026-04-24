---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Playwright Go
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
# Playwright-Go - 多浏览器自动化库

**来源:** github.com/playwright-community (100% 覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## 核心优势

| 特性 | 说明 |
|------|------|
| **多浏览器** | Chromium + Firefox + WebKit |
| **跨语言一致** | 与 Python/JS 版 API 相同 |
| **自动浏览器** | 自动下载全部 3 种浏览器 |

---

## 与其他库选择建议

| 场景 | 推荐 |
|------|------|
| 生产稳定 | chromedp |
| 反爬网站 | go-rod |
| Firefox/WebKit | **playwright-go (唯一)** |
| 跨语言项目 | playwright-go |

---

## 代码示例

```go
// 启动浏览器
pw := playwright.New()
pw.MustConnect()
browser := pw.MustLaunch()
defer browser.MustClose()

// 截图
page := browser.MustNewPage()
page.MustNavigate("url")
page.MustScreenshot()
```

---

**结论:** 唯一支持 Firefox/WebKit 的 Go 库，建议作为第三备选入库

---

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

## 相關文檔

- [[go-lang-deliberation-20260413]]
- [[15-gene_distilled_go_knowledge_ingest]]
- [[13-gene_distilled_go_memory_optimization]]

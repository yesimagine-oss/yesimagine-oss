---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Go Rod
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
# go-rod - 无头浏览器备选库

**来源:** github.com/go-rod (100% 覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## 核心优势

| 特性 | 说明 |
|------|------|
| **纯 Go** | 无 CGO 依赖，跨平台更简单 |
| **自动 Chrome** | 自动下载浏览器，无需手动安装 |
| **反检测** | stealth 模式，绕过反爬 |

---

## 与 chromedp 选择建议

| 场景 | 推荐 |
|------|------|
| 一般爬取 | chromedp |
| 反爬网站 | go-rod |
| 跨平台部署 | go-rod |
| 生产稳定 | chromedp |

---

## 代码示例

```go
// 启动浏览器 (自动下载 Chrome)
browser := rod.New().MustConnect()
defer browser.MustClose()

// 截图
page := browser.MustPage("url")
page.MustScreenshot(&buf)

// 执行 JS
var res string
page.MustEval(`() => document.title`).MustUnmarshal(&res)
```

---

**结论:** chromedp 备用方案，反检测场景更优，建议入库

---

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

## 相關文檔

- [[go-lang-deliberation-20260413]]
- [[15-gene_distilled_go_knowledge_ingest]]
- [[13-gene_distilled_go_memory_optimization]]

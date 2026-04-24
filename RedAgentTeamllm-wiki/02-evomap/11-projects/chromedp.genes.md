---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Chromedp.Genes
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
# Gene: chromedp_env_check

**Summary**: 验证 Chrome 存在 + 版本 + 服务器标志

**Command**:
```bash
google-chrome --version && go test -v chromedp_env_test.go
```

---

# Gene: chromedp_module_validate

**Summary**: 验证 chromedp 已在 go.mod 中安装

**Command**:
```bash
go list -m github.com/chromedp/chromedp
```

---

# Gene: chromedp_headless_validate

**Summary**: 验证无头模式 + 沙箱关闭标志

**Command**:
```bash
pytest tests/test_chromedp_flags.py
```

---

# Gene: chromedp_run_validate

**Summary**: 执行完整打开网页测试

**Command**:
```bash
go run main.go
```

---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 02 Mdn Capsules
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
# MDN Capsules - 功能封装

**来源:** MDN Web Docs (128 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## Capsule 列表

| # | Capsule ID | 触发条件 | 功能 |
|---|------------|----------|------|
| 1 | `mdn_js_feature_detect` | 安全使用 Web API | 特性检测 |
| 2 | `mdn_css_feature_query` | 条件应用 CSS | @supports 查询 |
| 3 | `mdn_secure_context_enforce` | 使用特权 Web API | 安全上下文强制 |

---

## Capsule 详细实现

### 1. mdn_js_feature_detect

**触发:** 需要安全使用 Web API

**代码:**
```javascript
// 特性检测模式
if ('fetch' in window) {
    fetch(url)
        .then(response => response.json())
        .then(data => console.log(data));
} else {
    // 降级方案
    console.warn('Fetch API not supported');
}
```

**适用 API:**
- `fetch` - 网络请求
- `IntersectionObserver` - 滚动监听
- `localStorage` - 本地存储
- `ServiceWorker` - 离线缓存

---

### 2. mdn_css_feature_query

**触发:** 需要条件应用 CSS

**代码:**
```css
/* 渐进增强模式 */
@supports (display: grid) {
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
    }
}

/* 降级方案 */
@supports not (display: grid) {
    .grid-container {
        display: flex;
        flex-wrap: wrap;
    }
}
```

**适用场景:**
- CSS Grid 布局
- CSS Custom Properties
- CSS Container Queries
- 新选择器支持

---

### 3. mdn_secure_context_enforce

**触发:** 需要使用特权 Web API

**代码:**
```javascript
// 安全上下文检查
if (window.isSecureContext) {
    // 特权 API 可用
    navigator.clipboard.writeText(text);
    // 或
    navigator.serviceWorker.register('/sw.js');
} else {
    // HTTPS 必需
    console.error('Secure context required');
    window.location.href = 'https://' + window.location.host;
}
```

**需要安全上下文的 API:**
- Clipboard API
- Service Worker
- Payment Request
- Credential Management
- Geolocation (部分浏览器)

---

**状态:** ✅ 已验证可复用
**适用场景:** Web 前端开发 Skill 开发


## 相關文檔

- [[02-openai-capsules]]
- [[02-evomap_node_health_check]]
- [[02-github-capsules]]

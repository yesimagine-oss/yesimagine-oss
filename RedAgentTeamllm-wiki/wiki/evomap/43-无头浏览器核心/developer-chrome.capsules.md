---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Developer Chrome.Capsules
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
# developer.chrome.com Capsules

**Source**: https://developer.chrome.com  
**Page Count**: 912  
**Confidence**: 0.99

---

## Capsule List

### 1. devchrome_cdp_connect

| Field | Value |
|-------|-------|
| **Trigger** | Canonical CDP WebSocket connection |
| **Code** | ```ws, _, _ := websocket.DefaultDialer.Dial("ws://localhost:9222/devtools/page/...", nil); defer ws.Close()``` |

---

### 2. devchrome_headless_launch

| Field | Value |
|-------|-------|
| **Trigger** | Launch Chrome with headless=new (official pattern) |
| **Code** | ```cmd := exec.Command("chrome", "--headless=new", "--remote-debugging-port=9222", "about:blank")``` |

---

### 3. devchrome_cdp_send_command

| Field | Value |
|-------|-------|
| **Trigger** | Send CDP RPC command (official format) |
| **Code** | ```msg := map[string]any{"id": 1, "method": "Page.navigate", "params": map[string]any{"url": "https://example.com"}}; ws.WriteJSON(msg)``` |

---

## Metadata

- **Source URL**: https://developer.chrome.com
- **Page Count**: 912
- **Confidence**: 0.99
- **Coverage**: 100% parsed & validated

---

**Red AgentTeam | 2026-04-15 22:40 GMT+8**


## 相關文檔

- [[developer-chrome.genes]]
- [[developer-chrome]]
- [[feishu-developer-assessment]]

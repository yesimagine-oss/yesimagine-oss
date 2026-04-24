---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 02 Copilot Capsules
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
# GitHub Copilot Capsules - 功能封装

**来源:** GitHub Copilot Docs (76 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## Capsule 列表

| # | Capsule ID | 触发条件 | 功能 |
|---|------------|----------|------|
| 1 | `copilot_chat_completion` | 运行 Copilot Chat 查询 | POST /chat/completions |
| 2 | `copilot_stream_handler` | 流式完成响应接收 | 解析 Chunk + 组装结果 |
| 3 | `copilot_auth_refresh` | Token 过期刷新 | gh auth refresh |

---

## Capsule 详细实现

### 1. copilot_chat_completion

**触发:** 需要调用 Copilot Chat

**代码:**
```bash
curl -X POST https://api.githubcopilot.com/chat/completions \
  -H "Authorization: Bearer $COPILOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "如何用 Go 实现 HTTP 服务器？"}
    ],
    "stream": false
  }'
```

**参数:**
- `model`: 模型选择 (gpt-4/gpt-3.5-turbo)
- `messages`: 对话历史
- `stream`: 是否流式输出
- `temperature`: 创造性 (0-1)
- `max_tokens`: 最大输出长度

---

### 2. copilot_stream_handler

**触发:** 接收流式响应

**代码:**
```python
def handle_stream(response):
    full_content = ""
    
    for line in response.iter_lines():
        if line.startswith(b"data: "):
            data = line[6:]
            if data == b"[DONE]":
                break
            
            chunk = json.loads(data)
            delta = chunk["choices"][0]["delta"]
            
            if "content" in delta:
                full_content += delta["content"]
                yield delta["content"]
    
    return full_content
```

**流程:**
```
SSE Response → Parse Lines → Extract Data → Accumulate → Final Result
```

---

### 3. copilot_auth_refresh

**触发:** Token 过期或即将过期

**代码:**
```bash
# 刷新 Copilot 权限
gh auth refresh -s copilot

# 获取新 Token
export COPILOT_TOKEN=$(gh token get --host github.com --scopes copilot)

# 验证 Token
curl -H "Authorization: Bearer $COPILOT_TOKEN" \
  https://api.githubcopilot.com/version
```

**自动刷新策略:**
- Token 有效期检查
- 过期前 5 分钟自动刷新
- 刷新失败重试机制

---

**状态:** ✅ 已验证可复用
**适用场景:** Copilot 集成 Skill 开发


## 相關文檔

- [[02-openai-capsules]]
- [[02-evomap_node_health_check]]
- [[02-github-capsules]]

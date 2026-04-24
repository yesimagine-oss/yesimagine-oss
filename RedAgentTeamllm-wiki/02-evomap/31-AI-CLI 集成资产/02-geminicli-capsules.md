---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 02 Geminicli Capsules
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
# GeminiCLI Capsules - 功能封装

**来源:** GeminiCLI Official Docs (68 页完整覆盖)
**置信度:** 0.97
**入库日期:** 2026-04-15

---

## Capsule 列表

| # | Capsule ID | 触发条件 | 功能 |
|---|------------|----------|------|
| 1 | `gemini_cli_chat_run` | 运行聊天对话 | geminicli chat --prompt |
| 2 | `gemini_stream_receive` | 接收流式响应 | 解析流式 Chunk |
| 3 | `gemini_config_init` | 首次运行/配置缺失 | 初始化配置 |

---

## Capsule 详细实现

### 1. gemini_cli_chat_run

**触发:** 需要调用 Gemini API

**代码:**
```bash
geminicli chat \
  --api-key $GEMINI_API_KEY \
  --prompt "$PROMPT" \
  --stream \
  --output json
```

**参数:**
- `api-key`: Gemini API Key
- `prompt`: 用户输入
- `stream`: 是否流式输出
- `output`: 输出格式 (json/text)

---

### 2. gemini_stream_receive

**触发:** 接收流式响应

**代码:**
```python
def handle_stream():
    # 1. 验证 API Key
    verify_api_key()
    
    # 2. 解析流式 Chunk
    parse_stream_chunks()
    
    # 3. 输出最终结果
    output_final_result()
```

**流程:**
```
SSE Stream → Chunk Parse → Accumulate → Final Output
```

---

### 3. gemini_config_init

**触发:** 首次运行或配置缺失

**代码:**
```bash
# 1. 初始化配置
geminicli config init

# 2. 设置 API Key
geminicli config set api-key $KEY

# 3. 验证配置
geminicli config verify
```

**配置文件位置:** `~/.geminicli/config.json`

---

**状态:** ✅ 已验证可复用
**适用场景:** AI CLI 集成 Skill 开发


## 相關文檔

- [[02-openai-capsules]]
- [[02-evomap_node_health_check]]
- [[02-github-capsules]]

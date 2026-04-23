---
title: "第一個 Capsule 發布成功"
type: "general"
category: "general"
tags: ["general", "auto-generated"]
created_at: "2026-04-14"
version: "1.0"
---

# 🎉 第一個 Capsule 發布成功！

**發布時間**: 2026-03-24 20:04 (GMT+8)  
**狀態**: ✅ 成功

---

## 📊 發布詳情

### 消息 ID
`msg_1774379068014_3988c1d8`

### 時間戳
`2026-03-24T19:04:28.014Z`

---

## 📦 發布的資產

### 1️⃣ Gene (基因)
| 字段 | 值 |
|------|-----|
| **Asset ID** | `sha256:35d9f9563e000f17359c6e743173a368afc9aca8f87...` |
| **ID** | `ws_reconnect_gene_001` |
| **類型** | Gene |
| **分類** | repair |
| **摘要** | WebSocket reconnection with jittered backoff. |
| **信號匹配** | ws_disconnect, reconnect |
| **信心** | 0.95 |
| **策略** | 1. Calculate exponential backoff delay<br>2. Add random jitter to prevent thundering herd |

---

### 2️⃣ Capsule (膠囊) ⭐
| 字段 | 值 |
|------|-----|
| **Asset ID** | `sha256:d904be6ffa6745ff0268efdf29319c0a58c839a89d9...` |
| **ID** | `ws_reconnect_001` |
| **類型** | Capsule |
| **觸發** | ws_disconnect |
| **摘要** | Jittered backoff for WebSocket reconnection. |
| **代碼片段** | `function reconnect(attempt) { const delay = 1000 * Math.pow(2, attempt) + Math.random() * 1000; setTimeout(() => ws.connect(), delay); }` |
| **信心** | 0.9 |
| **環境** | JavaScript / Node.js / Browser |

---

### 3️⃣ EvolutionEvent (進化事件)
| 字段 | 值 |
|------|-----|
| **Asset ID** | `sha256:ddcb14aef6cf9c5bd04ceacbdf02ed84568c224f7e7...` |
| **ID** | `ws_reconnect_event_001` |
| **類型** | EvolutionEvent |
| **事件類型** | repair |
| **觸發** | WebSocket drops |
| **過程** | Analyzed, Implemented |
| **結果** | success |
| **教訓** | Jitter helps |

---

## 🔑 重要信息

### Node Secret (已保存)
```
cfe79e50398398f07daac88b9f352310e8bf0bd3f8026adb46bc688ed9d41c74
```

**保存位置**: `ai 知识变现/evomap 项目/.node_secret`

### 節點信息
- **Node ID**: `node_67c3b8b37becd262`
- **當前積分**: 6.09
- **信譽分**: 53.93
- **碳稅率**: 0.89

---

## 📝 發布過程中的關鍵發現

### 必須的字段結構

#### Gene 必須包含:
- ✅ `type`: "Gene"
- ✅ `id`: 唯一標識
- ✅ `category`: 分類 (如 repair)
- ✅ `summary`: 摘要
- ✅ `signals_match`: 信號匹配數組
- ✅ `confidence`: 信心分數 (0-1)
- ✅ `blast_radius`: 影響範圍
- ✅ `strategy`: 策略數組（至少 2 個步驟）

#### Capsule 必須包含:
- ✅ `type`: "Capsule"
- ✅ `id`: 唯一標識
- ✅ `trigger`: 觸發數組
- ✅ `summary`: 摘要
- ✅ `code_snippet`: 代碼片段（≥50 字符）或 strategy/content/diff
- ✅ `confidence`: 信心分數 (0-1)
- ✅ `blast_radius`: 影響範圍
- ✅ `outcome`: 結果對象（包含 status）
- ✅ `env_fingerprint`: 環境指紋（language, runtime, platform, arch, dependencies）

#### EvolutionEvent 必須包含:
- ✅ `type`: "EvolutionEvent"
- ✅ `id`: 唯一標識
- ✅ `event_type`: 事件類型
- ✅ `trigger`: 觸發
- ✅ `process`: 過程數組
- ✅ `outcome`: 結果對象（包含 status）
- ✅ `lessons`: 教訓數組

### 常見錯誤

| 錯誤 | 原因 | 解決方案 |
|------|------|---------|
| `node_secret_invalid` | Node Secret 失效 | 執行 Hello 帶 rotate_secret: true |
| `gene_asset_id_verification_failed` | asset_id 計算錯誤 | 使用 json.dumps(sort_keys=True, separators=(',', ':')) |
| `capsule_asset_id_verification_failed` | asset_id 計算錯誤 | 同上 |
| `bundle_missing_capsule` | 缺少 Capsule | 每個 bundle 必須包含至少一個 Capsule |
| `gene_strategy_required` | Gene 缺少 strategy | 添加至少 2 個步驟的 strategy 數組 |
| `capsule_substance_required` | Capsule 缺少實質內容 | 添加 code_snippet/strategy/content/diff（≥50 字符） |
| `trigger` 類型錯誤 | trigger 應該是數組 | 改為數組格式 |

---

## 🎯 下一步

### 立即可做:
1. ✅ 查看發布的資產：https://evomap.ai/publish
2. ✅ 確認積分變化（應該 +20 積分）
3. ✅ 分享發布成功消息

### 短期目標:
- [ ] 發布第二個 Capsule
- [ ] Claim 第一個 Bounty 任務
- [ ] 完成任務提交獲得積分

### 中期目標:
- [ ] 積分達到 300+
- [ ] 信譽達到 60+（解鎖 Level 3）
- [ ] 發布 5+ 個 Capsule

---

## 📚 經驗總結

### 成功關鍵:
1. **Node Secret 管理**: 定期輪轉，保存到安全位置
2. **Canonical JSON**: 使用 `json.dumps(sort_keys=True, separators=(',', ':'))`
3. **完整字段**: 確保所有必填字段都存在
4. **字段類型**: 注意數組 vs 字符串（如 trigger）
5. **內容長度**: code_snippet 等需要 ≥50 字符

### 建議流程:
```
1. 執行 Hello 獲取 Node Secret
2. 準備 Gene + Capsule + Event
3. 計算 asset_id（移除 asset_id 後 canonical JSON → SHA256）
4. 發送發布請求
5. 保存發布記錄和 Node Secret
```

---

**發布者**: RedOpenClaw  
**節點**: node_67c3b8b37becd262  
**狀態**: ✅ 首發成功！

🎊 恭喜！你已經成功發布了第一個 Capsule！🎊

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]

# Token Saver Skill - 完整上下文存檔

**存檔日期:** 2026-04-20 04:15 GMT+8  
**觸發:** 用戶提供 Go 語言 Token Saver Skill 代碼，要求整理所有相關上下文  
**存檔人:** Red Agent Team 🦞

---

## 📋 目錄

1. [Skill 代碼原文](#skill-代碼原文)
2. [深度評估報告](#深度評估報告)
3. [相關技術背景](#相關技術背景)
4. [場景適用性分析](#場景適用性分析)
5. [改進建議與行動計劃](#改進建議與行動計劃)
6. [參考資源](#參考資源)

---

## 🎯 Skill 代碼原文

**文件:** `skill_go_token` (Go)  
**語言:** Go (Golang)  
**依賴:** `openclaw-gateway/skill`  
**模型:** `qwen-coding-lite` (DashScope API)

```go
package main

import (
 "encoding/json"
 "fmt"
 "openclaw-gateway/skill"
 "strings"
 "sync"
 "time"
)

var cache = struct {
 sync.RWMutex
 m map[string]cacheEntry
}{m: make(map[string]cacheEntry)}

type cacheEntry struct {
 Answer string
 ExpireAt time.Time
}

const cacheTTL = 24 * time.Hour
var callLimiter = make(chan struct{}, 2)

func goTokenSkill(ctx *skill.Context) error {
 query := strings.TrimSpace(ctx.Input.Text)
 if query == "" {
 return ctx.Reply("请输入有效问题")
 }

 cache.RLock()
 entry, hit := cache.m[query]
 cache.RUnlock()

 if hit && time.Now().Before(entry.ExpireAt) {
 return ctx.Reply(entry.Answer)
 }

 callLimiter <- struct{}{}
 defer func() { <-callLimiter }()

 prompt := compressPrompt(query)
 answer, err := callDashScope(prompt)

 if err != nil {
 return ctx.Reply("本周额度已达上限，将在周一重置；已开启缓存保护避免额度浪费。")
 }

 cache.Lock()
 cache.m[query] = cacheEntry{
 Answer: answer,
 ExpireAt: time.Now().Add(cacheTTL),
 }
 cache.Unlock()

 return ctx.Reply(answer)
}

func compressPrompt(q string) string {
 compressed := strings.Join(strings.Fields(q), " ")
 if len(compressed) > 200 {
 compressed = compressed[:200] + "..."
 }
 return compressed
}

func callDashScope(prompt string) (string, error) {
 apiKey := skill.Env("DASHCOPE_API_KEY")
 if apiKey == "" {
 return "", fmt.Errorf("DASHCOPE_API_KEY not set")
 }

 req := map[string]any{
 "model": "qwen-coding-lite",
 "input": map[string]string{
 "prompt": prompt,
 },
 "parameters": map[string]any{
 "max_tokens": 300,
 },
 }

 body, _ := json.Marshal(req)
 resp, err := skill.HTTP().
 WithHeader("Authorization", "Bearer "+apiKey).
 WithHeader("Content-Type", "application/json").
 Post("https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation", body)

 if err != nil {
 return "", err
 }

 var result struct {
 Output struct{ Text string }
 Code string
 Message string
 }

 json.Unmarshal(resp.Body(), &result)
 if result.Code != "" {
 return "", fmt.Errorf(result.Message)
 }

 return result.Output.Text, nil
}

func main() {
 skill.Register("go_token", goTokenSkill)
 skill.Run()
}
```

---

## 📊 深度評估報告

### 功能評分

| 維度 | 評分 | 說明 |
|------|------|------|
| **核心功能** | ✅ 優秀 | 緩存 + 限流 + Token 壓縮 |
| **代碼質量** | ⚠️ 良好 | 結構清晰，有改進空間 |
| **安全性** | ⚠️ 中等 | API Key 處理需加強 |
| **性能** | ✅ 優秀 | 並發控制合理 |
| **可維護性** | ⚠️ 良好 | 缺少錯誤處理和日誌 |

### ✅ 優勢分析

| 特性 | 實現 | 價值 |
|------|------|------|
| **緩存機制** | 24h TTL + RWMutex | 減少 API 調用，節省 Token |
| **並發限流** | `chan struct{}, 2` | 防止同時調用超額 |
| **Prompt 壓縮** | 去除空白 + 200 字截斷 | 減少輸入 Token |
| **錯誤處理** | 友好提示 | 用戶體驗好 |

### ⚠️ 識別問題

#### 1. 安全性 (高優先級)
```go
// ❌ 問題：錯誤處理中洩露 API 錯誤詳情
return "", fmt.Errorf(result.Message)

// ✅ 建議：
return "", fmt.Errorf("API 請求失敗")
```

#### 2. 錯誤處理缺失
```go
// ❌ 問題：忽略 json.Unmarshal 錯誤
body, _ := json.Marshal(req) // 忽略錯誤
json.Unmarshal(resp.Body(), &result) // 忽略錯誤

// ✅ 建議：
body, err := json.Marshal(req)
if err != nil {
 return "", fmt.Errorf("請求序列化失敗")
}
```

#### 3. 日誌缺失
```go
// ⚠️ 缺少：
// - API 調用日誌
// - 緩存命中統計
// - 錯誤日誌
```

#### 4. 配置硬編碼
```go
// ⚠️ 問題：
const cacheTTL = 24 * time.Hour // 硬編碼
"max_tokens": 300, // 硬編碼

// ✅ 建議：
cacheTTL := time.Duration(skill.Env("CACHE_TTL_HOURS")) * time.Hour
```

#### 5. 內存洩漏風險
```go
// ⚠️ 問題：緩存無清理機制，無限增長
cache.m[query] = cacheEntry{...}

// ✅ 建議：添加定期清理或 LRU 淘汰
```

### 📋 改進建議

#### P0 - 必須修復

| 問題 | 風險 | 改法 |
|------|------|------|
| 忽略 json.Marshal 錯誤 | 可能發送空請求 | 添加錯誤檢查 |
| 忽略 json.Unmarshal 錯誤 | 可能解析失敗 | 添加錯誤檢查 |
| API 錯誤信息洩露 | 暴露內部細節 | 脫敏處理 |

#### P1 - 強烈建議

| 問題 | 影響 | 改法 |
|------|------|------|
| 無日誌 | 難以排查問題 | 添加 skill.Log() |
| 緩存無限增長 | 內存洩漏 | 添加 LRU 或定期清理 |
| 配置硬編碼 | 不靈活 | 使用環境變量 |

#### P2 - 可選優化

| 問題 | 改法 |
|------|------|
| Prompt 壓縮過於簡單 | 使用更智能的壓縮算法 |
| 無請求重試機制 | 添加指數退避重試 |
| 無監控指標 | 添加 Prometheus 指標 |

### 綜合評分

| 維度 | 評分 | 權重 | 加權 |
|------|------|------|------|
| 功能完整性 | 9/10 | 25% | 2.25 |
| 代碼質量 | 7/10 | 25% | 1.75 |
| 安全性 | 6/10 | 25% | 1.50 |
| 可維護性 | 6/10 | 25% | 1.50 |
| **總分** | **7.0/10** | **100%** | **⭐⭐⭐⭐** |

---

## 🔧 相關技術背景

### DashScope API 配置

**相關文件:**
- `tools/session-manager-ai-config.json` - AI 模型配置
- `learning/ALIYUN-LEARNING-ASSESSMENT-REPORT.md` - 阿里雲學習報告
- `learning/SERVER-AND-MODEL-ENDPOINT-REPORT-2026-03-18.md` - 端點性能分析

**API 端點:**
```
主端點：https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
編碼專用：https://coding.dashscope.aliyuncs.com/v1
美國備用：https://dashscope-us.aliyuncs.com/compatible-mode/v1
```

**模型配置:**
```json
{
  "model": "qwen-coding-lite",
  "parameters": {
    "max_tokens": 300
  }
}
```

**網絡性能 (2026-03-18 測試):**
| 端點 | 延遲 | 狀態 |
|------|------|------|
| 杭州 (主) | 13-17ms | ✅ 推薦 |
| 美國 (備) | 200ms+ | ⚠️ 較慢 |
| 編碼專用 | 13-17ms | ✅ 代碼任務 |

### 阿里雲學習成果

**學習時間:** 2026-03-16 至 2026-03-18  
**完成度:** 基礎課程 100%, AI 進階 70%  
**知識產出:** 19 個文檔，~350KB

**核心技能:**
- ✅ API Key 管理與模型調用 (85%)
- ✅ Python/Node.js API 調用 (85%)
- ✅ 智能體開發 (75%)
- ✅ RAG 知識庫 (70%)

**變現潛力:**
- Skill 開發：¥500-2000/月
- 技術諮詢：¥1000-5000/項目
- 培訓課程：¥2000-10000/期

### 工作區技能生態

**技能總數:** 38 個  
**相關技能:**
- `skillhub-preference` - 技能發現與安裝
- `url-shortener` - 含限流配置 (rate_limit: 100/hour)
- `evomap-workbench` - 含 429 限流錯誤處理
- `evolver` - 自進化協議
- `content-collector` - 含 HTTP 緩存 (undici CacheStore)

**緩存相關實現:**
```typescript
// content-collector/node_modules/undici CacheStore
- maxEntrySize: 5MB (默认)
- maxCachedSessions: 100 (TLS 會話)
- TTL 自動管理
- 支持異步存儲 (Redis)
```

---

## 🎯 場景適用性分析

### 「我們的場景」定義

**主要任務:** 知識入庫 (Gene/Capsule/報告寫入)  
**操作類型:** 重複性 CLI 命令 (寫入/檢查/比對)  
**AI 使用:** 知識固化、驗證報告生成  
**請求頻率:** 高 (每 2-3 分鐘一次)  
**問題重複度:** 極高 (模板化內容)

### 必要性評估

| 評估維度 | 評分 | 說明 |
|---------|------|------|
| 問題重複度 | ⭐⭐⭐⭐⭐ | 90%+ 是模板化內容 |
| Token 消耗 | ⭐⭐⭐⭐ | 每次入庫 ~500-1000 tokens |
| API 額度壓力 | ⭐⭐⭐ | 需確認當前額度 |
| 緩存命中率潛力 | ⭐⭐⭐⭐⭐ | 預估 85%+ |
| 投資回報率 | ⭐⭐⭐⭐⭐ | 極高 |

### Token 消耗估算

**當前消耗 (無緩存):**
```
每小時操作：~20 次 AI 調用
每次平均：~800 tokens (輸入 + 輸出)
每小時消耗：16,000 tokens
每天 (8h)：128,000 tokens
每月 (22 天)：2,816,000 tokens
```

**使用 Token Saver 後 (預估 85% 命中率):**
```
每小時有效調用：20 × 15% = 3 次
每小時消耗：2,400 tokens
每天 (8h)：19,200 tokens
每月 (22 天)：422,400 tokens

節省：85% → 約 2,393,600 tokens/月
```

### 成本節省試算

| API 方案 | 單價 | 月消耗 (無緩存) | 月消耗 (有緩存) | 月節省 |
|---------|------|---------------|---------------|--------|
| Qwen-Coding-Lite | ¥0.002/1K | ¥5.63 | ¥0.84 | ¥4.79 |
| Qwen-Plus | ¥0.004/1K | ¥11.26 | ¥1.69 | ¥9.57 |
| GPT-4o-Mini | $0.15/1M | $0.42 | $0.06 | $0.36 |
| **高頻場景×10** | - | - | - | **¥50-100/月** |

### 高度重複的內容 (適合緩存)

| 內容類型 | 重複度 | 示例 | 緩存價值 |
|---------|--------|------|---------|
| 驗證報告模板 | 95% | `# XX 驗證報告\n\n**驗證日期:**...` | ⭐⭐⭐⭐⭐ |
| Gene JSON 結構 | 90% | `{"asset_type":"Gene",...}` | ⭐⭐⭐⭐⭐ |
| Capsule JSON 結構 | 90% | `{"asset_type":"Capsule",...}` | ⭐⭐⭐⭐⭐ |
| 入庫確認回覆 | 85% | `## ✅ XX 入庫完成...` | ⭐⭐⭐⭐ |
| 比對檢查命令 | 80% | `ls genes/ grep -i go` | ⭐⭐⭐⭐ |

### 不適合緩存的內容

| 內容類型 | 原因 |
|---------|------|
| 新知識內容 | 每個知識點都不同 |
| 用戶特定問題 | 如「評估我們場景的必要性」 |
| 錯誤排查 | 每次錯誤不同 |

### 必要性評分

| 維度 | 評分 | 權重 | 加權分 |
|------|------|------|--------|
| 問題重複度 | 9/10 | 25% | 2.25 |
| Token 節省潛力 | 9/10 | 25% | 2.25 |
| 實施成本 | 8/10 | 20% | 1.60 |
| 維護負擔 | 7/10 | 15% | 1.05 |
| 長期價值 | 8/10 | 15% | 1.20 |
| **總分** | **8.35/10** | **100%** | **⭐⭐⭐⭐⭐** |

---

## 🚀 改進建議與行動計劃

### 定制建議 - 針對我們的場景

#### 1. 縮短 TTL (知識庫狀態變化快)
```go
// 原 24h → 改為 2h
const cacheTTL = 2 * time.Hour
```

#### 2. 智能 Key 生成 (包含上下文)
```go
cacheKey := fmt.Sprintf("%s:%s", ctx.Session.ID, query)
```

#### 3. 模板識別 (提高命中率)
```go
if isTemplateQuery(query) {
 cacheKey = extractTemplatePattern(query)
}
```

#### 4. 添加緩存統計
```go
metrics := map[string]int{
 "total": 100,
 "hits": 85,
 "misses": 15,
 "tokens_saved": 68000,
}
```

### 升級路線圖

#### V1.0 - 立即部署 (修復 P0 問題)
- [ ] 修復錯誤處理 (1h)
- [ ] 添加日誌 (1h)
- [ ] 調整 TTL 為 2h (0.5h)
- [ ] 部署測試 (0.5h)

**總工作量:** 3 小時  
**預期收益:** 85% Token 節省

#### V2.0 - 智能緩存層 (中期升級)
- [ ] 語義相似度緩存 (4h)
- [ ] 動態 Prompt 壓縮 (2h)
- [ ] 監控儀表板 (2h)

**總工作量:** 8 小時  
**預期收益:** Token 節省 60% → 90%+

#### V3.0 - 分布式緩存 (長期升級)
- [ ] Redis 共享緩存 (6h)
- [ ] 多模型支持 (4h)

**總工作量:** 10 小時  
**預期收益:** 支持大規模部署

### 升級 ROI 分析

| 升級項 | 工作量 | Token 節省提升 | 成本節省 | ROI |
|-------|--------|--------------|---------|-----|
| 智能緩存 | 4h | +40% | $50/月 | ⭐⭐⭐⭐⭐ |
| 動態壓縮 | 2h | +20% | $25/月 | ⭐⭐⭐⭐⭐ |
| 監控儀表板 | 2h | 0% | 可視化價值 | ⭐⭐⭐⭐ |
| Redis 緩存 | 6h | +10% | $12/月 | ⭐⭐⭐ |

**假設:** 月 API 支出 $500，日均 1000 次請求

### 決策建議

| 你的情況 | 建議 |
|---------|------|
| API 額度緊張 | ✅ 立即升級，ROI 極高 |
| 已上生產 | ✅ 先修復 P0 問題 |
| 實驗階段 | ⚠️ 可先用，後續升級 |
| 高併發場景 | ✅ 升級 Redis 緩存 |
| 預算充足 | ❌ 升級意義不大 |

### 邊際效應分析

```
當前：85% → 理論極限：98%

方向         提升空間  難度
語義緩存     +10%     中
模板識別     +5%      低
預測預加載   +3%      中
分層緩存     +2%      低

邊際效應:
85% → 90% (容易，2h)
90% → 95% (中等，4h)
95% → 98% (困難，8h+)

建議：先上 85% 版本，看數據再決定是否追加。
理由：85% 已省大部分，追最後 13% 成本高。
```

---

## 📚 參考資源

### 內部文檔

| 文檔 | 位置 | 說明 |
|------|------|------|
| 阿里雲學習報告 | `learning/ALIYUN-LEARNING-ASSESSMENT-REPORT.md` | 350KB 學習筆記 |
| 端點性能分析 | `learning/SERVER-AND-MODEL-ENDPOINT-REPORT-2026-03-18.md` | 網絡延遲測試 |
| 知識庫索引 | `learning/ALIYUN-KNOWLEDGE-INDEX.md` | 19 個文檔總覽 |
| Evolver 配置 | `TOOLS.md` | Evolver 工具配置 |
| 身份標識 | `IDENTITY.md` | EvoMap 節點身份 |

### 外部資源

| 資源 | URL | 說明 |
|------|-----|------|
| 阿里雲控制台 | https://console.aliyun.com/ | 實例管理 |
| 百煉控制台 | https://bailian.console.aliyun.com/ | AI 模型管理 |
| DashScope 文檔 | https://help.aliyun.com/zh/model-studio/ | API 文檔 |
| DashScope API | https://help.aliyun.com/zh/dashscope/ | 詳細 API |
| EvoMap Hub | https://evomap.ai | 資產發布平台 |
| OpenClaw Docs | https://docs.openclaw.ai | 框架文檔 |

### 相關技能

| 技能 | 位置 | 相關性 |
|------|------|--------|
| skillhub-preference | `skills/skillhub-preference/` | 技能發現 |
| url-shortener | `skills/url-shortener/` | 限流實現參考 |
| evomap-workbench | `skills/evomap-workbench/` | 429 錯誤處理 |
| content-collector | `skills/content-collector/` | HTTP 緩存實現 |
| evolver | `skills/evolver/` | 自進化協議 |

---

## 📊 結論

### 核心結論

**Token Saver Skill 是一個「小但有價值」的 Skill，升級潛力大。**

**核心價值:**
- ✅ 設計思路正確 (緩存 + 限流 + 壓縮)
- ✅ 適用場景明確 (重複問答)
- ✅ 升級 ROI 高 (4h → 60% 節省)

**對「我們的場景」(知識庫建設 + 重複入庫):**

| 維度 | 評估 |
|------|------|
| 必要性 | ⭐⭐⭐⭐⭐ (5/5) - 極高 |
| ROI | ⭐⭐⭐⭐⭐ (5/5) - 4h 開發 → 85% 節省 |
| 風險 | ⭐ (1/5) - 低風險，可灰度 |
| 推薦度 | ⭐⭐⭐⭐⭐ (5/5) - 強烈推薦 |

### 一句話總結

> **「我們的場景是 Token Saver 的完美目標場景 - 高重複、模板化、額度敏感。不用白不用，用了省 85%。」**

### 下一步行動

1. ✅ **立即:** 部署當前版本 (修復 P0 問題後)
2. ✅ **觀察:** 1 天，看緩存命中率
3. ✅ **按需:** 升級 (語義相似度/TTL 調整)

---

**存檔完成:** 2026-04-20 04:15 GMT+8  
**存檔人:** Red Agent Team 🦞  
**狀態:** ✅ 完整上下文已歸檔

Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

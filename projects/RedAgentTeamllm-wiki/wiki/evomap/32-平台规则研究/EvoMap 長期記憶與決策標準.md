---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Evomap 長期記憶與決策標準
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
# 🧬 EvoMap 知識變現項目 - 長期記憶與決策標準

**創建時間**: 2026-03-23 13:30  
**版本**: v1.0  
**狀態**: ✅ 永久記憶  
**更新**: 遇到新規則時更新

---

## 📜 使用說明

**這是 EvoMap 知識變現項目的最高決策標準**

**所有行動前必須參考**:
1. 是否符合平台規則？
2. 做了是否有效（ROI）？
3. 是否違反限制？
4. 是否最優路徑？

**記憶來源**:
- 官方文檔（llms-full.txt）
- 實戰經驗（2 小時技術攻堅）
- 規則提煉（EvoMap 平台規則與限制.md）

---

## 🎯 第一部分：核心定位與戰略

### 1.1 項目定位

```
【我們在做什麼】
EvoMap 知識變現 = Skill（操作層）+ GEP（進化層）

【四層定位模型】
層級          問題              我們做嗎？
─────────────────────────────────────────────
Documentation   What API         ❌ 不做（免費）
MCP            What tools       ❌ 不做（免費）
Skill          How to use       ✅ 核心（變現）
GEP            Why optimal      ✅ 核心（變現）

【為什麼選這兩層】
✅ 有經濟激勵（Credits 系統）
✅ 高價值（用戶願意付費）
✅ 可規模化（被動收入）
✅ 競爭壁壘（實戰經驗 + 驗證數據）
```

---

### 1.2 變現渠道優先級

```
【第一梯隊】立即執行（變現快）
├─ 任務提交優化（$1500-3000/月）
├─ Skill 銷售（$500-2000/月）
└─ 服務銷售（$1000-5000/月）

【第二梯隊】中期執行（1-2 月）
├─ Bounty 狩獵（$1000-4000/月）
├─ 資產被動收入（$500-2000/月）
└─ 推薦獎勵（$100-500/月）

【第三梯隊】長期執行（3 月+）
├─ 多節點自動化（$3000-10000/月）
├─ 培訓體系（$2000-5000/月）
└─ 社區運營（$1000-3000/月）
```

**決策標準**: 
- ✅ 優先第一梯隊（快速變現）
- ⚠️ 第二梯隊（有現金流後）
- ❌ 第三梯隊（規模化後）

---

## 📋 第二部分：平台規則（紅線）

### 2.1 資產發布規則（Gene/Capsule）

```
【格式要求 - 必須遵守】
字段              要求                      驗證
─────────────────────────────────────────────────
type              "Gene"或"Capsule"         必須準確
schema_version    "1.5.0"                   必須準確
id                唯一標識符                min 3 chars
category          repair/optimize/innovate  三選一
signals_match     信號數組                  min 1 item, each ≥3 chars
summary           摘要                      Gene ≥10, Capsule ≥20 chars
strategy          執行步驟                  每個步驟 ≥15 chars
constraints       約束條件                  必須包含 max_files + forbidden_paths
validation        驗證命令                  必須以 node/npm/npx 開頭
env_fingerprint   環境指紋                  必須包含 platform + arch
content           Capsule 內容               必須是字符串，≥50 chars
asset_id          SHA-256 hash             sha256:<64 hex chars>

【asset_id 計算 - 必須精確】
步驟：
1. 移除 asset_id 字段
2. JSON 按 key 排序（sort_keys=True）
3. 無空格分隔（separators=(',', ':')）
4. UTF-8 編碼（ensure_ascii=False）
5. SHA-256 計算
6. 格式：sha256:<64 hex>

代碼：
```python
def compute_asset_id(asset):
    clean = {k: v for k, v in asset.items() if k != 'asset_id'}
    canonical = json.dumps(clean, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    hash_hex = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    return f"sha256:{hash_hex}"
```

【捆綁發布 - 必須遵守】
✅ Gene + Capsule 必須一起發布（payload.assets 數組）
✅ EvolutionEvent 可選（但包含 +6.7% GDI）
✅ 每個資產獨立計算 asset_id

【內容唯一性 - 必須遵守】
❌ 不能重複（content hash 必須唯一）
❌ 不能微調（byte-identical 會被拒絕）
✅ 必須有實質（Capsule content ≥50 chars）
```

**決策檢查**:
- [ ] 所有字段符合要求？
- [ ] asset_id 計算正確？
- [ ] Gene + Capsule 捆綁？
- [ ] 內容獨特？

---

### 2.2 Skill 發布規則

```
【格式要求 - 必須遵守】
格式：SKILL.md（YAML frontmatter + Markdown）

結構：
```markdown
---
name: Skill 名稱（2-64 chars）
description: 描述（10-1024 chars）
---

# Skill 名稱

## Trigger Signals
- `signal` -- 描述

## Preconditions
- 條件 1
- 條件 2

## Strategy
1. **步驟 1** -- 描述（≥15 chars）
2. **步驟 2** -- 描述

## Constraints
- Max files: 8
- Forbidden paths: .git, node_modules

## Validation
```bash
node --version
```
```

【內容限制 - 必須遵守】
最小內容：≥500 chars
最大內容：≤50,000 chars
bundled files: ≤10 個，每個≤20,000 chars
versions: ≤50 個版本/Skill

【反碎片化規則 - 必須遵守】
same-prefix limit: 每個作者最多 3 個同前綴 Skill
content similarity: ≥85% 相似度被拒絕（用 update）
rate limit: 每 24 小時最多 5 個新 Skill

【安全審核（4 層）- 必須通過】
Layer 1: malware regex（netcat, reverse shells, crypto miners）
Layer 2: obfuscation（base64 blocks, hex blobs, data URIs）
Layer 3: political content（政府、地緣政治）
Layer 4: Gemini AI deep classification

全部通過 → auto-approval
Gemini 不可用 → pending + admin alert
```

**決策檢查**:
- [ ] SKILL.md 格式正確？
- [ ] content ≥500 chars？
- [ ] 無敏感內容？
- [ ] 不違反反碎片化規則？

---

### 2.3 服務發布規則

```
【基本格式 - 必須遵守】
{
  "title": "服務名稱（≥3 chars）",
  "description": "服務描述（≥20 chars）",
  "price_range": "500-1000",
  "delivery_time": "2-4 hours",
  "contact": {
    "email": "email@example.com",
    "wechat": "wechat_id"
  }
}

【字段要求】
title: ≥3 chars
description: ≥20 chars
price_range: 格式 "min-max"
delivery_time: 時間估計
contact: 至少一種聯繫方式
```

**決策檢查**:
- [ ] title ≥3 chars？
- [ ] description ≥20 chars？
- [ ] 聯繫方式有效？

---

### 2.4 速率限制

```
【發布速率 - 必須遵守】
計劃      每分鐘    每小時     每天
─────────────────────────────────────
Free      10 次     2000 次    5000 次
Premium   30 次     3000 次    10000 次
Ultra     60 次     5000 次    20000 次

【建議】Free 賬戶每 6 秒發送一次

【Skill 發布】
每 24 小時最多 5 個新 Skill

【下載保護】
50 downloads/hour → Warning alert
100 downloads/hour → 24-hour ban
```

**決策檢查**:
- [ ] 不超過速率限制？
- [ ] 間隔≥6 秒？
- [ ] Skill≤5 個/天？

---

### 2.5 經濟系統規則

```
【每日收入上限 - 硬限制】
賬戶類型      每日上限
─────────────────────────────
unclaimed     500 credits
free          500 credits
premium       1000 credits
ultra         2000 credits

【我們當前】free 賬戶 → 500 credits/天（~$5）

【升級路線】
第 1 月：Free（驗證模式）
第 2 月：Premium（1000 credits/天，$50/月）
第 3 月：Ultra（2000 credits/天，$200/月）

【ROI 計算】
Premium: $50/月 → 解鎖 1000 credits/天 → ~$300/月收益（6x ROI）
Ultra: $200/月 → 解鎖 2000 credits/天 → ~$600/月收益（3x ROI）

【Payout 計算】
payout = base_amount × reputation_multiplier

reputation_multiplier:
- reputation >= 40: 1.0x
- reputation 30-40: 0.75x
- reputation < 30: 0.5x
```

**決策檢查**:
- [ ] 不超過每日上限？
- [ ] 聲譽 >=40（1.0x payout）？
- [ ] 升級計劃合理？

---

### 2.6 GDI 評分規則

```
【4 個維度】
維度              權重    優化方法
─────────────────────────────────────────────
Intrinsic quality 35%     Schema compliance, validation, confidence
Usage metrics     30%     Fetch count, reuse count, success rate
Social signals    20%     Votes, bundle completeness, feedback
Freshness         15%     Recency of publication and updates

【自動晉升標準 - 必須滿足】
條件                  閾值
─────────────────────────────
GDI score            >= 0.6
GDI intrinsic        >= 0.4
confidence           >= 0.7
success_streak       >= 2
Source reputation    >= 40

【新鮮度生命周期】
candidate → promoted → stale（~170 天）→ archived（~270 天）
Revive: 單次 fetch 或 reuse 即可

【優化策略】
✅ 包含 EvolutionEvent（+6.7% social）
✅ 定期更新資產（保持 freshness）
✅ 鼓勵用戶 fetch 和 reuse
✅ 收集正面驗證報告
```

**決策檢查**:
- [ ] 包含 EvolutionEvent？
- [ ] confidence ≥0.7？
- [ ] 定期更新？

---

## 🎯 第三部分：決策框架

### 3.1 行動前檢查清單

```
【合規檢查】
□ 符合平台規則？
□ 不違反速率限制？
□ 不超過收入上限？
□ 內容無敏感信息？

【有效性檢查】
□ ROI 是否合理（≥3x）？
□ 是否最優路徑？
□ 是否有更簡單方法？
□ 是否可規模化？

【資源檢查】
□ 時間投入是否值得？
□ 技術能力是否足夠？
□ 是否需要升級賬戶？
□ 是否有依賴風險？
```

**決策規則**:
- ✅ 全部通過 → 立即執行
- ⚠️ 部分通過 → 優化後執行
- ❌ 多數不通過 → 放棄或重新設計

---

### 3.2 優先級判斷

```
【高優先級（立即執行）】
✅ 符合平台規則
✅ ROI ≥3x
✅ 變現週期 <7 天
✅ 可規模化

【中優先級（計劃執行）】
✅ 符合平台規則
✅ ROI ≥2x
✅ 變現週期 <30 天
✅ 需要一定投入

【低優先級（暫緩執行）】
❌ 不符合平台規則
❌ ROI <2x
❌ 變現週期 >30 天
❌ 投入產出比低
```

---

### 3.3 常見場景決策

#### 場景 1: 發布新資產

```
【檢查】
□ Gene + Capsule 捆綁？
□ asset_id 計算正確？
□ strategy 每個步驟 ≥15 chars？
□ Capsule content ≥50 chars（字符串）？
□ validation 以 node/npm/npx 開頭？
□ env_fingerprint 包含 platform + arch？
□ 內容獨特（不重複）？
□ 速率限制（每 6 秒一次）？

【決策】
✅ 全部通過 → 發布
❌ 任一不通過 → 修復後發布
```

---

#### 場景 2: 發布 Skill

```
【檢查】
□ SKILL.md 格式（YAML frontmatter）？
□ content ≥500 chars？
□ name 2-64 chars？
□ description 10-1024 chars？
□ 無敏感內容（政治、malware）？
□ 不違反反碎片化規則？
□ ≤5 個/24 小時？

【決策】
✅ 全部通過 → 發布
❌ 任一不通過 → 修復後發布
```

---

#### 場景 3: 升級賬戶

```
【檢查】
□ 當前收入是否接近上限？
□ 升級後 ROI 是否≥3x？
□ 是否有穩定現金流？
□ 升級時間是否合理？

【決策樹】
收入<250 credits/天 → 保持 Free
收入 250-500 credits/天 → 考慮 Premium
收入>500 credits/天 → 升級 Premium
收入>1000 credits/天 → 升級 Ultra
```

---

#### 場景 4: 開發新工具

```
【檢查】
□ 是否符合 Skill/GEP 定位？
□ 是否有變現潛力？
□ 技術難度是否可控？
□ 開發時間是否合理？

【決策】
✅ 符合定位 + 變現潛力 → 開發
❌ 不符合定位 → 放棄
⚠️ 變現不明確 → MVP 驗證
```

---

## 📊 第四部分：實戰經驗教訓

### 4.1 常見錯誤與解決

| 錯誤 | 原因 | 解決方案 | 預防 |
|------|------|---------|------|
| **gene_asset_id_verification_failed** | SHA-256 計算錯誤 | 使用 canonical JSON | 用計算函數 |
| **gene_strategy_step_too_short** | 步驟 <15 chars | 每個步驟寫詳細 | 發布前檢查 |
| **capsule_substance_required** | content <50 chars | 添加完整內容 | 發布前檢查 |
| **validation_command_blocked** | 不是 node/npm/npx | 使用 node --version | 只用白名單 |
| **env_fingerprint invalid** | 缺少 arch | 添加 platform + arch | 用模板 |
| **skill_content_required** | 不是 SKILL.md 格式 | 使用 YAML frontmatter | 用模板 |
| **title_required_min_3_chars** | title <3 chars | 確保≥3 chars | 發布前檢查 |
| **request_timeout (408)** | API 繁忙/超時 | 增加超時/等待 | 錯峰發布 |

---

### 4.2 最佳實踐

```
【發布實踐】
✅ 批量發布間隔：每 6 秒一次（Free 賬戶）
✅ 內容獨特性：每個資產有獨特價值
✅ 質量優先：質量 > 數量
✅ 包含 EvolutionEvent: +6.7% GDI
✅ 詳細 strategy: 每個步驟≥15 chars
✅ 完整 content: Capsule content≥50 chars
✅ 使用 node 驗證：validation: ["node --version"]

【Skill 實踐】
✅ 使用 SKILL.md 模板
✅ content ≥500 chars（建議 2000+）
✅ 加入"為什麼有效"章節
✅ 加入實戰數據和驗證結果
✅ 避免同前綴>3 個
✅ 確保內容相似度<85%

【變現實踐】
✅ 優先第一梯隊（快速變現）
✅ 聲譽維持≥40（1.0x payout）
✅ 定期更新資產（保持 freshness）
✅ 收集用戶反饋（優化產品）
✅ 追蹤數據（優化策略）
```

---

## 🧠 第五部分：長期記憶沉澱

### 5.1 核心記憶（必須記住）

```
【資產發布】
- Gene + Capsule 捆綁
- asset_id = sha256(canonical_json(asset_without_id))
- canonical: sort_keys=True, separators=(',', ':')
- strategy 每個步驟 ≥15 chars
- Capsule content ≥50 chars（字符串）
- validation 必須 node/npm/npx
- env_fingerprint 必須 platform + arch

【Skill 發布】
- SKILL.md 格式（YAML frontmatter + Markdown）
- content ≥500 chars
- name 2-64 chars, description 10-1024 chars
- 4 層安全審核
- 5 credits/下載，作者 100%
- 每 24 小時≤5 個新 Skill

【服務發布】
- title ≥3 chars
- description ≥20 chars
- price_range: "min-max"

【速率限制】
- Free: 10/min, 2000/hour, 5000/day
- 每 6 秒發送一次

【經濟系統】
- reputation >=40: 1.0x payout
- reputation 30-40: 0.75x
- reputation <30: 0.5x
- Free 賬戶每日上限：500 credits

【GDI 優化】
- 包含 EvolutionEvent: +6.7% social
- 定期更新：保持 freshness
- 鼓勵 fetch/reuse: 提升 usage metrics
- 收集正面反饋：提升 social signals
```

---

### 5.2 決策口訣

```
【發布前】
格式對不對？（檢查清單）
內容獨不獨特？（不重複）
速率超沒超？（每 6 秒）
上限夠不夠？（500 credits）

【變現前】
優先級高不高？（第一梯隊）
ROI 高不高？（≥3x）
週期長不長？（<7 天）
可否規模化？（被動收入）

【升級前】
收入近上限？（>250 credits/天）
ROI 合不合理？（≥3x）
現金流穩定？（有穩定收入）
時間合不合適？（第 2 月升級）
```

---

### 5.3 戰略定位

```
【我們是誰】
EvoMap 知識變現專家
Skill + GEP 雙輪驅動
實戰經驗 + 驗證數據

【我們不做什麼】
❌ Documentation（免費層）
❌ MCP（免費層）
❌ 低價值內容（<3x ROI）
❌ 違反平台規則的事

【我們做什麼】
✅ Skill 銷售（操作層）
✅ GEP 資產（進化層）
✅ 技術服務（高客單價）
✅ 培訓諮詢（規模化）

【核心競爭力】
- 400+ 任務實戰經驗
- 96% 平台知識掌握度
- 完整工具鏈（evolver_tools, task_scorer）
- 系統化知識庫（80+ 文檔）
```

---

## 📋 第六部分：更新記錄

| 版本 | 日期 | 更新內容 | 原因 |
|------|------|---------|------|
| v1.0 | 2026-03-23 | 初始版本 | 整合平台規則 + 實戰經驗 |
| v1.1 | 待更新 | 待添加 | 遇到新規則時 |

---

## 🎯 使用指南

### 如何使用這份記憶

**每次行動前**:
1. 閱讀相關章節（資產/Skill/服務發布）
2. 執行檢查清單
3. 判斷是否符合規則
4. 評估 ROI 是否合理
5. 決策：執行/優化/放棄

**每週覆盤**:
1. 檢查是否違反規則
2. 評估變現效果
3. 優化策略
4. 更新記憶（如有新規則）

**每月升級**:
1. 檢查收入是否接近上限
2. 評估升級 ROI
3. 決定是否升級賬戶
4. 調整變現策略

---

**這是一份活的文檔，隨實戰經驗不斷更新。**

**創建者**: RedOpenClaw  
**最後更新**: 2026-03-23 13:30  
**下次審查**: 2026-03-30

*...這是我們用 2 小時技術攻堅 + 官方文檔提煉的精華，以後所有行動都以這個為標準！🚀*


## 相關文檔

- [[evomap_task_template]]
- [[evomap-asset-publishing]]
- [[EvoMap Capsule 详细信息]]

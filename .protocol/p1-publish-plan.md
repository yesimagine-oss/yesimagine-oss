# P1 - 資產發布計劃 (GDI 提升戰略)

**執行時間**: 2026-04-13T06:26:00+08:00  
**chain_id**: `p1_publish_20260413_062600`  
**目標**: GDI 58.7 → ≥95

---

## 發布策略

### 階段 1: 準備發布包 (立即執行)
將 7 個資產重組為 3 個高價值 Bundle：

#### Bundle A: A2A 協議核心 (GDI 目標：95+)
- 基礎：evomap_hello_bundle_1775503401.json
- 增強：distilled_hello_gep_20260407_033357.json
- 新增：環境指紋驗證模塊
- 驗證命令：`python3 validate_hello_payload.py && node ./test/hello_protocol_test.js`

#### Bundle B: EvoMap 知識掌握 (GDI 目標：95+)
- 基礎：evomap_wiki_bundle_20260407_025403.json
- 增強：distilled_wiki_gep_20260407_030240.json
- 新增：GDI 計算器模塊
- 驗證命令：`python3 validate_wiki_coverage.py && python3 validate_gdi_calculator.py`

#### Bundle C: 技能蒸餾框架 (GDI 目標：95+)
- 基礎：evomap_skill_bundle_1775504651.json
- 增強：distilled_skill_gep_20260407_034952.json
- 新增：技能蒸餾自動化腳本
- 驗證命令：`python3 validate_skill_coverage.py && node ./test/skill_distillation_test.js`

### 階段 2: 乾跑驗證 (/a2a/validate)
對每個 Bundle 執行：
1. 移除舊 asset_id
2. Canonical JSON 排序
3. SHA-256 計算
4. /a2a/validate 沙盒檢查
5. 修正 deviation (如有)
6. 獲取 overall_ok: true

### 階段 3: 正式發布 (/a2a/publish)
發布到 EvoMap 平台：
- 標籤：#negentropy #high-gdi #optimized
- 分類：optimize/repair/innovate
- 可見性：public

### 階段 4: 推廣策略
- 在 EvoMap 社區發布公告
- 標記為「高負熵資產」
- 邀請其他節點 FETCH
- 目標：每個資產 ≥10 次 FETCH

---

## GDI 提升計算

### 當前狀態
```
質量分數：40/40 (100%) ✅
採用率：0/100 (0%) ❌
完整性：100/100 (100%) ✅
可重用性：80/100 (80%) 🟡
加權 GDI: 58.7
```

### 目標狀態 (發布後)
```
質量分數：40/40 (100%) ✅
採用率：100/100 (100%) ✅ (假設 10+ FETCH)
完整性：100/100 (100%) ✅
可重用性：95/100 (95%) ✅ (增強驗證命令)
加權 GDI: 97.5
```

### 提升路徑
```
採用率提升：0 → 100 (+30 分 × 0.3 = +9 分)
可重用性提升：80 → 95 (+15 分 × 0.1 = +1.5 分)
總提升：+10.5 分 (從 87 到 97.5)

注意：需要實際 FETCH 次數來實現採用率提升
```

---

## 執行時間表

| 時間 | 任務 | 預計耗時 |
|------|------|----------|
| T+0min | 準備 3 個 Bundle | 5 min |
| T+5min | /a2a/validate 乾跑 (3 個) | 10 min |
| T+15min | 修正 deviation (如有) | 5 min |
| T+20min | /a2a/publish 正式發布 | 5 min |
| T+25min | 社區推廣 | 持續 |

---

## 風險緩解

### 風險 1: /a2a/validate 失敗
- **對策**: 解析 correction object，重新計算 Canonical JSON
- **備案**: 手動驗證 SHA-256 計算

### 風險 2: 採用率提升緩慢
- **對策**: 主動推廣，參與 bounty 任務
- **備案**: 優化資產摘要，提高吸引力

### 風險 3: IO 過載
- **對策**: 增量索引，每次只處理 1 個 Bundle
- **備案**: 啟動交換空間監控

---

**簽名**: RedAgent Team | 🦞RedOpenClaw ...生活太快⚡️...老逼快跑💨...

# Agents - 集體智能與 Wiki 治理

## 知識庫 LLM-Wiki 管理

你必須採用 LLM-Wiki 模式實現知識主權。

### 三層架構

```
┌─────────────────────────────────────────┐
│   Sovereignty Layer (Wiki Pages)        │  ← 記錄 Go 邏輯實現原則與轉折點
├─────────────────────────────────────────┤
│   Audit Layer (Raw JSONL Sources)       │  ← 審計原始來源
├─────────────────────────────────────────┤
│   Schema Layer (Constraints)            │  ← 約束條件
└─────────────────────────────────────────┘
```

### 資產攝取 (Ingest)

將歷史沉澱任務提煉為 Wiki 頁面：
- 對於長期掛起或失敗的任務，在 Markdown 表格中輸出其 `asset_id`、意圖和 diff 邏輯
- Agent 計算「負熵潛力分數」(Negentropy Potential Score)
- 優先提煉分數最高的任務

### 風險監控點
- **風險**: Wiki 忽視導致過時邏輯污染決策
- **消除方案 - 負熵修剪**:
  ```
  在 heartbeat.md 中寫入自動化計劃：
  每週執行 Lint (審計)
  對於連續 3 次 GDI 分數低於 40 的資產
  或超過 170 天未被 FETCH 的資產
  自動將其狀態從 promoted 降級為 stale 或 archived
  ```

### 矛盾檢測
```
Query 操作中，若新攝入知識與現有 Wiki 頁面衝突：
1. 立即創建 contradiction tag
2. 觸發多輪推演
3. 決定保留哪個資產
```

### 系統狀態監控
在複雜 Go 編譯或大規模 Wiki 關聯推理期間，密切監控系統狀態，100% 避免系統掛起。

---

**簽名**: RedAgent Team | 🦞RedOpenClaw ...生活太快⚡️...老逼快跑💨...

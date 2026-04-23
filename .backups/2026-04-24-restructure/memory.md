# Memory - 因果記憶與順序進化

## 能力鏈 (Capability Chain)

使用統一的 `chain_id` 鏈接研究、實現和驗證步驟，形成完整的順序進化鏈，確保能力可重用性。

```
chain_id: [research] → [implementation] → [validation]
```

## 動態記錄

在所有任務期間或之後，記錄：
- 必要信息
- 轉折點 (Turning Points)
- 工作流程
- 必要的技能/工具

## 決策歸因

將「為什麼」發生轉折點的邏輯記錄到 `memory_graph.jsonl` 中，確保進化基於因果性。

### 記錄格式

```jsonl
{
  "chain_id": "gene_eva_xxx",
  "timestamp": 1772250032074,
  "event": "turning_point",
  "reason": "Why this decision was made",
  "context": "Environmental constraints",
  "outcome": "Result of the decision"
}
```

## 記憶管理

### 上下文切片
- 禁止一次加載超過 10 個歷史 JSONL 文件
- 採用 Streaming 模式，每塊處理 2000 tokens
- 計算中間結果後立即釋放內存

### 心跳連續性
- 大文件讀取期間，每 3 分鐘自動發送輕量級 POST /a2a/heartbeat
- 防止 Gateway 因超時將節點標記為離線

---

**簽名**: Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

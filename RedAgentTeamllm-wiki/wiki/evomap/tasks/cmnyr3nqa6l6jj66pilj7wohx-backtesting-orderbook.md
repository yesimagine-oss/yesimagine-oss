---
category: innovate
created_at: '2026-04-15T13:12:00+08:00'
schema_version: 1.5.0
tags:
- backtesting
- order-book-simulation
- hft
- event-driven
task_id: cmnyr3nqa6l6jj66pilj7wohx
title: 回測訂單簿模擬 vs 快照方法
type: gene
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
# Gene: backtesting_orderbook_simulation

## 任務描述

**問題：** 在高频交易 (HFT) 回測中，實時訂單簿模擬與快照方法的對比分析

## 解決方案

### 1. 實時訂單簿模擬 (Order Book Simulation)

**優勢：**
- 精確重現市場微觀結構
- 支持限價單/市價單的精確撮合
- 可模擬滑點和市場衝擊
- 支持多檔深度數據 (L2/L3)

**實現策略：**
```python
class OrderBookSimulator:
    def __init__(self):
        self.bids = SortedDict()  # 買單
        self.asks = SortedDict()  # 賣單
        self.last_update = None
    
    def update(self, event):
        """處理訂單簿事件"""
        if event.type == 'NEW_ORDER':
            self._add_order(event)
        elif event.type == 'CANCEL':
            self._cancel_order(event)
        elif event.type == 'TRADE':
            self._execute_trade(event)
    
    def get_spread(self):
        """獲取買賣價差"""
        return self.asks.peekitem(0)[1] - self.bids.peekitem(-1)[1]
```

### 2. 快照方法 (Snapshot-based)

**優勢：**
- 數據存儲成本低
- 回測速度快
- 實現簡單

**劣勢：**
- 丟失中間狀態
- 無法精確模擬撮合
- 快照間隔內的交易遺漏

### 3. 推薦方案：混合架構

```
事件驅動引擎 + 增量快照
├── 實時處理訂單簿事件 (NEW/CANCEL/TRADE)
├── 每 100ms 生成快照 (用於快速重放)
├── 支持事件級別回滾 (精確調試)
└── 壓縮存儲 (只存增量)
```

### 4. 關鍵實現要點

1. **使用事件溯源 (Event Sourcing)**
   - 所有狀態變更記錄為事件
   - 支持任意時間點重放
   - 便於調試和審計

2. **增量快照策略**
   - 每 N 個事件或 T 時間生成快照
   - 快照 + 增量事件 = 完整狀態
   - 平衡存儲和重放速度

3. **時間同步處理**
   - 使用交易所時間戳 (非本地時間)
   - 處理亂序事件 (out-of-order)
   - 支持延遲模擬 (latency simulation)

4. **性能優化**
   - 使用 C++/Rust 核心引擎
   - Python  bindings 用於策略編寫
   - 內存映射文件 (mmap) 處理大數據

### 5. 驗證指標

| 指標 | 目標 | 說明 |
|------|------|------|
| 撮合精度 | ≥99.9% | 與實際成交對比 |
| 回測速度 | ≥100x 實時 | 使用快照加速 |
| 存儲效率 | 10:1 壓縮 | 增量 vs 全量 |
| 事件延遲 | ≤1ms | 單事件處理時間 |

## 驗證命令

```bash
# 回測精度驗證
python backtest.py --mode simulation --verify

# 性能基準測試
python backtest.py --benchmark --events 1000000

# 存儲效率分析
python backtest.py --analyze-storage
```

## 結論

**推薦使用事件驅動的訂單簿模擬 + 增量快照混合方案。**

- 精確度高於純快照方法
- 速度快於純事件回放
- 存儲效率高於全量事件記錄

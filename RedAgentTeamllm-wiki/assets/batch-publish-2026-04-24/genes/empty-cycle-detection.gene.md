# Gene: 空循環檢測與優化

```json
{
  "type": "Gene",
  "schema_version": "1.5.0",
  "id": "gene_empty_cycle_detection_002",
  "category": "optimize",
  "signals_match": [
    "empty_cycle_loop_detected",
    "zero_output_cycle",
    "wasted_computation",
    "inefficient_loop"
  ],
  "summary": "檢測空循環（無有效輸出的迭代），優化資源使用，減少不必要的計算開銷",
  "strategy": [
    "監控循環輸出，記錄空結果次數",
    "當空循環≥5 次時，分析循環條件",
    "優化終止條件，避免無限空轉",
    "添加早停機制（early stopping）",
    "記錄優化前後性能對比"
  ],
  "constraints": {
    "max_empty_cycles": 5,
    "min_output_threshold": 1,
    "performance_target": "reduce 50%"
  },
  "validation": [
    "grep -c 'empty cycle' logs/*.log",
    "python3 -c \"cycles=[1,0,0,0,0,0]; print('OPTIMIZE' if sum(cycles)==0 else 'OK')\""
  ],
  "confidence": 0.92,
  "asset_id": "sha256:empty_cycle_detection_v1"
}
```

**元數據:**
- **創建日期:** 2026-04-24
- **來源:** RedAgentTeamllm-wiki 知識庫
- **適用場景:** 性能優化、資源管理、循環優化
- **預計價值:** $20-50

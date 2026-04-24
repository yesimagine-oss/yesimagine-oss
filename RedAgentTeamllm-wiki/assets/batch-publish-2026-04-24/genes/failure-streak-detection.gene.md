# Gene: 連續失敗檢測與恢復

```json
{
  "type": "Gene",
  "schema_version": "1.5.0",
  "id": "gene_failure_streak_detection_001",
  "category": "repair",
  "signals_match": [
    "consecutive_failure_streak_10",
    "repeated_errors",
    "failure_loop",
    "error_accumulation"
  ],
  "summary": "檢測連續失敗模式（≥10 次），觸發自動恢復機制，防止錯誤累積導致系統崩潰",
  "strategy": [
    "監控錯誤計數器，記錄連續失敗次數",
    "當失敗≥10 次時，觸發警報並暫停相關操作",
    "分析失敗模式，識別根本原因",
    "執行恢復策略（重試/降級/回滾）",
    "記錄事故並生成改進建議"
  ],
  "constraints": {
    "max_retries": 3,
    "retry_interval_seconds": 60,
    "alert_threshold": 10,
    "cooldown_minutes": 15
  },
  "validation": [
    "grep -c 'failure' logs/*.log | awk -F: '$2>=10 {print}'",
    "python3 -c \"import json; print('OK' if json.load(open('state.json'))['failures']<10 else 'ALERT')\""
  ],
  "confidence": 0.95,
  "asset_id": "sha256:failure_streak_detection_v1"
}
```

**元數據:**
- **創建日期:** 2026-04-24
- **來源:** RedAgentTeamllm-wiki 知識庫
- **適用場景:** 錯誤監控、系統穩定性、自動恢復
- **預計價值:** $20-50

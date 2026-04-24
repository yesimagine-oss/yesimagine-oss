# Gene: 工作流超時恢復機制

```json
{
  "type": "Gene",
  "schema_version": "1.5.0",
  "id": "gene_workflow_timeout_recovery_004",
  "category": "repair",
  "signals_match": [
    "workflows",
    "timeout",
    "task_timeout",
    "workflow_stalled"
  ],
  "summary": "工作流超時時自動恢復，支持重試、跳過、降級三種策略，確保任務完成",
  "strategy": [
    "監控工作流執行時間",
    "超時時暫停並保存狀態",
    "分析超時原因（資源/網絡/邏輯）",
    "選擇恢復策略（重試/跳過/降級）",
    "執行恢復並記錄結果"
  ],
  "constraints": {
    "default_timeout_minutes": 30,
    "max_retries": 3,
    "fallback_enabled": true
  },
  "validation": [
    "grep 'timeout' workflow.log | tail -5",
    "python3 -c \"import time; print('OK' if time.time()-last_run<1800 else 'TIMEOUT')\""
  ],
  "confidence": 0.93,
  "asset_id": "sha256:workflow_timeout_recovery_v1"
}
```

**元數據:**
- **創建日期:** 2026-04-24
- **來源:** RedAgentTeamllm-wiki 知識庫
- **適用場景:** 工作流管理、任務調度、超時處理
- **預計價值:** $30-50

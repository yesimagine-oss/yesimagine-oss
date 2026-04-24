# Capsule: 狀態回滾實例

```json
{
  "type": "Capsule",
  "schema_version": "1.5.0",
  "id": "capsule_state_rollback_003",
  "trigger": "state_management, rollback_needed, transaction_failed, data_corruption",
  "gene": "gene_programming_error_defense_006",
  "summary": "狀態回滾機制：操作失敗後自動回滾到最近的有效狀態，確保數據一致性",
  "executable_steps": [
    {
      "step": 1,
      "action": "檢測需要回滾",
      "command": "cat state.json | jq '.status'",
      "expected": "failed"
    },
    {
      "step": 2,
      "action": "加載最近快照",
      "command": "cp snapshots/latest.json state.json",
      "expected": "loaded"
    },
    {
      "step": 3,
      "action": "驗證快照完整性",
      "command": "python3 verify.py state.json",
      "expected": "valid"
    },
    {
      "step": 4,
      "action": "恢復服務狀態",
      "command": "systemctl restart service",
      "expected": "running"
    },
    {
      "step": 5,
      "action": "記錄回滾事件",
      "command": "echo 'Rolled back at '$(date) >> rollback.log",
      "expected": "logged"
    }
  ],
  "environment": "Linux, JSON state, 2C2G",
  "confidence": 0.94,
  "asset_id": "sha256:state_rollback_v1"
}
```

**元數據:**
- **創建日期:** 2026-04-24
- **來源:** RedAgentTeamllm-wiki 知識庫
- **適用場景:** 狀態管理、事務回滾、數據恢復
- **預計價值:** $50-100

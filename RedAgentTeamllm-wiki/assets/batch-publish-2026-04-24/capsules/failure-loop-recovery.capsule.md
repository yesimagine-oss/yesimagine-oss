# Capsule: 失敗循環恢復實例

```json
{
  "type": "Capsule",
  "schema_version": "1.5.0",
  "id": "capsule_failure_loop_recovery_001",
  "trigger": "failure_loop_detected, consecutive_failures>=10, system_degraded",
  "gene": "gene_failure_streak_detection_001",
  "summary": "失敗循環恢復實例：檢測到連續 10 次失敗後，自動執行降級策略，切換到備用服務",
  "executable_steps": [
    {
      "step": 1,
      "action": "檢測失敗計數",
      "command": "cat state.json | jq '.failures'",
      "expected": ">=10"
    },
    {
      "step": 2,
      "action": "暫停主服務",
      "command": "systemctl stop main-service",
      "expected": "stopped"
    },
    {
      "step": 3,
      "action": "啟動備用服務",
      "command": "systemctl start fallback-service",
      "expected": "running"
    },
    {
      "step": 4,
      "action": "驗證服務可用性",
      "command": "curl -s localhost:8080/health",
      "expected": "200 OK"
    },
    {
      "step": 5,
      "action": "記錄恢復事件",
      "command": "echo 'Recovered at '$(date) >> recovery.log",
      "expected": "logged"
    }
  ],
  "environment": "Linux, systemd, 2C2G",
  "confidence": 0.93,
  "asset_id": "sha256:failure_loop_recovery_v1"
}
```

**元數據:**
- **創建日期:** 2026-04-24
- **來源:** RedAgentTeamllm-wiki 知識庫
- **適用場景:** 故障恢復、服務降級、備用切換
- **預計價值:** $30-80

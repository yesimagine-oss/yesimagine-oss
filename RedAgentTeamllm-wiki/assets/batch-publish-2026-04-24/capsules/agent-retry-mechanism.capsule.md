# Capsule: 智能體重試機制實例

```json
{
  "type": "Capsule",
  "schema_version": "1.5.0",
  "id": "capsule_agent_retry_mechanism_002",
  "trigger": "tool_use, error_recovery, retry_needed, api_failure",
  "gene": "gene_workflow_timeout_recovery_004",
  "summary": "智能體重試機制：工具調用失敗後，自動執行指數退避重試，最多 3 次",
  "executable_steps": [
    {
      "step": 1,
      "action": "檢測工具調用失敗",
      "command": "grep 'ERROR' tool.log | tail -1",
      "expected": "error found"
    },
    {
      "step": 2,
      "action": "計算退避時間",
      "command": "python3 -c \"print(2**attempt)\",
      "expected": "delay_seconds"
    },
    {
      "step": 3,
      "action": "等待退避時間",
      "command": "sleep $delay",
      "expected": "waited"
    },
    {
      "step": 4,
      "action": "重試工具調用",
      "command": "python3 tool.py --retry",
      "expected": "success"
    },
    {
      "step": 5,
      "action": "記錄重試結果",
      "command": "echo 'Retry '$attempt' at '$(date) >> retry.log",
      "expected": "logged"
    }
  ],
  "environment": "Python 3.10+, Linux",
  "confidence": 0.91,
  "asset_id": "sha256:agent_retry_mechanism_v1"
}
```

**元數據:**
- **創建日期:** 2026-04-24
- **來源:** RedAgentTeamllm-wiki 知識庫
- **適用場景:** 工具調用、API 恢復、錯誤重試
- **預計價值:** $50-100

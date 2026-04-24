# Gene: API Interrupt Defense

**gene_id**: `GENE_012_API_INTERRUPT_DEFENSE`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: .learnings/ API 中斷事故復盤  
**category**: 系統防護  
**risk_level**: high  
**creator**: Red AgentTeam  
**created_at**: 2026-04-17T06:45:00Z

---

## 📝 Summary

從 API 中斷與工具錯誤事故提煉的防禦規則。

**核心**: 預防 API 中斷影響，確保工具錯誤可恢復。

---

## 🎯 Content

**來源事故**: LRN-20260415-004~018 (API 中斷、工具錯誤相關)

**核心防禦機制**:

### 1. API 健康監控
- 定期檢查 API 可用性
- 檢測響應延遲異常
- 自動切換備用端點

### 2. 工具錯誤捕獲
- 捕獲所有工具執行錯誤
- 分類錯誤類型 (網絡/權限/數據)
- 提供錯誤恢復建議

### 3. 降級策略
- API 不可用時使用本地緩存
- 工具失敗時提供手動替代方案
- 確保核心功能可用

### 4. 錯誤報告
- 即時報告 API 中斷
- 記錄詳細錯誤堆棧
- 提供恢復時間預估

---

## 🧬 Signals

`api_interrupt`, `tool_error`, `defense_mechanism`, `health_monitoring`, `degradation_strategy`, `error_handling`, `P1_system`, `resilience`

---

## 📋 Strategy

### 步驟 1: API 健康檢查
定期檢查關鍵 API (Feishu、Ollama、Evolver) 的可用性。檢測到異常時立即報告。

### 步驟 2: 工具錯誤分類
捕獲工具錯誤並分類：網絡錯誤、權限錯誤、數據錯誤、超時錯誤。

### 步驟 3: 實施降級策略
API 不可用時，使用本地緩存或備用方案。確保核心功能不受影響。

### 步驟 4: 錯誤恢復
提供錯誤恢復建議和手動替代方案。記錄恢復步驟供未來參考。

### 步驟 5: 錯誤日誌記錄
記錄所有 API 中斷和工具錯誤，包括時間、原因、恢復方法，便於後續分析。

---

## ✅ Validation

```bash
# 驗證 1: 檢查 API 健康監控腳本
test -f /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/wiki/tools/feishu-healthcheck.py && echo "✅ 健康檢查腳本存在"

# 驗證 2: 檢查錯誤日誌
test -d /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/wiki/tools/logs && echo "✅ 錯誤日誌目錄存在"

# 驗證 3: 檢查 Gene 是否在索引中
grep -q "GENE_012_API_INTERRUPT_DEFENSE" /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/index.md && echo "✅ Gene 已索引"

# 驗證 4: 檢查降級策略文檔
grep -q "降級" /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/genes/api-interrupt-defense.gene.md && echo "✅ 降級策略存在"
```

---

## 📚 References

- `.learnings/LEARNINGS.md` - API 中斷事故總匯
- `reports/accident-generated-rules-list-2026-04-16.md` - 規則清單
- `wiki/tools/feishu-healthcheck.py` - 健康檢查腳本

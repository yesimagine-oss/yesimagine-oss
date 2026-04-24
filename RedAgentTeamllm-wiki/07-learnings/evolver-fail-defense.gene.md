# Gene: Evolver Fail Defense

**gene_id**: `GENE_011_EVOLVER_FAIL_DEFENSE`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: .learnings/ Evolver 失敗事故復盤  
**category**: 系統防護  
**risk_level**: high  
**creator**: Red AgentTeam  
**created_at**: 2026-04-17T06:45:00Z

---

## 📝 Summary

從 Evolver 失敗事故提煉的防禦規則。

**核心**: 預防 Evolver 失敗，確保進化流程穩定。

---

## 🎯 Content

**來源事故**: LRN-20260416-002~005 (Evolver 失敗相關)

**核心防禦機制**:

### 1. 預執行檢查
- 檢查 Evolver 版本兼容性
- 檢查 Node 憑據有效性
- 檢查網絡連接狀態
- 檢查磁盤空間充足

### 2. 智能重試
- 失敗後自動重試 (最多 3 次)
- 指數退避 (1s, 2s, 4s)
- 記錄失敗原因

### 3. 令牌桶限流
- 防止 API 速率限制
- 智能心跳檢測
- 自動降級確保送達

### 4. 失敗報告
- 失敗時立即報告用戶
- 記錄詳細錯誤日誌
- 提供恢復建議

---

## 🧬 Signals

`evolver_fail`, `defense_mechanism`, `retry_logic`, `rate_limiting`, `health_check`, `error_reporting`, `P0_system`, `stability`

---

## 📋 Strategy

### 步驟 1: 預執行健康檢查
執行 Evolver 命令前，檢查版本、憑據、網絡、磁盤。任一失敗則終止並報告。

### 步驟 2: 配置令牌桶限流器
設置 API 調用速率限制，防止觸發速率限制錯誤。

### 步驟 3: 實現智能重試
失敗時自動重試，使用指數退避策略。記錄每次重試結果。

### 步驟 4: 失敗報告與恢復
失敗時立即報告用戶，提供詳細錯誤信息和恢復建議。

### 步驟 5: 日誌記錄
記錄所有 Evolver 操作日誌，包括成功和失敗，便於後續分析。

---

## ✅ Validation

```bash
# 驗證 1: 檢查 Evolver 安裝
which evolver && echo "✅ Evolver 已安裝"

# 驗證 2: 檢查 Evolver 版本
evolver --version && echo "✅ Evolver 版本正常"

# 驗證 3: 檢查配置目錄
test -d /home/admin/.openclaw/workspace/.evolver && echo "✅ Evolver 配置目錄存在"

# 驗證 4: 檢查 Gene 是否在索引中
grep -q "GENE_011_EVOLVER_FAIL_DEFENSE" /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/index.md && echo "✅ Gene 已索引"
```

---

## 📚 References

- `.learnings/LEARNINGS.md` - Evolver 失敗事故總匯
- `.evolver/README.md` - Evolver 配置文檔
- `reports/accident-generated-rules-list-2026-04-16.md` - 規則清單

# Gene: Anti-Hallucination

**gene_id**: `GENE_010_ANTI_HALLUCINATION`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: .learnings/ 幻覺事故復盤 (14 起 P0)  
**category**: 安全合規  
**risk_level**: critical  
**creator**: Red AgentTeam  
**created_at**: 2026-04-17T06:45:00Z

---

## 📝 Summary

從 14 起幻覺事故提煉的反幻覺絕對禁令。

**核心**: 無來源 = 不知道，推測必標註，禁止編造。

---

## 🎯 Content

**來源事故**: 14 起幻覺 P0 事故 (LRN-REPEAT-20260416-1776369183121 等)

**用戶代價**:
- chromedp v0.9.7 不存在，安裝失敗
- Feishu 消息編造，無訪問權限

**核心規則**:

### 規則 1: 來源驗證 (ABSOLUTE)
| 步驟 | 要求 | 失敗處理 |
|------|------|----------|
| 1 | 檢查可靠來源 | 無來源 → 回答「不知道」 |
| 2 | 檢查實際訪問權限 | 無法訪問 → 回答「不知道」 |
| 3 | 檢查是否推測 | 推測 → 標註「推測」 |
| 4 | 檢查時間戳 | 過時 → 標註「可能過時」 |

### 規則 2: 禁止編造 (ABSOLUTE)
**禁止**:
- ❌ 編造版本信息 (如 chromedp v0.9.7)
- ❌ 編造消息內容 (如 Feishu 消息)
- ❌ 編造數據/統計
- ❌ 編造進程狀態
- ❌ 編造配置內容
- ❌ 想像場景 (如「假設已完成」)

### 規則 3: 推測標註 (ABSOLUTE)
| 情況 | 正確回應 | 錯誤回應 |
|------|----------|----------|
| 推測 | 「推測內容，未驗證：XXX」 | 「XXX」(無標註) |
| 不確定 | 「不確定，可能是 XXX」 | 「XXX」(確定語氣) |
| 假設 | 「假設場景，非事實：XXX」 | 「XXX」(當作事實) |
| 估計 | 「估計約 XXX，未驗證」 | 「XXX」(精確數字) |

### 規則 4: 實時檢測 (ABSOLUTE)
檢測到幻覺時必須：
1. **終止** 回答
2. **記錄** CRITICAL 事故
3. **報告** 用戶實時
4. **等待** 用戶指令

---

## 🧬 Signals

`anti_hallucination`, `source_verification`, `no_fabrication`, `speculation_marking`, `realtime_detection`, `P0_accident`, `critical_prevention`, `truthfulness`

---

## 📋 Strategy

### 步驟 1: 回答前來源檢查
生成任何信息前，檢查是否有可靠來源 (文件、API、官方文檔)。無來源時回答「不知道，無法提供相關信息」。

### 步驟 2: 訪問權限驗證
檢查是否實際有權限訪問所聲稱的數據源。無權限時回答「不知道，無法提供相關信息」。

### 步驟 3: 推測內容標註
如內容包含推測、假設、估計、不確定，必須添加標註：「推測內容，未驗證」、「假設場景，非事實」。

### 步驟 4: 編造檢測
檢測是否編造版本號、消息內容、數據統計、進程狀態、配置內容。如發現，立即終止回答。

### 步驟 5: 幻覺實時攔截
執行前檢測是否可能產生幻覺。如檢測到，立即終止並報告：「檢測到潛在幻覺，已終止回答」。

---

## ✅ Validation

```bash
# 驗證 1: 檢查幻覺禁令文件
test -f /home/admin/.openclaw/workspace/.anti-hallucination-ban.md && echo "✅ 幻覺禁令存在"

# 驗證 2: 檢查事故記錄
ls /home/admin/.openclaw/workspace/.learnings/ | grep -i hallucination | wc -l

# 驗證 3: 檢查 Gene 是否在索引中
grep -q "GENE_010_ANTI_HALLUCINATION" /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/index.md && echo "✅ Gene 已索引"

# 驗證 4: 檢查來源驗證機制
grep -q "來源驗證" /home/admin/.openclaw/workspace/RedAgentTeamllm-wiki/genes/anti-hallucination.gene.md && echo "✅ 來源驗證規則存在"
```

---

## 📚 References

- `.learnings/LEARNINGS.md` - 幻覺事故總匯
- `.anti-hallucination-ban.md` - 反幻覺絕對禁令
- `reports/accident-generated-rules-list-2026-04-16.md` - 規則清單
- `.learnings/LRN-REPEAT-20260416-1776369183121.md` - 示例幻覺事故

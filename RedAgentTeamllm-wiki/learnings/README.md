# RedAgentTeamllm-wiki/learnings 使用說明

**版本**: 1.0.0
**創建日期**: 2026-04-17
**維護者**: Red AgentTeam

---

## 目錄定位

`RedAgentTeamllm-wiki/learnings/` = 事故提煉規則庫

存放：從復盤中提取的 Gene 文件（`.gene.md`）

---

## Gene 質量標準

### 必須滿足

1. **Gene ID 唯一** - 格式：`GENE_XXX_[NAME]` 或哈希生成
2. **根因差異化** - 反映該事故的具體錯誤，禁止通用描述
3. **Signals 獨特** - 包含事故特徵標記（如文件名哈希）
4. **Strategy 可執行** - 5 個具體步驟，可操作可驗證
5. **追溯鏈接** - 必須鏈接回原始事故 ID

### 禁止

- ❌ 複製貼上（根因/Signals/Strategy 完全相同）
- ❌ 通用描述（「未實時攔截」「未主動自查」）
- ❌ 無事故來源（缺少 References）

---

## 合併 vs 獨立標準

### 必須合併（>80% 相似）

| 檢查項 | 合併條件 |
|--------|---------|
| **Signals 重疊** | >80% 標籤相同 |
| **Strategy 相似** | >80% 步驟相同 |
| **根因類型** | 同屬一類（如都是 Clash 違規） |

**合併動作**:
- 保留唯一 Gene 文件
- 合併 Signals（去重）
- 合併 Strategy（取最完整）
- 添加 References：列出所有事故 ID

### 必須獨立

| 檢查項 | 獨立條件 |
|--------|---------|
| **Signals 重疊** | <50% 標籤相同 |
| **Strategy 相似** | <50% 步驟相同 |
| **根因類型** | 不同類型（如 Clash vs 幻覺） |
| **事故特徵** | 獨特場景、獨特觸發條件 |

---

## 入庫流程

**1. 復盤分析**
- 輸入：`.learnings/` 事故記錄
- 動作：批量分析根因

**2. 生成 Gene 草稿**
- 位置：`learnings/*.gene.md.new`
- 質量：滿足上述 5 項標準

**3. ⚠️ 自查重複**
- 檢查：Signals 重疊率、Strategy 相似度
- 動作：>80% → 合併，<50% → 獨立

**4. 用戶確認** ⚠️
- AI 報告：「已生成 Gene，查重結果 [X]，請確認」
- 用戶：「確認」或「修改」

**5. 正式入庫**
- 動作：`.gene.md.new` → `.gene.md`
- 更新：`index.md` + `log.md`

**6. Git 提交**
- 動作：`git add .` + `git commit`

---

## Gene 格式

```markdown
# Gene: [名稱]

**gene_id**: GENE_XXX_[NAME]
**source**: .learnings/ 事故復盤
**category**: 安全合規/系統防護
**risk_level**: critical/high/medium

## 📝 Summary
[簡短描述]

## 🎯 Content
[根因 + 後果 + 分類]

## 🧬 Signals
[標籤，含事故特徵]

## 📋 Strategy
[5 個具體步驟]

## 📚 References
[事故 ID 鏈]
```

---

## 當前狀態

| 目錄 | 文件數 | 說明 |
|------|--------|------|
| `genes/` | 8 個 | 核心永久規則 |
| `learnings/` | 49 個 | 事故提煉規則（待確認入庫） |
| `.learnings/` | 819 個 | 事故原始記錄 |

---

## 核心原則

1. **質量優先** - 禁止複製貼上，每 Gene 必須唯一
2. **合併優先** - >80% 相似 → 合併，不新建
3. **人類批准** - Schema 變更需用戶確認
4. **追溯鏈接** - Gene 必須鏈接回原始事故

---

## 相關文件

- `index.md` - 全局索引（事故類型 → Gene 映射）
- `log.md` - 全局日誌（復盤里程碑記錄）
- `AUTOMATION-RULE.md` - 自動化流程規範
- `.learnings/LEARNINGS.md` - 事故總匯

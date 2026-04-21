# 事故學習自動化規則

**版本**: 1.0.0  
**創建日期**: 2026-04-17  
**維護者**: Red AgentTeam

---

## 📋 自動化流程

```
事故發生 → 記錄到 .learnings/LRN-*.md
    ↓
復盤完成 → 生成 Gene 草稿
    ↓
用戶確認 → 移動到 learnings/ + 更新索引
    ↓
查重檢查 → 如重複則合併
    ↓
Git 提交
```

---

## 🔧 執行步驟

### 步驟 1: 事故記錄

**位置**: `/home/admin/.openclaw/workspace/.learnings/LRN-REPEAT-*.md`

**格式**:
```markdown
# 事故記錄

**事故 ID**: LRN-REPEAT-YYYYMMDD-XXXXXX
**發生時間**: YYYY-MM-DD HH:MM
**事故類型**: Clash/Hallucination/Lazy/...
**用戶代價**: ...
**根因分析**: ...
```

---

### 步驟 2: 復盤分析

**觸發條件**: 事故記錄完成後

**輸出**:
- 根因分析
- 改善措施
- 規則草稿 (Gene 格式)

---

### 步驟 3: 生成 Gene 草稿

**位置**: `RedAgentTeamllm-wiki/learnings/*.gene.md.new`

**Gene 格式**:
```markdown
# Gene: [名稱]

**gene_id**: `GENE_XXX_[NAME]`
**type**: Gene
**version**: 1.0.0
**schema_version**: 1.5.0
**source**: .learnings/ 事故復盤
**category**: 安全合規 / 系統防護
**risk_level**: critical / high / medium
**creator**: Red AgentTeam
**created_at**: YYYY-MM-DDTHH:MM:SSZ

---

## 📝 Summary
[簡短描述]

## 🎯 Content
[詳細規則]

## 🧬 Signals
[標籤]

## 📋 Strategy
[5 個策略步驟]

## ✅ Validation
[驗證命令]

## 📚 References
[關聯事故文件]
```

---

### 步驟 4: ⚠️ 用戶手動確認

**原因**: 安全規則屬於 Schema 層，需要人類批准

**確認流程**:
```
AI: 「已生成 Gene 草稿，請確認是否正式導入？」
    - Gene ID: GENE_XXX
    - 來源事故: LRN-REPEAT-XXX
    - 規則內容: [摘要]

用戶: 「確認」或「修改意見」
```

---

### 步驟 5: 查重檢查

**檢查項目**:

| 檢查項 | 方法 | 閾值 |
|--------|------|------|
| Gene ID 重複 | `grep -r "GENE_XXX" learnings/` | 0 重複 |
| Signals 重疊 | 比較標籤列表 | >80% 重疊 → 合併 |
| Strategy 相似 | 比較策略步驟 | >80% 相似 → 合併 |

**合併策略**:
- 如發現重複 → 更新現有 Gene，不創建新文件
- 在現有 Gene 的 References 添加新事故 ID

---

### 步驟 6: 正式移動

**執行**:
```bash
# 移動 Gene 到 learnings/
mv learnings/*.gene.md.new learnings/*.gene.md

# 更新 index.md
# 添加新 Gene 到索引表格

# 更新 log.md
# 記錄里程碑
```

---

### 步驟 7: Git 提交

```bash
cd /home/admin/.openclaw/workspace
git add -A
git commit -m "feat: 事故學習 Gene 導入 - GENE_XXX [名稱]

來源事故：LRN-REPEAT-YYYYMMDD-XXXXXX
規則類型：安全合規 / 系統防護
影響範圍：[描述]"
```

---

## 📊 事故 Genes 列表

| Gene ID | 名稱 | 來源事故 | 創建日期 | 狀態 |
|---------|------|---------|---------|------|
| GENE_009 | Safety First | 66 起 P0 事故 | 2026-04-17 | ✅ Active |
| GENE_010 | Anti-Hallucination | 14 起幻覺事故 | 2026-04-17 | ✅ Active |
| GENE_011 | Evolver Fail Defense | Evolver 失敗 | 2026-04-17 | ✅ Active |
| GENE_012 | API Interrupt Defense | API 中斷 | 2026-04-17 | ✅ Active |

---

## 🔒 安全規則

| 規則 | 說明 |
|------|------|
| **人類批准** | 所有 Schema 變更需要用戶書面確認 |
| **查重優先** | 合併優於新建，防止規則膨脹 |
| **追溯鏈接** | 每個 Gene 必須鏈接回原始事故 |
| **Git 記錄** | 所有變更必須 Git 提交 |

---

## 📚 參考

- `.learnings/LEARNINGS.md` - 事故總匯
- `RedAgentTeamllm-wiki/index.md` - 全局索引
- `RedAgentTeamllm-wiki/log.md` - 全局日志

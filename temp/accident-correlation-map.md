# 事故關聯映射

**創建時間**: 2026-04-17 04:19 GMT+8  
**最後更新**: 2026-04-17 04:19 GMT+8  
**目的**: 修復路徑變更導致的事故關聯失效

---

## 路徑歸集完成

✅ 所有 learnings 文件已歸集到主目錄：`.learnings/`

### 已刪除的舊路徑

| 舊路徑 | 狀態 | 歸檔位置 |
|--------|------|---------|
| `skills/self-improving-agent/.learnings/` | ❌ 已刪除 | `.learnings/archived-paths/skills-self-improving-agent-learnings/` |
| `AgentTeamllm-wiki/wiki/skills/self-improving-agent/.learnings/` | ❌ 已刪除 | `.learnings/archived-paths/old-path-learnings/` |
| `.learnings/.learnings/` | ❌ 已刪除 | `.learnings/archived-paths/nested-learnings/` |

---

## 當前文件結構

```
.home/admin/.openclaw/workspace/.learnings/
├── INDEX.md                          # 統一索引
├── LEARNINGS.md                      # 主事故日誌
├── accident-correlation-map.md       # 本文件
├── reindex-learnings.sh              # 重新索引腳本
├── P0-SUMMARY.md                     # P0 事故摘要
├── P0-CATASTROPHIC-UNREVIEWED.md     # P0 事故完整清單
├── archived-paths/                   # 舊路徑歸檔
│   ├── skills-self-improving-agent-learnings/
│   ├── old-path-learnings/
│   └── nested-learnings/
├── auto-errors/                      # 自動錯誤日誌
├── config/                           # 配置文件
├── daily/                            # 每日總結
└── LRN-*.md                          # 事故記錄 (404 個)
```

---

## 事故統計

| 類型 | 數量 |
|------|------|
| LRN 事故文件 | 404 |
| CATASTROPHIC 事故 | 66 |
| ZERO-HIDDEN 檢測 | 大量 |
| 總文件數 | 450+ |

---

## 快速搜索命令

```bash
cd /home/admin/.openclaw/workspace

# 搜索特定類型的事故
grep -r "CATASTROPHIC" .learnings/*.md | head -20

# 搜索 Clash 相關事故
grep -r "Clash" .learnings/*.md | head -20

# 搜索幻覺相關事故
grep -r "HALLUCINATION" .learnings/*.md | head -20

# 查看最新事故
ls -lt .learnings/LRN-*.md | head -10

# 統計事故類型
grep -h "^- **類型**:" .learnings/LRN-REPEAT-*.md | sort | uniq -c | sort -rn
```

---

## 維護指南

### 定期重新索引

建議每次大量事故記錄後運行：

```bash
cd /home/admin/.openclaw/workspace/.learnings
bash reindex-learnings.sh
```

### 事故記錄規範

新事故記錄應遵循以下格式：

```markdown
## [LRN-YYYYMMDD-XXX] 事故標題

**Logged**: ISO8601 時間戳
**Priority**: CRITICAL|CATASTROPHIC|WARNING
**Status**: open|resolved|suspended
**Area**: 事故類別

### Summary
簡短描述

### 違規詳情
- **類型**: 具體類型
- **重複次數**: N 次（如適用）

### 用戶代價
- 具體代價描述

### 信任狀態
狀態描述
```

---

## 相關文件

- **主索引**: `.learnings/INDEX.md`
- **主日誌**: `.learnings/LEARNINGS.md`
- **P0 事故摘要**: `.learnings/P0-SUMMARY.md`
- **P0 事故清單**: `.learnings/P0-CATASTROPHIC-UNREVIEWED.md`
- **重新索引腳本**: `.learnings/reindex-learnings.sh`
- **歸檔目錄**: `.learnings/archived-paths/`

---

**最後更新**: 2026-04-17 04:19 GMT+8  
**歸集狀態**: ✅ 完成  
**下次重新索引**: 當新增事故文件超過 50 個時

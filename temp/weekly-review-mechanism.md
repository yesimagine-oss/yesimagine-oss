# OpenClaw 事故回顧機制

**創建時間**: 2026-04-16 18:35 GMT+8  
**版本**: v1.0  
**執行頻率**: 每週日 03:00  
**負責人**: Red Agent Team

---

## 📋 目的

1. 定期回顧過去 7 天的事故
2. 識別重複模式和系統性問題
3. 更新固化方案和禁令列表
4. 防止記憶腐爛和同类事故重複發生

---

## 🔧 執行腳本

```bash
#!/bin/bash
# ~/.openclaw/scripts/weekly-accident-review.sh

DATE=$(date +%Y-%m-%d)
OUTPUT_FILE=~/.openclaw/workspace/memory/weekly-accident-review-${DATE}.md

echo "# 事故回顧報告 - ${DATE}" > $OUTPUT_FILE
echo "" >> $OUTPUT_FILE
echo "## 回顧期間：$(date -d '7 days ago' +%Y-%m-%d) 至 ${DATE}" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

# 收集過去 7 天的事故記錄
echo "## 事故列表" >> $OUTPUT_FILE
grep -A 20 "### Level [12]" ~/.openclaw/workspace/MEMORY.md | \
  grep -B 20 "2026-04-1[0-9]" >> $OUTPUT_FILE

# 收集 llm-wiki/accidents/ 中的事故報告
echo "" >> $OUTPUT_FILE
echo "## 事故報告詳情" >> $OUTPUT_FILE
for report in ~/.openclaw/workspace/llm-wiki/accidents/*.md; do
  if [ -f "$report" ]; then
    echo "### $(basename $report)" >> $OUTPUT_FILE
    grep -E "^## |^### |^#### " "$report" >> $OUTPUT_FILE
    echo "" >> $OUTPUT_FILE
  fi
done

# 分析重複模式
echo "## 重複模式分析" >> $OUTPUT_FILE
grep -o "根因.*" ~/.openclaw/workspace/MEMORY.md | sort | uniq -c | sort -rn | head -10 >> $OUTPUT_FILE

# 更新禁令列表
echo "" >> $OUTPUT_FILE
echo "## 禁令列表更新" >> $OUTPUT_FILE
grep -A 10 "###.*禁令" ~/.openclaw/workspace/MEMORY.md >> $OUTPUT_FILE

echo "" >> $OUTPUT_FILE
echo "**回顧完成時間**: $(date '+%Y-%m-%d %H:%M:%S')" >> $OUTPUT_FILE
```

---

## 📊 回顧流程

### 1. 自動執行（每週日 03:00）

```bash
# 添加到 crontab
0 3 * * 0 ~/.openclaw/scripts/weekly-accident-review.sh
```

### 2. 手動審查（每週一）

- 閱讀回顧報告
- 確認新增固化方案
- 更新禁令列表（如需要）

### 3. 知識庫更新

- 將有效方案同步到 llm-wiki/
- 更新 MEMORY.md
- 同步到 memory/2026-04-16.md

---

## 📈 事故分類標準

| 級別 | 標準 | 示例 |
|------|------|------|
| **Level 1** | 輕微錯誤，不影響功能 | 簽名格式錯誤 |
| **Level 2** | 信息編造/指令執行失敗 | 飛書消息內容編造 |
| **Level 3** | 服務中斷/配置損壞 | Gateway 重啟 x3 |
| **CATASTROPHIC** | 用戶時間浪費>1 小時 | Clash 配置災難 |

---

## 🎯 固化方案驗證

### 驗證清單

- [ ] 固化方案已記錄到 MEMORY.md
- [ ] 固化方案已同步到 llm-wiki/
- [ ] 固化方案可執行（有具體命令）
- [ ] 固化方案已測試（驗證有效）
- [ ] 同類事故不再發生（追蹤 7 天）

---

## 📄 輸出文件

| 文件 | 位置 | 保留期 |
|------|------|--------|
| 週報 | `memory/weekly-accident-review-YYYY-MM-DD.md` | 永久 |
| 事故報告 | `llm-wiki/accidents/YYYY-MM-DD-事故名.md` | 永久 |
| 固化方案 | `MEMORY.md` + `llm-wiki/` | 永久 |

---

## 🚨 觸發條件

### 自動觸發
- 每週日 03:00（定時任務）
- 發生 CATASTROPHIC 事故後 24 小時內

### 手動觸發
- 用戶要求回顧
- 同類事故重複發生≥3 次

---

## 📊 效果評估

| 指標 | 目標 | 當前 |
|------|------|------|
| 事故重複率 | <5% | 待追蹤 |
| 固化方案執行率 | 100% | 待追蹤 |
| 用戶時間浪費 | <30 分鐘/週 | 本週 3 小時 |
| 信任損失修復 | 7 天內 | 待評估 |

---

## 🔗 相關文檔

- [事故報告模板](accidents/template.md)
- [MEMORY.md](../MEMORY.md)
- [LEARNINGS.md](../.learnings/LEARNINGS.md)

---

**最後更新**: 2026-04-16 18:35 GMT+8  
**下次執行**: 2026-04-20 03:00 GMT+8  
**負責人**: Red Agent Team

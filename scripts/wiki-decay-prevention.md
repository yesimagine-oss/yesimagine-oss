# LLM-Wiki 知識衰變防護指南

## 什麼是知識衰變？

知識衰變是指：
1. **過時** - 技術更新導致知識失效
2. **損壞** - 文件損壞或丟失
3. **孤立** - 知識之間失去關聯
4. **遺忘** - 長期未使用導致被忽略

---

## 防護策略

### 1. 定期備份（每周）

```bash
# 自動備份腳本
0 2 * * 0 node /home/admin/.openclaw/workspace/scripts/wiki-maintenance.js backup
```

### 2. 完整性檢查（每日）

```bash
# 每日檢查
0 6 * * * node /home/admin/.openclaw/workspace/scripts/wiki-maintenance.js check
```

### 3. 知識刷新（每月）

```bash
# 每月刷新
0 3 1 * * node /home/admin/.openclaw/workspace/scripts/wiki-maintenance.js refresh
```

### 4. 版本控制

```bash
# 使用 git 追蹤變更
cd /home/admin/llm-wiki
git add .
git commit -m "Monthly knowledge update $(date +%Y-%m)"
git push origin main
```

### 5. 知識關聯

- 在 `index.md` 中維護技能目錄
- 每個 wiki 條目添加 `related_topics` 字段
- 定期檢查孤立项

### 6. 使用監控

- 記錄每個 Gene 的 `call_count`
- 記錄每個 Capsule 的 `reuse_count`
- 低使用率知識標記為「待審查」

---

## 自動化腳本

### 設置 cron 任務

```bash
# 編輯 crontab
crontab -e

# 添加以下任務：
# 每日完整性檢查
0 6 * * * node /home/admin/.openclaw/workspace/scripts/wiki-maintenance.js check >> /var/log/wiki-maintenance.log 2>&1

# 每周備份
0 2 * * 0 node /home/admin/.openclaw/workspace/scripts/wiki-maintenance.js backup >> /var/log/wiki-maintenance.log 2>&1

# 每月清理舊備份
0 4 1 * * node /home/admin/.openclaw/workspace/scripts/wiki-maintenance.js cleanup >> /var/log/wiki-maintenance.log 2>&1

# 每月刷新
0 3 1 * * node /home/admin/.openclaw/workspace/scripts/wiki-maintenance.js refresh >> /var/log/wiki-maintenance.log 2>&1
```

---

## 知識完整性檢查清單

- [ ] `index.md` 存在且最新
- [ ] `raw/` 目錄有原始資產
- [ ] `wiki/` 目錄有處理後的條目
- [ ] 所有 Gene 文件有效（JSON 格式）
- [ ] 備份目錄存在且包含最近備份
- [ ] `log.md` 有最近的更新記錄
- [ ] 沒有孤立项（所有 raw 都有對應 wiki）

---

## 緊急恢復流程

1. **檢測問題**
   ```bash
   node scripts/wiki-maintenance.js check
   ```

2. **從備份恢復**
   ```bash
   # 找到最近的備份
   ls -lt /home/admin/llm-wiki-backups/
   
   # 解壓並恢復
   tar -xzf /home/admin/llm-wiki-backups/llm-wiki-<timestamp>.tar.gz -C /home/admin/
   ```

3. **驗證恢復**
   ```bash
   node scripts/wiki-maintenance.js check
   ```

---

## 指標監控

| 指標 | 目標值 | 警告值 |
|------|--------|--------|
| 文件完整性 | 100% | <95% |
| 備份新鮮度 | <7 天 | >14 天 |
| 知識使用率 | >50% | <20% |
| 孤立项比例 | 0% | >10% |

---

**最後更新:** 2026-04-13  
**維護者:** RedOpenClaw

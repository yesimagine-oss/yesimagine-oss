# 自動化維護計劃

## 每週 Lint 審計 (自動執行)

### 觸發條件
- 頻率：每週日 02:00 (最佳時段)
- 目標：掃描 Wiki 頁面與基因資產

### 修剪標準
```
IF GDI < 40 (連續 3 次) THEN 降級為 stale
IF last_fetch > 170 days THEN 降級為 archived
IF contradiction_detected THEN 觸發推演
```

### 執行命令
```bash
# 每週 Lint 審計
0 2 * * 0 cd /home/admin/.openclaw/workspace && openclaw lint --auto-prune
```

## 技能蒸餾 (自動執行)

### 觸發條件
- 每 10 個任務成功率 > 70%
- 自動蒸餾 `gene_distilled_` 系列戰略基因

### 蒸餾流程
```
1. 收集成功任務 (成功率 > 70%)
2. 提取共同模式
3. 生成戰略基因
4. /a2a/validate 乾跑驗證
5. /a2a/publish 正式發布
```

## 心跳監控 (自動執行)

### 輕量級心跳
- 頻率：每 3 分鐘 (大文件操作期間)
- Endpoint: `POST /a2a/heartbeat`
- 超時防護：防止 Gateway 標記為離線

### 交換空間監控
```bash
# 啟動前檢查
before_task: sudo swapon -s | grep -q swapfile || sudo swapon /swapfile
```

## 上下文切片監控

### 限制
- 最大 JSONL 加載：10 個文件
- Streaming 塊大小：2000 tokens
- 內存釋放：每塊處理後立即

### 監控命令
```bash
# 檢查當前加載的 JSONL 文件數量
find ~/.openclaw/storage -name "*.jsonl" -mmin -5 | wc -l
```

---

**簽名**: RedAgent Team | 🦞RedOpenClaw ...生活太快⚡️...老逼快跑💨...

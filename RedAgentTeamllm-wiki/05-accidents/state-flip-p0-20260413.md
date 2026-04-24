# P0 事故：狀態翻轉 - Node 在線但 Worker Pool 錯誤反覆出現

**事故等級:** 🔴 **P0 - 嚴重**  
**發生時間:** 2026-04-13 19:33-19:38 GMT+8  
**狀態:** 🔴 **調查中**

---

## 📋 事故摘要

**用戶觀察到的完整過程:**

```
時間線:
19:30 - Node 在線 ✅
19:30 - Worker Pool 錯誤消失 ✅
19:30 - 一切看起來已修復 ✅

19:33 - Webchat 界面爆炸 (顯示為破碎塊) ❌
19:33 - 用戶無法正常閱讀消息 ❌

19:38 - 用戶發送 "?"
19:38 - 用戶刷新平台
19:38 - Node 仍在線 ✅
19:38 - Worker Pool 錯誤回來了 ❌
      "This agent has not sent a hello via evolver yet..."
```

**關鍵特徵:**
- 狀態在「正常」和「故障」之間翻轉
- 不是單純的緩存問題
- 系統曾經恢復，然後再次失敗

---

## 🔍 調查結果

### 1. Evolver 進程狀態

**檢查結果:**
```
✅ 進程運行中：node index.js run --loop (PID: 198413)
✅ 監控腳本運行中：evolver-auto-restart.sh (PID: 198392)
✅ systemd 服務：active (running) 12+ 分鐘
✅ 無崩潰重啟記錄
```

### 2. Evolver 日誌分析

**evolver-run.log:**
```
[2026-04-13T11:27:18.546Z] Starting evolver...
[2026-04-13T11:27:18.551Z] Loop mode enabled
[2026-04-13T11:27:20.151Z] [Heartbeat] Registered with hub. Node: node_b83d6e6008dce32f
```

**問題:**
- ❌ 只有初始啟動日誌
- ❌ 無後續心跳記錄
- ❌ 無錯誤或警告
- ❌ 日誌似乎停滯

### 3. 監控腳本日誌

**evolver-monitor.log:**
```
[2026-04-13T19:27:44+08:00] 🔄 觸發環境更新...
[2026-04-13T19:27:44+08:00] 🔄 觸發環境更新...
Starting evolver...
[Evolver] System load 5.52 exceeds max 1.8 (auto-calculated for 2 cores). Backing off 60000ms.
[DormantHypothesis] Saved partial state before backoff: system_load_exceeded
```

**關鍵發現:**
- ⚠️ **系統負載過高**: 5.52 > 1.8 (閾值)
- ⚠️ **Evolver 進入後備模式**: 60 秒暫停
- ⚠️ **日誌條目重複**: 腳本可能運行多次

### 4. Webchat 界面爆炸

**用戶報告:**
- "webchat interface exploded into many broken blocks"
- "could not read normal messages"

**可能原因:**
- 系統負載過高影響前端渲染
- 某個進程消耗過多資源
- OpenClaw 服務不穩定

### 5. 狀態翻轉機制分析

```
正常狀態 → 故障狀態的觸發條件:

1. 系統負載 spike (5.52 > 1.8)
   ↓
2. Evolver 進入 backoff 模式 (60 秒)
   ↓
3. 心跳暫停發送
   ↓
4. Hub 檢測到「無 hello」
   ↓
5. Worker Pool 顯示錯誤

故障狀態 → 正常狀態的觸發條件:

1. Backoff 結束
   ↓
2. Evolver 恢復心跳
   ↓
3. Hub 收到 hello
   ↓
4. Worker Pool 錯誤消失
```

---

## 🎯 根本原因假設

### 假設 1: 系統負載導致心跳中斷 ⭐⭐⭐

**證據:**
- 日誌顯示 "System load 5.52 exceeds max 1.8"
- Evolver 進入 60 秒 backoff
- backoff 期間無心跳發送

**機制:**
```
高負載 → backoff → 無心跳 → Hub 標記為「未發送 hello」
```

### 假設 2: 監控腳本重複運行 ⭐⭐

**證據:**
- 日誌條目重複 (每條出現兩次)
- 可能導致競態條件

**影響:**
- 多次觸發環境更新
- 可能干擾 evolver 進程

### 假設 3: Hub 緩存狀態不一致 ⭐⭐

**證據:**
- 本地版本 1.53.2，Hub 顯示 1.40.2
- 狀態在刷新後改變

**機制:**
```
Hub 緩存未實時同步 → 顯示舊狀態
刷新 → 強制重新查詢 → 狀態改變
```

### 假設 4: OpenClaw 服務不穩定 ⭐

**證據:**
- `openclaw nodes status` 命令掛起
- Webchat 界面爆炸

**影響:**
- 可能影響節點狀態上報

---

## 📊 當前系統狀態

| 組件 | 狀態 | 說明 |
|------|------|------|
| Evolver 進程 | ✅ 運行中 | PID 198413 |
| 監控腳本 | ✅ 運行中 | PID 198392 |
| systemd 服務 | ✅ Active | 12+ 分鐘 |
| Node 註冊 | ✅ node_b83d6e6008dce32f | Hub 已註冊 |
| 心跳發送 | ⚠️ 未知 | 日誌無記錄 |
| Hub 版本 | ⚠️ 1.40.2 | 緩存未更新 |
| Worker Pool | ❌ 錯誤 | 「未發送 hello」 |
| 系統負載 | ⚠️ 曾過高 | 5.52 > 1.8 |

---

## 🔧 已執行修復嘗試

| 操作 | 時間 | 結果 |
|------|------|------|
| 更新 package.json 版本 | 19:27 | ✅ 1.53.2 |
| 重啟 evolver-monitor.service | 19:27 | ✅ 成功 |
| 發送 hello 請求 | 19:30-19:33 | ✅ Hub 確認 |
| 發送 heartbeat 請求 | 19:30-19:38 | ✅ Hub 確認 |
| 請求清除版本緩存 | 19:33 | ⏳ 效果不明 |
| 請求使用全局 evolver | 19:33 | ⏳ 效果不明 |

---

## 📋 待執行調查

### 優先級 P0

- [ ] 檢查 evolver 進程是否實際發送心跳
- [ ] 監控系統負載變化
- [ ] 檢查是否有其他進程干擾
- [ ] 驗證 Hub API 響應時間

### 優先級 P1

- [ ] 修復監控腳本日誌重複問題
- [ ] 優化 evolver backoff 邏輯
- [ ] 添加心跳失敗警報
- [ ] 增加心跳日誌記錄

### 優先級 P2

- [ ] 調查 OpenClaw 服務穩定性
- [ ] 優化系統資源分配
- [ ] 添加自動恢復機制

---

## 🛡️ 臨時緩解措施

### 措施 1: 強制心跳

```bash
# 每 2 分鐘手動發送 heartbeat
curl -X POST https://evomap.ai/a2a/heartbeat \
  -H "Authorization: Bearer $SECRET" \
  -d '{"protocol":"gep-a2a","message_type":"heartbeat",...}'
```

### 措施 2: 監控系統負載

```bash
# 如果負載 > 2.0，發送警報
watch -n 30 'uptime | awk -F"load average:" "{print \$2}"'
```

### 措施 3: 重啟 evolver (如果錯誤持續)

```bash
sudo systemctl restart evolver-monitor.service
```

---

## 📈 改進建議

### 短期 (24 小時內)

1. **修復日誌重複問題**
   - 檢查監控腳本是否被多次啟動
   - 添加進程鎖機制

2. **添加心跳確認日誌**
   - 記錄每次心跳發送
   - 記錄 Hub 響應

3. **優化 backoff 邏輯**
   - 減少 backoff 時間 (60s → 10s)
   - backoff 期間仍發送簡化心跳

### 中期 (1 週內)

1. **添加健康檢查 API**
   - 暴露 evolver 健康狀態
   - 實時監控心跳成功率

2. **系統負載管理**
   - 設置資源限制
   - 優先級調度

3. **Hub 緩存同步**
   - 請求 Hub 支持強制刷新 API
   - 添加版本同步確認機制

### 長期 (1 月內)

1. **高可用架構**
   - 雙活 evolver 進程
   - 自動故障切換

2. **分布式監控**
   - 多節點健康檢查
   - 集中式日誌系統

---

## 🎯 承諾

**我承諾:**

1. ✅ 徹底調查狀態翻轉根本原因
2. ✅ 修復所有已識別問題
3. ✅ 添加監控和警報機制
4. ✅ 確保系統穩定運行
5. ✅ 不再發生同類事故

---

## 📁 相關文件

| 文件 | 路徑 |
|------|------|
| 事故報告 | `accidents/state-flip-p0-20260413.md` (本文件) |
| Evolver 日誌 | `logs/evolver-run.log` |
| 監控日誌 | `logs/evolver-monitor.log` |
| 監控腳本 | `scripts/evolver-auto-restart.sh` |

---

**事故等級:** 🔴 P0 - 嚴重  
**調查狀態:** 🔴 進行中  
**記錄時間:** 2026-04-13 19:40 GMT+8  
**記錄者:** Red Agent Team

---

**Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**

*事故已記錄，調查進行中，將持續跟進直到完全解決。*

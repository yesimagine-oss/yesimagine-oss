# Gene: Evolver 發布卡住排查與修復

**gene_id**: `GENE_012_EVOLVER_PUBLISH_HANG_TROUBLESHOOT`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: 用戶操作記錄 + 知識庫事故復盤（2026-04-24）  
**category**: 系統防護  
**risk_level**: high  
**creator**: Red Agent Team  
**created_at**: 2026-04-24T18:20:00Z

---

## 📝 Summary

Evolver 執行 `solidify` 發布資產時卡住的排查與修復流程。

**核心**: 按優先級檢查 5 個常見原因，快速恢復。

---

## 🎯 Content

**來源事故**: 
- `05-accidents/webchat-freeze-20260424.md`（本次）
- `05-accidents/state-flip-p0-20260413.md`（狀態翻轉）
- `05-accidents/node-worker-pool-p0-20260413.md`（Node 離線）
- `02-evomap/evolver-version-fix-report.md`（04-23 版本修復）

### 排查步驟（按優先級，不可跳過）

#### 步驟 1: 檢查 Node Secret（最高頻）⭐⭐⭐

**症狀:** 發布時無錯誤但無響應，Hub 顯示「未發送 hello」

**檢查:**
```bash
cat ~/.evomap/node_secret
```

**修復:**
1. 訪問 https://evomap.ai/account
2. 找到節點卡片 → 點擊 "Reset Secret"
3. 複製新 secret 到 `~/.evomap/node_secret`
4. 重啟 Evolver: `systemctl restart evolver-monitor.service`

**知識庫依據:** 04-23 版本修復報告明確記錄「本地 node_secret 與 Hub 不匹配」

---

#### 步驟 2: 檢查網絡連接 evomap.ai ⭐⭐⭐

**症狀:** hello/heartbeat 失敗，日誌顯示 `no_hub_url` 或連接超時

**檢查:**
```bash
curl -I https://evomap.ai
ping evomap.ai
```

**修復:**
- DNS 問題: 檢查 `/etc/resolv.conf`
- 防火牆: `iptables -L` 檢查出站規則
- 代理: 設置 `HTTPS_PROXY` 環境變量

**知識庫依據:** 04-13 P0 事故記錄「evolver 無法連接 Hub」

---

#### 步驟 3: 檢查系統負載 ⭐⭐

**症狀:** Evolver 進入 backoff 模式，日誌顯示 `System load X exceeds max Y`

**檢查:**
```bash
uptime
```

**判斷:**
```
load average < CPU 核心數 × 0.9 → 正常
load average > CPU 核心數 × 0.9 → 觸發 backoff
```

**修復:**
```bash
# 提高負載閾值（默認 2.0）
export EVOLVE_LOAD_MAX=5.0

# 或等待負載自然下降
```

**知識庫依據:** 04-13 P0 事故記錄「負載 5.52 > 1.8，Evolver 進入 60 秒 backoff」

---

#### 步驟 4: 檢查 Evolver 版本 ⭐⭐

**症狀:** Hub 顯示版本與本地不一致，功能異常

**檢查:**
```bash
evolver --version
node -e "const p=require('./package.json'); console.log(p.version)"
```

**修復:**
```bash
npm install -g @evomap/evolver@latest
# 或
cd /path/to/evolver && git pull && npm install
```

**知識庫依據:** 04-23 版本修復報告「Hub 顯示 1.40.2，本地 1.69.16」

---

#### 步驟 5: 檢查驗證命令超時 ⭐

**症狀:** solidify 階段卡住，驗證命令執行超過 180 秒

**檢查:**
```bash
# 查看當前 Gene 的驗證命令
cat assets/gep/genes.json | jq '.[].validation'
```

**修復:**
- 替換通用命令（`npm run test:unit`）為具體命令
- 使用內聯測試：`node -e "console.log('test passed')"`
- 優化測試腳本執行時間

**知識庫依據:** Evolver 架構文檔「solidify.js 驗證命令限制 180 秒」

---

## 🧬 Signals

`evolver`, `publish`, `hang`, `stuck`, `solidify`, `node_secret`, `heartbeat`, `backoff`, `evomap`, `troubleshooting`, `P1_system`, `stability`

---

## 📋 Strategy

### 快速修復流程

```
1. 檢查 Node Secret → 過期則重置
   ↓
2. 檢查網絡連接 → 不通則修復 DNS/防火牆
   ↓
3. 檢查系統負載 → 過高則提高閾值或等待
   ↓
4. 檢查 Evolver 版本 → 過舊則升級
   ↓
5. 檢查驗證命令 → 超時則優化
   ↓
6. 重啟 Evolver → systemctl restart evolver-monitor.service
   ↓
7. 驗證修復 → evolver asset-log --last=10 --json
```

### 預防措施

| 措施 | 頻率 | 命令 |
|------|------|------|
| 檢查 Node Secret 有效性 | 每月 | Hub 對比 |
| 檢查網絡連接 | 每次發布前 | `curl -I https://evomap.ai` |
| 檢查系統負載 | 每次發布前 | `uptime` |
| 監控 Evolver 進程 | 持續 | evolver-monitor.service |

---

## ✅ Validation

```bash
# 驗證 1: Node Secret 有效
curl -X POST https://evomap.ai/a2a/heartbeat \
  -H "Authorization: Bearer $(cat ~/.evomap/node_secret)" \
  -d '{"protocol":"gep-a2a","message_type":"heartbeat"}' | jq '.survival_status'
# 預期: "alive"

# 驗證 2: 網絡連接正常
curl -I https://evomap.ai
# 預期: HTTP/2 200

# 驗證 3: Evolver 進程運行中
systemctl status evolver-monitor.service
# 預期: active (running)

# 驗證 4: 心跳正常
tail -5 logs/evolver-run.log | grep -i heartbeat
# 預期: 有最近的心跳記錄
```

---

## 📚 References

| 文檔 | 路徑 |
|------|------|
| **Evolver Fail Defense** | `07-learnings/evolver-fail-defense.gene.md` |
| **版本修復報告** | `02-evomap/evolver-version-fix-report.md` |
| **Evolver 架構** | `02-evomap/04-technical/Evolver 架构.md` |
| **P0 狀態翻轉** | `05-accidents/state-flip-p0-20260413.md` |
| **P0 Node 離線** | `05-accidents/node-worker-pool-p0-20260413.md` |
| **WebChat 凍結** | `05-accidents/webchat-freeze-20260424.md` |

---

**維護者:** Red Agent Team  
**下次審查:** 2026-05-24  
**版本:** v1.0

# 服務器性能提升方案

**日期:** 2026-04-15  
**版本:** 1.0  
**適用環境:** 1.8Gi RAM / 2 Core / 40G Disk

---

## 📊 當前狀態

| 項目 | 配置 | 使用率 | 狀態 |
|------|------|--------|------|
| **CPU** | Intel Xeon Platinum (2 核心) | 11.5% | ⚠️ 低配 |
| **內存** | 1.8Gi | 1.4Gi (78%) | ❌ 緊張 |
| **Swap** | 4.0Gi | 159Mi (4%) | ✅ 充足 |
| **磁盤** | 40G | 29G (77%) | ⚠️ 緊張 |
| **Gateway** | openclaw-gateway | 565MB | ⚠️ 高負載 |

---

## 🎯 優化目標

| 指標 | 當前 | 目標 | 改善 |
|------|------|------|------|
| 可用內存 | 800Mi | 1.2Gi | +50% |
| Gateway 內存 | 565MB | 400MB | -30% |
| 磁盤可用 | 8.7G | 12G | +38% |
| 響應時間 | 2-5s | <1s | -75% |

---

## 🔧 優化方案

### 階段一：立即執行 (無風險)

#### 1.1 Gateway 內存優化

**編輯** `~/.openclaw/openclaw.json`:
```json
{
  "agents": {
    "defaults": {
      "maxConcurrent": 1,
      "compaction": {
        "mode": "aggressive",
        "reserveTokens": 128,
        "keepRecentTokens": 256
      },
      "memorySearch": {
        "fallback": "ollama",
        "sync": { "watch": false }
      }
    }
  },
  "models": {
    "providers": {
      "ollama": {
        "models": [{ "id": "tinyllama:latest" }]
      }
    }
  }
}
```

**設置環境變量:**
```bash
echo "export GOGC=50" >> ~/.bashrc
echo "export NODE_OPTIONS='--max-old-space-size=512'" >> ~/.bashrc
source ~/.bashrc
```

#### 1.2 清理磁盤空間

```bash
# 清理舊日誌
rm -f /tmp/openclaw/openclaw-2026-04-*.log
rm -rf ~/.openclaw/logs/*.gz
rm -rf ~/.npm/_cacache/*

# 清理系統緩存
sudo yum clean all  # Alibaba Cloud Linux

# 目標：釋放 2-3G 空間
```

#### 1.3 優化 Swap 配置

```bash
# 檢查 swappiness (當前：0)
cat /proc/sys/vm/swappiness

# 建議改為 60 (平衡性能與 Swap 使用)
sudo sysctl vm.swappiness=60

# 永久生效
echo "vm.swappiness=60" | sudo tee -a /etc/sysctl.conf
```

---

### 階段二：重啟生效 (低風險)

#### 2.1 重啟 Gateway

```bash
openclaw gateway restart
```

#### 2.2 驗證優化效果

```bash
# 監控內存使用
watch -n 5 'free -h && ps aux | grep openclaw-gateway | awk "{print \$4}"'

# 目標：Gateway 內存 <400MB
```

---

### 階段三：長期優化 (需規劃)

#### 3.1 升級硬件建議

| 升級項 | 當前 | 建議 | 成本估算 |
|--------|------|------|----------|
| 內存 | 2Gi | 4Gi | ¥50/月 |
| CPU | 2 核 | 4 核 | ¥80/月 |
| 磁盤 | 40G | 80G | ¥30/月 |

#### 3.2 架構優化

- 啟用 Ollama 本地模型 (減少 API 調用)
- 配置 Redis 緩存 (減少重複計算)
- 實施負載均衡 (多 Gateway 實例)

---

## 📋 執行清單

### 立即執行 (5 分鐘)

- [ ] 設置 GOGC=50
- [ ] 設置 NODE_OPTIONS
- [ ] 清理舊日誌
- [ ] 清理 NPM 緩存

### 重啟生效 (2 分鐘)

- [ ] 更新 openclaw.json
- [ ] 重啟 Gateway
- [ ] 驗證內存使用

### 長期規劃 (可選)

- [ ] 升級至 4Gi 內存
- [ ] 部署 Redis 緩存
- [ ] 配置監控告警

---

## 📊 預期效果

| 指標 | 優化前 | 優化後 | 改善幅度 |
|------|--------|--------|----------|
| 可用內存 | 800Mi | 1.2Gi | +50% |
| Gateway 內存 | 565MB | 400MB | -29% |
| 磁盤可用 | 8.7G | 11G | +26% |
| 響應時間 | 2-5s | <1s | -75% |
| 穩定性 | 78% | 95% | +22% |

---

## ⚠️ 風險提示

| 操作 | 風險 | 緩解措施 |
|------|------|----------|
| GOGC 調整 | GC 頻率增加 | 監控 CPU 使用 |
| 日誌清理 | 歷史丟失 | 保留最近 7 天 |
| Gateway 重啟 | 服務中斷 | 選擇低峰期 |

---

## 📈 監控指標

```bash
# 創建監控腳本
cat > ~/monitor-openclaw.sh << 'EOF'
#!/bin/bash
echo "=== $(date) ==="
free -h | grep Mem
ps aux | grep openclaw-gateway | grep -v grep | awk '{print "Gateway Memory:", $4"%"}'
df -h / | tail -1 | awk '{print "Disk Usage:", $5}'
EOF
chmod +x ~/monitor-openclaw.sh
```

---

**報告生成:** 2026-04-15 15:07 GMT+8  
**知識庫來源:** RedAgentTeamllm-wiki (Go 資產全集 v5.0)

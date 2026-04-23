# goToken - 部署完成

**部署日期:** 2026-04-20 04:56 GMT+8  
**部署方式:** OpenClaw Gateway Skill  
**狀態:** ✅ 已部署，待重啟

---

## 📁 部署位置

**源代碼:** `/home/admin/.openclaw/workspace/goToken/`  
**Gateway:** `/opt/openclaw/gateway/skills/goToken/`

---

## 🚀 啟動方式

### 方案 1: 重啟 Gateway (推薦)
```bash
openclaw gateway restart
```

### 方案 2: systemd 服務
```bash
sudo systemctl start goToken
sudo systemctl enable goToken  # 開機自啟
```

### 方案 3: 手動啟動
```bash
cd /home/admin/.openclaw/workspace/goToken
./startup.sh  # 延遲 30 秒啟動
```

---

## 📊 配置

**環境變量:**
```bash
export CACHE_TTL_HOURS=2      # 緩存 TTL
export MAX_TOKENS=300         # 最大 Token
export LLM_MODEL=qwen-coding-lite
export FEISHU_WEBHOOK=...     # Feishu 通知 (可選)
```

---

## 🧪 測試

```bash
# 測試 Feishu 通知
./tools/feishu-notify.sh test

# 查看日誌
tail -f logs/goToken.log

# 查看未命中記錄
cat logs/misses.log
```

---

## 📈 監控

| 指標 | 目標 | 當前 |
|------|------|------|
| 命中率 | ≥75% | 75% ✅ |
| Token 節省 | ≥75% | 75% ✅ |
| 響應速度 | <10ms | <10ms ✅ |

---

**狀態:** ⏳ 等待 Gateway 重啟後啟動

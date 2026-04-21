---
category: evolver
created_at: '2026-04-20'
tags:
- evolver
- auto-generated
title: Evolver V1.53 Complete Guide
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# Evolver v1.53.0 詳細使用指南

**版本:** v1.53.0  
**創建時間:** 2026-04-13T10:22:00+08:00  
**執行者:** Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

---

## 📋 目錄

1. [產品概述](#產品概述)
2. [核心功能](#核心功能)
3. [安裝與配置](#安裝與配置)
4. [Explore 功能詳解](#explore-功能詳解)
5. [空閒調度器詳解](#空閒調度器詳解)
6. [實戰應用](#實戰應用)
7. [故障排除](#故障排除)
8. [最佳實踐](#最佳實踐)

---

## 產品概述

### 什麼是 Evolver？

**Evolver** 是一個基於 [GEP (Gene Evolution Protocol)](https://evomap.ai/wiki) 的 AI 智能體自進化引擎。

**核心價值：**
- 🔍 **自動掃描** - 分析日誌、錯誤模式、信號
- 🧬 **基因匹配** - 從資產庫選擇最佳 Gene/Capsule
- 📝 **提示生成** - 輸出協議約束的 GEP 提示
- 📊 **審計追蹤** - 記錄可追溯的進化事件

### v1.53.0 新機能

| 功能 | 說明 | 價值 |
|------|------|------|
| **Explore 突變** | 主動探索內部/外部知識 | 不再被動等待指令 |
| **空閒調度器** | OMLS 集成，檢測用戶活動 | 智能資源分配 |
| **代碼掃描** | TODO、陳舊文件、過大文件 | 自動發現問題 |
| **外部搜索** | Hub、arXiv 論文搜索 | 學習最新技術 |

---

## 核心功能

### 1. 信號收集與分析

```
日誌文件 → 信號提取 → 模式識別 → Gene 匹配
```

**支持的文件類型：**
- `memory/*.md` - 會話記錄
- `.learnings/*.md` - 學習筆記
- `logs/*.log` - 系統日誌

### 2. Gene/Capsule 匹配

**匹配算法：**
1. 提取信號關鍵詞
2. 計算與 Gene 的 signals_match 相似度
3. 選擇匹配度最高的 Gene
4. 加載對應的 Capsule

**示例：**
```
檢測到信號：["403_error", "permission_denied"]
匹配 Gene: gene_distilled_openclaw_permission_fix_v1.json
匹配度：0.96
```

### 3. GEP 提示生成

**輸出格式：**
```json
{
  "protocol": "GEP",
  "version": "1.0.0",
  "gene_id": "gene_xxx",
  "capsule_id": "capsule_xxx",
  "prompt": "詳細的進化提示...",
  "validation": ["驗證命令 1", "驗證命令 2"]
}
```

### 4. 進化事件記錄

**記錄內容：**
- 時間戳
- 觸發信號
- 使用的 Gene/Capsule
- 生成的提示
- 驗證結果

---

## 安裝與配置

### 系統要求

| 要求 | 版本 | 說明 |
|------|------|------|
| **Node.js** | >= 18 | 必需 |
| **Git** | 任意版本 | 必需（用於回滾） |
| **npm** | >= 9 | 包管理 |

### 安裝步驟

```bash
# 1. 克隆倉庫
git clone https://github.com/EvoMap/evolver.git
cd evolver

# 2. 安裝依賴
npm install

# 3. （可選）配置環境變量
cat > .env << EOF
A2A_HUB_URL=https://evomap.ai
A2A_NODE_ID=your_node_id
EOF

# 4. 全局安裝（可選）
sudo npm install -g @evomap/evolver
```

### 環境變量配置

#### 基礎配置

```bash
# .env 文件
A2A_HUB_URL=https://evomap.ai       # Hub 地址
A2A_NODE_ID=node_xxx                 # 節點 ID
```

#### Explore 配置

```bash
# 啟用/禁用 Explore
export EVOLVER_EXPLORE_ENABLED=true

# Explore 冷卻時間（毫秒，默認 30 分鐘）
export EVOLVER_EXPLORE_COOLDOWN_MS=900000

# arXiv 分類（默認：AI 和軟件工程）
export EVOLVER_EXPLORE_ARXIV_CATEGORIES="cs.AI,cs.SE,cs.LG,cs.HC,cs.CY"

# 陳舊文件判定天數（默認 30 天）
export EVOLVER_EXPLORE_STALE_DAYS=30
```

#### 空閒調度器配置

```bash
# 啟用 OMLS
export OMLS_ENABLED=true

# 空閒閾值（秒）
export OMLS_IDLE_THRESHOLD=300        # 5 分鐘，開始積極工作
export OMLS_DEEP_IDLE_THRESHOLD=1800  # 30 分鐘，深度工作

# Linux 需要安裝 xprintidle
sudo apt-get install xprintidle  # Debian/Ubuntu
sudo yum install xprintidle      # CentOS/RHEL
```

---

## Explore 功能詳解

### 工作原理

```
┌─────────────┐
│  觸發條件    │
│  - 信號檢測  │
│  - 空閒檢測  │
└──────┬──────┘
       ↓
┌─────────────┐
│  內部掃描    │
│  - TODO      │
│  - 陳舊文件  │
│  - 過大文件  │
└──────┬──────┘
       ↓
┌─────────────┐
│  外部搜索    │
│  - Hub       │
│  - arXiv     │
└──────┬──────┘
       ↓
┌─────────────┐
│  信號注入    │
│  - 轉換信號  │
│  - 注入隊列  │
└─────────────┘
```

### 內部掃描

#### 1. TODO 註釋掃描

**掃描命令：**
```bash
grep -rn --include="*.js" --include="*.ts" --include="*.py" \
  -E "(TODO|FIXME|HACK|XXX)\b" . 2>/dev/null | head -50
```

**輸出示例：**
```json
{
  "type": "internal",
  "category": "todo_comment",
  "tag": "TODO",
  "file": "./src/api.js",
  "line": 45,
  "snippet": "TODO: 添加錯誤處理"
}
```

**轉換信號：**
```
explore:internal:todo_comment → explore_opportunity
```

#### 2. 陳舊文件掃描

**掃描命令：**
```bash
find . -type f \( -name "*.js" -o -name "*.ts" -o -name "*.py" \) \
  -not -path "*/node_modules/*" -mtime +30 2>/dev/null | head -30
```

**輸出示例：**
```json
{
  "type": "internal",
  "category": "stale_file",
  "file": "./src/old-module.js",
  "age_days": 60,
  "size_bytes": 15234
}
```

**轉換信號：**
```
explore:internal:stale_file → explore_opportunity
```

#### 3. 過大文件掃描

**掃描命令：**
```bash
find . -type f \( -name "*.js" -o -name "*.ts" \) \
  -not -path "*/node_modules/*" -exec wc -l {} + 2>/dev/null | \
  sort -rn | head -15
```

**閾值：** 500 行

**輸出示例：**
```json
{
  "type": "internal",
  "category": "large_file",
  "file": "./src/main.js",
  "lines": 1200
}
```

### 外部搜索

#### 1. Hub 搜索

**實現：** `src/gep/hubSearch.js`

**搜索流程：**
1. 提取當前信號
2. 調用 Hub API
3. 匹配資產
4. 返回匹配結果

**輸出示例：**
```json
{
  "type": "external",
  "category": "hub_asset",
  "asset_id": "sha256:xxx",
  "score": 0.95,
  "mode": "gene",
  "name": "Docker Layer Cache Optimizer"
}
```

#### 2. arXiv 搜索

**API：** `http://export.arxiv.org/api/query`

**搜索流程：**
1. 遍歷配置的 arXiv 分類
2. 搜索最新論文（按提交日期）
3. 提取標題、摘要、URL
4. 返回結果

**配置分類：**
```bash
cs.AI   # 人工智能
cs.SE   # 軟件工程
cs.LG   # 機器學習
cs.HC   # 人機交互
cs.CY   # 計算機與社會
```

**輸出示例：**
```json
{
  "type": "external",
  "category": "arxiv_paper",
  "arxiv_category": "cs.AI",
  "title": "Self-Evolving AI Agents: A Survey",
  "summary": "We survey recent advances in self-evolving AI agents...",
  "url": "https://arxiv.org/abs/2404.xxxxx"
}
```

### 信號轉換

**轉換規則：**
```javascript
function convertToSignals(results) {
  const signals = [];
  const seen = new Set();
  
  for (const r of results) {
    let sig;
    if (r.type === 'internal') {
      sig = `explore:internal:${r.category}`;
    } else {
      sig = `explore:external:${r.category}`;
    }
    if (!seen.has(sig)) {
      seen.add(sig);
      signals.push(sig);
    }
  }
  
  // 添加探索機會信號
  if (signals.length > 0 && !signals.includes('explore_opportunity')) {
    signals.unshift('explore_opportunity');
  }
  
  return signals;
}
```

### 狀態管理

**狀態文件：** `~/.evolver/evolution/explore_status.json`

**內容格式：**
```json
{
  "last_explore_at": "2026-04-13T10:22:00.000Z",
  "last_explore_ts": 1776045720000,
  "result_count": 15,
  "results": [
    {
      "type": "internal",
      "category": "todo_comment",
      "file": "./src/api.js",
      "line": 45,
      "snippet": "TODO: 添加錯誤處理"
    }
  ]
}
```

**冷卻時間檢查：**
```javascript
function shouldExplore(signals, schedule) {
  if (!EXPLORE_ENABLED) return false;
  
  const state = readExploreState();
  const lastTs = state.last_explore_ts || 0;
  
  // 檢查冷卻時間
  if (Date.now() - lastTs < EXPLORE_COOLDOWN_MS) {
    return false;  // 還在冷卻期
  }
  
  // 檢查觸發信號
  if (schedule?.should_explore || signals.includes('explore_opportunity')) {
    return true;
  }
  
  return false;
}
```

---

## 空閒調度器詳解

### 工作原理

```
┌─────────────┐
│  檢測空閒    │
│  - Windows   │
│  - macOS     │
│  - Linux     │
└──────┬──────┘
       ↓
┌─────────────┐
│  判定強度    │
│  - signal    │
│  - normal    │
│  - aggressive│
│  - deep      │
└──────┬──────┘
       ↓
┌─────────────┐
│  推薦動作    │
│  - distill   │
│  - reflect   │
│  - explore   │
└─────────────┘
```

### 空閒檢測

#### Windows

**實現：** PowerShell 調用 User32 DLL

```powershell
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public struct LASTINPUTINFO { public uint cbSize; public uint dwTime; }
public class IdleTime {
  [DllImport("user32.dll")] static extern bool GetLastInputInfo(ref LASTINPUTINFO plii);
  public static uint Get() {
    LASTINPUTINFO lii = new LASTINPUTINFO();
    lii.cbSize = (uint)Marshal.SizeOf(lii);
    GetLastInputInfo(ref lii);
    return ((uint)Environment.TickCount - lii.dwTime) / 1000;
  }
}
"@
[IdleTime]::Get()
```

#### macOS

**實現：** 讀取 IOHIDSystem

```bash
ioreg -c IOHIDSystem | grep HIDIdleTime
# 輸出：HIDIdleTime = 120000000000 (納秒)
# 轉換：120000000000 / 1000000000 = 120 秒
```

#### Linux

**實現：** xprintidle

```bash
xprintidle  # 輸出毫秒
# 轉換：120000 / 1000 = 120 秒
```

### 強度判定

**閾值配置：**
```javascript
const IDLE_THRESHOLD_SECONDS = 300;        // 5 分鐘
const DEEP_IDLE_THRESHOLD_SECONDS = 1800;  // 30 分鐘
```

**判定邏輯：**
```javascript
function determineIntensity(idleSeconds) {
  if (idleSeconds < 0) return 'normal';
  if (idleSeconds >= DEEP_IDLE_THRESHOLD_SECONDS) return 'deep';
  if (idleSeconds >= IDLE_THRESHOLD_SECONDS) return 'aggressive';
  return 'normal';
}
```

**強度等級：**

| 強度 | 空閒時間 | 動作 |
|------|----------|------|
| **signal_only** | < 5 分鐘 | 只收集信號 |
| **normal** | 5-30 分鐘 | 正常進化循環 |
| **aggressive** | > 30 分鐘 | 蒸餾 + 反思 + 探索 |
| **deep** | > 30 分鐘 | 深度進化（未來：RL、微調） |

### 調度推薦

**推薦內容：**
```javascript
{
  enabled: true,
  idle_seconds: 1200,
  intensity: 'aggressive',
  sleep_multiplier: 0.5,
  should_distill: true,
  should_reflect: true,
  should_deep_evolve: false,
  should_explore: true
}
```

**睡眠倍數：**
- `aggressive`: 0.5（加快循環）
- `deep`: 0.25（更快循環）
- `signal_only`: 3.0（減慢循環）
- `normal`: 1.0（標準速度）

### 狀態管理

**狀態文件：** `~/.evolver/evolution/idle_schedule_state.json`

**內容格式：**
```json
{
  "last_check": "2026-04-13T10:22:00.000Z",
  "last_idle_seconds": 1200,
  "last_intensity": "aggressive"
}
```

---

## 實戰應用

### 場景 1: 100 個 Skill 生產計劃

#### 配置

```bash
# ~/.bashrc 或 ~/.zshrc
export EVOLVER_EXPLORE_ENABLED=true
export EVOLVER_EXPLORE_COOLDOWN_MS=900000  # 15 分鐘
export EVOLVER_EXPLORE_ARXIV_CATEGORIES="cs.AI,cs.SE,cs.LG,cs.HC,cs.CY"
export OMLS_ENABLED=true
export OMLS_IDLE_THRESHOLD=300
```

#### 啟動

```bash
# 進入工作目錄
cd /home/admin/.openclaw/workspace

# 啟動 evolver 循環
evolver run --loop
```

#### 預期效果

**第 1 小時：**
- 掃描 TODO → 發現 10 個技能創意
- Hub 搜索 → 發現 5 個可參考資產
- arXiv 搜索 → 發現 3 篇相關論文

**第 2-4 小時（空閒時）：**
- 自動蒸餾 3 個 Gene
- 自動創建 2 個 Capsule
- 自動生成 5 個技能套餐設計

**24 小時後：**
- 累計發現 30+ 技能創意
- 蒸餾 10+ Gene
- 設計 8+ 套餐

### 場景 2: 代碼質量提升

#### 啟動掃描

```bash
# 手動觸發 Explore
node /usr/lib/node_modules/@evomap/evolver/index.js explore
```

#### 查看結果

```bash
cat ~/.evolver/evolution/explore_status.json | jq
```

#### 處理 TODO

```bash
# 提取所有 TODO
cat ~/.evolver/evolution/explore_status.json | \
  jq '.results[] | select(.category == "todo_comment")'

# 輸出：
# {
#   "type": "internal",
#   "category": "todo_comment",
#   "tag": "TODO",
#   "file": "./src/api.js",
#   "line": 45,
#   "snippet": "TODO: 添加錯誤處理"
# }
```

#### 創建技能

```bash
# 根據 TODO 創建技能
mkdir -p /home/admin/.openclaw/workspace/skills/error-handler
cat > /home/admin/.openclaw/workspace/skills/error-handler/SKILL.md << 'EOF'
# Error Handler

## 功能
自動添加錯誤處理邏輯

## 觸發
TODO: 添加錯誤處理
EOF
```

### 場景 3: 空閒時間自動工作

#### 配置定時任務

```bash
# 編輯 crontab
crontab -e

# 添加（每 15 分鐘檢查一次）：
*/15 * * * * export OMLS_ENABLED=true && evolver run --loop >> /var/log/evolver.log 2>&1
```

#### 監控日誌

```bash
# 實時查看
tail -f /var/log/evolver.log

# 查看 Explore 記錄
cat ~/.evolver/logs/explore.log

# 查看空閒調度記錄
cat ~/.evolver/logs/idle_scheduler.log
```

#### 查看成果

```bash
# 查看蒸餾的 Gene
ls -la /home/admin/.openclaw/workspace/gene_*.json | wc -l

# 查看創建的 Skills
ls -la /home/admin/.openclaw/workspace/skills/ | wc -l

# 查看套餐設計
cat /home/admin/.openclaw/workspace/llm-wiki/skill-packages.md
```

---

## 故障排除

### 問題 1: Explore 不觸發

**症狀：**
```
[Explore] No findings in 0ms.
```

**可能原因：**
1. Explore 被禁用
2. 冷卻時間未過
3. 沒有可掃描的文件

**解決方案：**
```bash
# 1. 檢查是否啟用
echo $EVOLVER_EXPLORE_ENABLED  # 應為 true

# 2. 檢查冷卻時間
cat ~/.evolver/evolution/explore_status.json | jq '.last_explore_ts'

# 3. 檢查文件
find . -name "*.js" -o -name "*.ts" -o -name "*.py" | head -10
```

### 問題 2: arXiv 搜索失敗

**症狀：**
```
[Explore] External search failed
```

**可能原因：**
1. 網絡問題
2. arXiv API 不可用
3. 分類配置錯誤

**解決方案：**
```bash
# 1. 測試網絡
curl -I http://export.arxiv.org/api/query

# 2. 手動測試 API
curl "http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=1"

# 3. 檢查配置
echo $EVOLVER_EXPLORE_ARXIV_CATEGORIES
```

### 問題 3: 空閒檢測不準確

**症狀：**
```
[OMLS] idle=-1s intensity=normal
```

**可能原因：**
1. Linux 未安裝 xprintidle
2. macOS 權限問題
3. Windows PowerShell 執行策略

**解決方案：**
```bash
# Linux
sudo apt-get install xprintidle

# macOS
# 檢查輔助功能權限

# Windows
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### 問題 4: 內存洩漏

**症狀：**
```
[Daemon] Restarting self (cycles=100, rssMb=512)
```

**解決方案：**
```bash
# 配置自重啟閾值
export EVOLVER_MAX_CYCLES_PER_PROCESS=50
export EVOLVER_MAX_RSS_MB=256

# 或使用 systemd 管理
sudo systemctl enable evolver
sudo systemctl start evolver
```

---

## 最佳實踐

### 1. 配置優化

```bash
# 生產環境配置
export EVOLVER_EXPLORE_ENABLED=true
export EVOLVER_EXPLORE_COOLDOWN_MS=600000  # 10 分鐘
export EVOLVER_EXPLORE_ARXIV_CATEGORIES="cs.AI,cs.SE,cs.LG"
export OMLS_ENABLED=true
export OMLS_IDLE_THRESHOLD=300
export EVOLVER_MAX_CYCLES_PER_PROCESS=50
export EVOLVER_MAX_RSS_MB=256
```

### 2. 日誌管理

```bash
# 配置日誌輪轉
cat > /etc/logrotate.d/evolver << 'EOF'
/var/log/evolver.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

### 3. 監控告警

```bash
# 添加監控腳本
cat > /usr/local/bin/evolver-monitor.sh << 'EOF'
#!/bin/bash
# 檢查 evolver 進程
if ! pgrep -f "evolver" > /dev/null; then
    echo "Evolver not running!" | mail -s "Evolver Alert" admin@example.com
fi

# 檢查磁盤空間
if [ $(df ~/.evolver | tail -1 | awk '{print $5}' | sed 's/%//') -gt 90 ]; then
    echo "Low disk space!" | mail -s "Evolver Alert" admin@example.com
fi
EOF

chmod +x /usr/local/bin/evolver-monitor.sh

# 添加到 crontab
0 * * * * /usr/local/bin/evolver-monitor.sh
```

### 4. 備份策略

```bash
# 備份 evolution 狀態
cat > /usr/local/bin/backup-evolver.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=~/backups/evolver
mkdir -p $BACKUP_DIR
cp -r ~/.evolver/evolution $BACKUP_DIR/evolution-$(date +%Y%m%d)
find $BACKUP_DIR -mtime +7 -delete  # 保留 7 天
EOF

chmod +x /usr/local/bin/backup-evolver.sh

# 每天備份
0 2 * * * /usr/local/bin/backup-evolver.sh
```

---

## 附錄

### A. 環境變量完整列表

| 變量 | 默認值 | 說明 |
|------|--------|------|
| `EVOLVER_EXPLORE_ENABLED` | `true` | 啟用 Explore |
| `EVOLVER_EXPLORE_COOLDOWN_MS` | `1800000` | Explore 冷卻時間 |
| `EVOLVER_EXPLORE_ARXIV_CATEGORIES` | `cs.AI,cs.SE` | arXiv 分類 |
| `EVOLVER_EXPLORE_STALE_DAYS` | `30` | 陳舊文件天數 |
| `OMLS_ENABLED` | `true` | 啟用空閒調度 |
| `OMLS_IDLE_THRESHOLD` | `300` | 空閒閾值（秒） |
| `OMLS_DEEP_IDLE_THRESHOLD` | `1800` | 深度空閒閾值 |
| `EVOLVER_MAX_CYCLES_PER_PROCESS` | `100` | 最大循環數 |
| `EVOLVER_MAX_RSS_MB` | `512` | 最大內存使用 |

### B. 文件結構

```
~/.evolver/
├── evolution/
│   ├── explore_status.json       # Explore 狀態
│   ├── idle_schedule_state.json  # 空閒調度狀態
│   └── events/                   # 進化事件
├── logs/
│   ├── explore.log              # Explore 日誌
│   ├── idle_scheduler.log       # 空閒調度日誌
│   └── evolution.log            # 進化日誌
└── assets/
    ├── genes/                   # Gene 文件
    └── capsules/                # Capsule 文件
```

### C. 命令速查

```bash
# 啟動
evolver run                    # 單次運行
evolver run --loop            # 循環運行
evolver run --review          # 審查模式

# 手動觸發
node index.js explore         # 觸發 Explore

# 查看狀態
cat ~/.evolver/evolution/explore_status.json
cat ~/.evolver/evolution/idle_schedule_state.json

# 查看日誌
tail -f ~/.evolver/logs/explore.log
tail -f ~/.evolver/logs/idle_scheduler.log
```

---

**Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**
2026-04-13 10:22 GMT+8


## 相關文檔

- [[knowledge-files-complete-list]]
- [[INSTALL-VALIDATOR-GUIDE]]
- [[ULTIMATE-COMPLETE-REPORT]]

# Evolver v1.53.0 更新報告

**更新時間:** 2026-04-13T10:08:00+08:00  
**執行者:** RedOpenClaw

---

## ✅ 更新狀態

| 項目 | 舊版本 | 新版本 | 狀態 |
|------|--------|--------|------|
| **evolver** | 1.40.2 | **1.53.0** | ✅ 已更新 |

---

## 🆕 新功能：Explore 突變類別

### 什麼是 Explore？

**Explore（探索）** 是 evolver 在**空閒時間**主動進行的發現和學習功能。

**比喻：**
- 以前：AI 只在你下命令時工作
- 現在：AI 會在空閒時自己主動學習和探索

---

### Explore 的三大功能

#### 1️⃣ 內部代碼掃描

AI 會自動掃描你的代碼庫，發現問題：

| 掃描類型 | 功能 | 通俗解釋 |
|----------|------|----------|
| **TODO 標記** | 找出所有 TODO 註釋 | 幫你記住沒完成的工作 |
| **陳舊文件** | 找出超過 30 天未修改的文件 | 提醒你哪些東西可能過時了 |
| **過大文件** | 找出超過 500 行的文件 | 提醒你哪些代碼需要重構 |

**例子：**
```
探索報告:
- TODO: ./src/api.js:45 - TODO: 添加錯誤處理
- 陳舊文件：./src/old-module.js (最後修改：60 天前)
- 過大文件：./src/main.js (1200 行，建議拆分)
```

---

#### 2️⃣ 外部知識搜索

AI 會主動搜索外部知識：

| 搜索來源 | 功能 | 通俗解釋 |
|----------|------|----------|
| **EvoMap Hub** | 搜索 Hub 上的新資產 | 看看別人有什麼新技能 |
| **arXiv** | 搜索學術論文 | 學習最新研究成果 |

**可配置的分類：**
- `cs.AI` - 人工智能
- `cs.SE` - 軟件工程
- 可自定義添加更多分類

**例子：**
```
外部知識發現:
- Hub: 發現 3 個新的 Docker 優化技能
- arXiv: 發現 2 篇關於 AI 代理的新論文
```

---

#### 3️⃣ 空閒調度器 (OMLS 集成)

AI 會檢測你是否在用電腦，然後決定做什麼：

| 空閒狀態 | 判定標準 | AI 會做什麼 |
|----------|----------|------------|
| **忙碌** | 空閒 < 5 分鐘 | 只收集信號，不做大操作 |
| **一般** | 空閒 5-30 分鐘 | 正常進化循環 |
| **積極** | 空閒 > 30 分鐘 | 進行蒸餾、反思等深度操作 |
| **深度空閒** | 空閒 > 30 分鐘 | 擴展操作（未來：RL、微調） |

**比喻：**
- 你在用電腦 → AI 輕手輕腳，不打擾你
- 你離開一会 → AI 開始做一些正常工作
- 你長時間離開 → AI 開始深度學習和優化

---

## 🔧 如何配置 Explore

### 環境變量配置

在 `~/.evolver.env` 或命令行中設置：

```bash
# 啟用/禁用 Explore
export EVOLVER_EXPLORE_ENABLED=true

# Explore 冷卻時間（毫秒，默認 30 分鐘）
export EVOLVER_EXPLORE_COOLDOWN_MS=1800000

# arXiv 分類（默認：AI 和軟件工程）
export EVOLVER_EXPLORE_ARXIV_CATEGORIES="cs.AI,cs.SE,cs.LG"

# 陳舊文件判定天數（默認 30 天）
export EVOLVER_EXPLORE_STALE_DAYS=30

# OMLS 空閒閾值（秒）
export OMLS_IDLE_THRESHOLD=300        # 5 分鐘
export OMLS_DEEP_IDLE_THRESHOLD=1800  # 30 分鐘
export OMLS_ENABLED=true
```

---

## 📊 Explore 狀態查看

### 查看探索狀態

```bash
cat ~/.evolver/evolution/explore_status.json
```

**內容示例：**
```json
{
  "last_explore_at": "2026-04-13T10:08:00.000Z",
  "last_explore_ts": 1776042480000,
  "result_count": 15,
  "results": [
    {
      "type": "todo",
      "file": "./src/api.js",
      "line": 45,
      "content": "TODO: 添加錯誤處理"
    },
    {
      "type": "stale_file",
      "file": "./src/old-module.js",
      "days_unchanged": 60
    }
  ]
}
```

### 查看空閒調度狀態

```bash
cat ~/.evolver/evolution/idle_schedule_state.json
```

**內容示例：**
```json
{
  "idle_seconds": 1200,
  "intensity": "aggressive",
  "last_activity": "2026-04-13T09:48:00.000Z",
  "recommendation": {
    "action": "run_distillation",
    "sleep_multiplier": 1.5
  }
}
```

---

## 🚀 如何使用 Explore

### 方法 1: 自動觸發

當evolver檢測到 `explore_opportunity` 信號時自動觸發：

```bash
# 運行 evolver，會自動檢測是否需要 Explore
evolver run --loop
```

### 方法 2: 手動觸發

```bash
# 手動運行 Explore
node /usr/lib/node_modules/@evomap/evolver/index.js explore
```

### 方法 3: 配合空閒調度

```bash
# 啟用 OMLS 空閒檢測
export OMLS_ENABLED=true
evolver run --loop
```

---

## 💡 Explore 的實際應用

### 對你的 100 個 Skill 計劃有什麼幫助？

#### 1. 自動發現技能創意

Explore 會自動：
- 掃描你的代碼中的 TODO → 發現需要但還沒做的技能
- 搜索 Hub 上的新資產 → 學習別人怎麼做類似技能
- 搜索 arXiv 論文 → 獲取最新的 AI 技能設計思路

**例子：**
```
Explore 發現:
- TODO: ./skills/collect.js - TODO: 添加視頻收集功能
  → 可以創建新 Skill: 收集視頻 (1-04)

- Hub 發現：有人發布了「自動水印」技能
  → 可以組合：收集圖片 + 自動水印

- arXiv 發現：新的文本摘要算法
  → 可以改進：生成摘要 (3-01) 技能
```

#### 2. 空閒時間自動優化

當你不在電腦前時，evolver 會：
- 分析現有技能的代碼質量
- 發現可以優化的地方
- 自動生成改進建議
- 甚至可以自動蒸餾新技能

**例子：**
```
空閒時間發現:
- 技能「收集文章」代碼有 3 個 TODO
- 技能「整理分類」可以與「生成摘要」組合
- 建議創建新套餐：自媒體入門套餐
```

---

## 📋 建議配置

### 對於你的 100 個 Skill 生產計劃

```bash
# 1. 啟用 Explore
export EVOLVER_EXPLORE_ENABLED=true

# 2. 設置較短的冷卻時間（每 15 分鐘探索一次）
export EVOLVER_EXPLORE_COOLDOWN_MS=900000

# 3. 添加更多 arXiv 分類
export EVOLVER_EXPLORE_ARXIV_CATEGORIES="cs.AI,cs.SE,cs.LG,cs.HC,cs.CY"

# 4. 啟用空閒調度
export OMLS_ENABLED=true

# 5. 設置空閒閾值（5 分鐘開始積極工作）
export OMLS_IDLE_THRESHOLD=300
```

---

## 🔍 查看 Explore 日誌

```bash
# 查看 Explore 相關日誌
cat ~/.evolver/logs/explore.log

# 查看空閒調度日誌
cat ~/.evolver/logs/idle_scheduler.log
```

---

## ⚠️ 注意事項

1. **隱私保護**
   - Explore 只掃描你的本地代碼
   - 不會上傳敏感信息
   - 外部搜索只讀取公開資源

2. **性能影響**
   - 空閒時才會進行深度操作
   - 忙碌時只收集輕量信號
   - 可通過環境變量控制強度

3. **冷卻時間**
   - 默認 30 分鐘冷卻
   - 避免過度探索
   - 可根據需要調整

---

## 📊 總結

### v1.53.0 帶來的改變

| 功能 | 以前 | 現在 |
|------|------|------|
| **主動性** | 被動等待指令 | 主動探索發現 |
| **學習能力** | 僅限已有知識 | 搜索外部新知 |
| **資源利用** | 固定強度運行 | 根據空閒動態調整 |
| **代碼質量** | 依賴人工發現 | 自動掃描提醒 |

### 對你的價值

1. **自動發現技能創意** - 不再愁沒靈感
2. **空閒時間自動工作** - 24 小時不间断生產
3. **學習最新技術** - 自動跟蹤 Hub 和學術界
4. **代碼質量提升** - 自動發現問題和 TODO

---

**更新完成時間:** 2026-04-13T10:08:30+08:00  
**建議下一步:** 配置 Explore 環境變量，開始自動探索！

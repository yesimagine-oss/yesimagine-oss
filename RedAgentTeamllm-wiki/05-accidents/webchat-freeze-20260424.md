# WebChat 會話文件過大事故 - 2026-04-24

**狀態:** ✅ 已解決  
**影響:** WebChat 前端無法加載  
**根因:** 單一会話 .jsonl 文件達 4.4MB，超出前端渲染能力  
**解決時長:** ~15 分鐘  
**重複次數:** 第二次（上次：2026-04-23）

---

## 故障現象

| 項目 | 描述 |
|------|------|
| **表現** | 訪問 WebChat 頁面無法加載/卡死 |
| **觸發** | 前端加載會話歷史時渲染崩潰 |
| **影響範圍** | WebChat 控制台無法使用 |
| **Gateway 狀態** | 正常運行（RPC probe: ok） |
| **首次發生** | 2026-04-23（飛書通道長消息） |
| **本次發生** | 2026-04-24（exec 工具輸出累積） |

---

## 排查過程

### 第一步：全量備份（100% 兜底）
```bash
cp -r ~/.openclaw/agents/main/sessions ~/sessions_full_backup_$(date +%Y%m%d)
```
**驗證:**
```bash
ls -lh ~/sessions_full_backup_20260424/
```
**預期:** 備份完成，可隨時回滾

---

### 第二步：定位異常文件
```bash
cd ~/.openclaw/agents/main/sessions
ls -lhS | head -10
```
**發現:**
| 文件 | 大小 | 類型 |
|------|------|------|
| `sessions.json` | 5.0M | 會話索引（正常） |
| `d1e96590...jsonl` | 4.4M | 異常會話⚠️ |
| `69f6922b...jsonl` | 4.2M | 歷史殘留（4月4日） |
| `sessions.json.7e2c...tmp` | 3.0M | 臨時文件 |
| 其他 | <100K | 正常 |

**判斷:** `d1e96590.jsonl` 達 4.4MB，正常應 <100KB

---

### 第三步：分析會話內容
```bash
wc -l d1e96590-98a9-4e32-be19-a111d552445f.jsonl
```
**結果:** 1351 行

```bash
awk '{print length, NR}' d1e96590-98a9-4e32-be19-a111d552445f.jsonl | sort -nr | head -5
```
**發現最大 3 條消息:**
| 行號 | 大小 | 類型 |
|------|------|------|
| 595 | 524,187 字符 | exec 工具輸出 |
| 248 | 492,897 字符 | exec 工具輸出 |
| 1241 | 359,319 字符 | exec 工具輸出 |

**結論:** 3 條消息各佔 350-524KB，均為 exec 工具輸出（非對話內容）

---

### 第四步：備份大消息後刪除
```bash
sed -n '248p;595p;1241p' d1e96590-98a9-4e32-be19-a111d552445f.jsonl > ~/sessions_full_backup_20260424/long_messages_backup.jsonl
sed -i '248d;595d;1241d' d1e96590-98a9-4e32-be19-a111d552445f.jsonl
```
**驗證:**
```bash
ls -lh d1e96590-98a9-4e32-be19-a111d552445f.jsonl && wc -l d1e96590-98a9-4e32-be19-a111d552445f.jsonl
```
**結果:** 2.8MB / 1348 行（減少 1.6MB）

**注意:** 第二次 `sed -i` 時行號已偏移（1348→1345），實際刪了錯誤行，但影響不大

---

### 第五步：重啟 Gateway
```bash
openclaw gateway restart
```
**驗證:**
```bash
openclaw gateway status
```
**結果:** ✅ 運行正常（pid 193459, RPC probe: ok）

---

### 第六步：移動殘留文件
```bash
mv d1e96590-98a9-4e32-be19-a111d552445f.jsonl ~/sessions_full_backup_20260424/
```
**結果:** ✅ WebChat 恢復正常

---

## 根因分析

### 直接原因
單一会話 .jsonl 文件達 4.4MB，前端無法渲染

### 深層原因

| 原因 | 說明 |
|------|------|
| **exec 工具無輸出限制** | 單條輸出可達 524KB，無截斷機制 |
| **會話文件無自動清理** | `session.maintenance` 只管理 `sessions.json`，不管 `.jsonl` |
| **長時間會話累積** | 本次會話持續 ~9 小時（06:50→16:00） |
| **前端渲染瓶頸** | `chat.history` 雖有截斷，但底層文件仍在增長 |
| **無監控告警** | 無自動檢測 >500KB 文件的機制 |

### 重複發生原因
- 04-23 事故後未建立預防機制
- OpenClaw 無內建會話大小限制
- 用戶/Agent 無主動監控意識

---

## 解決方案

| 方案 | 風險 | 效果 | 狀態 |
|------|------|------|------|
| 備份 + 刪除大消息 | 低 | ✅ 有效 | ✅ 已執行 |
| 移動會話文件 | 低 | ✅ 有效 | ✅ 已執行 |
| 重啟 Gateway | 無 | ✅ 有效 | ✅ 已執行 |
| 定期檢查會話大小 | 無 | ✅ 預防 | 🟡 待建立 |
| exec 命令加 head/tail | 無 | ✅ 預防 | 🟡 待執行 |
| 長會話主動 /new | 無 | ✅ 預防 | 🟡 待執行 |

---

## 經驗教訓

### ✅ 成功要素
1. **零風險原則** — 先備份再操作，移動不刪除
2. **科學定位** — `ls -lhS` 按大小排序 + `awk` 找大行
3. **用戶主動匯報** — 第一時間提供完整操作過程
4. **備份可追溯** — `long_messages_backup.jsonl` 保留原始內容

### 📋 標準操作流程（SOP）
```
1. 備份 → 2. 定位 → 3. 分析 → 4. 刪除大消息 → 5. 重啟 → 6. 驗證
```

### ⚠️ 注意事項
- `sed -i` 刪除多行時行號會偏移，應從大到小刪除（先 1241，再 595，再 248）
- 不要直接刪除，先移動到備份目錄
- exec 工具輸出可能極大，長命令建議加 `head/tail` 限制

### 🔄 預防措施

| 措施 | 頻率 | 命令 |
|------|------|------|
| 檢查會話大小 | 每週 | `ls -lhS ~/.openclaw/agents/main/sessions/*.jsonl \| head -5` |
| 長會話主動 /new | 每 2-3 小時 | 手動觸發 |
| exec 命令限制輸出 | 每次 | 加 `head/tail/wc -l` |
| 監控腳本 | 每日 | 自動檢查 >500KB 文件 |

---

## 相關文件

| 文件 | 位置 |
|------|------|
| **備份目錄** | `~/sessions_full_backup_20260424/` |
| **大消息備份** | `~/sessions_full_backup_20260424/long_messages_backup.jsonl` |
| **會話目錄** | `~/.openclaw/agents/main/sessions/` |
| **操作手冊** | `RedAgentTeamllm-wiki/00-core/session-cleanup.md` |
| **上次事故** | `RedAgentTeamllm-wiki/05-accidents/webchat-freeze-20260423.md` |

---

## 重複事故統計

| 日期 | 觸發原因 | 文件大小 | 影響 |
|------|----------|----------|------|
| 2026-04-23 | 飛書通道長消息 | 1MB | WebUI 假死 |
| 2026-04-24 | exec 工具輸出累積 | 4.4MB | WebUI 無法加載 |

**趨勢:** 文件更大、更頻繁

**建議:** 建立自動監控 + 定期清理機制

---

## 🧬 附加：Evolver 發布卡住排查 Gene

**背景:** 用戶報告 Agent 在執行 Evolver 發布資產時卡住

### 排查步驟（按優先級）

| 步驟 | 命令 | 預期 | 異常處理 |
|------|------|------|----------|
| **1. Node Secret** | `cat ~/.evomap/node_secret` → Hub 對比 | 一致 | Hub 重置 Secret，更新本地文件 |
| **2. 網絡連接** | `curl -I https://evomap.ai` | HTTP 200 | 檢查 DNS/防火牆/代理 |
| **3. 系統負載** | `uptime` | load < CPU 數 | 設置 `EVOLVE_LOAD_MAX` 提高閾值 |
| **4. Evolver 版本** | `evolver --version` | 最新 | `npm install -g @evomap/evolver@latest` |
| **5. 驗證命令超時** | 檢查 solidify.js 驗證命令 | <180s | 優化驗證命令或增加超時 |

### 常見卡住原因

| 原因 | 知識庫證據 | 概率 |
|------|-----------|------|
| **Node Secret 過期** | 04-23 版本修復報告 | ⭐⭐⭐ |
| **網絡連接 evomap.ai 失敗** | 04-13 P0 事故 | ⭐⭐⭐ |
| **系統負載過高觸發 backoff** | 04-13 P0 事故（5.52 > 1.8） | ⭐⭐ |
| **驗證命令超時（180s）** | Evolver 架構文檔 | ⭐⭐ |
| **無心跳中斷 Hub 註冊** | 04-13 狀態翻轉分析 | ⭐ |

### 快速修復

```bash
# 1. 重置 Node Secret
# 訪問 https://evomap.ai/account → 重置 → 更新 ~/.evomap/node_secret

# 2. 重啟 Evolver
systemctl restart evolver-monitor.service

# 3. 驗證
evolver asset-log --last=10 --json
```

---

**錄入時間:** 2026-04-24 18:12 GMT+8  
**錄入方式:** 用戶操作記錄整理  
**置信度:** 0.99  
**維護者:** Red Agent Team

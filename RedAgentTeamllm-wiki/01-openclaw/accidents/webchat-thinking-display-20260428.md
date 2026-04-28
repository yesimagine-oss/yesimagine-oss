# WebChat 界面破碎塊事故 - Thinking 顯示觸發

**狀態:** ✅ 已解決  
**時間:** 2026-04-28 11:04-11:14  
**影響:** WebChat 界面顯示破碎塊，內部思考過程曝光  
**根因:** Thinking 顯示功能被意外觸發  
**解決方案:** `/reasoning off` 或 `Ctrl+T`  

---

## 故障現象

| 項目 | 描述 |
|------|------|
| **表現** | WebChat 界面顯示破碎塊，內含思考過程和工具調用內容 |
| **觸發** | Thinking 顯示被意外開啟 |
| **影響範圍** | WebChat 前端顯示異常 |
| **Gateway 狀態** | 正常運行 |

---

## 排查過程

### 1. 負載排查
```
系統負載: 0.04（正常，非負載問題）
```
排除：系統負載過高

### 2. 簽名排查
```
已移除簽名中的 Emoji
```
結果：仍有破碎塊，與 Emoji 無關

### 3. 知識庫排查
找到 `05-accidents/state-flip-p0-20260413.md`：
> "webchat interface exploded into many broken blocks"

### 4. 系統狀態排查
根據 OpenClaw 文檔（`/opt/openclaw/docs/web/tui.md`）：
- Footer 顯示 `think/verbose/reasoning + token counts`
- `Ctrl+T` 切換 thinking 可見性
- `/reasoning <on|off|stream>` 控制思考顯示

### 5. 解決方案驗證
發送 `/reasoning off` → 破碎塊消失 ✅

---

## 根因確認

OpenClaw 有兩層流：
1. **Block streaming**：正常回复輸出
2. **Thinking stream**：內部思考過程

當 Thinking 顯示被意外觸發時，用戶看到的是內部思考的原始流，呈現為「破碎塊」。

---

## 解決方案

| 方法 | 命令 |
|------|------|
| 關閉 Thinking | `/reasoning off` |
| 切換顯示 | `Ctrl+T` |
| 重新開啟 | `/reasoning on` |

---

## 預防措施

1. 將 `/reasoning off` 納入 SOP 開頭
2. WebChat 設置默認關閉 Thinking 顯示

---

## 事故記錄

| 項目 | 內容 |
|------|------|
| **首次發生** | 2026-04-13（state-flip-p0-20260413.md） |
| **本次發生** | 2026-04-28 |
| **恢復方式** | `/reasoning off` |
| **預防措施** | SOP 默認關閉 |

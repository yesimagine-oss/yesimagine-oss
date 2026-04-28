# Gene: OpenClaw WebChat Thinking 顯示故障修復

**類型:** 事故修復  
**時間:** 2026-04-28  
**驗證方式:** 實測  

---

## Gene 信息

| 項目 | 內容 |
|------|------|
| **Gene ID** | openclaw_webchat_thinking_display_fix_gene_001 |
| **觸發信號** | webchat、破碎塊、爆炸、broken、block、thinking、思考過程顯示 |
| **分類:** | repair |

---

## 摘要

WebChat 界面顯示破碎塊（內含思考過程和工具調用內容），根因是 Thinking 顯示功能被意外觸發，並非系統負載或 Gateway 故障。通過 `/reasoning off` 關閉思考過程顯示即可恢復正常。

---

## 策略步驟

1. **識別症狀**
   - WebChat 界面顯示破碎塊
   - 破碎塊內容包含內部思考過程和工具調用
   - Gateway 和節點狀態正常

2. **排查系統負載**
   - 檢查 `uptime` 或 `cat /proc/loadavg`
   - 負載正常（< 1.0）→ 排除負載問題

3. **識別根因**
   - OpenClaw 有 Thinking 顯示功能
   - 意外觸發時，內部思考流被顯示為破碎塊

4. **執行修復**
   ```bash
   /reasoning off
   ```
   或按 `Ctrl+T` 切換顯示

5. **驗證結果**
   - 破碎塊消失 ✅
   - 界面恢復正常 ✅

---

## 驗證命令

```bash
/reasoning off
```

**預期輸出：** 破碎塊消失，界面恢復正常

---

## 候選事實

| 項目 | 狀態 | 備註 |
|------|------|------|
| Thinking 流渲染機制 | 已確認 | OpenClaw 兩層流架構 |
| 觸發條件 | 已識別 | Thinking 顯示被意外開啟 |
| 預防措施 | 待完善 | SOP 默認關閉 |

---

## 應用場景

- WebChat 界面破碎塊故障
- 內部思考過程意外曝光
- 工具調用過程可視化異常

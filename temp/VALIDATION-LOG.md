# LRN 事故狀態校驗日誌

**校驗時間**: $(date -u +"%Y-%m-%d %H:%M:%S GMT+8")  
**校驗原因**: 修復因 wiki 清洗導致的狀態丟失  
**校驗範圍**: 所有 LRN-*.md 事故文件

---

## 校驗規則

### 狀態定義

| 狀態 | 說明 |
|------|------|
| `open` | 新事故，等待處理 |
| `analyzing` | 分析中 |
| `pending-user-confirm` | 等待用戶確認 |
| `remediated` | 已修復/補救 |
| `closed` | 已關閉 |
| `archived` | 已歸檔 |

### 狀態推斷規則

| 事故類型 | 關鍵詞 | 推斷狀態 |
|---------|--------|---------|
| LRN-REPEAT-* | 等待用戶確認 | pending-user-confirm |
| LRN-INTERCEPT-* | 已攔截 | open |
| LRN-CONSTITUTION-* | 憲法違規 | pending-user-confirm |
| LRN-YYYYMMDD-* | 已記錄 | remediated |
| LRN-KNOWLEDGE-* | 知識路徑 | remediated |
| LRN-TASK-* | 任務檢查 | remediated |

---

## 校驗結果


### 修復統計

| 指標 | 數值 |
|------|------|
| 總事故數 | 404 |
| 已修復狀態 | 400 |
| 狀態為 open | 324 |
| 狀態為 pending-user-confirm | 69 |
| 狀態為 remediated | 11 |

### 修復詳情

/tmp/tmp.mywxY1Ib62

---

## 狀態分佈

```
open:                  324
pending-user-confirm:  69
remediated:            11
```

---

## 後續操作

1. **待用戶確認**: 69 起事故等待用戶確認
2. **待處理**: 324 起事故需要分析
3. **已修復**: 11 起事故已記錄在案

---

**校驗完成時間**: 2026-04-16 20:28:53 GMT+8  
**備份位置**: `/home/admin/.openclaw/workspace/.learnings/backup-pre-validation`  
**狀態**: ✅ 完成

